# Technical Docs & Content Engineer, Claude Docs - Take Home

Take-home submission for the Technical Documentation and Content Engineer role.
The slice is **Skills, Plugins, and Connectors** across Claude Docs, using a
[54-page snapshot](corpus/manifest.json) fetched on 14 September 2026. Claude Code
and developer-platform documentation are outside this exercise.

[Open the interactive previews](https://atrnh.github.io/anthropic-take-home/)
for the [worked rewrite](https://atrnh.github.io/anthropic-take-home/rewrite/)
and [review report](https://atrnh.github.io/anthropic-take-home/review/).

## Deliverables

Read the four parts in order, or go straight to the one you want to review. Each
part's README links to its supporting drafts, evidence, and experiments.

| Part | Start here | What's included |
| --- | --- | --- |
| 1️⃣ Audit | [Audit memo](1-audit/README.md) | Prioritized problems, merge and removal decisions with old-URL handling, proposed IA, migration, and measurement. Links to the full disposition ledger and supporting analysis. |
| 2️⃣ Standards | [Standards and worked rewrite](2-standards/README.md) | Style-guide excerpt, how-to template, the original page, the rewritten Markdown and interactive preview, and what changed and why. |
| 3️⃣ System | [Duplicate-prose review workflow](3-check/README.md) | A runnable review queue and report for repeated explanations, the retrieval and model-judgment experiments that shaped it, their limits, and maintenance. The queue is advisory and not yet validated for routine editorial alerts. |
| 4️⃣ Adoption | [Adoption playbook](4-adoption/README.md) | How to earn adoption across teams, lower the cost for contributors, and respond when a team ignores the standard or check. |

## Process, AI use, and time

The [project log](log.md) records the decisions, retrospective, and
[23 exported conversations](log.md#conversation-sources). Exports are redacted
snapshots, not a complete record of every later session. The
[Claude transcript workflow](.claude/skills/dump-transcript/SKILL.md) and
[Codex transcript workflow](.agents/skills/dump-transcript/SKILL.md) that produced
them are included.

The declared [six-hour checkpoint](log.md#17-september-six-hour-checkpoint) is
17 September 2026 at approximately 10:35 a.m. PDT, measured as human attention.
The audit, standards and rewrite, initial checker experiments, and adoption draft
existed by that checkpoint. Everything else is submission cleanup and reviewing/refining
deliverables.
