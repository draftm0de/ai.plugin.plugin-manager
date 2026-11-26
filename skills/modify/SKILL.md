---
name: modify
description: Change what a plugin or marketplace repository states about itself - technical name, display name and description (a marketplace has no description). Shows the consequences first and writes only after the person's explicit yes. Does not rewrite documentation, tests or the repository URL; the marketplace association stays in setup.
---

# modify (`/plugin-manager:modify`)

Changes what a plugin or marketplace states about itself: name, display name and description.

## Read first

- `../_shared/WORKFLOWS.md` for the rules every action shares; the rules of this action are here.
- Helper: `scripts/modify.py`; it takes the kind from the configuration evidence of the workpackage, never from the call.

## Start

Follow `../_shared/flows/gate.md` (`setup_state.py gate --action modify`) before asking anything. When the gate is closed, stop as that flow says: the one-sentence stop message, then the question whether to run `/plugin-manager:setup`; this skill writes nothing then.

Only `setup` changes configuration, skeleton files or sync decisions.

## Steps

1. Ask what to change: name, display name, description (marketplace: name and display name only), with the fixed wording of `python3 -B "../setup/scripts/setup_state.py" questions --target "<folder>"` (R55): the question `change`, then `new_value` for each chosen field (replace only {field} with the chosen answer and {current} with the present value in plugin.json or marketplace.json; add no sentence of your own). Take values the person gave in the call; never invent them. One targeted question at a time; a cancelled or unanswered question is a pause.
2. Show the consequences with `python3 -B "scripts/modify.py" --root "<folder>" [--name N] [--display-name D] [--description T] --dry-run` (writes nothing): the files that would change, whether the marketplace entry follows, and for a marketplace the affected plugins. Name only paths and facts, no file contents.
3. Write only after the person's explicit yes to exactly these values. The dry run answers with `write_request`: that whole text, every file line included and unchanged, is the question itself (with the host's question tool it goes into the question text, because the person may see only that dialog; choices "Yes" and "No" in the operator language; write no text before it). On no write `write_declined` and stop. After yes run the same call without `--dry-run` and show its `result_message` unchanged. Success is exit 0; a refusal prints `ERROR:` and changed nothing.
4. Report `changed`, `catalog_entry_remains` and the `follow_up` notes: call forms and documentation are refreshed with `/plugin-manager:docs`, the person commits and pushes the changed files.

### What changes

- The plugin and its derived host manifests, `artifact` in config.json and the marketplace entry change in one rollback-capable transaction.
- The entry is updated only when the marketplace checkout named by the ignored local.json is available, otherwise `catalog_entry_remains` says what to change there.
- A marketplace rename lists the affected plugin checkouts and writes nothing into them; each plugin takes the new name through the `associate` flow of setup.
- The repository name and URL stay.

### After a rename

- Do not report a rename as done before `verify` shows `local_development.complete` (its finding names a stale catalog entry) and `make install-local DRY_RUN=1` runs without identity mismatch.
- If no local marketplace is configured, say that this check was not run.
- Call forms (`/<name>:<skill>`, `<name>@<marketplace>`), documentation and tests are refreshed by `docs`, never by modify.

## Boundaries

Never commit, push, install or publish.

## Messages

Messages to the person (failures, stops, results) follow `../_shared/references/messages.md`: two short paragraphs of running text, shell commands in a code block, (what could not be done, because of what, what was changed; then the request with the exact way and the call to repeat), no labels, no technical terms.
