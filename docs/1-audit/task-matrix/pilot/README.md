# Task-matrix pilot (v2)

Second pilot run, 2026-09-14, with the `task-matrix` skill after the schema
revision. Same 11 pages as the first pilot (superseded, not kept), now 14 work
units because the long Microsoft 365 page splits at H3. Opus throughout.

## What changed from v1

| dimension | v1 | v2 |
| --- | --- | --- |
| record dimensions | product, actor, mechanism (surface and mechanism conflated; `admin-console` was both a product and a mechanism) | product, actor, surface, mechanism, outcome, all independent |
| task matching | by label similarity | by **outcome**: a record belongs to a task only if its last step makes the task's outcome true |
| products | 11, including two audience buckets | 6 products; audiences live in `actor`; claude.ai, Desktop, and Cowork are one product |
| views | one table | product view (tasks × products) and builder view (stage × artifact) |
| reconciler source access | none; trusted the records | targeted reads around each record's anchor; 90 reads across 33 tasks |
| gap analysis | rendered `gaps.md` | out of scope |

## Results

| phase | v1 | v2 |
| --- | --- | --- |
| extraction records | 71 accepted, 0 NEW | 79 accepted, 6 NEW |
| product overrides rejected | 0 (1 bad one slipped through) | 0 after adding product `names` to the taxonomy |
| tasks reconciled | 29 | 33 (24 product view, 9 builder view) |
| families / variants | 46 / 67 | 45 / 58 |
| T-019 M365 setup | 6 families, 9 variants | 2 families, 6 variants, stages merged |
| records misfiled by reconcilers | n/a | 2 |
| summary length max | 64 words | 25 words |
| open questions | 55 | 54 |

Outputs: `out/inventory.md`, `out/builder-inventory.md`, `out/appendix.md`.

## What the outcome rule caught

- **plugins/overview "Plugin directory"** now files under T-070 *browse the
  plugin directory* instead of T-033 *install a plugin*. This was the v1
  failure you pointed at.
- **Enterprise role delegation** on the connector submission page came back
  as NEW ("delegate directory management access") because nothing is filed
  after its last step. v1 had it as a variant of *submit a connector*.
- **Entra consent revocation** on the M365 page was misfiled out of
  *manage installed connectors* by the reconciler after a source read: it
  changes tenant-level app consent, not an installed connector's state.
- **"Before uploading" skill validation** was misfiled out of *test a skill*:
  it never gives Claude a matching task, so the skill is never exercised.
  This exposes a taxonomy error, not a worker error; see below.
- **Blocking a connector's own tools** as an end user came back NEW; T-023
  covers admins restricting members, T-008 covers the in-chat card, neither
  covers self-service blocking in Customize > Connectors.

## NEW task candidates (added to the taxonomy as T-074 to T-079)

| candidate | from | proposed view |
| --- | --- | --- |
| delegate directory management access | connectors/building/submission | builder / connector / submit |
| block a connector's individual tools for yourself | connectors/custom/remote-mcp | product |
| troubleshoot missing or incomplete connector search results | connectors/microsoft/365 (2 records) | product |
| troubleshoot a connector that does not appear in the product | third-party m365 part04 | product |
| check plugin submission review status | plugins/submit | builder / plugin / review |
| validate a skill package before upload (from the T-045 misfile) | skills/how-to | builder / skill / test |

## Remaining problems

1. **`claude` vs `claude-web` vs `claude-desktop` vs `cowork`.** Resolved:
   for this corpus they are one product, `claude`, on two clients with an
   optional Cowork mode. The three IDs are gone from the taxonomy; the
   client or mode goes in the record's `notes` when a page names it. Ten
   records were remapped and seven tasks re-reconciled. The audit memo
   should still say the docs do not distinguish web from desktop.
2. **Cross-task overlaps still land in `open_questions`** (T-019 vs T-023 on
   write scopes; T-023 vs T-022). The reconcilers now flag them with source
   evidence, but nothing resolves them. A short pass that reads only the
   `open_questions` and `misfiled` lists from every task file and proposes
   merges or taxonomy edits is the next piece to build.
3. **Multi-actor variants.** `actor` is now a list in the schema, validator,
   and renderer; most pilot matrix files predate that and carry strings,
   which the renderer tolerates.
4. **Builder view cells are sparse** in the pilot because only two builder
   pages were included. Expected; the full corpus has ~20.
5. **`claude-desktop-3p` as a column.** Kept for now to compare against
   `claude`, but it is a deployment of the same product rather than a
   different product. It likely belongs in a third view, deployment ×
   task, the way builder tasks got their own view.
6. **Cost.** 14 extraction + 19 reconcile + 1 taxonomy agent, roughly 3.1M
   tokens. Targeted source reads added ~10k tokens per reconciler and were
   worth it: both misfiles came from them.

## Recommendation

The six NEW tasks are in the taxonomy as T-074 to T-079. Next: run all 54 pages. Build the cross-task pass before rendering the final inventory.
