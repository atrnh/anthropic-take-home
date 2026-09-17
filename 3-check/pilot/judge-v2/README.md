# Editorial judgment refinement

This experiment compares the original rubric and two revisions on an identical
24-case packet. The original pilot and labels remain unchanged.

## Results and decision

| Run | True positives | False positives | False negatives | True negatives | Abstentions |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original pilot, v1 | 5 | 1 | 1 | 9 | 0 |
| Fresh control, unchanged v1 | 6 | 0 | 0 | 10 | 0 |
| Broad revision, v2 | 0 | 0 | 5 | 10 | 1 |
| Narrow revision, v3 | 5 | 0 | 0 | 10 | 1 |

The unchanged rubric matched all 16 labels on this run. The earlier error is
therefore not a stable baseline failure, and a corrected prediction alone cannot
establish an improvement. The original pilot also had eight different companion
cases, so that contrast cannot isolate randomness from batch-context effects.
The control still suggested the lifecycle page as the canonical slug explanation, contrary to the audit's ownership direction.

**Version 2 failed calibration.** It treated local usefulness and different page
tasks as reasons to keep whole explanations. It missed both plugin definitions,
the sales example, the skill definition, and the slug explanation. The one
abstention was the disputed Drive FAQ, as instructed. With no accepted findings,
its precision is undefined, not 100%; recall against the six original positives
is 0/6.

The narrower [version 3](prompt-v3.md) starts from the original rubric and asks
whether the shared explanatory part can be shortened while retaining necessary
local information. It explicitly distinguishes partial consolidation from
removing an entire passage. Version 2 remains saved as a rejected experiment.

Version 3 recovered the five other positive cases and rejected all ten known
negatives. It made five accepted findings, all matching the historical labels,
for diagnostic precision of 5/5. Recall remains **5/6**, because the disputed FAQ
is still in the denominator; coverage is 15/16. Calling this 100% recall would
hide the abstention. All three judges rejected all eight fresh candidates and
agreed with the parent's separate assessments.

The revised classification rule is a useful candidate for further testing, but
this run does **not** demonstrate higher accuracy than the unchanged control.
Keep the original defaults. Reject v2. The post-run FAQ policy below is now
recorded in v4 for the next calibration; obtain fresh positive examples
before judging a larger queue. Do not tune again on these same cases to manufacture
a perfect score.

### Suggested edits remain a separate review

Version 3's slug suggestion keeps the rule in listing management and preserves
the lifecycle page's URL and sharing details, matching the audit's ownership
direction. However, its sales-example suggestion chooses the submission page
because the example is fuller. That does not establish canonical ownership and
fails the revised instruction against choosing by length alone. The parent
would require an ownership decision before accepting that edit.

Thus five correct duplicate classifications do not mean five approved edits.
This is a qualitative review of suggestions, not a separately labeled accuracy
metric. Source-quote validation cannot verify these editorial judgments.

All 72 responses passed schema, source-context, and literal-evidence checks.
Raw decisions and metrics are saved for the [control](control-decisions.json),
[v2](judge-decisions.json), and [v3](v3-decisions.json); [runs.json](runs.json)
records requested settings, input/output hashes, and the adaptive sequence.

## What changed

The first [revision, v2](prompt.md), checks local necessity before lexical or semantic
similarity. An actionable finding must explain each passage's reader task, what
would remain locally, and why shortening would preserve independent usability.
Identical text and an absence of unique facts are insufficient reasons to remove
prerequisites, permissions, warnings, or decision-relevant conditions.

Canonical ownership is a separate decision. The judge must justify a suggested
home from supplied context or leave that choice to an editor. Longer text alone
is not evidence of ownership. This experiment does not supply an ownership map.

At the time of these runs, the summary-versus-FAQ policy was awaiting human
adjudication. The v2 and v3 rubrics explicitly defer short same-page feature-summary/FAQ repetitions with
`needs_review: true`. This is a targeted deferral of a known disputed case, not a
new correct prediction. The evaluator retains all six historical positives in
its recall denominator, including an abstained positive.

## Adopted FAQ policy (after these runs)

Ashley approved case-by-case judgment: allow brief repetition when a feature
summary and a direct FAQ answer serve useful reader purposes. Flag substantial
repeated explanation that adds no reader value when consolidation preserves
both entry points' usefulness.

