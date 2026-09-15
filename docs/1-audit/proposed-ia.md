# Proposed information architecture and migration

Draft, 2026-09-15. This applies the [plugin example](plugin-disposition-example.md) across the [54-page disposition ledger](disposition-ledger.md). The [memo](audit-memo.md) is the short recommendation. Paths below are proposed unless the ledger identifies them as existing. This document is maintained by hand.

## Organize by capability and task

```text
Extend Claude
├── Skills
│   ├── Understand skills
│   ├── Use and manage skills
│   ├── Create a skill with Claude or in the app
│   └── Write and test a skill package
├── Plugins
│   ├── Understand plugins
│   ├── Install a plugin
│   ├── Manage installed plugins
│   ├── Create a plugin with Claude
│   └── Financial services collection
├── Connectors
│   ├── Understand connectors
│   ├── Find or request a connector
│   ├── Understand verification labels
│   ├── Connect a service
│   │   ├── Google Docs, Gmail, and Calendar
│   │   ├── GitHub files
│   │   ├── Microsoft 365
│   │   └── Slack
│   ├── Add a custom connector
│   ├── Use connected tools and data
│   └── Manage a connection
├── Administer extensions
│   ├── Distribute and manage plugins, including bundled skills
│   ├── Enable connectors and set tool policies
│   ├── Set up Microsoft 365 access
│   ├── Set up GitHub tools
│   ├── Configure built-in Desktop connectors
│   ├── Set up a skills repository Claude can update
│   └── Connect a private network
│       ├── Understand MCP tunnels
│       ├── Set up a tunnel
│       ├── Configure tunnel authentication
│       ├── Rotate credentials or remove a tunnel
│       └── Troubleshoot a tunnel
└── Build and publish extensions
    ├── Choose MCP, a plugin, or both
    ├── Understand MCP
    ├── Build a connector or desktop extension
    ├── Implement authentication
    │   ├── Authentication reference
    │   ├── Lazy authentication
    │   └── Enterprise Managed Auth
    ├── Build MCP Apps
    │   ├── Try an example and start building
    │   ├── Design guidelines and style variables
    │   ├── Support multiple hosts
    │   ├── Open external links
    │   ├── Supersede older instances
    │   ├── Apply the host's theme
    │   └── Troubleshoot rendering
    ├── Test and troubleshoot connectors
    ├── Choose directory or custom distribution
    ├── Check submission requirements
    ├── Submit a connector or plugin
    └── Update integrations and manage listings
```

This is a navigation proposal, not a demand to move every URL. Most builder and specialist references keep their addresses. Keep existing Cowork, Government, Claude Tag, Science, M365, and managed-Desktop entry points as additional routes to these tasks. Science also retains its useful resource catalog. A reader entering through Microsoft 365 should not need to know the term "connector" first.

## Give new destinations explicit scope

| Proposed destination | Outcome and source-backed variants |
| --- | --- |
| `/docs/skills/use` | Enable, invoke, or manage skills. Government Desktop, Science, and M365 add-in usage remain labeled procedures. M365's task ends at use; do not invent local creation or deletion controls. General help-center routes remain until reviewed. |
| `/docs/skills/create` | Create through the app. Government and Science have distinct documented methods. Hand-authored files remain at `/docs/skills/how-to`. |
| `/docs/plugins/install` | Install for personal use. Cowork and Government workflows are demonstrated by the worked example. Installation method belongs inside the applicable workflow. |
| `/docs/plugins/manage` | Update or remove installed plugins. Preserve Cowork and Government differences in required/auto-installed behavior. |
| `/docs/plugins/create-with-claude` | Create a plugin with Claude. Government is the source-backed context; other contexts are unestablished. |
| `/docs/plugins/collections/financial-services` | Install the Cowork collection in its required order, then connect licensed data providers as applicable. |
| `/docs/admin/plugins` | Make plugins available to members or channels, update delivery, or stop delivery. Government and Claude Tag have separate complete procedures. Government skill packaging includes the final member-device activation check. Claude Tag upload includes attachment, not just catalog entry. |
| `/docs/connectors/add-custom` | Add a custom server. Compose the existing general remote guide and Science's remote/local methods. Separate owner enablement from member connection, retaining the handoff and prerequisites in both relevant views. |
| `/docs/connectors/use` | Use connected tools/data in a conversation or app. Show contextual usage instructions and link to service-specific tasks and the distinct Claude Tag personal-connector guide. Do not turn all uses into generic file attachment. |
| `/docs/connectors/manage` | Change or remove a connection using documented general remote procedures. Include reconnect effects. Other contexts link to retained guidance until a complete variant is established. |
| `/docs/admin/connectors` | Enable organization connectors or set tool policy. Compose the general owner setup and Government policy sections as separate tasks/sections with explicit scope. Link existing provisioning guides where the snapshot lacks setup. |
| `/docs/admin/connectors/microsoft-365` | Enable M365 access. General Claude-account setup and managed-Desktop deployment are separate variants; the latter retains its local/remote comparison and full methods. Keep Microsoft tenant administration distinct from Claude organization ownership. |
| `/docs/admin/connectors/github` | Deploy GitHub MCP tools for managed Desktop. Keep hosted PAT and built-in OAuth methods separate. File attachment remains at `/docs/connectors/github/index`. |
| `/docs/connectors/mcp-tunnels/manage` | Rotate credentials or decommission a claude.ai Enterprise tunnel. Preserve method-specific operational steps and irreversible archive behavior. |

