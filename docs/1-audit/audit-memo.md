# Make the task the destination

**Draft audit memo · 15 September 2026**

Skills, plugins, and connectors share concepts across Claude, but the instructions depend on where someone works, how their organization provides access, and what they are trying to do. I recommend organizing this slice around capabilities and reader tasks, with complete, separately maintained procedures for the contexts that change the work.

This audit covers the [54-page snapshot fetched on 14 September](../../corpus/manifest.json). The [disposition ledger](disposition-ledger.md) records a treatment for every page. Findings describe that snapshot, not independently verified current product behavior. Priority reflects the consequence for a reader; we have not measured incident frequency.

## Fix applicability before rearranging navigation

**First, stop presenting specific workflows as universal.** The connector overview says prebuilt integrations need no setup beyond authentication. Microsoft 365's own guide requires Microsoft tenant consent and, on Team and Enterprise, organization enablement. A reader following the generic sequence can reach a blocked Connect action without knowing whose help they need. Replace the universal promise with scoped prerequisites and an explicit administrator-to-member handoff. [Overview](../../corpus/connectors/overview.md), [Microsoft 365 setup](../../corpus/connectors/microsoft/365.md).

The same problem affects skill distribution. The general authoring guide permits scripts and describes a skill-folder ZIP. Government administration requires a plugin wrapper and text-only skill contents; even an accepted upload can contain a malformed skill that never loads. Keep the shared authoring explanation, but present complete packaging and verification instructions for the chosen delivery route. Likewise, Government plugin installation does not connect bundled tools, and a Claude Tag upload does not attach a plugin to a channel. "Uploaded," "installed," and "ready to use" need distinct completion checks. [Skill authoring](../../corpus/skills/how-to.md), [Government skills](../../corpus/government/desktop/skills.md), [plugin evidence](plugin-disposition-example.md).

**Second, separate tasks that happen to share a product name.** GitHub file attachment and GitHub MCP tools produce different results. The Slack page mixes the earlier app with the data connector while pointing to Claude Tag as the current product. Readers should choose a goal before receiving instructions. Preserve the legacy Slack route until its prerequisites and retirement conditions are verified. Move the financial-services plugin collection out of `office-agents`: its installation steps explicitly target Cowork. [GitHub files](../../corpus/connectors/github/index.md), [GitHub tools](../../corpus/third-party/claude-desktop/connectors-github.md), [Slack](../../corpus/connectors/slack/index.md), [financial-services collection](../../corpus/office-agents/fsi-plugins.md).

**Third, remove competing explanations and redundant upkeep.** Explain each capability once. Replace the plugin overview's duplicate catalog with a directory link and cut its promotional/history detours. Resolve its unqualified promise of future organization management against the existing managed-plugin instructions. Consolidate listing-edit and permanent-slug guidance under listing management, while preserving separate server and plugin update outcomes. Keep useful specialist builder references; their detail is not a reason to merge them. [Plugin overview](../../corpus/plugins/overview.md), [Cowork management](../../corpus/cowork/guide/plugins.md), [after publishing](../../corpus/connectors/building/after-publishing.md), [listing management](../../corpus/connectors/building/managing-your-listing.md).

## Give shared tasks one home

Use **Skills**, **Plugins**, and **Connectors** as capability entries, followed by recognizable tasks: use a skill, install a plugin, connect a service. Add **Administer extensions** and **Build and publish** routes for distinct work. Keep product/context landing pages as additional entrances to the same instructions. Most specialist URLs can stay where they are; a navigation change does not require a URL migration.

A task page can compose separately authored workflows. Government and Cowork installation sources can produce one "Install a plugin" page without flattening their differences. Ask readers to choose context only when it changes the steps. Put **How to check** beside the choice, with an administrator-question fallback. Preserve comparisons where the reader must decide, such as Microsoft 365's local and remote data paths. The [worked page](../2-standards/rewrite/README.md) demonstrates this pattern; the [proposed IA](proposed-ia.md) applies it across the slice.

Keep role, place of use, deployment, and installation method distinct. "Desktop" is not enough to infer a workflow. An unspecified context is an evidence gap, not proof of support or non-support.

## Merge content without abandoning old links

The ledger proposes four whole-page relocations: the financial-services collection, Science custom connectors, and managed-Desktop GitHub and Microsoft 365 setup. Publish replacements first, then redirect with the relevant context and preserve heading targets.

Keep multi-task old URLs as short task-choice pages. The old Government plugins page must still serve install, create, and manage intents. Its administration page must route plugin distribution and connector policy separately. Retain real legacy anchor targets; a server redirect cannot inspect a URL fragment. Include machine-readable `.md` routes and `llms.txt` in the migration.

Delete duplicate authored passages only after their canonical replacements and incoming links work. No unique workflow should disappear. Do not blanket-redirect local-extension readers to a builder manual or all publishing readers to a remote-only dashboard.

## Migrate and measure one family at a time

Have product owners resolve the ledger's open correctness questions, then migrate plugin installation/distribution and Government skill packaging first. Follow with connector setup and administration. Each batch includes content, navigation, old-link behavior, and a reader check. Keep the previous publication and route map available for rollback.

Establish a baseline with members and administrators on the current docs, then test the same tasks on the proposal with order counterbalanced. Report raw outcomes and timings; a small formative study does not establish a population-wide improvement.

| Question | Measure and instrumentation |
| --- | --- |
| Can readers find their instructions? | Observed correct first destination, time to applicable steps, and wrong-context attempts. Add `procedure_view` with allowlisted task/variant IDs and selection origin. |
| Can they complete the right task? | Observe completion and ask what changed: did a skill load, was a plugin attached, whose consent is still needed? Use a task rubric and optional "Did these instructions work?" feedback with reason categories. A page view is not completion. |
| Do old links still help? | Check every inventoried browser/Markdown route and rendered anchor. Browser tests verify task, context, and visible target. Record `legacy_route_resolved` using route IDs. Require all known mappings to pass before release. |
| Does consolidation prevent drift? | At each release, review shared claims and count independently authored duplicates and contradictory statements. Track claim/context corrections, not simply page count. |

Collect no prompts, credentials, repository URLs, or organization identifiers in documentation events. Treat context switching as a clue to investigate, not automatic failure. Set improvement targets after the baseline. The test is whether readers reach the right outcome with the right expectations.
