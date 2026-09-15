# Appendix: procedures by task

## T-003 add a custom connector  (product view)

Only the undistinguished Claude product documents adding a custom connector: self-serve on Free/Pro/Max, owner-then-member on Team/Enterprise.

### P1 · app-settings / click-through · Add custom connector from Customize > Connectors

**P1a** Self-serve: Add custom connector, paste the remote MCP server URL — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: Free, Pro, or Max plan; the remote MCP server URL
1. Navigate to Customize > Connectors
2. Click "Add custom connector"
3. Enter the remote MCP server URL
4. Optionally configure OAuth credentials (in the rolling-out two-step dialog: name, authentication mode, OAuth client, request headers, Advanced > Transport)
5. Click "Add"
Sources: `connectors--custom--remote-mcp` ### For Free, Pro, and Max plans

### P2 · admin-settings / click-through · Owner adds the custom connector in Organization settings, members then connect

**P2a** Team/Enterprise: owner adds by URL, member connects and authenticates — actor: admin; products: Claude (claude.ai and Claude Desktop)
Preconditions: Team or Enterprise plan; an organization owner performs the first stage; the remote MCP server URL
1. Owner: navigate to Organization settings > Connectors
2. Owner: select Add, then Custom; if Claude asks for the connector type, choose Web
3. Owner: enter the remote MCP server URL
4. Owner: optionally configure OAuth Client ID/Secret in Advanced settings
5. Owner: click "Add"
6. Member: go to Customize > Connectors
7. Member: find the connector with the "Custom" label
8. Member: click "Connect" to authenticate
Sources: `connectors--custom--remote-mcp` ### For Team and Enterprise plans

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a, P2a; diff only-here. The only product with a documented procedure; the plan tier decides the path (self-serve vs owner-then-member).
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- The owner stage of P2a could also be read as T-022 'allow or block connectors for an organization'; kept here because the owner supplies the server URL, which creates the connector rather than allowlisting an existing directory one.
- The unit's product default is the undistinguished 'claude'; the page never says whether claude-web, claude-desktop, cowork, claude-gov, claude-tag, or claude-desktop-3p show the same Customize > Connectors path, so those cells are absent rather than confirmed same.
- Whether the rolling-out two-step Add custom connector dialog is a separate variant could not be settled: its field-by-field section is descriptive, not a procedure, and the page says the numbered steps still apply.

## T-006 authenticate a connector with request headers  (product view)

Only claude.ai/Desktop documents adding up to four approved request headers in the Add custom connector dialog.

### P1 · app-settings / click-through · Request headers in the Add custom connector dialog (app-settings, click-through)

**P1a** Open Request headers, pick a name, enter the exact value, mark Required, Add — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: request header authentication is in beta and available to a limited set of organizations; a custom header name must be approved by Anthropic before Claude will send it
1. In the Add custom connector dialog, open Request headers
2. Select a header name from the list, or choose Custom header to enter a different name
3. Enter the header value exactly as the server expects it, including any scheme such as Bearer and its trailing space
4. Choose whether the header is Required
5. Repeat for any additional headers, up to four
6. Click Add
Sources: `connectors--custom--remote-mcp` ### Adding a request header

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a; diff only-here. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

## T-007 use a connector in a chat or project  (product view)

Only undistinguished Claude documents using a connector in chat: a per-conversation toggle in the "+" menu, or automatic tool selection.

### P1 · chat / click-through · Toggle connectors per conversation from the chat "+" menu

**P1a** "+" button > Connectors > enable/disable for this conversation — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: the connector is already added and connected
1. Click the "+" button in the chat interface
2. Open "Connectors"
3. Enable or disable the connectors you want for this conversation
Sources: `connectors--custom--remote-mcp` ### Enabling connectors in chat

### P2 · chat / prompt-claude · Ask Claude for the data or action and let it select the connector's tools

**P2a** Microsoft 365: ask a question or request an action, tools chosen automatically — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: the Microsoft 365 connector is connected for the account
1. Ask Claude a question that requires Microsoft 365 data, or ask it to take an action such as sending an email or updating a file
2. Let Claude automatically detect and use the necessary tools
Sources: `connectors--microsoft--365` ## Usage

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a, P2a; diff only-here. Both documented paths are written for claude.ai/Desktop without distinguishing them; no other product documents this task.
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- The Microsoft 365 Usage record (P2a) never switches a connector on for the conversation; it was kept because Claude calls the connector's tools while answering, but a stricter reading of T-007's outcome would move it to NEW ("ask Claude to use a connected connector").
- Neither record names claude.ai versus Claude Desktop, so P1a/P2a could not be split across claude-web and claude-desktop.
- No record covers the project half of the task (enabling a connector for a project), so whether the project path differs from the chat path is unsettled.

## T-010 manage installed connectors  (product view)

Only two products document managing a connector: claude edits or removes it in user and admin settings, claude-desktop-3p disconnects and then ends brokered access.

### P1 · app-settings / click-through · Manage the connector from the product's own connector settings

**P1a** Edit name or URL, or remove, via Customize > Connectors — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: the connector is already added
1. Go to Customize > Connectors
2. Click "Remove" or select the three-dot menu
3. Follow the prompts
4. To change OAuth credentials or request headers, remove the connector and add it again with the new details; members then reconnect
Sources: `connectors--custom--remote-mcp` ## Managing connectors

**P1b** Disconnect the M365 local connector, then end brokered access — actor: end-user; products: Claude Desktop on third-party inference
Preconditions: the connector entry is configured and the user is signed in
1. Select Disconnect next to the connector; the user is signed out and its stored Entra tokens are deleted from the device
2. If the user signed in through the device broker, the work or school account survives Disconnect: remove it in Windows Settings (Accounts > Access work or school) or macOS Company Portal, or revoke the user's sessions in Entra, to end access entirely
3. Expect revocation to take effect within minutes when continuousAccessEvaluation is enabled, otherwise when the current one-hour access token expires
Sources: `third-party--claude-desktop--connectors-m365--part04` ### Token storage and sign-out

### P2 · admin-settings / click-through · Manage the organization's connector from Admin settings

**P2a** Edit name or URL, or remove, via Admin settings > Connectors — actor: admin; products: Claude (claude.ai and Claude Desktop)
Preconditions: Team or Enterprise owner
1. Go to Admin settings > Connectors
2. Click "Remove" or select the three-dot menu
3. Follow the prompts
4. Authentication settings cannot be changed in place; remove and re-add the connector, after which members must reconnect
Sources: `connectors--custom--remote-mcp` ## Managing connectors

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a, P2a; diff steps-differ, actor-differs, surface-differs. Edit-or-remove path only; the same three steps are offered to Team and Enterprise owners on the admin surface. No in-place re-authentication: auth settings require remove and re-add.
- Claude Desktop on third-party inference: documented; variants P1b; diff steps-differ, surface-differs. Disconnect signs out and deletes local tokens only; ending access entirely continues into OS account settings or Entra session revocation.
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Misfiled records (excluded):
- `third-party--claude-desktop--connectors-m365--part03` ### Configure scopes: outcome not met: removing the app registration's consent in Entra changes which scopes the tenant can obtain tokens for, not the connection state of an installed connector on an account. The passage is a note attached to scope configuration, and after its last step no user's connector has been re-authenticated, reconnected, turned off, or removed. → T-022 or NEW

