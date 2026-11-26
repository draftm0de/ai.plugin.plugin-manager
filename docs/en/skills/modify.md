# 🛠 :modify

[Deutsch](../../de/skills/modify.md) | **English**

[Home](../../../README.en.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Concepts](../concepts.md) · [Development](../development.md) · [Shared files](../files.md)

## Description

With `modify` you change what your repository says about itself: the technical name, the display name and the description. A marketplace has no description. First you see which files would change, including the marketplace entry. Nothing is written before your yes. The name and address of the repository stay, and `modify` does not rewrite the documentation.

## Workflow

1. Checks that the repository is set up.
2. Asks what should change.
3. Shows every affected file without writing.
4. Writes only after your yes.
5. Names the next steps: refresh the documentation with `docs`, commit and push the changes yourself.

### Questions from the workflow

| Question | What is it? | Mind |
| --- | --- | --- |
| Run /plugin-manager:setup now? | The setup is missing or incomplete | `modify` changes nothing before it is done. Call it again afterwards. |
| What should change? | Technical name, display name or description | A marketplace has no description. |
| What is the new value for `<field>`? | The new name or text | A new technical name changes the call forms and the installation. |
| May I write? | Above it stands the list of the files that change, also in the marketplace | On "No" everything stays as it is. |

## Example

"Give the plugin the display name Interview Coach."

## Reads and writes

Reads the configuration and the associated marketplace. Writes the manifests and, for a plugin, its marketplace entry if the marketplace folder is available on your machine. When you rename a marketplace, the affected plugins are only listed, not changed.
