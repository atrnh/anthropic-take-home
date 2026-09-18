# Task pages with context-dependent instructions

Draft excerpt, demonstrated by the plugin installation rewrite. These rules
address misleading scope, repeated explanations, and workflows scattered across
product sections in the [plugin audit example](../1-audit/plugin-disposition-example.md).

Each rule has an ID that editorial records and review comments can cite. **Check**
says who or what can confirm the rule: a human editor, a machine check, or both.

| Area | Rules |
| --- | --- |
| [Task and scope](#task-and-scope) | TASK-01, SCOPE-01, SCOPE-02 |
| [Procedures](#procedures) | PROC-01, PROC-02, PROC-03 |
| [Interface and navigation](#interface-and-navigation) | UI-01, NAV-01 |
| [Shared content and evidence](#shared-content-and-evidence) | SHARE-01, EVID-01 |

## Task and scope

### TASK-01: Name one reader outcome

Name one reader outcome in the H1. Keep unrelated lifecycle tasks in descriptive
next-step links. Readers need to know when they are done.

- **Do:** Install a plugin; link to updating and removing plugins.
- **Don't:** A page titled Install a plugin that also teaches administration and
  public submission.
- **Check:** Human: identify the outcome of every procedure. Machine: exactly one H1.

### SCOPE-01: Label every variant and source it separately

Give each procedure variant a visible context label and a separate Markdown source.
Document its applicability and evidence in the editorial record. Do not infer
coverage from silence.

- **Do:** Cowork in Claude for Government, with Government source evidence.
- **Don't:** Assume all Desktop users follow the general Cowork procedure.
- **Check:** Human: compare applicability with sources. Machine: check that every
  configured variant has a source file and a rendered label.

### SCOPE-02: Tell readers how to choose

Put a **How to check** explanation beside any setup-dependent chooser. Give an
actionable way to identify the relevant context or ask the responsible person.
Don't use unverified UI labels or classify the reader automatically.

- **Do:** Check your organization's setup instructions; ask your administrator if
  they do not identify the guide.
- **Don't:** Select your inference backend.
- **Check:** Human: follow the identification advice using only facts established
  by sources.

## Procedures

### PROC-01: Make each method complete

Each selectable method must contain the steps required to reach its outcome without
borrowing steps from another variant or method.

- **Do:** Each method begins with opening **Customize**, then **Plugins**.
- **Don't:** Follow the other tab, but skip step 2.
- **Check:** Human: read each method in isolation and trace its outcome.

### PROC-02: Put conditions before the steps they govern

Put permissions, trust conditions, and behavior that could change the reader's
decision before the steps they govern. Distinguish installation from connector
access.

- **Do:** Explain before Government installation that bundled connectors are not
  added.
- **Don't:** Mention after installation that a bundled local MCP server never runs.
- **Check:** Human: locate each condition and the step it affects.

### PROC-03: End with an observable result

End each method with an observable result supported by the source. Do not claim
that installation proves every capability works.

- **Do:** Open the installed plugin to see its components.
- **Don't:** Your team now has access to all connected data.
- **Check:** Human: compare the result with the procedure and source.

## Interface and navigation

### UI-01: Use exact, source-backed UI labels

Use exact, source-backed UI labels in bold and numbered steps for ordered actions.
Flag ambiguous labels in the editorial record rather than inventing precision.

- **Do:** Select **Browse plugins**.
- **Don't:** Click the green Import package button when no source names it.
- **Check:** Human: compare controls and sequence with source.

### NAV-01: Keep links pointed at the right instructions

Variant links must select the named instructions and retain the requested section.
Unknown context must not select a different workflow. No-script and print views
must retain labeled instructions.

- **Do:** `?instructions=government#government-file`.
- **Don't:** An old Government link opens general Cowork instructions.
- **Check:** Browser: direct URLs, unknown values, back/forward, keyboard
  selection, disabled JavaScript, and print.

## Shared content and evidence

### SHARE-01: Give each explanation one home

Keep one canonical explanation for a concept or behavior and link to it from other
pages. Retain local prerequisites, warnings, and brief answers needed to complete
the task. Before consolidating, account for every unique fact and context qualifier
in both passages. Part 3's [duplicate-prose workflow](../3-check/README.md) finds
candidates for this rule.

- **Do:** Link to the plugin definition while keeping Government connector
  restrictions beside installation steps.
- **Don't:** Copy the full definition into each product guide, or remove a local
  prerequisite solely because its wording repeats.
- **Check:** Machine: retrieve overlapping passages for comparison. Human: decide
  whether the reader purpose is shared and whether the proposed home preserves all
  necessary facts.

### EVID-01: Account for everything you remove

Preserve the unmodified before page and record where every removed section goes.
Record source conflicts and unverified assumptions.

- **Do:** Exact before copy, section disposition table, unresolved UI check.
- **Don't:** Delete limits or a unique workflow without recording its destination.
- **Check:** Machine: compare before bytes with pinned source. Human: reconcile all
  original sections.

## What these rules can't establish

These are editorial rules, not a claim that a style checker can establish product
truth. Structural checks can confirm a heading or source file exists; an editor
must verify that the instructions actually apply and produce the stated outcome.