Open questions:
- Whether the Entra consent-removal note belongs to T-022 (org allow/block) or needs a new admin-revocation task; no pilot unit documents an org allowlist procedure for the M365 local connector.
- No product documents re-authenticating a connector or reconnecting one at a changed endpoint; the remote-MCP page explicitly routes both through remove-and-re-add, so those facets of the task outcome are undocumented everywhere.
- Whether turning a connector off with the toggles in the chat '+' menu (mentioned under ## Security and privacy in connectors--custom--remote-mcp) belongs here or to T-007; no record was extracted for it, so it could not be reconciled.

## T-012 report a problem with a connector  (product view)

Only the generic Claude connector page documents reporting, and only malicious servers to the Bug Bounty Program.

### P1 · web-portal / click-through · Bug Bounty Program report (web-portal, click-through)

**P1a** Report a malicious MCP server through the responsible-disclosure page — actor: end-user; products: Claude (claude.ai and Claude Desktop)
1. Report the malicious MCP server to Anthropic's Bug Bounty Program
Sources: `connectors--custom--remote-mcp` ## Reporting issues

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a; diff only-here. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- The source gives no reference-ID collection step, so the task outcome's 'carrying the reference ID' clause is unevidenced.

## T-013 troubleshoot connector sign-in  (product view)

Only Microsoft 365 documents connector sign-in troubleshooting: an end-user checklist for Claude, admin Entra error tables for third-party Desktop.

### P1 · third-party-admin / click-through · Match the Entra sign-in error code to the setup step that is wrong and fix it in the app registration

**P1a** Remote M365 connector: error/cause/fix table against the remote setup steps — actor: admin; products: Claude Desktop on third-party inference
Preconditions: A sign-in error appeared during remote Microsoft 365 connector setup
1. Read the error code returned at sign-in
2. AADSTS50011 redirect mismatch: re-check that the redirect URI is exactly http://127.0.0.1/callback and registered under Mobile and desktop applications, not Web
3. AADSTS50194 multi-tenant required: add the Tenant ID to the configuration
4. AADSTS65001 admin consent required: complete admin consent for the app
5. Client application is not authorized for this resource: wait for confirmation that Anthropic's allowlist was updated
6. AADSTS9000411 duplicate prompt parameter: upgrade Claude Desktop to the current release
Sources: `third-party--claude-desktop--connectors-m365--part02` ### Troubleshoot sign-in errors

**P1b** Local (built-in) M365 connector: symptom/cause/fix table against the local-mode app registration and the device broker — actor: admin; products: Claude Desktop on third-party inference
Preconditions: The built-in Microsoft 365 server is configured to run locally on each user's device
1. Read the error code or symptom from the sign-in attempt; sign-in and Graph errors are written to mcp-server-office365-builtin.log in the Claude Desktop logs directory
2. AADSTS50011 redirect mismatch: add or correct the redirect URI named in the error under Mobile and desktop applications on the local-mode app
3. AADSTS900971 no reply address: register msauth.com.anthropic.claudefordesktop://auth on the local-mode app
4. AADSTS65001 admin consent required: re-check that the Graph delegated permissions were admin-consented
5. AADSTS53003 blocked by Conditional Access: meet the brokered sign-in requirements for the platform, then restart Claude Desktop
6. AADSTS7000218: set Allow public client flows to Yes on the local-mode app registration
7. Sign-in opens the browser where the broker was expected: re-check the platform's brokered sign-in requirements (app version, Company Portal or Entra join, SSO profile, broker redirect URI, microsoftAuthBroker setting)
Sources: `third-party--claude-desktop--connectors-m365--part04` ### Troubleshoot the local connector

### P2 · app-settings / click-through · Work an end-user checklist of credential, licence, policy, and browser-state causes

**P2a** Authentication failures accordion on the Microsoft 365 connector page — actor: end-user; products: Claude (claude.ai and Claude Desktop)
1. Verify the Microsoft 365 credentials being used are correct
2. Check that the Microsoft 365 licence is active
3. Review the organization's third-party app policies
4. Try a different browser
5. Clear cookies and cache
Sources: `connectors--microsoft--365` ## Troubleshooting

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P2a; diff surface-differs, actor-differs, steps-differ. End-user self-checks only (credentials, licence, org policy, browser state); no error codes and no admin-side fix.
- Claude Desktop on third-party inference: documented; variants P1a, P1b; diff surface-differs, actor-differs, steps-differ, precondition-differs. Admin-side Entra diagnosis, split by connector mode: remote setup steps (P1a) vs local-mode app registration and device broker (P1b).
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- P1a and P1b were kept as separate variants because the remote and local connector modes are mutually exclusive deployments with different registrations; if the reconciler treats them as one path the family collapses to a single variant.
- The generic 'Authorization with the MCP server failed' OAuth error named in the task definition appears in no record here; unclear whether a product-neutral sign-in troubleshooting procedure exists on a page no record was extracted from.
- The claude record's surface was extracted as app-settings, but its steps (credentials, licence, org policy, browser cookies) happen outside Claude's settings; 'other' may be truer, though the family count would not change.

## T-015 troubleshoot a connector tool call failure  (product view)

Only third-party-inference Claude Desktop documents fixing M365 tool failures by adding and consenting missing Graph scopes.

### P1 · third-party-admin / click-through · Entra app registration and connector scope list (third-party-admin, click-through)

**P1a** Add the missing Graph scope in both places and grant admin consent — actor: admin; products: Claude Desktop on third-party inference
1. For a tool permission error or Graph 403, identify the scope the tool needs
2. Add the scope on the app registration and in the entry's scope list
3. Grant admin consent for the scope
4. For missing or failing write tools, add the matching write scope to the entry and consent it on the app registration
5. Upgrade Claude Desktop if the installed version predates write support
Sources: `third-party--claude-desktop--connectors-m365--part04` ### Troubleshoot the local connector

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: documented; variants P1a; diff only-here. 
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

## T-019 set up the Microsoft 365 connector  (product view)

Two products document M365 setup: claude.ai admin-then-user connect, and third-party-inference Desktop with Entra registration plus in-app or managed-file configuration.

### P1 · app-settings / click-through · Configure through the product's own connector settings, then each user connects from Customize > Connectors

**P1a** Team/Enterprise: owner adds M365 org-wide, then members connect — actor: admin, end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: Owner or Primary Owner role on a Team or Enterprise plan; Global Administrator access to the Microsoft Entra tenant; work or school Microsoft account on an Entra tenant (personal accounts unsupported); active Microsoft 365 accounts for all users
1. Admin: navigate to Organization settings > Connectors
2. Select Add, then All available
3. Find Microsoft 365 and select "Add to your team"
4. Connect individually and grant organization-wide permissions
5. Optionally restrict user access or revoke specific permission scopes
6. Member: navigate to Customize > Connectors
7. Find Microsoft 365 and click "Connect"
8. Authenticate with Microsoft 365 credentials
Sources: `connectors--microsoft--365` ### Phase 1: Administrator setup; `connectors--microsoft--365` ### Phase 2: User enablement

**P1b** Free/Pro/Max: user connects directly, no organization-level setup — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: Free, Pro, or Max plan; a Microsoft Entra Global Administrator has granted the one-time tenant consent for the Microsoft organization
1. Navigate to Customize > Connectors in claude.ai
2. Find Microsoft 365 and click "Connect"
3. Authenticate with Microsoft 365 credentials
Sources: `connectors--microsoft--365` ## Setup requirements; `connectors--microsoft--365` ### Phase 2: User enablement

**P1c** Remote connector: Entra consent, desktop app registration and Anthropic allowlisting, configured in the in-app configuration window — actor: admin, end-user; products: Claude Desktop on third-party inference
Preconditions: Global Administrator or Cloud Application Administrator in the Entra tenant; Claude Desktop deployed on third-party inference; Anthropic allowlists the tenant and client IDs (two to three business days); FedRAMP/GovCloud deployments need a different connector app ID and hostname from an Anthropic representative
1. Copy the Directory (tenant) ID from Entra admin center > Overview
2. Open the adminconsent URL for that tenant with Anthropic's connector client_id, review the delegated read-only Graph permissions, and select Accept
3. In App registrations > New registration, register a desktop client app (this directory only) with redirect URI http://127.0.0.1/callback under Mobile and desktop applications
4. Select Register and note the Application (client) ID and Directory (tenant) ID
5. Under API permissions, add the Anthropic API delegated permission access_as_user and select Grant admin consent for your organization
6. Email the Directory (tenant) ID and Application (client) ID to your Anthropic representative or support and wait for allowlist confirmation
7. Open the Claude Desktop in-app configuration window and open Connectors
8. Select Add server > Microsoft 365 and enter the Client ID, Tenant ID, and the access_as_user offline_access scope string
9. Select Save and deploy the configuration through your device-management tool
10. Each user opens Customize > Connectors in Claude Desktop and selects Connect next to Microsoft 365
11. The user signs in on the tenant's sign-in page in the browser and consents
Sources: `third-party--claude-desktop--connectors-m365--part02` ### Set up the remote connector; `third-party--claude-desktop--connectors-m365--part02` ### Sign in as a user

**P1d** Local connector: dedicated public client app in Entra, built-in M365 server configured in the in-app configuration window — actor: admin, end-user; products: Claude Desktop on third-party inference
Preconditions: Microsoft Entra admin center access; a separate app registration dedicated to local mode (do not reuse the remote connector's desktop client app); brokered sign-in needs Claude Desktop 1.13576.0 or later on Windows, 1.19367.0 or later on macOS; the built-in server activates only from managed configuration; users cannot add it themselves
1. In Entra admin center > App registrations > New registration, register a public client app for local mode with Supported account types set to this directory only
2. Under Authentication > Redirect URI configuration, add http://localhost under the Mobile and desktop applications card
3. For brokered sign-in on managed devices, add the per-platform broker redirect URI to the same platform via Edit and Save
4. Set Allow public client flows to Yes and Save; block the device-code flow with a Conditional Access policy scoped to All resources
5. Under API permissions > Microsoft Graph > Delegated permissions, add the scopes the connector will request and select Grant admin consent
6. Note the Application (client) ID and Directory (tenant) ID from the overview page
7. In the Claude Desktop in-app configuration window, open Connectors, select Add server, and choose Microsoft 365 under the Built-in group
8. Enter the Tenant ID and Client ID, choose the Azure cloud (global, us-gov-high, or us-gov-dod), and leave Access empty or list scopes explicitly
9. Select Test connection to verify the server starts and lists its tools, then Save and deploy the configuration
10. For brokered sign-in, meet the platform device requirements: Entra join or registration and compliance on Windows; MDM enrollment, Intune Company Portal, and an Extensible SSO Redirect profile on macOS
11. Each user opens Customize > Connectors in Claude Desktop and selects Connect on Microsoft 365
12. The user completes sign-in in the broker's system account-picker dialog, or in the system browser when the broker is unavailable
Sources: `third-party--claude-desktop--connectors-m365--part03` ### Set up the local connector; `third-party--claude-desktop--connectors-m365--part04` ### How users sign in

### P2 · filesystem / edit-file · Declare the connector in managedMcpServers in the managed JSON or plist and deploy it

**P2a** Remote connector declared in managedMcpServers by URL and transport — actor: admin, end-user; products: Claude Desktop on third-party inference
Preconditions: Global Administrator or Cloud Application Administrator in the Entra tenant; configuration managed through JSON or a plist instead of the in-app configuration window; tenant and client IDs allowlisted by Anthropic
1. Copy the Directory (tenant) ID from Entra admin center > Overview
2. Open the adminconsent URL for that tenant with Anthropic's connector client_id, review the delegated Graph permissions, and select Accept
3. In App registrations > New registration, register a desktop client app (this directory only) with redirect URI http://127.0.0.1/callback under Mobile and desktop applications, and note its Application (client) ID
4. Under API permissions, add the Anthropic delegated permission access_as_user and select Grant admin consent for your organization
5. Email the Directory (tenant) ID and Application (client) ID to Anthropic and wait for allowlist confirmation
6. Open the managed configuration JSON or plist
7. Add a managedMcpServers entry named m365 with the connector service URL and transport http
8. Set oauth.clientId to the Application (client) ID and oauth.tenantId to the Directory (tenant) ID
9. Set oauth.scope to the access_as_user offline_access scope string
10. Deploy the configuration through your device-management tool
11. Each user opens Customize > Connectors in Claude Desktop, selects Connect next to Microsoft 365, signs in on the tenant page, and consents
Sources: `third-party--claude-desktop--connectors-m365--part02` ### Set up the remote connector; `third-party--claude-desktop--connectors-m365--part02` ### Sign in as a user

**P2b** Local built-in connector declared in managedMcpServers with server set to microsoft365 — actor: admin, end-user; products: Claude Desktop on third-party inference
Preconditions: configuration managed through JSON or a plist directly; a local-mode app registration with its Application (client) ID and Directory (tenant) ID; microsoftAuthBroker required only where every device runs Claude Desktop 1.49585.0 or later; required is unsupported on Linux
1. Register a separate public client app for local mode in Entra (this directory only); do not reuse the remote connector's desktop client app
2. Under Authentication, add http://localhost, plus the per-platform broker redirect URI for brokered sign-in, under Mobile and desktop applications
3. Set Allow public client flows to Yes and Save
4. Add the Microsoft Graph delegated scopes under API permissions, select Grant admin consent, and note the Application (client) ID and Directory (tenant) ID
5. Open the managed JSON or plist configuration
6. Add a managedMcpServers entry with server set to microsoft365 and set name, clientId, and tenantId
7. Optionally set azureCloud, continuousAccessEvaluation, scope, and toolPolicy; do not mix url, transport, or command into a built-in entry
8. Set microsoftAuthBroker to auto, disabled, or required to choose between the device broker and the system browser
9. Deploy the configuration through your device-management tool
10. For brokered sign-in, meet the Windows or macOS device requirements (Entra join or MDM enrollment and compliance, Intune Company Portal and an Extensible SSO Redirect profile on macOS)
11. Each user opens Customize > Connectors in Claude Desktop and selects Connect on Microsoft 365
12. The user completes sign-in in the broker's account-picker dialog, or in the system browser when the broker is unavailable
Sources: `third-party--claude-desktop--connectors-m365--part03` ### Set up the local connector; `third-party--claude-desktop--connectors-m365--part04` ### How users sign in

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a, P1b; diff steps-differ, precondition-differs. Only the product's own settings are involved: an owner adds the connector org-wide on Team/Enterprise, or the user connects directly on Free/Pro/Max; the Entra tenant consent is assumed rather than walked through.
- Claude Desktop on third-party inference: documented; variants P1c, P1d, P2a, P2b; diff steps-differ, surface-differs, mechanism-differs, precondition-differs. Adds an Entra app-registration stage in third-party-admin, a choice of remote vs local connector, a managed-file alternative to in-app configuration, and Anthropic allowlisting on the remote path.
- Claude for Government: absent; variants —; diff absent. Referenced only indirectly: FedRAMP/GovCloud use a different connector app ID and hostname, and the local connector takes azureCloud us-gov-high or us-gov-dod, but no Gov-specific procedure is documented.
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- The microsoftAuthBroker record and the two brokered sign-in requirement records do not meet the task outcome on their own; they were folded into the local-connector variants as sub-options of the configuration and sign-in stages rather than misfiled, because the page presents them inside the same local-connector path. A stricter reading would drop the microsoftAuthBroker record as a configuration-key reference rather than a procedure.
- The local connector's optional toolPolicy field and explicit scope list restrict which tools members can invoke, which is T-023's outcome; that was kept as one optional step inside P2b instead of being split out as a T-023 record.
- The Phase 1 admin record's own outcome (connector added for the team with organization-wide permissions) also matches T-022; it is retained here because the page frames it as Phase 1 of this two-phase setup and the task outcome is only reached with Phase 2.
- P1b (Free/Pro/Max direct connect) rests on the Setup requirements prose and the Phase 2 record's notes, not a separately numbered procedure; it could instead be treated as a precondition note on P1a.
- No record says whether claude-web or claude-desktop differ from the undistinguished claude path, or whether claude-gov follows the same procedure with a different connector app ID.

## T-023 set connector tool policies for members  (product view)

Only the Microsoft 365 connector documents tool policy: an admin write-actions toggle on claude, managed-config scope and toolPolicy lists on third-party Desktop.

### P1 · admin-settings / click-through · Enable the Microsoft 365 connector's write actions for the organization (Entra consent, then connector configuration)

**P1a** Approve the write permission set in Entra, then turn write actions on in the connector configuration — actor: admin; products: Claude (claude.ai and Claude Desktop)
Preconditions: the Microsoft 365 connector is already added for the organization; the tenant's existing consent covers only read permissions; Microsoft Entra Global Administrator or Application Administrator role for the consent stage
1. Stage 1 (Entra admin center, one-time per tenant): open Enterprise applications
2. Approve the updated permission set covering mail, calendar, mailbox settings, and file writes
3. Stage 2: open the Microsoft 365 connector configuration
4. Turn write actions on for all users
5. Alternatively, enable write actions only for specific users with role-based access control (beta)
Sources: `connectors--microsoft--365` ## Write actions; `connectors--microsoft--365` ## Write actions

### P2 · filesystem / edit-file · Set the managedMcpServers entry's scope list (and toolPolicy) for the local Microsoft 365 connector

**P2a** List the exact delegated Graph scopes in the entry's scope field and keep the Entra app registration consent in sync — actor: admin; products: Claude Desktop on third-party inference
Preconditions: an existing Microsoft 365 managedMcpServers entry for the local connector; every scope listed must also be consented on the app registration from step 1; write tools need Claude Desktop 1.19367.0 or later; Teams write tools 1.24012.0 or later
1. List the delegated scopes you want in the entry's scope field; with no scope field the connector requests the standard read set
2. Narrow the read surface, or add any of the six optional read scopes, to change which read and search tools appear
3. Add the desired write scopes (Mail.Send, Mail.ReadWrite, Calendars.ReadWrite, Files.ReadWrite.All, MailboxSettings.ReadWrite, ChatMessage.Send, ChannelMessage.Send, Chat.Create) to expose a matching subset of write tools
4. Consent the same list on the app registration in Entra and keep the two lists in sync
5. Optionally set per-tool approval with toolPolicy, noting that allow resolves to ask for the send tools
6. Sign in again so the connector requests the new set
Sources: `third-party--claude-desktop--connectors-m365--part03` ### Configure scopes; `third-party--claude-desktop--connectors-m365--part03` ### Grant write scopes

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a; diff surface-differs, mechanism-differs, steps-differ. Admin flips a coarse read/write split in a UI (after one-time Entra consent); no per-tool selection beyond per-user RBAC.
- Claude Desktop on third-party inference: documented; variants P2a; diff surface-differs, mechanism-differs, steps-differ, precondition-differs. Policy is set in the managed configuration file at scope granularity, with per-tool toolPolicy on top; gated on Claude Desktop versions and on matching Entra app-registration consent.
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- P1a's Entra consent stage overlaps T-019 (set up the Microsoft 365 connector), whose outcome also covers tenant consent. Kept here because the text frames it as changing which tools members can invoke on an already-added connector rather than as initial setup, but a reviewer may prefer T-019.
- connectors--microsoft--365 never says where the 'Microsoft 365 connector configuration' screen lives, so P1a's surface (admin-settings) is inferred from the actor and the 'Organization settings > Connectors' path used earlier on the same page.
- The same page's Phase 1 step 5, 'Restrict user access or revoke specific permission scopes', reads like a third T-023 path but carries no steps and produced no record; unresolved whether it is a distinct family.
- No records for claude-web, claude-desktop, claude-gov, claude-tag, or cowork; the corpus does not say whether tool policies are merely undocumented there or unsupported.

## T-033 install a plugin  (product view)

Two install families: marketplace browse (Claude/Cowork only) and package-file upload (Claude and Government, with differing steps and device scope).

### P1 · app-settings / click-through · Install from a marketplace or catalog listing under Customize > Plugins

**P1a** Browse plugins in the default marketplace and Install (Cowork mode) — actor: end-user; products: Claude (claude.ai and Claude Desktop)
1. Open Customize in the sidebar, then Plugins
2. Select Browse plugins to see available plugins (default marketplace is Anthropic's official catalog)
3. Select a plugin and click Install
4. Sign in if the plugin includes a connector that needs authentication
Sources: `cowork--guide--plugins` ## Install a plugin

### P2 · app-settings / click-through · Install from a plugin package file under Customize > Plugins

**P2a** Upload option on the Plugins page (Cowork mode) — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: a plugin package file
1. Open Customize in the sidebar, then Plugins
2. Select the upload option on the Plugins page
3. Select the plugin package
Sources: `cowork--guide--plugins` ## Install a plugin

**P2b** Add plugin > Upload plugin, .zip with trust notice, installed on this device only — actor: end-user; products: Claude for Government
Preconditions: you have a plugin .zip file
1. Open Customize in the sidebar, then Plugins
2. Select Add plugin
3. Select Upload plugin
4. Choose the plugin's .zip file
5. Acknowledge the notice to install only plugins you trust
Sources: `government--desktop--plugins` ## Find and install plugins

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a, P2a; diff only-here. Only product documenting the marketplace-catalog install path (P1); the source names Cowork mode. File install is one sentence with no trust notice.
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P2b; diff steps-differ, precondition-differs. No public marketplace; file install goes through Add plugin > Upload plugin, requires a trust acknowledgement, and applies only on the current device.
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- Government documents a catalog install (Browse plugins > Organization tab, admin-provided plugins) but no record was extracted for it; it would belong in P1 as a Government variant with a precondition difference.
- No records for claude-desktop-3p or claude-tag; unclear whether the task is undocumented there or the relevant units were not extracted.

## T-034 add a plugin marketplace  (product view)

Both documented products register marketplaces from the Plugins page; only Claude documents repository URL forms and marketplace Update.

### P1 · app-settings / click-through · Register a marketplace from the Plugins page

**P1a** Add marketplace by Git repository URL (Cowork mode) — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: a Git repository containing plugin packages; GitHub or GitHub Enterprise, or a public GitLab or Bitbucket repository
1. Open Customize > Plugins
2. Select Add marketplace
3. Enter the repository URL as https://github.com/owner/repo or the owner/repo shorthand
4. Plugins defined in the repository appear alongside other marketplaces' plugins and install the same way
Sources: `cowork--guide--plugins` ## Use a Git repository as a marketplace

**P1b** Add your own marketplace from Browse plugins, subject to network controls — actor: end-user; products: Claude for Government
Preconditions: the deployment's network controls allow the marketplace to be downloaded; no public plugin marketplace exists in this deployment
1. Open Customize > Plugins
2. Select Browse plugins
3. Add a plugin marketplace of your own
Sources: `government--desktop--plugins` ## Where plugins come from

### P2 · app-settings / click-through · Refresh an already-registered marketplace

**P2a** Click Update on a marketplace to pull its latest plugins (Cowork mode) — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: the marketplace is already added
1. Open the Plugins page
2. Click Update on the marketplace to pull the latest plugins from its repository
Sources: `cowork--guide--plugins` ## Use a Git repository as a marketplace

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a, P2a; diff same, only-here. Only product documenting the URL and shorthand forms and the marketplace Update action; source names Cowork mode.
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1b; diff steps-differ, precondition-differs. Entry point is Browse plugins; no public marketplace, and network controls decide whether a marketplace can be downloaded.
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- Government names Browse plugins as the entry point but no fields; unclear whether it accepts the same repository URL forms as Cowork.
- Whether the marketplace limits and the Update action apply in Claude for Government is not stated.

## T-035 configure an installed plugin's components  (product view)

One click-through path: open the installed plugin under Customize > Plugins and toggle components. Documented only for claude and claude-gov.

### P1 · app-settings / click-through · Open the installed plugin under Customize > Plugins and toggle its components

**P1a** Open the installed plugin, review its components, turn them on or off (Cowork mode in the Cowork guide) — actor: end-user; products: Claude (claude.ai and Claude Desktop), Claude for Government
Preconditions: the plugin is already installed
1. Open Customize in the sidebar, then Plugins
2. Open the installed plugin to see the components it provides (skills, connectors/slash commands, agents or sub-agents, hooks)
3. Enable or disable individual components as needed
Sources: `cowork--guide--plugins` ## Install a plugin; `government--desktop--plugins` ## Manage installed plugins

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a; diff same. Cowork mode. Skills and agents appear as tabs; connectors and hooks have their own pages. Written as the third step of the install sequence.
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1a; diff terminology-only. Components listed as skills, slash commands, sub-agents, hooks; connectors declared by a self-added plugin are never added, so there are no connector components to toggle.
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- Whether the differing component lists (Cowork names connectors, Government names slash commands) are wording or a real capability gap; Government omits connectors because self-added plugin connectors never load.
- Neither page names the control used to toggle a component, so the final step cannot be verified at step granularity.

## T-037 remove a plugin  (product view)

One family: open the installed plugin and click Uninstall. Claude and Government differ only in preconditions; two products undocumented.

### P1 · app-settings / click-through · Open the installed plugin and click Uninstall

**P1a** Customize > Plugins > Uninstall (Cowork mode); org-managed plugins need an administrator — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: the plugin was installed by the user; organization-managed plugins can only be removed by an administrator
1. Open the plugin under Customize > Plugins
2. Click Uninstall
Sources: `cowork--guide--plugins` ## Update and remove plugins

**P1b** Uninstall from the installed plugin; removal sticks over admin auto-install, required plugins blocked — actor: end-user; products: Claude for Government
Preconditions: the plugin is not one your organization requires
1. Open the installed plugin
2. Click Uninstall
Sources: `government--desktop--plugins` ## Manage installed plugins

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a; diff same. Cowork mode page; entry point named as Customize > Plugins
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1b; diff precondition-differs. uninstall persists against admin auto-install; a required plugin cannot be removed
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- Neither source gives an admin-side procedure for removing an organization-distributed plugin; that may belong to T-040 rather than here.
- No removal procedure documented for Claude Desktop on third-party inference or Claude Tag.

## T-038 create a plugin with Claude  (product view)

Only Claude for Government documents Create with Claude; the plugin lands on that device only.

### P1 · app-settings / prompt-claude · Customize > Plugins, Create with Claude (app-settings, prompt-claude)

**P1a** Add plugin > Create with Claude, describe it, install the result — actor: end-user; products: Claude for Government
1. Open Customize > Plugins
2. Select Add plugin
3. Select Create with Claude
4. Describe the plugin you want
5. Install the plugin Claude builds
Sources: `government--desktop--plugins` ## Find and install plugins

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1a; diff only-here. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

## T-040 add a plugin for an organization  (product view)

Both documented products upload a plugin zip in an admin console; Government picks an install behavior, Claude Tag must attach the plugin to a bundle.

### P1 · admin-settings / click-through · Admin uploads a plugin archive on the Plugins card/page

**P1a** Config > Plugins card: drop the zip, then choose Auto-install or Members choose — actor: admin; products: Claude for Government
Preconditions: a plugin zip (a .claude-plugin/plugin.json manifest plus the skill folders under skills/); a skill distributed this way must contain only text files (.md, .txt, .json, .yaml, .yml, .csv)
1. Open the Config page in the admin portal
2. Open the Plugins card
3. Click Add plugins
4. Drop the zip
5. Check the preview showing the plugin's name, version, and description (a skills-only package is not marked Runs code)
6. Choose Auto-install to deliver it to every member, or Members choose to let members install it themselves
7. Optionally verify on a device: open Claude Desktop as a member, install it if you chose Members choose, and give Claude a task the skill should match
Sources: `government--desktop--skills` ## Building and deploying your own skills

**P1b** claude.ai/admin-settings/plugins: Add plugins > Upload a file, then attach to a bundle or scope — actor: admin; products: Claude Tag (Claude in Slack)
Preconditions: a .zip or .plugin archive of up to 200 MB laid out as a Claude Code plugin: a .claude-plugin/plugin.json manifest at the archive root with skills at skills/<name>/SKILL.md, the same layout inside one top-level folder, or a single top-level SKILL.md
1. Go to the Plugins page at claude.ai/admin-settings/plugins
2. Click Add plugins and choose Upload a file
3. Upload the .zip or .plugin archive (an archive with no manifest, more than one plugin.json, or a misplaced manifest is rejected at upload)
4. After upload the plugin is in the organization's catalog but attached nowhere
5. Toggle the plugin on in a bundle's Plugins tab, or add it directly on a scope, to make it available in channels
Sources: `claude-tag--admins--skills-repo` ## Upload a plugin as a zip file

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1a; diff steps-differ. Delivery is settled at upload time by an explicit install-behavior choice: Auto-install or Members choose. Distributed skills must be text-only.
- Claude Tag (Claude in Slack): documented; variants P1b; diff steps-differ, precondition-differs. Upload only puts the plugin in the org catalog; a second gate (toggle on in a bundle's Plugins tab, or add on a scope) is what makes it reach channels. 200 MB archive cap.

Open questions:
- Claude Tag's Sync from GitHub path sits in the same Add plugins menu and also ends with toggling plugins on in a bundle; whether that path should be a second variant here or stays under T-034/T-049 is unsettled by these records.
- Claude Tag documents no equivalent of Auto-install vs Members choose, so whether a Tag admin can force a plugin on members is unknown.
- No records for claude, claude-web, claude-desktop, claude-desktop-3p, or cowork; the absences may reflect pilot unit coverage rather than the products lacking the capability.

## T-042 find and enable a skill  (product view)

Only Claude for Government documents seeing the skill list and toggling a skill on or off.

### P1 · app-settings / click-through · Customize > Skills toggle list (app-settings, click-through)

**P1a** Open Customize > Skills and toggle a listed skill on or off — actor: end-user; products: Claude for Government
1. Open Customize in the sidebar
2. Open Skills
3. Turn a listed skill on or off
Sources: `government--desktop--skills` ## Create and manage skills

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1a; diff only-here. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

## T-043 create a skill in the product  (product view)

Only Claude for Government documents creating a skill in-product: Add skill under Customize > Skills, or asking Claude mid-task.

### P1 · app-settings / click-through · Add skill in Customize > Skills

**P1a** Add skill, then Create with Claude or Write skill instructions — actor: end-user; products: Claude for Government
1. Open Customize in the sidebar, then Skills
2. Select Add skill
3. Choose Create with Claude to build one with Claude's help, or Write skill instructions to write it yourself
Sources: `government--desktop--skills` ## Create and manage skills

### P2 · chat / prompt-claude · Ask Claude to save the current workflow as a skill

**P2a** Save a workflow as a skill mid-task — actor: end-user; products: Claude for Government
1. While working on a task, ask Claude to save the workflow as a skill
Sources: `government--desktop--skills` ## Create and manage skills

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1a, P2a; diff only-here. Skills created here are stored on the user's device, so they are available only there.
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- The same paragraph's Upload a skill option belongs to T-044; whether it was extracted under that task cannot be settled from here.
- The Building and deploying section mentions having Claude draft a skill in a Cowork task; whether Cowork documents a real in-product creation path needs Cowork units, not readable from this task's records.

## T-044 upload or import a skill  (product view)

Only Claude for Government documents uploading an existing skill file into the member's skill list.

### P1 · app-settings / click-through · Customize > Skills, Add skill upload (app-settings, click-through)

**P1a** Add skill > Upload a skill, then add the skill file you have — actor: end-user; products: Claude for Government
Preconditions: a skill file the user already has
1. Open Customize > Skills
2. Select Add skill
3. Choose Upload a skill
4. Add the skill file you have
Sources: `government--desktop--skills` ## Create and manage skills

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1a; diff only-here. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

## T-047 manage your skills  (product view)

Only Claude for Government documents renaming or deleting a skill you created, stored on that device.

### P1 · app-settings / click-through · Customize > Skills, open a skill you created (app-settings, click-through)

**P1a** Open a skill you created and rename or delete it — actor: end-user; products: Claude for Government
Preconditions: the skill was created by this user
1. Open Customize > Skills
2. Open a skill you created
3. Rename or delete it
Sources: `government--desktop--skills` ## Create and manage skills

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1a; diff only-here. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

## T-048 distribute skills to an organization  (product view)

Only Claude for Government documents org skill distribution, and only indirectly through an auto-installed plugin.

### P1 · admin-settings / click-through · Plugins card auto-install in the Gov admin portal (admin-settings, click-through)

**P1a** Bundle skills in a plugin, add it on the Plugins card, set Auto-install — actor: admin; products: Claude for Government
Preconditions: the admin portal has no skills view or per-skill controls
1. Bundle the skills in a plugin, as small as the skill plus a plugin manifest
2. Add the plugin on the Plugins card
3. Set the plugin to Auto-install so its skills reach every member
4. To change or retire the skill later, update or remove the plugin
Sources: `government--desktop--skills` ## Skills for administrators

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1a; diff only-here. 
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

## T-049 set up a skills repository with auto-sync  (product view)

Only Claude Tag documents a git-backed skills marketplace with auto-sync and Claude write access via an Access bundle.

### P1 · admin-settings / click-through · claude.ai admin Plugins page, Sync from GitHub (admin-settings, click-through)

**P1a** Create a private marketplace repo, sync it, grant repo access in a bundle, attach plugins — actor: admin; products: Claude Tag (Claude in Slack)
Preconditions: a private or internal GitHub repository laid out as a Claude Code plugin marketplace with .claude-plugin/marketplace.json at the root; for a github.com repository, the GitHub connector must be enabled for the organization; the Claude GitHub App must already be linked to the GitHub organization; the repository archive must be no larger than 512 MiB
1. Create a private or internal GitHub repository laid out as a Claude Code plugin marketplace, with .claude-plugin/marketplace.json at the root and one folder per plugin
2. Fork a public repository into a private one first, since a public repository cannot be selected
3. Go to the Plugins page at claude.ai/admin-settings/plugins
4. Click Add plugins and choose Sync from GitHub
5. Select the repository, leave Sync automatically on, and click Create
6. Open an Access bundle and go to its Repositories tab
7. Add the repository to the bundle
8. In the same bundle's Plugins tab, toggle on the plugins from the new marketplace
Sources: `claude-tag--admins--skills-repo` ## Set up the skills repository

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): documented; variants P1a; diff only-here. 

## T-050 prompt Claude to propose skill updates  (product view)

Only Claude Tag documents prompting Claude to open skill pull requests; Claude never opens them unprompted.

### P1 · chat / prompt-claude · Ask @Claude in a Slack channel (chat, prompt-claude)

**P1a** Ask @Claude in the channel to open a PR to the skills repo, then merge it — actor: admin; products: Claude Tag (Claude in Slack)
Preconditions: the skills repository is set up and Claude has write access to it
1. In the channel, mention @Claude and ask it to open a PR to the skills repo so the skill includes what it just learned
2. Or ask @Claude to set a recurring routine that reviews the channel's corrections and opens one PR with the fixes
3. Review, edit, or close the pull request like any contributor's
4. Merge the PR so the updated plugin syncs to the organization
Sources: `claude-tag--admins--skills-repo` ## Prompt Claude to propose updates

Cells:

- Claude (claude.ai and Claude Desktop): absent; variants —; diff absent. 
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: absent; variants —; diff absent. 
- Claude Tag (Claude in Slack): documented; variants P1a; diff only-here. 

## T-070 browse the plugin directory  (product view)

Two documented paths: Claude for Government's in-product Organization tab, and the public claude.com/plugins directory site; five products undocumented.

### P1 · app-settings / click-through · Browse the in-product plugin catalog under Customize > Plugins

**P1a** Organization tab as the catalog (no public marketplace) — actor: end-user; products: Claude for Government
Preconditions: administrators have added plugins for the organization
1. Open Customize in the sidebar
2. Open Plugins
3. Review the installed plugins listed under Organization plugins
4. Select Browse plugins
5. Open the Organization tab, which lists every plugin administrators have made available
Sources: `government--desktop--plugins` ## Find and install plugins

### P2 · web-portal / click-through · Browse the public plugin directory site

**P2a** Open claude.com/plugins and browse the open-sourced collection — actor: end-user; products: Claude (claude.ai and Claude Desktop)
1. Open claude.com/plugins
2. Browse the full collection of open-sourced plugins and what each one does
Sources: `plugins--overview` ## Plugin directory

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P2a; diff surface-differs, steps-differ. The directory is an external website rather than an in-product catalog; the overview's table of 11 plugins is descriptive, the action is the link out.
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1a; diff surface-differs, steps-differ, precondition-differs. No public plugin marketplace; the Organization tab under Browse plugins is the catalog, and it lists nothing until administrators add plugins.
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- The plugins--overview record is filed to the undistinguished 'claude' product, but its directory link points at claude.com/plugins-for/cowork; the unit has no product-scoped wording to settle whether the cell belongs to cowork.
- Whether Cowork or the Claude apps expose their own in-product Browse plugins catalog (a P1 sibling) is not documented in either unit, so those absences may be coverage gaps rather than real ones.

## T-073 verify an uploaded skill works in the product  (product view)

Both documented cells confirm a skill by prompting Claude, but differ in actor, enabling gate, and how the skill reached the account.

### P1 · chat / prompt-claude · Give Claude a matching task and confirm the skill loads

**P1a** Enable in Customize > Skills, prompt, read Claude's thinking, iterate the description — actor: end-user; products: Claude (claude.ai and Claude Desktop)
Preconditions: the skill has been uploaded to the account
1. Enable the skill in Customize > Skills
2. Try prompts that should trigger it
3. Review Claude's thinking to confirm it is loading the skill
4. Iterate on the description if Claude is not using it when expected
Sources: `skills--how-to` ### After uploading

**P1b** Check a plugin-delivered skill on a member device after the admin upload — actor: admin; products: Claude for Government
Preconditions: the skill is packaged in a plugin and added on the admin portal Plugins card; if the admin chose Members choose, the plugin must be installed on the device first
1. Open Claude Desktop as a member
2. Install the plugin if you chose Members choose
3. Give Claude a task the skill should match
4. Confirm Claude picks it up
5. To change the skill later, update the plugin
Sources: `government--desktop--skills` ## Building and deploying your own skills

Cells:

- Claude (claude.ai and Claude Desktop): documented; variants P1a; diff actor-differs, steps-differ, precondition-differs. self-uploaded skill: the user enables it in Customize > Skills, then prompts and inspects Claude's thinking
- Claude Desktop on third-party inference: absent; variants —; diff absent. 
- Claude for Government: documented; variants P1b; diff actor-differs, steps-differ, precondition-differs. admin verifies a plugin-delivered skill on a device; the upload checks packaging, not skill content, so a malformed SKILL.md only shows up here
- Claude Tag (Claude in Slack): absent; variants —; diff absent. 

Open questions:
- The claude-gov record is tagged actor admin while its steps say to open Claude Desktop 'as a member'; the text does not say whether the admin verifies on their own device or asks a member, so P1b may be a two-actor path.
- Whether P1a's first step (enable in Customize > Skills) belongs to T-042 rather than here could not be settled from the source; it was kept because it opens the same numbered list that ends in a confirmed trigger.
- No records for claude-web, claude-desktop, claude-desktop-3p, claude-tag, or cowork; the reads could not distinguish pages that genuinely omit a verification step from units absent in the pilot corpus.

## T-039 package a plugin archive  (builder view)

Only Claude for Government documents plugin packaging: a hand-built zip, or the same layout assembled by Claude in a Cowork task.

### P1 · filesystem / edit-file · Lay out .claude-plugin/plugin.json plus skills/ by hand and zip it

**P1a** Hand-assembled plugin zip for admin portal upload — actor: admin; products: Claude for Government
Preconditions: a written skill folder containing SKILL.md; skill holds only text files (.md, .txt, .json, .yaml, .yml, .csv) or the portal upload is rejected
1. Create .claude-plugin/plugin.json with name and version, plus a description
2. Place each skill folder under skills/, one folder per skill
3. Zip the plugin contents, or the wrapping plugin folder itself
Sources: `government--desktop--skills` ## Building and deploying your own skills

### P2 · chat / prompt-claude · Ask Claude to assemble and zip the plugin

**P2a** Assembly in a Cowork mode task, layout pasted into the request — actor: admin; products: Claude for Government
Preconditions: Cowork tasks available in your deployment; the layout and the full Plugin archive formats rules must be pasted in, since Claude Desktop in Claude for Government has no packaging skill
1. Open a Cowork task
2. Give Claude the plugin layout
3. Paste in the full rules from Plugin archive formats
4. Ask Claude to arrange the files and produce the zip
Sources: `government--desktop--skills` ## Building and deploying your own skills


Open questions:
- Reversed the record's product override from claude back to claude-gov. The Cowork sentence sits inside the Claude for Government page and is scoped to that deployment: skills can be drafted in a Cowork task 'where those are available in your deployment', and the packaging paragraph ends 'Claude Desktop in Claude for Government does not include a packaging skill, so put the layout in your request'. Cowork here names a mode inside the Gov deployment, not a generic Claude page. If the pilot rule is that any Cowork mention means product claude regardless of host deployment, P2a moves to the claude cell and claude-gov loses only-here.
- Whether generic Claude or plugin-authoring docs elsewhere in the corpus document a packaging path that was not extracted into this task; that would change claude from absent.

## T-041 submit a plugin to the plugin directory  (builder view)

One page documents plugin directory submission on claude: an admin-settings form for Team/Enterprise orgs and a Console web-portal form for individuals.

### P1 · admin-settings / click-through · Submit via the claude.ai in-app form in organization Directory settings

**P1a** Team/Enterprise org with directory management access submits the public GitHub link — actor: developer; products: Claude (claude.ai and Claude Desktop)
Preconditions: the plugin repo is public on GitHub; closed-source plugins are not accepted; signed in to a claude.ai Team or Enterprise organization with directory management access (Organization Owners have it by default; on Enterprise an Owner can delegate it through a custom role); the plugin complies with the Anthropic Software Directory Terms and Policy
1. Run `claude plugin validate` to check formatting and structure
2. Sign in to claude.ai with directory management access
3. Open https://claude.ai/admin-settings/directory/submissions/plugins/new
4. Share the GitHub link to your plugin in the submission form
5. Submit the form and wait for review
6. Track review status on the Directory page at claude.ai/admin-settings/directory/submissions
Sources: `plugins--submit` ### Before you start

### P2 · web-portal / click-through · Submit via the Console submission form at platform.claude.com

**P2a** Individual author outside a Team/Enterprise org submits from Console — actor: developer; products: Claude (claude.ai and Claude Desktop)
Preconditions: the plugin repo is public on GitHub; closed-source plugins are not accepted; a Developer, Admin, or Owner role on a Console organization; the plugin complies with the Anthropic Software Directory Terms and Policy
1. Run `claude plugin validate` to check formatting and structure
2. Sign up for Console at platform.claude.com if you are not part of a claude.ai Team or Enterprise organization
3. Open https://platform.claude.com/plugins/submit
4. Share the GitHub link to your plugin in the submission form
5. Submit the form and wait for review
Sources: `plugins--submit` ### Before you start


Open questions:
- Console is a separate web portal, not a listed product; both paths are filed under `claude` because the taxonomy has no Console product id.
- The directory serves Cowork and Claude Code users, but no Cowork-side submission procedure exists, so the cowork cell is marked absent rather than sharing the claude cell.

## T-045 test a skill before distributing it  (builder view)

No documented procedure: the only candidate validates the package statically and never exercises the skill against a matching task.


Misfiled records (excluded):
- `skills--how-to` ### Before uploading: outcome not met: the steps are static file review plus a skills-ref validate run; Claude is never given a task the skill should match, so nothing confirms the skill triggers. The adjacent '### After uploading' block is the section that exercises the skill, and it runs after upload (T-073). → NEW (validate a skill package before upload) or T-071

## T-057 prepare a connector for directory review  (builder view)

Connector review prep is documented only for undistinguished Claude: privacy policy files, carousel asset specs, and a pre-submission checklist plus plugin validate.

### P1 · filesystem / edit-file · Add the required privacy policy disclosures to the connector's files

**P1a** README section plus privacy_policies array in manifest.json (local connectors) — actor: developer; products: Claude (claude.ai and Claude Desktop)
Preconditions: local connector; manifest_version 0.2+
1. Add a "Privacy Policy" section to README.md
2. Add a privacy_policies array to manifest.json
3. Point the entries at HTTPS privacy policy URLs
4. Cover data collection, usage and storage, third-party sharing, retention, and contact information
Sources: `connectors--building--submission` ## Privacy policy requirements

### P2 · filesystem / other · Produce directory assets to the published specifications

**P2a** Carousel screenshots and paired prompt text (MCP Apps) — actor: developer; products: Claude (claude.ai and Claude Desktop)
Preconditions: submitting an MCP App
1. Capture three to five PNG screenshots at least 1000px wide
2. Crop each to the app response only, leaving out the prompt
3. Provide the prompt text separately for each screenshot
4. Optionally start from the Anthropic MCP Apps Figma community carousel template
Sources: `connectors--building--submission` ### Carousel screenshots (MCP Apps)

### P3 · terminal / command · Run the pre-submission checklist and validate before filing

**P3a** Pre-submission checklist, plus claude plugin validate for plugins — actor: developer; products: Claude (claude.ai and Claude Desktop)
1. Run the pre-submission checklist from the review criteria page
2. For plugins, run claude plugin validate
3. Submit only after both pass
Sources: `connectors--building--submission` ## Review process


Open questions:
- The substantive checklist lives on connectors/building/review-criteria, from which no record was extracted; P3a may be a one-line stub for a much larger procedure on that page.
- The 'Submission requirements' list (security, tool annotations, OAuth, documentation) is stated as criteria with no actions, so nothing here covers the tool-design or prompt-injection preparation the task definition names.
- No record covers preparing reviewer test credentials, although the task outcome names them.
- Whether carousel asset preparation (P2a) belongs here or with T-058, since the assets are attached inside the submission portal, could not be settled from the page text.

## T-058 submit a connector to the directory  (builder view)

One web-portal click-through family on `claude`: org-settings portal for remote servers and MCP Apps, separate form for MCPB desktop extensions.

### P1 · web-portal / click-through · File the connector through an Anthropic submission form on the web

**P1a** Remote MCP servers (including MCP Apps): multi-step submission portal in organization settings on Claude.ai — actor: developer; products: Claude (claude.ai and Claude Desktop)
Preconditions: a Team or Enterprise organization (the portal is part of organization settings); directory management access: Owner or Primary owner, or on Enterprise a custom role carrying the Directory or Libraries permission; documentation URL, privacy policy URL, icon, support contact, and test account credentials ready; 3-5 carousel screenshots if submitting an MCP App; the server is remote and served over https:// (the portal accepts remote MCP servers only)
1. Open the submission portal at claude.ai/admin-settings/directory/submissions/new in your organization's settings
2. Read the Introduction step on what a directory listing does and does not do
3. In Connection, confirm the https:// server URL, the transport (streamable HTTP or SSE), and whether users reach the server by Universal URL, Multiple URLs, or a URL pattern
4. In Tools, let tools, prompts, and resources sync, and fix on your server any tools flagged for missing titles or annotations
5. In Listing, enter server name, tagline, description, one to five categories, documentation and privacy policy URLs, support contact, icon, and the permanent URL slug
6. In Use cases, describe the primary use cases, what users need before connecting, and whether the connector reads, writes, or both
7. In Company, give company name and website plus a primary contact for review updates
8. In Authentication, choose OAuth, a custom connection, or no authentication, within the limits the Connection choice imposes
9. In Data handling, state whether the API is your own, proxied with permission, or a third party's, and whether health data or sponsored content is involved
10. In Test & launch, give reviewer test-account setup and access instructions and confirm you ran every tool via MCP Inspector or as a custom connector in Claude
11. In Compliance, give all seven policy acknowledgments
12. Read through the Review step, note any quality warnings, and submit
Sources: `connectors--building--submission` ### What to expect in the portal; `connectors--building--submission` ## Before you start; `connectors--building--submission` ## Submit your connector

**P1b** Desktop extensions (MCPB): separate submission form, no portal or organization access — actor: developer; products: Claude (claude.ai and Claude Desktop)
Preconditions: the local MCP server is packaged as an MCP Bundle (.mcpb); privacy policy section in README.md, a privacy_policies array in manifest.json (manifest_version 0.2+), and HTTPS privacy policy URLs; no portal or organization access required
1. Open the desktop extension submission form at clau.de/desktop-extention-submission
2. File the desktop extension through that form
Sources: `connectors--building--submission` ## Submit your connector; `connectors--building--submission` ## Before you start; `connectors--building--submission` ## Privacy policy requirements


Open questions:
- The MCPB form's own steps and how directory terms are accepted there are not documented in the corpus; only the entry link is given, so P1b's outcome rests on the routing sentence.
- Whether MCPB submission is genuinely client-specific (Claude Desktop) rather than product-wide cannot be settled from this unit alone, now that claude.ai and Claude Desktop are one product.
- Plugin submission (/docs/plugins/submit) is referenced as the route for skills but lies outside this unit; not checked here.

## T-059 use the submissions dashboard  (builder view)

Only the generic connector submission page documents tracking review status; post-publication metrics live on the listing page.

### P1 · web-portal / click-through · Submissions dashboard in claude.ai org settings (web-portal, click-through)

**P1a** Open the submissions dashboard, read status and reviewer feedback — actor: developer; products: Claude (claude.ai and Claude Desktop)
Preconditions: a submission has been filed
1. Open the submissions dashboard at claude.ai/admin-settings/directory/submissions
2. Read the submission's status and any reviewer feedback
3. Email mcp-review@anthropic.com for escalations
Sources: `connectors--building--submission` ## Review process


## T-067 allowlist external link destinations for an MCP App  (builder view)

Only the generic connector submission page documents declaring link targets to suppress the external-link confirmation prompt.

### P1 · web-portal / click-through · Allowed link URIs field in the submission portal (web-portal, click-through)

**P1a** List each owned HTTPS origin or custom URI scheme with the submission — actor: developer; products: Claude (claude.ai and Claude Desktop)
Preconditions: the connector uses the ui/open-link capability; every origin or scheme listed is owned by the submitting organization
1. List with your submission every link target your server will request
2. Give each as an HTTPS origin such as https://example.com, listing each subdomain separately
3. Or give a custom URI scheme such as myapp: for deep links into a native app you own
4. Leave out any third-party domain or URI scheme you do not publish
Sources: `connectors--building--submission` ## Allowed link URIs


## T-071 author a skill package on disk  (builder view)

Both products author a skill folder holding SKILL.md on disk; government restricts the folder to text files for admin-portal distribution.

### P1 · filesystem / edit-file · Create a skill directory with SKILL.md and its supporting files

**P1a** Full skill directory: SKILL.md plus references/, assets/, scripts/ — actor: developer; products: Claude (claude.ai and Claude Desktop)
1. Create a directory whose name matches the skill's name field
2. Create SKILL.md inside it
3. Start SKILL.md with YAML frontmatter containing name (lowercase letters, numbers, hyphens, max 64 characters) and description (max 1,024 characters)
4. Write the markdown body with step-by-step procedures, examples, templates, and edge cases, keeping it under 500 lines
5. Put detailed documentation in references/, templates and data in assets/, and executable Python, JavaScript/Node.js, or Bash code in scripts/
6. Reference those files from SKILL.md so Claude knows when to load them
7. Declare Python or npm dependencies in the frontmatter dependencies field
Sources: `skills--how-to` ## Creating a `SKILL.md` file

**P1b** Text-only skill folder intended for admin-portal distribution — actor: admin; products: Claude for Government
Preconditions: the skill will be distributed through the admin portal, which accepts only text files
1. Create a folder named after the skill
2. Add a SKILL.md file starting with YAML frontmatter carrying name and description
3. Write the instructions as markdown after the frontmatter
4. Make the folder name match the name in the frontmatter
5. Keep contents to text files only: .md, .txt, .json, .yaml, .yml, .csv
6. If Claude hands back a .skill file, keep the folder it came from instead
Sources: `government--desktop--skills` ## Building and deploying your own skills


Open questions:
- The government page links out to the generic authoring guide, so whether claude-gov authors may use references/, assets/, and scripts/ for locally created (undistributed) skills is implied but never given as steps.
- No record documents on-disk skill authoring for claude-web, claude-desktop, claude-desktop-3p, claude-tag, or cowork; those absences may reflect corpus coverage rather than a real product gap.

## T-072 package a skill for distribution  (builder view)

Only the generic skill authoring guide documents zipping a skill folder, with the directory inside the ZIP root.

### P1 · filesystem / edit-file · Zip the skill folder on disk (filesystem, edit-file)

**P1a** Match the directory name to the skill name and zip the directory itself — actor: developer; products: Claude (claude.ai and Claude Desktop)
Preconditions: a skill directory with SKILL.md exists
1. Ensure the directory name matches the skill's name field
2. Create a ZIP file containing the skill directory, not its files at the ZIP root
Sources: `skills--how-to` ## Packaging your skill


