# Claude Docs improvements

Take-home submission for the Technical Documentation and Content Engineer role.
The slice is **Skills, Plugins, and Connectors** across Claude Docs, using a
[54-page snapshot](corpus/manifest.json) fetched on 14 September 2026. Claude Code
and developer-platform documentation are outside this exercise.

## Deliverables

Read the four parts in order, or go straight to the artifact you want to review.

| Part | Start here | Included deliverables |
| --- | --- | --- |
| 1. Audit | [Audit memo](1-audit/README.md) | Prioritized problems, merge/delete decisions and old-URL handling, proposed IA, migration, and measurement. Links to the full disposition ledger and supporting analysis. |
| 2. Standards | [Standards and rewrite](2-standards/README.md) | Style-guide excerpt, how-to template, original page, rewritten Markdown and interactive preview, and an explanation of what changed. |
| 3. System | [Duplicate-prose review workflow](3-check/README.md) | Runnable check, saved corpus output, reviewed mistakes, evaluation targets, and maintenance approach. |
| 4. Adoption | [Adoption approach](4-adoption/README.md) | How to earn adoption across teams, reduce contributor effort, and respond to teams that ignore the standard or check. |

The [GitHub repository](https://github.com/atrnh/anthropic-take-home) contains the
prototype and its saved results. The checker is an advisory prototype; its wider
candidate queue has not been validated for routine editorial use.

## Worked examples and experiments

These READMEs provide the setup and evidence behind Parts 2 and 3:

- [Plugin installation rewrite](2-standards/rewrite/README.md): before, after,
  interactive preview, source decisions, and build instructions.
- [Checker pilot archive](3-check/pilot/README.md): initial findings, false
  positives, evaluation, and plans for detecting degradation.
- [Controlled judge comparisons](3-check/pilot/judge-v2/README.md): prompt
  revisions and comparison with the original judge.
- [Expanded extraction and fresh-case evaluation](3-check/pilot/judge-v5/README.md):
  broader retrieval, repeated judge runs, and review of proposed edits.

## Process, AI use, and time

The [project log](log.md) records the decisions, retrospective, and
[18 exported conversations](log.md#conversation-sources). Exports are redacted
snapshots, not a complete record of every subsequent session. The
[Claude transcript workflow](.claude/skills/dump-transcript/SKILL.md) and
[Codex transcript workflow](.agents/skills/dump-transcript/SKILL.md) are included.

The declared [six-hour checkpoint](log.md#17-september-six-hour-checkpoint) is
17 September 2026 at approximately 10:35 a.m. PDT, measured as human attention.
The audit, standards and rewrite, initial checker experiments, and adoption draft
were present by that checkpoint. Later work includes the controlled judge
refinements, packaged review report, portable rewrite build, revised adoption
response, transcript/log updates, and this repository cleanup. The current checkout includes those later additions.
