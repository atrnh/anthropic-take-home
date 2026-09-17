# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["scikit-learn==1.7.2"]
# ///
"""Export a complete TF-IDF candidate queue for human review; no judge filtering."""

import argparse
from importlib.metadata import version
import json
from pathlib import Path
import platform

from bakeoff import case_pairs, ranked_pairs, similarities, summarize, top_k
from duplicates import evaluate, load_corpus
from judge_pilot import packet_side, pair_hash, sha256, stable_bytes


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def build(corpus: Path, k: int = 20, examples_paths: tuple[Path, ...] = ()) -> dict:
    if type(k) is not int or k < 1:
        raise ValueError("k must be a positive integer")
    snapshot, items = load_corpus(
        corpus, 10, include_lists=True, include_ordered_lists=True
    )
    matrix = similarities(items)["tfidf"]
    pairs, ranks = ranked_pairs(matrix)
    selected = top_k(pairs, ranks, k)
    candidates = [
        {"id": pair_hash(items[a], items[b]), "left": a, "right": b,
         "score": float(matrix[a, b]), "left_rank": ranks[a, b],
         "right_rank": ranks[b, a]}
        for a, b in pairs if (a, b) in selected
    ]
    coverage = []
    for path in examples_paths:
        raw = path.read_bytes()
        examples = json.loads(raw)
        evaluate(examples, [], corpus)
        cases = case_pairs(examples, items)
        details = []
        for row in examples:
            matches = [pair for pair in pairs if pair in cases[row["id"]] and pair in selected]
            eligible_ranks = [ranks[p] for pair in cases[row["id"]]
                              for p in (pair, pair[::-1]) if p in ranks]
            details.append({
                "id": row["id"], "duplicate": row["duplicate"],
                "eligible": bool(cases[row["id"]]), "retrieved": bool(matches),
                "best_direction_rank": min(eligible_ranks) if eligible_ranks else None,
                "example_candidate_id": pair_hash(items[matches[0][0]], items[matches[0][1]]) if matches else None,
            })
        coverage.append({
            "examples_sha256": sha256(raw),
            "summary": summarize(f"tfidf_top_{k}", selected, cases, examples),
            "cases": details,
        })
    return {
        "schema_version": 1, "snapshot": snapshot,
        "settings": {"min_words": 10, "include_unordered_lists": True,
                     "include_ordered_lists": True, "top_k": k,
                     "ordered_list_chunks": "Contiguous same-indent items together; blank lines and code split chunks",
                     "pair_policy": "Either direction; self and zero-score pairs excluded",
                     "judge_policy": "Advisory only; no judge verdict removes or approves a candidate"},
        "runtime": {"python": platform.python_version(),
                    "packages": {name: version(name) for name in ("scikit-learn", "numpy", "scipy")}},
        "passage_count": len(items), "candidate_count": len(candidates),
        "passages": [packet_side(corpus, item) for item in items],
        "candidates": candidates, "coverage": coverage,
    }


def main() -> None:
    project = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=project / "corpus")
    parser.add_argument("--top-k", type=positive_int, default=20)
    parser.add_argument("--examples", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    queue = build(args.corpus, args.top_k, tuple(args.examples))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(stable_bytes(queue))
    print(json.dumps({"output": str(args.output), "passages": queue["passage_count"],
                      "candidates": queue["candidate_count"], "coverage": queue["coverage"]}, indent=2))


if __name__ == "__main__":
    main()
