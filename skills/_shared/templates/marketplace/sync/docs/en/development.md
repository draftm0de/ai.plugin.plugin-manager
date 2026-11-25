# Development

[Installation](installation.md) · [Plugins](plugins.md) · [Concepts](concepts.md)

For people who work on this marketplace. You do not need this page to use it.

## Requirements

- Git and Python 3.10 or newer. Make is optional.
- Claude or Codex with the Plugin Manager installed.
- For a local installation the CLI of the host (`claude` or `codex`).
- One GitHub repository for the marketplace and one per plugin, each cloned locally.

## Set up

1. Create the marketplace repository on GitHub and clone it.
2. Run `/plugin-manager:setup` in it and choose "Marketplace".
3. Create and clone a plugin repository, run `/plugin-manager:setup` in it, choose "Plugin" and name this marketplace. This writes the entry in `marketplace.json` and the local association.

## Test locally

In the marketplace folder:

```bash
make install-local TARGET=claude
```

This installs the local state of every listed plugin as a separate development marketplace `<name>-dev`, uncommitted changes included. Open a new session afterwards. For Codex use `TARGET=codex`.

## Publish

Commit and push the plugins first, then the marketplace:

```bash
make sync
```

```bash
make check test verify
```

Hosts install what lies on the default branch. There are no versions, tags or releases. People who already use the marketplace update it as described under [Installation](installation.md).
