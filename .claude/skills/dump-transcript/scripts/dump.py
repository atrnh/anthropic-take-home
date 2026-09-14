"""Render a Claude Code session transcript (.jsonl) to Markdown in transcripts/.

Usage: dump.py SESSION_ID [TITLE]
"""

import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
PROJECT_DIR = pathlib.Path.home() / ".claude/projects" / re.sub(r"[^A-Za-z0-9]", "-", str(REPO))
OUT_DIR = REPO / "transcripts"
MAX_RESULT_CHARS = 2000

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
ALLOWED_EMAILS = {"noreply@anthropic.com"}
IDENTIFIER_KEYS = ("ownerAccountUuid", "ownerOrganizationUuid", "bridgeSessionId")
# Gitignored, one value per line: identifiers that aren't in the session log or git config.
DENYLIST = pathlib.Path(__file__).resolve().parents[1] / "redact.local"


def sensitive_values(records) -> list[str]:
    """Identifiers to scrub, read from the session and git config rather than hardcoded.

    Each value is also scrubbed by fragment (UUID first segment, email local part),
    since commands and prose can quote an identifier partially.
    """
    values = set()
    for rec in records:
        for key in IDENTIFIER_KEYS:
            if rec.get(key):
                values.add(rec[key])
                values.add(rec[key].split("-")[0])

    git_email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True, cwd=REPO).stdout.strip()
    extras = DENYLIST.read_text().split() if DENYLIST.exists() else []
    for value in [git_email, *extras]:
        if not value or value in ALLOWED_EMAILS:
            continue
        values.add(value)
        if "@" in value:
            values.add(value.split("@")[0])

    return sorted((v for v in values if len(v) >= 6), key=len, reverse=True)


def redact(text: str, values: list[str]) -> str:
    for value in values:
        text = text.replace(value, "[redacted]")
    text = EMAIL.sub(lambda m: m.group() if m.group() in ALLOWED_EMAILS else "[email]", text)
    return text.replace(str(pathlib.Path.home()), "~")


def strip_reminders(text: str) -> str:
    return re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S).strip()


def fence(text: str, lang: str = "") -> str:
    ticks = "````" if "```" in text else "```"
    return f"{ticks}{lang}\n{text}\n{ticks}"


def truncate(text: str) -> str:
    if len(text) <= MAX_RESULT_CHARS:
        return text
    return text[:MAX_RESULT_CHARS] + f"\n… [{len(text) - MAX_RESULT_CHARS} chars truncated]"


def result_text(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", f"[{b.get('type')}]") for b in content)


def render(records) -> tuple[str, int]:
    out, count = [], 0
    for rec in records:
        if rec.get("type") not in ("user", "assistant") or rec.get("isSidechain"):
            continue
        content = rec["message"]["content"]
        blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content

        for b in blocks:
            kind = b["type"]
            if kind == "text":
                text = strip_reminders(b["text"])
                if not text:
                    continue
                count += 1
                role = "User" if rec["type"] == "user" else "Claude"
                out.append(f"## {role}\n\n{text}")
            elif kind == "tool_use":
                args = json.dumps(b["input"], indent=2, ensure_ascii=False)
                out.append(f"**Tool call — `{b['name']}`**\n\n{fence(args, 'json')}")
            elif kind == "tool_result":
                text = strip_reminders(result_text(b.get("content", "")))
                label = "Tool error" if b.get("is_error") else "Tool result"
                out.append(f"<details><summary>{label}</summary>\n\n{fence(truncate(text))}\n\n</details>")
            # thinking blocks are redacted in the log; skip them.
    return "\n\n".join(out), count


def main() -> None:
    if len(sys.argv) < 2 or not sys.argv[1]:
        sys.exit("usage: dump.py SESSION_ID [TITLE]")
    session_id, title = sys.argv[1], " ".join(sys.argv[2:]).strip()

    src = PROJECT_DIR / f"{session_id}.jsonl"
    if not src.exists():
        sys.exit(f"transcript not found: {src}")

    records = [json.loads(line) for line in src.read_text().splitlines() if line.strip()]
    stamps = [r["timestamp"] for r in records if "timestamp" in r]
    date = stamps[0][:10] if stamps else "undated"

    body, count = render(records)
    heading = title or f"Session {session_id[:8]}"
    header = f"# {heading}\n\n- Session: `{session_id}`\n- Started: {stamps[0] if stamps else 'unknown'}\n- Last activity: {stamps[-1] if stamps else 'unknown'}\n"

    values = sensitive_values(records)
    output = redact(f"{header}\n{body}\n", values)

    leaks = [v for v in values if v in output]
    if leaks:
        sys.exit(f"refusing to write: {len(leaks)} identifier(s) survived redaction")

    OUT_DIR.mkdir(exist_ok=True)
    dest = OUT_DIR / f"{date}-{session_id[:8]}.md"
    dest.write_text(output)
    print(f"wrote {dest.relative_to(REPO)} ({count} messages, {len(values)} identifiers scrubbed)")


if __name__ == "__main__":
    main()
