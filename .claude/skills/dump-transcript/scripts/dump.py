"""Render a Claude Code session transcript (.jsonl) to Markdown in transcripts/.

Usage: dump.py SESSION_ID [TITLE]
"""

import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
PROJECT_DIR = pathlib.Path.home() / ".claude/projects" / re.sub(r"[^A-Za-z0-9]", "-", str(REPO))
OUT_DIR = REPO / "transcripts"
MAX_RESULT_CHARS = 2000

# Account identifiers that shouldn't land in a shared repo.
REDACTIONS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[email]"),
    (re.compile(r"(owner(Account|Organization)Uuid)\W+[0-9a-f-]{36}"), r"\1: [redacted]"),
]


def redact(text: str) -> str:
    for pattern, repl in REDACTIONS:
        text = pattern.sub(repl, text)
    return text


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
    return redact("\n\n".join(out)), count


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

    OUT_DIR.mkdir(exist_ok=True)
    dest = OUT_DIR / f"{date}-{session_id[:8]}.md"
    dest.write_text(f"{header}\n{body}\n")
    print(f"wrote {dest.relative_to(REPO)} ({count} messages)")


if __name__ == "__main__":
    main()
