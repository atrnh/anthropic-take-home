# Project log

Reconstructed on 15 September 2026 from repository artifacts, committed transcripts,
additional local Claude and Codex/ChatGPT conversations, and my retrospective in
the log-writing conversation. Dates use America/Los_Angeles. First-person
reflections are Ashley's; interpretations of the conversation history are labeled.
This is a record of work and decisions, not a timesheet or a claim that the drafts
are ready to publish.

## 14 September: establish the scope and preserve the sources

- Chose skills, plugins, and connectors in Claude Docs as the documentation slice.
  Created a project README and a deliverable checklist in
  [the roadmap](docs/roadmap.md).
- Corrected the initial corpus fetch, which had pulled from Claude Code Docs.
  The exercise concerns `claude.com/docs`; Claude Code and developer-platform
  documentation are outside its scope.
- Saved a [54-page corpus snapshot](corpus/manifest.json) and a
  [fetch script](docslint/fetch_corpus.py), giving the audit a fixed body of source
  material to inspect and cite.
- Added a Claude transcript-dumping skill and saved the setup conversation.
  Refined redaction to remove personal identifiers and the take-home prompt by
  default, then regenerated the transcript.

## 14 and 15 September: investigate overlap through a task matrix

- Reframed the inventory as a task/procedure/difference matrix. The question was
  how much the documented work overlaps across products, which procedures are
  shared, and where instructions actually differ. A task such as installing a
  plugin can have several procedure families and variants.
- Explored an agent workflow for extracting procedures from the corpus and
  reconciling them across pages. Built a task-matrix skill, taxonomy, structured
  extraction records, validation, and rendered inventories.
- Ran an 11-page pilot, then revised and reran it. The revised pilot split the
  pages into 14 work units, accepted 79 extraction records, and reconciled 33
  tasks into 45 procedure families and 58 variants. These are pilot results,
  not counts for a completed full-corpus matrix.
- Reworked the classification model. Separated product, actor, interface,
  mechanism, and outcome; moved audience categories out of the product list;
  and separated the product/task view from the builder view.
- Changed task matching from similar wording to the outcome of the procedure.
  Browsing the plugin directory, for example, does not accomplish installing a
  plugin. Added targeted source reads during reconciliation so that a plausible
  extraction could be challenged against the original instructions.
- Removed gap identification from the scope so that the output stayed focused
  on the inventory and its appendix.
- Consolidated claude.ai, Desktop, and Cowork into one product category for the
  pilot, with client or mode recorded separately. The pilot still flagged
  third-party-inference Desktop as a deployment being represented as a product.
  This was a working taxonomy, not a settled model of the entire product family.
- Preserved the [pilot results and remaining problems](docs/1-audit/task-matrix/pilot/README.md),
  including unresolved cross-task overlaps and 54 open questions.
- Added six newly discovered tasks and cleaned up references to removed product
  IDs across the pilot data, schema, and splitting logic.
- Attempted expansion to all 54 pages, split into 62 work units. Nearly all raw
  extraction workers returned, but the last worker and a retry hit a usage limit.
  The run stopped before validation, merge, and reconciliation produced a final
  inventory. Only the pilot is preserved in the current checkout.

### Where the effort went

- **Inference from the conversations:** the recurring effort was building and
  repairing the analysis workflow and its classification model. This is a
  qualitative account, not a measured allocation of hours.
- Built schemas, taxonomy entries, agent instructions, and scripts to split,
  validate, merge, and render the source extractions before the matrix could
  answer the original editorial questions.
- Ran the pilot twice, changed the matching rules, and reread source passages to
  correct plausible but wrongly grouped procedures.
- Repeatedly revisited product boundaries. Merging web, Desktop, and Cowork
  categories required remapping records and reconciling affected tasks again.
  A later audit still found stale product IDs in 28 matrix files and in the
  workflow code.
- Continued into a full-corpus extraction even though the pilot had already
  exposed the category problem. The resulting raw extractions did not become a
  completed, validated matrix.

## 14 and 15 September: clarify the information architecture

- Researched ways to organize overlapping documentation across products and
  audiences, including task-first, product-first, and hybrid structures. The
  suggested hybrid was a hypothesis to test, not a validated navigation design.
- Articulated the category problem: the existing navigation presents unlike
  things as peer "products." Shared capabilities, places where Claude is used,
  deployment conditions, and administrative roles need to be distinguished.
