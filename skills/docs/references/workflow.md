# Documentation workflow

The rules of the `docs` action. Paths are relative to `skills/_shared/` unless explicitly rooted elsewhere.

## Action

`docs` creates the structure of the documentation and reports what is missing. It writes no texts of its own: what a person writes is the person's. Whether the documentation gets written is their decision.

## Inputs and boundaries

- Use the requested repository as the output. Ask which only when it cannot be inferred from the current project.
- Never inspect private CVs, state, runs, credentials, `.env` files, ignored test output, or unrelated repositories. Source files are never executed.
- Never write, merge, translate or improve text on a page that exists, apart from the generated pages, which the helper writes.
- Never invent a fact, and do not ask for a missing one: the page states it as open and the report names it.

## Workflow

### 1. Languages

- Read `docs/documentation.json` → `documentation.languages` and `documentation.default_language`.
- Honor an explicit user choice, including English only. With no saved policy and no clear instruction, ask with the question `documentation_languages` of `setup_state.py questions` (fixed wording, R55); read `references/languages.md`.

### 2. Generate, create and check

Run this one command, exactly as written. The helper lies in the shared folder, `../../_shared/scripts/documentation.py` relative to this file, not in the folder of this skill:

`python3 -B "<plugin>/skills/_shared/scripts/documentation.py" scaffold --source "<repository>" --output "<repository>"`

Add `--languages` and `--default-language` only for the first run. The command

- writes the generated pages anew: `installation.md`, `concepts.md`, `development.md` and, for a plugin, `skills.md` and `files.md`
- creates missing pages the person writes: `README` and, for a plugin, `skills/<skill>.md`
- checks the documentation; everything it finds is a warning, never a failure

### 3. Answer

Write `result_message` of the answer unchanged as the whole final answer: no added sentences, no closing-summary or next-step card. On a failure follow the message rules instead.

Fix nothing by hand and offer no text. When the person asks for texts afterwards, that is ordinary work outside this action. Never commit, push, publish or install. Only when the person asks what belongs into an open section, say it (`warnings` of the answer name it).

## Pages

| Page | Plugin | Marketplace |
| --- | --- | --- |
| `README` | by hand: introduction, Quick start, Features per skill | by hand: introduction, Plugins with one `### <plugin>` and a link to its README |
| `installation.md`, `concepts.md`, `development.md` | generated | generated |
| `skills.md`, `files.md` | generated | none |
| `skills/<skill>.md` | by hand | none |

A marketplace has no page per plugin. The headings each page needs are in `scripts/verify/docs.py` (`OUTLINE`, `EXACT_HEADINGS`). Pages of the former structure are reported; nothing is converted or deleted.
