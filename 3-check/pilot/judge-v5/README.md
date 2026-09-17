# Pre-release calibration

## Protocol recorded before judging

Scope remains duplicate retrieval and editorial judgment of the retrieved overlap.
This experiment does not reorganize the corpus by Diataxis mode or edit source pages.

1. Preserve all historical artifacts. Use [examples-adjudicated.json](examples-adjudicated.json)
   as a new version of the 16 familiar cases. Five cases carry Ashley's explicit
   decisions and expected treatments; the other eleven retain historical agent labels.
2. Freeze one [rubric revision](prompt.md), then run it twice with the same packet
   and requested model/effort. Do not revise the rubric between runs or retry for
   a better score. Judge inputs exclude labels, expected treatments, and prior outputs
   by instruction; filesystem isolation is not enforced.
3. Select six fresh source pairs purposefully, aiming for three plausible duplicates
   and three negatives. Exclude previously judged pairs and equivalent overlapping
   spans. Review expected decisions with Ashley before judging these cases. Selection
   is not random and the resulting small set cannot estimate whole-corpus accuracy.
   Familiar and fresh cases use separate packets. Each packet receives two independent
   runs. Familiar-case results may be collected while fresh human review is pending;
   those results will not be used to revise the frozen rubric or fresh expectations.
4. Keep TF-IDF extraction and top-10 retrieval unchanged. Measure whether each case
   is eligible for extraction and retrieved, separately from full-span judge results.
5. Report verdict agreement, abstentions, and run-to-run stability. Review suggested
   treatment separately for information preservation, destination, local requirements,
   and unverified claims. This treatment assessment is an editorial review, not a
   deterministic correctness test. Do not count a correct label as an approved edit.

The two judge runs will request GPT-5.6-Terra with high effort, matching the requested
settings of earlier experiments. Actual runtime settings may remain unobservable.
No model output exists for v5 when this protocol is first recorded.

## Familiar-case results

The adjudicated version changes two binary labels: Drive becomes negative and the
financial-services marketplace becomes positive. Three other cases retain positive
labels with explicit merge-and-shorten treatments. The other eleven labels are
inherited agent judgments, not newly human-approved ground truth.

The unchanged top-10 TF-IDF queue contains extracted pairs for all six positives
in this version: 980 passages and 6,755 candidate pairs. See the separate
[retrieval result](retrieval-adjudicated.json). A full-span judgment result does
not establish that the smaller retrieved excerpts support the same decision.

| Run | True positives | False positives | False negatives | True negatives | Abstentions |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 3 | 0 | 3 | 10 | 0 |
| B | 4 | 0 | 2 | 10 | 0 |

Both runs retained Drive and all ten negative cases. Both missed the slug
consolidation. A missed the Government plugin and skill definitions; B found
those but missed the marketplace consolidation. Binary decisions agree on
13/16 cases; exact three-way classifications agree on 12/16. Recall is 3/6 and
4/6. These runs do not show stable application of the adjudicated treatments.

The [parent treatment review](treatment-review.json) covers the five cases Ashley
explicitly adjudicated, separately from verdict scoring:

| Run | Pass | Partial | Fail |
| --- | ---: | ---: | ---: |
| A | 2 | 0 | 3 |
| B | 1 | 2 | 2 |

B's Government suggestions shorten and link but do not explicitly merge the
useful general additions into the overviews. A's marketplace treatment includes
the required merge and identifies UI wording to verify before editing. These are
parent assessments of suggested edits, not fresh human treatment scores.

The rubric remains frozen for this experiment; no score-driven retries or further
prompt tuning were performed. The original tool default remains unchanged.
Do not promote v5 on these results. [Run provenance](runs.json) records requested
settings, unobservable actual settings, input/output hashes, and evidence-quote
corrections. All 32 final responses pass the existing structural, source, and
literal-quote validation. Those checks do not validate editorial correctness.

## Fresh-case results

Ashley approved all [six cases and treatments](fresh-review.md) before either
fresh judge run. The approved version is [examples-fresh.json](examples-fresh.json);
the [original proposals](fresh-proposals.json) remain saved. This set contains three
consolidations and three negatives, selected from source material before consulting
their retrieval ranks. New pairings are not necessarily unseen passages:
the testing-guide span includes a warning used in an earlier, unrelated comparison.
None overlaps both sides of a previous example, pilot pair, or baseline finding.

The [unchanged top-10 retrieval](retrieval-fresh.json) finds only **1/3 positives**:

