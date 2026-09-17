# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["scikit-learn==1.7.2"]
# ///
"""Compare candidate retrieval on the frozen corpus; no editorial judgments."""

import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import sys

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from duplicates import Passage, evaluate, find_duplicates, load_corpus, words


def similarities(items: list[Passage]) -> dict[str, np.ndarray]:
    texts = [" ".join(words(item.text)) for item in items]
    vectors = TfidfVectorizer(ngram_range=(1, 2), stop_words="english",
                             sublinear_tf=True, norm="l2").fit_transform(texts)
    # ponytail: dense pair scores fit this 54-page experiment; block multiplication at larger scale.
    tfidf = (vectors @ vectors.T).toarray()
    shingles = []
    for text in texts:
        tokens = text.split()
        shingles.append(set(zip(tokens, tokens[1:], tokens[2:])))
    trigram = np.zeros_like(tfidf)
    for a in range(len(items)):
        for b in range(a + 1, len(items)):
            if shingles[a] and shingles[b]:
                trigram[a, b] = trigram[b, a] = (
                    len(shingles[a] & shingles[b]) / min(len(shingles[a]), len(shingles[b])))
    for matrix in (trigram, tfidf):
        np.fill_diagonal(matrix, 0)
        matrix[:] = matrix.round(12)
    return {"trigram": trigram, "tfidf": tfidf}


def ranked_pairs(matrix):
    """Positive-score pairs, with directional rank and deterministic index tie breaks."""
    ranks = {}
    for a, row in enumerate(matrix):
        neighbors = sorted((b for b in range(len(row)) if b != a and row[b] > 0),
                           key=lambda b: (-row[b], b))
        ranks.update({(a, b): rank for rank, b in enumerate(neighbors, 1)})
    pairs = sorted(((a, b) for a, b in ranks if a < b),
                   key=lambda pair: (-matrix[pair], pair))
    return pairs, ranks


def top_k(pairs, ranks, k):
    return {pair for pair in pairs if min(ranks[pair], ranks[pair[::-1]]) <= k}


def case_pairs(examples, items):
    result = {}
    for example in examples:
        sides = []
        for name in ("left", "right"):
            span = example[name]
            sides.append([i for i, item in enumerate(items)
                          if item.path == span["path"] and span["start"] <= item.start
                          and item.end <= span["end"]])
        result[example["id"]] = {tuple(sorted((a, b)))
                                 for a in sides[0] for b in sides[1] if a != b}
    return result


def summarize(name, selected, cases, examples):
    positives = [e for e in examples if e["duplicate"]]
    negatives = [e for e in examples if not e["duplicate"]]
    found = [e["id"] for e in examples if cases[e["id"]] & selected]
    return {
        "method": name,
        "candidate_pairs": len(selected),
        "positive_cases_retrieved": sum(e["id"] in found for e in positives),
        "positive_cases_total": len(positives),
        "eligible_positive_cases": sum(bool(cases[e["id"]]) for e in positives),
        "negative_cases_retrieved": sum(e["id"] in found for e in negatives),
        "negative_cases_total": len(negatives),
        "retrieved_case_ids": found,
    }


