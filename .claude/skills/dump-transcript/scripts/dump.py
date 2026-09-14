"""Render a Claude Code session transcript (.jsonl) to Markdown in transcripts/.

Usage: dump.py SESSION_ID [--keep-prompt] [TITLE]

By default the take-home prompt is redacted: tool results that read it are
replaced, and any verbatim run of PROMPT_NGRAM words from it is scrubbed
wherever it appears. --keep-prompt disables this.
"""

import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
PROJECT_DIR = pathlib.Path.home() / ".claude/projects" / re.sub(r"[^A-Za-z0-9]", "-", str(REPO))
OUT_DIR = REPO / "transcripts"
MAX_RESULT_CHARS = 2000

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
ALLOWED_EMAILS = {"noreply@anthropic.com"}
IDENTIFIER_KEYS = ("ownerAccountUuid", "ownerOrganizationUuid", "bridgeSessionId")
# Gitignored, one value per line: identifiers that aren't in the session log or git config.
DENYLIST = SKILL_DIR / "redact.local"

# A tool call whose input mentions this string is treated as reading the prompt.
PROMPT_MARKER = "take-home.md"
# Gitignored copy of the prompt, for sessions that quote it without reading it.
PROMPT_FILE = SKILL_DIR / "prompt.local"
PROMPT_NGRAM = 10
# Word tokens, skipping JSON escape sequences so quoted text matches inside tool args.
WORD = re.compile(r"\\[nrt\"\\/]|[A-Za-z0-9]+")
PROMPT_RESULT = "[take-home prompt redacted]"
PROMPT_EXCERPT = "[prompt excerpt redacted]"


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


def words(text: str) -> list[re.Match]:
    return [m for m in WORD.finditer(text) if not m.group().startswith("\\")]


def ngrams(tokens: list[str]) -> set[tuple[str, ...]]:
    return {tuple(tokens[i : i + PROMPT_NGRAM]) for i in range(len(tokens) - PROMPT_NGRAM + 1)}


def reads_prompt(tool_input: dict) -> bool:
    """True when a path-like input names the prompt file; mentions inside commands or file bodies don't count."""
    return any(isinstance(v, str) and v.rstrip().endswith(PROMPT_MARKER) for v in tool_input.values())


def prompt_reads(records) -> tuple[set[str], list[str]]:
    """Return tool_use ids that read the prompt, and the prompt text they returned."""
    ids = {
        b["id"]
        for rec in records
        if rec.get("type") == "assistant" and isinstance(rec["message"]["content"], list)
        for b in rec["message"]["content"]
        if b["type"] == "tool_use" and reads_prompt(b["input"])
    }
    texts = [
        document_body(result_text(b.get("content", "")))
        for rec in records
        if rec.get("type") == "user" and isinstance(rec["message"]["content"], list)
        for b in rec["message"]["content"]
        if b["type"] == "tool_result" and b.get("tool_use_id") in ids
    ]
    return ids, texts


def document_body(raw: str) -> str:
    """Unwrap JSON read results (e.g. a vault read) to their content field, so metadata like the file path isn't treated as prompt text."""
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    return parsed.get("content", raw) if isinstance(parsed, dict) else raw


def scrub_prompt(text: str, grams: set[tuple[str, ...]]) -> str:
    """Replace every run of words that shares a PROMPT_NGRAM-word window with the prompt."""
    matches = words(text)
    tokens = [m.group().lower() for m in matches]
    covered = [False] * len(tokens)
    for i in range(len(tokens) - PROMPT_NGRAM + 1):
        if tuple(tokens[i : i + PROMPT_NGRAM]) in grams:
            covered[i : i + PROMPT_NGRAM] = [True] * PROMPT_NGRAM

    spans, i = [], 0
    while i < len(covered):
        if covered[i]:
            j = i
            while j + 1 < len(covered) and covered[j + 1]:
                j += 1
            spans.append((matches[i].start(), matches[j].end()))
            i = j + 1
        else:
            i += 1
    for start, end in reversed(spans):
        text = text[:start] + PROMPT_EXCERPT + text[end:]
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


def render(records, hidden_results: set[str]) -> tuple[str, int]:
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
                if b.get("tool_use_id") in hidden_results:
                    text = PROMPT_RESULT
                else:
                    text = truncate(strip_reminders(result_text(b.get("content", ""))))
                label = "Tool error" if b.get("is_error") else "Tool result"
                out.append(f"<details><summary>{label}</summary>\n\n{fence(text)}\n\n</details>")
            # thinking blocks are redacted in the log; skip them.
    return "\n\n".join(out), count


def main() -> None:
    args = sys.argv[1:]
    keep_prompt = "--keep-prompt" in args
    args = [a for a in args if a != "--keep-prompt"]
    if not args or not args[0]:
        sys.exit("usage: dump.py SESSION_ID [--keep-prompt] [TITLE]")
    session_id, title = args[0], " ".join(args[1:]).strip()

    src = PROJECT_DIR / f"{session_id}.jsonl"
    if not src.exists():
        sys.exit(f"transcript not found: {src}")

    records = [json.loads(line) for line in src.read_text().splitlines() if line.strip()]
    stamps = [r["timestamp"] for r in records if "timestamp" in r]
    date = stamps[0][:10] if stamps else "undated"

    hidden, grams = set(), set()
    if not keep_prompt:
        hidden, prompt_texts = prompt_reads(records)
        if PROMPT_FILE.exists():
            prompt_texts.append(PROMPT_FILE.read_text())
        for text in prompt_texts:
            grams |= ngrams([m.group().lower() for m in words(text)])

    body, count = render(records, hidden)
    heading = title or f"Session {session_id[:8]}"
    header = f"# {heading}\n\n- Session: `{session_id}`\n- Started: {stamps[0] if stamps else 'unknown'}\n- Last activity: {stamps[-1] if stamps else 'unknown'}\n"

    values = sensitive_values(records)
    output = redact(scrub_prompt(f"{header}\n{body}\n", grams), values)

    leaks = [v for v in values if v in output]
    if leaks:
        sys.exit(f"refusing to write: {len(leaks)} identifier(s) survived redaction")
    if grams and ngrams([m.group().lower() for m in words(output)]) & grams:
        sys.exit("refusing to write: take-home prompt text survived redaction")

    OUT_DIR.mkdir(exist_ok=True)
    dest = OUT_DIR / f"{date}-{session_id[:8]}.md"
    dest.write_text(output)
    prompt_note = "prompt kept" if keep_prompt else f"{len(hidden)} prompt read(s) redacted"
    print(f"wrote {dest.relative_to(REPO)} ({count} messages, {len(values)} identifiers scrubbed, {prompt_note})")


if __name__ == "__main__":
    main()
