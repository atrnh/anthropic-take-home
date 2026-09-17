# Install a plugin: worked rewrite

This example applies the [style-guide excerpt](../style-guide.md) and
[how-to template](../how-to-template.md) to the pinned Cowork installation page.
It incorporates a separately authored Government variant to demonstrate one
task page presenting different workflows. It is not a published Claude Docs page.

- [Before](snapshots/cowork--guide--plugins.md): exact copy of `corpus/cowork/guide/plugins.md`.
- [Government source](snapshots/government--desktop--plugins.md): preserved evidence for that variant.
- [After](build/page.md): assembled Markdown, including both labeled variants.
- [Interactive preview](build/page.html): a standalone page with a native selector.
- [What changed and why](changelog.md): source mapping, dispositions, and open checks.

## View the result

Download or open `build/page.html` in a browser. It includes its styles and
script, so you can share that file on its own. No build tools or server are needed.
GitHub's file viewer shows the HTML source; download the file to view the page.

## Set up and preview

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```sh
cd docs/2-standards/rewrite
uv sync --locked
uv run build.py serve --open
```

`uv` creates the local environment and installs the locked dependencies. It can
also download a compatible Python if you do not have one; Python 3.11 or later
is required. There is no Pandoc or Node.js dependency.

The preview command builds the page, starts a server on your machine, and opens
[the preview](http://127.0.0.1:8765/page.html) in your browser. If the browser does
not open, use that link. Stop the server with **Ctrl+C**. If port 8765 is in use,
choose another with `uv run build.py serve --open --port 8766`.

You can copy this entire `rewrite` directory elsewhere and run the same commands
from inside it. The build and checks do not depend on the parent repository.
The editorial links to the parent style guide, template, and corpus still refer
to that repository.

## Edit, build, and check

```text
rewrite/
├── source/
│   ├── page.md             shared Markdown and Jinja2 loops
│   ├── variants/           complete Markdown workflows by context
│   └── templates/
│       ├── page.html       Jinja2 HTML document template
│       └── preview-head.html  inline styles and chooser behavior
├── build/                  committed output; do not edit directly
│   ├── page.md
│   └── page.html
├── snapshots/              preserved evidence; do not edit
├── build.py                build and local preview commands
├── verify.py               artifact and snapshot checks
├── pyproject.toml          Python requirements and dependencies
├── uv.lock                 resolved dependency versions
├── changelog.md            editorial decisions
└── README.md
```

Edit `source/`, then run:

```sh
uv run build.py
uv run verify.py
```

Refresh the browser after rebuilding. The server does not watch for edits.
To build and open the file without starting a server, use `uv run build.py --open`.
Commit `build/` with source changes so reviewers can view the result without
installing anything. Verification reports missing or stale outputs without
rewriting them, checks the snapshot's pinned SHA-256 digest, and checks composed
content, variant discovery and defaults, heading count, and fragment IDs. These comparisons
normalize line endings so Windows checkouts work too.

Jinja2 loops assemble the Markdown from the available variants. Python-Markdown
renders it using its
`md_in_html`, `attr_list`, `toc`, `fenced_code`, and `tables` extensions; Jinja2 then
places the result in `source/templates/page.html`. Use `<div markdown="1">` for Markdown inside HTML
containers and `{#some-id}` for explicit heading IDs. Jinja2 comments use
`{## comment ##}` here to avoid conflicting with heading IDs. Missing template
variables or includes fail the build. Sources are trusted, authored files: raw
HTML is preserved, and the rendered body is deliberately marked safe in the HTML
template.

## Add or choose a default variant

Add a Markdown file to `source/variants/`; the build discovers files in filename
order and generates both selector options and content sections. The filename
without `.md` becomes the URL value and section ID. Use lowercase letters,
numbers, and hyphens, starting with a letter; `all` is reserved.

Set a selector label and optional default in YAML frontmatter:

```yaml
---
label: Claude Desktop (General)
default: true
---
```

The build uses the filename as the label if `label` is omitted. Only one variant
may set `default: true`; omit it or use `default: false` for other variants.
Frontmatter is removed from the rendered content. Variant bodies are Markdown;
page layout and loops belong in `source/page.md`. The shared page generates an
H2 from each label, so variant bodies start with applicability text and use H3
headings for methods. Put trust conditions and restrictions before the affected
steps; use `<aside class="callout" markdown="1">` with a bold title for a callout.

Cowork is the default on a plain page URL. An explicit `instructions` query or
a variant fragment takes precedence. With no configured default, the page asks
the reader to choose. Unknown or contradictory URLs also ask the reader to choose.
Selecting **Choose a guide** keeps that choice in the URL as `?instructions=`.

## Try the chooser

The chooser supports `?instructions=cowork`, `?instructions=government`, and
`?instructions=all`. For example,
[the Government file-install procedure](http://127.0.0.1:8765/page.html?instructions=government#government-file)
opens the matching instructions while the preview server is running.
Unknown or contradictory context asks the reader to choose. Without JavaScript,
both labeled workflows remain readable and the chooser stays hidden. Print also
shows both guides.

This demonstrates a local chooser, not a site-wide preference system. It has no
tracking, saved account settings, production redirects, or deployed URLs. The
task page links to existing documentation for adjacent tasks and references;
their eventual consolidation is described in the audit example.
