# 🛠 :setup

[Deutsch](../../de/skills/setup.md) | **English**

[Home](../../../README.en.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Concepts](../concepts.md) · [Development](../development.md) · [Shared files](../files.md)

## Description

You start here. `setup` configures your cloned repository as a plugin or a marketplace and asks you step by step for what it needs to know. After that it keeps the shared files in sync. Before it writes, it names the files. If you changed one of them yourself, you decide whether your version stays or the template is adopted. You can call it again at any time.

## Workflow

1. Resolve the language.
2. Configure plugin or marketplace.
3. Add and update shared files: it first names the files and writes after your yes; for changed files you decide one by one. Afterwards it lists what it wrote.
4. One line "fully configured".

Which files are shared and what changing one means is described under [Shared files](../files.md).

To get a file you kept managed again, ask `setup` for it, for example "Take the Makefile back into the sync".

Every plugin belongs to exactly one marketplace. To change it, or when its folder has moved, ask `setup`.

Plugins also get a Git hook that checks the standards before every commit. It runs only after you activate it once per clone: `git config core.hooksPath githooks`.

## Example

`/plugin-manager:setup` in an empty, cloned repository.

## Reads and writes

Reads the folder and the selected marketplace. Writes management files under `.project/`, one rule in `.gitignore`, the shared files, the writing style and, when creating, the skeleton. Creating a plugin or changing its marketplace also changes the selected marketplace folder, and a change touches the previous one too. Only shared files whose template was dropped are deleted: untouched ones automatically, changed ones only by your decision.

---

Documentation prepared with Plugin Manager.
