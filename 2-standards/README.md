# Editorial standards and worked rewrite

Start with the [style-guide excerpt](style-guide.md) for rules on writing task
pages with context-dependent instructions. The [how-to template](how-to-template.md)
provides the page structure.

Continue reading to learn how to view the [plugin installation rewrite](rewrite/README.md).

> [!NOTE]
> The plugin installation instructions don't match the version of Claude Desktop I have on
> my machine. I went ahead and optimistically updated the general installation
> instructions since I'm familiar with the product. I did not update the Claude for
> Government instructions, since I can't verify the accuracy of those instructions myself.

## View the rewrite in a browser

Open `rewrite/build/page.html` in your browser. The file includes its styles
and script, so no installation or server is needed.

## Build it yourself

To rebuild and open a local preview, install
[uv](https://docs.astral.sh/uv/getting-started/installation/), then run these commands
from the repository root:

```sh
cd 2-standards/rewrite
uv sync --locked
uv run build.py serve --open
```

The last command builds the page, starts a local server, and opens your browser.
If the browser does not open, visit [the preview](http://127.0.0.1:8765/page.html).
Stop the server with **Ctrl+C**.

See the [rewrite README](rewrite/README.md) for editing, verification, and alternate
port instructions. Compare the [original](rewrite/snapshots/government--desktop--plugins.md) [pages](rewrite/snapshots/cowork--guide--plugins.md) with
the result, and read [the rewrite decisions](rewrite/changelog.md) for what changed
and why.
