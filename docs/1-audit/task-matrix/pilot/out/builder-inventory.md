# Development and publication inventory (builder view)

Rows are lifecycle stages; columns are artifact types. A cell lists the tasks documented for that stage and artifact with their procedure variant IDs, so shared workflows line up across artifact types. `—` = nothing documented.

| Stage | skill | plugin | connector | mcp-app |
|---|---|---|---|---|
| build | T-071 author a skill package on disk: P1a, P1b | — | — | T-067 allowlist external link destinations for an MCP App: P1a |
| test | T-045 test a skill before distributing it:  | — | — | — |
| package | T-072 package a skill for distribution: P1a | T-039 package a plugin archive: P1a, P2a | — | — |
| submit | — | T-041 submit a plugin to the plugin directory: P1a, P2a | T-058 submit a connector to the directory: P1a, P1b | — |
| review | — | — | T-057 prepare a connector for directory review: P1a, P2a, P3a<br>T-059 use the submissions dashboard: P1a | — |

## Per-task summaries

- **T-039 package a plugin archive** (plugin / package): Only Claude for Government documents plugin packaging: a hand-built zip, or the same layout assembled by Claude in a Cowork task.
- **T-041 submit a plugin to the plugin directory** (plugin / submit): One page documents plugin directory submission on claude: an admin-settings form for Team/Enterprise orgs and a Console web-portal form for individuals.
- **T-045 test a skill before distributing it** (skill / test): No documented procedure: the only candidate validates the package statically and never exercises the skill against a matching task.
- **T-057 prepare a connector for directory review** (connector / review): Connector review prep is documented only for undistinguished Claude: privacy policy files, carousel asset specs, and a pre-submission checklist plus plugin validate.
- **T-058 submit a connector to the directory** (connector / submit): One web-portal click-through family on `claude`: org-settings portal for remote servers and MCP Apps, separate form for MCPB desktop extensions.
- **T-059 use the submissions dashboard** (connector / review): Only the generic connector submission page documents tracking review status; post-publication metrics live on the listing page.
- **T-067 allowlist external link destinations for an MCP App** (mcp-app / build): Only the generic connector submission page documents declaring link targets to suppress the external-link confirmation prompt.
- **T-071 author a skill package on disk** (skill / build): Both products author a skill folder holding SKILL.md on disk; government restricts the folder to text files for admin-portal distribution.
- **T-072 package a skill for distribution** (skill / package): Only the generic skill authoring guide documents zipping a skill folder, with the directory inside the ZIP root.
