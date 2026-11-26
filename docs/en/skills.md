# 🛠 Skills

[Deutsch](../de/skills.md) | **English**

[Home](../../README.en.md) · [Installation](installation.md) · [Skills](skills.md) · [Concepts](concepts.md) · [Development](development.md) · [Shared files](files.md)

A skill is comparable to a work instruction for an employee.

It describes how the AI assistant is to carry out a certain task, which rules apply and which steps must be followed.

Plugin Manager comes with the following skills, one per task. In Claude Code you call them by their name. In Codex and ChatGPT you describe the task or pick the skill.

## 📖 Skills

### docs

`/plugin-manager:docs`

`docs` takes care of how your documentation is built. It creates some of the pages itself; for the others you write the texts and only the structure matters. It creates missing pages. What does not fit is reported to you.

Which pages these are and what is checked depends on whether your repository is a plugin or a marketplace. `docs` detects that itself.

📖 [/plugin-manager:docs – More](skills/docs.md)

### modify

`/plugin-manager:modify`

With `modify` you change what your repository says about itself: the technical name, the display name and the description. A marketplace has no description. First you see which files would change, including the marketplace entry. Nothing is written before your yes. The name and address of the repository stay, and `modify` does not rewrite the documentation.

📖 [/plugin-manager:modify – More](skills/modify.md)

### setup

`/plugin-manager:setup`

You start here. `setup` configures your cloned repository as a plugin or a marketplace and asks you step by step for what it needs to know. After that it keeps the shared files in sync. Before it writes, it names the files. If you changed one of them yourself, you decide whether your version stays or the template is adopted. You can call it again at any time.

📖 [/plugin-manager:setup – More](skills/setup.md)

### verify

`/plugin-manager:verify`

`verify` tells you whether your repository follows the rules. It detects by itself whether it is a plugin or a marketplace and checks structure, shared standards and documentation. On request it also compares `SCOPE.md` with the source code. It only reads: it changes nothing and runs no code of your repository.

📖 [/plugin-manager:verify – More](skills/verify.md)

<hr>

This page is created automatically by `/plugin-manager:docs`. Do not edit it by hand.
