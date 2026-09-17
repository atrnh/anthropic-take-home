# TF-IDF retrieval bake-off

Follow-up: [expanded extraction](extraction-followup.md) now admits the missing
Drive passages and tests all six positives. The fixed-input results below remain
the original comparison.

**TF-IDF improves candidate retrieval on our known examples.** At top 5 it
retrieves 4 of 6 positive cases, compared with 3 of 6 for trigram top-5 retrieval.
At top 10 it retrieves all **5 representable positives**. The sixth case never
enters the extracted passage set, so neither retriever can recover it.

This supports retaining TF-IDF for the next experiment. It does not establish
editorial accuracy or an affordable final judging workload. No LLM judge,
explanation inventory, embedding model, or vector database was run in this test.

## Question and controls

The question from the Semantic Deduplication Architecture discussion was: of the
six known cases of unnecessary explanatory duplication, how many would reach a
final judge? We tested the cheaper TF-IDF option before escalating to another
approach.

- Same pinned 54-page corpus, unchanged extractor, and 15-word minimum: **661
  passages**, or **218,130 possible unordered pairs**.
- Same 16 labeled cases: 6 positive and 10 negative. No labels or source text were
  changed for this experiment. These are familiar diagnostic examples, not an
  unseen test set or a representative sample.
- Same Markdown cleanup from `duplicates.words()` before either method scores
  passages. No headings, adjacent paragraphs, concept labels, or known answers
  are added to retrieval inputs. Labels are used only for measurement.
