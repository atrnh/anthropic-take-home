# Reconciler prompt (phases 4–5, one agent per task)

Fill in `{TASK_PATH}`, `{UNITS_DIR}`, and `{OUT_PATH}`.

---

You are reconciling every extracted procedure record for one task into a matrix record, and checking that each record really belongs to the task.

Read, in this order:
1. `{SKILL_DIR}/references/schema.md` — dimensions, family/variant rule, outcome rule, diff types.
2. `{SKILL_DIR}/references/taxonomy.yaml` — this task's `outcome` and `view`, the product list, and neighbouring tasks a misfiled record might belong to.
3. `{TASK_PATH}` — JSON with `task_id`, `task`, `outcome`, `view`, `products_in_scope`, and `records` (each with `_unit_id`, `_page`, and evidence).

Source access: the units are in `{UNITS_DIR}/<unit_id>.json` (field `text`). Make targeted reads around each record's `anchor` whenever you decide to merge two records, split them, or judge whether a record meets the task outcome. Do not read whole pages you have no record from. List what you read in `checked`.

Write `{OUT_PATH}` as the per-task matrix record in schema.md.

Rules:
- **Outcome check first.** For each record, ask: after its last step, is the task's `outcome` true? If not, move the record to `misfiled` with the reason and a suggested task ID (or NEW) and exclude it from families and cells. A `partial: true` record for a multi-actor task passes if it is a genuine stage of the path.
- Families = same `surface` + `mechanism`. Within a family, sequential stages of one path become ONE variant with the stages concatenated (summarize a stage as one step if the total would exceed 12). Split into variants only when a reader would follow a different path or a different gate.
- IDs: `P1`, `P2`, … by number of products using the family, then `P1a`, `P1b`, ….
- Keep every source on each variant.
- Fill a cell for every product in `products_in_scope`. No records → `absent`. If only one product documents the task, its cell is `only-here`.
- Diff types are relative to the other documented cells. Use `terminology-only` for name-only differences; do not create a variant for that.
- `summary`: ONE sentence, ≤ 25 words; it is a table cell.
- `open_questions`: things the records and targeted reads could not settle.

Output only the JSON file. Reply with at most two sentences.
