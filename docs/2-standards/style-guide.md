# Task pages with context-dependent instructions

Draft excerpt, demonstrated by the plugin installation rewrite. These rules
address misleading scope, repeated explanations, and workflows scattered across
product sections in the [plugin audit example](../1-audit/plugin-disposition-example.md).

| ID | Requirement and rationale | Conforming example | Violating example | Check |
| --- | --- | --- | --- | --- |
| TASK-01 | Name one reader outcome in the H1. Keep unrelated lifecycle tasks in descriptive next-step links. Readers need to know when they are done. | Install a plugin; link to updating and removing plugins. | A page titled Install a plugin that also teaches administration and public submission. | Human: identify the outcome of every procedure. Machine: exactly one H1. |
| SCOPE-01 | Give each procedure variant a visible context label and a separate Markdown source. Document its applicability and evidence in the editorial record. Do not infer coverage from silence. | Cowork in Claude for Government, with Government source evidence. | Assume all Desktop users follow the general Cowork procedure. | Human: compare applicability with sources. Machine: check that every configured variant has a source file and a rendered label. |
| SCOPE-02 | Put a How to check explanation beside any setup-dependent chooser. Give an actionable way to identify the relevant context or ask the responsible person. No unverified UI labels or automatic classification. | Check your organization's setup instructions; ask your administrator if they do not identify the guide. | Select your inference backend. | Human: follow the identification advice using only facts established by sources. |
| PROC-01 | Each selectable method must contain the steps required to reach its outcome without borrowing steps from another variant or method. | Each method begins with opening Customize, then Plugins. | Follow the other tab, but skip step 2. | Human: read each method in isolation and trace its outcome. |
| PROC-02 | Put permissions, trust conditions, and behavior that could change the reader's decision before the steps they govern. Distinguish installation from connector access. | Explain before Government installation that bundled connectors are not added. | Mention after installation that a bundled local MCP server never runs. | Human: locate each condition and the step it affects. |
| PROC-03 | End each method with an observable result supported by the source. Do not claim that installation proves every capability works. | Open the installed plugin to see its components. | Your team now has access to all connected data. | Human: compare the result with the procedure and source. |
| UI-01 | Use exact, source-backed UI labels in bold and numbered steps for ordered actions. Flag ambiguous labels in the editorial record rather than inventing precision. | Select **Browse plugins**. | Click the green Import package button when no source names it. | Human: compare controls and sequence with source. |
| NAV-01 | Variant links must select the named instructions and retain the requested section. Unknown context must not select a different workflow. No-script and print views must retain labeled instructions. | `?instructions=government#government-file`. | An old Government link opens general Cowork instructions. | Browser check: direct URLs, unknown values, back/forward, keyboard selection, disabled JavaScript, and print. |
| EVID-01 | Preserve the unmodified before page and record where every removed section goes. Record source conflicts and unverified assumptions. | Exact before copy, section disposition table, unresolved UI check. | Delete limits or a unique workflow without recording its destination. | Machine: compare before bytes with pinned source. Human: reconcile all original sections. |

These are editorial rules, not a claim that a style checker can establish product
truth. Structural checks can confirm a heading or source file exists; an editor
must verify that the instructions actually apply and produce the stated outcome.
