# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["scikit-learn==1.7.2"]
# ///
"""Prepare and evaluate a deterministic, file-based editorial judge pilot."""

import argparse
from collections import Counter
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import re

from bakeoff import case_pairs, ranked_pairs, similarities, top_k
from duplicates import Passage, evaluate as validate_examples, load_corpus


SCHEMA_VERSION = 1
CLASSIFICATIONS = {
    "ACTIONABLE_DUPLICATE",
    "NECESSARY_REPETITION",
    "RELATED_BUT_DISTINCT",
}
CASE_FIELDS = {
    "id", "classification", "needs_review", "shared_explanation", "unique_left",
    "unique_right", "rationale", "suggested_consolidation", "evidence",
}
SIDE_FIELDS = {
    "path", "start", "end", "text", "heading_context", "context_start",
    "context_end", "context_text",
}
MANIFEST_CASE_FIELDS = {
    "id", "source_group", "example_id", "left", "right", "score", "global_rank",
    "queue_rank", "left_rank", "right_rank", "stratum", "selection_sha256",
}


def stable_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def locator(span: Passage | dict) -> dict:
    if isinstance(span, Passage):
        return {"path": span.path, "start": span.start, "end": span.end}
    return {name: span[name] for name in ("path", "start", "end")}


def canonical_pair(left: Passage | dict, right: Passage | dict) -> list[dict]:
    return sorted((locator(left), locator(right)), key=lambda row: (row["path"], row["start"], row["end"]))


def pair_hash(left: Passage | dict, right: Passage | dict) -> str:
    return sha256(json.dumps(canonical_pair(left, right), sort_keys=True,
                             separators=(",", ":")).encode())


def packet_order(case_id: str) -> str:
    return sha256(f"packet-order:{case_id}".encode())


def headings_before(lines: list[str], start: int) -> list[str]:
    ancestry: list[tuple[int, str]] = []
    fence: tuple[str, int] | None = None
    for line in lines[:start - 1]:
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
            continue
        if fence is not None:
            continue
        match = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        level, title = len(match[1]), match[2]
        ancestry = [heading for heading in ancestry if heading[0] < level]
        ancestry.append((level, title))
    return [title for _, title in ancestry]


def packet_side(root: Path, span: Passage | dict) -> dict:
    location = locator(span)
    lines = (root / location["path"]).read_text().splitlines()
    start, end = location["start"], location["end"]
    context_start, context_end = max(1, start - 8), min(len(lines), end + 8)
    return {
        **location,
        "text": "\n".join(lines[start - 1:end]),
        "heading_context": headings_before(lines, start),
        "context_start": context_start,
        "context_end": context_end,
        "context_text": "\n".join(lines[context_start - 1:context_end]),
    }


def strata(rows: list[tuple[int, int]], count: int = 4) -> list[list[tuple[int, int]]]:
    size, extra = divmod(len(rows), count)
    result, offset = [], 0
    for number in range(count):
        end = offset + size + (number < extra)
        result.append(rows[offset:end])
        offset = end
    return result


