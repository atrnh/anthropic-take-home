## Cowork — general guide

Use these instructions in Cowork. Plugins are not used in Chat.

Install plugins only from sources you trust. Review a plugin's contents,
permissions, connected services, and data access before installing it. See
[plugin security guidance](https://claude.com/docs/plugins/submit#security).

A plugin can contain skills, connectors, agents, commands, and hooks. Hooks can
run scripts during a session. A connector may require you to sign in before
Claude can use it.

### Install from a marketplace {#cowork-marketplace}

Use this method to browse a marketplace already available in Cowork.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select **Browse plugins**. The default marketplace is Anthropic's official catalog.
3. Select a plugin and choose **Install**.
4. If a bundled connector asks you to sign in, complete the sign-in.
5. Open the installed plugin to inspect its components. Enable or disable individual components as needed.

The plugin is installed and you can inspect what it provides. Installation does
not replace any sign-in required by its connectors.

### Install from a Git marketplace {#cowork-git}

Use this method when someone has shared a repository of plugins with you. Cowork
supports GitHub, including GitHub Enterprise, and public GitLab and Bitbucket
repositories.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select **Add marketplace** and enter the repository URL. For GitHub, you can also enter `owner/repo`.
3. Select **Browse plugins** and find the plugin from the added marketplace.
4. Select the plugin and choose **Install**.
5. If a bundled connector asks you to sign in, complete the sign-in.
6. Open the installed plugin to inspect its components. Enable or disable individual components as needed.

The repository's plugins appear alongside plugins from other marketplaces, and
the plugin you selected is installed.

### Install from a file {#cowork-file}

Use this method when someone has shared a plugin package with you. Check the
[package limits](https://claude.com/docs/cowork/guide/plugins#limits) before uploading it.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select the upload option and choose the plugin package.
3. Open the installed plugin to inspect its components. Enable or disable individual components as needed.

The plugin appears in your installed plugins. Check its connectors for any
sign-in they require before using their tools.

### Plugins your organization requires {#cowork-required}

On Team and Enterprise plans, required plugins install automatically. A required
plugin shows **This plugin is required by your organization**, and you cannot
remove it. You do not need to install it yourself.

### Next steps {#cowork-next}

- [Update or remove a plugin](https://claude.com/docs/cowork/guide/plugins#update-and-remove-plugins).
- [Provision plugins for an organization](https://claude.com/docs/cowork/3p/extensions).
- [Submit a plugin to the public directory](https://claude.com/docs/plugins/submit).
