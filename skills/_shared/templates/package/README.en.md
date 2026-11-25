# Plugin Manager

[Deutsch](README.md) | **English**

This plugin documents accessible local skills and plugins from source evidence. Documentation languages are chosen per repository: German only, English only or both. Use `setup` to set up a marketplace or create and associate a separate plugin, `docs` to refresh documentation, `modify` for name and description, or `verify` for a read-only structure audit. The agent asks about material uncertainties. Passing structural checks does not establish production readiness. Nothing is published or installed without instruction.

In Claude: `/plugin-manager:verify SOURCE_PATH`, with the equivalent `/plugin-manager:setup` (setup, plugin or marketplace), `:docs` and `:modify` commands. In ChatGPT request the action in natural language. The host must have access to the source; helpers require Python 3.10 or newer.

[Workflow and limitations](skills/_shared/WORKFLOWS.md)

## Publishing

You commit and push yourself; what lies on the default branch is installed. Push new plugin repositories before their marketplace entries. No versions, tags or releases.

Management tools require Git and Python 3.10+; Make is only a convenience wrapper. Management needs the selected host CLI only for automatic local installation/updates; explicitly requested model tests also need an authenticated CLI. No additional Python packages.

Local snapshots read the current checkout including uncommitted changes, regardless of branch. After edits or branch switches run `install-local` and open a new host session. Local tests require no commit, push or PR. Keep one shared `<marketplace-id>-dev`, with no additional marketplaces per branch.

The local association of a plugin with its one marketplace is set up and changed by `plugin-manager` (associate). The path of the marketplace checkout lives in the Git-ignored `.project/plugins/plugin-manager/local.json` of the plugin; the checkouts of the plugins live under `sources` in the Git-ignored `.local/marketplace.json` of the marketplace; never commit those mappings. `local-marketplace.example.json` is an optional manual copy template for the marketplace side.

## Skills

`setup`, `docs`, `modify` and `verify`; the marketplace association of a plugin is a flow of setup. Shared rules: `skills/_shared/WORKFLOWS.md`.
