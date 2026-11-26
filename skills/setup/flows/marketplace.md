# Flow: marketplace setup

Used when the person chose "marketplace" in `flows/configure.md` (the `kind` is `marketplace`). The working folder is the already cloned marketplace repository; stay in this call and in this folder. The dialogue rules of the section "Guided dialogue (both kinds)" in `flows/configure.md` apply unchanged: ask one question or one small coherent group at a time with the host's question tool, take over only explicitly answered facts, treat a cancelled or unanswered question as a pause, and write nothing before all required facts are answered.

## Preconditions

- The Git repository with its GitHub `origin` already exists (checked by the entry); the flow never creates repositories, sets remotes, commits, pushes, installs or publishes. The name of a marketplace is its identity and it records no repository of its own.
- The folder is not a plugin repository: a root plugin.json makes the generator refuse ("a plugin repository cannot become a marketplace"). Report it and stop.
- No marketplace is embedded and no plugin is created here.

## Steps

1. Required facts, never invented or dummy-filled: the technical name (lowercase kebab-case), the display name and the owner (publisher). An existing `marketplace.json` supplies values the person did not give; the folder name or Git metadata may only be offered as a suggestion, and a suggestion is never a selection: the person answers explicitly. The owner is never taken from the Git author; it is a publisher decision of the person.
2. When all facts are answered, run the generator. First run the same call with `--plan` added: it writes nothing and answers with `write_request`. Ask before writing (R50): write the `write_request` unchanged as the first visible text of this step, nothing before it, and ask exactly this one question, with the host's question tool or in one message without it, with the choices "Yes" and "No" in the operator language. Only an explicit yes runs the call without `--plan`; on no, or when the question is cancelled or unanswered, write nothing, write `write_declined` unchanged and end. A `write_request` of null means nothing would change: run the call without asking. Write the `result_message` of the run unchanged in the final answer. (`<shared>` is the shared directory `../../_shared`, resolved from this file):

   ```sh
   python3 -B "<shared>/scripts/workflows.py" create --kind marketplace --root "<folder>" \
     --name <technical-name> --display-name "<Display Name>" --owner "<Owner>"
   ```

   It creates the canonical `marketplace.json`, both derived host catalogs (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`), the standalone scripts, the Makefile (`sync`, `check`, `test`, `verify`, `install-local`), the starter instructions, the starter READMEs, the documentation settings with the pages Installation, Concepts and Development (German and English) and `local-marketplace.example.json`. Existing README files, licenses and other prose are preserved. It neither judges nor replaces an existing synced skeleton file (also a deviating one): such a file stays byte-identical and is decided later by the sync flow. Repeating the operation is idempotent (`changed` stays empty); an identity conflict with an existing `marketplace.json` stops without writes, and nothing is migrated.
3. Judge the result by the generator's own answer, which has `action`, `changed` and `published: false` but no `ok` and no `checks`: success means exit 0. On a non-zero exit write the text the command printed on stderr, up to the line `[Technical details`, unchanged (`../../_shared/references/messages.md`) and stop; do not run `record`.
4. Only after exit 0 write the evidence: `python3 -B "<helper>" record --target "<folder>" --plugin plugin-manager --kind marketplace --artifact <technical-name>`. `record` checks that the root `marketplace.json` exists with exactly that name and writes `.project/plugins/plugin-manager/config.json`; judge it by exit 0 and `ok: true`; on failure write the `message` of the answer unchanged (`../../_shared/references/messages.md`).
5. Run `status` again (see SKILL.md). The skeleton flow now records the hash evidence of the synced files of the kind marketplace, then `ready`. Report what was created and that publishing, installation and plugin registration are separate steps; the local checkout mappings (`.local/marketplace.json`, never committed) are created when plugins are associated, and `local-marketplace.example.json` is only an optional manual template.

## Boundaries

Never execute target code, create or change remotes, commit, push, install or publish. Structural creation is not host or GitHub acceptance.
