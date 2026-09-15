# Rewrite decisions and evidence

## Scope and challenge alignment

The challenge's Part 2 asks for a style-guide excerpt, a content-type template,
and one existing page rewritten to that standard, with before/after and reasons.
This package demonstrates those deliverables with **Install a plugin**. It is a
worked draft for review, not completion of the entire take-home.

Ashley confirmed on 2026-09-15 that readers cannot be expected to know their setup,
that the chooser needs a short How to check explanation, and that one complete
task-page example is sufficient. A variant is separately authored content; the
selector is its presentation. This example does not build a new docs platform.

The supplied challenge sets an approximately six-hour budget and asks candidates
to mark what existed at that point if they exceed it. This session cannot establish
the cumulative six-hour boundary; no retrospective timing claim is made here.

## Source provenance

| Source | Used for |
| --- | --- |
| [Pinned Cowork guide](../../../corpus/cowork/guide/plugins.md) | Exact before page; marketplace, repository and file installation; required plugins; links to limits and adjacent tasks. |
| [Pinned Government member guide](../../../corpus/government/desktop/plugins.md) | Government organization and file workflows; local scope; trust notice; connector restrictions; marketplace limitation. |
| [Pinned submission guide](../../../corpus/plugins/submit.md) | Review source, permissions, services, and data access before installation. |
| [GitHub Docs version guidance](https://docs.github.com/en/get-started/using-github-docs/about-versions-of-github-docs), consulted 2026-09-15 | Design precedent for pairing a chooser with identification help and an owner-question fallback. Its GitHub-specific URL and UI checks are not applied to Claude. |

A live spot check of the [Cowork overview](https://claude.com/docs/cowork/overview)
and [Government overview](https://claude.com/docs/government/overview) did not
establish a reliable member-visible label that distinguishes every setup. The
How to check copy therefore directs organization-managed readers to their setup
instructions or administrator. Starting self-setup readers at the general guide
is an editorial routing recommendation, not a claim that the page can classify
their account. The choice stays visible and can be changed.

## Changes tied to the standard

| Change | Why | Rules |
| --- | --- | --- |
| Keep installation as the reader outcome; move maintenance and public submission to links. | Readers can finish one task without traversing the plugin lifecycle. | TASK-01 |
| Compose separate Cowork and Government Markdown files into one page. | Preserve complete procedures while providing one task destination. | SCOPE-01, PROC-01 |
| Add a native chooser and How to check help, including an administrator question and an unmatched-setup route. | Readers need help choosing; absence of one label does not prove another context. | SCOPE-02 |
| Put Government connector behavior before its procedures. | Installing a package does not make bundled connectors available in that context. | PROC-02 |
| Repeat the starting location in each method. | Readers can use a method without borrowing steps from another section. | PROC-01 |
| Add an observable result to each method. | Distinguish successful installation from usable external-service credentials. | PROC-03 |
| Preserve source-backed UI wording; use “upload option” where the Cowork source does. | Avoid inventing a button label to make the rewrite appear more precise. | UI-01 |
| Give variants distinct stable IDs and shareable URLs. | Deep links reveal the correct instructions; unknown context never defaults to another workflow. | NAV-01 |
| Preserve the exact source and record every original section below. | Removing prose from this page must not lose unique content. | EVID-01 |

## Every section of the original page

| Original section | Treatment in the rewrite |
| --- | --- |
| Introduction | Short shared definition links to the overview. Applicability and relevant component behavior move into the variants. |
| What a plugin can contain | Replace the table with a task-focused component summary and an overview link. The proposed shared overview will own the complete component reference, including hooks. The original table remains available pending that migration. |
| Install a plugin | Marketplace and file methods become separate complete procedures in the Cowork source. |
| Use a Git repository as a marketplace | Retain repository support, URL/shorthand, and full installation path. Marketplace update action remains at the existing source section and belongs to future management content. |
| Limits | Link to the existing limits reference before file upload. All limit values and the preview-size caveat remain in the pinned before/source; they are not silently deleted or generalized across variants. |
| Plugins managed by your organization | Retain required-plugin behavior in Cowork and link administrator provisioning as a separate task. |
| Update and remove plugins | Link to the existing section, preserving the local-edit overwrite warning and organization-managed removal rule there. |
| Related | Retain concept, public submission, and administrator destinations as contextual links. |

The Government source supplements the rewrite; it is not a second page claimed
as the “before.” Its create-with-Claude and management tasks remain linked.
Government personal-marketplace installation is acknowledged, but the pinned
source lacks complete click-by-click steps. The example directs readers to their
administrator rather than presenting an invented third procedure.

## Open product checks before publication

- Confirm the chooser labels and identification help with members who do not know
  their setup. The current fallback is honest but may require contacting someone.
- Confirm the Cowork file-upload label and whether authentication differs by
  installation method. The source describes a generic upload option and connector
  authentication but does not enumerate every prompt in the file path.
- Confirm the Government organization-install control label and any action required
  after its upload trust notice. The source establishes the task but omits those
  exact controls; the rewrite does not invent them.
- Confirm the marketplace entry path. The pinned financial-services guide uses
  different UI wording; this rewrite follows the general Cowork source, pending
  owner verification.

## Verification

Verified on 2026-09-15:

- `python3 docs/2-standards/rewrite/verify.py` passes: before/source byte equality,
  reproducible outputs, one H1, unique IDs, and both authored variants assembled.
- Browser checks pass for general and Government selection, keyboard selection,
  direct Government file-install links, unknown and contradictory context,
  show-both mode, and back/forward navigation.
- With JavaScript disabled, both labeled guides remain readable and the inactive
  chooser is hidden. Scripting was restored after the check.
- Visual inspection confirms that a deep link keeps the selected context visible
  above the file-install procedure and shows the Government restriction before
  the steps.

These checks establish the demonstration's behavior; they cannot verify the actual
Claude installation UI. Screen-reader testing and a wider device matrix remain
outside this small demonstration.
