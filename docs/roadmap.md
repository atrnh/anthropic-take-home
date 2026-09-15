# Roadmap

Audit and improve a slice of [Claude Docs](https://claude.com/docs).
Our chosen slice is **Skills, Plugins, and Connectors**. The separate Claude Code
and developer-platform documentation sites are outside the exercise.

## Drafts available for review

- [Short audit memo](1-audit/README.md), backed by the
  [54-page disposition ledger](1-audit/disposition-ledger.md) and
  [proposed IA and migration](1-audit/proposed-ia.md).
- [Style-guide excerpt](2-standards/style-guide.md),
  [how-to template](2-standards/templates/how-to.md), and
  [worked before/after page](2-standards/rewrite/README.md).
- [Repeated-prose checker, results, and evaluation](3-check/README.md).
  The working prototype finds useful cases but does not meet its proposed
  precision or coverage targets for routine use.
  The [TF-IDF bake-off](3-check/tfidf-bakeoff.md) tests candidate retrieval separately.
  The [editorial judge pilot](3-check/judge-pilot.md) tests classification and
  source-evidence validation on a small sample.

These are drafts, not approved final submission artifacts. The audit proposes
changes against the pinned snapshot; live product checks, rendered-anchor
inventory, and reader validation remain publication work.

## Submission checklist

### 1. Audit

- [ ] Write a short, opinionated memo covering:
  - What is wrong and which improvements matter most.
  - What to delete or merge, and what happens to readers following the old URLs.
  - A proposed information architecture and how to migrate to it.
  - What to measure and how to instrument it to determine whether the changes work.

### 2. Standards

- [ ] Write a style-guide excerpt and one content-type template that address the
  audit findings. Make the rules specific enough to apply consistently.
- [ ] Rewrite one existing page using those standards. Include the original,
  the rewrite, and a note explaining what changed and why.

### 3. Automated check

- [ ] Build a working prototype that flags one class of problem identified in the
  audit, and run it against the live docs or a scrape of them.
- [ ] Provide a GitHub link and the results, including a few cases the check got wrong.
- [ ] Explain how to evaluate the check, the acceptable false-positive rate and
  its rationale, how to detect degradation, and how to keep it current.

### 4. Adoption

- [ ] In a few paragraphs, explain how to get teams to adopt the standards and
  check without authority over them, including how to handle a team that ignores them.

## Time and submission

- Aim for about six hours. If work continues beyond that, identify what existed
  at the six-hour mark and distinguish later additions.
- Prefer depth over breadth. Note unfinished work and proposed next steps.
- Submit the memo as Markdown, PDF, or part of the GitHub submission; include the
  standards, template, and before/after page as Markdown or in the repository.
- Include Claude transcripts, chats, and workflows if Claude is used.