[Version 4](prompt-v4.md) replaces v3's blanket FAQ deferral with this policy.
The follow-up run is reported below.

Ashley also adjudicated `evaluation-drive-live-sync-faq`: **keep both passages**
(`NECESSARY_REPETITION`; `duplicate: false` for future evaluations). The brief
feature bullet supports scanning, while the FAQ gives a direct answer to whether
documents update after being added. Replacing that one-sentence answer with a link
would add reader effort for little benefit.

This decision supersedes the original positive label for future evaluations.
Historical prompts, decisions, labels, and metrics remain frozen; their reported
scores remain unchanged. A separate comparison below rescores saved decisions
under the adjudicated policy.

## V4 follow-up: Drive resolved, other judgments regressed

V4 classified Drive as `NECESSARY_REPETITION` without abstaining. Its rationale
matches the approved policy: scanning features and seeking a direct FAQ answer
are useful purposes for these two brief passages.

The rest of the run was worse. On the same 16 known cases, scored with Drive now
negative and the other 15 labels unchanged:

| Saved run | True positives | False positives | False negatives | True negatives | Abstentions |
| --- | ---: | ---: | ---: | ---: | ---: |
| Unchanged-v1 control | 5 | 1 | 0 | 10 | 0 |
| V3 | 5 | 0 | 0 | 10 | 1 |
| V4 | 2 | 1 | 3 | 10 | 0 |

V4 missed the Government plugin definition, Government skill definition, and
permanent-slug explanation. It treated their local usefulness as sufficient to
keep the repetition. It also flagged the financial-services marketplace procedure,
contrary to the existing requirement to keep that procedure independently usable.
All eight sampled candidates remained `RELATED_BUT_DISTINCT`.

**Keep the approved FAQ policy, but do not promote v4 based on this run.** It
resolved the targeted ambiguity while introducing four disagreements elsewhere.
The sales-example suggestion also still chooses a canonical home because it is
fuller, which does not establish ownership. Correct duplicate classifications
still require separate review of the proposed edits.

This is one adaptive run on familiar cases, with no new positive examples.
The results do not isolate prompt effects from model variability. Before another
rubric rewrite, review the remaining disputed examples with an editor and obtain
fresh positive cases. The original default remains unchanged.

The [comparison](v4-policy-comparison.json) applies the same explicit Drive-label
override to all three saved runs; it does not rewrite historical artifacts. The
[historical-label metrics](v4-metrics.json) instead count Drive as a false negative
and therefore show 2 TP, 1 FP, 4 FN, and 9 TN. Neither view is held-out accuracy.
The [run record](v4-run.json) binds the files and discloses the judge's evidence-quote
format corrections before finalization. All 24 final responses pass schema,
source-context, and literal-evidence validation. The judge was instructed to read
only the prompt and packet; exclusive access was not enforced or verified.

To reproduce the policy comparison (including validation of all three saved runs):

```sh
uv run 3-check/docslint/compare_faq_policy.py > /tmp/claude-v4-policy-comparison.json
cmp 3-check/pilot/judge-v2/v4-policy-comparison.json /tmp/claude-v4-policy-comparison.json
uv run 3-check/docslint/judge_pilot.py evaluate \
  --prompt 3-check/pilot/judge-v2/prompt-v4.md \
  --packet 3-check/pilot/judge-v2/judge-packet.json \
  --manifest 3-check/pilot/judge-v2/v4-manifest.json \
  --judgments 3-check/pilot/judge-v2/v4-decisions.json > /tmp/claude-v4-metrics.json
cmp 3-check/pilot/judge-v2/v4-metrics.json /tmp/claude-v4-metrics.json
```

## Initial comparison design (control, v2, and v3)

The control, v2, and v3 judges were requested as GPT-5.6-Terra with high effort and were
instructed to use only their respective prompt and the shared
[packet](judge-packet.json), without reading labels or earlier decisions. Exclusive
file access was not enforced or independently verified. Actual runtime model and
effort are unobservable. No classifier output was repaired or relabeled. Version 3 was written after the parent saw
version 2 regress on the familiar examples, so it is an adaptive calibration pass.
Each rubric gets one run, so differences can reflect model variability; they do not establish a causal or repeatable
prompt improvement.

