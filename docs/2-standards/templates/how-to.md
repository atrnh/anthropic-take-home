# {Verb + one reader outcome}

{State who this helps and what they will have when finished. Link to a shared
concept only when readers need it to complete the task.}

## Choose your instructions

{Name the context that changes the procedure. Put a **How to check** explanation
beside the chooser. Give readers who are unsure a way to identify their context
or ask the responsible person. Do not infer one environment from the absence of
another.}

{`source/page.md` owns the shared H1, introduction, chooser, and Jinja loops.
It renders each discovered variant below.}

<!-- Create one source/variants/{context}.md file for each complete workflow.
The filename becomes its URL value and section ID. The frontmatter label becomes
the rendered H2. Do not put an H2 in a variant body. -->

```yaml
---
label: "{Recognizable context label}"
default: true
---
```

{Start the variant body with its applicability. State prerequisites, permissions,
restrictions, and trust decisions that change the reader's choice before the
steps. Link long reference material instead of reproducing it.}

<aside class="callout" markdown="1">
**{Trust, access, or capability limit}.**

{State the decision-relevant condition before the method it affects.}
</aside>

### {Method} {#context-method}

{State when the reader should choose this method.}

1. {Start from a named, accessible location.}
2. {Give the next action with exact UI labels or commands.}
3. {Continue until this method reaches the page's outcome.}

{State the source-backed result and how the reader can inspect it. Do not claim
that installation proves a separate capability works.}

### Next steps {#context-next}

{Link to distinct tasks rather than adding their procedures here.}

<!-- Editorial record, outside the published page:
Task and outcome:
Actor and place of use:
Source and section for shared content:
Source and section for each variant and method:
Applicability, access, and deployment conditions established by sources:
Personal product knowledge used in place of a pinned source, including date and context:
Source conflicts, incomplete procedures, and unverified UI labels:
Disposition of content removed from the original:
Stable context and method IDs:

Assembly:
- `source/page.md` contains shared Markdown and Jinja loops.
- `source/variants/` contains independently authored Markdown variants with YAML
  `label` and optional boolean `default`. The build discovers variants in filename
  order. Only one variant can be the default.
- `source/templates/page.html` is the HTML wrapper.
- `source/templates/preview-head.html` contains preview styles and chooser behavior.
- Build and review `build/page.md` and `build/page.html`. Do not edit them directly.
-->
