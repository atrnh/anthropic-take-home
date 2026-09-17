"""Verify that the archived pilot inventory matches its relocation manifest."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PILOT = ROOT / "docs/3-check/pilot"
MANIFEST = PILOT / "relocation-manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check() -> None:
    records = json.loads(MANIFEST.read_text())["files"]
    archived_paths = [record["archived_path"] for record in records]
    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in PILOT.rglob("*")
        if path.is_file() and path != MANIFEST
    }
    assert len(archived_paths) == len(set(archived_paths))
    assert set(archived_paths) == actual_paths

    immutable = 0
    for record in records:
        path = ROOT / record["archived_path"]
        assert sha256(path) == record["archived_sha256"], path
        is_prompt = path.suffix == ".md" and (
            path.name == "judge-prompt.md" or path.name.startswith("prompt")
        )
        if path.suffix == ".json" or is_prompt:
            assert record["original_sha256"] == record["archived_sha256"], path
            immutable += 1

    print(
        f"PASS: {len(records)} archived pilot files verified; "
        f"{immutable} JSON and prompt artifacts remain byte-identical"
    )


if __name__ == "__main__":
    check()
