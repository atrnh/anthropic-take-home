# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["scikit-learn==1.7.2"]
# ///
"""Exercise report generation and queue-bound advice without a model call."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from run import generate


def check():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        corpus, output = root / "corpus", root / "output"
        corpus.mkdir()
        prose = 'Configure your service using the supported authentication settings before connecting external clients to private resources. </script><script>alert("test")</script>'
        pages = []
        for name in ("overview.md", "guide.md"):
            content = prose + "\n"
            (corpus / name).write_text(content)
            pages.append({"path": name, "sha256": hashlib.sha256(content.encode()).hexdigest()})
        (corpus / "manifest.json").write_text(json.dumps({"fetched_at": "fixture", "page_count": 2, "pages": pages}))
        protected = root / "protected" / "sources"
        protected.mkdir(parents=True)
        try:
            generate(protected, protected.parent, 1)
        except ValueError:
            pass
        else:
            raise AssertionError("Overlapping source export accepted")
        assert protected.exists()
        result = generate(corpus, output, 1)
        assert result["candidates"] == 1
        assert json.loads((output / "run.json").read_text())["report"] == "review.html"
        original_queue = (output / "queue.json").read_bytes()
        original_report = (output / "review.html").read_bytes()
        generate(corpus, output, 1)
        assert (output / "review.html").read_bytes() == original_report
        queue = json.loads(original_queue)
        for passage in queue["passages"]:
            assert passage["source_href"].endswith(".html#L1")
            source = (output / "sources" / (passage["path"] + ".html")).read_text()
            assert 'id="L1"' in source and '&lt;/script&gt;' in source
        assert prose.encode() not in original_report
        advice = root / "advice.json"
        data = {"queue_sha256": result["queue_sha256"], "cases": [{
            "id": queue["candidates"][0]["id"], "classification": "NECESSARY_REPETITION",
            "needs_review": False, "rationale": "Keep both explanations for local context.",
            "suggested_consolidation": None}]}
        advice.write_text(json.dumps(data))
        assert generate(corpus, output, 1, advice)["advisory_notes"] == 1
        assert (output / "queue.json").read_bytes() == original_queue
        advised_report = (output / "review.html").read_bytes()
        assert b'Keep both explanations' in advised_report
        data["queue_sha256"] = "stale"
        advice.write_text(json.dumps(data))
        try:
            generate(corpus, output, 1, advice)
        except ValueError:
            pass
        else:
            raise AssertionError("Stale advice accepted")
        assert (output / "review.html").read_bytes() == advised_report
        (corpus / "guide.md").rename(corpus / "replacement.md")
        pages[1]["path"] = "replacement.md"
        (corpus / "manifest.json").write_text(json.dumps({"fetched_at": "fixture-2", "page_count": 2, "pages": pages}))
        generate(corpus, output, 1)
        assert not (output / "sources/guide.md.html").exists()
        assert (output / "sources/replacement.md.html").exists()
    print("PASS: complete workflow, deterministic output, escaped sources, advisory queue preservation, stale advice rejection")


if __name__ == "__main__":
    check()
