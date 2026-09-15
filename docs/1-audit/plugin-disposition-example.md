# Plugin installation and distribution: editorial disposition example

Status: proposal for review, 2026-09-15. This is the first worked example for
the audit memo, not the complete slice audit or an implemented migration.
Evidence comes from the 54-page snapshot fetched on 2026-09-14, recorded in
[the manifest](../../corpus/manifest.json). Statements below describe that
snapshot, not independently verified current product behavior.

Continuation: the [slice-wide ledger](disposition-ledger.md) now covers all 54
pages, including the Government connector-policy destination left open below.
The [proposed IA](proposed-ia.md) carries the current migration recommendation;
this file preserves the detailed first example.

## Recommendation

Give plugin concepts one home and give readers task-based destinations for
installation, organization distribution, and public submission. Author distinct
procedures in separate Markdown files and compose the applicable procedure into
the task page. Preserve specialized workflows without making readers work
through instructions for every environment.

Uploading, making available, installing, and granting tool access are different
outcomes. Document each outcome explicitly, including the handoff to the next task.

## Evidence and priorities

Priorities describe reader consequences, not measured incident frequency.

| Priority | Finding in the snapshot | Reader consequence and decision |
| --- | --- | --- |
| 1 | The general overview says organization-wide management is forthcoming; Cowork already documents required plugins. [S1, Availability; S2, Plugins managed by your organization] | Readers receive incompatible availability guidance. Remove the unqualified roadmap promise from the proposed overview and have the responsible owner verify availability for each context before publication. |
| 1 | Cowork describes connector sign-in during installation. Government says plugin-declared connectors are not connected and local MCP servers declared by plugins never run. [S2, Install a plugin; S3, What plugins add; S4, Plugins versus connectors] | A successful plugin install does not establish the same tool access everywhere. Put the applicable behavior in the selected workflow before installation, and distinguish installation success from connector availability. |
| 1 | Government auto-installed plugins can stay uninstalled by a member; required plugins cannot be removed. Removing a plugin from Government administration stops delivery but does not remotely uninstall existing copies. [S3, Manage installed plugins; S4, Install behavior / Update or remove a plugin] | Collapsing these states could mislead both members and administrators. Preserve auto-install, required, stop delivery, and uninstall as distinct operations and outcomes. Do not extrapolate Cowork's removal rules to Government. |
| 1 | A Claude Tag upload enters the organization catalog but is not attached anywhere until enabled for a scope. [S5, Upload a plugin as a zip file] | An administrator can finish uploading while channels still lack the plugin. The distribution procedure must continue through attachment and identify the resulting scope. |
| 2 | A page under `office-agents/` explicitly instructs readers to open Cowork and install financial-services plugins. [S7, Add the marketplace] | Its location suggests M365 add-ins even though its steps target Cowork. Move its reader-facing home to plugin collections and preserve the specialized installation order. This source does not establish plugin support in M365 add-ins. |
| 2 | The member guides repeat plugin definitions, while the overview combines definition, catalog, history, and availability. [S1–S3] | Readers must reconcile repeated explanations. Keep the full component explanation in the overview; retain a short orientation and applicable behavior in task pages. |
| 3 | Cowork and financial-services pages name different marketplace entry controls. [S2, Use a Git repository as a marketplace; S7, Add the marketplace] | Treat this as an unresolved UI wording difference, not proof of different installation mechanisms. Verify the current path before consolidating repeated steps. |

## Proposed navigation and content ownership

```text
Extend Claude
├── Plugins
│   ├── Understand plugins                     /docs/plugins/overview
│   ├── Install a plugin                      /docs/plugins/install
│   ├── Manage installed plugins              /docs/plugins/manage
│   ├── Create a plugin with Claude           /docs/plugins/create-with-claude
│   └── Financial services collection         /docs/plugins/collections/financial-services
├── Administer extensions
│   └── Distribute and manage plugins         /docs/admin/plugins
└── Build and publish extensions
    └── Submit a plugin to the directory      /docs/plugins/submit
```

These paths are proposed, except the existing overview and submission paths.
Cowork, Government, and Claude Tag landing pages remain alternate entry points to
the applicable task and context. They do not own duplicate versions of the
complete plugin manual. Claude Code remains a link to its existing documentation;
this example does not migrate that external documentation.

The Claude Tag skills-repository guide keeps its existing URL. Its outcome is
establishing a repository Claude can propose changes to, with human review and
subsequent propagation. That is a distinct end-to-end task. Extract its reusable
distribution procedures into canonical source files that the repository guide
can also include, preserving the guide's sequence and prerequisites.

### Procedure variants

