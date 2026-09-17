"""Run with `uv run python 3-check/docslint/test_duplicates.py`. No test dependencies."""

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
<CodeGroup>
```text
{prose}
```
</CodeGroup>
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
    expanded = passages("example.md", source, 10, include_lists=True)
    assert len(expanded) == 3 and expanded[0].text == f"* {prose}", expanded
    ordered = passages("example.md", source, 10, include_ordered_lists=True)
    assert len(ordered) == 4 and ordered[2:] == extracted, ordered
    assert ordered[0].text == f"1. {prose}" and ordered[1].text == f"   {prose}", ordered
    list_source = f"""- {prose}
  Wrapped detail remains part of this item.
+ Too short
1. {prose}
   Ordered continuation stays excluded.

{prose}"""
    expanded = passages("lists.md", list_source, 10, include_lists=True)
    assert [(p.start, p.end) for p in expanded] == [(1, 2), (7, 7)], expanded
    assert passages("lists.md", list_source, 10) == [expanded[1]]
    for item in expanded:
        assert item.text == "\n".join(list_source.splitlines()[item.start - 1:item.end])
    mixed_lists = f"""1. {prose}
   Wrapped ordered detail remains part of this item.
- {prose}
  Wrapped unordered detail remains part of this item.
2. Too short

{prose}"""
    ordered = passages("mixed-lists.md", mixed_lists, 10, include_ordered_lists=True)
    unordered = passages("mixed-lists.md", mixed_lists, 10, include_lists=True)
    both = passages("mixed-lists.md", mixed_lists, 10, include_lists=True,
                    include_ordered_lists=True)
    assert [(p.start, p.end) for p in ordered] == [(1, 2), (7, 7)], ordered
    assert [(p.start, p.end) for p in unordered] == [(3, 4), (7, 7)], unordered
    assert [(p.start, p.end) for p in both] == [(1, 2), (3, 4), (7, 7)], both
    checklist = "1. Add the connector to Claude.\n2. Validate authentication using the inspector.\n\n" + prose
    grouped = passages("checklist.md", checklist, 10, include_ordered_lists=True)
    assert [(p.start, p.end) for p in grouped] == [(1, 2), (4, 4)], grouped
    assert grouped[0].text == "\n".join(checklist.splitlines()[:2])
    boundaries = f"""<AccordionGroup>
  <Accordion>
    * {prose}
    ```text
    This code must never be mistaken for explanatory prose in the corpus.
    ```
    Standalone prose after the fence still belongs in the extracted corpus.
  </Accordion>
  <Accordion>
    1. {prose}
       This ordered continuation must stay excluded from the extracted corpus.
  </Accordion>
  <Accordion>
    Standalone sibling prose after the ordered list must also be extracted.
  </Accordion>
</AccordionGroup>"""
    expanded = passages("boundaries.md", boundaries, 10, include_lists=True)
    assert [(p.start, p.end) for p in expanded] == [(3, 3), (7, 7), (14, 14)], expanded
    ordered = passages("boundaries.md", boundaries, 10, include_ordered_lists=True)
    assert [(p.start, p.end) for p in ordered] == [(7, 7), (10, 11), (14, 14)], ordered
    ordered_code = f"""1. {prose}
   ```text
   {prose}
   ```
   This continuation after nested code still belongs to the ordered step.

{prose}"""
    assert [p.start for p in passages("ordered-code.md", ordered_code, 10, include_lists=True)] == [7]
    ordered = passages("ordered-code.md", ordered_code, 10, include_ordered_lists=True)
    assert [p.start for p in ordered] == [1, 5, 7], ordered
    assert all("code must never" not in p.text for p in ordered)
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

        list_text = f"1. {prose}\n- {prose}"
        (root / "lists.md").write_text(list_text)
        manifest["pages"].append({
            "path": "lists.md", "sha256": hashlib.sha256(list_text.encode()).hexdigest(),
        })
        manifest["page_count"] = 4
        (root / "manifest.json").write_text(json.dumps(manifest))
        _, loaded = load_corpus(root, 10, include_ordered_lists=True)
        list_passages = [item for item in loaded if item.path == "lists.md"]
        assert [item.start for item in list_passages] == [1], list_passages

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
    root = Path(__file__).resolve().parents[2]
    artifacts = root / "3-check/pilot"
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
    _, expanded = load_corpus(root / "corpus", 10, include_lists=True)
    drive = {p.start: p for p in expanded if p.path == "connectors/google/drive.md"}
    assert drive[51].end == 51 and drive[59].end == 59
    assert len(words(drive[51].text)) == 11 and len(words(drive[59].text)) == 10
    print("PASS: expanded extraction includes both Drive passages with exact source ranges")


if __name__ == "__main__":
    check()
    check_artifacts()
