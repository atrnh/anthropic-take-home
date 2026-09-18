# Review candidate passages

Use this guide to generate and review the candidate queue described in the
[project overview](README.md).

## Start here

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and a browser.
Run this command from the repository root:

```sh
uv run 3-check/run.py
```

The command uses the checked-in, 54-page Claude Docs snapshot. On the first run,
uv prepares the script's Python environment and dependencies. No model account or
API key is needed. Open the printed `review.html` path in your browser, or open
`3-check/output.local/review.html` after the command finishes.

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
hashes before processing. The historical [fetch script](docslint/fetch_corpus.py)
records how this snapshot was obtained. It references a local path and an
untracked URL list, so it is not a portable refresh command. This package normally runs
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

## Verify the workflow

Run these checks from the repository root:

```sh
uv run 3-check/test_workflow.py
uv run python 3-check/docslint/test_archive.py
uv run python 3-check/docslint/test_duplicates.py
uv run 3-check/docslint/test_candidates.py
uv run 3-check/docslint/test_judge_pilot.py
```
