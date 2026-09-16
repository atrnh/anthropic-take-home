# Audit Memo

## Improvements that matter most

### Align docs with how Claude actually works

Claude Docs lists connectors, skills, and plugins as products, but they aren't. The main
site navigation gets it right: they're capabilities that work across many products.

Organize the docs the same way. Lead with **Skills**, **Plugins**, and **Connectors**
belong together, with tasks under each: use a skill, install a plugin, connect a service.
Add **Administer extensions** and **Build and publish** for readers doing that work.
Product landing pages stay as entrances to the same pages, so most URLs don't need to
move. The [proposedIA](proposed-ia.md) maps the full slice.

### Give each page one clear job

Docs should meet users where they are. Someone just getting started doesn't need to know
about `SKILL.md` files or progressive disclosure yet. Someone in the middle of authoring a
skill doesn't need to be told what a skill is.

Pick one Diátaxis mode (tutorial, explainer, how-to guide, reference) for each page and
stick to it.

This gets easier after [aligning the docs with
reality](#align-docs-with-how-claude-actually-works): we know that skills are conceptually
the same across all products, so [the page on connectors and skills for Claude
Science](../../corpus/claude-science/connectors-and-skills.md) can be decomposed into
universal explainers (what a connector/skill is), tutorials (how to get started with
connectors/skills), how-tos (how to add a skill), and product-specific reference (list of
connectors/skills included with Claude Science).

### Separate tasks with different outcomes

Readers arrive with a goal in mind. The docs should help readers choose the job they're
trying to do before showing them the steps. Each how-to guide should name one outcome and
make it clear when the reader is done. A custom skill and a published distribution of a
skill are two different outcomes.

Sharing a product name doesn't make two tasks the same. [Attaching GitHub
files](../../corpus/connectors/github/index.md) and [using GitHub MCP
tools](../../corpus/third-party/claude-desktop/connectors-github.md) get readers different
results, so they need different guides. "Done" needs the same care: in Government, an
installed plugin doesn't connect its bundled tools, so "installed" and "ready to use" need
separate checks.

### Scope instructions to the reader's context

The same capability can work differently depending on where someone uses Claude and how
their organization provides access. Instructions written for one context read as universal,
and readers in other contexts hit dead ends with no idea why.

State prerequisites where they apply, and when a step needs an admin, tell the reader what
to ask for. When steps differ by context, put each context's workflow on the same task page.
Ask readers to choose only when the choice changes the steps, and tell them how to find out
which context they're in. The [worked example](../2-standards/rewrite/README.md) shows this
on "Install a plugin."

The [connector overview](../../corpus/connectors/overview.md) says prebuilt integrations
need nothing beyond authentication, but [Microsoft
365](../../corpus/connectors/microsoft/365.md) needs tenant consent and, on Team and
Enterprise, admin enablement. Skills have the same gap: the [authoring
guide](../../corpus/skills/how-to.md) allows scripts, while
[Government](../../corpus/government/desktop/skills.md) requires text-only skills in a
plugin wrapper.

### Explain each concept once

Every duplicate explanation is one more thing to keep accurate, and duplicates drift apart.
Readers who find two versions can't tell which one to trust.

Give each concept one home and link to it from everywhere else.

The [plugin overview](../../corpus/plugins/overview.md) repeats the plugin directory and
promises org management that [the Cowork guide already
documents](../../corpus/cowork/guide/plugins.md). Detailed specialist references aren't
duplicates, though, and can stay.


## Principles behind the proposal

