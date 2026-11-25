---
name: docs
description: Create the structure of a repository's documentation in its selected languages, write the generated pages anew and report what is still missing. Writes no texts of its own; findings are warnings.
---

# docs (`/plugin-manager:docs`)

Creates the structure of the documentation, writes the generated pages anew and reports what is still missing. It writes no texts of its own.

## Read first

- `../_shared/WORKFLOWS.md` for the rules every action shares.
- `references/workflow.md` with the rules of this action.

## Start

Follow `../_shared/flows/gate.md` (`setup_state.py gate --action docs`) before writing anything. When the gate is closed, stop as that flow says: the one-sentence stop message, then the question whether to run `/plugin-manager:setup`; this skill writes nothing then.

Only `setup` changes configuration, skeleton files or sync decisions.

## Steps

Follow `references/workflow.md`: languages, generate and create, check, report.

## Boundaries

No texts of its own, no questions about missing facts, no failing on findings; it never commits, pushes, publishes or installs.

## Messages

Messages to the person (failures, stops, results) follow `../_shared/references/messages.md`: two short paragraphs of running text (what could not be done, because of what, what was changed; then the request with the exact way and the call to repeat), no labels, no technical terms.
