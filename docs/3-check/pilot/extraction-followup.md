# Expanded extraction follow-up

**The extraction gap is fixed. TF-IDF top-10 now retrieves all six known positive
cases.** This is a separate full-corpus experiment after the
[fixed-input bake-off](tfidf-bakeoff.md), with the same labels and retrieval
settings. It measures candidate retrieval, not editorial accuracy.

## Change

`uv run docs/3-check/docslint/bakeoff.py --expanded-extraction` admits unordered Markdown list
items and their indented prose continuations, and lowers the minimum from 15 to
10 words. Each list item begins a new passage; blank lines still separate prose
paragraphs. Numbered items and their prose continuations remain excluded, as do
fenced code, tables, navigation cards, and `Steps` bodies.

In expanded mode, list state ends at sibling MDX and fenced-code boundaries;
blocks indented inside an item retain its state. This also
admits five valid standalone paragraphs in Microsoft 365 accordion sections that
the legacy parser skips after a list. They remain eligible as ordinary prose,
not as continuations of the preceding item. The frozen legacy mode retains its
original behavior for reproducibility.

Both retrievers receive the same **980 passages** from all 54 pages, compared with
661 in the earlier run. There are 479,710 possible unordered pairs. This includes
every additional eligible passage, not just the known missing example. TF-IDF's
vocabulary and IDF weights are refitted on the full expanded set.

The Google Drive feature bullet at `connectors/google/drive.md:51` has 11 words;
its FAQ answer at line 59 has 10. Both now enter retrieval with exact source text
and line ranges. They rank first in either method's better retrieval direction.

The feature is opt-in in the shared extractor. The original checker and the
default bake-off still use the old passage selection and reproduce their saved
results. Source files, labels, and prior JSON artifacts are unchanged.

## Results

| Policy | Trigram cases found | Trigram pairs | TF-IDF cases found | TF-IDF pairs |
| --- | ---: | ---: | ---: | ---: |
| Top 1 | 3/6 | 677 | 4/6 | 762 |
| Top 3 | 4/6 | 1,718 | 5/6 | 2,141 |
| Top 5 | 4/6 | 2,504 | 5/6 | 3,486 |
| Top 10 | 5/6 | 3,901 | **6/6** | **6,755** |

The expanded trigram 0.5 threshold returns 40 pairs and retrieves 1/6 known
positives. This is a new run on different inputs, not the published 18-pair
baseline. At equal global budgets, TF-IDF retrieves 1/6 in 18 pairs and 2/6 in
50 or 100 pairs; trigrams retrieve 1/6 at all three budgets.

| Positive case | Trigram best-direction rank | TF-IDF best-direction rank |
| --- | ---: | ---: |
| Plugin definition: overview and Cowork | No positive score | 8 |
| Plugin definition: overview and Government | 7 | 2 |
| Sales plugin example | 1 | 1 |
| Skill definition: overview and Government | 2 | 1 |
| Google Drive live sync | 1 | 1 |
| Permanent directory slug | 1 | 1 |

Adding competing passages changes rankings as well as coverage. For example,
the TF-IDF Cowork plugin match moves from rank 7 to rank 8. The six-case result
was measured after reranking everything, not inferred by adding one success to
the earlier total.

## Interpretation

Keep TF-IDF for the next step; these results do not justify a heavier retrieval
method yet. The known extraction failure no longer prevents a 6/6 result.

The queue is still substantial. Top-10 TF-IDF forwards 6,755 pairs, about 1.4% of
all possibilities, and includes 7/10 labeled negative cases. Top 3 finds five
positives in 2,141 pairs; top 5 adds 1,345 pairs without another known positive.
These are costs to evaluate before judging the full queue. No model judge was
run, and unlabeled pairs were not reviewed.

Unordered lists can contain instructions, prerequisites, or warnings as well as
explanations. Inclusion does not classify a bullet as explanatory prose; a later
editorial judge must distinguish necessary repetition. This remains the small
snapshot-specific Markdown parser, with limited nested-list/MDX handling. The
six known cases are diagnostic and reused, not a held-out accuracy benchmark.

## Reproduce

```sh
uv run python docs/3-check/docslint/test_duplicates.py
uv run docs/3-check/docslint/bakeoff.py --self-check > /tmp/claude-original.json
diff -u docs/3-check/pilot/tfidf-bakeoff.json /tmp/claude-original.json
uv run docs/3-check/docslint/bakeoff.py --expanded-extraction --self-check > /tmp/claude-expanded.json
diff -u docs/3-check/pilot/tfidf-expanded.json /tmp/claude-expanded.json
uv run docs/3-check/docslint/bakeoff.py --expanded-extraction --candidates > /tmp/claude-expanded-candidates.tsv
```

The last command exports the expanded primary top-5 queue of 3,486 pairs. The
tests check opt-in extraction, wrapped list text, short-item filtering, numbered
step exclusion, transitions through fences and sibling MDX components, source
ranges, and the two real Drive passages. Existing baseline
verification still passes. Both runs reproduce exactly in the recorded local
environment; the [earlier dependency-version caveat](tfidf-bakeoff.md#reproduce-and-inspect)
still applies.

[tfidf-expanded.json](tfidf-expanded.json) records all 15 configurations, case
ranks, input hashes, settings, and runtime versions.
