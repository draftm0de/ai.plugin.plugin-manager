---
name: verify
description: Detect plugin or marketplace structure and report production-readiness gaps. Distinguish automated structural checks from unverified host acceptance.
---

# verify (`/plugin-manager:verify`)

Detect plugin or marketplace structure and report production-readiness gaps. Distinguish automated structural checks from unverified host acceptance.

## Read first

- `../_shared/WORKFLOWS.md` for the rules every action shares; the rules of this action are here.

## Start

No gate: when `setup_state.py status` shows a pending setup or sync, report it as a finding and continue; verify never runs setup.

Ask for paths only if they cannot be determined.

- TARGET comes from the user or current project root, never from this plugin installation. Reject ambiguous roots.
- The kind is detected (`--kind auto`) and never a call argument of the command; an explicit `--kind plugin` or `--kind marketplace` stays possible (`structure.py`, `standards.py`). Wrong or ambiguous roots fail with guidance.

## Steps

### Structural checks

Run each check with `--source TARGET` and report every result, also after a failed one:

| Check | For |
| --- | --- |
| `../_shared/scripts/verify/structure.py` (it detects the kind) | plugin and marketplace |
| `../_shared/scripts/verify/standards.py` | plugin and marketplace |
| `../_shared/scripts/verify/docs.py` | plugin and marketplace |
| `../_shared/scripts/verify/conventions.py` | plugin |
| `../_shared/scripts/verify/hashes.py` | plugin |

A repository runs the same checks with `make verify`, in its CI and (plugin) before each commit.

### Report

- Report `structure_valid` independently from `local_development.complete`. Missing local checkout mappings on a fresh clone mean local checks are unavailable; they do not invalidate the published structure. Installation requires those checkouts, but verification never installs them.
- Report structural checks separately from host acceptance and unverified remote content.
- `plugin_audit.py` is an internal scaffold/template audit, not the verification entry point.

### Explicit scope/source review

When asked to compare target requirements with implementation:

1. Read `../_shared/references/scope-review.md` in full.
2. Run `../_shared/scripts/verify/scope.py --source TARGET`.
3. Perform the actual requirement-by-requirement source/test comparison as instructed.

- `SCOPE.md` is authoritative only for confirmed requirements; never infer the target from code or silently promote draft requirements.
- Cite concrete source lines, explain why a change is needed, distinguish contradictions from missing evidence, and report unexecuted tests.
- The helper's `ready_for_source_review` is not semantic acceptance.
- No repairs, code execution or tests during verify. Keep exactly the same read-only boundary.

## Boundaries

- This action is read-only; configuration and repair belong to a separate action. No target code is executed, no repairs or installation occur.
- A skeleton is not functional acceptance.

## Messages

Messages to the person (failures, stops, results) follow `../_shared/references/messages.md`: two short paragraphs of running text (what could not be done, because of what, what was changed; then the request with the exact way and the call to repeat), no labels, no technical terms.