def prepare(output_dir: Path, project: Path | None = None, *,
            prompt_path: Path | None = None, sample_offset: int = 0) -> tuple[Path, Path]:
    project = project or Path(__file__).resolve().parents[1]
    if type(sample_offset) is not int or sample_offset < 0:
        raise ValueError("sample_offset must be a nonnegative integer")
    corpus = project / "corpus"
    examples_path = project / "docs/3-check/examples.json"
    results_path = project / "docs/3-check/results.json"
    prompt_path = prompt_path or project / "docs/3-check/judge-prompt.md"
    snapshot, items = load_corpus(corpus, 10, include_lists=True)
    examples_raw = examples_path.read_bytes()
    examples = json.loads(examples_raw)
    validate_examples(examples, [], corpus)
    results_raw = results_path.read_bytes()
    reviewed = {pair_hash(row["left"], row["right"])
                for row in json.loads(results_raw)["findings"]}

    matrices = similarities(items)
    pairs, ranks = ranked_pairs(matrices["tfidf"])
    candidates = top_k(pairs, ranks, 10)
    frozen = set().union(*case_pairs(examples, items).values())
    queue = [pair for pair in pairs
             if pair in candidates and pair not in frozen
             and pair_hash(items[pair[0]], items[pair[1]]) not in reviewed]
    groups = strata(queue)
    selected = []
    for number, group in enumerate(groups, 1):
        chosen = sorted(group, key=lambda pair: pair_hash(items[pair[0]], items[pair[1]]))[
            sample_offset:sample_offset + 2
        ]
        if len(chosen) != 2:
            raise ValueError(f"Stratum {number} cannot supply two candidates at offset {sample_offset}")
        selected.extend((pair, number) for pair in chosen)
    if len(examples) != 16 or len(selected) != 8:
        raise ValueError("Pilot requires 16 frozen examples and 8 sampled candidates")

    cases: list[dict] = []
    manifest_cases: list[dict] = []
    for example in examples:
        left, right = example["left"], example["right"]
        case_id = pair_hash(left, right)
        cases.append({"id": case_id, "left": packet_side(corpus, left),
                      "right": packet_side(corpus, right)})
        manifest_cases.append({
            "id": case_id, "source_group": "known", "example_id": example["id"],
            "left": locator(left), "right": locator(right), "score": None,
            "global_rank": None, "queue_rank": None, "left_rank": None,
            "right_rank": None, "stratum": None, "selection_sha256": None,
        })
    queue_rank = {pair: rank for rank, pair in enumerate(queue, 1)}
    global_rank = {pair: rank for rank, pair in enumerate(pairs, 1)}
    for (a, b), stratum in selected:
        left, right = items[a], items[b]
        case_id = pair_hash(left, right)
        cases.append({"id": case_id, "left": packet_side(corpus, left),
                      "right": packet_side(corpus, right)})
        manifest_cases.append({
            "id": case_id, "source_group": "sample", "example_id": None,
            "left": locator(left), "right": locator(right),
            "score": float(matrices["tfidf"][a, b]),
            "global_rank": global_rank[(a, b)], "queue_rank": queue_rank[(a, b)],
            "left_rank": ranks[(a, b)], "right_rank": ranks[(b, a)],
            "stratum": stratum, "selection_sha256": pair_hash(left, right),
        })

    cases.sort(key=lambda row: packet_order(row["id"]))
    manifest_cases.sort(key=lambda row: row["id"])
    packet = {"schema_version": SCHEMA_VERSION, "cases": cases}
    packet_raw = stable_bytes(packet)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "snapshot": snapshot,
        "packet_sha256": sha256(packet_raw),
        "examples_sha256": sha256(examples_raw),
        "results_sha256": sha256(results_raw),
        "prompt_sha256": sha256(prompt_path.read_bytes()),
        "selection": {
            "method": "expanded_tfidf_top_10_hash_stratified",
            "min_words": 10,
            "include_unordered_lists": True,
            "top_k": 10,
            "candidate_pairs": len(candidates),
            "excluded_frozen_pairs": len(candidates & frozen),
            "excluded_reviewed_pairs": sum(
                pair_hash(items[a], items[b]) in reviewed
                for a, b in candidates if (a, b) not in frozen
            ),
            "remaining_pairs": len(queue),
            "strata": [
                {"number": number, "rank_start": sum(map(len, groups[:number - 1])) + 1,
                 "rank_end": sum(map(len, groups[:number])), "size": len(group)}
                for number, group in enumerate(groups, 1)
            ],
            "cases": manifest_cases,
        },
        "runtime": {
            "python": platform.python_version(),
            "packages": {name: version(name) for name in ("scikit-learn", "numpy", "scipy")},
        },
    }
    if sample_offset:
        manifest["selection"]["sample_offset"] = sample_offset
    output_dir.mkdir(parents=True, exist_ok=True)
    packet_path = output_dir / "judge-packet.json"
    manifest_path = output_dir / "judge-manifest.json"
    packet_path.write_bytes(packet_raw)
    manifest_path.write_bytes(stable_bytes(manifest))
    return packet_path, manifest_path


def _object(value: object, fields: set[str], name: str) -> dict:
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f"Invalid {name} fields")
    return value


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def nonnegative_int(value: str) -> int:
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return number