| Approved duplicate | Extractable pair | In top-10 queue | Reason for a miss |
| --- | --- | --- | --- |
| MCPB route page / builder guide | Yes | No | Best cross-passage directional rank is 15 |
| Builder index / testing guide | No | No | The index's testing instructions are a numbered list, which extraction excludes |
| External-link allowlist | Yes | Yes | — |

The test-credentials negative is also retrieved. The warning-branch and generic-auth
negative pairs are not extractable in their selected spans. Missing negative pairs
do not demonstrate correct editorial judgment. These source-level probes expose a
scope limit as well as a ranking limit: extraction deliberately excludes numbered
procedures, while the approved testing case includes a procedural checklist.

Both judges received all six full-span pairs, including the retrieval misses:

| Run | True positives | False positives | False negatives | True negatives | Abstentions |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 3 | 0 | 0 | 3 | 0 |
| B | 2 | 0 | 1 | 3 | 0 |

Both kept all three negatives. B missed MCPB, treating the route and builder passages
as distinct reader questions. Binary and exact-class agreement are both 5/6.
The [comparison](fresh/comparison.json) does not estimate end-to-end performance:
the retrieved excerpts can be smaller than these full-span targets, and two approved
duplicates never reached the queue.

The separate [parent treatment review](fresh/treatment-review.json) finds:

| Run | Pass | Partial | Fail |
| --- | ---: | ---: | ---: |
| A | 4 | 2 | 0 |
| B | 4 | 1 | 1 |

Both testing suggestions keep the Claude Code check in the index instead of merging
it into the testing guide. A's MCPB suggestion shortens and links but leaves useful
additions on the route page rather than explicitly merging them into the builder
guide. Both allowlist treatments preserve local submission requirements. These are
parent assessments against human-approved expectations, not new human ratings of
the outputs. All 12 final fresh responses pass structural, source, and literal-quote
validation. The rubric hash is identical to the one used in the familiar runs.

## Decision after steps 1–3

The versioned adjudications, single rubric revision, and two-run familiar/fresh
checks are complete. No further prompt revision or score-driven retry was made.
The evidence does **not** justify promoting v5 or claiming release readiness:
fresh retrieval misses two of three approved duplicates, familiar judgments vary,
and even correct duplicate verdicts can omit the required merge treatment.

The next bounded decisions are whether extraction should include procedural
checklists, how much to widen candidate retrieval, and whether the initial release
should show candidate pairs for human review without using the judge to suppress
them. Broader retrieval alone would not address treatment quality. These decisions
and any resulting implementation are outside this completed experiment.

The pending-fresh status in the earlier `familiar/comparison.json` records that
artifact's creation time; [runs.json](runs.json) and this report give the final status.

## Reproduce the completed checks

```sh
uv run 3-check/docslint/test_judge_pilot.py
uv run 3-check/docslint/bakeoff.py --expanded-extraction \
  --examples 3-check/pilot/judge-v5/examples-adjudicated.json > /tmp/v5-retrieval.json
cmp 3-check/pilot/judge-v5/retrieval-adjudicated.json /tmp/v5-retrieval.json
uv run 3-check/docslint/judge_pilot.py prepare \
  --examples 3-check/pilot/judge-v5/examples-adjudicated.json \
  --prompt 3-check/pilot/judge-v5/prompt.md --output-dir /tmp/v5-familiar
cmp 3-check/pilot/judge-v5/familiar/judge-packet.json /tmp/v5-familiar/judge-packet.json
cmp 3-check/pilot/judge-v5/familiar/judge-manifest.json /tmp/v5-familiar/judge-manifest.json
uv run 3-check/docslint/judge_pilot.py evaluate \
  --examples 3-check/pilot/judge-v5/examples-adjudicated.json \
  --prompt 3-check/pilot/judge-v5/prompt.md \
  --packet 3-check/pilot/judge-v5/familiar/judge-packet.json \
  --manifest 3-check/pilot/judge-v5/familiar/judge-manifest.json \
  --judgments 3-check/pilot/judge-v5/familiar/decisions-a.json > /tmp/v5-metrics-a.json
cmp 3-check/pilot/judge-v5/familiar/metrics-a.json /tmp/v5-metrics-a.json
```

Repeat evaluation with `decisions-b.json` and compare against `metrics-b.json`.
For the fresh checks, substitute `examples-fresh.json` for the label file and
`fresh` for `familiar` in packet, manifest, judgment, and output paths. Compare the
retrieval result with `retrieval-fresh.json`.
The comparison counts can be reconstructed from these per-case outcomes;
treatment review requires reading the suggestions against the recorded expectations.
These commands replay saved artifacts, not the model. Retrieval and preparation
byte equality depend on the recorded Python and dependency versions.
