# Editorial judge pilot

**The judge agreed with 14 of 16 existing binary labels: five true positives,
one false positive, one false negative, and nine true negatives.** It rejected
all eight new sampled candidates, agreeing with a separate parent-agent review.
All 24 responses passed source and evidence validation, with no abstentions.

This experiment adds model judgment after the
[expanded TF-IDF retrieval run](extraction-followup.md). It tests whether the
model distinguishes removable explanations from repetition readers need locally.
It does not change the source documentation or run the full candidate queue.

## Results and decision

| Diagnostic set | True positives | False positives | False negatives | True negatives |
| --- | ---: | ---: | ---: | ---: |
| Development, 8 cases | 3 | 0 | 0 | 5 |
| Evaluation, 8 cases | 2 | 1 | 1 | 4 |
| Combined, 16 cases | 5 | 1 | 1 | 9 |

Combined diagnostic precision is **5/6, or 83.3%**; recall is also **5/6**.
The negative-case false-positive rate is 1/10. All 16 received a decision.
The original split names are retained for traceability, but both sets have
already informed this project and cannot establish held-out performance.
The labels score actionable versus non-actionable; they do not establish
accuracy for the two non-actionable subclasses.

Two disagreements explain the current limit:

| Case | Judge decision | Assessment against the existing policy |
| --- | --- | --- |
| Gmail and Calendar owner enablement, line 21 on each page | `ACTIONABLE_DUPLICATE` | False positive. Its rationale relies on identical wording and recommends removing or cross-referencing one instance. Each service needs its local prerequisite. The rubric explicitly protects this information. |
| Drive live-sync feature, line 51, and FAQ, lines 58–60 | `NECESSARY_REPETITION` | False negative under the existing label. The judge values the feature-list and FAQ entry points; the label favors one answer with a preserved reference target. This is an editorial policy disagreement worth human adjudication. |

Even a correct binary classification does not validate the proposed edit. For
the permanent-slug duplicate, the judge recommends keeping the lifecycle
explanation and removing or linking the listing-management copy. The
[audit](../1-audit/audit-memo.md) proposes the opposite canonical home. The
classification counts as a true positive; its consolidation direction still
needs editorial correction. The judge was not given the audit's ownership
decisions, so supplying that context would be part of evaluating such suggestions.

The eight new candidates all received `RELATED_BUT_DISTINCT`. The parent
recorded the same eight decisions in [judge-sample-review.json](judge-sample-review.json)
before reading the judge's output. This is agreement between agents using the
same rubric, not human ground truth. There were no proposed findings in this
sample, so it provides no estimate of finding precision or positive-case recall.

**Keep TF-IDF and refine the judge before expanding the run.** Retrieval already
finds all six known positives. This pilot loses one at judgment and still makes
the prerequisite mistake the lexical baseline made. Its diagnostic precision
is below the proposed 90% target, and the small reused set cannot validate that
target even if a later run reaches it.

The next experiment should require a specific explanation of why a proposed
consolidation preserves local prerequisites and reader decisions, adjudicate the
FAQ policy with a human editor, and score canonical-home suggestions separately.
Version the rubric and test fresh cases; do not overwrite this run or relabel its
errors to improve the result. Processing all 6,755 pairs is premature.

## Method

The [rubric](judge-prompt.md) was written before the model run. It asks whether a
concrete consolidation can preserve unique facts and local usability. It also
allows abstention when the supplied context does not support a reliable decision.

The packet combines two sets:

- All 16 existing labeled examples, with their complete annotated source ranges.
  These test the judge directly, including procedures the extractor may exclude.
  They do not measure end-to-end retrieval and judgment.
- Eight new passage pairs from the expanded TF-IDF top-10 queue. After excluding
  pairs covered by existing examples or the reviewed baseline findings, the
  runner divides the score-ranked queue
  into four equal-sized strata and selects two pairs per stratum by a stable
  hash. This samples across the ranking without choosing cases by their apparent
  editorial value.

