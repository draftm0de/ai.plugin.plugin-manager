# Plugin Manager

[Deutsch](README.md) | **English**

<img src="assets/icon.png" alt="draftmode.io" width="48">

[Installation](docs/en/installation.md) · [Skills](docs/en/skills.md) · [Concepts](docs/en/concepts.md) · [Development](docs/en/development.md) · [Shared files](docs/en/files.md)

With the Plugin Manager your plugins are all built the same way: set up, documented, checked and published under your control.

## What it does

The Manager sets up plugin and marketplace repositories and keeps their shared files current. It gives every plugin the same standards for code, messages, tests and skills, writes the documentation from the sources, changes names and descriptions, checks the structure.

## Who it is for

For developers and teams who maintain skills as installable plugins for Claude or Codex and want all their plugins to follow the same rules.

## What it solves

Otherwise every new plugin starts from scratch: its own folders, its own rules, its own error messages, documentation that lags behind the code. The Manager lays the common ground, carries changes to it into each plugin and reports what deviates.

## Data and privacy

The Manager writes into the repository you select and, when a plugin is created, renamed, described or associated, into the folder of its marketplace. This covers management files under `.project/`, the shared files, documentation and, after your yes, changes to name or description. It never commits, pushes or publishes and reads no credentials or private data. What each skill reads and writes is listed with the skill. The AI host processes the sources under its own terms.

## Documentation

[Installation](docs/en/installation.md) · [Skills](docs/en/skills.md) · [Concepts](docs/en/concepts.md) · [Development](docs/en/development.md) · [Shared files](docs/en/files.md)

License: [MIT](LICENSE).

---

Documentation prepared with Plugin Manager.
