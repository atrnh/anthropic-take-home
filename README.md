# Claude Docs — audit, standards, and an automated conformance checker

This repository holds a documentation-engineering package for the cross-product
primitives documented on [Claude Docs](https://claude.com/docs): **Skills,
Plugins, and Connectors**. These three are documented by different teams for
different product surfaces, which makes them the place where inconsistency in
the estate is easiest to see and most expensive for readers.

The package has four pieces: an audit of what's wrong today, a standard precise
enough for someone else to enforce, a tool that does the enforcing on the live
corpus, and a plan for getting teams to adopt both without a reporting line.

## What's here

### Audit — `docs/1-audit/`

A memo on the current state of the primitives slice: a prioritized list of what
is wrong and why it matters in that order, what should be deleted or merged
along with the redirect disposition for every affected URL, a proposed
information architecture with a migration path from today's structure, and the
metrics that would show whether any of it worked.

Backed by [`inventory.md`](docs/1-audit/inventory.md), a page-by-page table of
the slice, and by `corpus/` — a pinned snapshot of the live pages so the claims
in the memo can be checked against what was actually on the site.

### Standards — `docs/2-standards/`

A style guide excerpt covering the conventions that address the audit findings.
Rules are written to be conformance-testable, not aspirational: each carries a
stable ID, a rationale, conforming and violating examples, and a note on whether
it can be checked by machine, by a human reviewer, or both.

Alongside it, a content-type template for the type most abused in the slice, and
a before/after rewrite of one real page — the live version, the rewritten
version, and a changelog tying every edit back to the rule ID that required it.

### The checker — `docslint/`

A Python CLI that fetches the docs corpus from
[`llms.txt`](https://claude.com/docs/llms.txt), runs the style guide's rules
against it, and reports findings keyed to those rule IDs. Rules that can be
decided structurally run as deterministic Python; rules that need reading
comprehension run through a Claude-backed judge with a versioned prompt.

`reports/` holds a committed run against the real corpus, so the output is
readable without running anything.
[`docs/3-system/error-analysis.md`](docs/3-system/error-analysis.md) walks
through the cases it got wrong, and
[`docs/3-system/evaluation.md`](docs/3-system/evaluation.md) covers how the
checker itself is measured — the labeled gold set, the false-positive tolerance
and the reasoning behind that number, and what keeps it from going stale.

### Adoption — `docs/4-adoption/`

How the standard and the checker reach teams that don't report to you, and what
happens with the team that ignores both.

## Layout

```
README.md                  this file
docs/
  roadmap.md               deliverable checklist and where each piece lives
  time-log.md              where the hours went
  1-audit/                 audit memo, page inventory, proposed IA
  2-standards/             style guide, content-type template, before/after rewrite
  3-system/                error analysis and evaluation plan for the checker
  4-adoption/              adoption memo
docslint/                  the checker (CLI, rules, judge prompt, gold set)
corpus/                    pinned snapshot of the docs pages under audit
reports/                   committed checker output on the real corpus
transcripts/               Claude sessions and workflows used to build this
```

## Running the checker

```bash
uv run docslint fetch --out corpus/
```

```bash
uv run docslint check corpus/ --report reports/
```

See [`docslint/README.md`](docslint/README.md) for configuration, the rule
catalog, and how to read the output.

## Status

Work in progress. [`docs/roadmap.md`](docs/roadmap.md) tracks which deliverables
are done and which are still outstanding.
