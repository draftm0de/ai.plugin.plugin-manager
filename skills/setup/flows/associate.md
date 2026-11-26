# Flow: marketplace association of a plugin

Used when the person asks to set, change or move the marketplace of a plugin ("change the marketplace association", "move this plugin to another marketplace", "my marketplace checkout moved"). The state loop never routes here and `ready` stays one line; this flow is started by a request after the language gate of the entry. The working folder is the plugin repository of the workpackage; stay in this call and in this folder. The dialogue rules of the section "Guided dialogue (both kinds)" in `flows/configure.md` apply unchanged.

## The rule

A plugin belongs to exactly one marketplace. Two facts carry it, nothing else does:

- the identity `marketplace: {name}` in the committed `.project/plugins/plugin-manager/config.json` (mandatory for the kind `plugin`), and
- the path of the checkout on this machine in the Git-ignored `.project/plugins/plugin-manager/local.json` (`{"schema_version": 1, "marketplace_path": "<path>"}`).

There is no second association, no list of named associations and no fallback to the former `.local/marketplace.json` of the plugin; a `local.json` in any other format is refused and never migrated. The marketplace side keeps the checkouts of its plugins under `sources` in its own ignored `.local/marketplace.json`.

## Preconditions

- `status` shows `configuration.kind: plugin`. Without configuration evidence, stop and send the person to the configuration flow (`flows/configure.md`); for the kind `marketplace` say that only plugins belong to a marketplace and stop.
- The folder is a Git checkout whose GitHub `origin` matches the `repository` of its `plugin.json`; the name in `plugin.json` is the `artifact` of the evidence.
- The flow never creates repositories, commits, pushes, installs or publishes and creates no development tools (the skeleton and sync flows own them).

## Steps

1. Run `status` (see `SKILL.md`) and read `association`: `marketplace` (the committed identity), `path` and `state` (`ok`, `path_missing`, `path_invalid`, `mismatch`, `unsupported`). Name the current marketplace and the state in one sentence, without quoting file contents.
2. Ask for the local path of the target marketplace checkout: the same marketplace after a fresh clone or a moved checkout, or another one. Use the host's question tool; a suggestion is never a selection, so confirm the concrete path explicitly ("Use this checkout" / "Choose another checkout"). Nothing is written before the answer.
3. When the target is another marketplace than the current one, say before the run what happens: the plugin entry, its local `sources` mapping and the host catalogs leave the old marketplace and enter the new one, and `config.json` of the plugin gets the new identity. These are committed files; nothing is committed here.
4. Run the helper. First run the same call with `--plan` added: it writes nothing and answers with `write_request`. Ask before writing (R50), with no text before the question. The whole `write_request`, every file line included and unchanged, is the question: with the host's question tool it goes into the question text itself, because the person may see only that dialog (never ask only its last line or point to a list shown elsewhere); without such a tool send it as one message. The choices are "Yes" and "No" in the operator language. Only an explicit yes runs the call without `--plan`; on no, or when the question is cancelled or unanswered, write nothing, write `write_declined` unchanged and end. A `write_request` of null means nothing would change: run the call without asking. Write the `result_message` of the run unchanged in the final answer. (`<shared>` is the shared directory `../../_shared`, resolved from this file):

   ```sh
   python3 -B "<shared>/scripts/workflows.py" associate --root "<folder>" --plugin plugin-manager \
     --marketplace "<path of the target checkout>"
   ```

   It checks the target as a marketplace, that plugin and marketplace are separate repositories, that the identity fits, that no local configuration is tracked by Git and that the ignore rules are effective, and writes everything in one transaction with rollback. The same marketplace is idempotent (a fresh clone only gets its `local.json`).
5. Judge the result by the helper's own answer, which has `action: "associate"`, `changed`, `published: false`, `from`, `to`, `old_catalog_entry_remains` and a prose `next`, but no `ok`: success means exit 0. On a non-zero exit write the text the command printed on stderr, up to the line `[Technical details`, unchanged (`../../_shared/references/messages.md`) and stop. Typical reasons: the target is no marketplace or a plugin repository, the marketplace name belongs to another repository, a local configuration is tracked, `local.json` has an unsupported format, a second marketplace without the explicit change, or the previous marketplace is not available locally.
6. When the previous marketplace checkout is gone, its catalog entry cannot be removed. Explain that and ask for restoring the checkout. Only after the person's explicit consent repeat the call with `--drop-missing-old`: it releases only the local reference and the identity of the plugin; the result then carries `old_catalog_entry_remains: true` and the entry has to be removed by hand in that repository.
7. Run `status` again. Report the changed paths by name and the helper's `next` text: the plugin's `config.json`, the `marketplace.json` and the host catalogs of the marketplaces involved are changed and unversioned; they are published through the separate publish action after its own approval.

## Boundaries

Never execute target code, never commit, push, install or publish, never write development tools, never read or migrate the former plugin-side `.local/marketplace.json`, and never keep a second marketplace. Structural association is not host or GitHub acceptance.
