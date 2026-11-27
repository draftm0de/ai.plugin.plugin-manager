# Skill standards / Skill-Standards

Managed by the plugin manager and identical in every plugin. Do not edit it here.

## Cut

- One skill per action. The call, not the model, selects the action. Every call names plugin and skill
  (`/plugin:skill`), also when the plugin has exactly one skill.
- With several skills, Claude Code gets one `commands/<skill>.md` per skill; Codex has no command files.
- A skill description names the task and its boundary in one short text. It does not cover several actions.

## Boundaries as structure

- A read-only skill has no path that writes. Publishing never acts without a concrete approval and never commits on its own.
- A concrete order is the person's approval for exactly the change it names: the skill writes it without asking again
  and afterwards reports what it changed. Missing facts are asked for as facts, not as permission, and never invented.
- The skill asks first and waits for an explicit yes, naming the files or the effect, when a script changes files the
  order does not make evident, when the person's own content would be lost, or when an effect the order does not name
  leaves the working copy (commit, push, publishing, installation). Costs are always confirmed. Both rules hold in
  every plugin.
- A gate and a setup skill belong only to a plugin whose writing skills depend on a state of the person's project
  (a configuration, a prepared folder). Without such a state the plugin has neither; do not invent one.
- With such a state, a writing skill asks a shared gate first. The gate is one read-only script and one flow text that
  every writing skill follows. When the gate is closed the skill stops, writes nothing and points to the one skill that
  sets up.
- That setup skill is exactly one per plugin, brings the project into the configured state, may be called
  repeatedly and runs the open step and nothing else.
- The kind of a repository is never a call argument; it comes from the state of the folder.

## Text

- Every skill loads the operator-language reference before it talks to the person and follows its section "How a skill
  uses the language" (language from the helper only, everything the person reads in it, passed on to scripts that print
  text); the skill text does not repeat these rules. It follows `messages.md` for every failure and stop.
- If the plugin has `skills/_shared/references/style.md` (how it talks with its user), every skill reads it after the
  language rules. It never overrides a standard, the operator language or the message layout. The file is optional.
- `docs/style.md` may say how the documentation is written. It is optional: nothing asks for it or checks it.
- Skill and flow texts do not duplicate wording that belongs to the message catalogue or to this standard.
- Instruction texts are not product behavior. Test them with contracts and model cases, never as acceptance.