| Task | Applicability established by the source | Mechanism and completion condition | Content treatment |
| --- | --- | --- | --- |
| Install a plugin | Cowork member; deployment is not fully specified by S2 | Marketplace or file; plugin appears installed, with connector sign-in when needed | Separate Cowork procedure source; local method tabs only where complete instructions exist. Do not label it universally applicable or infer a direct-account prerequisite. |
| Install a plugin | Government Desktop member | Organization catalog, personal file, or an added marketplace subject to network controls; distinguish already auto-installed plugins | Separate Government source; present the matching instructions on the same install page. Keep device-local scope and connector restrictions. Marketplace click-by-click details remain an evidence gap. |
| Create a plugin with Claude | Government Desktop member | Create with Claude, then install the result on that device | Separate task destination, linked from installation; do not invent equivalent instructions for other contexts. |
| Distribute plugins | Government tenant administrator or organization owner | Upload package or marketplace archive, review trust markers, choose install behavior at the applicable level; members receive or can choose the plugin | Government administrator source, separate from member installation. Preserve package constraints, inheritance, and the limits of removal. |
| Distribute plugins to Claude Tag channels | Claude Tag administrator; scope attachment required | Upload and attach, or sync a marketplace and attach; catalog membership alone is insufficient | Claude Tag administrator source with method variants. Preserve the GitHub connector prerequisite for github.com sync and private/internal repository requirement. Do not require repository write access merely to distribute a ZIP. |
| Let Claude propose skill improvements | Claude Tag administrator and human reviewer | Set up repository, sync, grant write access, attach plugins; requested PR changes reach new threads after review, merge, and sync | Keep the existing repository guide; reuse distribution content without losing its larger workflow. |
| Publish to the public directory | Author with submission access described in S6 | Validate and submit a public repository, then track review; submission is not acceptance | Keep submission separate from private distribution. Its claude.ai and Console routes are local submission choices, not deployment settings. |

Sources: [S2], [S3], [S4], [S5], [S6]. A blank or unreviewed context means
not established by this example, not unsupported. Cowork administrator provisioning
is linked outside the snapshot at `/docs/cowork/3p/extensions`; keep that route
until it has been reviewed. Do not synthesize its instructions from member UI.

## One page, separate Markdown sources

Illustrative authoring layout only; these files and selectors are not implemented:

```text
plugins/install.md                         shared purpose and page assembly
procedures/plugins/install/cowork.md        complete Cowork workflow
procedures/plugins/install/government.md    complete Government workflow
admin/plugins.md                           administrator task assembly
procedures/plugins/distribute/government.md
procedures/plugins/distribute/claude-tag-upload.md
procedures/plugins/distribute/claude-tag-sync.md
```

Each procedure records task, actor, place of use, deployment conditions when
known, mechanism, outcome, and source evidence. Where an administrator performs
setup is separate from where members use the plugin. These fields describe
applicability; they are not a requirement to show seven controls to the reader.

### Assembled install-page outline

1. **Purpose:** add a plugin for your own use. Link administrators to distribution.
2. **Visible context:** show the place of use and relevant deployment condition.
   Select the specific Government procedure when that condition applies. A source
   with unspecified deployment is not a fallback for every other deployment.
3. **Before you start:** selected procedure's availability, trust requirements,
   package requirements, and what installing makes available.
4. **Choose a method:** tabs for the documented methods in that context, such as
   marketplace or file. Each contains a complete procedure, including any sign-in.
5. **Check the result:** identify the installed plugin and its available components.
   Government instructions explicitly distinguish installation from connector access.
6. **Next steps:** manage the installed plugin, or follow applicable connector setup.

Persist deployment context across tasks only when it remains relevant. Keep
installation method local to the task. Do not offer one dropdown mixing Cowork,
Government, and ZIP upload, or imply that every combination exists.

Readers cannot be expected to identify their setup unaided. Put a short **How to
check** explanation next to the chooser, with an administrator-question fallback
when the available sources establish no reliable self-service check. Ashley
confirmed this direction on 2026-09-15. Demonstrate one complete task page before
expanding the presentation system; see the [worked rewrite](../2-standards/rewrite/README.md).

Explicit context in an incoming link wins over a saved preference, and the page
visibly shows that context. With no applicable procedure, explain the documentation
gap and retain the existing relevant route. Do not silently show another workflow.

The eventual interface must support keyboard operation, shareable context links,
and a readable no-script/print representation with labeled variants. Hidden tabs
must not make a directly linked section inaccessible. These are acceptance criteria,
not a commitment to a particular component or static-site framework.

## Disposition of every reviewed URL

All old paths below are relative to `https://claude.com`. New destinations are
proposals, not existing routes. Retained bridge pages contain short task links and
include canonical content where needed; they are not separately maintained manuals.

