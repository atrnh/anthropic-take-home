---
label: Claude Desktop (Government)
---

Use these instructions in Claude Desktop when your organization provides
Claude for Government. Plugins your administrators set to install automatically
are already installed.

<aside class="callout" aria-label="Connector and local server restrictions" markdown="1">

**Plugin connectors and local servers don't run**

Connectors declared by a plugin you add yourself are not added to Claude Desktop.
Your administrators provide connectors separately under **Customize**, then
**Connectors**.

[Local MCP servers](https://claude.com/docs/connectors/overview) declared by a
plugin never run.

</aside>

### Install a plugin your organization provides {#government-organization}

Use this method for plugins your administrators make available.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Look under **Organization plugins** to see which plugins are already installed.
3. If the plugin you want isn't listed, select **Browse plugins**, open the
   **Organization** tab, and install it.

The plugin is listed under **Organization plugins**. To turn individual components
on or off, open the plugin there.

### Install from a file {#government-file}

Use this method when someone has shared a plugin package with you. Install only
plugins you trust: uploaded plugins are not controlled by Anthropic. A plugin you
upload is added only on the device you are using.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select **Add plugin**, then **Upload plugin**.
3. Choose the plugin's `.zip` file. Review the trust notice and follow its
   instructions to finish the upload.

The plugin is installed on this device. Open it to review its components and turn
individual components on or off. Its declared connectors are not added; use the
connectors your administrators provide.

### Other ways to get plugins {#government-other}

Claude for Government does not include a public plugin marketplace. You can add
a marketplace of your own from **Browse plugins**, but your deployment's network
controls determine whether it can be downloaded. You can also ask Claude to
create a plugin with you. See
[where plugins come from](https://claude.com/docs/government/desktop/plugins#where-plugins-come-from).

### Next steps {#government-next}

- [Update or remove a plugin](https://claude.com/docs/government/desktop/plugins#manage-installed-plugins).
- [Create a plugin with Claude](https://claude.com/docs/government/desktop/plugins#find-and-install-plugins).
- [Provision plugins for an organization](https://claude.com/docs/government/config/plugins-and-connectors).
