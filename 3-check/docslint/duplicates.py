"""Flag repeated prose in a pinned Markdown corpus. Findings require editorial review."""

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import html
from itertools import combinations
import json
from pathlib import Path
import re


@dataclass(frozen=True)
class Passage:
    path: str
    start: int
    end: int
    text: str


def words(text: str) -> list[str]:
    text = re.sub(r"!?\[([^\]]+)\]\([^\n]*?\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.findall(r"\w+", html.unescape(text).casefold())


def passages(path: str, source: str, min_words: int, *, include_lists: bool = False,
             include_ordered_lists: bool = False) -> list[Passage]:
    """Read prose paragraphs in this snapshot's Markdown/MDX, retaining source lines."""
    result = []
    block: list[tuple[int, str]] = []
    fence = ""
    hidden = ""
    comment = False
    in_list = False
    capture_item = False
    ordered_item = False
    list_indent = 0

    def flush() -> None:
        if block:
            text = "\n".join(line for _, line in block)
            if len(words(text)) >= min_words:
                result.append(Passage(path, block[0][0], block[-1][0], text))
            block.clear()

    for number, line in enumerate(source.splitlines(), 1):
        stripped = line.strip()
        if fence:
            if re.fullmatch(re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", stripped):
                fence = ""
            continue
        if hidden:
            if f"</{hidden}>" in line:
                hidden = ""
            continue
        if comment:
            if "-->" in line:
                comment = False
            continue
        indent = len(line) - len(line.lstrip())
        if ((include_lists or include_ordered_lists) and indent <= list_indent
                and (stripped.startswith("<") or re.match(r"(`{3,}|~{3,})", stripped))):
            in_list = capture_item = False
        match = re.match(r"(`{3,}|~{3,})", stripped)
        if match:
            flush()
            fence = match[1]
            continue
        if "<!--" in line:
            flush()
            comment = "-->" not in line
            continue
        match = re.match(r"<(Steps|Card|Columns|CodeGroup)(?:\s|>)", stripped)
        if match:
            flush()
            if f"</{match[1]}>" not in line:
                hidden = match[1]
            continue
        marker = re.match(r"([-+*]|\d+[.)])\s", stripped)
        if marker:
            unordered = marker[1] in ("-", "+", "*")
            if not (include_ordered_lists and in_list and ordered_item
                    and not unordered and indent == list_indent):
                flush()
            in_list = True
            list_indent = indent
            ordered_item = not unordered
            capture_item = ((include_lists and unordered)
                            or (include_ordered_lists and not unordered))
            if capture_item:
                block.append((number, line))
            continue
        if in_list and line[:1].isspace():
            if not capture_item:
                continue
        elif stripped:
            in_list = False
            capture_item = False
        if (not stripped or stripped.startswith(("#", ">", "|", "<"))
                or re.match(r"(?:import|export)\s", stripped)
                or re.fullmatch(r"[-*_]{3,}", stripped)
                or re.match(r"\[[^]]+\]:", stripped)):
            flush()
            continue
        block.append((number, line))
    flush()
    return result


def load_corpus(root: Path, min_words: int, *, include_lists: bool = False,
                include_ordered_lists: bool = False) -> tuple[dict, list[Passage]]:
    manifest_bytes = (root / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest["page_count"] != len(manifest["pages"]):
        raise ValueError("Manifest page count does not match its entries")
    seen = set()
    result = []
    for page in sorted(manifest["pages"], key=lambda row: row["path"]):
        path = page["path"]
        target = (root / path).resolve()
        if not target.is_relative_to(root.resolve()) or path in seen:
            raise ValueError(f"Unsafe or duplicate manifest path: {path}")
        seen.add(path)
        raw = target.read_bytes()
        if hashlib.sha256(raw).hexdigest() != page["sha256"]:
            raise ValueError(f"Snapshot hash mismatch: {path}")
        result.extend(passages(path, raw.decode("utf-8"), min_words,
                               include_lists=include_lists,
                               include_ordered_lists=include_ordered_lists))
    return {
        "fetched_at": manifest["fetched_at"],
        "page_count": len(seen),
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
    }, result


def find_duplicates(items: list[Passage], threshold: float) -> list[dict]:
    shingles = []
    for item in items:
        tokens = words(item.text)
        shingles.append(set(zip(tokens, tokens[1:], tokens[2:])))
    findings = []
    # ponytail: all-pairs comparison suits 54 pages; use a shingle index for larger corpora.
    for left, right in combinations(range(len(items)), 2):
        a, b = shingles[left], shingles[right]
        if not a or not b:
            continue
        score = len(a & b) / min(len(a), len(b))
        if score < threshold:
            continue
        pair = {"left": asdict(items[left]), "right": asdict(items[right])}
        identity = json.dumps(pair, sort_keys=True).encode()
        findings.append({
            "id": hashlib.sha256(identity).hexdigest()[:12],
            "similarity": round(score, 4),
            **pair,
        })
    return sorted(findings, key=lambda row: (-row["similarity"], row["id"]))


def evaluate(examples: list[dict], findings: list[dict], root: Path) -> dict:
    """Score labeled ranges; a finding must fit entirely inside both ranges."""
    counts = {split: Counter(TP=0, FP=0, FN=0, TN=0)
              for split in ("development", "evaluation")}
    cases = []
    seen = set()
    for example in examples:
        if (example["id"] in seen or example["split"] not in counts
                or type(example["duplicate"]) is not bool):
            raise ValueError(f"Invalid example: {example['id']}")
        seen.add(example["id"])
        for side in ("left", "right"):
            span = example[side]
            target = (root / span["path"]).resolve()
            if not target.is_relative_to(root.resolve()):
                raise ValueError(f"Unsafe example path: {span['path']}")
            if not 1 <= span["start"] <= span["end"] <= len(target.read_text().splitlines()):
                raise ValueError(f"Invalid example range: {span}")

        def contains(span: dict, passage: dict) -> bool:
            return (span["path"] == passage["path"]
                    and span["start"] <= passage["start"]
                    and passage["end"] <= span["end"])

        matched = [finding["id"] for finding in findings if any(
            contains(example["left"], finding[a]) and contains(example["right"], finding[b])
            for a, b in (("left", "right"), ("right", "left"))
        )]
        outcome = ("T" if bool(matched) == example["duplicate"] else "F") + (
            "P" if matched else "N")
        counts[example["split"]][outcome] += 1
        cases.append({"id": example["id"], "split": example["split"],
                      "outcome": outcome, "finding_ids": matched})
    return {"counts": counts, "cases": cases}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path)
    parser.add_argument("--min-words", type=int, default=15)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--examples", type=Path)
    args = parser.parse_args()
    if args.min_words < 3 or not 0 < args.threshold <= 1:
        parser.error("min-words must be >= 3 and threshold must be in (0, 1]")
    try:
        snapshot, items = load_corpus(args.corpus, args.min_words)
        findings = find_duplicates(items, args.threshold)
        result = {
            "snapshot": snapshot,
            "settings": {"min_words": args.min_words, "threshold": args.threshold,
                         "shingle_words": 3},
            "passage_count": len(items),
            "finding_count": len(findings),
            "findings": findings,
        }
        if args.examples:
            result["evaluation"] = evaluate(json.loads(args.examples.read_text()), findings, args.corpus)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
