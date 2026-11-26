# 🛠 :docs

[Deutsch](../../de/skills/docs.md) | **English**

[Home](../../../README.en.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Concepts](../concepts.md) · [Development](../development.md) · [Shared files](../files.md)

## Description

`docs` takes care of how your documentation is built. It creates some of the pages itself; for the others you write the texts and only the structure matters. It creates missing pages. What does not fit is reported to you.

Which pages these are and what is checked depends on whether your repository is a plugin or a marketplace. `docs` detects that itself.

### Plugins

#### Created automatically

| File | Where the content comes from |
| --- | --- |
| `docs/<lang>/installation.md` | fixed text, plus the name of your plugin from `plugin.json` and the name and address of your marketplace |
| `docs/<lang>/skills.md` | fixed text, plus for each skill the section "Description" of its skill page |
| `docs/<lang>/concepts.md` | fixed text |
| `docs/<lang>/development.md` | fixed text |
| `docs/<lang>/files.md` | fixed text, plus the file trees from what Plugin Manager delivers |

#### Written by you

Only the headings are prescribed. Everything below them is free.

**`README.md`** (and `README.<lang>.md` for each further language)

```text
# <title>                  required, exactly one
│   introduction           free
├── ## ⚡ Quick start       required
│   └── ### …              free
└── ## 🛠 Features          required
    └── ### :<skill>       required, one per skill
            explanation    at most 200 characters
            link           to docs/<lang>/skills/<skill>.md
```

**`docs/<lang>/skills/<skill>.md`** (one file per skill, file name equals skill name)

```text
# <title>                  required, exactly one
├── ## Description         required
│   └── ### …              free
├── ## Workflow            required
├── 

You are asked only when the setup is missing ("Run /plugin-manager:setup (in Codex: $plugin-manager:setup) now?") or, the first time, for the documentation languages ("Which documentation languages?").

## Example             required
└── ## Reads and writes    required
```

The `##` headings must have exactly these names and this order. In the README an icon may precede them. From "Description", `skills.md` shows only the text up to the first sub-heading.

#### Checked

- All pages exist, and the created pages have exactly their headings.
- The README has Quick start and Features, with exactly one entry per skill, short enough and linked.
- `skills.md` has one entry per skill, and every skill page has its four sections.

### Marketplaces

#### Created automatically

| File | Where the content comes from |
| --- | --- |
| `docs/<lang>/installation.md` | fixed text, plus the name and address of the marketplace; only add, update, remove |
| `docs/<lang>/concepts.md` | fixed text, the same as in plugins |
| `docs/<lang>/development.md` | fixed text: connecting plugins, local testing, commands and CI |

There is no page per plugin, no plugin list and no page "Shared files".

#### Written by you

Only the headings are prescribed. Everything below them is free.

**`README.md`** (and `README.<lang>.md` for each further language)

```text
# <title>                  required, exactly one
│   introduction           free, no quick start
└── ## 📦 Plugins          required
    └── ### <display name> required, one per plugin in marketplace.json
            explanation    free
            link           to the README in the repository of the plugin
```

An icon may precede `## Plugins`.

#### Checked

- All pages exist, and the created pages have exactly their headings.
- The README has exactly one entry per listed plugin, each with a link into its repository.
- Former pages `plugins.md` or `files.md` are reported but not deleted.

### For both

`/plugin-manager:docs` writes the created pages anew on every run. Do not edit them by hand, your changes would be lost; each carries a note saying so at the bottom. Your own pages are only created when they are missing and are never overwritten.

When a fact is missing, for example the address of the marketplace, the page says "(not set yet)" and the command reports it.

`/plugin-manager:verify`, `make verify` and CI also check that every language is linked and no internal link leads nowhere. Everything they find is a **warning**: CI stays green. Whether and how you write your documentation is your decision.

`<lang>` stands for each selected documentation language.

## Workflow

1. Checks that the repository is set up and, the first time, clarifies the documentation languages.
2. Writes the automatically created pages anew and creates missing pages.
3. Checks structure and links.
4. Reports briefly what was written and what is still open. It writes no texts.

## Example

`/plugin-manager:docs` (Codex: `$plugin-manager:docs`) after adding a skill: the skills page gets its section.

## Reads and writes

Reads the facts of your repository, for example `plugin.json`, without running code. Writes the README and pages under `docs/`; it does not change your existing texts.
