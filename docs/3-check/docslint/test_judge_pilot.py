# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["scikit-learn==1.7.2"]
# ///
"""Run with `uv run docs/3-check/docslint/test_judge_pilot.py`."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile

from judge_pilot import evaluate, headings_before, prepare, sha256, stable_bytes


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "docs/3-check/pilot"


def reject(call, message: str) -> None:
    try:
        call()
    except (FileNotFoundError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return
    raise AssertionError(message)


def judgments(packet: dict, manifest: dict, examples_path: Path | None = None) -> dict:
    examples_path = examples_path or ARTIFACTS / "examples.json"
    examples = {row["id"]: row for row in json.loads(examples_path.read_text())}
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

        alternate_prompt = temp / "alternate-prompt.md"
        alternate_prompt.write_text("Alternate judge instructions.\n")
        alternate_dir = temp / "alternate"
        alternate_packet_path, alternate_manifest_path = prepare(
            alternate_dir, prompt_path=alternate_prompt, sample_offset=2
        )
        alternate_packet = json.loads(alternate_packet_path.read_text())
        alternate_manifest = json.loads(alternate_manifest_path.read_text())
        repeat_dir = temp / "repeat"
        repeat_packet, repeat_manifest = prepare(
            repeat_dir, prompt_path=alternate_prompt, sample_offset=2
        )
        assert repeat_packet.read_bytes() == alternate_packet_path.read_bytes()
        assert repeat_manifest.read_bytes() == alternate_manifest_path.read_bytes()
        assert alternate_manifest["prompt_sha256"] == sha256(alternate_prompt.read_bytes())
        assert alternate_manifest["selection"]["sample_offset"] == 2

        original_known = {
            row["id"] for row in manifest["selection"]["cases"]
            if row["source_group"] == "known"
        }
        alternate_known = {
            row["id"] for row in alternate_manifest["selection"]["cases"]
            if row["source_group"] == "known"
        }
        original_sample = {
            row["id"] for row in manifest["selection"]["cases"]
            if row["source_group"] == "sample"
        }
        alternate_sample = {
            row["id"] for row in alternate_manifest["selection"]["cases"]
            if row["source_group"] == "sample"
        }
        assert len(original_known) == len(alternate_known) == 16
        assert original_known == alternate_known
        assert len(original_sample) == len(alternate_sample) == 8
        assert original_sample.isdisjoint(alternate_sample)

        alternate_judgments = temp / "alternate-judgments.json"
        alternate_judgments.write_bytes(stable_bytes(judgments(alternate_packet, alternate_manifest)))
        evaluate(
            alternate_packet_path, alternate_manifest_path, alternate_judgments,
            prompt_path=alternate_prompt,
        )
        reject(
            lambda: evaluate(alternate_packet_path, alternate_manifest_path,
                             alternate_judgments),
            "Alternate prompt binding accepted the default prompt",
        )
        reject(
            lambda: evaluate(
                alternate_packet_path, alternate_manifest_path, alternate_judgments,
                prompt_path=temp / "missing-prompt.md",
            ),
            "Missing prompt was accepted",
        )
        reject(lambda: prepare(temp / "negative", sample_offset=-1),
               "Negative sample offset was accepted")
        reject(lambda: prepare(temp / "oversized", sample_offset=1_000_000),
               "Unavailable sample offset was accepted")

        source_examples = json.loads((ARTIFACTS / "examples.json").read_text())
        custom_examples = deepcopy([source_examples[0], source_examples[3]])
        custom_examples[0]["duplicate"] = False
        for example in custom_examples:
            example["cohort"] = "fresh"
            example["label_authority"] = "external editorial review"
            example["expected_treatment"] = "retain both passages"
        custom_examples_path = temp / "custom-examples.json"
        custom_examples_path.write_bytes(stable_bytes(custom_examples))
        custom_dir = temp / "custom"
        custom_packet_path, custom_manifest_path = prepare(
            custom_dir, examples_path=custom_examples_path
        )
        custom_packet = json.loads(custom_packet_path.read_text())
        custom_manifest = json.loads(custom_manifest_path.read_text())
        assert len(custom_packet["cases"]) == 2
        assert len(custom_manifest["selection"]["cases"]) == 2
        assert {row["source_group"] for row in custom_manifest["selection"]["cases"]} == {"known"}
        assert custom_manifest["selection"]["method"] == "provided_labeled_examples"
        reject(
            lambda: prepare(temp / "custom-offset", examples_path=custom_examples_path,
                            sample_offset=1),
            "Explicit examples accepted a nonzero sample offset",
        )

        custom_judgments_path = temp / "custom-judgments.json"
        custom_judgments_path.write_bytes(stable_bytes(
            judgments(custom_packet, custom_manifest, custom_examples_path)
        ))
        custom_metrics = evaluate(
            custom_packet_path, custom_manifest_path, custom_judgments_path,
            examples_path=custom_examples_path,
        )
        assert custom_metrics["known"]["counts"] == {"TP": 0, "FP": 0, "FN": 0, "TN": 2}
        assert len(custom_metrics["known"]["outcomes"]) == 2
        assert custom_metrics["new_sample"] == {
            "classification_counts": {
                "ACTIONABLE_DUPLICATE": 0,
                "NECESSARY_REPETITION": 0,
                "RELATED_BUT_DISTINCT": 0,
            },
            "abstentions": 0,
        }
        reject(
            lambda: evaluate(custom_packet_path, custom_manifest_path,
                             custom_judgments_path),
            "Custom packet accepted the default labels",
        )
        changed_examples = deepcopy(custom_examples)
        changed_examples[0]["expected_treatment"] = "consolidate"
        changed_examples_path = temp / "changed-examples.json"
        changed_examples_path.write_bytes(stable_bytes(changed_examples))
        reject(
            lambda: evaluate(
                custom_packet_path, custom_manifest_path, custom_judgments_path,
                examples_path=changed_examples_path,
            ),
            "Treatment metadata hash mismatch was accepted",
        )

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
    refinement = ARTIFACTS / "judge-v2"
    for prefix, prompt in (("control", ARTIFACTS / "judge-prompt.md"),
                           ("judge", refinement / "prompt.md"),
                           ("v3", refinement / "prompt-v3.md")):
        evaluated = evaluate(refinement / "judge-packet.json",
                             refinement / f"{prefix}-manifest.json",
                             refinement / f"{prefix}-decisions.json", prompt_path=prompt)
        assert evaluated == json.loads((refinement / f"{prefix}-metrics.json").read_text())
    print("PASS: deterministic preparation, strict bindings, judgment validation, and abstention metrics")


if __name__ == "__main__":
    check()
