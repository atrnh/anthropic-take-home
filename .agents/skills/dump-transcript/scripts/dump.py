"""Render a local Codex task transcript to Markdown in transcripts/.

Usage: dump.py SESSION_ID [--keep-prompt] [TITLE]
"""

import json
import os
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
CODEX_HOME = pathlib.Path(os.environ.get("CODEX_HOME", pathlib.Path.home() / ".codex"))
OUT_DIR = REPO / "transcripts"
MAX_RESULT_CHARS = 2000

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
ALLOWED_EMAILS = {"noreply@anthropic.com"}
PROMPT_MARKER = "take-home.md"
PROMPT_NGRAM = 10
WORD = re.compile(r'\\[nrt"\\/]|[A-Za-z0-9]+')
PROMPT_RESULT = "[take-home prompt redacted]"
PROMPT_EXCERPT = "[prompt excerpt redacted]"


def local_file(name: str) -> pathlib.Path:
    own = SKILL_DIR / name
    legacy = REPO / ".claude/skills/dump-transcript" / name
    return own if own.exists() else legacy


def find_transcript(session_id: str) -> pathlib.Path:
    matches = [
        path
        for root in (CODEX_HOME / "sessions", CODEX_HOME / "archived_sessions")
        if root.exists()
        for path in root.rglob(f"*{session_id}.jsonl")
    ]
    if len(matches) != 1:
        detail = "not found" if not matches else f"ambiguous ({len(matches)} matches)"
        sys.exit(f"transcript {detail}: {session_id}")
    return matches[0]


def sensitive_values(records) -> list[str]:
    values = set()
    email = subprocess.run(
        ["git", "config", "user.email"], capture_output=True, text=True, cwd=REPO
    ).stdout.strip()
    denylist = local_file("redact.local")
    extras = denylist.read_text().split() if denylist.exists() else []
    for value in [email, *extras]:
        if not value or value in ALLOWED_EMAILS:
            continue
        values.add(value)
        if "@" in value:
            values.add(value.split("@")[0])
    return sorted((value for value in values if len(value) >= 6), key=len, reverse=True)


def redact(text: str, values: list[str]) -> str:
    for value in values:
        text = text.replace(value, "[redacted]")
    text = EMAIL.sub(lambda match: match.group() if match.group() in ALLOWED_EMAILS else "[email]", text)
    return text.replace(str(pathlib.Path.home()), "~")


def words(text: str) -> list[re.Match]:
    return [match for match in WORD.finditer(text) if not match.group().startswith("\\")]


def ngrams(tokens: list[str]) -> set[tuple[str, ...]]:
    return {tuple(tokens[i : i + PROMPT_NGRAM]) for i in range(len(tokens) - PROMPT_NGRAM + 1)}


def scrub_prompt(text: str, grams: set[tuple[str, ...]]) -> str:
    matches = words(text)
    tokens = [match.group().lower() for match in matches]
    covered = [False] * len(tokens)
    for i in range(len(tokens) - PROMPT_NGRAM + 1):
        if tuple(tokens[i : i + PROMPT_NGRAM]) in grams:
            covered[i : i + PROMPT_NGRAM] = [True] * PROMPT_NGRAM

    spans = []
    i = 0
    while i < len(covered):
        if not covered[i]:
            i += 1
            continue
        end = i
        while end + 1 < len(covered) and covered[end + 1]:
            end += 1
        spans.append((matches[i].start(), matches[end].end()))
        i = end + 1

    for start, end in reversed(spans):
        text = text[:start] + PROMPT_EXCERPT + text[end:]
    return text


def fence(text: str, lang: str = "") -> str:
    ticks = "````" if "```" in text else "```"
    return f"{ticks}{lang}\n{text}\n{ticks}"


def truncate(text: str) -> str:
    if len(text) <= MAX_RESULT_CHARS:
        return text
    return text[:MAX_RESULT_CHARS] + f"\n… [{len(text) - MAX_RESULT_CHARS} chars truncated]"


def block_text(block: dict) -> str:
    return block.get("text", f"[{block.get('type', 'unknown')}]")


