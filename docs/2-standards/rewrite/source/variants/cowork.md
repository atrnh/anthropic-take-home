---
label: Claude Desktop (General)
default: true
---

Use these instructions in Claude Desktop.

<aside class="callout" aria-label="Plugin security" markdown="1">

**Before you install**

Install plugins only from sources you trust. Review a plugin's contents,
permissions, connected services, and data access before installing it. See
[plugin security guidance](https://claude.com/docs/plugins/submit#security).

</aside>

### Install from a marketplace {#cowork-marketplace}

Use this method to install a plugin from a marketplace already available in Claude Desktop.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Under the **Discover** tab, you'll see curated plugin recommendations from Anthropic's
   official catalog and other partners.
3. Select a plugin to open it and inspect its components. Click **Add** to install it.
4. If a bundled connector asks you to sign in, complete the sign-in.
5. Open the installed plugin to inspect its components. Enable or disable individual components as needed.

The plugin you installed will be listed in the **Yours** tab.

### Install from a Git marketplace or URL {#cowork-git}

Use this method when someone has shared a repository of plugins with you. Cowork
supports GitHub, including GitHub Enterprise, and public GitLab and Bitbucket
repositories.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Open the **Add** dropdown and select **Add marketplace**.
3. In the **Add marketplace** window that appears, select **Add from a repository**.
4. Under **URL**, enter the repository URL. For GitHub, you can also enter `owner/repo`.
5. Click **Sync** to add the marketplace and sync its plugins.
6. This should take you to a list of the marketplace's plugins. Select a plugin to open it
   and inspect its components. Click **Add** to install it.
7. If a bundled connector asks you to sign in, complete the sign-in.
8. Open the plugin to inspect its components. Enable or disable individual components as needed.

The repository's plugins appear alongside plugins from other marketplaces. The plugin you
installed will be listed in the **Yours** tab.

### Install from a file {#cowork-file}

Use this method when someone has shared a plugin package with you. To do this, you will
need to upload the plugin package. Check the [package
limits](https://claude.com/docs/cowork/guide/plugins#limits) before uploading it.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Open the **Add** dropdown and select **Upload a plugin**.
3. Select the plugin package to upload, then click **Upload**.
4. Open the installed plugin to inspect its components. Enable or disable individual components as needed.

The plugin you installed will be listed in the **Yours** tab.

### Next steps {#cowork-next}

- [Update or remove a plugin](https://claude.com/docs/cowork/guide/plugins#update-and-remove-plugins).
- [Provision plugins for an organization](https://claude.com/docs/cowork/3p/extensions).
- [Submit a plugin to the public directory](https://claude.com/docs/plugins/submit).
