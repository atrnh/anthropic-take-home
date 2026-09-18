---
label: Claude Desktop (General)
default: true
---

Use these instructions in Claude Desktop unless your organization provides Claude
for Government.

On Team and Enterprise plans, your installation may already include plugins
from your administrators. Follow this guide to install more.

<aside class="callout" aria-label="Plugin security" markdown="1">

**Install only plugins you trust**

Review a plugin's components before you install it. Connectors give Claude access
to external services, and hooks run scripts at defined points in a session.
You can open a marketplace plugin before installing it. An uploaded plugin is
installed when you upload it, so review the package's contents first. See
[plugin security guidance](https://claude.com/docs/plugins/submit#security).

</aside>

### Install from a marketplace {#cowork-marketplace}

Use this method to install a plugin from a marketplace already available in Claude Desktop,
including Anthropic's official marketplace.

1. Open **Customize** in the sidebar, then **Plugins**.
2. On the **Discover** tab, select a plugin to open it and review its components.
3. Click **Add** to install it.
4. If a bundled connector asks you to sign in, complete the sign-in.

The plugin is listed on the **Yours** tab. To turn individual components on or off,
open the plugin there.

### Install from a Git repository {#cowork-git}

Use this method when someone has shared a repository of plugins with you. Claude
Desktop supports GitHub and GitHub Enterprise repositories, and public GitLab and
Bitbucket repositories. See the [marketplace
limits](https://claude.com/docs/cowork/guide/plugins#limits).

1. Open **Customize** in the sidebar, then **Plugins**.
2. Open the **Add** dropdown and select **Add marketplace**.
3. In the **Add marketplace** window, select **Add from a repository**.
4. Under **URL**, enter the repository URL. For GitHub, you can also enter `owner/repo`.
5. Click **Sync** to add the marketplace and sync its plugins.
6. From the marketplace's list of plugins, select a plugin to open it and review its
   components.
7. Click **Add** to install it.
8. If a bundled connector asks you to sign in, complete the sign-in.

The repository's plugins appear alongside plugins from other marketplaces. The
plugin you installed is listed on the **Yours** tab. To turn individual components
on or off, open the plugin there.

### Install from a file {#cowork-file}

Use this method when someone has shared a plugin package with you. Check the
[package limits](https://claude.com/docs/cowork/guide/plugins#limits) before
uploading it.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Open the **Add** dropdown and select **Upload a plugin**.
3. Select the plugin package to upload, then click **Upload**.
4. If a bundled connector asks you to sign in, complete the sign-in.

The plugin is listed on the **Yours** tab. Open it to review its components and
turn individual components on or off.

### Next steps {#cowork-next}

- [Update or remove a plugin](https://claude.com/docs/cowork/guide/plugins#update-and-remove-plugins).
- [Provision plugins for an organization](https://claude.com/docs/cowork/3p/extensions).
- [Submit a plugin to the official marketplace](https://claude.com/docs/plugins/submit).
