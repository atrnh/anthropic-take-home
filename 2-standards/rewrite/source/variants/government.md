---
label: Claude Desktop (Government)
---

Use these instructions in Claude Desktop when your organization provides
Claude for Government.

<aside class="callout" aria-label="Connector and local server restrictions" markdown="1">

**Before you install**

Local MCP servers included in a plugin will never run, even for plugins you install
yourself.

Connectors declared by a plugin you add yourself are not added to Claude Desktop.
Your administrators provide connectors separately under **Customize**, then
**Connectors**.

</aside>

### Install a plugin your organization provides {#government-organization}

Use this method for plugins your administrators make available. Plugins set to
install automatically are already installed.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Check **Organization plugins** to see which plugins are already installed.
3. If the plugin is not installed, select **Browse plugins**, open the **Organization** tab, and install the plugin your administrators have made available.
4. Open the installed plugin to inspect its components. Turn individual components on or off as needed.

The plugin is listed under **Organization plugins**.

### Install from a file {#government-file}

Use this method when someone has shared a plugin package with you. Install only
plugins you trust: uploaded plugins are not controlled by Anthropic. A plugin you
upload is added only on the device you are using.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select **Add plugin**, then **Upload plugin**.
3. Choose the plugin's `.zip` file. Review the trust notice and follow its instructions to finish the upload.
4. Open the installed plugin to inspect its components. Turn individual components on or off as needed.

The plugin is installed on this device. Its declared connectors are not added;
use the connectors your administrators provide separately.

### Next steps {#government-next}

- [Create a plugin with Claude](https://claude.com/docs/government/desktop/plugins#find-and-install-plugins).
- [Manage installed plugins](https://claude.com/docs/government/desktop/plugins#manage-installed-plugins).
- [Distribute plugins to an organization](https://claude.com/docs/government/config/plugins-and-connectors).
