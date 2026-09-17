"""Write a self-contained, local-file-friendly duplicate-review report."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


_TEMPLATE = Path(__file__).with_name("report.html")


def _script_json(value: object) -> str:
    """Serialize embedded data without allowing corpus text to end the script."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def _passage(value: dict[str, Any]) -> dict[str, Any]:
    """Keep only report fields, including an optional, precomputed source link."""
    return {
        key: value.get(key)
        for key in (
            "path", "start", "end", "text", "heading_context", "context_start",
            "context_end", "context_text", "source_href",
        )
    }


def write_report(
    queue: dict,
    output: Path,
    advice: dict[str, dict] | None = None,
) -> None:
    """Write a standalone HTML review queue from a candidate export.

    ``advice`` is displayed only for matching candidate IDs. Its content is not
    interpreted, filtered, or used to change candidate order.
    """
    passages = queue.get("passages", [])
    rows = []
    for candidate in queue.get("candidates", []):
        row = {
            "id": candidate.get("id"),
            "score": candidate.get("score"),
            "ranks": candidate.get("ranks") or {
                key: candidate[key]
                for key in ("left_rank", "right_rank")
                if key in candidate
            },
            "left": candidate["left"],
            "right": candidate["right"],
        }
        if advice and candidate.get("id") in advice:
            row["advice"] = {
                key: advice[candidate["id"]].get(key)
                for key in (
                    "classification", "needs_review", "rationale",
                    "suggested_consolidation",
                )
                if key in advice[candidate["id"]]
            }
        rows.append(row)

    data = {
        "candidate_count": len(rows),
        "passage_count": queue.get("passage_count", len(passages)),
        "passages": [_passage(passage) for passage in passages],
        "items": rows,
    }
    template = _TEMPLATE.read_text(encoding="utf-8")
    if template.count("__REPORT_DATA__") != 1:
        raise ValueError("report.html must contain exactly one __REPORT_DATA__ placeholder")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template.replace("__REPORT_DATA__", _script_json(data)), encoding="utf-8")
