# Repository layout, distribution and local installation

Paths are relative to `skills/_shared/` unless explicitly rooted elsewhere.

## Shared installation source

Follow the temporary-file, ignore and Python rules in `references/source-of-truth.md`.

### Templates

- Canonical plugin templates live in `templates/plugin/{sync,seed}/`; standalone marketplace tools live in `templates/marketplace/{sync,seed}/` (`sync/` is hashed in `manifests/<kind>.sync.json`, `seed/` is created once).
- Keep authorized consumer copies synchronized.
- Neither a new marketplace nor a plugin requires a fixed Manager checkout.

### Ownership and host metadata

- Plugins own `plugin.json`, `skills/`, documentation and derived `.claude-plugin/plugin.json`; they never own marketplace catalogs. `make sync` generates host plugin metadata; `make check` checks drift.
- Marketplaces own `marketplace.json` and derive `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json` using `python3 -B scripts/marketplace.py sync`; `check` instead of `sync` reports drift.
- All repository manifests and catalog entries omit versions. Local content hashes are cache labels only.

### Local installation

- `make install-local` / `make install-local TARGET=claude|codex` run in the marketplace only and install all locally associated plugins as `<marketplace-name>-dev`; a plugin repository has no local installation of its own.
- A missing checkout blocks installation before host changes.
- `DRY_RUN=1` creates snapshots but does not invoke a host.
- Personal installations are not test fixtures. Native acceptance uses isolated profiles; GitHub and GUI acceptance remain separate.

### Verify results

- Verify only reads: `valid` and `structure_valid` describe the publishable structure; `local_development.complete` separately describes available local configuration.
- Missing local paths are expected on fresh clones and do not invalidate published catalogs.
- No repairs, target code execution or installation during verify. The older internal template audit is not the public verify action.

## Repository distribution

Read `references/release-distribution.md`.

- The Manager never commits, pushes or publishes: the person does that.
- What lies on the default branch is what a host installs; for a new marketplace entry the plugin has to be pushed first.
- Host refresh and GUI acceptance are separate checks.

## No embedded plugins

- Every plugin, the Plugin Manager included, has its own repository; a marketplace embeds none and owns only its catalogs.
- Do not modify the earlier zyris.skill.manager repository.

## Prerequisites and local checkout semantics

`references/prerequisites.md` is canonical for Git, Python 3.10+, and optional Make. Do not install tools automatically.

- Local snapshots use the current checkout, including uncommitted edits, on any branch.
- After edits or branch switches run install-local and open a new host session.
- No commit/push/PR or per-branch marketplace for local tests.
- configure is the normal setup path; local-marketplace.example.json is an optional manual template, never a runtime fallback.
- Only ignored .local/marketplace.json stores local runtime mappings.
