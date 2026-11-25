# Development

[Installation](installation.md) · [Skills](skills.md) · [Concepts](concepts.md)

For people who work on this plugin. You do not need this page to use it.

## Requirements

- Git and Python 3.10 or newer. Make is optional.
- Claude or Codex with the Plugin Manager installed.
- For a local installation the CLI of the host (`claude` or `codex`).
- One GitHub repository for the marketplace and one per plugin, each cloned locally.

## Set up

1. Have a marketplace: its own repository, set up with `/plugin-manager:setup` as "Marketplace" and cloned locally.
2. Create the plugin repository on GitHub and clone it.
3. Run `/plugin-manager:setup` in it, choose "Plugin" and name the marketplace. This writes the marketplace entry and the local association.
4. Record the requirements in `SCOPE.md` and build the skills under `skills/<skill>/`.

## Test locally

In the plugin folder:

```bash
make sync
```

```bash
make check test verify
```

Install from the marketplace folder:

```bash
make -C ../<marketplace> install-local TARGET=claude
```

Open a new session afterwards. Uncommitted changes are included. For Codex use `TARGET=codex`.

## Shared files

Plugin Manager keeps some files up to date (synced) and creates others only once (seed). `.project/plugins/plugin-manager/skeleton.json` lists the synced files. Do not change them: your own rules belong into `CUSTOM.AGENTS.md`, your own commands into `CUSTOM.mk`, your own CI steps into another file under `.github/workflows/`. If you change a synced file anyway, `/plugin-manager:setup` asks whether to keep it or adopt the template. If you keep `AGENTS.md`, the `SCOPE.md` of a marketplace or a standard under `docs/standards/`, `verify` fails.

## Publish

Commit and push to the default branch; hosts install what lies there. There are no versions, tags or releases. Push a new plugin first, then the marketplace with its entry.
