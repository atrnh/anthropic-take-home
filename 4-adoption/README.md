# Adoption playbook

Adoption is like a political campaign: I'm asking people to buy into something that
changes how they work, that they'll live with long after the decision is made, and that
many of them didn't ask for.

## Start door to door

Meet with individuals from product teams and talk to them. The goal is to get to know
people, not to persuade. Understand where they're at, what they're working on, what
they like and don't like, how they usually do things, who writes documentation, etc. This
happens via lots of direct contact, casual Slack messages, etc.

## Collect endorsements

Demonstrate value to a small handful of people first. A new platform[^1] is much more credible
if people are actually using it. Others will be more willing to come on board when they
hear "you should use this, it's fine" from someone besides the person who built it.

## Solidify messaging

Come up with a one sentence pitch that allows someone to instantly understand the platform's
value. Do the same for every feature/benefit/solution (or at least the ones that people
would actually care about). Messages have an easier time traveling when they're short,
memorable, and easy to understand. Work this out before larger communications go out.

## Lower the cost of voting

Make adoption easy. Developer/writer experience should be just as important as reader
experience. Build internal tooling that automates boring stuff and improves quality of
life: codemods, linters, skills, Git hooks, PR checks, etc. Developer/writer-facing
platform docs must have a quickstart/tutorial and how-to guides for the most common
tasks—not just reference documentation.

## Govern responsibly

Uphold the social contract between the platform team and its users. Product teams cede
some freedom and control to the platform; in return, it must be fast, reliable, and
responsive to the teams' needs.

**When a team ignores me**, something has lost their trust: maybe checks are too noisy to
be reliable; maybe there's uncertainty about document ownership or a standard that
doesn't fit their content; maybe it's something else entirely, or it's me. Diagnose where
the disconnect is happening and fix it. Follow through until engaging feels worth their time.

Trust runs both ways. When a team holds firm against my recommendation, I assume they know
something I don't. My job is informed consent: the people a decision affects should
understand its risks before it's made. The bigger the blast radius, the wider that circle
gets, sometimes up to the product owner or other stakeholders.

[^1]: I'm assuming a documentation platform with structure, checks, standards, tooling, etc.