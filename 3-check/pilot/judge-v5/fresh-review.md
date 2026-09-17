# Fresh duplicate-prose proposals

These six cases were selected on purpose to probe three plausible partial consolidations and three kinds of necessary or distinct repetition. They are not random samples.

Ashley approved all six proposed decisions and treatments before either fresh judge
run. The approved version is recorded in `examples-fresh.json`; the proposals below
preserve the wording presented for review.

Freshness means new passage pairs, not entirely unseen source documents. The testing
case includes a warning line previously compared with troubleshooting text. The
current comparison concerns the builder index and testing guide, not that warning
pair. No proposed pair overlaps both sides of an earlier example or judged pair.
The human review question clarifies that useful MCPB additions must be preserved,
the Claude Code check belongs in the consolidated testing guide, and submission
ownership constraints must remain locally visible after linking the allowlist rules.

## 1. MCPB route page vs builder guide

Provisional call: duplicate. Expected treatment: keep the full concept in `connectors/building/mcpb.md`; shorten the route page to an orientation and link while preserving its user and administrator routes.

`connectors/custom/desktop-extensions.md:24-38`

> ## MCPB (MCP Bundles)
>
> MCPB is Anthropic's utility for building and deploying desktop extensions:
>
> * Package MCP servers for distribution
> * Handle cross-platform compatibility
> * Manage dependencies
> * Support enterprise deployment
>
> ### Key features
>
> * **Bundling**: Package your MCP server with all dependencies
> * **Distribution**: Deploy to users via your organization's channels
> * **Updates**: Manage version updates centrally
> * **Security**: Sign and verify extensions

`connectors/building/mcpb.md:15-25`

> ## What is an MCPB?
>
> An `.mcpb` file is a zip archive containing a local MCP server and a `manifest.json`. It enables single-click installation in Claude Desktop, similar to a browser extension.
>
> Key characteristics:
>
> * Runs locally on the user's machine
> * Communicates via stdio transport
> * Bundles all dependencies
> * Works offline
> * No OAuth required

Why it is useful: this is a clear route-page versus canonical-builder ownership question, and neither span appeared in the earlier examples, results, or judge packets.

## 2. Builder testing summary vs testing guide

Provisional call: duplicate. Expected treatment: let the testing guide own the sequence; route to it from the builder index and preserve the unique Claude Code check.

`connectors/building/index.md:66-70`

