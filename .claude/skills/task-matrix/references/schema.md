# Data model

## Five dimensions

Every procedure record is described along five independent dimensions.
Do not collapse them into each other: an admin can use a CLI, a UI can be an
admin console, and the same surface hosts many mechanisms.

| dimension   | question                                  | values                                   |
| ----------- | ----------------------------------------- | ---------------------------------------- |
| `product`   | which product or deployment does this concern? | IDs in `taxonomy.yaml` → `products`  |
| `actor`     | who performs it?                          | list of `end-user`, `admin`, `developer` (a multi-stage path lists each) |
| `surface`   | where do they perform it?                 | enum below                               |
| `mechanism` | how do they perform it?                   | enum below                               |
| `outcome`   | what does completing it accomplish?       | one clause, from the text                |

### surface

| surface             | meaning                                                             |
| ------------------- | ------------------------------------------------------------------- |
| `app-settings`      | the product's own settings / Customize area                         |
| `admin-settings`    | an organization admin area (claude.ai admin settings, Gov Config page, Tag admin) |
| `chat`              | inside a conversation with Claude                                   |
| `terminal`          | a shell                                                             |
| `filesystem`        | files on disk (SKILL.md, settings.json, plist, manifest, .zip)      |
| `web-portal`        | a separate website: Console, submission portal, directory site      |
| `third-party-admin` | another vendor's admin tool (Entra, GitHub settings, Slack admin)   |
| `other`             | explain in `notes`                                                  |

### mechanism

| mechanism        | meaning                                                   |
| ---------------- | --------------------------------------------------------- |
| `click-through`  | navigate and click controls                                |
| `command`        | run a command                                              |
| `edit-file`      | create or edit a file                                      |
| `api-call`       | HTTP or SDK call                                           |
| `prompt-claude`  | ask Claude in natural language to do it                    |
| `request-person` | ask another person (usually an admin) to do it             |
| `other`          | explain in `notes`                                         |

## Entities

