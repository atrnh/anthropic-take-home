# Project log

| Date | Work and decisions |
| --- | --- |
| Sept. 14 | Establish scope, preserve sources, and set up the repo. [(see details)](#14-september-establish-the-scope-and-preserve-the-sources) |
| Sept. 14–15 | Investigate product overlap through a task matrix, revise the taxonomy, and attempt a full-corpus extraction. [(see details)](#14-and-15-september-investigate-overlap-through-a-task-matrix) |
|  | Trace the effort spent building the analysis workflow, correcting task matches, and reconciling product boundaries. [(see details)](#where-the-effort-went) |
|  | Clarify the information architecture, distinguish shared capabilities from product contexts, and shift toward editorial decisions. [(see details)](#14-and-15-september-clarify-the-information-architecture) |
|  | Revisit my assumptions, recognize the matrix's diminishing returns, and define a smaller investigation for next time. [(see details)](#what-i-learned-and-why-i-would-scope-this-differently) |
| Sept. 15 | Turn the findings into an editorial proposal, audit all 54 pages, and plan navigation and migration. [(see details)](#15-september-turn-the-findings-into-an-editorial-proposal) |
|  | Demonstrate the standards with a plugin-installation rewrite and verify its context-specific workflows. [(see details)](#15-september-demonstrate-the-standards-with-one-worked-page) |
|  | Record the process, plan the remaining deliverables, and establish a time estimate based on human attention. [(see details)](#15-september-record-the-process-and-initial-remaining-work) |
|  | Build and evaluate the duplicate-prose check, compare retrieval methods, and test model-based editorial judgment. [(see details)](#15-september-build-and-evaluate-the-duplicate-prose-check) |
| Sept. 15–16 | Refine the memo's voice and conceptual argument, clarify each page's purpose, and remove obsolete artifacts. [(see details)](#15-and-16-september-refine-the-memo-and-its-presentation) |
|  | Draft an adoption approach around a willing team's work, contributor support, and an advisory check. [(see details)](#15-and-16-september-draft-the-adoption-approach) |
| Sept. 17 | Mark the six-hour checkpoint and identify subsequent work as beyond the budget. [(see details)](#17-september-six-hour-checkpoint) |
|  | Package the deliverables and clean up the submission after the checkpoint. [(see details)](#17-september-submission-cleanup-after-the-checkpoint) |
| Sept. 18 | Refine the deliverables through review, clarify editorial decisions, and record the reasoning behind accepted and rejected changes. [(see details)](#18-september-refine-the-deliverables-through-review) |
| Sept. 15–18 | Export the supporting conversations, refresh later discussions, and link the redacted source records. [(see details)](#conversation-sources) |

Reconstructed on 15 September 2026 and updated through 18 September from repository
artifacts, committed transcripts,
additional local Claude and Codex/ChatGPT conversations, and my retrospective in
the log-writing conversation. Dates use America/Los_Angeles. First-person
reflections are Ashley's; interpretations of the conversation history are labeled.
This is a record of work and decisions, not a timesheet or a claim that the drafts
are ready to publish.

## 14 September: establish the scope and preserve the sources

- Chose skills, plugins, and connectors in Claude Docs as the documentation slice.
  Created a project README and a deliverable checklist in
  the former roadmap, removed during submission cleanup.
- Corrected the initial corpus fetch, which had pulled from Claude Code Docs.
  The exercise concerns `claude.com/docs`; Claude Code and developer-platform
  documentation are outside its scope.
- Saved a [54-page corpus snapshot](corpus/manifest.json) and a
  [fetch script](3-check/docslint/fetch_corpus.py), giving the audit a fixed body of source
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
- Preserved the pilot results and remaining problems, including unresolved
  cross-task overlaps and 54 open questions. The
  [pilot conversation](transcripts/2026-09-14-8e6904c0.md) records this work;
  the pilot files were later removed from the working tree on 16 September.
- Added six newly discovered tasks and cleaned up references to removed product
  IDs across the pilot data, schema, and splitting logic.
- Attempted expansion to all 54 pages, split into 62 work units. Nearly all raw
  extraction workers returned, but the last worker and a retry hit a usage limit.
  The run stopped before validation, merge, and reconciliation produced a final
  inventory. Only the pilot was committed, in `1d77690`; its files remain in
  Git history after the later cleanup.

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

- Developed a detailed [plugin disposition example](1-audit/plugin-disposition-example.md)
  to work through shared concepts, distinct tasks, complete workflow variants,
  and the fate of existing pages and links.
- Extended the editorial pass to every page in the snapshot. Drafted the
  [54-page disposition ledger](1-audit/disposition-ledger.md),
  [audit memo](1-audit/audit-memo.md), and
  [proposed IA and migration plan](1-audit/proposed-ia.md).
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

- Created a [style-guide excerpt](2-standards/style-guide.md) and
  [how-to template](2-standards/how-to-template.md) tied to the audit's
  findings about scope, complete procedures, outcomes, and source evidence.
- Rewrote "Install a plugin" as one task page composed from separately authored
  Cowork and Government workflows. Preserved the original Cowork page, generated
  Markdown and an interactive HTML preview, and documented every original
  section's treatment in the [rewrite package](2-standards/rewrite/README.md).
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
  [recorded verification](2-standards/rewrite/changelog.md#verification)
  covers source preservation, reproducible output, both variants, keyboard
  selection, direct links, unknown context, history navigation, and no-script
  behavior. Those checks establish the demonstration's behavior, not the
  correctness of the live Claude installation UI.

## 15 September: record the process and initial remaining work

- Simplified the root README to describe the project and moved the deliverable
  checklist into the roadmap. I did not want to overdefine the tasks or embed
  implementation assumptions in the checklist.
- Committed the slice-wide audit and standards work and merged it to `main` as
  `bda1f3c`. This was the baseline for the first version of this log.
- Completed a later readability pass in worktree `836b`: broke the audit into
  smaller sections, added an audit-folder README as the short memo, retained and
  linked the supporting drafts, and linked that entry point from the root README.
  Those edits were still uncommitted when this log was first compiled. The
  later commit and integration are recorded below.
- Planned task 3 around a prototype that flags duplicated explanatory prose,
  distinguishing harmful duplication from useful repetition and related but
  different content. Implementation and evaluation followed later that day.
- Planned task 4 around adoption through a willing team's concrete problem and
  the plugin rewrite as a pilot. A working draft followed later that day.
- Added a Codex transcript-dumping skill alongside the Claude version. Kept
  transcript capture separate from the editorial deliverables.
- Asked for project-time estimates and explicitly checked that parallel work was
  not counted twice. A later assistant estimate was about 5 hours 35 minutes.
  I challenged whether I had actually spent that long. The assistant acknowledged
  conflating agent runtime with my attention.
- Clarified that I multitask: unattended agent runtime often does not count,
  while immediate replies usually mean I am still engaged. I reported about
  three hours of work on 14 September and accepted a revised checkpoint of
  **4 hours 15 minutes spent, 1 hour 45 minutes remaining** on 15 September.
  That is an accepted estimate at that point, not a final total or an exact
  six-hour cutoff for the later work.
- Began reconstructing this log from both dumped and undumped conversations.
  Confirmed access to project transcripts for Claude Desktop's Code sessions.
- Added the retrospective above so that the record includes my assumptions,
  corrections, and judgment about effort, alongside artifacts and agent actions.

## 15 September: build and evaluate the duplicate-prose check

- Confirmed that duplicated explanatory prose was the right problem because it
  directly matched the audit. The later change of approach did not change that
  target.
- Built a working checker for repeated explanatory prose against the pinned
  54-page corpus. It retains source text and line numbers, verifies the corpus
  hashes, and reports candidate passage pairs for editorial review.
- The first lexical baseline flagged 18 pairs. Review judged three actionable
  and 15 false positives; it also missed all six positive cases in the small
  audit-derived example set. Saved those results and examples instead of
  presenting the prototype as ready to enforce in CI.
- Created the private `atrnh/anthropic-take-home` GitHub repository and pushed
  the initial prototype as `431298a`. The task recorded passing verification,
  reproducible saved results, and a check that the remote commit and report
  matched the local work.
- Questioned the false positives and whether a deterministic approach was viable.
  I had assumed the check needed to be deterministic; it did not. Shifted toward
  code for extraction, source validation, and evaluation, with a model making
  the editorial judgment about redundancy.
- Explored inexpensive alternatives to embeddings, then chose a small TF-IDF
  comparison before escalating to a heavier approach. Approved fixing the
  extraction gap and then running a bounded model-judge pilot.
- Compared TF-IDF, which weights words and phrases by how distinctive they are,
  with the baseline's three-word overlap method. With the same extracted
  passages, TF-IDF retrieved five of the six known positives at ten candidates
  per passage. The sixth was missing from the extracted text, so changing the
  matcher alone could not recover it.
- Expanded extraction to include short unordered-list prose. On the full corpus,
  TF-IDF then retrieved all six known positives among 6,755 candidate pairs.
  Kept the original baseline and earlier experiment reproducible. This was a
  retrieval result on reused examples, not a measure of editorial accuracy.
- Ran a blinded model-judge pilot on the 16 existing labeled cases and eight
  newly sampled candidates. The judge received source text and context without
  the labels or retrieval scores. Its source and evidence checks passed for all
  24 responses.
- Against the existing labels, the judge produced five true positives, one false
  positive, one false negative, and nine true negatives. It still treated a
  necessary local prerequisite as removable duplication. A correct duplicate
  classification could also recommend the wrong canonical home for the text.
- The experiment's recommendation was to keep TF-IDF and improve the editorial
  rubric before judging the whole queue. The eight new candidates were all
  rejected, with agreement from a separate agent review; that agreement is not
  human ground truth. These small, reused sets do not validate production
  precision or recall.
- Committed the prototype and experiments as `431298a`, `633df9b`, `b3336b6`,
  and `db76af4` on `codex/duplicate-prose-check`. As of this update, that branch
  has not been merged into `main`. Its reports live under `3-check/` on
  that branch, including `README.md`, `tfidf-bakeoff.md`,
  `extraction-followup.md`, and `judge-pilot.md`.

## 15 and 16 September: refine the memo and its presentation

- Brought the introduction from my audit note into the memo, including two
  screenshots comparing the main site's navigation with Claude Docs. Kept the
  supporting drafts and made the audit-folder README the short memo's entry point.
- Asked for a "Silicon Valley professional" voice: casual, concise, more
  contractions, and sentences that sound natural read aloud. I wanted to assume
  an intelligent reader and cut disclosures that did not serve the memo's
  purpose, including repeated scope and testing-status notes.
- Committed that pass on 15 September and integrated it into `main` on
  16 September as `a579ab8`.
- Continued editing the memo around the improvements that matter most: align
  the conceptual model, give each page a clear job, distinguish task outcomes,
  scope instructions to the reader's context, and explain each concept once.
- Connected the IA argument to software architecture: getting the model right
  makes later design decisions easier. A shared concept can have one explanation,
  while how-to instructions and reference material vary with the reader's task
  and context.
- Clarified that docs should support the reader's current stage of work. Someone
  getting started with skills does not need implementation details immediately;
  someone already authoring a skill does not need another basic definition.
  Applied Diátaxis to give each page one clear purpose.
- Committed the streamlined memo on 16 September as `77a1d7c`. That cleanup also
  removed the two screenshots and 115 matrix-pilot files from the working tree.
  Their history and the exported conversations remain available. Added
  `.DS_Store` to the repository ignore rules.

## 15 and 16 September: draft the adoption approach

- Created an [adoption draft](4-adoption/README.md) grounded in my prior
  curriculum and build-system work, rather than treating adoption as a generic
  rollout. It remains a working draft for me to revise in my own voice.
- Asked for the approach to reflect my historical practice using the vault and
  SelfWiki. Accepted the result as "a good start" and asked to commit it, while
  explicitly reserving a rewrite in my own voice.
- Proposed starting with individual conversations and a willing team's real
  documentation problem, using the plugin before/after example to invite
  critique and work through an actual update.
- Connected standards to contributor support: onboarding, acceptance criteria,
  good and bad examples, explanations of reader consequences, and a shared place
  for questions and decisions. The goal is for authors to maintain the content
  without depending on me to rewrite it for them.
- Kept the automated check advisory while contributors assess its usefulness
  and incorrect flags. The draft distinguishes a noisy check, unclear ownership,
  deadline pressure, and a legitimate exception when a team does not follow it.
  Blocking publication would need evidence that the check earns that role.
- Rebasing and integration on 16 September put the draft and its roadmap link
  on `main` as `c3af9e6`. This records a proposed adoption approach, not a
  completed rollout or approved final submission.

## 17 September: six-hour checkpoint

- Marked **6 hours of project time spent, 0 hours remaining in the six-hour
  budget** at my request on 17 September 2026, at approximately 10:35 a.m. PDT.
  This is my declared checkpoint, using the human-attention basis established
  above. Work after this point falls beyond the six-hour budget.

## 17 September: submission cleanup after the checkpoint

The four deliverables now live at the repository root, with their entry points
linked from the main README. The obsolete roadmap and a tracked Python cache
were removed. The saved corpus and frozen checker evidence were preserved.
The checker runs from its new location, and the rewrite and checker checks pass.

The earlier adoption section records the initial draft. At this point, the response
incorporated the later campaign-style rewrite and had been condensed to three
paragraphs, with the template and advisory check tied to a willing team's update.
SHARE-01 now makes the audit's shared-explanation rule explicit in the style guide.
These edits, the portable rewrite build, and the packaged checker workflow are
post-checkpoint work. The root README distinguishes them from the earlier artifacts.

## 18 September: refine the deliverables through review

- Reviewed the deliverables with Claude for both functional correctness and the
  reader's experience. Asked for more than working links and accurate prose:
  the documents should have flow, anticipate readers' needs, and reward their
  attention. Today's work is after the six-hour checkpoint; I have not declared
  an additional time total.
- Reworked the [standards introduction](2-standards/README.md) around the
  problem, the standard, and what the plugin rewrite demonstrates. Added a
  chooser screenshot, removed duplicate link lists and build instructions, and
  made the administrator question use the chooser's actual labels.
- Gave each style rule its own section, moved build mechanics out of the how-to
  template, and replaced submission-facing scope notes with design decisions.
  The standards conversation records a rebuilt preview and passing verification.
- Added a GitHub Pages publishing workflow, but the hosted preview was not
  deployed. Claude reported that the private repository's plan prevented Pages
  activation. The workflow remains available for later use.
- Corrected the audit review's interpretation of "priority": I meant the most
  important fixes, not the order in which to implement them. Kept aligning the
  docs with how Claude works as the leading recommendation. Asked why the memo
  needed another scope preamble, then chose my earlier version over Claude's
  broader rewrite while retaining targeted accuracy corrections.
- Narrowed the Government plugin claim to plugins a user uploads themselves,
  whose declared connectors are not added. Clarified that the skills gap is in
  the authoring guide, which teaches scripts without mentioning Government's
  text-only upload requirement. Kept my navigation tree beside the recommendation
  it illustrates. These changes were committed as `ecef820`.
- Revised the [adoption playbook](4-adoption/README.md) around the campaign
  sequence: listen, collect endorsements, develop the message, lower the cost of
  participation, and govern responsibly. This supersedes the three-paragraph
  response described in the 17 September entry.
- Explained why trust is the frame I want for adoption. A noisy check undermines
  confidence in its output; unclear ownership undermines confidence that engaging
  will lead anywhere. The response should address what people cannot trust.
- Drew on a team that resisted my recommendations. I prioritize freedom and
  informed consent, assume people may know something I do not, and want them to
  own their decisions. Bringing in stakeholders is about including the people
  affected in proportion to the decision's consequences, rather than routinely
  escalating disagreement. Kept this brief instead of adding the full story.
  The revised playbook was committed as `3b4d123`.
- Recast the [checker README](3-check/README.md) as the story of its experiments,
  starting with the independently labeled examples and proceeding through
  retrieval, judge revisions, and fresh cases. Asked Claude to unpack claims
  about Drive, the slug warning, local prerequisites, and v4 until the prose
  explained the actual editorial decisions. These were explanations of earlier
  experiments, not new judge runs on 18 September.
- Made the v4 account follow the disagreement and subsequent label review,
  rather than requiring readers to reconcile an interim score with labels that
  later changed. Preserved historical scores and distinguished my decisions on
  five original cases from the agent labels retained for the other eleven.
- Updated SHARE-01 with the resulting rules: choose an explanation's home by
  who it applies to, not its current location or length, and merge relevant
  general facts from a specialized page before shortening that page to a link.
  Committed this with the narrative rewrite as `9716838`; the follow-up cleanup
  added Stage 0 to the timeline and corrected portability claims in `d1b7905`.
- Simplified the root README around the four deliverables and their own evidence
  links, removing a redundant experiments list. Clarified the post-checkpoint
  work and committed the introduction as `afd5185`.
- Obtained a separate content review of the worked plugin page. It raised
  routing gaps for Team and Enterprise members and inconsistent wording between
  the variants. That conversation records findings, not an implemented fix;
  those suggestions still need a decision and source checks where indicated.
- Exported today's five Claude conversations and linked them below, preserving
  the accepted edits, rejected rewrites, and my reasoning as well as the work.

## Conversation sources

The original source snapshots were exported on 15 September 2026. On 16
September, four exports were refreshed and three conversations were added.
On 18 September, five Claude project conversations from that day were exported.
The Claude and Codex exports include user and assistant messages, tool calls,
and truncated tool results. The ChatGPT architecture discussion contains the
messages available through the app; its original search results were unavailable.
The take-home prompt and identifying values are redacted; hidden instructions,
reasoning, and attached app screenshots are omitted. Message counts below are
the exporters' counts, not counts of human turns.

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
- [Time-estimate discussion](transcripts/2026-09-15-01a0a6be.md) · Codex/ChatGPT · 19 messages.
- [Task 3 planning](transcripts/2026-09-15-01a0a6db-4c58.md) · Codex/ChatGPT · 72 messages.
- [Task 4 planning](transcripts/2026-09-15-01a0a6db-85a2.md) · Codex/ChatGPT · 13 messages.
- [Audit readability pass](transcripts/2026-09-15-01a0a6e4.md) · Codex/ChatGPT · 27 messages.
- [This log and Ashley's retrospective](transcripts/2026-09-15-01a0a6eb.md) · Codex/ChatGPT · 19 messages.
- [Add architecture foundation sentence](transcripts/2026-09-16-01a0abf6.md) · Codex/ChatGPT · 6 messages.
- [Commit all changes](transcripts/2026-09-16-01a0ac9a.md) · Codex/ChatGPT · 10 messages.
- [Semantic Deduplication Architecture](transcripts/2026-09-15-6aa9d341.md) · ChatGPT · 5 messages.
- [Standards presentation and preview publishing](transcripts/2026-09-18-aedcab04.md) · Claude · 14 messages.
- [Adoption, trust, and informed consent](transcripts/2026-09-18-70fa253d.md) · Claude · 15 messages.
- [Audit priorities and accuracy fixes](transcripts/2026-09-18-302a8a1a.md) · Claude · 22 messages.
- [Checker narrative, SHARE-01, and repository introduction](transcripts/2026-09-18-b2b3975b.md) · Claude · 44 messages.
- [Worked rewrite content review](transcripts/2026-09-18-b96dc4b1.md) · Claude · 2 messages.

All 23 supporting conversations referenced here have local exports. The seven
conversations used for the 16 September update are captured through their
latest available messages at that export time. Today's five Claude exports are
18 September snapshots; the remaining exports retain their original snapshots.

The original artifact check used `main` at `c3af9e6` and the separate checker
branch at `db76af4`. The 18 September update was checked against `main` at
`afd5185`, which includes the packaged checker and subsequent editorial work.
Earlier unmerged-branch descriptions record their status at that earlier point.
Dates describe when work happened; later rebases can change commit identifiers.
