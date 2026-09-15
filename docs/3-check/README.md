# Check for repeated explanatory prose

Follow-up: the [TF-IDF retrieval bake-off](tfidf-bakeoff.md) compares candidate
generation while preserving this lexical baseline and its editorial evaluation.

This working prototype flags exact and near-exact prose overlap in the pinned
Claude Docs snapshot. It addresses the audit's recommendation to
[remove competing explanations and redundant upkeep](../1-audit/audit-memo.md).
Every finding needs editorial review. It neither edits documentation nor decides
which page should own an explanation.

**Result: 18 flagged passage pairs across 54 pages; 3 actionable, 15 false
positives after review.** It also misses all six positive examples in our small
audit-derived evaluation set. This baseline is reproducible, but it does not meet
our proposed adoption threshold. Do not make it a required CI check or generate
routine review requests from it yet.

## Run it

From the repository root, with Python 3.10 or later and `uv`:

```sh
uv run python docslint/duplicates.py corpus --examples docs/3-check/examples.json
uv run python docslint/test_duplicates.py
```

The first command writes JSON to stdout. To regenerate the committed results
without overwriting them on a failed run:

```sh
uv run python docslint/duplicates.py corpus --examples docs/3-check/examples.json > /tmp/claude-duplicates.json
```

After a successful exit, compare that file with `docs/3-check/results.json`.
An unchanged snapshot and settings produce identical output. The verification
command checks this as well as extraction, matching, evaluation, and rejection of
modified snapshot files. There are no third-party Python dependencies, network
calls, or inference API credentials.

Exit code 0 means the scan completed, including when it found duplicates. Exit
code 2 means invalid arguments or input. Findings are advisory, never an automatic
merge or deletion instruction.

## What it checks

The command reads only pages listed in `corpus/manifest.json` and verifies every
page's SHA-256 before scanning. The committed run uses the 54-page snapshot fetched
on 14 September 2026, not current live product behavior.

It extracts paragraphs with at least **15 words**, retaining exact source text and
one-based line ranges. It excludes headings, blockquotes including the repeated
documentation index, tables, fenced code, Markdown list items and their indented
continuations, and `Steps`, `Card`, `Columns`, and `CodeGroup` bodies. Standalone
MDX tags and single-line import/export declarations are omitted. Callout prose
remains eligible, which accounts for several false positives.

For matching, the checker keeps link labels but removes inline link destinations,
ignores case and punctuation, and makes a set of each paragraph's three-word
sequences. The score is:

```text
shared three-word sequences / sequences in the shorter set
```

A score of **0.5 or greater** produces a finding. A paragraph contained in a longer
paragraph can therefore score 1.0 even when the longer passage adds important
information. Score measures wording overlap, not editorial certainty. The checker
compares paragraphs within a page as well as across pages and reports pairs, not
groups. Four copies of a notice produce six pairs.

This is a small parser for the snapshot's Markdown conventions, not a general MDX
parser. Nested components, multiline JavaScript declarations, reference-style
links, and other Markdown dialects need additional validation before reuse. Bullet
explanations, tables, cross-paragraph matches, and semantic paraphrases are outside
its reliable coverage. A scrape also cannot establish whether two rendered copies
already come from one shared authoring source.

## Why these settings

The first experiment used 25 words and 0.65 overlap. Its nine findings were all
necessary notices or prerequisites. A broader exploratory run used 15 words and
0.25 and returned 50 pairs, including weak topic matches. The final 15-word,
0.5 configuration preserves the audit-backed plugin-update match and a same-page
repeated explanation without that entire exploratory queue. Removing an MDX
`export` declaration from eligible prose left 18 findings.

We also inspected word and two-word overlap and a term-weighted word comparison on
the development examples. They did not provide a clear separation between
paraphrased explanations and related procedures. Those experiments were not added
to the implementation. The retained method is an inspectable lexical baseline;
the measurements below do not justify presenting it as a semantic detector.

Settings are CLI options: `--min-words` and `--threshold`. The JSON records both,
the snapshot manifest hash, page and extracted-passage counts, and every finding's
score, ID, excerpts, and source lines. The run extracted **661 paragraphs**.

## Review policy and results

A pair is actionable when both passages do the same explanatory job and at least
one can be removed, shortened, or replaced with a link without weakening local
prerequisites, applicability, decision safety, or completion. Repeated text that
each procedure needs in place is legitimate, even when verbatim. A shared-source
opportunity alone is insufficient because the scrape cannot reveal authoring reuse.

The parent agent reviewed every emitted pair under this policy. These are proposed
editorial judgments, not product-owner approval. [reviews.json](reviews.json)
records all 18 decisions; [results.json](results.json) preserves the evidence.

### Three actionable findings

