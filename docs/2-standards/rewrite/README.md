# Install a plugin: worked rewrite

This example applies the [style-guide excerpt](../style-guide.md) and
[how-to template](../templates/how-to.md) to the pinned Cowork installation page.
It incorporates a separately authored Government variant to demonstrate one
task page presenting different workflows. It is not a published Claude Docs page.

- [Before](snapshots/before.md): exact copy of `corpus/cowork/guide/plugins.md`.
- [After](generated/after.md): assembled Markdown, including both labeled variants.
- [Interactive preview](generated/after.html): one standalone page with a native selector.
- [What changed and why](changelog.md): source mapping, dispositions, and open checks.

## What to edit

```text
rewrite/
├── source/                 edit these to change the page
│   ├── page.md             shared introduction and identification help
│   ├── variants/           complete workflows by context
│   └── preview-head.html   preview styles and chooser behavior
├── generated/              machine-generated; do not edit
│   ├── after.md            assembled Markdown
│   └── after.html          standalone preview
├── snapshots/              preserved evidence; do not edit
│   └── before.md           exact copy of the original page
├── build.py                editable build tool
├── verify.py               editable artifact checks
├── changelog.md            editable editorial decisions
└── README.md               this guide
```

Change the files under `source/`, then rebuild `generated/`. Keep the snapshot
unchanged so the before/after comparison stays verifiable. The style guide and
template in the parent directory are also maintained by hand.

## Build and verify

Rebuild:

```sh
python3 docs/2-standards/rewrite/build.py
```

The build uses the existing `pandoc` executable; it introduces no package
dependency or general-purpose documentation framework. Commit the files in
`generated/` for reviewers who do not run the build, but never patch them directly.
Each generated file includes a do-not-edit notice.

Run `python3 docs/2-standards/rewrite/verify.py` to check the before copy,
reproducibility, composed content, heading count, and unique fragment IDs.

For a local browser preview:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs/2-standards/rewrite
```

Open `http://127.0.0.1:8765/generated/after.html`. The chooser supports
`?instructions=cowork`, `?instructions=government`, and `?instructions=all`.
For example, `?instructions=government#government-file` opens the matching
file-install instructions. Unknown or contradictory context asks the reader to
choose; it never silently substitutes the general guide. Without JavaScript,
the Markdown and HTML retain both labeled workflows. Print also shows both.

This demonstrates a local chooser, not a site-wide preference system. It has no
tracking, saved account settings, production redirects, or deployed URLs. The
task page links to existing documentation for adjacent tasks and references;
their eventual consolidation is described in the audit example.
