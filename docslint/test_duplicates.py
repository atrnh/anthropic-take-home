"""Run with `uv run python docslint/test_duplicates.py`. No test dependencies."""

import hashlib
import json
from pathlib import Path
import tempfile

from duplicates import Passage, evaluate, find_duplicates, load_corpus, passages, words


def check() -> None:
    prose = "Shared explanations should have one maintained source so editors can update them consistently."
    source = f"""# Title
> {prose}
export const Beta = () => <Info>{prose}</Info>;

<Columns>
  <Card title="Navigation">
    {prose}
  </Card>
</Columns>

```python
{prose}
````
~~~text
{prose}
~~~
1. {prose}

   {prose}
* {prose}

<Steps>
  <Step title="Action">
    {prose}
  </Step>
</Steps>
| {prose} |
<!--
{prose}
-->
## Explanation
{prose}
Editors can link to that explanation from their task pages.

<Note>
  {prose}
</Note>
"""
    extracted = passages("example.md", source, 10)
    assert len(extracted) == 2, extracted
    for item in extracted:
        assert item.text == "\n".join(source.splitlines()[item.start - 1:item.end])
    assert extracted[0].text.endswith("task pages.")
    assert words("**Read** [the guide](/first) &amp; `verify`.") == ["read", "the", "guide", "verify"]
    assert words("**Read** [the guide](/second) &amp; `verify`.") == ["read", "the", "guide", "verify"]

    items = [Passage("a.md", 1, 1, prose),
             Passage("b.md", 1, 1, prose + " Keep the necessary context on each page."),
             Passage("c.md", 1, 1, "An entirely unrelated discussion about flowers and growing vegetables.")]
    findings = find_duplicates(items, 1)
    assert len(findings) == 1 and findings[0]["similarity"] == 1
    assert find_duplicates(items, 1) == findings
    assert not find_duplicates([Passage("short.md", 1, 1, "one")], 1)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for item in items:
            (root / item.path).write_text(item.text)
        manifest = {
            "fetched_at": "fixture", "page_count": 3,
            "pages": [{"path": item.path, "sha256": hashlib.sha256(item.text.encode()).hexdigest()}
                      for item in items],
        }
        (root / "manifest.json").write_text(json.dumps(manifest))
        snapshot, loaded = load_corpus(root, 3)
        assert snapshot["page_count"] == 3 and loaded == items

        def span(path: str) -> dict:
            return {"path": path, "start": 1, "end": 1}

        evaluation = evaluate([
            {"id": "reversed", "split": "evaluation", "left": span("b.md"),
             "right": span("a.md"), "duplicate": True},
            {"id": "unrelated", "split": "evaluation", "left": span("a.md"),
             "right": span("c.md"), "duplicate": False},
            {"id": "legitimate", "split": "development", "left": span("a.md"),
             "right": span("b.md"), "duplicate": False},
            {"id": "paraphrase", "split": "development", "left": span("a.md"),
             "right": span("c.md"), "duplicate": True},
        ], findings, root)
        assert evaluation["counts"]["evaluation"] == {"TP": 1, "FP": 0, "FN": 0, "TN": 1}
        assert evaluation["counts"]["development"] == {"TP": 0, "FP": 1, "FN": 1, "TN": 0}

        (root / "a.md").write_text("changed")
        try:
            load_corpus(root, 3)
        except ValueError as error:
            assert "hash mismatch" in str(error)
        else:
            raise AssertionError("Changed source accepted against the pinned manifest")
        manifest["pages"][0]["path"] = "../outside.md"
        (root / "manifest.json").write_text(json.dumps(manifest))
        try:
            load_corpus(root, 3)
        except ValueError as error:
            assert "Unsafe" in str(error)
        else:
            raise AssertionError("Manifest path escaped the corpus")
    print("PASS: extraction, source ranges, matching, evaluation, and snapshot validation")


def check_artifacts() -> None:
    root = Path(__file__).resolve().parents[1]
    artifacts = root / "docs/3-check"
    expected = json.loads((artifacts / "results.json").read_text())
    settings = expected["settings"]
    snapshot, items = load_corpus(root / "corpus", settings["min_words"])
    findings = find_duplicates(items, settings["threshold"])
    assert expected == {
        "snapshot": snapshot,
        "settings": {**settings, "shingle_words": 3},
        "passage_count": len(items),
        "finding_count": len(findings),
        "findings": findings,
        "evaluation": evaluate(json.loads((artifacts / "examples.json").read_text()),
                               findings, root / "corpus"),
    }, "Committed results differ from the current code, corpus, or labels"
    reviews = json.loads((artifacts / "reviews.json").read_text())
    assert len(reviews) == len(findings)
    assert {row["id"] for row in reviews} == {row["id"] for row in findings}
    assert all(type(row["actionable"]) is bool and row["reason"] for row in reviews)
    actionable = sum(row["actionable"] for row in reviews)
    print(f"PASS: reproducible snapshot results; {actionable}/{len(findings)} findings labeled actionable")
    print(json.dumps(expected["evaluation"]["counts"], sort_keys=True))


if __name__ == "__main__":
    check()
    check_artifacts()