Of the 6,755 pairs, 16 were excluded for coverage by frozen examples and another
17 for exact matches to reviewed baseline findings. The remaining 6,722 pairs
form strata of 1,681, 1,681, 1,680, and 1,680 pairs. The selection manifest records
each sampled pair's score and ranks; none of that metadata went to the judge.

Each side includes its exact text, path, one-based line range, preceding Markdown
heading hierarchy, and eight source lines before and after the target. A long
target is included in full. This bounded context can miss relevant information
elsewhere on a page; the judge must flag uncertainty when that affects a decision.

The model receives opaque IDs and the mixed packet in a separate hash order. Labels,
example IDs, split names, scores, and sampling groups are absent. The parent
already knows the diagnostic examples; only the judging agent receives a fresh
context without that history. These reused cases are not a held-out benchmark.

The model returns a classification, shared and unique information, rationale,
literal evidence from both targets, and a consolidation suggestion for actionable
pairs. Code checks the response against the packet and pinned snapshot before
counting any result. Evidence matching establishes that a quote exists; it does
not establish that the editorial reasoning is correct.

Saved artifacts: [packet](judge-packet.json), [selection manifest](judge-manifest.json),
[raw decisions](judge-decisions.json), [metrics](judge-metrics.json), and
[run provenance](judge-run.json). The raw decisions and original labels are
unchanged. The evaluator binds the metrics to the packet, manifest, and response
hashes, and checks the source snapshot, prompt, and label hashes.

## Execution and limits

Judging uses a native Codex subagent and saved JSON. The runner prepares inputs
and validates and scores an imported response; it does not call a model API.
No inference SDK, API key, provider adapter, or new model dependency is required.
Requested model settings and observable run metadata are recorded with the
results. A requested model is not proof of the runtime model when the host does
not expose that metadata.

This run requested **GPT-5.6-Terra with high reasoning effort**, with a fresh
context and one judgment attempt. Runtime model and effort, token usage, and
monetary cost were unobservable. No output repair or reclassification was needed
to pass validation. The parent inspected the complete response afterward.

Deterministic preparation and evaluation can be reproduced. Regenerating the
model response is a new experiment and may produce different decisions. No
corpus-wide precision, recall, latency, or monetary cost follows from this small
run. Findings remain proposals for an editor; they are never deletion commands.

## Reproduce

From the repository root:

```sh
uv run docslint/test_judge_pilot.py
uv run docslint/judge_pilot.py prepare --output-dir /tmp/claude-judge-pilot
diff -u docs/3-check/judge-packet.json /tmp/claude-judge-pilot/judge-packet.json
diff -u docs/3-check/judge-manifest.json /tmp/claude-judge-pilot/judge-manifest.json
uv run docslint/judge_pilot.py evaluate \
  --packet docs/3-check/judge-packet.json \
  --manifest docs/3-check/judge-manifest.json \
  --judgments docs/3-check/judge-decisions.json > /tmp/claude-judge-metrics.json
diff -u docs/3-check/judge-metrics.json /tmp/claude-judge-metrics.json
```

Preparation uses the existing isolated scikit-learn dependency. The
[numerical environment caveat](tfidf-bakeoff.md#reproduce-and-inspect) still
applies to retrieval and recorded runtime metadata. Input validation rejects
invalid responses before emitting metrics. Tests cover literal evidence,
duplicate or missing IDs, source and context changes, unsafe paths, swapped
example mappings, and abstention denominators.

To run a new judging experiment, give a fresh agent only
[judge-prompt.md](judge-prompt.md) and [judge-packet.json](judge-packet.json),
instruct it to return the required JSON, and save that response separately.
Keep the manifest, labels, reports, and earlier decisions out of its context.
Evaluate the new response with `--judgments`. Record the requested model,
observable runtime settings, input and output hashes, and any retries. These
instructions define the intended information boundary; a fresh agent is not an
enforced filesystem sandbox.
