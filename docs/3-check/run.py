# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["scikit-learn==1.7.2"]
# ///
"""Build a local candidate queue, source pages, and searchable review report."""

import argparse
import html
import json
import shutil
from pathlib import Path
import sys
from urllib.parse import quote

PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE / "docslint"))

from candidates import build, positive_int
from judge_pilot import CLASSIFICATIONS, sha256, stable_bytes
from review_report import write_report


def read_advice(path: Path | None, queue: dict) -> dict:
    if path is None:
        return {}
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or set(data) != {"queue_sha256", "cases"}:
        raise ValueError("Advice must contain queue_sha256 and cases")
    if data["queue_sha256"] != sha256(stable_bytes(queue)):
        raise ValueError("Advice does not match this queue; regenerate it for the current queue")
    if not isinstance(data["cases"], list):
        raise ValueError("Advice cases must be a list")
    known = {row["id"] for row in queue["candidates"]}
    result = {}
    fields = {"id", "classification", "needs_review", "rationale", "suggested_consolidation"}
    for row in data["cases"]:
        if not isinstance(row, dict) or set(row) != fields:
            raise ValueError("Invalid advice fields")
        case_id = row["id"]
        if not isinstance(case_id, str) or case_id not in known or case_id in result:
            raise ValueError("Advice contains an unknown or repeated candidate ID")
        if not isinstance(row["classification"], str) or row["classification"] not in CLASSIFICATIONS:
            raise ValueError("Invalid advice classification")
        if type(row["needs_review"]) is not bool:
            raise ValueError("Advice needs_review must be true or false")
        if not isinstance(row["rationale"], str) or not row["rationale"].strip():
            raise ValueError("Advice rationale must be nonempty text")
        suggestion = row["suggested_consolidation"]
        if row["classification"] == "ACTIONABLE_DUPLICATE":
            if not isinstance(suggestion, str) or not suggestion.strip():
                raise ValueError("A consolidation suggestion must contain text")
        elif suggestion is not None:
            raise ValueError("Only a consolidation suggestion may propose an edit")
        result[case_id] = row
    return result


def write_sources(corpus: Path, output: Path, queue: dict) -> None:
    for path in sorted({row["path"] for row in queue["passages"]}):
        source = corpus / path
        target = output / "sources" / (path + ".html")
        if not target.resolve().is_relative_to((output / "sources").resolve()):
            raise ValueError("Source path would escape the exported sources directory")
        target.parent.mkdir(parents=True, exist_ok=True)
        lines = "".join(
            f'<span class="line" id="L{number}"><a href="#L{number}" aria-label="Line {number}">{number}</a> {html.escape(line)}</span>'
            for number, line in enumerate(source.read_text().splitlines(), 1)
        )
        target.write_text(
            '<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(path)}</title><style>'
            'body{font:16px system-ui;margin:2rem;color:#172d38;background:#fafaf7}'
            'pre{overflow:auto;padding:1rem;background:white;border:1px solid #ccd7d6}'
            '.line{display:block;min-height:1.4em}.line:target{background:#fff0ad}'
            '.line a{display:inline-block;min-width:3ch;color:#49666a;text-align:right}'
            '</style><h1>Source snapshot</h1>'
            f'<p>{html.escape(path)}</p><pre>{lines}</pre></html>'
        )


def generate(corpus: Path, output: Path, top_k: int = 20, advice_path: Path | None = None) -> dict:
    corpus, output = corpus.resolve(), output.resolve()
    if output.is_relative_to(corpus) or corpus.is_relative_to(output / "sources"):
        raise ValueError("The corpus must not overlap the output directory or its generated sources tree")
    queue = build(corpus, top_k)
    for passage in queue["passages"]:
        passage["source_href"] = f'sources/{quote(passage["path"], safe="/")}.html#L{passage["start"]}'
    advice = read_advice(advice_path, queue)
    output.mkdir(parents=True, exist_ok=True)
    # The sources tree is generated output; replace it so old corpus text cannot linger.
    sources = output / "sources"
    if sources.exists():
        shutil.rmtree(sources)
    write_sources(corpus, output, queue)
    queue_bytes = stable_bytes(queue)
    (output / "queue.json").write_bytes(queue_bytes)
    write_report(queue, output / "review.html", advice)
    summary = {"passages": queue["passage_count"], "candidates": queue["candidate_count"],
               "advisory_notes": len(advice), "queue_sha256": sha256(queue_bytes),
               "report": str(output / "review.html")}
    (output / "run.json").write_bytes(stable_bytes(summary))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=PACKAGE.parents[1] / "corpus")
    parser.add_argument("--output-dir", type=Path, default=PACKAGE / "output.local")
    parser.add_argument("--top-k", type=positive_int, default=20)
    parser.add_argument("--advice", type=Path, help="Optional queue-bound advisory notes; never filters candidates")
    args = parser.parse_args()
    try:
        result = generate(args.corpus, args.output_dir, args.top_k, args.advice)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(f"Ready: {result['candidates']:,} candidates from {result['passages']:,} passages.")
    print(f"Open {result['report']}")


if __name__ == "__main__":
    main()
