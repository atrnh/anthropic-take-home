# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["scikit-learn==1.7.2"]
# ///
"""Replay saved judge runs against Ashley's post-run Drive adjudication."""

from collections import Counter
import json
from pathlib import Path

from judge_pilot import evaluate, sha256


def main():
    project = Path(__file__).resolve().parents[3]
    directory = project / "docs/3-check/pilot/judge-v2"
    labels_path = project / "docs/3-check/pilot/examples.json"
    labels = {row["id"]: row["duplicate"] for row in json.loads(labels_path.read_text())}
    drive = "evaluation-drive-live-sync-faq"
    assert labels[drive] is True, "Historical label changed; revisit this comparison"
    labels[drive] = False
    runs = {}
    for name, prompt, manifest, decisions in (
        ("control", "../judge-prompt.md", "control-manifest.json", "control-decisions.json"),
        ("v3", "prompt-v3.md", "v3-manifest.json", "v3-decisions.json"),
        ("v4", "prompt-v4.md", "v4-manifest.json", "v4-decisions.json"),
    ):
        result = evaluate(
            directory / "judge-packet.json", directory / manifest,
            directory / decisions, prompt_path=directory / prompt,
        )
        counts = Counter(TP=0, FP=0, FN=0, TN=0, ABSTAIN=0)
        outcomes = []
        for row in result["known"]["outcomes"]:
            predicted = row["classification"] == "ACTIONABLE_DUPLICATE"
            expected = labels[row["example_id"]]
            outcome = "ABSTAIN" if row["needs_review"] else (
                ("T" if predicted == expected else "F") + ("P" if predicted else "N")
            )
            counts[outcome] += 1
            outcomes.append({**row, "expected_duplicate": expected, "outcome": outcome})
        assert sum(counts.values()) == len(labels) == 16
        runs[name] = {
            "provenance": result["provenance"],
            "historical_counts": result["known"]["counts"],
            "adjudicated_counts": dict(counts),
            "coverage": (16 - counts["ABSTAIN"]) / 16,
            "recall": counts["TP"] / sum(labels.values()),
            "outcomes": outcomes,
            "sample": result["new_sample"],
        }
    print(json.dumps({
        "scope": "Post-hoc rescoring of familiar cases; not held-out accuracy",
        "historical_labels_sha256": sha256(labels_path.read_bytes()),
        "label_override": {
            "example_id": drive, "duplicate": False,
            "classification": "NECESSARY_REPETITION",
            "authority": "Ashley explicitly chose to keep both passages after adopting case-by-case FAQ policy.",
        },
        "runs": runs,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
