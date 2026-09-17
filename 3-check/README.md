# Review duplicated explanatory prose

This local workflow finds passages worth comparing and presents them side by side
for an editor. It uses TF-IDF word similarity to retrieve candidates. Similarity
is not a duplicate verdict, and optional model advice never removes a candidate.

## Start here

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and a browser.
Run this command from the repository root:

```sh
uv run 3-check/run.py
```

The command uses the checked-in, 54-page Claude Docs snapshot. On the first run,
uv prepares the script's Python environment and dependencies. No model account or
API key is needed. Open the printed `review.html` path in your browser, or open
[the generated report](output.local/review.html) after the command finishes.

The default run creates `3-check/output.local/` with:

| File | Purpose |
| --- | --- |
| `review.html` | Searchable, paginated review report; opens directly as a local file |
| `queue.json` | Complete candidate queue and source excerpts |
| `sources/` | Escaped source copies with working line-number links |
| `run.json` | Queue checksum, counts, and report location |

Generated output is ignored by Git. Rerunning the command replaces the generated
files, including replacing the entire generated `sources/` tree. Keep your own
files outside that tree. To share a report with working source links, copy the whole output folder.
The report contains source text from the corpus you provide.

## Review a pair

1. Search for a topic or source path to focus the queue. The page-pairing filter
   separates same-page from cross-page comparisons. **Clear filters** restores
   access to every candidate; the page controls reach the full queue.
2. Read both excerpts and expand their neighboring context. Source links open
   line-numbered copies of the snapshot, not live product documentation.
3. Decide whether there is a useful consolidation. Preserve necessary local
   warnings, prerequisites, and short answers. For useful overlap, consider merging
   general additions into the shared explanation before shortening another page.
4. Record the decision in your normal editorial workflow. This report does not
   save review decisions or edit documentation. Treat any advisory suggestion as
   a proposal, even when its author did not request additional review.

See the [worked example](worked-example.md) for one consolidation and one case
where repetition should remain.

## Change the input or queue size

```sh
uv run 3-check/run.py --top-k 10 --output-dir /tmp/docs-review
uv run 3-check/run.py --corpus /path/to/snapshot --output-dir /tmp/other-review
```

The input is a pinned Markdown snapshot, not an arbitrary directory of files. It
must contain `manifest.json` with `fetched_at`, `page_count`, and a `pages` list;
each page needs a relative `path` and its file's `sha256`. The loader verifies the
hashes before processing. The existing [fetch script](docslint/fetch_corpus.py)
documents how this repository's snapshot was obtained. This package normally runs
inside this repository, where the default `corpus/` remains at the repository root.

The default selects each passage's top 20 positive-score neighbors, then combines
both directions. A passage can appear in more than 20 pairs when other passages
select it. Top 10 creates a smaller queue but misses the known MCPB example.

## Optional advisory notes

The workflow does not call a model. You can review selected passages separately
using the archived [v5 rubric](pilot/judge-v5/prompt.md), or supply your own notes.
Keep evaluation labels out of any blinded model input.

To display notes in the report, create a JSON file with the checksum from
`output.local/run.json` and candidate IDs from `queue.json`:

```json
{
  "queue_sha256": "copy the queue checksum",
  "cases": [
    {
      "id": "copy an exact candidate ID",
      "classification": "NECESSARY_REPETITION",
      "needs_review": false,
      "rationale": "Both procedures need this prerequisite beside their own steps.",
      "suggested_consolidation": null
    }
  ]
}
```

Then rerun with the same corpus and retrieval settings:

```sh
uv run 3-check/run.py --advice /path/to/advice.json
```

Allowed classifications are `ACTIONABLE_DUPLICATE`, `NECESSARY_REPETITION`, and
`RELATED_BUT_DISTINCT`. Only `ACTIONABLE_DUPLICATE` takes a nonempty consolidation
suggestion; the other two use `null`. Notes may cover a subset of the queue. The
loader rejects stale checksums, unknown or repeated IDs, and malformed fields.
These checks establish which queue a note belongs to, not whether it is correct.
All candidates remain in their original order with or without notes.

## What the evidence supports

The default snapshot produces **1,027 passages and 13,786 candidate pairs**. It
retrieves all six familiar positives and all three approved fresh positives in
the small pilot. The wider queue's precision and human review effort have not
been measured. These cases informed the implementation, so they do not establish
general recall.

The extractor includes prose, unordered items, and contiguous numbered checklists.
It skips code, tables, navigation cards, and MDX step containers. It is tailored
to this snapshot rather than a complete Markdown parser. A 10-word minimum can
exclude short explanations. TF-IDF can miss paraphrases that share little wording.

Model judgments varied between runs, and correct duplicate labels sometimes led
to incomplete merge suggestions. Model advice therefore stays optional and advisory.
This is an informal local review workflow, not an automatic documentation gate.

## Pilot archive and verification

All pilot artifacts live under [pilot/](pilot/README.md), including rejected
experiments, source-bound packets, decisions, labels, metrics, and the frozen queue.
The relocation manifest records their original and current checksums. Only narrative
links and reproduction commands were updated during migration; JSON evidence and
rubric prompts retain their original bytes.

```sh
uv run 3-check/test_workflow.py
uv run python 3-check/docslint/test_archive.py
uv run python 3-check/docslint/test_duplicates.py
uv run 3-check/docslint/test_candidates.py
uv run 3-check/docslint/test_judge_pilot.py
```

Implementation lives in [docslint/](docslint); the [starter](run.py) builds the
queue, exports sources, and renders the [static report](report.html). No server,
database, provider integration, or JavaScript build step is required.
