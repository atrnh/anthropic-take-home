## Cowork — Claude for Government

Use these instructions in Claude Desktop when your organization provides
Claude for Government.

Plugins add skills, commands, agents, and hooks. Hooks run on your device.
Connectors declared by a plugin you add yourself are not added to Claude Desktop,
and a local MCP server declared by a plugin never runs. Your administrators
provide connectors separately under **Customize**, then **Connectors**.

### Install a plugin your organization provides {#government-organization}

Installing a plugin does not add its bundled connectors. Your administrators
provide connectors separately.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Check **Organization plugins** to see the organization plugins already installed.
3. If the plugin is not installed, select **Browse plugins**, then the **Organization** tab.
4. Find the plugin your administrators have made available and install it.
5. Open the installed plugin to inspect its components. Turn individual components on or off as needed.

The plugin appears under **Organization plugins**. If your administrators set it
to install automatically, it is already installed and you do not need to install
it again.

### Install from a file {#government-file}

Install only plugins you trust. Uploaded plugins are not controlled by Anthropic.
A plugin you upload is added only on the device you are using. Its bundled
connectors are not added, and its declared local MCP servers do not run.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select **Add plugin**, then **Upload plugin**.
3. Choose the plugin's `.zip` file. Claude Desktop displays a notice about trusting uploaded plugins.
4. Open the installed plugin to inspect its skills, commands, agents, and hooks. Turn individual components on or off as needed.

The plugin is installed on this device. Its declared connectors are not added;
use the connectors your administrators provide separately.

### Looking for a marketplace? {#government-marketplace}

Claude for Government does not include a public plugin marketplace. You can add
your own from **Browse plugins**, but your organization's network controls
determine whether it can be downloaded. Ask your administrator which marketplace
you can use and how to add it.

### Next steps {#government-next}

- [Create a plugin with Claude](https://claude.com/docs/government/desktop/plugins#find-and-install-plugins).
- [Manage installed plugins](https://claude.com/docs/government/desktop/plugins#manage-installed-plugins).
- [Distribute plugins to an organization](https://claude.com/docs/government/config/plugins-and-connectors).