| Old URL | Content disposition | Reader-facing URL behavior |
| --- | --- | --- |
| `/docs/plugins/overview` | Keep the shared definition and component relationship. Replace the duplicate catalog table with a directory link. Remove promotional paragraphs, historical detours, and the unqualified future-management promise; retain necessary links and verified applicability guidance. | Keep URL. Preserve legacy heading anchors as short signposts to the surviving explanation, directory, or task. |
| `/docs/cowork/guide/plugins` | Move installation/marketplace instructions to install; management to manage; component explanation to overview; limits to the applicable procedure/reference section. | Keep a compatibility bridge initially because the page covers several tasks. Bare URL offers those tasks with Cowork context; old section anchors route to the corresponding task with that context. No blanket redirect to installation. |
| `/docs/government/desktop/plugins` | Move installation and management into Government variants; preserve Create with Claude as a separate task. Keep marketplace/network restrictions, device-local scope, and connector behavior. | Keep a compatibility bridge with Government context. Bare URL offers install, create, and manage; old anchors retain their task intent. |
| `/docs/government/config/plugins-and-connectors` | Compose plugin administration from the Government admin source. Preserve connector policies in this page until a connector disposition pass assigns their canonical home. | Keep URL as an admin bridge. Plugin anchors point to the appropriate admin section with Government context; connector-policy anchors keep working here. Never redirect the entire page to plugin installation. |
| `/docs/claude-tag/admins/skills-repo` | Keep the skills-improvement workflow, repository guidance, prompts, and related resources. Reuse canonical distribution sources for upload/sync steps. Resolve conflicting archive-format claims before rewriting them. | Keep URL and headings, including `#upload-a-plugin-as-a-zip-file`. The included upload procedure is the same source shown in the administrator task page. |
| `/docs/plugins/submit` | Keep the direct-install / own-marketplace / public-directory route choice, validation, access prerequisites, submission, review, update behavior, trust information, and policy links. Shorten repeated component definitions into links; retain publisher-specific setup guidance. | Keep URL and existing anchors. Route direct installation to the applicable member guide, own-marketplace setup to the existing Claude Code guide or reviewed administration instructions, and public submission to the retained section. Do not funnel all sharing through administration. |
| `/docs/office-agents/fsi-plugins` | Move collection guidance under plugins; retain repository URL, core-first order, add-ons, skills, provider access requirements, customization guidance, and review warning. Reuse verified generic installation steps. | After publishing the replacement, permanent redirect to `/docs/plugins/collections/financial-services`. Preserve all existing heading IDs at the destination. |

This pass proposes one whole-page relocation, several content consolidations, and
specific prose deletions. It proposes no deletion of a unique workflow and no 404s.
Delete redundant authored copies only after canonical content and URL compatibility
are verified. Keep the pinned corpus unchanged.

### Old-link examples and compatibility contract

The query fields here are a proposed public URL contract, not deployed functionality.

| Incoming path and fragment | Required destination or retained behavior |
| --- | --- |
| `/docs/cowork/guide/plugins#install-a-plugin` | `/docs/plugins/install?experience=cowork#install` |
| `/docs/cowork/guide/plugins#use-a-git-repository-as-a-marketplace` | `/docs/plugins/install?experience=cowork&method=marketplace#add-marketplace` |
| `/docs/cowork/guide/plugins#limits` | `/docs/plugins/install?experience=cowork#limits` |
| `/docs/cowork/guide/plugins#update-and-remove-plugins` | `/docs/plugins/manage?experience=cowork#update-and-remove` |
| `/docs/government/desktop/plugins#find-and-install-plugins` | `/docs/plugins/install?deployment=government#install` |
| `/docs/government/desktop/plugins#manage-installed-plugins` | `/docs/plugins/manage?deployment=government#manage` |
| `/docs/government/config/plugins-and-connectors#plugin-archive-formats` | `/docs/admin/plugins?deployment=government#archive-formats` |
| `/docs/government/config/plugins-and-connectors#update-or-remove-a-plugin` | `/docs/admin/plugins?deployment=government#update-or-remove` |
| `/docs/government/config/plugins-and-connectors#connector-tool-policies-for-members` | Keep the current anchor and connector-policy content until that task is migrated. |
| `/docs/claude-tag/admins/skills-repo#upload-a-plugin-as-a-zip-file` | Keep current URL/anchor and include the canonical Claude Tag upload-and-attach workflow. |
| `/docs/office-agents/fsi-plugins#install-plugins` | `/docs/plugins/collections/financial-services#install-plugins`, retaining core-first instructions. |

These are representative mappings, not a complete anchor inventory. Before launch,
enumerate every rendered heading/explicit ID on all seven old pages and account for
each. The Markdown snapshot establishes headings; actual rendered IDs need checking.
The manifest also records `.md` source URLs. Inventory those machine-readable routes
alongside extensionless browser URLs, preserve access to the corresponding content,
and update the documentation index when destinations change. Give composed variants
unique IDs so repeated headings do not compete for the same fragment.
URL fragments are not sent to the server, so a server redirect cannot choose a
different task based on the incoming fragment. Retain real legacy anchor targets
and useful links on bridge pages; optional client routing can read the fragment and
open the chosen task/variant. For the collection's whole-page redirect, test fragment
preservation through the actual host and retain the same IDs on the replacement.

