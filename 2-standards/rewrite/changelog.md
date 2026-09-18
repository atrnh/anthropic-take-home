# Rewrite decisions and evidence

## Design decisions

Readers cannot be expected to know their setup, so the chooser needs a short
How to check explanation. A variant is separately authored content; the chooser
is only its presentation. One complete task page is enough to demonstrate the
standard; this example does not build a new docs platform.

## Source provenance

| Source | Used for |
| --- | --- |
| [Pinned Cowork guide](snapshots/cowork--guide--plugins.md) | Exact before page; marketplace, repository and file installation; required plugins; links to limits and adjacent tasks. |
| [Pinned Government member guide](snapshots/government--desktop--plugins.md) | Government organization and file workflows; local scope; trust notice; connector restrictions; marketplace limitation. |
| [Pinned submission guide](../../corpus/plugins/submit.md) | Review source, permissions, services, and data access before installation. |
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
| Distinguish pinned-source wording from my current-product updates in the method record below. | Keep the evidence for exact controls visible; flag unverified labels before publication. | UI-01 |
| Give variants distinct stable IDs and shareable URLs. | Deep links reveal the correct instructions; unknown context never defaults to another workflow. | NAV-01 |
| Preserve the exact source and record every original section below. | Removing prose from this page must not lose unique content. | EVID-01 |

## Every section of the original page

| Original section | Treatment in the rewrite |
| --- | --- |
| Introduction | Short shared definition links to the overview. Applicability and relevant component behavior move into the variants. |
| What a plugin can contain | Replace the table with a short shared definition and an overview link; keep Government restrictions before its procedures. The proposed shared overview will own the complete component reference, including hooks. The original table remains available pending that migration. |
| Install a plugin | Marketplace and file methods become separate complete procedures in the Cowork source. |
| Use a Git repository as a marketplace | Retain repository support, URL/shorthand, and full installation path. Marketplace update action remains at the existing source section and belongs to future management content. |
| Limits | Link to the existing limits reference before file upload. All limit values and the preview-size caveat remain in the pinned before/source; they are not silently deleted or generalized across variants. |
| Plugins managed by your organization | Link administrator provisioning as a separate task. Required-plugin behavior remains in the pinned Cowork source and that destination; the current rewrite omits the member-facing summary. |
| Update and remove plugins | Link to the existing section, preserving the local-edit overwrite warning and organization-managed removal rule there. |
| Related | Retain concept, public submission, and administrator destinations as contextual links. |

The Government snapshot supplies the second variant and is preserved alongside
the Cowork before page. Its create-with-Claude and management tasks remain linked.
Government marketplace availability and network restrictions remain in the pinned
Government source under **Where plugins come from**. The current rewrite omits
that discussion; the source lacks a complete marketplace installation procedure.

## Open product checks before publication

- Confirm the chooser labels and identification help with members who do not know
  their setup. The current fallback is honest but may require contacting someone.
- Confirm my current general-UI labels against the target release, including
  file upload and connector authentication. The pinned Cowork source predates
  these label changes; it does not establish every prompt in the revised steps.
- Confirm the Government organization-install control label and any action required
  after its upload trust notice. The source establishes the task but omits those
  exact controls. The rewrite says to install the organization plugin and follow
  the upload notice; it does not name an unsupported confirmation button.
- Confirm the marketplace entry path. The pinned financial-services guide uses
  different UI wording; the general variant now follows my local-product
  knowledge, pending release-specific verification.

## Verification

Verified on 2026-09-15:

- `python3 2-standards/rewrite/verify.py` passes: before/source byte equality,
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

### Portable build refactor, 2026-09-17

The example is now a standalone `uv` project. Jinja2 includes compose the existing
Markdown variants, Python-Markdown renders the content, and a Jinja2 HTML template
replaces Pandoc's document wrapper. The authored workflows and chooser behavior
are unchanged. The snapshot check uses its pinned digest so verification also
works outside the parent repository. Verification normalizes line endings to
accommodate Windows checkouts.

Verified the locked setup, build, and artifact checks in a clean copy without a
virtual environment or generated files; its outputs matched the repository build.
Browser checks covered both guides, Government file deep links, show-both mode,
back navigation, unknown and contradictory context, JavaScript disabled, and print.
Use the commands in [the README](README.md) for the current build and checks.


### Layout, callouts, and style audit, 2026-09-17

Build output now lives in `build/page.md` and `build/page.html`; HTML templates
live in `source/templates/`. The shared Jinja page supplies each variant's H2 from
its frontmatter label. Both requested notes are callouts placed before the steps.
The chooser retains an empty option and live status for unknown or conflicting
links; its help text matches **Which guide should I use?**. These changes implement
SCOPE-01, SCOPE-02, PROC-02, and NAV-01. Procedure numbering, spelling, bold UI
labels, and the Government file method's inspection/result were also corrected.

The earlier verification entries describe earlier revisions. The current general
procedures include my subsequent edits, so the earlier statement that the
workflows were unchanged does not apply to this revision.

| Method | Evidence and current status |
| --- | --- |
| General marketplace | Pinned Cowork **Install a plugin** establishes the workflow. My 2026-09-17 local Claude Desktop knowledge supplies **Discover**, partner recommendations, **Add**, and **Yours**. These differ from the snapshot and have not been independently checked against a specified app version or plan. |
| General Git marketplace | Pinned Cowork **Use a Git repository as a marketplace** establishes repository support. I supplied the **Add** dropdown, **Add from a repository**, **URL**, **Sync**, and **Yours** path. Release-specific validation remains open. |
| General file upload | Pinned Cowork **Install a plugin** establishes package upload. I supplied **Upload a plugin**, **Upload**, and **Yours**. The exact upload and sign-in sequence remains a publication check. |
| Government organization plugin | Pinned Government **Find and install plugins** establishes **Customize**, **Plugins**, **Organization plugins**, **Browse plugins**, **Organization**, and automatic installation. The unsupported **Add** label was removed. **Manage installed plugins** supports opening and inspecting the result. |
| Government file upload | Pinned Government **Find and install plugins** establishes **Add plugin**, **Upload plugin**, ZIP selection, and a trust notice; **Manage installed plugins** establishes inspection and device-local scope. The procedure refers to the notice without inventing its controls. The exact confirmation sequence remains unverified. |

The callouts retain the pinned security and Government connector restrictions.
Installation does not establish that bundled connectors are available. Snapshot
content is unchanged. This audit checks editorial structure and records evidence
limits; it does not establish that either installation flow matches every current
Claude Desktop release.
