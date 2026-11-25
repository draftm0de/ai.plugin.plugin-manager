# Documentation workflow

The rules of the `docs` action. Paths are relative to `skills/_shared/` unless explicitly rooted elsewhere.

## Action

- Re-read source evidence and use the documentation workflow below to refresh the configured languages.
- The documentation manifest locates source and owns documentation language settings.
- Preserve unrelated edits and media.

## Inputs and boundaries

### Source

- Accept a local skill directory containing `SKILL.md`, or a repository containing a skill. The folder must be accessible to the host. The user does not have to copy it into this plugin.
- Ask for the source only when it cannot be inferred from the current project. Ask which skill if several are found. Do not silently document the wrong one.
- For a hosted session without local access, request an uploaded source archive. Never claim that a Mac path exists in the cloud. Inspect uploaded files safely; do not execute their code.

### Output

- Use the requested repository as the output. If a standalone skill folder is supplied without an unambiguous output repository, inspect it first and ask where to write.
- Do not generate user documentation inside a distributable skill by default.

### Fixtures and screenshots

- Test fixtures must be explicitly fictional before reuse. Only use screenshots supplied/authorized for this documentation.

## Workflow

The documentation workflow, in order.

### 1. Read the rules

- Read the target's `docs/style.md` (writing style, owned by the repository; without it the gate stops `docs`).
- Read `references/documentation-layout.md`, `references/source-of-truth.md` and `references/evidence.md` in this shared directory.
- Read `scripts/verify/docs.py` for the exact structure and order.

### 2. Inspect the sources

Run the bundled helper with `inspect --source PATH` to list the documentation sources:

- every skill of the repository (`SKILL.md`, `references`, `flows`, `scripts` of each) and `SCOPE.md`, or the one skill folder when a standalone skill is documented
- a marketplace has no skills: it lists `marketplace.json`, `SCOPE.md`, `Makefile`, `CUSTOM.mk` and the workflows

Documentation is never tied to a single skill.

- Read SCOPE.md and shared development rules when present, distinguishing desired behavior from actual implementation; never rewrite scope as a side effect of update.
- Read the returned `SKILL.md`, relevant references and runtime files, plus public repository manifests, installer, Makefile, tests and existing documentation.
- Do not execute the source as part of inspection.

### 3. Clarify before drafting

- Before drafting, explain what the source appears to do and how it is used, distinguishing evidence from uncertainty.
- Ask concise, specific questions when purpose, intended audience, supported installation, output ownership or contradictory evidence materially affects the documentation.
- Continue independent inspection while awaiting replies; do not silently settle unresolved factual questions.
- Build a claim/evidence checklist in working context: purpose, audience, capabilities, modes, entry points, setup, storage, limitations, real test results, release state.
- Missing capability is documented as unavailable; missing evidence stays unverified.
- Check official current documentation before making host-specific installation or update claims, or link it and mark verification pending if browsing is unavailable.

### 4. Resolve the languages

Resolve the language policy **per target repository** before writing.

- Read `docs/documentation.json` → `documentation.languages` and `documentation.default_language`.
- Honor an explicit user choice, including English only.
- With no saved policy or clear instruction, ask whether to use German only, English only or both and which is the default; do not impose bilingual output.
- Existing manifests require explicit valid language settings; reject missing policy without inference.
- Read `references/languages.md`.
- Record the chosen settings once in the documentation manifest, never duplicate product facts.
- The default language uses `README.md`; a second language uses `README.<language>.md`. Guides live under `docs/<language>/`.
- Require counterpart links only for bilingual output. Use the selected localized headings from `scripts/verify/docs.py`.

### 5. Keep one source of facts

- Reuse an existing `docs/documentation.json` as a source locator and documentation configuration.
- It may contain source paths, unresolved questions and the single authoritative documentation language policy; it MUST NOT duplicate capabilities, versions, commands, privacy rules or generated summaries.
- Re-read the actual sources on every run.
- When a user clarifies a product fact, propose updating its canonical SKILL/reference/config location; write there only within authorization.
- Do not maintain a parallel factual manifest.

### 6. Scaffold

- Run `scaffold --source PATH --output REPOSITORY --title "Product name" --languages en --default-language en` for English-only output; use the saved policy when it exists.
- It creates missing pages only and copies the bundled ZYRIS icon to `assets/icon.png`.
- For installed plugins use `<plugin-root>/skills/_shared/scripts/documentation.py`; no developer checkout is required.
- The helper scaffolds structure; YOU must research and write the actual prose.

