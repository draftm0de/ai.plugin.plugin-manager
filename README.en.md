# Plugin Manager

[Deutsch](README.md) | **English**

<img src="assets/icon.png" alt="draftmode.io" width="48">

[Home](README.en.md) · [Installation](docs/en/installation.md) · [Skills](docs/en/skills.md) · [Concepts](docs/en/concepts.md) · [Development](docs/en/development.md) · [Shared files](docs/en/files.md)

Plugin Manager is a plugin that lets you create, develop and maintain, in one standard way,

- **plugins** and
- **marketplaces**.

Its own skills (`:setup`, `:docs`, `:modify`, `:verify`) guide you through each step.

The manager also rolls out what your repository needs: shared files and folders, standards, check scripts, a `Makefile` and the GitHub CI. Before it writes, it names the files and asks you.

## ⚡ Quick start

### Installation

You add the marketplace once and install Plugin Manager from it.

#### Claude

- [Claude CLI](docs/en/installation.md#claude-cli)
- [Claude Desktop App](docs/en/installation.md#claude-desktop-app)

#### ChatGPT

- [Codex CLI](docs/en/installation.md#codex-cli)
- [ChatGPT Desktop App](docs/en/installation.md#chatgpt-desktop-app)

### Setup

`/plugin-manager:setup`

Your folder has to be a Git repository with a GitHub address (`origin`). The easiest way is to create the repository on GitHub and clone it.

Run `:setup` to configure your connected folder as a plugin or a marketplace. The skill guides you through the configuration with questions.

In Claude Code you call the skills as above. In Codex and ChatGPT you describe the task or pick the skill.

### Building a plugin

You do not need a skill call to develop. After the setup you open the folder of your plugin and simply describe what you want. Your repository brings the rules for the assistant with it: it reads `AGENTS.md`, your requirements in `SCOPE.md` and the shared standards for code, messages, tests and skills.

First you clarify what the plugin should and should not do, and record that in `SCOPE.md`. What you have not confirmed does not count as a requirement. Only then does the assistant build the skills under `skills/`, with tests. With `make verify` or `/plugin-manager:verify` you can check at any time that everything still follows the rules.

An example prompt:

```text
I want a plugin that turns my meeting notes into a task list.
Every task should have a responsible person and, if one is mentioned, a date.
First ask me what is unclear and record the requirements in SCOPE.md.
Build the skill only after I have confirmed the requirements.
```

## 🛠 Features

### :setup

Configures your repository as a plugin or marketplace and keeps its synced files in sync. Before writing it names the files and asks you.

📖 [/plugin-manager:setup – More](docs/en/skills/setup.md)

### :docs

Checks the structure of the documentation and creates missing `skills/<skill>.md` pages. You get a report of what is missing where and what each area should contain.

📖 [/plugin-manager:docs – More](docs/en/skills/docs.md)

### :modify

Changes the name, display name and description. Shows the changes first and writes only after your yes.

📖 [/plugin-manager:modify – More](docs/en/skills/modify.md)

### :verify

Checks, read-only, that structure, standards and documentation follow the rules.

📖 [/plugin-manager:verify – More](docs/en/skills/verify.md)
