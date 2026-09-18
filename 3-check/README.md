# Duplicate-prose review workflow

This workflow helps an editor find explanations that belong in one shared home.
It retrieves similar passages from the Claude Docs snapshot and presents them
side by side, with source lines and surrounding context. The editor decides what
to merge, shorten, or keep.

The package implements candidate discovery for the
[SHARE-01 shared-explanation rule](../2-standards/style-guide.md). It includes a
runnable checker, a searchable report, worked examples, and saved evaluation
results. It is ready for informal local review. Its broader queue has not been
validated for routine editorial alerts or a required CI check.

The [usage guide](usage.md) covers setup, the starting command, report controls,
custom snapshots, optional advice, and verification. The
[worked example](worked-example.md) explains one consolidation and one decision
to keep repeated text.

## How the workflow works

The input is the checked-in [54-page snapshot](../corpus/manifest.json), fetched
on 14 September 2026. The loader verifies each source file against its recorded
hash. Source links in the report refer to that snapshot, not live documentation.

The extractor includes prose, unordered list items, and contiguous numbered
checklists with at least 10 words per extracted passage. TF-IDF weights words by
how distinctive they are across the passages, then scores pairs by similarity.
The workflow selects each passage's top 20 positive-score neighbors and combines
both directions. It compares passages within a page and across pages.

