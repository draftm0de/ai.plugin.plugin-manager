# 🛠 :setup

[Deutsch](../../de/skills/setup.md) | **English**

[Home](../../../README.en.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Concepts](../concepts.md) · [Development](../development.md) · [Shared files](../files.md)

## Description

You start here. `setup` configures your cloned repository as a plugin or a marketplace and asks you step by step for what it needs to know. The repository needs a GitHub address (`origin`); if it is missing, `setup` names the commands and stops. After that it keeps the shared files in sync. Before it writes, it names the files. If you changed one of them yourself, you decide whether your version stays or the template is adopted. You can call it again at any time.

## Workflow

1. Resolve the language.
2. Check the Git repository and `origin`.
3. Configure plugin or marketplace.
4. Add and update shared files: it first names the files and writes after your yes; for changed files you decide one by one. Afterwards it lists what it wrote.
5. One line "fully configured".

Which files are shared and what changing one means is described under [Shared files](../files.md).

To get a file you kept managed again, ask `setup` for it, for example "Take the Makefile back into the sync".

Every plugin belongs to exactly one marketplace. To change it, or when its folder has moved, ask `setup`.

Plugins also get a Git hook that checks the standards before every commit. It runs only after you activate it once per clone: `git config core.hooksPath githooks`.

### Questions from the workflow

`setup` asks only what it cannot know itself, always in the same words. What the questions mean:

#### Applies to both

| Question | What is it? | Mind |
| --- | --- | --- |
| Which operator language should I use? | The language the Plugin Manager talks to you in | Only for you, never committed. The documentation languages are independent of it. |
| Message: Git repository or GitHub address (`origin`) is missing | Your folder needs both | Run the commands shown and call `setup` again. The repository need not exist on GitHub yet. |
| Plugin or marketplace? | A plugin is the package of skills, a marketplace the directory people install from | Create the marketplace first, then the plugins. |

#### Marketplace

| Question | What is it? | Mind |
| --- | --- | --- |
| What is the technical name? | The identifier, for example in `plugin@marketplace` | Lowercase letters, digits and hyphens. Changeable with `modify`; whoever uses the marketplace adds it again afterwards. |
| What is the display name? | The readable name | Free to choose, changeable with `modify`. |
| Who is the publisher? | The person or organisation that publishes the marketplace | Part of the catalog and therefore visible. |

#### Plugin

| Question | What is it? | Mind |
| --- | --- | --- |
| What is the technical name? | The identifier, for example in `/name:skill` | Lowercase letters, digits and hyphens. The first skill skeleton has the same name; when building, give the skill its own. |
| What is the display name? | The readable name | Free to choose, changeable with `modify`. |
| What does the plugin do, in one or two sentences? | The description, also shown in the marketplace | "Still open" is allowed, changeable with `modify`. |
| Who is the publisher? | Who publishes the plugin | Visible. |
| Which documentation languages? | German, English or both, with a default | Each language means texts of its own to maintain. |
| Which licence? | What others may do with your code | MIT allows almost everything. Another licence needs its complete text. "Decide later" means that no rights are granted yet. |
| Which year goes into the copyright notice? (MIT only) | The year of the notice | |
| Who holds the rights? (MIT only) | Whom the rights belong to | This may differ from the publisher, for example your company. |
| Which marketplace does the plugin belong to? | The marketplace folder the plugin is listed in | It is cloned on your machine and set up with `setup`. Every plugin belongs to exactly one. |

#### When writing, and later

| Question | What is it? | Mind |
| --- | --- | --- |
| May I write? | Above it stands the list of all files that are created, changed or deleted. `../` means another repository, for example your marketplace. | On "No" none of it is written. |
| `<file>` differs from the template. | A shared file and its template are different | "Keep my file" leaves your version without updates until you change it again or a new template arrives. |
| The template of `<file>` is gone. | The Plugin Manager no longer ships this file | You are asked only if you had changed it. |

## Example

`/plugin-manager:setup` in an empty, cloned repository.

## Reads and writes

Reads the folder, its Git settings and the selected marketplace. Writes management files under `.project/`, one rule in `.gitignore`, the shared files, the writing style and, when creating, the skeleton. Creating a plugin or changing its marketplace also changes the selected marketplace folder, and a change touches the previous one too. Only shared files whose template was dropped are deleted: untouched ones automatically, changed ones only by your decision.