| Finding | Evidence and proposed treatment |
| --- | --- |
| `3a2092bab58f`, 0.65 | [Lifecycle router](../../corpus/connectors/building/after-publishing.md#update-your-plugin) and [plugin submission](../../corpus/plugins/submit.md#submitting-your-plugin) both explain that CI mirrors plugin updates and screens each update. Keep the explanation at the plugin destination and link from the router, as the audit proposes. |
| `d654de3b8aaf`, 0.8 | [Design guidelines](../../corpus/connectors/building/mcp-apps/design-guidelines.md#interaction-patterns), lines 256 and 274, repeat the preference for visible controls over menus. Keep the fuller explanation under its dedicated heading. |
| `cd561a0f2e24`, 0.5366 | [Directory overview](../../corpus/connectors/directory.md) and [verification guide](../../corpus/connectors/verification.md#community) repeat the explanation that labels describe review rather than tool capabilities. Shorten the overview while preserving its trust caveat and link. |

### Cases it got wrong

| Case | Error and reason |
| --- | --- |
| MCP tunnels availability notices | Six false-positive pairs from four pages. Research-preview eligibility must be visible at each entrance. The longer overview also contains extra limitations; a 1.0 containment score does not make the whole paragraph redundant. |
| Google owner-enablement prerequisites | Two false-positive pairs. Gmail and Calendar each need their authentication and administrator prerequisites before connection steps. Matching wording does not justify sending readers elsewhere to discover a blocker. |
| Authentication product list | One false positive, `62975f03076b`. The same product list scopes two different facts: held credentials and the redirect URI to register. |
| Plugin definitions and sales example | Three development misses. They repeat explanatory work with substantially different wording or ordering; shared three-word sequences do not capture it. |
| Skill definition | An evaluation miss. Equivalent explanation uses different wording in the general and Government pages. |
| Permanent directory slug | An evaluation miss. The audit calls for consolidation, but its short, differently worded paragraphs do not clear the lexical threshold. |
| Google Drive live sync | An evaluation miss. One copy is a bullet, which the extractor deliberately excludes, and the FAQ answer is short. |

The remaining false positives are a pair of standalone SDK prerequisites, repeated
dialog signposts, a missing-toggle remedy, remote-connector context, submission
status guidance, and a short MCP orientation. There are 15 false-positive pairs in
total; see the machine-readable reviews for the per-pair decisions.

## Evaluation

An independent agent labeled 16 passage pairs using the audit and surrounding
source text without seeing checker output. Eight plugin-family pairs were assigned
to development; eight skills/connector-family pairs to evaluation. Two labels were
then corrected after a read-only policy review: the Google prerequisite and the
Government disconnected-connector warning must remain visible locally. The
corrections were made for PROC-01/02 consistency, not to improve the scores.

The groups remain separate in [examples.json](examples.json), with line ranges,
labels, and reasons. They are **diagnostic sets, not a blind held-out benchmark**:
the parent inspected whole-corpus exploratory output before final settings, and
the examples are few and deliberately chosen. Several negative examples contain
procedures the parser excludes, making them easy negatives. Obtain an unseen,
more varied set and human adjudication before making performance claims.

A labeled pair is detected only if an emitted pair falls wholly inside both
annotated ranges, in either order. Multiple emitted pairs within one labeled case
count once. Excluded or too-short positive passages still count as misses; they
are not removed from the denominator.

| Set | True positives | False positives | False negatives | True negatives |
| --- | ---: | ---: | ---: | ---: |
| Development, 8 pairs | 0 | 0 | 3 | 5 |
| Evaluation, 8 pairs | 0 | 1 | 3 | 4 |

Development precision is undefined because it emitted no matches for those
examples. Evaluation precision is 0/1 and recall is 0/3. The diagnostic negative
false-positive rate is 1/5, or 20%, on the evaluation set. These small, selected
counts are not population estimates.

Across the **entire emitted queue**, precision is 3/18, or **16.7%**. The share of
flags that waste reviewer attention is 15/18, or **83.3%**. That last quantity is
the false-discovery proportion, often loosely called the false-positive rate. We
do not claim corpus-wide recall or a corpus-wide negative false-positive rate;
unflagged pairs have not all been labeled. The three useful findings came from
the full queue, not the six positive diagnostic cases.

### Acceptance threshold and next experiment

Before routine advisory use, require at least **90% actionable findings**, or at
most 10% false discoveries, on a fresh, fully reviewed queue. Editors should not
have to dismiss most alerts. Also require recovery of at least **80% of a fresh
set of audit-confirmed duplicates**, including paraphrases, and report results
separately for prose the extractor supports and content it excludes. These are
proposed operating targets, not achieved results or statistically established
thresholds. An empty queue does not pass.

This prototype fails both targets. Raising the threshold alone will not fix it:
the most exact matches include necessary notices. Next, run a bounded experiment
that compares meaning and local reader purpose, using these known mistakes to
develop it and reserving new examples for evaluation. Measure its accuracy, cost,
and reviewer time against this baseline before adding it to an authoring workflow.
Keep human review and avoid automatic deletions even if that experiment succeeds.

## Detect degradation and keep it current

- Assign a documentation-platform maintainer to the code and an editor to the
  labeling policy. Have domain owners resolve disagreements about context.
- On each checker change, rerun the runnable checks and diagnostic cases. Review
  changed outcomes rather than rewriting labels to match the implementation.
- For a new scrape, create a new dated manifest and results artifact. Preserve
  this snapshot and baseline. Re-anchor labels deliberately; hash verification
  prevents silently evaluating changed text against old evidence.
- Compare extracted paragraphs per page as well as findings. Unexpected drops,
  new MDX constructs, or suspiciously empty queues trigger extraction review.
- During any future adoption pilot, review all new findings, sample unflagged
  prose, and record actionable/dismissed counts and review time. Pause notifications
  if the 90% precision target is missed or known positive examples stop matching.
- Track approved exceptions with a reason and the relevant content hash. Do not
  add a blanket ignore for a whole product or lower thresholds to preserve a
  preferred result. No suppression system is needed for this one-shot prototype.

## Artifacts

- [Checker](../../docslint/duplicates.py) and [runnable verification](../../docslint/test_duplicates.py).
- [Labeled cases](examples.json), [complete run](results.json), and [editorial decisions](reviews.json).
- [GitHub repository](https://github.com/atrnh/anthropic-take-home), private.
  Reviewers need repository access; this link is not a public submission.

This task's artifacts are additions after the prior audit and standards drafts.
The available record does not establish which work existed at the exercise's
six-hour mark; no claim of fitting the entire exercise into six hours is made.
