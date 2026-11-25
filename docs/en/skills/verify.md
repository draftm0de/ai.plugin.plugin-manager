# 🛠 :verify

[Deutsch](../../de/skills/verify.md) | **English**

[Home](../../../README.en.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Concepts](../concepts.md) · [Development](../development.md) · [Shared files](../files.md)

## Description

Reports whether a repository follows the rules, and what is not yet proven.

## Workflow

1. Detects plugin or marketplace itself.
2. Checks the structure, for plugins also the standards and shared instructions, and the documentation.
3. Reports a setup that is still open, without running it.
4. On request compares `SCOPE.md` with the source code.

## Example

`/plugin-manager:verify` before publishing.

## Reads and writes

Reads the repository. Writes nothing and runs no code of the repository. The same check runs in CI, including the documentation structure and, where a plugin keeps files in sync, the hash files.

---

Documentation prepared with Plugin Manager.