def run(root: Path, examples_path: Path, *, expanded_extraction: bool = False):
    min_words = 10 if expanded_extraction else 15
    snapshot, items = load_corpus(root, min_words, include_lists=expanded_extraction)
    examples = json.loads(examples_path.read_text())
    evaluate(examples, [], root)  # Validate frozen labels and source ranges before scoring.
    cases = case_pairs(examples, items)
    matrices = similarities(items)
    rankings = {name: ranked_pairs(matrix) for name, matrix in matrices.items()}
    baseline = {pair for pair in rankings["trigram"][0] if matrices["trigram"][pair] >= 0.5}
    # Check agreement with the shared checker on this mode's passage set.
    index = {(p.path, p.start, p.end): i for i, p in enumerate(items)}
    archived = {tuple(sorted(index[(f[side]["path"], f[side]["start"], f[side]["end"])]
                             for side in ("left", "right")))
                for f in find_duplicates(items, 0.5)}
    assert baseline == archived, "Trigram selection diverged from the existing checker"
    baseline_name = "expanded_trigram_0.5" if expanded_extraction else "published_trigram_0.5"
    summaries = [summarize(baseline_name, baseline, cases, examples)]
    for name, (pairs, ranks) in rankings.items():
        for k in (1, 3, 5, 10):
            summaries.append(summarize(f"{name}_top_{k}", top_k(pairs, ranks, k), cases, examples))
        for budget in (18, 50, 100):
            summaries.append(summarize(f"{name}_budget_{budget}", set(pairs[:budget]), cases, examples))
    details = []
    for example in examples:
        detail = {"id": example["id"], "split": example["split"],
                  "duplicate": example["duplicate"], "eligible": bool(cases[example["id"]])}
        for name, matrix in matrices.items():
            pairs, ranks = rankings[name]
            candidates = cases[example["id"]]
            if not candidates:
                detail[name] = None
                continue
            pair = min(candidates, key=lambda p: (-matrix[p], p))
            directional_ranks = [ranks[p] for pair in candidates
                                 for p in (pair, pair[::-1]) if p in ranks]
            detail[name] = {
                "highest_score": round(float(matrix[pair]), 6),
                "best_global_rank": pairs.index(pair) + 1 if pair in pairs else None,
                "best_direction_rank": min(directional_ranks) if directional_ranks else None,
            }
        details.append(detail)
    result = {
        "snapshot": snapshot,
        "examples_sha256": hashlib.sha256(examples_path.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "packages": {name: version(name) for name in ("scikit-learn", "numpy", "scipy")},
        "settings": {"min_words": min_words, "ngram_range": [1, 2], "stop_words": "english",
                     "sublinear_tf": True, "norm": "l2", "smooth_idf": True,
                     "floor": "score > 0", "primary_k": 5,
                     "pair_policy": "either direction; self excluded; same-page pairs retained",
                     "tie_break": "score rounded to 12 decimals, then corpus path/line order"},
        "passage_count": len(items),
        "possible_pairs": len(items) * (len(items) - 1) // 2,
        "runs": summaries,
        "cases": details,
    }
    if expanded_extraction:
        result["settings"]["include_unordered_lists"] = True
    return result, items, matrices, rankings


def self_check():
    # Ties, reverse-neighbor inclusion, self/zero exclusion, and a fair global budget.
    matrix = np.array([[0, .9, .9, 0], [.9, 0, .2, .8], [.9, .2, 0, 0], [0, .8, 0, 0]])
    pairs, ranks = ranked_pairs(matrix)
    assert pairs[:2] == [(0, 1), (0, 2)]
    assert top_k(pairs, ranks, 1) == {(0, 1), (0, 2), (1, 3)}
    assert (0, 3) not in pairs
    items = [Passage("a.md", 1, 1, "alpha beta gamma delta"),
             Passage("b.md", 2, 2, "delta gamma beta alpha"),
             Passage("c.md", 3, 3, "oranges apples pears plums")]
    scores = similarities(items)
    assert scores["trigram"][0, 1] == 0
    assert scores["tfidf"][0, 1] > scores["tfidf"][0, 2] == 0
    examples = [{"id": "one", "left": {"path": "a.md", "start": 1, "end": 1},
                 "right": {"path": "b.md", "start": 1, "end": 2}}]
    assert case_pairs(examples, items) == {"one": {(0, 1)}}
    examples[0]["right"]["end"] = 1
    assert case_pairs(examples, items) == {"one": set()}
    print("PASS: ranking, ties, pair deduplication, lexical retrieval, and span eligibility", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--candidates", action="store_true", help="Print TF-IDF top-5 pairs as TSV")
    parser.add_argument("--examples", type=Path, help="Evaluation labels; defaults to the original examples")
    parser.add_argument("--expanded-extraction", action="store_true",
                        help="Include unordered list prose and lower the minimum to 10 words")
    args = parser.parse_args()
    if args.self_check:
        self_check()
    project = Path(__file__).resolve().parents[2]
    result, items, matrices, rankings = run(project / "corpus", args.examples or project / "3-check/pilot/examples.json",
                                          expanded_extraction=args.expanded_extraction)
    if args.candidates:
        print("left_path\tleft_start\tleft_end\tright_path\tright_start\tright_end\tscore")
        pairs, ranks = rankings["tfidf"]
        chosen = top_k(pairs, ranks, 5)
        for a, b in pairs:
            if (a, b) in chosen:
                p, q = items[a], items[b]
                print(f"{p.path}\t{p.start}\t{p.end}\t{q.path}\t{q.start}\t{q.end}\t{matrices['tfidf'][a, b]:.6f}")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
