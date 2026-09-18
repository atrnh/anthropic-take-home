# Duplicate-prose review workflow

This workflow helps an editor find explanations that belong in one shared home,
as the [SHARE-01 rule](../2-standards/style-guide.md#share-01-give-each-explanation-one-home)
requires. It retrieves similar passages from the Claude Docs snapshot and shows
them side by side, with source lines and surrounding context. The editor decides
what to merge, shorten, or keep.

The [usage guide](usage.md)
covers setup and the report, and the [worked example](worked-example.md) walks through a human review of the retrieval report.

The project began as a checker meant to flag duplicates for an editor to fix, but I also
wanted to see if an agent could reliably decide which duplicates should be consolidated
and propose the right edit. I got varied results, but they are still promising enough to
give a human editor useful information.

## What the workflow does

The input is the checked-in [54-page snapshot](../corpus/manifest.json) (fetched
Sept. 14, 2026). The loader verifies each file against its recorded hash. Source links in
the report point to that snapshot, not to live documentation.

The extractor takes prose paragraphs, unordered list items, and contiguous
numbered checklists of at least 10 words. TF-IDF weights words by how distinctive
they are across the corpus and scores every passage against every other, within
a page and across pages. The workflow keeps each passage's 20 best-scoring
neighbors, in both directions.

The [starter command](usage.md#start-here) produces **1,027 passages and 13,786
candidate pairs** and writes the queue, a static HTML report with search and
page-pairing filters, line-numbered source copies, and a run summary. It makes no
model calls, needs no API key or server, and doesn't save decisions or edit
documents. Similarity measures wording overlap, not whether an edit is warranted.

## How it evolved


| Stage                    | Question                                                      | What happened                                                          | What changed                                         |
| ------------------------ | ------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------- |
| 1. Exact-wording checker | Can shared wording flag duplicates?                           | 18 pairs, 3 useful; 0 of 6 known duplicates found                      | Split retrieval from judgment                        |
| 2. Better retrieval      | Can a ranked search reach the known duplicates?               | TF-IDF found 5 of 6; the sixth was never extracted                     | Extract list items and shorter passages; 6 of 6      |
| 3. Model judgment, v1–v5 | Can a model tell useful consolidation from needed repetition? | Unstable verdicts; right labels with wrong edits; wrong labels exposed | Clarified the editorial policy with human review     |
| 4. Fresh cases           | Does any of it hold on new examples?                          | Two retrieval misses; the judge still varied between runs              | Extract numbered checklists; retrieve 20 neighbors   |
| Current workflow         |                                                               | Every candidate goes to an editor                                      | Model advice is optional and can't remove candidates |

### Stage 0: evaluation set

An agent picked 16 passage pairs. It labeled each one as a duplicate or not, using
findings from the [audit](../1-audit/README.md) and the surrounding source text. The
result was 6 duplicates and 10 negatives.

These were an agent's judgments, not verified answers. I re-evaluated five cases
during [Stage 3](#stage-3-can-a-model-judge-the-overlap).

### Stage 1: exact wording finds the wrong things

The [first checker](pilot/README.md) was the naive attempt: it compared three-word sequences between
paragraphs of 15 words or more and flagged pairs that shared at least half of
them. It found 18 pairs. After review, 3 were actionable and 15 were false
positives, mostly necessary warnings and prerequisites that each page needs
locally. It also missed all six duplicates in the evaluation set.

Raising the threshold wouldn't help, because the most exact matches were the
necessary notices. That separated two jobs: *retrieval*, reaching real duplicates
without drowning the editor, and *judgment*, deciding which overlaps are worth
consolidating. I worked on them separately from then on.

### Stage 2: ranking instead of a threshold

The [retrieval bake-off](pilot/tfidf-bakeoff.md) replaced the fixed threshold
with each passage's top-k neighbors and compared trigram overlap with TF-IDF on
the same 661 passages. Switching to top-k alone let trigrams recover 3 of 6
known duplicates. TF-IDF reached 4 of 6 at top 5 and 5 of 6 at top 10, so I
kept it.

The sixth case was Drive. Its passages were an 11-word bullet and a 10-word FAQ
answer, and the extractor skipped both list items and anything under 15 words.
The [extraction follow-up](pilot/extraction-followup.md) admitted unordered list
items and lowered the minimum to 10 words. With 980 passages, TF-IDF top 10
retrieved all 6.

### Stage 3: can a model judge the overlap?

GPT-5.6-Terra at high reasoning effort was used as the judge. It received each pair's source passages and neighboring context, without
labels or similarity scores. It could propose consolidation, keep necessary
repetition, call the content related but distinct, or defer. Each run also mixed
in eight newly sampled candidates from the queue.

| Version                                     | Change                                    | Result on the 6 duplicates                                 | Lesson                                                  |
| ------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------- |
| [v1](pilot/judge-pilot.md)                  | Original rubric                           | 5 found; 1 false positive; kept Drive                              | Promising labels, unreliable edits                      |
| [v2](pilot/judge-v2/README.md#what-changed) | Justify every reader task and destination | 0 found; deferred Drive                                            | Protecting local use became a reason to keep everything |
| [v3](pilot/judge-v2/prompt-v3.md)           | Allow partial consolidation               | 5 found; deferred Drive                                            | Recovered findings; still chose homes by length         |
| [v4](pilot/judge-v2/prompt-v4.md)           | Case-by-case FAQ policy                   | Kept Drive; disagreed with 4 other labels                          | Its "errors" exposed label disagreements                |
| [v5](pilot/judge-v5/README.md)              | Revised labels and policy; two runs       | 3 and 4 of 6; no false positives                                   | Clearer expectations, still unstable                    |

#### v1

The first run matched 14 of 16 labels.

Its false positive was the identical owner-enablement prerequisite on the Gmail and
Calendar pages: it offered to remove one copy, although each connection procedure needs
it. It made the same mistake with the slug duplication, which it recognized correctly but
proposed fixing by deleting the one-line locked-slug warning beside the listing's editing
instructions. Twice, v1 matched on identical wording and ignored the local requirements
its rubric told it to protect. v2 was written to address that.

#### v2

v2 asked the judge to explain each passage's reader task and justify any
destination. It overcorrected: it treated different page tasks as reasons to keep
whole explanations, and missed both Government plugin definitions, the skill
definition, the sales example, and the slug. I rejected it.

#### v3

v3 went back to v1 with one narrow change: shorten the shared portion of a
passage and keep what's needed locally. It recovered the other five duplicates,
rejected all ten negatives, and put the slug explanation under listing
management. But it still chose the sales example's destination because that
example was longer, and length doesn't establish ownership. One run also
couldn't show it was better than the v1 control, so the
[comparison](pilot/judge-v2/README.md#results-and-decision) keeps both results.

#### v4

v4 added a rule I decided after v3: brief repetition that helps readers scan or find a
quick answer can stay, but longer repeated explanations should still be merged. With that
rule, v4 correctly kept Drive.

It disagreed with the labels on four other cases. It kept two Government definitions and
the slug, which the labels said to merge, and it wanted to merge a financial-services
marketplace procedure, which the labels said to keep. At first that looked like v4 had
gotten worse. So I reviewed those four cases myself instead of trusting the labels.

The judge was right about the marketplace procedure: it should be merged. It was wrong
about the other three, but the labels hadn't said how to merge them either. The Government
pages, for example, contained general information that belonged in the overview pages
first.

That review settled two principles, which I added to
[SHARE-01](../2-standards/style-guide.md#share-01-give-each-explanation-one-home):

- **A page's location doesn't decide who a fact applies to.** General information in a
  Government guide can belong in the general overview.
- **Unique information can be a reason to merge, not only to keep.** The shared home may
  need facts from both passages before the other page can shrink to a link.

I recorded these decisions as a new
[adjudicated set](pilot/judge-v5/examples-adjudicated.json) and left the historical
scores unchanged. Five of its 16 cases carry my decisions; the other eleven keep the
agent's labels.

#### v5

v5 built those decisions into one revision, then stayed frozen for two runs
on the familiar cases. The runs found 3 and 4 of 6 duplicates with no false
positives. Both missed the slug, and they disagreed on the Government definitions
and the marketplace procedure. I didn't keep revising the prompt or retrying
until the scores looked better.

### Stage 4: fresh cases

I then chose six fresh pairs, three duplicates and three that should stay, and
approved their decisions and expected edits before either v5 run. The duplicates
were the MCP Bundles (MCPB) packaging explanation, a builder testing checklist,
and the external-link allowlist.

**The judge** found 3 and then 2 of the 3 duplicates, with no false positives;
the runs disagreed on MCPB. Checked against the approved edits, 4 of 6
suggestions passed in each run, including all three keep decisions. Both runs
left the Claude Code testing check in the builder index instead of merging it
into the testing guide. That assessment was made by an agent against my approved
expectations, not by me rating each output.

**Retrieval** also missed two cases at top 10. MCPB's best match ranked 18th, and
the extractor skipped the testing checklist because it was a numbered list. The
[coverage follow-up](pilot/candidate-coverage.md) added contiguous numbered
checklists and widened retrieval to 20 neighbors. That recovers all 9 known
duplicates, at about twice the queue size. The judge scored full annotated
passages, so its results don't depend on either retrieval setting.

## Why the workflow ends here

Retrieval, classification, and the proposed edit each failed in a different way.
A judge's decision to keep both passages would hide a useful consolidation, and
even a correct duplicate label could recommend the wrong edit. So the packaged
workflow keeps every retrieved candidate in front of the editor. You can attach
[advisory notes](usage.md#optional-advisory-notes), from the v5 rubric or
elsewhere, to selected pairs, but they never remove candidates or approve changes.

## Caveats

- **Extractor implementation is bad.** I deferred reviewing/refining how the extractor is
  written so it skips code, tables, MDX step containers, and probably more. Also, the
  10-word minimum can exclude short explanations.
- **Recall.** The retrieval changes were tuned on the same 9 known duplicates they now
  find, so 6 of 6 and 3 of 3 don't establish general recall. TF-IDF can miss paraphrases
  with little shared wording.
- **Precision and effort.** The 13,786-pair queue is an exploration list, not a list of
  confirmed defects. Its precision and review time are unmeasured.
- **Judge accuracy.** Each set is small and purposefully chosen. v1–v4 had one run
  each. The work clarified the policy and exposed failure modes, but didn't show a
  repeatable improvement over v1.
- **Not production-ready.** This is a prototype built on *this exact repository*, so it's
  not portable at all and relies on a hardcoded path to the snapshots.
- **Nice as a utility, not ready as a source for automated alerts.** I'd require at least
  90% actionable findings on a fresh, fully reviewed queue and recovery of at least 80% of
  a fresh set of confirmed duplicates. Adoption would also need measured review time and
  checks that proposed edits preserve information, choose the right destination, and keep
  local requirements.

## Maintenance

A documentation-platform maintainer owns the code and an editor owns the
labeling policy, with domain owners resolving applicability questions. Checker
changes need the [verification checks](usage.md#verify-the-workflow) and a review
of changed outcomes. A new snapshot needs a dated manifest and deliberately
re-anchored evaluation cases, with earlier evidence preserved. Investigate unexpected drops in extracted passages, unfamiliar Markdown structures, or missed
known duplicates. Any alerting pilot should review every finding, sample
unflagged prose, and pause when it misses the targets.

## Files

- [run.py](run.py) builds the queue with [docslint](docslint/) and renders the
[static report](report.html).
- The [pilot archive](pilot/README.md) keeps each experiment reproducible with its
original conclusions, which describe that stage rather than the current
workflow.
- [Frozen queue](pilot/review-queue.json) and
[coverage results](pilot/candidate-coverage.md) for the current configuration.

