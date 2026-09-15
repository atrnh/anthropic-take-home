# Extraction worker prompt (phase 2)

Fill in `{UNIT_PATH}` and `{OUT_PATH}`. Workers may open sibling units of the same page for context but extract only from their own unit.

---

You are extracting documented procedures from one unit of a documentation corpus.

Read, in this order:
1. `{SKILL_DIR}/references/schema.md` — the five dimensions, the outcome rule, and what counts as a procedure.
2. `{SKILL_DIR}/references/taxonomy.yaml` — task IDs with their outcomes, and product IDs.
3. `{UNIT_PATH}` — JSON with `unit_id`, `page`, `product_default`, `heading_chain`, `sibling_units`, and `text`.

If a passage refers to something "above" or the heading chain is unclear, you may open a sibling unit for context. Extract only what is in your own unit's `text`.

Write `{OUT_PATH}` as JSON:

```json
{
  "unit_id": "...", "page": "...", "product_default": "...",
  "records": [ <extraction records per schema.md> ],
  "no_procedures": false,
  "coverage_notes": "one or two sentences: what this unit covers, anything you deliberately skipped and why"
}
```

Rules:
- One record per (task, product, surface, mechanism, distinct step sequence). If the same steps apply to two products and the page says so, emit two records.
- **Outcome rule.** Before choosing `task_id`, write the record's `outcome` from the text. Pick the task whose taxonomy `outcome` is satisfied when the steps are done. A procedure that only points toward a task (a link, a "see also", a prerequisite) does not belong to it. If no task's outcome fits, use `"NEW"` with a label, outcome, and one-line reason. If it is one stage of a multi-actor task, keep the task and set `partial: true`, `stage_of` to the task ID.
- `product` defaults to `product_default`. Override only when the text names a different product itself ("Claude for Government", "Claude Tag"); Cowork is a mode of `claude`, not a product, and put that phrase in `product_evidence`. A UI label such as "Customize > Skills" is not product evidence.
- `surface` and `mechanism` are separate. An admin clicking in admin settings is `admin-settings` + `click-through`; an admin editing a plist is `filesystem` + `edit-file`.
- `evidence.quote`: ≤ 30 words copied verbatim from inside the procedure; it is grepped. `evidence.anchor`: the nearest heading line above, verbatim with its `#`s.
- Steps ≤ 12, ordered, short imperatives, nothing the text does not state.
- Do not extract concepts, tables, limits, or FAQ answers with no actions.
- If the unit has no procedures, set `no_procedures: true` and `records: []`.

Output only the JSON file. Reply with at most two sentences.
