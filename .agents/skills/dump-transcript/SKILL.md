---
name: dump-transcript
description: Dump the current local Codex or ChatGPT desktop task transcript into this repository's transcripts/ folder as redacted Markdown.
---

Run:

```bash
python3 .agents/skills/dump-transcript/scripts/dump.py "${CODEX_SESSION_ID}"
```

The script renders the local task to `transcripts/<date>-<session-id-prefix>.md`, overwriting any earlier dump of the same task. It includes user and assistant messages plus tool calls and truncated tool results; hidden instructions and reasoning are omitted.

Append `--keep-prompt` when the user asks to include the take-home prompt. Append any requested transcript title after the options. Local redaction values come from this skill's gitignored `prompt.local` and `redact.local`; while migrating from the Claude skill, its matching local files are used as fallbacks.

Report the output path and counts printed by the script. Do not commit unless asked.