def _load_bound_inputs(packet_path: Path, manifest_path: Path, project: Path, *,
                       prompt_path: Path | None = None) -> tuple[dict, dict, dict[str, dict], dict[str, str]]:
    packet_raw = packet_path.read_bytes()
    manifest_raw = manifest_path.read_bytes()
    packet = json.loads(packet_raw)
    manifest = json.loads(manifest_raw)
    if not isinstance(manifest, dict) or manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported manifest schema")
    if manifest.get("packet_sha256") != sha256(packet_raw):
        raise ValueError("Packet hash mismatch")
    corpus = project / "corpus"
    snapshot, _ = load_corpus(corpus, 10, include_lists=True)
    if manifest.get("snapshot") != snapshot:
        raise ValueError("Snapshot binding mismatch")
    examples_path = project / "docs/3-check/examples.json"
    examples_raw = examples_path.read_bytes()
    examples = json.loads(examples_raw)
    validate_examples(examples, [], corpus)
    if manifest.get("examples_sha256") != sha256(examples_raw):
        raise ValueError("Examples hash mismatch")
    results_path = project / "docs/3-check/results.json"
    if manifest.get("results_sha256") != sha256(results_path.read_bytes()):
        raise ValueError("Baseline results hash mismatch")
    prompt_path = prompt_path or project / "docs/3-check/judge-prompt.md"
    if manifest.get("prompt_sha256") != sha256(prompt_path.read_bytes()):
        raise ValueError("Prompt hash mismatch")
    corpus_manifest = json.loads((corpus / "manifest.json").read_text())
    allowed_paths = {row["path"] for row in corpus_manifest["pages"]}

    if not isinstance(packet, dict) or set(packet) != {"schema_version", "cases"} \
            or packet["schema_version"] != SCHEMA_VERSION or not isinstance(packet["cases"], list):
        raise ValueError("Invalid packet schema")
    selection = manifest.get("selection")
    if not isinstance(selection, dict) or not isinstance(selection.get("cases"), list):
        raise ValueError("Invalid manifest selection")
    records = selection["cases"]
    by_id = {row.get("id"): row for row in records if isinstance(row, dict)}
    if (len(by_id) != len(records) or len(packet["cases"]) != len(records)
            or set(by_id) != {row.get("id") for row in packet["cases"] if isinstance(row, dict)}):
        raise ValueError("Packet and manifest case IDs differ")
    if [row.get("id") for row in packet["cases"]] != sorted(by_id, key=packet_order):
        raise ValueError("Packet cases are not hash ordered")
    known_by_id = {pair_hash(row["left"], row["right"]): row for row in examples}
    if len(known_by_id) != len(examples):
        raise ValueError("Frozen examples contain duplicate span pairs")
    known_count = sample_count = 0
    for case_id, record in by_id.items():
        _object(record, MANIFEST_CASE_FIELDS, "manifest case")
        if case_id in known_by_id:
            example = known_by_id[case_id]
            if (record["source_group"] != "known" or record["example_id"] != example["id"]
                    or record["left"] != locator(example["left"])
                    or record["right"] != locator(example["right"])):
                raise ValueError("Known manifest case does not match its frozen example")
            known_count += 1
        elif record["source_group"] != "sample" or record["example_id"] is not None:
            raise ValueError("Sample manifest case has invalid provenance")
        else:
            sample_count += 1
    if known_count != 16 or sample_count != 8:
        raise ValueError("Manifest requires 16 known and 8 sample cases")
    for case in packet["cases"]:
        _object(case, {"id", "left", "right"}, "packet case")
        _text(case["id"], "case id")
        record = by_id[case["id"]]
        if record.get("source_group") not in {"known", "sample"}:
            raise ValueError("Invalid source group")
        for side_name in ("left", "right"):
            side = _object(case[side_name], SIDE_FIELDS, f"packet {side_name}")
            path = side["path"]
            if not isinstance(path, str) or path not in allowed_paths:
                raise ValueError(f"Unsafe or unknown corpus path: {path}")
            lines = (corpus / path).read_text().splitlines()
            start, end = side["start"], side["end"]
            context_start, context_end = side["context_start"], side["context_end"]
            if any(type(number) is not int for number in (start, end, context_start, context_end)):
                raise ValueError("Line ranges must be integers")
            if not 1 <= start <= end <= len(lines):
                raise ValueError("Invalid target line range")
            expected = packet_side(corpus, side)
            if side != expected:
                raise ValueError(f"Packet {side_name} does not match corpus")
            if record.get(side_name) != locator(side):
                raise ValueError("Manifest span does not match packet")
        if case["id"] != pair_hash(case["left"], case["right"]):
            raise ValueError("Case ID does not match its spans")
    return packet, manifest, by_id, {
        "packet_sha256": sha256(packet_raw),
        "manifest_sha256": sha256(manifest_raw),
    }