The packet includes the same 16 familiar full-span diagnostic examples and eight
new TF-IDF candidates. The runner takes the third and fourth smallest pair hashes
in each of the existing four rank strata with `--sample-offset 2`. The prior
pilot used the first and second. The new sample is disjoint from the earlier
sample and excludes frozen-example matches and reviewed baseline findings.
Neither sample was selected by inspecting its apparent editorial value.

The parent assessed the eight fresh cases before any of these judges ran and saved
[sample-review.json](sample-review.json). All eight were judged related but
distinct. This agent review is a qualitative check, not human ground truth, and
contains no new positive examples. It cannot establish generalization to fresh
actionable duplication.

The [control manifest](control-manifest.json) binds the original prompt; the
[v2 manifest](judge-manifest.json) and [v3 manifest](v3-manifest.json) bind their
respective revisions. All three bind identical packet bytes, snapshot, and original labels. Comparing against those
unchanged labels keeps policy deferral separate from classifier improvement.
These are direct judgment tests, not full-queue end-to-end measurements.

## Reproduce

From the repository root:

```sh
uv run 3-check/docslint/test_judge_pilot.py
uv run 3-check/docslint/judge_pilot.py prepare --sample-offset 2 \
  --output-dir /tmp/claude-judge-v2-control
cmp 3-check/pilot/judge-v2/judge-packet.json /tmp/claude-judge-v2-control/judge-packet.json
cmp 3-check/pilot/judge-v2/control-manifest.json /tmp/claude-judge-v2-control/judge-manifest.json
uv run 3-check/docslint/judge_pilot.py prepare --sample-offset 2 \
  --prompt 3-check/pilot/judge-v2/prompt.md --output-dir /tmp/claude-judge-v2
cmp 3-check/pilot/judge-v2/judge-packet.json /tmp/claude-judge-v2/judge-packet.json
cmp 3-check/pilot/judge-v2/judge-manifest.json /tmp/claude-judge-v2/judge-manifest.json
uv run 3-check/docslint/judge_pilot.py evaluate \
  --packet 3-check/pilot/judge-v2/judge-packet.json \
  --manifest 3-check/pilot/judge-v2/control-manifest.json \
  --judgments 3-check/pilot/judge-v2/control-decisions.json > /tmp/claude-control-metrics.json
cmp 3-check/pilot/judge-v2/control-metrics.json /tmp/claude-control-metrics.json
uv run 3-check/docslint/judge_pilot.py evaluate \
  --prompt 3-check/pilot/judge-v2/prompt.md \
  --packet 3-check/pilot/judge-v2/judge-packet.json \
  --manifest 3-check/pilot/judge-v2/judge-manifest.json \
  --judgments 3-check/pilot/judge-v2/judge-decisions.json > /tmp/claude-v2-metrics.json
cmp 3-check/pilot/judge-v2/judge-metrics.json /tmp/claude-v2-metrics.json
uv run 3-check/docslint/judge_pilot.py prepare --sample-offset 2 \
  --prompt 3-check/pilot/judge-v2/prompt-v3.md --output-dir /tmp/claude-judge-v3
cmp 3-check/pilot/judge-v2/judge-packet.json /tmp/claude-judge-v3/judge-packet.json
cmp 3-check/pilot/judge-v2/v3-manifest.json /tmp/claude-judge-v3/judge-manifest.json
uv run 3-check/docslint/judge_pilot.py evaluate \
  --prompt 3-check/pilot/judge-v2/prompt-v3.md \
  --packet 3-check/pilot/judge-v2/judge-packet.json \
  --manifest 3-check/pilot/judge-v2/v3-manifest.json \
  --judgments 3-check/pilot/judge-v2/v3-decisions.json > /tmp/claude-v3-metrics.json
cmp 3-check/pilot/judge-v2/v3-metrics.json /tmp/claude-v3-metrics.json
```

The existing [dependency-version caveat](../tfidf-bakeoff.md#reproduce-and-inspect)
applies. Replaying preparation and scoring is deterministic in the recorded
environment; rerunning any judge is a new model experiment.