The [ledger](disposition-ledger.md) assigns every existing URL to a retained page, bridge, or proposed destination. Retained service pages remain canonical for their distinct tasks. New task names are not a commitment to a framework, schema, global preference system, or exact control design.

## Author complete procedures, compose the reader's view

Keep shared concepts in their existing Skills, Plugins, and Connectors overviews. Maintain divergent workflows in separate source files. Compose the applicable workflow into its task page. Reuse small identical passages only when scope and outcome stay identical.

Record these dimensions independently in the editorial record:

- **Place of use:** for example, an M365 add-in, Science, or Desktop.
- **Access/deployment condition:** for example, Government or managed Desktop on third-party inference, only when established by a source.
- **Actor and permissions:** member, Claude organization owner, Microsoft tenant administrator, or publisher.
- **Local method:** file/marketplace, remote/local, or Helm/Compose.
- **Outcome:** installed, attached to a scope, authenticated, permitted to act, or submitted for review.

These are applicability facts, not five required dropdowns. Ask only for choices that change instructions. Use recognizable account/application labels and adjacent **How to check** guidance. If the evidence supplies no reliable UI check, tell readers what to ask their administrator. Never infer deployment merely because a page mentions Cowork or Desktop.

An explicit incoming context wins over a saved choice and remains visible. Preserve a method comparison when readers need to decide, especially Microsoft 365's local/remote data paths. Unknown context must offer identification help and the retained relevant route, never silently substitute an arbitrary procedure. Keyboard, no-script, print, and shareable links must retain complete labeled instructions.

The existing [Install a plugin example](../2-standards/rewrite/README.md) demonstrates this with `?instructions=cowork` and `?instructions=government`. The earlier plugin disposition uses illustrative `experience`/`deployment` fields. Neither is a deployed site-wide URL contract; publishing must choose one contract and map old links to it.

## Preserve incoming intent

Use a direct permanent redirect only when the old page identifies one destination:

| Old page | Proposed replacement and required context |
| --- | --- |
| `/docs/office-agents/fsi-plugins` | `/docs/plugins/collections/financial-services`, with the same headings and Cowork installation order. |
| `/docs/claude-science/custom-connectors` | `/docs/connectors/add-custom`, Science selected and both documented methods available. |
| `/docs/third-party/claude-desktop/connectors-github` | `/docs/admin/connectors/github`, managed Desktop selected; old remote/local headings select or expose their method. |
| `/docs/third-party/claude-desktop/connectors-m365` | `/docs/admin/connectors/microsoft-365`, managed Desktop selected; bare URL retains comparison, deep links expose the correct method. |

Multi-task pages keep useful links at their old URLs. For example, the bare Government plugins page offers install/create/manage; its management anchor leads to Government management. The Government admin page routes plugin delivery and connector policy separately. The existing `after-publishing` page retains runtime-update guidance and links to listing management and plugin updates. A remote-only dashboard page cannot absorb every publishing outcome.

Do not send removed sections to a homepage. Before redirecting a page, preserve its rendered heading IDs at the destination or provide a compatible landing page. Server redirects cannot inspect a fragment. Test fragment preservation on the actual host, and ensure a hidden variant cannot hide the target. Cover manifest `.md` routes and update `llms.txt` alongside browser navigation.

## Migrate in reader-testable batches

1. **Resolve consequential claims.** Product documentation owners confirm the questions in the ledger, particularly broad availability, skill archive rules, and Slack legacy behavior. Scope or remove unqualified claims only after their applicable replacement is ready. Record owner, evidence, and review date.
2. **Establish the baseline.** Test the scenarios below on the current pages. Include members and administrators unfamiliar with the documentation structure. Record task, setup, outcome, wrong-context attempts, and time to applicable instructions.
3. **Publish one complete family at a time.** Start with plugin installation/distribution and Government skill packaging, using the existing worked example. Then migrate connector setup and service administration. Retain specialist builder pages while repairing their entry routes and shared claims. Each batch includes complete content, source ownership, navigation, incoming links, and verification.
4. **Test content and compatibility together.** Inventory all original sections and anchors. Verify every unique instruction has a home, each applicable workflow stands alone, and old links preserve task/context. Check unknown choices, saved-context conflicts, keyboard use, and no-script/print views. Review `.md` outputs for labeled variants.
5. **Release and observe.** Publishing owners ship content and routing together. Keep the previous published version and route map available for rollback. If a migrated link selects the wrong workflow, restore its prior useful page while repairing the mapping. Remove duplicate authored text after acceptance; retain bridges while bare links still carry multiple plausible intents.

Acceptance scenarios:

- A Government member installs a plugin and correctly identifies that its bundled connectors were not connected.
- A Government administrator packages a textual skill as a plugin and verifies that it actually loads on a member device.
- A Claude Tag administrator uploads and attaches a plugin, then identifies when reviewed repository changes reach new threads.
- An M365 administrator chooses a documented setup based on data path and authentication needs; a member finds the correct sign-in handoff.
- A reader distinguishes adding GitHub files from configuring GitHub tools, without treating either as proof the other is available.
- A Science user finds custom-connector instructions with the correct organization restrictions and local-command warning.
- A reader arriving at an old Slack link distinguishes the earlier app, the Slack data connector, and the Claude Tag migration route.
- A builder finds authentication/testing guidance without entering member instructions or losing submission-type prerequisites.

No usability baseline, production redirect, or live product validation has been completed by this proposal. Page-level coverage is complete; those checks are explicit release work.
