# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["scikit-learn==1.7.2"]
# ///
"""Check that numbered prose reaches the queue and negative labels cannot hide it."""

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from candidates import build


def check() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        prose = "Configure your service using the supported authentication settings before connecting external clients to private resources."
        sources = {"index.md": f"1. {prose}\n", "guide.md": prose + "\n",
                   "hidden.md": f"<Steps>\n{prose}\n</Steps>\n"}
        pages = []
        for path, text in sources.items():
            (root / path).write_text(text)
            pages.append({"path": path, "sha256": hashlib.sha256(text.encode()).hexdigest()})
        (root / "manifest.json").write_text(json.dumps({
            "fetched_at": "fixture", "page_count": len(pages), "pages": pages,
        }))
        queue = build(root, 1)
        assert queue["passage_count"] == 2 and queue["candidate_count"] == 1
        pair = queue["candidates"][0]
        assert {queue["passages"][pair[side]]["path"] for side in ("left", "right")} == {"index.md", "guide.md"}
        labels = root / "labels.json"
        labels.write_text(json.dumps([{
            "id": "keep-local-prerequisite", "split": "evaluation", "duplicate": False,
            "left": {"path": "index.md", "start": 1, "end": 1},
            "right": {"path": "guide.md", "start": 1, "end": 1},
        }]))
        annotated = build(root, 1, (labels,))
        assert annotated["candidates"] == queue["candidates"]
        assert annotated["coverage"][0]["summary"]["negative_cases_retrieved"] == 1
        try:
            build(root, 0)
        except ValueError:
            pass
        else:
            raise AssertionError("Zero candidate limit was accepted")
    print("PASS: numbered prose, procedure exclusion, complete queue despite negative label, invalid limit")


if __name__ == "__main__":
    check()