def evaluate(packet_path: Path, manifest_path: Path, judgments_path: Path,
             project: Path | None = None, *, prompt_path: Path | None = None) -> dict:
    project = project or Path(__file__).resolve().parents[1]
    packet, _, records, provenance = _load_bound_inputs(
        packet_path, manifest_path, project, prompt_path=prompt_path
    )
    judgments_raw = judgments_path.read_bytes()
    judgments = json.loads(judgments_raw)
    if not isinstance(judgments, dict) or set(judgments) != {"cases"} or not isinstance(judgments["cases"], list):
        raise ValueError("Invalid judgments schema")
    expected_ids = {case["id"] for case in packet["cases"]}
    rows = judgments["cases"]
    ids = [row.get("id") for row in rows if isinstance(row, dict)]
    if len(ids) != len(rows) or len(ids) != len(set(ids)) or set(ids) != expected_ids:
        raise ValueError("Judgments must contain every packet ID exactly once")
    targets = {case["id"]: case for case in packet["cases"]}
    for row in rows:
        _object(row, CASE_FIELDS, "judgment")
        _text(row["id"], "judgment id")
        if (not isinstance(row["classification"], str)
                or row["classification"] not in CLASSIFICATIONS
                or type(row["needs_review"]) is not bool):
            raise ValueError("Invalid classification or needs_review")
        for name in ("shared_explanation", "unique_left", "unique_right", "rationale"):
            _text(row[name], name)
        consolidation = row["suggested_consolidation"]
        if row["classification"] == "ACTIONABLE_DUPLICATE":
            _text(consolidation, "suggested_consolidation")
        elif consolidation is not None:
            raise ValueError("Only actionable duplicates may suggest consolidation")
        evidence = _object(row["evidence"], {"left", "right"}, "evidence")
        for side in ("left", "right"):
            quote = _text(evidence[side], f"{side} evidence")
            if quote not in targets[row["id"]][side]["text"]:
                raise ValueError(f"{side} evidence is not a literal target substring")

    examples = {row["id"]: row for row in json.loads((project / "docs/3-check/examples.json").read_text())}
    known = Counter(TP=0, FP=0, FN=0, TN=0)
    abstentions = 0
    outcomes, sample = [], Counter({name: 0 for name in sorted(CLASSIFICATIONS)})
    sample_abstentions = 0
    for row in rows:
        record = records[row["id"]]
        if record["source_group"] == "sample":
            sample[row["classification"]] += 1
            sample_abstentions += row["needs_review"]
            continue
        example = examples[record["example_id"]]
        if row["needs_review"]:
            outcome = "ABSTAIN"
            abstentions += 1
        else:
            predicted = row["classification"] == "ACTIONABLE_DUPLICATE"
            outcome = ("T" if predicted == example["duplicate"] else "F") + ("P" if predicted else "N")
            known[outcome] += 1
        outcomes.append({"example_id": example["id"], "classification": row["classification"],
                         "needs_review": row["needs_review"], "outcome": outcome})
    outcomes.sort(key=lambda row: row["example_id"])

    def rate(numerator: int, denominator: int) -> dict:
        return {"numerator": numerator, "denominator": denominator,
                "value": numerator / denominator if denominator else None}

    return {
        "schema_version": SCHEMA_VERSION,
        "provenance": {**provenance, "judgments_sha256": sha256(judgments_raw)},
        "scope": {
            "known": "direct editorial judge evaluation on frozen full-span examples",
            "new_sample": "classification distribution only; no independent labels",
            "retrieval_end_to_end": False,
        },
        "known": {
            "counts": dict(known), "abstentions": abstentions,
            "precision": rate(known["TP"], known["TP"] + known["FP"]),
            "conditional_recall": rate(known["TP"], known["TP"] + known["FN"]),
            "recall": rate(known["TP"], sum(row["duplicate"] for row in examples.values())),
            "coverage": rate(len(outcomes) - abstentions, len(outcomes)),
            "outcomes": outcomes,
        },
        "new_sample": {"classification_counts": dict(sample), "abstentions": sample_abstentions},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument("--output-dir", required=True, type=Path)
    prepare_parser.add_argument("--prompt", type=Path)
    prepare_parser.add_argument("--sample-offset", type=nonnegative_int, default=0)
    evaluate_parser = commands.add_parser("evaluate")
    evaluate_parser.add_argument("--packet", required=True, type=Path)
    evaluate_parser.add_argument("--manifest", required=True, type=Path)
    evaluate_parser.add_argument("--judgments", required=True, type=Path)
    evaluate_parser.add_argument("--prompt", type=Path)
    args = parser.parse_args()
    if args.command == "prepare":
        packet, manifest = prepare(
            args.output_dir, prompt_path=args.prompt, sample_offset=args.sample_offset
        )
        print(json.dumps({"packet": str(packet), "manifest": str(manifest)}, sort_keys=True))
    else:
        print(json.dumps(evaluate(
            args.packet, args.manifest, args.judgments, prompt_path=args.prompt
        ), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