> ## Testing your server
>
> 1. Add directly to Claude via **Customize > Connectors**
> 2. Use the [MCP inspector](https://modelcontextprotocol.io/docs/tools/inspector) to validate auth flows
> 3. Add to Claude Code with `claude mcp add` and check `/mcp` for status. See the [Claude Code MCP quickstart](https://code.claude.com/docs/en/mcp-quickstart).

`connectors/building/testing.md:9-25`

> Test your server against the real Claude client before submitting. There is no separate staging environment—you test in production using a custom connector.
>
> ## Test as a custom connector
>
> Any Claude account (Free, Pro, Max, Team, or Enterprise) can add a custom connector. Go to **Customize > Connectors**, select **Add custom connector**, and enter your server's URL. Custom connectors use the exact same runtime as directory connectors, so what works here will work after publication.
>
> ## Test a local server
>
> To test a server running on your machine, expose it as a public URL with a tunnel such as [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) or `ngrok`, then add the tunnel URL as a custom connector. This is the recommended pattern for iterating on MCP Apps as well.
>
> <Warning>
>   A tunnel exposes your local server to the public internet. Keep authentication enabled on your server while tunneling, and shut the tunnel down when you're done testing.
> </Warning>
>
> ## Validate with MCP Inspector
>
> Use the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) to verify protocol compliance, exercise your auth flow, and inspect tool schemas before connecting to Claude.

Why it is useful: it tests partial consolidation. Two checklist items repeat the specialist guide, while one item carries unique Claude Code scope.

## 3. External-link allowlist rules in submission and implementation guides

Provisional call: duplicate. Expected treatment: keep the matching rules in the external-links guide; keep the submission field instruction and a link in the submission guide.

`connectors/building/submission.md:73-85`

> ## Allowed link URIs
>
> If your connector uses the `ui/open-link` capability to open URLs in the user's browser or native apps, provide the list of link targets your server will request. Claude uses this list to suppress the "Open external link" confirmation prompt for destinations you've declared. Links to any other destination still work—users are simply asked to confirm before the link opens.
>
> Provide each entry in one of two forms:
>
> * **HTTPS origin** — `https://example.com`. Only the scheme and hostname are matched; paths, ports, and query strings are ignored. Subdomains are not implied—list each one (`https://app.example.com`, `https://docs.example.com`).
> * **Custom URI scheme** — `myapp:` for deep links into a native app you own (for example, `spotify:` or `notion:`). Only the scheme is matched.
>
> Every origin and scheme you list **must be owned by you** (the submitting organization). You may not list third-party domains or URI schemes registered to apps you don't publish. Entries you don't own will be removed during review.
>
> <Note>
>   This field is optional. If omitted, your connector functions normally, but users are shown a confirmation prompt each time it opens a link.
> </Note>

`connectors/building/mcp-apps/external-links.md:9-28`

> When your MCP App sends a `ui/open-link` request, Claude shows an "Open external link" confirmation modal before navigating. This protects users from being silently redirected by an embedded app.
>
> Directory connectors can declare a set of trusted destinations that open immediately without the modal. Custom connectors and locally configured servers always show the modal.
>
> ## Default behavior
>
> A `ui/open-link` request displays a confirmation modal showing the destination URL. The link opens in a new tab when the user confirms; the request resolves as cancelled if they dismiss the modal.
>
> ## Allowlisting link destinations
>
> If your connector is published in the [Connectors Directory](/docs/connectors/directory), you can declare destinations that skip the modal. Provide them in the **Allowed link URIs** field when you [submit](/docs/connectors/building/submission) or update your directory listing.
>
> Each entry must be one of two shapes:
>
> | Entry shape       | Example                         | Matches |
> | ----------------- | ------------------------------- | ------- |
> | HTTPS origin      | `https://docs.example.com`      | Any `https://` URL whose hostname is exactly `docs.example.com` (case-insensitive). Subdomains do not match implicitly; list each one you need. Port is not compared. |
> | Custom URI scheme | `example-app` or `example-app:` | Any URL with the scheme `example-app:`, typically a deep link into your native mobile or desktop app. |
>
> Entries that do not fit one of these shapes are ignored. This includes bare hostnames such as `example.com`, `http://` origins, and malformed values.

Why it is useful: this is detailed semantic overlap outside the old plugin, skill, Drive, slug, marketplace, and sales cases.

## 4. Tunnel API-key warnings in alternative deployment branches

Provisional call: not duplicate. Expected treatment: keep both rendered warnings at the completion point of their Helm and Docker Compose branches.

`connectors/mcp-tunnels/setup.md:96`

> Revoke the Tunnels API key in **Organization settings > Tunnels > Tunnels API** as soon as the install completes. Helm records `--set` values in its release history Secrets, and Kubernetes Secrets are not encrypted at rest by default, so the key remains recoverable from the cluster until you revoke it.

`connectors/mcp-tunnels/setup.md:216`

> Revoke the Tunnels API key in **Organization settings > Tunnels > Tunnels API** before continuing, and run `unset API_TOKEN`. The stack does not need the key at runtime.

Why it is useful: this is intentionally hard negative evidence. The repeated action is security-critical and locally necessary in mutually exclusive procedures.

## 5. Fully populated test credentials in preparation and checklist contexts

Provisional call: not duplicate. Expected treatment: retain the rejection-relevant prerequisite in the checklist and the preparation detail in the testing guide.

`connectors/building/testing.md:37-39`

> ## Prepare test credentials for review
>
> Directory submission requires test credentials. Provide a **fully populated account**—not an empty shell—so reviewers can exercise real functionality (list real records, search real data, exercise write tools on real resources). Include step-by-step setup instructions for someone unfamiliar with your service.

`connectors/building/review-criteria.md:68-72`

> ## Submission requirements
>
> * **Test credentials** are required and must be a fully populated account.
> * **Allowed link URIs** are recommended if your server calls `ui/open-link`. Declared HTTPS origins and custom URI schemes open without a confirmation prompt; anything else still prompts the user. See [Allowed link URIs](/docs/connectors/building/submission#allowed-link-uris).
> * **Public documentation** is required by your publish date—a blog post or help-center article is sufficient. You can share docs privately with Anthropic during review.

Why it is useful: it tests whether the reviewer preserves a short gate in a checklist even when a specialist page explains the same requirement.

## 6. Generic connector authentication vs Microsoft 365 prerequisites

Provisional call: not duplicate. Expected treatment: keep Microsoft tenant-consent and role requirements with the service procedure; scope the generic steps and route readers to service-specific prerequisites.

`connectors/getting-started.md:40-45`

> ### Step 3: Authenticate
>
> 1. Click "Connect" next to your chosen service
> 2. Log in to your account on that service
> 3. Grant Claude the requested permissions
> 4. Return to Claude

`connectors/microsoft/365.md:27-35`

> ## Setup requirements
>
> On Free, Pro, and Max plans, no organization-level setup is needed. Connect from **Customize > Connectors** in claude.ai. A Microsoft Entra Global Administrator still needs to grant one-time tenant consent for your Microsoft organization.
>
> ### Prerequisites
>
> * A work or school Microsoft account on a Microsoft Entra tenant (personal accounts such as outlook.com, hotmail.com, or live.com aren't supported)
> * Claude user with Owner or Primary Owner role (Team and Enterprise plans)
> * Global Administrator access to Microsoft Entra tenant

Why it is useful: the passages share the connection task but differ in actor, preconditions, and outcome. Treating the service-specific handoff as duplicate prose would remove a blocker readers need before connecting.
