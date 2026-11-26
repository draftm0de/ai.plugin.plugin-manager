# 🛠 :verify

[Deutsch](../../de/skills/verify.md) | **English**

[Home](../../../README.en.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Concepts](../concepts.md) · [Development](../development.md) · [Shared files](../files.md)

## Description

`verify` tells you whether your repository follows the rules. It detects by itself whether it is a plugin or a marketplace and checks structure, shared standards and documentation. On request it also compares `SCOPE.md` with the source code. It only reads: it changes nothing and runs no code of your repository.

## Workflow

1. Detects plugin or marketplace itself.
2. Checks the structure, for plugins also the standards and shared instructions, and the documentation.
3. Reports a setup that is still open, without running it.
4. On request compares `SCOPE.md` with the source code.

### What the report says

| Term | What does it mean? |
| --- | --- |
| Structure valid | Manifests, catalogs, skills and folders follow the rules. It says nothing about whether your skill does the right thing. |
| Local mapping incomplete | This machine lacks the path to the marketplace or the plugins. Normal after a fresh clone; needed for a local installation. |
| Standards | `AGENTS.md`, the shared standards and, in a marketplace, `SCOPE.md` are unchanged. |
| Documentation warnings | Missing pages, headings or links. They fail nothing. |
| Setup open | A shared file is missing or outdated: run `/plugin-manager:setup`. |
| Ready for source review | All evidence named in `SCOPE.md` can be read. It does not say that the requirements are met. |
| Not checked | Whether Claude or Codex load the plugin and how the skill behaves there. |

## Example

`/plugin-manager:verify` (Codex: `$plugin-manager:verify`) before publishing.

## Reads and writes

Reads the repository. Writes nothing and runs no code of the repository. The same check runs in CI, including the documentation structure and, where a plugin keeps files in sync, the hash files.
