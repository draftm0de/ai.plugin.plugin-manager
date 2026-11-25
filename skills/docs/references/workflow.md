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
- Honor an explicit user choice, including English only. With no saved policy and no clear instruction, ask whether German, English or both and which is the default; read `references/languages.md`.

### 2. Generate and create

Run `python3 -B "<helper>" scaffold --source PATH --output REPOSITORY` (the helper is `scripts/documentation.py`; add `--languages` and `--default-language` only for the first run). It

- writes the generated pages anew: `concepts.md`, `development.md`, `files.md` and, for a plugin, `installation.md` and `skills.md`
- creates missing pages the person writes: `README`, `skills/<skill>.md`; a marketplace also `installation.md` and `plugins.md`

### 3. Check

Run `python3 -B "<helper>" validate --output REPOSITORY`. Everything it names is a warning, never a failure.

### 4. Report

- the pages written anew and the pages created
- what is still to be written, per page and section, with what belongs there (the findings name it)
- missing facts (`missing_facts`), with the file where each is recorded
- other findings: missing pages, headings, links

Fix nothing by hand and offer no text. When the person asks for texts afterwards, that is ordinary work outside this action. Never commit, push, publish or install.

## Pages

| Page | Who writes it |
| --- | --- |
| `docs/<language>/installation.md` (plugin), `skills.md` (plugin), `concepts.md`, `development.md`, `files.md` | generated, anew on every run |
| `README`, `docs/<language>/skills/<skill>.md` | the person; created once when missing |
| `docs/<language>/installation.md` and `plugins.md` (marketplace) | the person; created once when missing |

The headings each page needs are in `scripts/verify/docs.py` (`OUTLINE`, `EXACT_HEADINGS`). Pages of the former structure are reported; nothing is converted or deleted.