I'd use these rules throughout. The
[content and presentation proposal](proposed-ia.md#author-complete-procedures-compose-the-readers-view)
goes into more detail.

- Give shared content one home and several ways to find it. Keep the existing
  entry points for readers who start with where they use Claude.
- Keep context choices distinct. Where you're working, how your organization
  provides access, your permissions, and your installation method aren't the same
  thing. Don't put Cowork, Government, and ZIP upload in one dropdown.
- Make the task the destination. Write complete workflows in separate Markdown
  files, then bring the right one into the task page. Readers shouldn't have to
  piece together a procedure from scattered exceptions.
- Ask for context only when it changes the steps. Put **How to check** beside the
  choice, and explain what to ask an admin if readers can't identify their setup.
  A setting that carries across tasks isn't the same as a local choice of method.
- Honor the context in a shared link, even if the reader has a different saved
  preference. Show which instructions they've landed on. Keep comparisons where
  they help readers choose, such as M365's local and remote data paths.
- Don't claim more than the evidence supports. A generic page doesn't mean a
  feature works everywhere. A missing procedure doesn't mean it's unsupported.

Give each page a clear job using Diátaxis. Tutorials teach through practice.
Explanations build understanding. How-to guides get a task done. Reference pages
make details easy to look up. Share a procedure when the person doing it, the
steps, and the outcome match. Keep complete variants when they don't. The
[Install a plugin rewrite](../2-standards/rewrite/README.md) shows how separate
sources come together on one task page.

## Proposed navigation

Here's how I'd organize **Extend Claude**. The
[full proposed tree](proposed-ia.md#organize-by-capability-and-task) expands the
service, authentication, MCP Apps, and tunnel sections.

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
└── Build and publish extensions
    ├── Choose MCP, a plugin, or both
    ├── Understand MCP
    ├── Build a connector or desktop extension
    ├── Implement authentication
    ├── Build MCP Apps
    ├── Test and troubleshoot connectors
    ├── Choose directory or custom distribution
    ├── Check submission requirements
    ├── Submit a connector or plugin
    └── Update integrations and manage listings
```


## What to merge or remove, and where old links go

Publish replacements before adding redirects. When an old page served several tasks, turn
it into a short "choose your task" page instead of redirecting everyone to one destination.
Keep legacy anchors in place, since redirects can't see URL fragments, and include `.md`
routes and `llms.txt`.

Migrate one family at a time, starting with plugin installation and Government skill
packaging. Product owners resolve the ledger's open questions first, and the previous build
stays available for rollback.

| Content decision | What readers following old URLs get |
| --- | --- |
| Share definitions and identical passages; remove duplicate catalog and promotional prose. | Existing overview URLs remain. Removed-section anchors point to the surviving explanation or directory. |
| Compose installation, management, and administration from complete workflow variants. | Multi-task URLs remain short task-choice pages with their context and real legacy anchor targets. The Government plugins URL still offers install, create, and manage. |
| Relocate the financial-services collection, Science custom connectors, and managed-Desktop GitHub and M365 setup. | Publish replacements first, then redirect the four pages with their context and heading targets preserved. |
| Consolidate listing guidance while retaining runtime and plugin update tasks. | The old after-publishing URL retains runtime guidance and routes readers to the appropriate listing or plugin task. |

The [relocation map](proposed-ia.md#preserve-incoming-intent) and
[ledger](disposition-ledger.md) show where each page goes. Check heading anchors
and `.md` routes, and update `llms.txt`. A server redirect can't read a URL
fragment. Keep the old anchor targets or handle those links in the browser, and
check that readers reach the right task and context.

## How to migrate

1. Work with doc owners to settle the claims that affect the steps: archive
   rules, availability, and legacy Slack behavior. Record the evidence and review
   date. See the [publication questions](disposition-ledger.md#publication-questions-to-resolve).
2. Watch members and admins try the current docs. That's the baseline.
3. Start with plugin installation and distribution, plus Government skill
   packaging. Then move to connector setup and administration. Each batch needs
   complete content, an owner, navigation, and working old links.
4. Test each batch with readers. Check keyboard access, shared links, print, and
   pages without JavaScript. Ship content and routing together, and keep the
   previous version and route map so we can roll back.

The [migration plan](proposed-ia.md#migrate-in-reader-testable-batches) has the
scenarios we'll use to check each batch.

## How to know it works

Have readers try the same tasks before and after. Vary the order so practice
doesn't skew the results. Compare completion, wrong-context attempts, and time
to the right instructions against the baseline.

| Question | Measure and instrumentation |
| --- | --- |
| Can readers find the right instructions? | Track whether their first destination is correct, how long it takes to find the right steps, and wrong-context attempts. Record `procedure_view` with task, variant, and selection-origin IDs. |
| Can they finish and explain the outcome? | Check what happened: did the skill load, was the plugin attached, whose consent is still needed? Pair observed completion with optional task feedback and reason categories. A page view doesn't tell us the task is done. |
| Do old links preserve intent? | Check every inventoried browser/Markdown route and rendered anchor. Browser checks verify task, context, and visible target; `legacy_route_resolved` records route IDs. Require every known mapping to pass before release. |
| Does consolidation reduce drift? | Review shared claims at each release; count independently authored duplicates and contradictions, recording corrections by claim and context. Page count alone says little. |

Use allowlisted task, variant, and route IDs in analytics. If readers switch
contexts, check why. They might be comparing workflows. See the
[detailed measurement proposal](plugin-disposition-example.md#measurement-proposal).

## Supporting drafts

- [Audit findings draft](audit-memo.md) develops the prioritized argument.
- [Disposition ledger](disposition-ledger.md) records each page's evidence,
  treatment, priority, and old-URL behavior.
- [Proposed IA and migration](proposed-ia.md) gives the full tree, destination
  scopes, and acceptance scenarios.
- [Plugin disposition example](plugin-disposition-example.md) traces one family
  through evidence, procedure ownership, old links, and measurement.
