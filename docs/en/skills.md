# Skills

[Deutsch](../de/skills.md) | **English**

<img src="../../assets/icon.png" alt="draftmode.io" width="48">

[Home](../../README.en.md) · [Installation](installation.md) · [Skills](skills.md) · [Concepts](concepts.md) · [Development](development.md)

Five skills, one per task. In Claude Code you call them with `/plugin-manager:<skill>`.

## Overview

| Skill | Purpose |
| --- | --- |
| [docs](#docs) | Write documentation from the sources |
| [modify](#modify) | Change name, display name, description |
| [setup](#setup) | Set up and keep current |
| [verify](#verify) | Check, read-only |

## docs

### Description

Writes or refreshes the documentation of a plugin or marketplace in the selected languages, from `SCOPE.md`, the skills and the source code.

### Workflow

1. Checks that the repository is set up and has its writing style `docs/style.md`.
2. Reads the sources and clarifies open points with you.
3. Writes README, installation, skills or plugin list, and concepts.
4. Checks structure and links.

### Example

`/plugin-manager:docs` after adding a skill: the skills page gets its section.

### Reads and writes

Reads the writing style and the sources of the repository without running its code. Writes README and pages under `docs/`; your own existing text stays.


## modify

### Description

Changes what a repository says about itself: technical name, display name and description. A marketplace has no description.

### Workflow

1. Checks that the repository is set up.
2. Asks what should change.
3. Shows every affected file without writing.
4. Writes only after your yes.
5. Names the next steps: refresh the documentation with `docs`, commit and push the changes yourself.

### Example

"Give the plugin the display name Interview Coach."

### Reads and writes

Reads the configuration and the associated marketplace. Writes the manifests and, for a plugin, its marketplace entry if the marketplace folder is available on your machine. When you rename a marketplace, the affected plugins are only listed, not changed.


## setup

### Description

Brings a plugin or marketplace repository into the configured state and keeps the shared files current. Call it as often as you like.

### Workflow

1. Resolve the language.
2. Configure plugin or marketplace.
3. Add and update shared files: it first names the files and writes after your yes; for changed files you decide one by one. Afterwards it lists what it wrote.
4. If the writing style `docs/style.md` is missing, you pick the template or describe your own.
5. One line "fully configured".

Which files are shared and what changing one means is described under [Shared files](files.md).

To get a file you kept managed again, ask `setup` for it, for example "Take the Makefile back into the sync".

Every plugin belongs to exactly one marketplace. To change it, or when its folder has moved, ask `setup`.

Plugins also get a Git hook that checks the standards before every commit. It runs only after you activate it once per clone: `git config core.hooksPath githooks`.

### Example

`/plugin-manager:setup` in an empty, cloned repository.

### Reads and writes

Reads the folder and the selected marketplace. Writes management files under `.project/`, one rule in `.gitignore`, the shared files, the writing style and, when creating, the skeleton. Creating a plugin or changing its marketplace also changes the selected marketplace folder, and a change touches the previous one too. Only shared files whose template was dropped are deleted: untouched ones automatically, changed ones only by your decision.


## verify

### Description

Reports whether a repository follows the rules, and what is not yet proven.

### Workflow

1. Detects plugin or marketplace itself.
2. Checks the structure, for plugins also the standards and shared instructions, and the documentation.
3. Reports a setup that is still open, without running it.
4. On request compares `SCOPE.md` with the source code.

### Example

`/plugin-manager:verify` before publishing.

### Reads and writes

Reads the repository. Writes nothing and runs no code of the repository. The same check runs in CI, including the documentation structure and, where a plugin keeps files in sync, the hash files.

---

Documentation prepared with Plugin Manager.
