"""Check the real assembled artifact. Run after editing the source files."""

from html.parser import HTMLParser
from pathlib import Path

from build import build


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        self.headings += tag == "h1"


root = Path(__file__).resolve().parent
assert (root / "snapshots/before.md").read_bytes() == (root.parents[2] / "corpus/cowork/guide/plugins.md").read_bytes()
outputs = [root / "generated/after.md", root / "generated/after.html"]
before = [path.read_bytes() for path in outputs]
build()
assert before == [path.read_bytes() for path in outputs], "Generated files were stale; rebuild and review them."
page = Page()
page.feed((root / "generated/after.html").read_text())
assert page.headings == 1
assert len(page.ids) == len(set(page.ids)), "Duplicate IDs break deep links."
assert {"instructions", "cowork", "government", "cowork-file", "government-file"} <= set(page.ids)
text = (root / "generated/after.md").read_text()
assert "{{" not in text
for name in ("cowork", "government"):
    assert (root / "source/variants" / f"{name}.md").read_text().strip() in text
print("PASS: exact before, reproducible outputs, one H1, unique IDs, both complete sources assembled.")