### 7. Fill the templates

- Fill the templates from evidence.
- On an existing repository, merge documentation deliberately: retain useful commands and caveats, move detailed information into linked pages, preserve unrelated docs and user edits.
- Do not replace existing custom assets silently.
- Keep exactly the required level-two sections in order; use level-three subsections for detail.
- Replace all `{{PLACEHOLDERS}}` and remove unsupported generic examples.

### 8. Icon and attribution

- Reference the plugin's own `assets/icon.png` in the documentation; the helper never copies an icon.
- Do not rewrite that project's plugin manifest or claim the source product is authored by ZYRIS; add a small "Documentation prepared with Plugin Manager" attribution.
- The icon's provenance is the user's supplied draftmode asset, not a generated or third-party image.

### 9. Fill the pages by their purpose

| Page | Content |
| --- | --- |
| `README` (plugin) | The start page of the repository, short and inviting. First, without a heading: what it is in one or two sentences, what you can do with it (a short list), and the skills by name. `Quick start`: how little it takes, in prose, then `### Claude` and `### ChatGPT` with one link per surface to its section of the installation page (`installation.md#claude-cli`, `#claude-desktop-app`, `#codex-cli`, `#chatgpt-desktop-app`; only sections that exist). `Features`: one `### :<skill>` per skill, an explanation of at most 200 characters in the person's words and a link `📖 [:<skill> – <more>](docs/<language>/skills/<skill>.md)` to its subpage. `Data and privacy`: what it reads and writes, in a few sentences. Sources: Purpose and Non-goals of `SCOPE.md`, confirmed requirements and the skill descriptions; never a draft as a feature. Show the draft and write it only after the person's yes. |
| `README` (marketplace) | What it offers and for whom, from `marketplace.json`. |
| `docs/<language>/skills.md` | The table of all skills: name (linking `skills/<skill>.md`) and one short purpose. |
| `docs/<language>/skills/<skill>.md` | One page per skill: description in plain words, workflow, one fictional example, what it reads and writes. It may go into detail with level-three headings. From `SKILL.md`, flows and source. |
| `docs/<language>/plugins.md` (marketplace) | One row per listed plugin. |
| `installation.md` | Not written by you: `scaffold` fills it from the repository's facts (plugin and marketplace name, marketplace address). |

When the answer of `scaffold` lists `missing_facts`:

- ask for the missing fact (the address as `https://github.com/<owner>/<name>`)
- record it as `marketplace_url` in `docs/documentation.json` and put it into the placeholders
- never invent a value or a host step

### 10. Validate

- Run `validate --output REPOSITORY` and fix missing pages, broken local links/images, unresolved placeholders, heading order and branding.
- Review commands against real source.
- For documentation-only work, use appropriate existing checks, not paid model calls or installations.
- Report what was checked and what remains unverified.

### 11. Summarize

- Summarize generated/updated paths and limitations.
- Documentation actions do not commit, push, publish, install or change visibility.

## Output contract

Produce the configured languages using the localized headings in `scripts/verify/docs.py`.

### Pages

- Default language: `README.md`; any additional selected language: `README.<language>.md`.
- Plugin, each selected language: `README`, `docs/<language>/installation.md`, `skills.md`, one `skills/<skill>.md` per skill, `concepts.md`, `development.md` (the last two are managed).
- Marketplace: the same with `plugins.md` instead of `skills.md`.
- Pages of the former structure (`usage`, `screens`, `faq`, `storage`, `docs/<language>/README.md`) are reported; they are never converted or deleted by the Manager.

### Languages

- English only means `README.md` plus `docs/en/`; no German pages or language switch are required. German only is equivalent under `docs/de/`.
- Supported template languages are currently de and en; ask before expanding that scope.

### Images

- Icon: the plugin's single `assets/icon.png`, referenced by the documentation and never copied.
- Generated illustrations only for selected languages under `docs/assets/<language>/`. Localize labels, captions, examples and alt text. For bilingual output, preserve equivalent content and layout.
- Real screenshots retain their actual UI language with a caption.

### Existing content

- Do not automatically delete unselected legacy pages or assets.
- Changing the default may require deliberate link and README migration; scaffold preserves existing pages and validate exposes remaining mismatches.
- Translated excerpts must be labelled as translations, not original model output.

### Limits

- This is a plugin workflow: the skill is a bundled capability inside the Claude/ChatGPT/Codex plugin, not a separate installation product.
- It generates GitHub Markdown, not a standalone website.
- It does not invent a marketplace, public release, license, backend or payment system.