- Questioned whether web and desktop should count as separate products when the
  desktop client mainly adds local file and command access. The research response
  recommended one product with client-specific variants; that recommendation did
  not by itself establish a definitive product taxonomy.
- Explored an initial IA draft and visualization with Claude, then asked to
  delete that written draft because I did not like how it was written. This does
  not establish rejection of every underlying idea. The proposal now in the
  repository was written later with Codex.
- Shifted toward an editorial disposition pass after revisiting the deliverables.
  The practical decisions were what to retain, merge, split, remove, or redirect,
  and how to test whether the proposed structure helps readers.

### What I learned, and why I would scope this differently

- Before the matrix, I assumed Claude for Government was an alternative version
  of Claude Desktop, similar to my understanding of Claude Science. I came to
  understand it as a government administration panel for Claude Desktop instead.
  That change in my mental model helped me recognize how confusing the existing
  information architecture was.
- I also expected skills, connectors, and plugins to share their underlying
  concepts across products, but I was not confident because my own experience
  was with Claude Code and Claude Desktop. Seeing skills thoroughly documented in
  Claude Code Docs but not comparably in Claude Docs made me question that
  assumption. The analysis gave me confidence in the conceptual overlap.
- Shared concepts do not make every procedure interchangeable. The later audit
  preserves differences in administration, packaging, permissions, installation,
  and what counts as a successful outcome. These are conclusions drawn from the
  documentation exercise, not fresh verification of every product's behavior.
- The matrix was difficult to construct because the information architecture and
  product boundaries were not well understood to begin with. Defining the rows
  and columns required resolving part of the problem the matrix was supposed to
  investigate.
- I recognized fairly quickly that the exercise was becoming less productive,
  but kept going out of "morbid curiosity." It still belongs in the account of
  time spent on this project, with that caveat. The useful discoveries do not
  mean all of the subsequent effort was necessary to reach them.
- Next time, I would make this a smaller, disposable investigation with two
  questions: how severe is the overlap, and do the sources support my assumptions
  about the IA? I should have stopped once Fable began struggling to reconcile
  the product boundaries, recorded that confusion as a finding, and moved on.

## 15 September: turn the findings into an editorial proposal

- Developed a detailed [plugin disposition example](docs/1-audit/plugin-disposition-example.md)
  to work through shared concepts, distinct tasks, complete workflow variants,
  and the fate of existing pages and links.
- Extended the editorial pass to every page in the snapshot. Drafted the
  [54-page disposition ledger](docs/1-audit/disposition-ledger.md),
  [audit memo](docs/1-audit/audit-memo.md), and
  [proposed IA and migration plan](docs/1-audit/proposed-ia.md).
- Proposed capability and task entries for skills, plugins, and connectors, with
  administration and building/publishing routes for distinct work. Existing
  product/context entry points can lead to the same canonical instructions.
- Prioritized misleading applicability and incomplete outcomes before navigation
  cleanup. Examples include Microsoft 365's administrator/member handoff,
  Government skill packaging, and the difference between uploading, installing,
  attaching, and actually being ready to use an extension.
- Distinguished tasks that share a name but produce different results, such as
  adding GitHub files and configuring GitHub MCP tools. Proposed removing
  duplicated explanations while preserving specialist references and unique
  procedures.
- Recorded migration behavior for old URLs, section anchors, Markdown routes,
  and `llms.txt`. Proposed retaining task-choice pages where a single old URL
  serves several intents, rather than sending every reader to one replacement.
- Added a proposed measurement approach: test whether readers find applicable
  instructions, complete the intended task, and retain their context when
  following old links. No reader study, production redirect, or documentation
  migration has been carried out by these drafts.

## 15 September: demonstrate the standards with one worked page

- Created a [style-guide excerpt](docs/2-standards/style-guide.md) and
  [how-to template](docs/2-standards/how-to-template.md) tied to the audit's
  findings about scope, complete procedures, outcomes, and source evidence.
- Rewrote "Install a plugin" as one task page composed from separately authored
  Cowork and Government workflows. Preserved the original Cowork page, generated
  Markdown and an interactive HTML preview, and documented every original
  section's treatment in the [rewrite package](docs/2-standards/rewrite/README.md).
- Required identification help beside the workflow chooser. Readers cannot be
  expected to know their setup; the page needs a short "How to check" explanation
  and an administrator-question fallback where the sources do not establish a
  reliable visible identifier.
