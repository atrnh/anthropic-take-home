---
name: dump-transcript
description: Dumps the current Claude Code session transcript into the repo's transcripts/ folder as Markdown.
disable-model-invocation: true
allowed-tools: Bash(python3 .claude/skills/dump-transcript/scripts/dump.py:*)
---

Run:

```bash
python3 .claude/skills/dump-transcript/scripts/dump.py ${CLAUDE_SESSION_ID} $ARGUMENTS
```

The script renders the session to `transcripts/<date>-<session-id-prefix>.md`, overwriting any earlier dump of the same session. The take-home prompt is redacted by default; pass `--keep-prompt` in the arguments to include it. Report the output path and counts it prints. Do not commit unless asked.
