"""Check the committed artifacts without changing them: uv run verify.py."""

from hashlib import sha256
from html.parser import HTMLParser
import re
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import frontmatter
from build import ROOT, render


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.headings = 0
        self.labels = []
        self.in_label = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        self.headings += tag == "h1"
        if tag == "h2":
            self.in_label = True
            self.labels.append("")

    def handle_data(self, data):
        if self.in_label:
            self.labels[-1] += data

    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_label = False


class BuildChecks(unittest.TestCase):
    def test_artifacts(self):
        outputs = render()
        self.assertEqual(outputs, render(), "Rendering must be deterministic")
        for name, content in outputs.items():
            path = ROOT / "build" / name
            self.assertTrue(path.exists(), f"Missing {name}; run uv run build.py")
            self.assertEqual(path.read_text(encoding="utf-8"), content,
                             f"Stale {name}; run uv run build.py")
        page = Page()
        page.feed(outputs["page.html"])
        self.assertEqual(page.headings, 1)
        self.assertEqual(len(page.ids), len(set(page.ids)), "Duplicate fragment IDs")
        self.assertIn("instructions", page.ids)
        self.assertIn("selection-status", page.ids)
        self.assertIn('<option value="">Choose a guide</option>', outputs["page.html"])
        for source in (ROOT / "source" / "variants").glob("*.md"):
            self.assertIn(source.stem, page.ids)
            self.assertIn(f"{source.stem}-heading", page.ids)
            post = frontmatter.loads(source.read_text(encoding="utf-8"))
            self.assertIn(post.get("label", source.stem), page.labels)
            text = post.content
            self.assertIn(text, outputs["page.md"])
            for fragment in re.findall(r"\{#([^}]+)\}", text):
                self.assertIn(fragment, page.ids)
        for marker in ("{{", "{%", 'markdown="1"', "<fixme"):
            self.assertNotIn(marker, outputs["page.html"])

    def test_snapshot(self):
        # Normalize checkout line endings before checking the pinned corpus digest.
        for name, digest in {
            "cowork--guide--plugins.md": "8f1af9bef9ff72a66ecad30170e0014559cc10e175a1c005e83c4ac9b2ac3e74",
            "government--desktop--plugins.md": "a5ed354d47b734da0862ce6ccecb9e9288acddda2cbbdd3e67f58246e91f13ec",
        }.items():
            text = (ROOT / "snapshots" / name).read_text(encoding="utf-8")
            self.assertEqual(sha256(text.encode("utf-8")).hexdigest(), digest)

    def test_variant_discovery_and_defaults(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "source", root / "source")
            variants = root / "source" / "variants"
            html = render(root)["page.html"]
            self.assertIn('data-default="cowork"', html)
            self.assertIn('value="cowork" selected', html)
            extra = variants / "example.md"
            extra.write_text('---\nlabel: "Example & friends"\n---\n\nNew workflow.\n', encoding="utf-8")
            html = render(root)["page.html"]
            self.assertIn('value="example">Example &amp; friends</option>', html)
            self.assertIn('class="variant" id="example"', html)
            self.assertIn('<p>New workflow.</p>', html)
            self.assertNotIn('label:', html)
            cowork = variants / "cowork.md"
            cowork.write_text(cowork.read_text(encoding="utf-8").replace('default: true', 'default: false'), encoding="utf-8")
            self.assertIn('data-default=""', render(root)["page.html"])
            extra.write_text(extra.read_text(encoding="utf-8").replace('---\nlabel:', '---\ndefault: true\nlabel:'), encoding="utf-8")
            self.assertIn('data-default="example"', render(root)["page.html"])
            cowork.unlink()
            html = render(root)["page.html"]
            self.assertNotIn('value="cowork"', html)
            self.assertNotIn('id="cowork"', html)
            extra.write_text(extra.read_text(encoding="utf-8").replace('default: true', 'default: "true"'), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, 'boolean'):
                render(root)
            shutil.copy(ROOT / "source" / "variants" / "cowork.md", cowork)
            extra.write_text('---\ndefault: true\n---\n\nExample workflow.\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, 'Only one'):
                render(root)


if __name__ == "__main__":
    unittest.main()