**Task** — a reader goal, imperative *verb + object* ("install a plugin").
Product-agnostic. Each task in `taxonomy.yaml` carries an `outcome`: the
state of the world when the task is done ("the plugin is installed and its
components are available to the user in this product"). Tasks also carry a
`view`: `product` or `builder` (see Views).

**Procedure family** — same task, same `surface` + `mechanism`. IDs per
task: `P1`, `P2`, ….

**Variant** — same family, but steps, actor, or preconditions differ enough
that a reader following one would not succeed by following the other. IDs
`P1a`, `P1b`, …. Different wording for the same steps is not a variant; it is
`terminology-only` in the diff.

Sequential **stages** of one path (admin registers app → admin configures
client → user signs in) are ONE variant with the stages concatenated, not one
variant per stage. Split only when a reader would follow a different path.

Worked example, "install a plugin":
- `P1` app-settings / click-through — `P1a` Customize → Plugins → Browse →
  Install (Cowork); `P1b` same but only the Organization tab is available
  (Government). Same surface and mechanism, different precondition → variants.
- `P2` app-settings / click-through, upload path — arguably the same family
  as P1; the reconciler decides by asking whether a reader would treat
  "upload a .zip" and "browse the catalog" as the same path. They would not,
  so it is `P2`.
- Admin allowlists the plugin in admin-settings → not this task at all; its
  outcome is "the plugin is available for members to install", which is
  T-040 "add a plugin for an organization".

## The outcome rule (task matching)

A procedure belongs to a task only if completing the procedure's steps
achieves the task's `outcome`. Test it explicitly:

1. Write the record's `outcome` from the text: what is true after the last step?
2. Compare to the candidate task's `outcome` in the taxonomy.
3. If the procedure only *points toward* the task (a link to a directory, a
   "see also", a prerequisite) it does not belong to that task. Either it
   belongs to a different task whose outcome it does meet, or it is `NEW`, or
   it is not a procedure and should not be extracted.
4. If the procedure is one stage of the task (admin half of a two-actor
   setup) it does belong, with `stage_of` set to the task and `partial: true`.

Wrong: "browse claude.com/plugins" filed under "install a plugin". Nothing
is installed after the last step.

## Views

`taxonomy.yaml` marks each task with a `view`:

- **`product`** — the outcome lands inside a product for its users or admins.
  Rendered as tasks × products in `inventory.md`.
- **`builder`** — the outcome is an artifact or a listing: build, test,
  package, submit, track review, update, delist. Rendered as lifecycle
  `stage` × `artifact` (skill, plugin, connector, mcp-app) in
  `builder-inventory.md`, so shared development and publication workflows
  line up across artifact types. Builder tasks carry `artifact` and `stage`.

The same verb can appear in both views on different tasks: "create a skill
in Customize > Skills" is product; "author a skill package on disk" is builder.

## Source access

Workers extract only from their own unit but MAY open the other parts of the
same page (listed in the unit as `sibling_units`) to resolve a heading chain
or a "see above" reference. Reconcilers work from records but MUST make
targeted reads of the source unit around each record's anchor when deciding
whether to merge two records, whether a record meets the task outcome, or
when two records contradict. Record what you read in `checked`.

## Evidence

Every record carries `anchor` (nearest heading above, verbatim) and `quote`
(≤ 30 words copied exactly from inside the procedure). `validate.py`
normalizes whitespace and backticks and requires the quote to be a substring
of the unit. No quote, no record.

## What counts as a procedure

An ordered set of actions a reader performs to reach an outcome. Concept
descriptions, scope tables, limits, and FAQ answers with no actions are not
procedures. A single sentence "Go to Settings > Connectors and click Add" is.
Troubleshooting entries are procedures for a "troubleshoot X" task only when
they give steps.

## Extraction record

```json
{
  "task_id": "T-004",
  "new_task": null,
  "product": "claude",
  "product_evidence": null,
  "actor": ["end-user"],
  "surface": "app-settings",
  "mechanism": "click-through",
  "outcome": "the remote MCP server is listed as a connector and can be enabled in chats",
  "partial": false,
  "stage_of": null,
  "preconditions": ["Pro, Max, Team, or Enterprise plan"],
  "steps": ["Open Settings > Connectors", "Click Add custom connector", "Paste the server URL", "Click Add"],
  "evidence": {"anchor": "## Add a custom connector", "quote": "Click Add custom connector and paste the remote MCP server URL"},
  "notes": ""
}
```

`new_task` is `{"label": "verb object", "outcome": "…", "why": "…"}` only when
no taxonomy task's outcome is met; then `task_id` is `"NEW"`.
`product_evidence` is required when `product` differs from the unit's default
and must contain the product's name. `steps` ≤ 12, ordered, paraphrased, no
invented steps.

## Per-task matrix record (reconciler output)

```json
{
  "task_id": "T-004",
  "task": "add a custom connector",
  "view": "product",
  "families": [
    {"family_id": "P1", "surface": "app-settings", "mechanism": "click-through", "label": "Add via Settings > Connectors",
     "variants": [
       {"variant_id": "P1a", "label": "Paste URL, OAuth in browser", "actor": ["end-user"],
        "products": ["claude"], "preconditions": ["paid plan"],
        "steps": ["…"], "sources": [{"unit_id": "connectors--custom--remote-mcp", "anchor": "## …"}]}
     ]}
  ],
  "cells": {
    "claude":         {"status": "documented", "variants": ["P1a"], "diff": ["same"], "note": ""},
    "claude-gov":     {"status": "documented", "variants": ["P1b"], "diff": ["precondition-differs"], "note": "admin must allowlist first"},
    "claude-tag":     {"status": "absent", "variants": [], "diff": ["absent"], "note": ""}
  },
  "misfiled": [{"unit_id": "…", "anchor": "…", "reason": "outcome not met: nothing is installed after the last step", "suggest": "T-001 or NEW"}],
  "checked": ["connectors--custom--remote-mcp ## Add a custom connector"],
  "summary": "≤ 25 words.",
  "open_questions": []
}
```

Diff types per cell, relative to the other documented cells for the task:
`same`, `terminology-only`, `steps-differ`, `actor-differs`,
`surface-differs`, `mechanism-differs`, `precondition-differs`, `absent`,
`only-here`. A cell may carry several.
