# Candidate coverage and advisory judgment

The working review queue now includes numbered Markdown checklists and retrieves
up to 20 neighbors per passage. Judge verdicts do not filter this queue. Every
candidate remains available for human review, including pairs a judge might keep
or consider distinct. Neither a similarity score nor a model suggestion approves
an edit.

## Coverage result

| Configuration | Passages | Candidate pairs | Familiar positives found | Fresh positives found |
| --- | ---: | ---: | ---: | ---: |
| Previous extraction, top 10 | 980 | 6,755 | 6/6 | 1/3 |
| Numbered checklists included, top 10 | 1,027 | 7,108 | 6/6 | 2/3 |
| Numbered checklists included, top 20 | 1,027 | 13,786 | 6/6 | 3/3 |

The testing checklist is extracted as one contiguous sequence, keeping its short
custom-connector, Inspector, and Claude Code steps together. Its best match ranks
2nd. MCPB's best match ranks 18th in the enlarged corpus, so it requires the wider
queue. The allowlist match ranks 1st. The [coverage artifact](candidate-coverage.json)
records label hashes, case-level results, and actual retrieved passages for all nine
positive examples. Finding a smaller passage inside each labeled pair establishes
retrieval coverage; it does not verify the proposed consolidation treatment.

This change responds to observed misses on the same small evaluation set. It is
adaptive tuning, not new held-out evidence or a corpus-wide recall estimate.
Candidate volume is about twice the previous queue. Precision and review effort
for the added candidates have not been measured. The list of negative examples
still retrieves seven familiar negatives and one fresh negative; those pairs are
deliberately retained for editorial review.

## Generate the queue

From the repository root:

```sh
uv run docs/3-check/docslint/candidates.py --output /tmp/claude-review-queue.json
cmp docs/3-check/pilot/review-queue.json /tmp/claude-review-queue.json
```

The generated JSON is ignored by Git through the existing `*.local` rule. It stores:

- `passages`: source paths, exact lines, headings, text, and neighboring context.
- `candidates`: stable span-pair IDs, similarity scores, directional ranks, and
  zero-based `left`/`right` indexes into `passages`, sorted by descending similarity.
- Snapshot and runtime metadata for reproduction.

Use `--top-k 10` for a smaller queue, accepting the measured MCPB miss. There is no
judge input to this command and no verdict-based suppression, approval, or automatic
editing. The existing judge experiment remains available for advisory suggestions;
this change adds no automatic inference service or advice-import integration.

For diagnostic coverage, repeat `--examples` for the relevant label files:

```sh
uv run docs/3-check/docslint/candidates.py \
  --examples docs/3-check/pilot/judge-v5/examples-adjudicated.json \
  --examples docs/3-check/pilot/judge-v5/examples-fresh.json \
  --output /tmp/claude-queue-coverage.json
```

The diagnostic queue adds coverage labels but contains exactly the same candidate
pairs. Keep that diagnostic output away from any blinded judge. The normal command
omits evaluation labels.

## Extraction boundaries and compatibility

Numbered items at the same indentation stay together when contiguous. Blank lines,
code blocks, and mixed/nested list boundaries split chunks; this is a snapshot-focused
Markdown extractor, not a complete Markdown parser. The minimum remains 10 words
per extracted chunk. Unordered items keep their existing per-item behavior.

Fenced code, tables, navigation cards, and MDX `Steps`, `Columns`, and `CodeGroup`
content remain excluded. This does not claim coverage of every procedure or warning.
The lower-level numbered-list option defaults to off, so historical extraction,
bake-off, and judge-pilot artifacts still reproduce unchanged. The new candidate
command enables it and uses top 20 by default.

## Verification

```sh
uv run python docs/3-check/docslint/test_duplicates.py
uv run docs/3-check/docslint/test_candidates.py
uv run docs/3-check/docslint/test_judge_pilot.py
```

The checks cover checklist grouping and source ranges, exclusions, invalid limits,
retention of a negatively labeled pair in the queue, and historical artifact
reproduction. The complete generated queue was also regenerated and compared
byte-for-byte in the recorded environment. No new judge run was used to select or
filter these candidates. The v5 treatment-quality limitations remain open.