## Migration and acceptance

1. **Resolve correctness questions.** Have the relevant owners confirm availability,
   marketplace UI wording, and applicability. S5 lists a single-skill archive layout
   but then says archives without a manifest are rejected. Preserve the contradiction
   as an open question; do not turn either claim into a universal packaging rule.
   Government admin upload limits do not establish member-upload limits.
2. **Author the selected procedures.** Extract the source-backed workflows into
   separate Markdown files, retaining permissions, trust notices, size-limit units,
   actor handoffs, and completion conditions. Shared text has one canonical source.
   Cowork specifies 200 MB uncompressed per plugin [S2, Limits]; Claude Tag specifies
   200 MB per uploaded archive [S5, Upload a plugin as a zip file]. Government admin
   upload specifies 10 MB for a single plugin, 15 MB for a marketplace archive, and
   50 MB of uncompressed content per plugin [S4, Plugin archive formats]. Keep these
   contexts and measures explicit rather than presenting one universal size limit.
3. **Assemble and test task pages.** Validate the context/method contract with a
   static page example before selecting a global UI design. Check that no workflow
   requires readers to consult another variant to complete its steps.
4. **Ship compatibility with the content.** Inventory old anchors, publish task
   destinations, update navigation and internal links, and then enable bridges and
   the collection redirect. Check ordinary links, deep links, saved-context conflicts,
   keyboard use, and no-script behavior. Keep bridges while multi-task inbound intent
   cannot be mapped safely to a single destination.
5. **Expand only after this example holds.** Apply the same disposition fields to
   the rest of the slice. The existing extraction artifacts are evidence inputs;
   this example neither reruns that pipeline nor establishes full-corpus coverage.

Acceptance examples: a Government member can identify that plugin installation
does not add connectors; a Government admin can distinguish stopping delivery from
remote uninstall; a Claude Tag admin reaches attachment after upload; a financial-services
reader reaches Cowork instructions and installs the core first. Require correct
answers and correct navigation in these scenarios, not just a lower page count.

## Measurement proposal

No baseline or improvement has been measured yet. Run the same scenarios on the
current pages and the assembled proposal, counterbalancing the order across readers
to reduce learning effects. Include members and administrators, record prior context,
and report raw successes/failures and timings without claiming statistical certainty
from a small formative study.

| Question | Measure | Instrumentation |
| --- | --- | --- |
| Can readers find the applicable workflow? | Correct first destination, wrong-context attempts, time to applicable instructions | Observed task sessions plus `procedure_view` with task ID, variant ID, and selection origin: explicit link, saved choice, or local selection. |
| Do readers understand the result and limits? | Scenario completion and correct explanation of connector access, attachment, and removal | Moderator rubric for the acceptance examples; optional task-specific feedback with a reason category. A page visit is not task completion. |
| Do old links preserve intent? | Broken target count and incorrect/missing context; successful resolution of each known anchor | Build/deployment link checks plus browser checks of redirect/bridge paths and saved-context conflicts. `legacy_route_resolved` records a route ID and chosen target, not a raw URL. |
| Does source consolidation reduce drift? | Conflicting claims and number of independently authored copies of shared instructions | Editorial review of the source/include map at release; record corrections by claim and applicable context. File-count reduction is not the goal. |

Use allowlisted task, variant, and route IDs. Do not collect repository URLs,
organization identifiers, prompts, plugin contents, or credentials. Context-switch
counts indicate investigation opportunities, not automatic failures: readers may be
deliberately comparing contexts. Set production targets after establishing a baseline;
all known compatibility links must work before launch.

## Source register

All references resolve to the pinned corpus. Section names in the tables identify
the evidence within each file.

[S1]: ../../corpus/plugins/overview.md
[S2]: ../../corpus/cowork/guide/plugins.md
[S3]: ../../corpus/government/desktop/plugins.md
[S4]: ../../corpus/government/config/plugins-and-connectors.md
[S5]: ../../corpus/claude-tag/admins/skills-repo.md
[S6]: ../../corpus/plugins/submit.md
[S7]: ../../corpus/office-agents/fsi-plugins.md

- [S1] General plugin overview.
- [S2] Cowork member installation and management.
- [S3] Government member installation and management.
- [S4] Government administration of plugins and connectors.
- [S5] Claude Tag skills repository, upload, sync, and scope attachment.
- [S6] Public plugin submission.
- [S7] Financial-services collection installation in Cowork.
