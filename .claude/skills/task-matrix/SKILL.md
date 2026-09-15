---
name: task-matrix
description: Build a task–procedure–difference matrix from the docs corpus in corpus/. Use when the user asks to inventory documented tasks, compare how a task's procedure differs across products, run the extraction pipeline or its pilot, or regenerate docs/1-audit/inventory.md. Orchestrates parallel Opus extraction workers, deterministic validation, per-task reconciliation, and script-rendered output.
---

# task-matrix

Produces two inventories. The **product view** is tasks × products: each cell
says which procedure variant(s) a product documents for that task and how
they differ. The **builder view** is lifecycle stage × artifact type for
development and publication tasks. Every record is described on five
dimensions: product, actor, surface, mechanism, outcome.
Models emit JSON records; scripts validate, merge, and render. No model ever
writes the final table.

Data model, vocabulary rules, and worker contracts live in `references/`.
Read `references/schema.md` before doing anything else.

## Layout

```
.claude/skills/task-matrix/
  references/schema.md              data model + family/variant rule (read first)
  references/taxonomy.yaml          frozen task + product vocabulary with IDs
  references/extraction-prompt.md   worker contract (phase 2)
  references/reconcile-prompt.md    per-task reconciler contract (phases 4–5)
  scripts/digest.py                 corpus → heading/lede digest for taxonomy seeding
  scripts/split.py                  manifest → work units (chunks long pages at H2)
  scripts/validate.py               schema + evidence-quote check on extractions
  scripts/merge.py                  validated extractions → per-task input bundles
  scripts/render.py                 per-task matrix JSON → inventory.md, builder-inventory.md, appendix.md
```

Working state goes in a workdir (default `docs/1-audit/task-matrix/`):
`units/`, `extractions/`, `validation.json`, `tasks/`, `matrix/`, `out/`.

## Procedure

0. **Prep** — `python3 scripts/split.py --workdir W [--pages a.md b.md ...]`
   writes one JSON per work unit (page, or H2 chunk when the page exceeds
   2,500 words) with a default product inferred from the path.

1. **Taxonomy seed** (once per corpus, one agent) — `python3 scripts/digest.py`
   prints titles, ledes, and headings for every page. Give the digest to one
   Opus agent with `schema.md` and ask for `taxonomy.yaml`. **Stop and have a
   human review it** before extraction; it is the highest-leverage checkpoint.

2. **Extraction** (parallel, one Opus worker per unit) — each worker gets the
   prompt in `extraction-prompt.md` with the unit path filled in. It reads
   `schema.md`, `taxonomy.yaml`, and the unit, then writes
   `W/extractions/<unit_id>.json`. Workers may open sibling units of the
   same page for context but extract only from their own.

3. **Validate** — `python3 scripts/validate.py --workdir W`. Rejects records
   with unknown IDs, bad enums, or evidence quotes that do not appear in the
   unit. Re-run failed units once with the failure text appended to the prompt.

4. **Merge** — `python3 scripts/merge.py --workdir W` groups accepted records
   by task into `W/tasks/<task_id>.json` and lists `NEW:` candidates.

5. **Reconcile + diff** (parallel, one Opus agent per task) — each agent gets
   `reconcile-prompt.md` with its task bundle and the units directory. It
   checks each record against the task's outcome (misfiled records are
   excluded and listed), makes targeted source reads around anchors when
   merging or splitting, assigns family/variant IDs, fills product cells
   with diff types, and writes `W/matrix/<task_id>.json`.

6. **Render** — `python3 scripts/render.py --workdir W` writes
   `W/out/inventory.md`, `W/out/builder-inventory.md`, and `W/out/appendix.md`.
   Gap analysis is out of scope; the audit memo reads the matrix and draws its
   own conclusions.

7. **QA** — re-extract a sample of units with a second worker and compare
   task recall and variant agreement. Record the disagreement rate.

## Rules that keep the output honest

- Task matching is by **outcome**: a record belongs to a task only if its
  last step makes the task's outcome true. Pointers and prerequisites do not
  count. Workers emit `NEW` with a label and outcome when nothing fits.
- `product`, `actor`, `surface`, and `mechanism` are independent. An admin
  console is a surface, not a product and not a mechanism.
- Every record carries a verbatim quote (≤ 30 words) and its heading anchor.
  `validate.py` greps the quote; a miss drops the record.
- Product defaults come from the path. Overriding requires `product_evidence`.
- Family = surface + mechanism; variant = different path or gate. Sequential
  stages of one path are one variant, not several.