def render(records, hidden_results: set[str]) -> tuple[str, int]:
    out = []
    count = 0
    for record in records:
        if record.get("type") != "response_item":
            continue
        item = record.get("payload", {})
        kind = item.get("type")

        if kind == "message" and item.get("role") in ("user", "assistant"):
            metadata = item.get("internal_chat_message_metadata_passthrough", {})
            content = item.get("content", [])
            content_kinds = metadata.get("content_item_kinds", [])
            if item["role"] == "user" and content_kinds:
                content = [block for block, source in zip(content, content_kinds) if source == "user.text"]
            text = "\n".join(block_text(block) for block in content if block.get("type") in ("input_text", "output_text")).strip()
            if not text:
                continue
            count += 1
            role = "User" if item["role"] == "user" else "ChatGPT"
            out.append(f"## {role}\n\n{text}")
        elif kind in ("custom_tool_call", "function_call"):
            raw = item.get("input", item.get("arguments", ""))
            args = raw if isinstance(raw, str) else json.dumps(raw, indent=2, ensure_ascii=False)
            out.append(f"**Tool call — `{item.get('name', 'unknown')}`**\n\n{fence(args)}")
        elif kind in ("custom_tool_call_output", "function_call_output"):
            if item.get("call_id") in hidden_results:
                text = PROMPT_RESULT
            else:
                output = item.get("output", "")
                text = output if isinstance(output, str) else "\n".join(block_text(block) for block in output)
                text = truncate(text.strip())
            out.append(f"<details><summary>Tool result</summary>\n\n{fence(text)}\n\n</details>")
    return "\n\n".join(out), count


def prompt_data(records) -> tuple[set[str], set[tuple[str, ...]]]:
    hidden = set()
    for record in records:
        if record.get("type") != "response_item":
            continue
        item = record.get("payload", {})
        if item.get("type") not in ("custom_tool_call", "function_call"):
            continue
        raw = item.get("input", item.get("arguments", ""))
        if PROMPT_MARKER in (raw if isinstance(raw, str) else json.dumps(raw)):
            hidden.add(item.get("call_id"))

    grams = set()
    prompt = local_file("prompt.local")
    if prompt.exists():
        grams = ngrams([match.group().lower() for match in words(prompt.read_text())])
    return hidden, grams


def main() -> None:
    args = sys.argv[1:]
    keep_prompt = "--keep-prompt" in args
    args = [arg for arg in args if arg != "--keep-prompt"]
    if not args or not args[0]:
        sys.exit("usage: dump.py SESSION_ID [--keep-prompt] [TITLE]")
    session_id, title = args[0], " ".join(args[1:]).strip()

    src = find_transcript(session_id)
    records = [json.loads(line) for line in src.read_text().splitlines() if line.strip()]
    meta = next((record["payload"] for record in records if record.get("type") == "session_meta"), {})
    cwd = pathlib.Path(meta.get("cwd", "/")).resolve()
    if cwd != REPO and REPO not in cwd.parents:
        sys.exit(f"refusing to dump a task from another repository: {cwd}")

    stamps = [record["timestamp"] for record in records if record.get("timestamp")]
    hidden, grams = (set(), set()) if keep_prompt else prompt_data(records)
    body, count = render(records, hidden)
    heading = title or f"Task {session_id[:8]}"
    header = (
        f"# {heading}\n\n- Session: `{session_id}`\n"
        f"- Started: {stamps[0] if stamps else 'unknown'}\n"
        f"- Last activity: {stamps[-1] if stamps else 'unknown'}\n"
    )

    values = sensitive_values(records)
    output = redact(scrub_prompt(f"{header}\n{body}\n", grams), values)
    if any(value in output for value in values):
        sys.exit("refusing to write: identifier survived redaction")
    if grams and ngrams([match.group().lower() for match in words(output)]) & grams:
        sys.exit("refusing to write: take-home prompt text survived redaction")

    OUT_DIR.mkdir(exist_ok=True)
    date = stamps[0][:10] if stamps else "undated"
    dest = OUT_DIR / f"{date}-{session_id[:8]}.md"
    dest.write_text(output)
    prompt_note = "prompt kept" if keep_prompt else f"{len(hidden)} prompt read(s) redacted"
    print(
        f"wrote {dest.relative_to(REPO)} "
        f"({count} messages, {len(values)} identifiers scrubbed, {prompt_note})"
    )


if __name__ == "__main__":
    main()
