# Shared files

[Installation](installation.md) · [Skills](skills.md) · [Concepts](concepts.md) · [Development](development.md)

Plugin Manager puts files into every plugin and marketplace. There are two classes, and the class decides what you can change.

| | Synced file | Seed file |
| --- | --- | --- |
| Belongs to | Plugin Manager, identical in all repositories | the repository |
| Created | by `setup`, also when it is missing later | once, when the repository is created |
| New template | taken over after your yes, with a question per file if you changed it | has no effect |
| Your change | leads to a question | stays, without a question |
| Deleted | `setup` creates it again | stays deleted |

Exception: when `docs/style.md` is missing, `setup` asks for the template or for your own style.

## Changing a synced file

Do not change it when there is a file of your own for the purpose:

| Instead of | Use |
| --- | --- |
| `AGENTS.md` | `CUSTOM.AGENTS.md` |
| `Makefile` | `CUSTOM.mk` |
| `.github/workflows/dm-verify.yml` | another file under `.github/workflows/` |

If you change it anyway, the next `setup` asks for each file:

- **Keep local file:** your version stays. You are asked again only when your file or the template changes.
- **Adopt template:** your version is replaced. Save what you want to keep first.

`setup` shows no file contents or diff; compare with Git beforehand.

**Keeping has limits:** `AGENTS.md`, in plugins the standards under `docs/standards/` and in marketplaces `SCOPE.md` are binding. When they differ, `verify` and CI fail, even if you chose to keep them.

## Back into the sync

Ask `setup` for it, for example "Take the Makefile back". After your yes the template replaces your version. Or delete the file and run `setup`.

## When a template is removed

`setup` removes an unchanged copy by itself. If you changed it, you decide: keep or delete.

## Files of a plugin

**Synced:** `AGENTS.md`, `CLAUDE.md`, `Makefile`, `.github/workflows/dm-verify.yml`, `docs/<lang>/concepts.md`, `docs/<lang>/development.md`, `docs/prerequisites.md`, `docs/standards/coding.md`, `docs/standards/messages.md`, `docs/standards/skills.md`, `docs/standards/testing.md`, `githooks/pre-commit`, `scripts/build_hashes.py`, `scripts/plugin.py`, `scripts/run_tests.py`, `scripts/verify/common.py`, `scripts/verify/conventions.py`, `scripts/verify/docs.py`, `scripts/verify/hashes.py`, `scripts/verify/scope.py`, `scripts/verify/standards.py`, `scripts/verify/structure.py`, `skills/_shared/references/operator-language-helper.md`, `skills/_shared/references/operator-language.md`, `skills/_shared/scripts/messages_base.py`, `skills/_shared/scripts/operator_language.py`, `tests/README.md`, `tests/behavior/run_cases.py`, `tests/contracts/test_operator_language.py`

**Seed:** `.gitignore`, `CUSTOM.AGENTS.md`, `CUSTOM.mk`, `SCOPE.md`, `assets/icon.png`, `docs/architecture.md`, `docs/style.md`, `tests/__init__.py`, `tests/contracts/__init__.py`, `tests/contracts/test_structure.py`

## Files of a marketplace

**Synced:** `AGENTS.md`, `CLAUDE.md`, `Makefile`, `SCOPE.md`, `.github/workflows/dm-verify.yml`, `docs/<lang>/concepts.md`, `docs/<lang>/development.md`, `docs/prerequisites.md`, `scripts/local_plugins.py`, `scripts/marketplace.py`, `scripts/plugin_payload.py`, `scripts/run_tests.py`, `scripts/verify/common.py`, `scripts/verify/docs.py`, `scripts/verify/scope.py`, `scripts/verify/standards.py`, `scripts/verify/structure.py`, `tests/README.md`, `tests/contracts/test_local_plugins.py`, `tests/contracts/test_marketplace_catalogs.py`, `tests/contracts/test_plugin_payload.py`, `tests/contracts/test_run_tests.py`

**Seed:** `CUSTOM.AGENTS.md`, `CUSTOM.mk`, `local-marketplace.example.json`, `docs/architecture.md`, `docs/style.md`, `tests/__init__.py`, `tests/contracts/__init__.py`, `tests/contracts/test_structure.py`

`<lang>` stands for each selected documentation language. In `.gitignore` only missing rules are added.
