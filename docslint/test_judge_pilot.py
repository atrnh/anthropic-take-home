# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["scikit-learn==1.7.2"]
# ///
"""Run with `uv run docslint/test_judge_pilot.py`."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile

from judge_pilot import evaluate, headings_before, prepare, sha256, stable_bytes


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "docs/3-check"


def reject(call, message: str) -> None:
    try:
        call()
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return
    raise AssertionError(message)


def judgments(packet: dict, manifest: dict) -> dict:
    examples = {row["id"]: row for row in json.loads((ARTIFACTS / "examples.json").read_text())}
    records = {row["id"]: row for row in manifest["selection"]["cases"]}
    abstained = False
    rows = []
    for case in packet["cases"]:
        record = records[case["id"]]
        duplicate = (record["source_group"] == "known"
                     and examples[record["example_id"]]["duplicate"])
        needs_review = bool(duplicate and not abstained)
        abstained |= needs_review
        classification = "ACTIONABLE_DUPLICATE" if duplicate else "RELATED_BUT_DISTINCT"
        rows.append({
            "id": case["id"], "classification": classification,
            "needs_review": needs_review,
            "shared_explanation": "A concise shared explanation.",
            "unique_left": "Left-specific context.", "unique_right": "Right-specific context.",
            "rationale": "The target passages have the stated editorial relationship.",
            "suggested_consolidation": "Keep one explanation and preserve unique context."
            if duplicate else None,
            "evidence": {
                side: next(line for line in case[side]["text"].splitlines() if line.strip())
                for side in ("left", "right")
            },
        })
    return {"cases": rows}


def check() -> None:
    packet_path = ARTIFACTS / "judge-packet.json"
    manifest_path = ARTIFACTS / "judge-manifest.json"
    packet = json.loads(packet_path.read_text())
    manifest = json.loads(manifest_path.read_text())

    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        generated_packet, generated_manifest = prepare(temp)
        assert generated_packet.read_bytes() == packet_path.read_bytes()
        assert generated_manifest.read_bytes() == manifest_path.read_bytes()

        valid_path = temp / "valid.json"
        valid_path.write_bytes(stable_bytes(judgments(packet, manifest)))
        metrics = evaluate(packet_path, manifest_path, valid_path)
        assert metrics["known"]["counts"] == {"TP": 5, "FP": 0, "FN": 0, "TN": 10}
        assert metrics["known"]["abstentions"] == 1
        assert metrics["known"]["conditional_recall"] == {
            "numerator": 5, "denominator": 5, "value": 1.0,
        }
        assert metrics["known"]["recall"] == {
            "numerator": 5, "denominator": 6, "value": 5 / 6,
        }
        assert metrics["known"]["coverage"] == {
            "numerator": 15, "denominator": 16, "value": 15 / 16,
        }
        assert set(metrics["new_sample"]) == {"classification_counts", "abstentions"}

        def files(changed_packet: dict, changed_manifest: dict, *, bind: bool = True):
            packet_copy = temp / "changed-packet.json"
            manifest_copy = temp / "changed-manifest.json"
            raw = stable_bytes(changed_packet)
            packet_copy.write_bytes(raw)
            if bind:
                changed_manifest["packet_sha256"] = sha256(raw)
            manifest_copy.write_bytes(stable_bytes(changed_manifest))
            return packet_copy, manifest_copy

        changed = deepcopy(packet)
        changed["cases"][0]["left"]["context_text"] += "tampered"
        paths = files(changed, deepcopy(manifest))
        reject(lambda: evaluate(*paths, valid_path), "Context tampering was accepted")

        changed = deepcopy(packet)
        changed["cases"][0]["left"]["path"] = "../outside.md"
        paths = files(changed, deepcopy(manifest))
        reject(lambda: evaluate(*paths, valid_path), "Path traversal was accepted")

        changed = deepcopy(packet)
        changed["cases"][0]["left"]["start"] = True
        paths = files(changed, deepcopy(manifest))
        reject(lambda: evaluate(*paths, valid_path), "Boolean line number was accepted")

        changed = deepcopy(packet)
        changed["cases"][0]["left"]["text"] += "tampered"
        paths = files(changed, deepcopy(manifest), bind=False)
        reject(lambda: evaluate(*paths, valid_path), "Packet hash mismatch was accepted")

        for field in ("examples_sha256", "results_sha256", "prompt_sha256"):
            changed_manifest = deepcopy(manifest)
            changed_manifest.pop(field)
            paths = files(deepcopy(packet), changed_manifest, bind=False)
            reject(lambda: evaluate(*paths, valid_path), f"Missing {field} binding was accepted")

        changed_manifest = deepcopy(manifest)
        known = [row for row in changed_manifest["selection"]["cases"]
                 if row["source_group"] == "known"]
        known[0]["example_id"], known[1]["example_id"] = known[1]["example_id"], known[0]["example_id"]
        paths = files(deepcopy(packet), changed_manifest, bind=False)
        reject(lambda: evaluate(*paths, valid_path), "Swapped example provenance was accepted")

        bad = judgments(packet, manifest)
        bad["cases"][0]["evidence"]["left"] = "not literal evidence"
        bad_path = temp / "bad-judgments.json"
        bad_path.write_bytes(stable_bytes(bad))
        reject(lambda: evaluate(packet_path, manifest_path, bad_path), "Invalid evidence was accepted")

        bad = judgments(packet, manifest)
        bad["cases"].pop()
        bad["cases"].append(deepcopy(bad["cases"][0]))
        bad_path.write_bytes(stable_bytes(bad))
        reject(lambda: evaluate(packet_path, manifest_path, bad_path), "Duplicate and missing IDs were accepted")

    fenced = ["# Real", "```md", "## Fake", "```", "## Actual", "target"]
    assert headings_before(fenced, 6) == ["Real", "Actual"]

    evaluated = evaluate(packet_path, manifest_path, ARTIFACTS / "judge-decisions.json")
    assert evaluated == json.loads((ARTIFACTS / "judge-metrics.json").read_text())
    print("PASS: deterministic preparation, strict bindings, judgment validation, and abstention metrics")


if __name__ == "__main__":
    check()