The default run produces **1,027 passages and 13,786 candidate pairs**. The
[starter command](usage.md#start-here) regenerates those counts and writes the
queue, a static HTML report, line-numbered source copies, and a run summary.
Search, page-pairing filters, and pagination make the queue browsable while
preserving access to every candidate.

Similarity measures wording overlap, not whether an edit is warranted. The
workflow makes no model calls. Optional advisory notes can accompany selected
pairs, but they never remove candidates or approve changes. The report does not
save review decisions or edit source documents.

## What makes a consolidation useful

Two passages are actionable when they repeat explanatory work that can move to
one shared home without weakening either page. The shared explanation may need
facts from both passages before another page can shorten its text and link to it.
Unique information is therefore a reason to consider a merge, not an automatic
reason to keep both explanations.

A page's location does not establish a claim's applicability. General information
in a Government guide can belong in the general overview. Any uncertain product
behavior or UI wording still needs verification before an editor changes it.
Necessary local prerequisites, warnings, and brief answers remain beside the task
or question they support.

The human review established these treatments:

| Case | Approved treatment |
| --- | --- |
| Government plugin and skill definitions | Merge broadly applicable additions into the general overviews, then shorten the Government introductions and link back. Retain Government-specific information locally. |
| Permanent directory slug | Consolidate the full explanation under listing management. Keep the constraint beside editing instructions and a reminder with a link on the after-publishing page. |
| Financial-services marketplace | Move the complete installation path into the general installation guide. Retain the repository URL and collection-specific details in the specialized guide. Verify the differing UI wording before editing. |
| Google Drive live sync | Keep the short feature bullet and FAQ answer. Each helps readers find the same fact for a different purpose. |

The [adjudicated cases](pilot/judge-v5/examples-adjudicated.json) record these
decisions and expected treatments. Scope remains duplicate retrieval and review
of the overlap; the tool does not classify or reorganize the whole corpus by
document type.

## What the evaluation establishes

Retrieval, editorial classification, and the proposed edit are separate checks.
A retrieved pair can be necessary repetition. A correct duplicate classification
can still lead to an incomplete merge suggestion.

| Check | Result | Interpretation |
| --- | --- | --- |
| Current retrieval on familiar cases | 6 of 6 positive cases retrieved | Covers the known examples, including revised human decisions. |
| Current retrieval on fresh cases | 3 of 3 approved positive cases retrieved | Includes the MCPB explanation, testing checklist, and external-link allowlist. |
| Latest model rubric, two runs on 16 familiar cases | 3 of 6 and 4 of 6 duplicates identified; no false positives | Classification varies between runs and misses approved consolidations. |
| Same rubric, two runs on six fresh cases | 3 of 3 and 2 of 3 duplicates identified; no false positives | Both runs preserve the three negative cases, but disagree on MCPB. |
| Treatment review on those six fresh cases | 4 of 6 treatments pass in each run, including the three keep decisions | Both runs omit the required merge of the Claude Code testing check into the testing guide. |

The [coverage analysis](pilot/candidate-coverage.md) and
[frozen queue](pilot/review-queue.json) support the current retrieval results.
Numbered-checklist extraction and top-20 retrieval address the observed misses.
These changes were tuned on the same small sets, so 6 of 6 and 3 of 3 do not
establish general recall. Five familiar cases carry explicit human adjudications;
the other eleven retain historical agent labels. All six fresh cases and expected
treatments were human-approved before the model runs.

The [model evaluation](pilot/judge-v5/README.md) used full annotated spans,
including cases the earlier retrieval configuration missed. Its scores are not
end-to-end results for the current queue. Treatment scores are agent assessments
against the approved expectations, not fresh human ratings of model outputs.
The latest rubric remains experimental. Its inconsistent classifications and
incomplete suggestions are why model advice stays optional and cannot filter
the queue.

## Limits and conditions for broader use

The 13,786-pair queue's precision and human review effort are unmeasured. TF-IDF
can miss paraphrases with little shared wording. The snapshot-specific extractor
skips code, tables, navigation cards, and MDX step containers; its 10-word minimum
can exclude short explanations. A scraped snapshot also cannot establish whether
repeated text already comes from one shared authoring source.

For future routine alerts, the proposed acceptance targets are at least 90%
actionable findings on a fresh, fully reviewed queue and recovery of at least
80% of a fresh set of confirmed duplicates. These are operating targets, not
achieved results. The exploration queue is not a list of confirmed defects.
Broader adoption also needs measured review time and checks of proposed edits
for information preservation, destination, and local requirements.

Maintenance depends on a documentation-platform maintainer for the code and an
editor for the labeling policy, with domain owners resolving applicability questions.
Checker changes need the [verification checks](usage.md#verify-the-workflow) and
review of changed outcomes. New snapshots need dated manifests and deliberately
updated source ranges for evaluation cases, with earlier evidence preserved.
Unexpected drops in extracted passages, unfamiliar Markdown structures, or missed
known positives require investigation. Any future alerting pilot needs reviewed
findings, sampled unflagged prose, and a pause when acceptance targets are missed.

## Implementation and saved evidence

The [starter](run.py) builds the queue with [docslint](docslint/), exports source
copies, and renders the [static report](report.html). The package runs locally
with uv and a browser. It needs no model account, API key, server, or database.

The [pilot archive](pilot/README.md) preserves the experiments and their original
conclusions. Its baseline results and proposed next steps describe those experiments,
not the current workflow. The original lexical checker found 18 pairs, of which
three were judged actionable and 15 were false positives. Those counts do not
measure the current TF-IDF queue.

The archive includes earlier retrieval comparisons, rubric revisions, source
packets, decisions, labels, and metrics. The
[relocation manifest](pilot/relocation-manifest.json) records preservation checks;
JSON evidence and rubric prompts retain their original bytes. The archive remains
available for reproduction without making readers reconstruct the current design
from successive follow-ups.

## How the judge experiment evolved

The judge experiment tested whether a model could distinguish useful consolidation
from repetition that readers need. Across five rubric versions, the work exposed
problems in both model judgment and our evaluation labels. More detailed instructions
did not produce a steady improvement. The experiments instead clarified the editorial
policy and the limits of delegating it to a model.

### V1: promising classifications, unreliable edit suggestions

The [original rubric and pilot](pilot/judge-pilot.md) asked whether a concrete
consolidation could preserve unique facts and local usability. The judge received
source passages and neighboring context, without the expected labels or retrieval
scores. It could propose consolidation, keep necessary repetition, identify related
but distinct content, or flag uncertainty.

On the 16 familiar cases, the first run matched 14 existing labels. It correctly
identified five duplicates and rejected nine negatives. The two disagreements
revealed different problems:

- The judge flagged identical Gmail and Calendar owner-enablement prerequisites.
  Each connection procedure needed its prerequisite locally, so this was a real
  error despite the rubric's instruction to protect that information.
- The judge kept the Drive live-sync feature bullet and FAQ answer. The original
  label called that a miss, but Ashley later agreed with the judge. The brief
  passages served useful scanning and question-answering purposes.

The judge also identified the permanent-slug duplication but recommended keeping
its explanation on the lifecycle page. The audit put that explanation under listing
management. A correct duplicate label therefore concealed an unsuitable proposed
edit. The judge had not received the audit's ownership decisions.

A later control run used the unchanged v1 rubric and matched all 16 original labels.
That score included flagging Drive, which Ashley subsequently decided to keep. The
control also retained the wrong consolidation direction for the slug explanation.
It used the same familiar cases with eight different companion cases, so the two
runs did not isolate model variability from the effect of the surrounding packet.
A perfect match to the old labels was neither proof of stability nor proof that
the proposed edits were sound.

### V2: protecting local usefulness became a reason to keep everything

The [v2 revision](pilot/judge-v2/README.md#what-changed) required the judge to explain
each passage's reader task, what would remain locally, and why shortening would
preserve independent usability. It also required evidence for choosing a canonical
home rather than assuming that the longer passage belonged there.

The result overcorrected. V2 treated local usefulness and different page tasks as
reasons to preserve entire explanations. It accepted no duplicate findings, missed
five expected consolidations, and deferred Drive pending a human decision. Those
misses included the plugin definitions, sales example, skill definition, and slug
explanation. V2 was rejected. Returning no findings did not make it precise;
precision was undefined because there were no accepted findings to assess.

### V3: partial consolidation recovered the useful findings

[V3](pilot/judge-v2/prompt-v3.md) returned to the original rubric with a narrower
change. It asked whether the shared explanatory portion could be shortened while
necessary local information remained. Consolidating part of a passage did not
require removing the whole passage.

The run recovered all five other expected duplicates, rejected all ten known
negatives, and continued to defer Drive. Under the original labels, that was five
of six positives recovered, with one abstention rather than a sixth correct decision.
The suggested slug treatment also matched the audit's ownership direction.

However, the sales-example suggestion still chose a destination because its example
was fuller. Length did not establish ownership. V3's five correct classifications
were therefore not five approved edits. Nor did this single run establish higher
accuracy than the unchanged v1 control. The
[controlled comparison](pilot/judge-v2/README.md#results-and-decision) preserved
both results rather than treating the revision as a demonstrated improvement.

### V4: resolving Drive exposed the remaining policy disagreements

Ashley approved a case-by-case FAQ policy: keep brief repetition when it helps
readers scan or find a direct answer. Substantial repeated explanation can still
warrant consolidation. [V4](pilot/judge-v2/prompt-v4.md) replaced the blanket FAQ
deferral with that policy and correctly kept both Drive passages without abstaining.

The rest of the run disagreed with four existing labels. It missed the Government
plugin definition, Government skill definition, and permanent-slug consolidation.
It also flagged the financial-services marketplace procedure, which was then
labeled necessary repetition. With Drive scored as negative and the other labels
unchanged, v4 found two duplicates, missed three, and produced one apparent false
positive. The [saved comparison](pilot/judge-v2/README.md#v4-follow-up-drive-resolved-other-judgments-regressed)
records that assessment at the time.

Reviewing those disagreements with Ashley changed the interpretation. The Government
passages contained general additions worth merging into the overviews before
shortening the specialized introductions. The slug explanation still belonged under
listing management, with necessary reminders retained locally. The financial-services
procedure also warranted consolidation: its complete installation path belonged in
the general guide, with the repository URL and collection-specific information
retained in the specialized guide.

The marketplace finding was therefore valid under the clarified policy, despite
being scored as a false positive against the earlier label. Together, these decisions
established that page placement does not determine applicability and that unique
information can strengthen a merge recommendation. Historical scores remained
unchanged; the revised labels and expected treatments went into a new evaluation set.

### V5: clearer expectations still did not produce stable judgment

[V5](pilot/judge-v5/README.md) incorporated those decisions in one focused revision.
It asked the judge to consider applicability, merge useful additions before
shortening, preserve necessary local information, and identify facts that needed
verification. The rubric then stayed fixed for two runs on the familiar cases and
two runs on six fresh cases. Ashley approved all six fresh decisions and expected
treatments before either fresh run.

The familiar runs found three of six and four of six duplicates, with no false
positives. Both missed the slug consolidation. Their decisions differed on the
Government definitions and marketplace procedure. The fresh runs found three of
three and two of three duplicates, again with no false positives, but disagreed
on MCPB.

Proposed edits remained a separate weakness. Both fresh runs left the Claude Code
testing check in the index instead of merging it into the testing guide. Only four
of six fresh treatments passed the agent's assessment in each run, including all
three decisions to keep the passages. The scores measured the suggestions against
human-approved expectations; they were not human approvals of the model's edits.

V5 made the expectations clearer, but the repeated runs did not establish reliable
application of them. It remained experimental. We did not keep revising the prompt
or retrying the same cases until the scores looked better.

### What the experiments changed in the packaged workflow

The fresh cases also exposed two retrieval misses, separate from the judge's
mistakes. Top-10 retrieval missed MCPB, and the extractor excluded the numbered
testing checklist. The current workflow includes numbered checklists and uses
top-20 retrieval, recovering all nine known positives across the familiar and fresh
sets. That change addresses observed coverage gaps, not the model's inconsistent
classifications or incomplete treatments.

The resulting package keeps every retrieved candidate available to the editor.
Model advice is optional and cannot suppress a pair. This follows from the evidence:
a mistaken decision to keep both passages would otherwise hide a useful consolidation,
while a correct duplicate label could still recommend the wrong edit.

These experiments used small, selected sets. Earlier revisions each had one run,
and the eight new sampled candidates in those comparisons contained no positive
examples under the separate agent review. The work clarified the policy and exposed
failure modes, but did not establish general accuracy or a repeatable improvement
over v1. The current workflow reflects those limits by making the evidence available
for human judgment.
