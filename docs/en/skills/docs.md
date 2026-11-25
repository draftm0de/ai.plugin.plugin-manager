# 🛠 :docs

[Deutsch](../../de/skills/docs.md) | **English**

[Home](../../../README.en.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Concepts](../concepts.md) · [Development](../development.md) · [Shared files](../files.md)

## Description

`docs` takes care of how your documentation is built. It creates some of the pages itself; for the others you write the texts and only the structure matters. It creates missing skill pages. What does not fit is reported to you.

### Files that are created automatically

`/plugin-manager:docs` writes these pages anew on every run. Do not edit them by hand, your changes would be lost. Each carries a note saying so at the bottom.

| File | Where the content comes from |
| --- | --- |
| `docs/<lang>/installation.md` | fixed text, plus the name of your plugin from `plugin.json` and the name and address of your marketplace |
| `docs/<lang>/skills.md` | fixed text, plus for each skill the section "Description" of its skill page |
| `docs/<lang>/concepts.md` | fixed text |
| `docs/<lang>/development.md` | fixed text |
| `docs/<lang>/files.md` | fixed text, plus the file trees from what Plugin Manager delivers |

When a fact is missing, for example the address of the marketplace, the page says "(not set yet)" and the command reports it.

### Files you write yourself

`/plugin-manager:docs` creates these pages only when they are missing. After that they are yours and are never overwritten. Only the structure is prescribed.

| File | Structure |
| --- | --- |
| `README.md`, `README.<lang>.md` | title and introduction, `## ⚡ Quick start` with free sub-sections, `## 🛠 Features` with one `### :<skill>` each: at most 200 characters and a link to the skill page |
| `docs/<lang>/skills/<skill>.md` | one file per skill, file name equals skill name: `## Description`, `## Workflow`, `## Example`, `## Reads and writes` |

From "Description", `skills.md` shows only the text up to the first sub-heading.

### What is checked

`/plugin-manager:verify`, `make verify` and CI check that all pages exist, the headings are right, every language is linked and no internal link leads nowhere. Everything they find is a **warning**: CI stays green. Whether and how you write your documentation is your decision.

`<lang>` stands for each selected documentation language. For marketplaces: `concepts.md`, `development.md` and `files.md` are created; `docs` only creates the installation and plugin list pages when missing.

## Workflow

1. Checks that the repository is set up and, the first time, clarifies the documentation languages.
2. Writes the automatically created pages anew and creates missing pages.
3. Checks structure and links.
4. Reports what is still to be written and what belongs into each section. It writes no texts.

## Example

`/plugin-manager:docs` after adding a skill: the skills page gets its section.

## Reads and writes

Reads the facts of your repository, for example `plugin.json`, without running code. Writes the README and pages under `docs/`; it does not change your existing texts.

---

Documentation prepared with Plugin Manager.
