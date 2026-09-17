# Two editorial decisions

These examples come from the pilot's human review. They illustrate the decision
to make after retrieval; a high similarity score alone cannot make it for you.

## Merge general additions, then shorten

The [plugins overview](../../corpus/plugins/overview.md) defines a plugin as a
package of connectors, skills, commands, and sub-agents. The
[Government introduction](../../corpus/government/desktop/plugins.md) repeats the
definition, mentions hooks, and says plugins work in Cowork and Code before linking
back to the overview.

**Decision: actionable consolidation.** Bring broadly applicable additions from
the Government introduction into the overview, retain genuinely Government-specific
information locally, then shorten the introduction and link back. Verify any
uncertain applicability before editing. The location of a statement in a Government
guide does not establish that it applies only to Government.

The important treatment is **merge, then shorten**. Merely deleting the specialized
definition could discard useful information; merely returning a duplicate label
does not tell an editor what to preserve.

## Keep brief repetition that helps readers

The [Google Drive page](../../corpus/connectors/google/drive.md) has a feature bullet:

> **Live sync:** Documents continue syncing with the latest Google Drive version.

Its FAQ also asks whether documents update after being added and answers:

> Yes, documents continue syncing with the latest Google Drive version.

**Decision: keep both.** The bullet helps readers scan capabilities. The one-sentence
FAQ answers a specific question where readers look for it. Replacing that answer
with a link would add navigation for little benefit.

This pair remains available in the candidate queue. A model may suggest keeping it,
but that suggestion never removes the evidence from human review.
