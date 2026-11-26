---
name: setup
description: Brings an explicitly selected plugin or marketplace repository into the configured state and keeps it up to date; may be called repeatedly. Checks language, configuration, shared development files and template sync, runs exactly the needed flow and re-checks after each flow. An existing managed file is replaced only by the person's explicit adopt decision, and removed only under the ownership rules for sources removed in the parent or by the person's explicit delete decision.
---

# setup (`/plugin-manager:setup`)

The state-guided skill of the Plugin Manager: it brings a repository into the configured state and keeps it up to date.

## Read first

- Follow `flows/entry.md` with `plugin = plugin-manager` (every helper call passes `--plugin plugin-manager`).
- The rules every action shares are in `../_shared/WORKFLOWS.md`. Specialised actions stay in their own skills.
- Helper: `scripts/setup_state.py`.
- Language rules: `../_shared/references/operator-language.md`, which applies only where it does not conflict with the entry flow. Precedence: the entry's read-only rule and flow order win. In particular its direct `--set` before continuing and its rule to ask/save a missing language even for read-only actions do not apply here.
- Resolve paths from this loaded SKILL.md; never search host caches.

## Start

No gate: `setup` is the skill that opens the gate of the others. The status answer decides which flow runs:

| Flow | For |
| --- | --- |
| `flows/language.md` | the missing operator language |
| `flows/configure.md`, `flows/marketplace.md` | plugin or marketplace configuration |
| `flows/skeleton.md` | missing or outdated shared files |
| `flows/sync.md` | a decision about a differing file |
| `flows/associate.md` | only on request: the one marketplace of a plugin |

## Steps

### Kinds and configuration

- The kinds are `plugin` (a plugin repository) and `marketplace` (a marketplace checkout); the configuration flow asks which one first.
- Configuration is two steps: the existing generator and then `record`, which writes the configuration evidence only after that success.
- The generator answers with `action`, `changed`, `checks` and prose `next`, but no `ok`; success means exit 0 **and** `checks.status == "passed"`.
- A configuration failure is a non-zero exit or `checks.status` other than `passed`, for example `needs_attention`: report the failing entries under `checks`, the files actually listed in `changed` and the generator's own `next` text.

### Writing shared files

- Before the skeleton flow writes, ask with the `write_request` of the status answer, with no text before the question; after writing, show each `result_message` (R50).
- Both are complete texts shown unchanged, not retold under the message layout.
- Run helper commands as plain single commands.
- A request to take back a file that was kept on purpose goes to `flows/sync.md`, section "Taking a kept file back" (R45).

### Marketplace association

- A request to set, change or move the marketplace of a plugin ("change the marketplace association") goes after the language gate directly to `flows/associate.md`; it needs the configuration evidence of the kind `plugin`.
- A plugin belongs to exactly one marketplace (R21): the status answer reports `association` (`marketplace`, `path`, `state`) as a read-only hint for a plugin, never as a gate for `ready`.
- A missing local path (`path_missing`, for example on a fresh clone) is only mentioned when installation, publication or association is asked for.

### Ready

On `ready` output only (after any `result_message`) the ready line `<Kind> <name> Status: fully configured` (German `<Kind> <name> Status: vollständig konfiguriert`) with no remark, exactly once and without a closing-summary or next-step card, and wait. `<Kind>` is `Plugin` or `Marketplace` from the field `state`, `<name>` the field `plugin` of the status answer, the configured repository.

## Boundaries

- Never the installed Manager or unrelated projects as target.
- Configuration uses the existing `create --kind plugin` generator with its documented prerequisites (it reads Git metadata); the entry adds no Git mutation or network action.
- This does not alter docs, verify, publish or `create --kind plugin`.

### Files this skill manages

| File | Content |
| --- | --- |
| `.project/plugins/plugin-manager/config.json` | configuration evidence, schema_version 2 with the mandatory `marketplace` identity of a plugin; written by `record` and, when the marketplace changes, by `associate` |
| `.project/plugins/plugin-manager/local.json` | Git-ignored path of the one marketplace checkout; written only by the plugin generator and `associate` |
| `.project/plugins/plugin-manager/skeleton.json` | skeleton evidence, schema_version 2 |

The plugin skeleton is the `common` list of `../_shared/manifests/plugin.json`, the marketplace skeleton that of `../_shared/manifests/marketplace.json`.

## Messages

Messages to the person (failures, stops, results) follow `../_shared/references/messages.md`: two short paragraphs of running text (what could not be done, because of what, what was changed; then the request with the exact way and the call to repeat), no labels, no technical terms.
