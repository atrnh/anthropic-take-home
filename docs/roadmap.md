# Roadmap

Slice under examination: the cross-product primitives — **Skills, Plugins, and
Connectors**.

## Part 1 — Audit

- [x] Fetch a pinned corpus snapshot of the slice — `corpus/`
- [ ] Build the page inventory table — `docs/1-audit/inventory.md`
- [ ] Write the audit memo — `docs/1-audit/audit-memo.md`
- [ ] Diagram the proposed IA and URL mapping — `docs/1-audit/proposed-ia.md`

## Part 2 — The standards

- [ ] Write the style guide excerpt, with a stable ID per rule —
      `docs/2-standards/style-guide.md`
- [ ] Write the how-to content-type template —
      `docs/2-standards/templates/how-to.md`
- [ ] Explain how authors pick a content type —
      `docs/2-standards/templates/README.md`
- [ ] Capture the unmodified source page — `docs/2-standards/rewrite/before.md`
- [ ] Rewrite the page to the standard — `docs/2-standards/rewrite/after.md`
- [ ] Log each edit against the rule ID that required it —
      `docs/2-standards/rewrite/changelog.md`

## Part 3 — The system

- [ ] Build the checker CLI — `docslint/`
- [ ] Version the Claude judge prompt — `docslint/prompts/`
- [ ] Label the gold-set fixtures and their expected findings —
      `docslint/tests/goldset/`
- [ ] Run the checker on the real corpus and commit the output — `reports/`
- [ ] Diagnose the checker's false positives and negatives —
      `docs/3-system/error-analysis.md`
- [ ] Set precision and recall targets, and justify the false-positive
      tolerance — `docs/3-system/evaluation.md`
- [ ] Wire the checker into CI — `.github/workflows/docslint.yml`
- [ ] Document how to install, run, and read the checker —
      `docslint/README.md`

## Part 4 — Adoption

- [ ] Write the adoption memo — `docs/4-adoption/adoption-memo.md`

## Supporting

- [ ] Write the project README — `README.md`
- [ ] Collect the Claude transcripts and workflows — `transcripts/`
- [ ] Keep the time log, marking the 6-hour line — `docs/time-log.md`

## Sequencing

1. Corpus snapshot — needed by both Part 1 and Part 3.
2. Inventory, then the audit memo and IA.
3. Style guide and template, then the rewrite as proof.
4. Checker against that standard, then the run, error analysis, and evaluation.
5. Adoption memo.
6. README, transcripts, and time log last.

If time runs short, Part 3 ships with fewer rules rather than Parts 1 and 2
shipping thinner.