- TF-IDF uses word unigrams and bigrams, the built-in English stop-word list,
  sublinear term frequency, smoothed corpus-fitted IDF, and L2 normalization.
  Cosine scores are the dot product of normalized vectors. This uses
  [scikit-learn's TfidfVectorizer](https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html),
  pinned to 1.7.2, rather than a custom TF-IDF implementation.
- Trigrams use the baseline's containment score. We retain the original 0.5
  threshold as one reference and also test trigram top-k retrieval, so a change
  of retrieval policy is not mistaken for a change of scoring quality.
- Primary k is 5; the preselected comparison grid is 1, 3, 5, and 10. Only positive
  scores are eligible. There is no tuned similarity floor. A pair is selected if
  either passage retrieves the other. Self-pairs are excluded; same-page pairs
  remain eligible because unnecessary repetition can occur within one page.
- Scores are rounded to 12 decimals before sorting, with source path/line order
  breaking ties. We deduplicate unordered pairs. Thus k is a per-query limit,
  not a limit on the number of times a passage can appear in the final queue.
- Equal global pair budgets of 18, 50, and 100 provide a separate cost control.
  These settings and the top-k grid were fixed before the first TF-IDF run.

The earlier baseline report describes a small term-weighted word experiment that
failed to separate editorial positives from negatives. This experiment asks a
different question: can weighted words retrieve useful candidates for a later
judge? Similarity is not used as an editorial verdict here.

## Results

| Retrieval policy | Trigram cases found | Trigram candidate pairs | TF-IDF cases found | TF-IDF candidate pairs |
| --- | ---: | ---: | ---: | ---: |
| Top 1 per passage | 3/6 | 476 | 3/6 | 514 |
| Top 3 per passage | 3/6 | 1,232 | 4/6 | 1,442 |
| **Top 5 per passage** | **3/6** | **1,791** | **4/6** | **2,345** |
| Top 10 per passage | 4/6 | 2,796 | 5/6 | 4,532 |

The published trigram checker, with its original 0.5 threshold, returns 18 pairs
and recovers 0/6 known positives. Simply switching trigrams to top-k already
recovers three cases. The incremental TF-IDF gain at k=5 is **one case**, not four.

The same k does not produce equal queue sizes: TF-IDF has more nonzero neighbors
and a different pattern of mutual neighbors. At k=5 its queue is about 31% larger.
At k=10 the TF-IDF queue is 2.1% of all possible pairs, but still 4,532 pairs for a
downstream judge. Top 5 adds 903 TF-IDF pairs over top 3 with no additional known
positive recovered. There is no justification here for calling every candidate
actionable or sending thousands of them to a judge without evaluating cost.

### Equal candidate budgets

| Highest-scoring pairs kept globally | Trigram cases found | TF-IDF cases found |
| --- | ---: | ---: |
| 18 | 0/6 | 1/6 |
| 50 | 0/6 | 1/6 |
| 100 | 0/6 | 2/6 |

TF-IDF also improves retrieval at these equal queue sizes. A global budget can
still starve uncommon concepts; this is a cost comparison, not a proposed final
retrieval policy.

### Which examples improve?

The rank below is the better direction, taking the best eligible passage pair
within each labeled range. A case succeeds at k when that rank is at most k.

| Positive case | Trigram rank | TF-IDF rank | Interpretation |
| --- | ---: | ---: | --- |
| Plugin definition: overview and Cowork | No positive score | 7 | TF-IDF retrieves a case with no shared three-word sequences. |
| Plugin definition: overview and Government | 6 | 2 | TF-IDF promotes it into the top-5 queue. |
| Sales plugin example | 1 | 1 | Both top-k methods retrieve it; the original threshold rejected it. |
| Skill definition: overview and Government | 1 | 1 | Both top-k methods retrieve it. |
| Permanent directory slug | 1 | 1 | Both top-k methods retrieve it; TF-IDF also places it 17th globally. |
| Google Drive live sync | Not extracted | Not extracted | This is an extraction miss, not a ranking miss. |

The Drive feature bullet at `connectors/google/drive.md:51` is 11 words and is
discarded as a list item. Its FAQ answer at line 59 is 10 words and fails the
minimum length. The end-to-end retrieval ceiling under this extractor is 5/6.
Among representable positives, TF-IDF retrieves 4/5 at k=5 and 5/5 at k=10;
trigrams retrieve 3/5 and 4/5 respectively. We keep the excluded case in the
six-case totals rather than silently dropping it.

At k=5, TF-IDF also forwards 6/10 labeled negative cases and trigrams forward
5/10. These are candidates the final judge would need to dismiss, not measured
editorial false positives. Unlabeled candidates were not reviewed, so we cannot
report candidate precision or end-to-end precision. The small, reused diagnostic
set does not establish generalization.

## Decision

Keep TF-IDF as the candidate generator to develop next. **Do not escalate to
embeddings or an LLM explanation inventory on this evidence alone.** TF-IDF can
already retrieve every positive that the unchanged extractor represents.

Before testing all six, make one separate extraction experiment: admit individual
prose list items and lower the word minimum to 10 for both methods. Rerun against
the entire corpus so the added distractors count too. Do not inject only the known
Drive passages, and report that experiment separately from this fixed-input test.

Then test a bounded editorial judge on candidates plus necessary-repetition
controls. Choose a candidate budget and assess its tradeoff with recall, runtime,
and judging cost using fresh labels. The TF-IDF improvement is a reason to test
this next step, not evidence that our 90% editorial-precision target is met.

## Reproduce and inspect

```sh
uv run docs/3-check/docslint/bakeoff.py --self-check > /tmp/claude-tfidf-bakeoff.json
diff -u docs/3-check/pilot/tfidf-bakeoff.json /tmp/claude-tfidf-bakeoff.json
uv run docs/3-check/docslint/bakeoff.py --candidates > /tmp/claude-tfidf-candidates.tsv
uv run python docs/3-check/docslint/test_duplicates.py
```

`uv` installs the script's isolated scikit-learn dependency on first run. Scoring
runs locally without model downloads, PyTorch, API calls, or credentials.
The JSON records the Python and numerical-library versions; a different resolver
environment may change those metadata fields or floating-point scores. The saved
run used Python 3.13.14, scikit-learn 1.7.2, NumPy 2.5.3, and SciPy 1.18.1.

The self-check exercises ranking, tie handling, reverse-neighbor inclusion,
self/zero exclusion, word-order changes, and range eligibility. Every run also
asserts that its trigram threshold selection agrees with the existing checker.
The TSV command exports the **2,345 primary TF-IDF top-5 pairs**, including paths,
line ranges, and scores, for inspection or a subsequent judge. It is not a list
of approved editorial changes.

[Machine-readable results](tfidf-bakeoff.json) contain all 15 configurations,
per-case ranks and retrieval outcomes, package versions, and hashes of the corpus
manifest and labels. [The script](../docslint/bakeoff.py) reuses the existing
corpus loader and extraction. The original checker, labels, results, and editorial
reviews remain unchanged.