- Kept this to one complete example rather than a new documentation platform.
  Separate source files own the procedures; the selector controls which content
  the reader sees.
- Asked for an explicit separation between editable `source/`, compiled
  `generated/`, and preserved `snapshots/` so that future edits go to the right
  files.
- Ran artifact checks and browser checks during the rewrite work. The
  [recorded verification](docs/2-standards/rewrite/changelog.md#verification)
  covers source preservation, reproducible output, both variants, keyboard
  selection, direct links, unknown context, history navigation, and no-script
  behavior. Those checks establish the demonstration's behavior, not the
  correctness of the live Claude installation UI.

## 15 September: record the process and remaining work

- Simplified the root README to describe the project and moved the deliverable
  checklist into the roadmap. I did not want to overdefine the tasks or embed
  implementation assumptions in the checklist.
- Committed the slice-wide audit and standards work and merged it to `main` as
  `bda1f3c`. This is the baseline present in this checkout.
- Completed a later readability pass in worktree `836b`: broke the audit into
  smaller sections, added an audit-folder README as the short memo, retained and
  linked the supporting drafts, and linked that entry point from the root README.
  At the time of this log, those edits remain uncommitted in that separate
  worktree and are not included here.
- Planned task 3 around a prototype that flags duplicated explanatory prose,
  distinguishing harmful duplication from useful repetition and related but
  different content. The detector and its evaluation have not been implemented.
- Planned task 4 around adoption through a willing team's concrete problem and
  the plugin rewrite as a pilot. The adoption write-up has not been produced.
- Added a Codex transcript-dumping skill alongside the Claude version. Kept
  transcript capture separate from the editorial deliverables.
- Asked for project-time estimates and explicitly checked that parallel work was
  not counted twice. A later assistant estimate was about 5 hours 35 minutes.
  That is a historical estimate, not a verified total or an established six-hour
  cutoff; this log does not use it to manufacture a before/after boundary.
- Began reconstructing this log from both dumped and undumped conversations.
  Confirmed access to project transcripts for Claude Desktop's Code sessions.
- Added the retrospective above so that the record includes my assumptions,
  corrections, and judgment about effort, alongside artifacts and agent actions.

## Conversation sources

Exported on 15 September 2026. Each file includes user and assistant messages,
tool calls, and truncated tool results. The take-home prompt and identifying
values are redacted; hidden instructions and reasoning are omitted. Message
counts below are the exporters' counts, not counts of human turns.

- [Setup](transcripts/2026-09-14-43576142.md) · Claude · 33 messages.
- [Matrix design and pilots](transcripts/2026-09-14-8e6904c0.md) · Claude · 106 messages.
- [Matrix expansion](transcripts/2026-09-15-3f59ef48.md) · Claude · 33 messages.
- [Claude IA discussion](transcripts/2026-09-14-724ead7b.md) · Claude · 9 messages.
- [Matrix workflow design](transcripts/2026-09-14-01a0a13a.md) · Codex/ChatGPT · 12 messages.
- [Cross-product IA research](transcripts/2026-09-14-01a0a128.md) · Codex/ChatGPT · 12 messages.
- [Product-boundary research](transcripts/2026-09-15-01a0a63a.md) · Codex/ChatGPT · 6 messages.
- [IA decisions](transcripts/2026-09-14-01a0a236.md) · Codex/ChatGPT · 14 messages.
- [Worked rewrite and standards](transcripts/2026-09-15-01a0a67f.md) · Codex/ChatGPT · 44 messages.
- [Slice-wide audit](transcripts/2026-09-15-01a0a6c9.md) · Codex/ChatGPT · 15 messages.
- [Time-estimate discussion](transcripts/2026-09-15-01a0a6be.md) · Codex/ChatGPT · 13 messages.
- [Task 3 planning](transcripts/2026-09-15-01a0a6db-4c58.md) · Codex/ChatGPT · 4 messages.
- [Task 4 planning](transcripts/2026-09-15-01a0a6db-85a2.md) · Codex/ChatGPT · 4 messages.
- [Audit readability pass](transcripts/2026-09-15-01a0a6e4.md) · Codex/ChatGPT · 16 messages.
- [This log and Ashley's retrospective](transcripts/2026-09-15-01a0a6eb.md) · Codex/ChatGPT · 19 messages.

All 15 referenced conversations now have local exports. The current conversation
is a snapshot taken during this export task. Artifact status in the log was
checked against `bda1f3c` and the additional local work described above.
