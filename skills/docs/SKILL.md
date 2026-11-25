---
name: docs
description: Re-read canonical sources and refresh documentation in the repository-selected languages. Reuse the source and language configuration manifest without duplicating product facts.
---

# docs (`/plugin-manager:docs`)

Re-read canonical sources and refresh documentation in the repository-selected languages. Reuse the source and language configuration manifest without duplicating product facts.

## Read first

- The repository's `docs/style.md` (how its documentation is written).
- `../_shared/WORKFLOWS.md` for the rules every action shares.
- `references/workflow.md` with the rules of this action.

## Start

Follow `../_shared/flows/gate.md` (`setup_state.py gate --action docs`) before reading sources or writing documentation. When the gate is closed, stop as that flow says: the one-sentence stop message, then the question whether to run `/plugin-manager:setup`; this skill writes nothing then.

Only `setup` changes configuration, skeleton files or sync decisions.

## Steps

Follow `references/workflow.md`. This is a thin plugin entry point; the page templates ship with the helper. Ask for paths only if they cannot be determined.

## Boundaries

The limits of this action stand with its workflow; it never commits, pushes, publishes or installs.

## Messages

Messages to the person (failures, stops, results) follow `../_shared/references/messages.md`: two short paragraphs of running text (what could not be done, because of what, what was changed; then the request with the exact way and the call to repeat), no labels, no technical terms.
