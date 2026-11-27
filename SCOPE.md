# Current-format policy / Aktuelle Formate

Status: confirmed

This scope records the approved compatibility boundary and creation interaction requirements, not a complete product acceptance. Every requirement states only the current target; history lives in Git. Requirement ids are stable and never reused; R19, R29 and R49 were withdrawn.

## R1: No backwards compatibility

Status: confirmed
Acceptance: Only current documented formats and entry points are supported. Reject obsolete formats without automatic inference, migration or modifying user data.
Source: skills/_shared/WORKFLOWS.md
Source: scripts/plugin.py
Source: skills/_shared/scripts/workflows.py
Source: skills/_shared/scripts/documentation.py
Test: tests/integration/update/test_documentation.py
Test: tests/integration/plugin_create/test_workflows.py
Test: tests/integration/test_shared_installer.py

## R2: Resolve the licensing decision before plugin creation

Status: confirmed
Acceptance: Before creation writes, the agent reuses an unambiguous existing target license or explicit session decision; otherwise it asks for a license or explicit deferral and waits for the answer. Conflicts require clarification and existing license content is preserved. Silence is not deferral. The completion report identifies a deferred decision as unresolved and distinguishes a selected license from files actually created.
Source: skills/setup/flows/configure.md
Source: skills/_shared/references/workflows.md
Test: tests/behavior/plugin_create_acceptance.md

## R3: Separate conversation language from documentation language

Status: confirmed
Acceptance: Creation through the setup skill uses the project-scoped operator-language gate of R12/R14. Documentation languages are resolved independently and never determine the operator language implicitly. The former standalone plugin creation entry is removed.
Source: skills/setup/flows/configure.md
Source: skills/_shared/references/workflows.md
Test: tests/behavior/plugin_create_acceptance.md

## R4: Complete skeleton documentation and report creation checks

Status: confirmed
Acceptance: New skeleton documentation contains localized, evidence-based scaffold content without unresolved placeholders for every selected language. No domain capabilities or test success are invented. Existing user prose is preserved and its validation failures remain visible. Creation checks actual plugin and marketplace structure and documentation, reports their results separately from licensing, pending functional acceptance and unexecuted tests/host checks, and does not claim completion on failed checks.
Source: skills/_shared/scripts/workflows.py
Source: skills/setup/flows/configure.md
Test: tests/integration/plugin_create/test_workflows.py

## R5: Guided plugin creation dialogue

Status: confirmed
Acceptance: Missing setup inputs are collected using the host's available structured question tool in small coherent groups. Unknown conversation language is asked alone first and the agent waits before continuing in that language. Confirmed inputs are not asked again. When no structured tool is available, the agent explains this limitation and asks one concise question at a time in chat instead of dumping a questionnaire. No target writes occur while required answers are missing.
Source: skills/setup/flows/configure.md
Source: skills/_shared/references/workflows.md
Test: tests/behavior/plugin_create_acceptance.md

## R6: Implement confirmed licensing and persist the decision

Status: confirmed
Acceptance: `create --kind plugin` requires an explicit license identifier or explicit deferral before writes. A selected MIT license creates the standard license with confirmed copyright year and holder; another selected license uses an explicitly confirmed complete file without alteration. Missing inputs, unsupported templates and conflicting existing license files fail before plugin/marketplace writes. Existing matching license bytes are preserved. Selected licensing appears in plugin and derived host manifests, and the decision is persisted with its license file in `docs/license.md`; no README gets a license line. Explicit deferral is persisted without claiming a license. Final checks distinguish implemented, deferred and inconsistent licensing; existing prose is preserved and missing licensing documentation is reported.
Source: skills/_shared/scripts/licensing.py
Source: skills/_shared/scripts/workflows.py
Source: skills/setup/flows/configure.md
Test: tests/integration/plugin_create/test_licensing.py

## R7: Repeated creation detects existing products before license validation

Status: confirmed
Acceptance: An existing target product is rejected before licensing validation or creation writes, even with missing/conflicting licensing arguments. Unknown conversation language is resolved alone before offering existing-plugin actions; known language is used exclusively. The setup skill does not recreate an existing plugin; after language/skeleton handling it reports ready and waits under R12/R14. The former standalone existing-plugin action dialog is removed. Existing files and marketplace entries remain unchanged.
Source: skills/_shared/scripts/workflows.py
Source: skills/setup/flows/configure.md
Source: skills/_shared/references/workflows.md
Test: tests/integration/plugin_create/test_workflows.py
Test: tests/behavior/plugin_create_acceptance.md

## R8: Skeleton-only plugin creation

Status: confirmed
Acceptance: `create --kind plugin` creates only a new nonfunctional skeleton. Its dialogue offers no skill import or mode choice and requests no source skill path. The public helper rejects --source and --import before writes, including when combined with --skeleton. Other actions retain their own source-reading options. Existing source directories and target/marketplace data remain unchanged on rejected import calls.
Source: skills/_shared/scripts/workflows.py
Source: skills/setup/flows/configure.md
Source: skills/_shared/references/workflows.md
Test: tests/integration/plugin_create/test_workflows.py
Test: tests/behavior/plugin_create_acceptance.md

## R9: Project-scoped operator language for generated plugins

Status: confirmed
Acceptance: Every newly generated plugin ships the shared operator-language helper and its reference. Before setup/domain interaction, a missing project preference is asked alone and persisted only after an explicit answer. Later calls reuse it, including bare slash commands and new sessions. An explicit change updates only that project's preference. Content/documentation languages remain independent; invalid state is rejected without mutation. Future skills preserve the same gate. The reference opens with the section "How a skill uses the language": the language comes only from the helper's `operator_language`, everything the person reads (previews, questions, answer labels, results, finished failure messages) is written in it, a script that prints text for the person receives it, and an unknown language is resolved first; the standards (`skills.md`) make this section binding for every skill, whose own text does not repeat it.
Source: skills/_shared/templates/plugin/sync/skills/_shared/scripts/operator_language.py
Source: skills/_shared/templates/plugin/sync/skills/_shared/references/operator-language.md
Source: skills/_shared/templates/plugin/sync/skills/_shared/references/operator-language-helper.md
Source: skills/_shared/scripts/workflows.py
Test: tests/integration/plugin_create/test_workflows.py
Test: tests/behavior/operator_language_acceptance.md

## R10: Manager copy and delivery of the operator-language building block

Status: confirmed
Acceptance: The generator template remains the canonical source of the operator-language helper and reference; the Manager ships byte-identical standalone copies under skills/_shared/ as a delivery requirement. Their only Manager use is the setup skill, which is separately authorized by R11; no other workflow uses them. The plugin generator template ignores exactly /.project/operator.json (no blanket .project/ rule, no duplicates); only newly created plugin repositories receive it, while marketplace repositories and existing plugins configured later keep their .gitignore. `create --kind plugin` ships helper and reference, never runs the helper and stores no preference. The helper does not edit .gitignore. Entry-point use (only R11's setup entry), skeleton sync and adoption by other plugins are not part of this requirement.
Source: skills/_shared/scripts/operator_language.py
Source: skills/_shared/references/operator-language.md
Source: skills/_shared/scripts/workflows.py
Test: tests/unit/operator_language/test_validation.py
Test: tests/integration/operator_language/test_cli.py
Test: tests/integration/plugin_create/test_operator_language_delivery.py

## R11: The setup skill sets up operator language and missing shared development files

Status: confirmed
Acceptance: The setup skill (/plugin-manager:setup), for an explicitly selected folder (never the installation of the running Manager; the Manager's own repository is a normal plugin), checks operator language and the closed list of managed files of the configured kind (R16) without writes, stops on technical conflicts before any write, asks for a missing language, then adds only missing files/folders from the generator template, ensures the exact ignore rule /.project/operator.json before the first language write, stores the language through operator_language.py and records, per verified path, the pair {source_hash, local_hash} of full SHA-256 hashes in .project/plugins/plugin-manager/skeleton.json (schema_version 2, the only supported format: an older, unknown or invalid file is rejected before writes and left unchanged, never migrated; the former .project/plugin.skeleton.lock.json is an unsupported location). The skeleton setup copies missing files and corrects missing or stale pairs of template-identical files; it never changes the bytes of an existing file. Existing files that differ are only changed by the explicit sync decision of R12; the only other files setup may modify are .gitignore (adding the exact rule) and .project/operator.json, each as specified. Technical errors (symlink, wrong type, unreadable, filesystem errors) are reported as such, never as content deviations, and stop further writes while actual partial changes stay listed. Concrete read-only requests only run the status. The state helper runs no Git; setup installs nothing, uses no network and runs no target code, and its only Git use before a generator is the read-only check of R12. Other plugins and host activation by slash command are not part of this requirement; updating and removing existing files is governed only by R12.
Source: skills/setup/scripts/setup_state.py
Source: skills/setup/SKILL.md
Test: tests/integration/project_setup/test_setup.py
Test: tests/contracts/test_plugin_manager_entry.py

## R12: The setup skill dispatches by state: language, configuration, skeleton, sync

Status: confirmed
Acceptance: /plugin-manager:setup reads a write-free status of an explicitly selected folder and runs exactly the needed flow, re-checking after every successfully completed flow. Priority as in R17: technical conflict (stop), operator language missing (language flow), configuration evidence missing (configuration flow), skeleton additions or skeleton evidence missing (skeleton flow), a managed file needing a keep/adopt decision (sync flow), otherwise ready. The skeleton is the sync list of the configured kind (R16) with parent folders, the ignore rule and skeleton evidence; it needs no plugin.json or marketplace and invents no identity. An acting call of setup (not a read-only request) first settles the operator language; then, before any further question or write, it checks, write-free and the same for both kinds, that the folder is itself a Git repository with a GitHub address as origin; otherwise it stops with one message that names only the missing commands, with the folder name as the suggested repository name, in the saved operator language whatever language the call names. Setup never runs these commands. A folder without plugin.json is accepted when it holds only .git/.idea (checked as directories, never opened), a regular UTF-8 .gitignore, valid .project metadata and skeleton paths, including the entry's own earlier output; other content, an invalid plugin.json or the embedded Manager stop before writes. Sync rules per managed file: missing locally, copy from a valid source and record both hashes after verification; source and local identical, correct a missing or stale pair without a dialogue; source and local differ and the stored pair equals the current pair (source_hash and local_hash both), the deviation is accepted without dialogue or writes; source or local changed since the accepted pair (or no pair, or no lock) while contents differ, a decision is required and nothing is overwritten automatically. Status reports path, hashes, reason and decision need structurally and asks nothing; the skill shows only the file path and the fact that differences exist, without file contents, text excerpts, diffs or content summaries, and explicitly asks for "keep local file" or "adopt template" in the operator language. Keep leaves the local bytes and records both current hashes; adopt replaces only the explicitly selected file (mode kept), verifies it and records both hashes. Cancellation, silence or a preselection is no decision and persists nothing; a decision holds only for the shown pair and a changed pair stops for a new check. Removal rules for a managed path whose source was removed in the parent template (a single missing source of a listed path, while the template base exists and holds at least one managed source; a missing or invalid base, symlinks, wrong types and read errors are technical conflicts, never removal): the file is deleted automatically only if the lock proves ownership and the current local hash equals the stored local_hash and the stored source_hash; a changed or accepted local file always requires an explicit "keep local file" or "delete local file" question (no content, excerpt, diff or summary is shown, only the path and that the source was removed); without lock evidence nothing is deleted; a locally missing owned file only loses its lock entry; keep records source_hash null with the current local_hash (a documented extension of lock schema_version 2, set only by this decision), so an unchanged repetition does not ask again and a later local change does; a returning source is classified normally again. After removal only empty parent folders of the removed file go, bottom-up with rmdir, never needed skeleton folders, the project root, .git, .idea or .project, and foreign files are never deleted. Status reports automatic removals, questions, kept files, unowned files and lock cleanup separately, writes nothing, and the skeleton flow executes the automatic part. Folders are not hashed or moved, extra local files are kept, AGENTS.md is not managed and new managed files need an entry in the fixed list; a removed source stays recognizable only while its path remains in that list. For the explicitly requested manual sync test, keep.md and remove.md are in that list. Accepted deviations cause no sync routing and never mean matches_template; ready is not product acceptance. Configuration runs after language and before the skeleton (R17) in the same call and folder through the existing `create --kind plugin` generator and its rules, with inputs, GitHub origin and marketplace asked or reported as external prerequisites, never invented, rolled back or changed without explicit selection; a generator collision with a deviating or deliberately kept skeleton file changes nothing and stops openly, to be resolved only by the sync flow. Read-only requests run one status only. Errors and missing progress stop with concrete reasons and actual partial changes; ready waits for input. Dialogue and flow text is instruction evidence, not model or host behavior; concurrent writers are organizationally excluded.
Source: skills/setup/scripts/setup_state.py
Source: skills/setup/SKILL.md
Source: skills/setup/flows/language.md
Source: skills/setup/flows/skeleton.md
Source: skills/setup/flows/configure.md
Source: skills/setup/flows/sync.md
Source: skills/setup/flows/entry.md
Source: skills/_shared/scripts/workflows.py
Test: tests/integration/plugin_create/test_prerequisites.py
Test: tests/integration/project_setup/test_fresh.py
Test: tests/integration/project_setup/test_sync.py
Test: tests/integration/project_setup/test_removal.py
Test: tests/contracts/test_plugin_manager_entry.py

## R13: Managed Claude compatibility file

Status: confirmed
Acceptance: The plugin generator and the skeleton flow of the setup skill share a CLAUDE.md template containing only an English compatibility comment and @AGENTS.md. All agent instructions belong in AGENTS.md. Missing CLAUDE.md is copied and its hash pair recorded in the skeleton lock, identical content is preserved and recorded, and existing different content is preserved until an explicit sync decision (R12) keeps or replaces it; it is never overwritten automatically. A fresh folder containing this skeleton file remains initializable. AGENTS.md is not added to skeleton management.
Source: skills/_shared/templates/plugin/sync/CLAUDE.md
Source: skills/setup/scripts/setup_state.py
Test: tests/integration/project_setup/test_setup.py
The same compatibility CLAUDE.md applies to every kind (plugin, marketplace) and to this repository itself; a differing "Project instructions" variant is not used.

## R14: Creation through the setup skill

Status: confirmed
Acceptance: Plugin creation has no separate public plugin creation skill or command wrapper. The configuration flow of the setup skill owns the guided creation instructions and uses the existing internal `create --kind plugin --skeleton` generator. Licensing, preservation and creation checks remain required. Existing marketplace associations are handled by the associate flow of R21 (the former configure skill is removed). Creation uses the saved operator-language gate of R12; former standalone entry dialogue rules do not create another public entry.
Source: skills/setup/flows/configure.md
Test: tests/contracts/test_skill_entrypoints.py
Test: tests/contracts/test_plugin_manager_entry.py

## R15: Workpackage configuration evidence per running plugin

Status: confirmed
Acceptance: The setup skill keeps the configuration evidence in the workpackage under .project/plugins/plugin-manager/config.json (the helper receives the plugin name as --plugin plugin-manager). Format: {schema_version: 2, plugin, kind, artifact, configured_at, marketplace}; kind is plugin or marketplace (the kinds of the manifests); artifact is the name of the created plugin or marketplace; configured_at is an ISO-8601 UTC timestamp; marketplace is {name} (the name is the identity of a marketplace; it has no repository of its own) for a kind whose manifest says requires_marketplace (plugin) and null for every other kind. The file is committed; schema_version 1 and a missing, partial or unexpected marketplace property are an unsupported format (conflict before any write, unchanged, no migration). A plugin belongs to exactly one marketplace, so its configuration is complete only with that identity (R21); ready therefore includes the association, without a further gate. The machine-specific path of that marketplace is never part of this file: it lives in the Git-ignored .project/plugins/<plugin>/local.json ({schema_version: 1, marketplace_path}, strictly validated). The file is written only after a successful configuration run (generator checks passed) and never earlier. A workpackage is configured for a plugin only if this file is valid; a root plugin.json or marketplace.json is a product, never evidence. Evidence of other plugins (other folders under .project/plugins/) does not configure this one. Missing, unreadable, extra-key, wrong-type, unknown-kind or plugin-mismatching files are reported as conflicts before any write, leave all data unchanged and are never migrated. Status reports configuration {plugin, configured, kind}. The helper operation record writes the file only after a passed configuration run and, for a kind with requires_marketplace, only if local.json names a marketplace checkout whose marketplace.json lists the plugin (name and the plugin's repository URL); it takes the identity {name} from that checkout and otherwise refuses with association_missing ("associate first") without writing.
Source: skills/setup/scripts/setup_state.py
Source: skills/setup/SKILL.md
Test: tests/integration/project_setup/test_workpackage_config.py

## R16: Skeleton per kind: sync/ and seed/ folders, generated hash file, manifest

Status: confirmed
Acceptance: Every kind has two template folders: skills/_shared/templates/<kind>/sync/<project path> (files kept in sync: copied 1:1, hashed in .project/plugins/<plugin>/skeleton.json, schema_version 2, and synchronized under the keep/adopt/delete rules of R12) and skills/_shared/templates/<kind>/seed/<project path> (files created once when missing, with a short intro of what the file is for, never what it does; never hashed or synced). The folder a file lies in is the only statement of its class. skills/_shared/manifests/<kind>.json is only {schema_version: 1, product, requires_marketplace, derived: [{path, generate, check}]} (product = root file naming the kind or null; requires_marketplace = boolean, true only for the kind plugin; derived = catalogs produced by a named command of the kind and only verified by its check command, never copied or hashed). skills/_shared/manifests/<kind>.sync.json is generated, never edited by hand: {schema_version: 1, files: {<path>: {sha256, executable}}, removed: [<path>]}, sorted, with a trailing newline. files lists exactly the files of sync/ (full SHA-256 of the bytes, executable bit); removed lists tombstones, paths whose template source was removed in the parent (plugin: keep.md, remove.md), and may not overlap files. The development tool scripts/build_hashes.py (make build-skeleton-hashes, which keeps removed) writes the file and scripts/verify/hashes.py verifies it (check exits 1 naming each path on a hash or executable mismatch, a missing or unlisted file, an invalid file or an overlap); the same comparison runs in CI as part of verify (R47). The helper trusts the file only as the expected value: before copying or comparing it hashes every source of sync/ and refuses with a template_base conflict (reason names make build-skeleton-hashes) on a deviating or missing source of a listed path, an unlisted file in sync/, an invalid sync file or an overlap, and writes nothing. The removal rules of R12 apply only to paths in removed. Templates and manifests carry -text in .gitattributes so line endings never change a hash. The kind marketplace has sync = AGENTS.md, CLAUDE.md, SCOPE.md (R41), the concepts pages (R36), the development pages (R42), Makefile (R43), docs/prerequisites.md, tests/README.md and .github/workflows/dm-verify.yml (R44), scripts/{local_plugins,marketplace,plugin_payload,run_tests,verify}.py and the tests of R40; seed = CUSTOM.mk, CUSTOM.AGENTS.md, docs/architecture.md, local-marketplace.example.json, tests/__init__.py, tests/contracts/__init__.py, tests/contracts/test_structure.py; derived = .claude-plugin/marketplace.json and .agents/plugins/marketplace.json (marketplace.py sync / check). The kind plugin has AGENTS.md, CLAUDE.md, Makefile (R43), docs/prerequisites.md, tests/README.md, .github/workflows/dm-verify.yml (R44), the standards under docs/standards/, scripts/plugin.py, scripts/run_tests.py, scripts/verify.py and the operator-language building block of R9/R10 in sync/; the setup flows and project_setup.py are no part of a generated plugin. Its seed/ holds the generator files (CUSTOM.AGENTS.md, SCOPE.md, CUSTOM.mk, gitignore.txt, assets/icon.png as a neutral placeholder, docs, tests). The former .project/plugin.skeleton.lock.json is an unsupported location (no read, migration or deletion). The ignore rules written by the generators are /.project/operator.json (new plugin repositories only) and /.project/plugins/*/local.json (every plugin repository where the association is written; effectiveness is checked with Git before writing); the marketplace side keeps .local/. A managed file that was an exact copy of the source at the last sync and is untouched since (its source changed, the local file did not) is updated by `setup` without a question, named by path; a file that was edited or deliberately kept (keep) is never replaced silently and comes as a decision under R12.
Source: skills/setup/scripts/setup_state.py
Source: scripts/build_hashes.py
Source: skills/setup/scripts/state/context.py
Test: tests/integration/project_setup/test_workpackage_config.py
Test: tests/integration/project_setup/test_manifest.py
Test: tests/integration/project_setup/test_sync_files.py
Test: tests/unit/skeleton_hashes/test_skeleton_hashes.py
## R17: Dispatch order and kind selection

Status: confirmed
Acceptance: The status priority is: technical conflict (stop), operator language missing (language), workpackage not configured for the running plugin (configure), skeleton additions or evidence missing (skeleton), managed file needing a decision (sync), otherwise ready. The configure flow first asks "plugin or marketplace?" (explicit answer, no preselection); plugin starts the plugin setup flow, marketplace the marketplace flow (R20); an existing root plugin.json is named and stops the plugin branch. A marketplace.json in the root is no conflict once the kind is marketplace. The generator creates only product files and never touches, judges or fails on existing managed skeleton files; skeleton differences are resolved by the skeleton and sync flows after the configuration evidence exists. Flow success is re-checked by status; after configuration both the evidence of R15 and the skeleton files of the chosen kind exist.
Source: skills/setup/scripts/setup_state.py
Source: skills/setup/SKILL.md
Source: skills/setup/flows/configure.md
Test: tests/integration/project_setup/test_workpackage_config.py
Test: tests/contracts/test_plugin_manager_entry.py

## R18: Ready output

Status: confirmed
Acceptance: When status is ready, the setup skill outputs only the line "<Kind> <name> Status: fully configured" (`<Kind>` is "Plugin" or "Marketplace" according to the configured kind; `<name>` is the configured plugin or marketplace repository from the status answer, not the running Manager) in the operator language (German: "<Kind> <name> Status: vollständig konfiguriert") and waits. Skeleton deviations and other details are not listed unless asked.
Source: skills/setup/SKILL.md
Test: tests/contracts/test_plugin_manager_entry.py

## R20: Marketplace setup is part of the setup skill

Status: confirmed
Acceptance: The marketplace setup is a flow of the setup skill; there is no skill skills/marketplace-create and no commands/marketplace-create.md. The complete procedure is skills/setup/flows/marketplace.md (no reference to a separate skill). flows/configure.md asks "Plugin or marketplace?" first (R17), holds the dialogue rules shared by both kinds (section "Guided dialogue (both kinds)") and hands over to flows/marketplace.md for the marketplace. The cloned marketplace folder is the working folder. Technical name (kebab-case), display name and owner/publisher are asked one at a time or in small coherent groups, never invented and never taken from the Git author; an existing marketplace.json supplies missing values ; the marketplace needs a Git repository with a GitHub address as origin (R12) but records no repository of its own. Nothing is written before the facts are answered. The helper call is workflows.py create --kind marketplace --root <folder> --name ... --display-name ... --owner ...; success is exit 0 (the answer carries action, changed and published: false, but no ok or checks), then record --kind marketplace --artifact <name> writes the configuration evidence, then status leads to the skeleton flow (hash evidence) and ready. Repeating the operation is idempotent; an identity conflict stops without writes; a plugin repository (plugin.json) is no marketplace. As in R17 the generator neither judges nor replaces an existing synced file listed in manifests/marketplace.sync.json (a deviating one stays byte-identical and surfaces as a sync decision afterwards); seed files never change existing files. The generated starter READMEs name only existing commands (python3 -B scripts/verify.py, python3 -B scripts/marketplace.py sync|check, make install-local), never removed make targets.
Source: skills/setup/flows/marketplace.md
Source: skills/setup/flows/configure.md
Source: skills/_shared/scripts/workflows.py
Test: tests/contracts/test_plugin_manager_entry.py
Test: tests/contracts/test_skill_entrypoints.py
Test: tests/integration/marketplace_create/test_workflows.py

## R21: Marketplace association is a flow of the setup skill; a plugin belongs to exactly one marketplace

Status: confirmed
Acceptance: A plugin belongs to exactly one marketplace; that is a mandatory property of its configuration (R15): the committed config.json carries the identity {name}, the Git-ignored .project/plugins/plugin-manager/local.json ({schema_version: 1, marketplace_path}, strict) the path of the checkout on this machine. The former plugin-side .local/marketplace.json (default marketplace and named associations) is neither written nor read, there is no fallback and no migration; the marketplace side keeps the checkouts of its plugins under sources in its own .local/marketplace.json. The association is the flow skills/setup/flows/associate.md; there is no skill skills/configure and no commands/configure.md, and the helper operation configure is replaced by workflows.py associate --root <plugin> --marketplace <local path of the target marketplace> [--plugin plugin-manager] [--drop-missing-old]. associate requires the configuration evidence (schema 2) of a kind with requires_marketplace and a plugin.json whose name equals the artifact; it validates the target structurally as a marketplace (marketplace.json with a name at its root, no plugin.json, valid catalogs; no configuration evidence of the target is required), plugin and marketplace are separate repositories, the plugin identity must not belong to another repository, neither .local of the marketplace nor local.json of the plugin may be tracked and the ignore rules must be effective. The same marketplace (same name) is idempotent: a fresh clone or moved checkout only gets its local.json. The same checkout under a new name (the path the plugin already records in local.json leads to this checkout, which lists the plugin; the marketplace was renamed, R24) is an identity update of the same marketplace: only the identity in config.json changes, no catalog entry, and no other marketplace is involved. Changing to another marketplace writes in ONE rollback-capable transaction: entry and sources of the plugin in the new marketplace, removal of exactly this plugin's entry (matching name and the plugin's repository URL) and of its sources mapping from the old marketplace, both host catalogs of both marketplaces regenerated, the identity in config.json and the path in local.json. The old marketplace is found through local.json and must carry the name of the identity; if it is not available locally the change is refused unless --drop-missing-old is given, which releases only the local reference and the identity and reports old_catalog_entry_remains: true because the committed catalog line of the old marketplace has to be removed there. The first association happens through plugin creation, which validates the marketplace exactly like associate (a name at its root) before any file is written and then writes local.json and refuses an existing association to another marketplace ("use associate to change"). associate creates no development tools, never commits, pushes, installs or publishes; its answer has action, changed, from, to, published: false, old_catalog_entry_remains and a note that the changed files (config.json of the plugin, marketplace.json and host catalogs of the marketplaces involved) are committed files left unversioned; the person commits and pushes them. project_setup status reports for a kind with requires_marketplace the read-only field association {marketplace, path, state: ok|path_missing|path_invalid|mismatch|unsupported}; it never gates ready, never writes and treats a missing local.json (fresh clone) as a hint only. The setup skill routes a request to set, change or move the marketplace of a plugin, after the language gate, to the flow, which asks the local path of the target marketplace as an explicit choice (a suggestion is not a selection). The read-only verification reads the path only from local.json; its messages name the plugin-manager association instead of "configure". A plugin repository has no local installation of its own (R43).
Source: skills/setup/flows/associate.md
Source: skills/setup/SKILL.md
Source: skills/_shared/scripts/workflows.py
Source: skills/setup/scripts/setup_state.py
Test: tests/integration/associate/test_associate.py
Test: tests/integration/associate/test_workflows.py
Test: tests/integration/modify/test_modify.py
Test: tests/integration/project_setup/test_association_status.py
Test: tests/integration/project_setup/test_workpackage_config.py
Test: tests/contracts/test_plugin_manager_entry.py
Test: tests/contracts/test_skill_entrypoints.py

## R22: Uniform generator operations

Status: confirmed
Acceptance: The generator CLI skills/_shared/scripts/workflows.py has exactly the operations `create --kind marketplace|plugin` and `associate`. The former subcommands marketplace-create, plugin-create and configure do not exist and are invalid calls (exit 2, no alias, nothing written). `create` requires a known `--kind`; arguments of the other kind (kind marketplace: --marketplace, --skeleton, --description, --author, --languages, --default-language, --license, --license-file, --copyright-year, --copyright-holder; kind plugin: --owner, and --marketplace is required) are invalid calls before any write (exit 2). The answers name their operation in `action`: create-marketplace, create-plugin, associate. The Python operations are create_marketplace, create_plugin and associate. Test groups and test folder names keep their historical names (plugin-create, plugin_create, marketplace_create); they name test areas, not operations. Source/test names in this document that mention an operation use the new names.
Source: skills/_shared/scripts/workflows.py
Source: skills/setup/flows/configure.md
Source: skills/setup/flows/marketplace.md
Test: tests/integration/plugin_create/test_create_cli.py

## R23: Skill set of the Manager: setup, docs, modify, verify

Status: confirmed
Acceptance: The Manager offers exactly four public skills, each invoked as `/plugin-manager:<skill>`; the call selects the instructions, no first-argument routing exists. The former skills `plugin-manager`, `update` and `publish` and the commands plugin-verify and marketplace-verify do not exist (R1, no alias). A skill never performs the task of another one. No skill commits, pushes or publishes: the person does that. The kind (plugin or marketplace) is never a call argument: `setup` asks it once (R17), `docs` and `modify` read it from the configuration evidence (R15), `verify` detects it (`--kind auto`, ambiguous roots are rejected) and accepts an explicit `--kind`.
- `setup`: the state-guided skill (R11, R12, R17, R18, R21). It is the only skill that brings a repository into the configured state: operator language, configuration, skeleton, template sync, marketplace association. It may be called repeatedly; on a configured and synchronous repository it only prints the ready line (R18).
- `docs`: creates and refreshes README and docs/<language>/ from the actual sources in the repository-selected languages (R4); invents no capabilities or test results and preserves existing user prose. It places and links only screenshots the person supplied or authorized and does not generate screenshots.
- `modify`: changes name, display name and description of a plugin or marketplace (R24).
- `verify`: read-only structural verification and the explicit `--review` scope/source comparison; no writing helper, no target code execution. A passed check is no product acceptance.
- State rule: every skill first runs the read-only `status`. `setup` runs the open flow. `docs` and `modify` stop with the reason and a pointer to `/plugin-manager:setup` when `next` is not `ready`, and write nothing. The stop message of `docs` and `modify` follows the mandatory layout of R25 (running text: "The <action> action was stopped, because this folder is not set up yet or only partly (<plain reason>).", a blank line, "Please run `/plugin-manager:setup` first."), delivered by `gate` as `message` and written unchanged, then, when the host offers a structured question tool, one question with two answers (run `/plugin-manager:setup` now: yes or no); on yes the skill hands over to `setup` and ends, on no or without an answer it ends, and it never runs a setup flow itself; the message is written in the language of the person's text in that call (labels and sentences translated) and in English for a bare command; it stores nothing, asks nothing and never guesses a language (the operator language stays with `setup`, R9/R10). `verify` continues and reports a pending setup or sync as a finding. Only `setup` writes the configuration evidence, skeleton files and sync decisions.
- The five skill descriptions name their task and boundary; `setup` states that it brings a repository up to date and may be called repeatedly.
- Generated plugins receive no setup flow and no setup_state.py; each plugin defines its own skills.
Evidence pending: the behavior of `/plugin-manager:<skill>` with several skills on Codex and Claude Code is unverified and needs a behavior test.
Source: skills/setup/SKILL.md
Source: skills/docs/SKILL.md
Source: skills/modify/SKILL.md
Source: skills/verify/SKILL.md
Source: skills/_shared/flows/gate.md
Source: skills/setup/scripts/setup_state.py
Test: tests/contracts/test_skill_set.py
Test: tests/contracts/test_plugin_manager_entry.py
Test: tests/integration/project_setup/test_gate.py
Test: tests/integration/plugin_create/test_no_entry_delivery.py

## R24: Skill modify

Status: confirmed
Acceptance: `/plugin-manager:modify` (a `--dry-run` shows the consequences and writes nothing) changes what a plugin or marketplace repository states about itself. The kind comes from the configuration evidence (R15), never from the call. Like `docs` it first passes the gate of R23 and stops with the reason and a pointer to `/plugin-manager:setup` when the workpackage is not ready, writing nothing then. The dialogue asks what to change (name, display name, description), shows the consequences before any write and writes only after the person's explicit yes; the helper takes explicit parameters (`--name`, `--display-name`, `--description`), validates them (technical name in lowercase kebab-case, display name and description not empty) and changes nothing when the values already match.
- Plugin: `name`, display name (`extensions.com.openai.interface.displayName`) and `description` of plugin.json; the derived host manifests are regenerated and, on a rename, `artifact` in config.json follows. The catalog entry of the plugin in its marketplace is updated in the same rollback-capable transaction when the checkout named by the ignored local.json is available (R21); otherwise the answer reports `catalog_entry_remains: true` with the values to change there. The repository name and URL stay. A name already registered in the marketplace for another repository is refused before any write.
- Marketplace: `name` and display name of marketplace.json with the derived host catalogs. The answer lists the plugin checkouts known from its ignored .local/marketplace.json (name, path) as affected plugins; modify never writes into them. A plugin repository takes the new marketplace name through `associate`, which treats the same checkout under a new name as an identity update of the same marketplace (config.json identity only, no catalog change; R21).
- The answer has `action: "modify"`, the kind, `changed`, `from`, `to`, `published: false`, `catalog_entry_remains` and `affected_plugins`, plus the follow-ups for the person: call forms (`/<name>:<skill>`, `<name>@<marketplace>`) and documentation are refreshed through `/plugin-manager:docs`; the changed files are committed files left unversioned; the person commits and pushes them. modify never commits, pushes, installs or publishes.
- Not part: keywords, category, icon, default prompts, owner, the repository URL, rewriting documentation or tests, and the marketplace association (stays in `setup`). With `modify` the Manager has five public skills (R23).
Source: skills/modify/SKILL.md
Source: skills/modify/scripts/modify.py
Source: skills/_shared/scripts/workflows.py
Test: tests/integration/modify/test_modify.py
Test: tests/contracts/test_skill_set.py

## R25: Messages to the person are plain

Status: confirmed
Acceptance: Every error message the Manager skills show has the same mandatory layout: two short paragraphs of running text without labels or list letters. The first says what could not be completed and why ("The <action> could not be completed, because <cause in plain words, the folder or file named by path>.") and, in one short sentence, what was already changed or that nothing was. The second, after one blank line, asks for the fix ("Please ..."; German: singular imperative), with at most two ways in one sentence ("either ... or ..."), exact commands and where to run them (for example in an IDE such as VS Code or in a terminal), and ends with the call to repeat. Every call form a person reads from a script is given for both hosts, `/<plugin>:<skill>` for Claude and `$<plugin>:<skill>` for Codex. Shell commands of a fix are the one exception to running text: after the request and a colon they stand in a `bash` code block (one command per line), then the message continues; no other block or list is allowed. The message is written as the reply itself, never only in a status or summary field of the host. Labels and sentences are translated into the person's language (German: "..., weil ...", "Bitte ..."). No exit codes, JSON field names, script, helper or generator names, no words such as schema, evidence, hash, lock, transaction or migration, no raw error text; details only when the person asks. Known causes (no Git repository, no GitHub address, a folder inside another repository, an address that is not a plain GitHub address, Git not installed, a folder that is no marketplace, other content in the folder, existing files that differ, an unsupported file format) use the wording of one catalogue. A cause that is not in the catalogue is not guessed: the cause is stated as not known and what was or was not changed, the solutions are to call the same skill again and to run `/plugin-manager:verify`, and, when the host offers a structured question tool, one question offers to show the technical details (shown once, as quoted technical text, on yes); no repair command is run and nothing is retried silently. The layout and the wording come from the module of R26; `skills/_shared/references/messages.md` holds the rules for the model, every skill and failure flow points to it, and the gate stop (R23) uses the same layout. The helper errors a person can reach through a skill (a folder that is no Git repository, a plugin folder without a GitHub address, a folder inside another repository, an address that is not a plain GitHub address) name the command to run and carry no tool output.
Source: skills/_shared/references/messages.md
Source: skills/_shared/scripts/workflows.py
Source: skills/setup/scripts/state/reporting.py
Test: tests/contracts/test_skill_set.py
Test: tests/integration/plugin_create/test_git_messages.py
Test: tests/integration/project_setup/test_gate.py
Test: tests/unit/behavior/test_skill_cases.py


## R26: Failures become their message in Python

Status: confirmed
Acceptance: A failure is turned into the message the person sees by one module (`messages.py`), not by the model. Scripts raise failures with a catalogue code and the facts of the wording (path, address); the helper answer or the command line prints the finished message, in the language of the person (the language passed with `--message-language`, else the saved operator language, else English), in the layout of R25, in German and English from one catalogue; the model writes it unchanged and never composes, translates, shortens or extends it. The catalogue holds the known causes (no Git, a plugin folder without Git or GitHub address with both steps in one message, no GitHub address, a folder inside another repository, an address that is not plain or differs, other content, differing files, an unsupported format, not configured, invalid input of `modify`) and the closed gate. A failure without a catalogue code, an error of the host or a crash gets the same layout with "the cause is not known" through `setup_state.py explain`; the raw text stays technical detail, shown only on request. A new cause is a new catalogue entry with a code, never a sentence in a flow. Tests check that every catalogue entry has the layout in both languages without technical words, that every code the scripts raise is in the catalogue, that no other place builds the layout, and that the commands print the finished message. The model cases check whether the model passes the finished message on as it is; a single run shows that the text steers a model, never a frequency.
Source: skills/setup/scripts/state/messages.py
Source: skills/setup/scripts/state/cli.py
Source: skills/_shared/scripts/workflows.py
Source: skills/modify/scripts/modify.py
Source: skills/_shared/references/messages.md
Source: skills/_shared/flows/gate.md
Test: tests/unit/messages/test_messages.py
Test: tests/integration/plugin_create/test_prerequisites.py
Test: tests/integration/project_setup/test_gate.py
Test: tests/unit/behavior/test_skill_cases.py

## R27: One set of standards for every plugin

Status: confirmed
Acceptance: Every plugin repository carries the same four standards under `docs/standards/` (`coding.md`, `messages.md`, `testing.md`, `skills.md`), delivered and kept current by the Manager as managed files (sync, per-file decision on a deviation as for every managed file), and read by the agent before implementing: the managed `AGENTS.md` (R28) tells to read them and imports them for Claude Code. The standards are identical in every plugin and have no plugin-specific exceptions; a deviation is a finding, never an accepted state. `SCOPE.md` of a plugin holds only the goal and requirements of that plugin and never copies a standard; when it contradicts a standard, the standard wins. `verify` reports read-only, as a structural error: a missing or changed standard, and standard text copied into `SCOPE.md` or `CUSTOM.AGENTS.md`. `verify --review` additionally compares SCOPE and source with the standards and reports contradictions as findings with the standard, path and line; it never changes a standard or SCOPE. The standards cover coding (layout, context instead of globals, current formats only, coded failures), messages (layout, address, one catalogue built in code, R25/R26), tests (structure, rules, model tests, reporting) and skills (one skill per action, boundaries as structure, shared gate). Marketplace repositories receive none of these four standards; their managed scope is R41. The Manager is a plugin and follows the same standards (its own copies equal the managed files). A check of source against the standards that cannot be decided by reading (for example whether a message is built in a second place) remains the task of the review.
Source: skills/_shared/templates/plugin/sync/docs/standards/coding.md
Source: skills/_shared/templates/plugin/sync/docs/standards/messages.md
Source: skills/_shared/templates/plugin/sync/docs/standards/testing.md
Source: skills/_shared/templates/plugin/sync/docs/standards/skills.md
Source: skills/_shared/templates/plugin/sync/AGENTS.md
Source: skills/_shared/manifests/plugin.sync.json
Source: skills/_shared/scripts/verify/structure.py
Source: skills/_shared/scripts/plugin_audit.py
Source: skills/_shared/references/scope-review.md
Test: tests/contracts/verify/test_standards.py
Test: tests/integration/project_setup/test_manifest.py
Test: tests/integration/project_setup/test_setup.py

## R28: Common agent instructions are managed, plugin-specific ones are the plugin's

Status: confirmed
Acceptance: Every plugin repository has two instruction files with separate owners. `AGENTS.md` carries the rules common to all plugins (scope first, current formats only, operator language, read the standards, read `CUSTOM.AGENTS.md`); the Manager delivers it as a managed file and keeps it current (sync, per-file decision on a deviation as for every managed file), and it is identical in every plugin. `CUSTOM.AGENTS.md` holds only what is specific to the plugin; the generator seeds it once, the Manager never manages, overwrites or deletes it, and it never repeats or weakens `AGENTS.md` or a standard. For Claude Code, `AGENTS.md` imports `CUSTOM.AGENTS.md` and the four standards, and `CLAUDE.md` stays limited to importing `AGENTS.md`; other hosts read the named files as text. `verify` reports, read-only, a missing or changed `AGENTS.md` and standard text copied into `CUSTOM.AGENTS.md`. A missing `CUSTOM.AGENTS.md` is not an error. Whether `CUSTOM.AGENTS.md` weakens a rule is a task of `verify --review`. The same two files for marketplace repositories are R41. An existing plugin whose `AGENTS.md` differs gets the per-file decision of `setup`; the Manager converts nothing silently.
Source: skills/_shared/templates/plugin/sync/AGENTS.md
Source: skills/_shared/templates/plugin/seed/CUSTOM.AGENTS.md
Source: skills/_shared/templates/plugin/sync/CLAUDE.md
Source: skills/_shared/manifests/plugin.sync.json
Source: skills/_shared/scripts/verify/structure.py
Source: skills/_shared/scripts/plugin_audit.py
Test: tests/contracts/verify/test_standards.py
Test: tests/integration/project_setup/test_manifest.py
Test: tests/integration/project_setup/test_setup.py
Test: tests/integration/project_setup/test_sync.py

## R30: Shared failure messages for plugins

Status: confirmed
Acceptance: Every plugin receives, as managed files, the module `skills/_shared/scripts/messages_base.py` and a language helper whose failures carry codes. `messages_base.py` is the only place that builds the layout of a failure message (R25/R26) and holds the layout in German and English, the failure class with a code and facts, the language choice (anything but German or English falls back to English), the name of the running plugin read from its `plugin.json` (never a constant) the command frame `run` that every skill script uses (it parses the call, turns a bad call into `ARGS_INVALID`, prints a failure as its finished message and reports anything else as not known, never raw text or a traceback) and a base catalogue with the failures every plugin has: the failures of the language helper (invalid tag, missing project folder, a link in the path, a path that is no folder, an unsupported saved setting), invalid call arguments and the "not known" failure. A plugin extends the base catalogue with its own entries in its own module and never builds the layout again. `operator_language.py` raises failures with the codes of that catalogue and its command line prints the finished message (options `--skill` and `--message-language`), never raw error text or a traceback; its other behavior is unchanged. The Manager ships byte-identical copies of both files. The standards (`coding.md`, `messages.md`) state these rules; whether a plugin follows them beyond what `verify` can read is a task of `verify --review`.
Source: skills/_shared/templates/plugin/sync/skills/_shared/scripts/messages_base.py
Source: skills/_shared/templates/plugin/sync/skills/_shared/scripts/operator_language.py
Source: skills/_shared/templates/plugin/sync/docs/standards/coding.md
Source: skills/_shared/templates/plugin/sync/docs/standards/messages.md
Source: skills/_shared/templates/plugin/sync/skills/_shared/references/operator-language.md
Test: tests/unit/messages/test_messages_base.py
Test: tests/integration/operator_language/test_cli.py
Test: tests/unit/operator_language/test_validation.py

## R31: A managed runner for model cases in every plugin

Status: confirmed
Acceptance: Every plugin receives the runner `tests/behavior/run_cases.py` as a managed file, identical everywhere. It reads the cases of the plugin from `tests/fixtures/skills/cases.json` (owned by the plugin; without the file it reports `NOT RUN` and exits 0) and, only when started explicitly with `--cli claude|codex` (`make test-behavior CLI=...` of a new plugin), sends each case to the model without tools: the real skill texts, the output of the commands the skill starts with and the conversation so far. The answer (reply, commands, next step, offered options, whether files are written) is graded deterministically against the expectation of the case: language, required and forbidden text, order, forbidden and required commands, next step, options, writes, number of questions. `--list` lists the cases without a model. The runner never installs a tool, starts no host and states that one run on one model shows that the text steers a model, not how often. `verify` does not run it. Model cases are optional: the standards (`testing.md`) require none; whether a model carries out a task correctly is not a concern of the Manager.
Source: skills/_shared/templates/plugin/sync/tests/behavior/run_cases.py
Source: skills/_shared/templates/plugin/sync/Makefile
Source: skills/_shared/templates/plugin/sync/docs/standards/testing.md
Test: tests/unit/behavior/test_run_cases.py
Test: tests/integration/project_setup/test_manifest.py

## R32: verify checks the mechanical rules of the standards

Status: confirmed
Acceptance: Besides the managed files (R27, R28), `verify` reads a plugin repository and reports as a structural error, without running anything, what the standards fix mechanically: with several skills, a `commands/<skill>.md` for every skill (a plugin with exactly one skill needs none); the failure layout only in `messages_base.py` (or a file named `messages.py` of the Manager's own catalogue), never in another script; every failure code used in a script (`Failure`, `failure`, `OperatorLanguageError`) has an entry in a catalogue of the repository; and the test folders: only `unit`, `integration`, `contracts`, `behavior`, `native`, `fixtures` and `support` below `tests/`, with an `__init__.py` in every folder on the way to a test file. All problems are listed in one answer with the path. What the standards also demand but cannot be read mechanically (for example whether a message wording is good, or an acceptance test per requirement, which `verify --review` compares) stays with the review. The checks apply to plugin repositories only.
Source: skills/_shared/scripts/verify/structure.py
Source: skills/_shared/templates/plugin/sync/docs/standards/skills.md
Source: skills/_shared/templates/plugin/sync/docs/standards/testing.md
Test: tests/contracts/verify/test_standards.py

## R33: The standards are checked in CI and, if the person activates it, before a commit

Status: confirmed
Acceptance: The managed workflow `dm-verify.yml` runs the check scripts (R51) in addition to the tests, so a missing, changed or violated standard fails the run. The copy of the standards check inside a plugin compares the standards and `AGENTS.md` with the source hashes recorded in the plugin's committed skeleton lock; without a readable lock it checks presence and the other rules only. Every plugin receives the managed, executable hook `githooks/pre-commit`, which runs the same checks and stays silent when they pass. Nothing activates the hook: only the person does, once per clone, with `make install-hooks`.
Source: skills/_shared/templates/plugin/sync/.github/workflows/dm-verify.yml
Source: skills/_shared/templates/plugin/sync/Makefile
Source: skills/_shared/templates/plugin/sync/githooks/pre-commit
Source: skills/_shared/scripts/verify/structure.py
Source: skills/_shared/scripts/plugin_audit.py
Test: tests/contracts/verify/test_standards.py
Test: tests/integration/project_setup/test_manifest.py

## R34: Documentation structure by kind

Status: confirmed
Acceptance: The user documentation of a repository is written from its sources (`SCOPE.md`, every `SKILL.md`, flows and source code) in each selected documentation language and has this structure. R4 and R29 apply to this structure.

| Page | Plugin | Marketplace | Required headings (en / de) |
| --- | --- | --- | --- |
| `README.md`, `README.<lang>.md` | yes | yes | Plugin: an introduction without a heading, then Quick start / Schnellstart and Features (an icon may precede a heading) with one `### :<skill>` entry per skill (a short explanation of at most 200 characters and a link to its subpage). The start page is written by hand, never generated, and carries no footer; only this structure is checked. Marketplace: a free introduction, then Plugins with one `### <plugin>` entry (display name) per listed plugin and a link to its README; no quick start, no page per plugin, written by hand |
| `docs/<lang>/installation.md` | yes | yes | Claude (Claude Desktop App, Claude CLI); Codex (ChatGPT Desktop App, Codex CLI, ChatGPT Workspace); Update / Aktualisieren; Remove / Entfernen — one level-three section per surface, so that other pages can link to it |
| `docs/<lang>/skills.md` | yes | no | `# 🛠 Skills`, `## 📖 Skills`, one `### <skill>` per skill (generated) |
| `docs/<lang>/skills/<skill>.md` | yes | no | Description; Workflow; Example; Reads and writes / Beschreibung; Ablauf; Beispiel; Liest und schreibt (level two, free level-three headings below) |
| `docs/<lang>/concepts.md` | yes | yes | Marketplace; Plugin; Skill |
| `docs/<lang>/development.md` | yes | yes | Requirements / Voraussetzungen; Set up / Einrichten; Test locally / Lokal testen; Publish / Veröffentlichen (R42) |

The README starts with the language switch and the links to the pages and then describes the product invitingly in prose; it uses only the Purpose and Non-goals of `SCOPE.md`, confirmed requirements and the skill descriptions and never presents a draft as a feature. `skills.md` is generated by `:docs` anew on every run (fixed text, then per skill its heading, call, the text of the section "Description" of its subpage and a link; footer saying so); `:docs` creates a missing subpage `docs/<lang>/skills/<skill>.md`, which then belongs to the person and may describe the skill in detail; `plugins.md` is a table of the plugins of `marketplace.json` (name, description, link to its documentation). The pages `screens`, `faq`, `usage`, `storage` and `docs/<lang>/README.md` are not part of the structure. Existing user text is never converted, overwritten or deleted by the Manager.
Source: skills/_shared/scripts/verify/docs.py
Source: skills/_shared/scripts/documentation.py
Test: tests/integration/update/test_documentation.py

## R35: The installation page comes from the repository's data

Status: confirmed
Acceptance: `installation.md` is produced from facts, not written freely; for a plugin `:docs` generates the whole page anew on every run (fixed text, the facts below, a footer saying so; headings of level 1 to 3 required one to one): the name and repository of a plugin (`plugin.json`), the name of its marketplace (configuration evidence) and the marketplace address. The address is read once from the `origin` of the marketplace checkout named in the local association and recorded as `marketplace_url` in `docs/documentation.json`; without a checkout or `origin` the page states it as open and the report names it; it is never invented. A marketplace uses its own `origin`. Steps that a host supports only through its interface (Claude Desktop) are described as that path, not as commands. Host steps are taken from verified evidence; an unverified step is not written. Evidence of 25 November 2026: the Claude Code commands from the official documentation (discover-plugins, plugin-marketplaces), the Codex commands from the help of the installed Codex CLI 0.165.0, the desktop interface paths of both apps from the owner's reports and screenshots (18 November 2026), not documented by the hosts.
Source: skills/_shared/scripts/documentation.py
Test: tests/integration/update/test_documentation.py

## R36: The concepts page is generated

Status: confirmed
Acceptance: `docs/<lang>/concepts.md` (German and English) explains marketplace, plugin and skill in plain language and is the same for every repository of both kinds; only the link to the skills or plugin list in the navigation differs. `:docs` generates it anew on every run; the footer says that the page is created automatically by `:docs`. `verify` requires its headings of level 1 to 3 one to one and in order. It is not a synced file.
Source: skills/_shared/scripts/documentation.py
Source: skills/_shared/templates/documentation/plugin/docs/en/concepts.md
Source: skills/_shared/templates/documentation/marketplace/docs/en/concepts.md
Test: tests/contracts/shared_files/test_shared_files_page.py

## R37: verify checks the documentation structure

Status: confirmed
Acceptance: The documentation check reads, without executing anything, that the pages of R34 for the kind exist in every selected language with their required headings, that `skills.md` has exactly one entry per skill linking its subpage and every subpage has the required headings (marketplace: every listed plugin a row in `plugins.md`), that no unresolved placeholder remains and that local links resolve. Pages of the former structure are reported. Whether the prose is good is not checked. It is its own script (R51) and so part of `make verify`, the CI and the verify skill. Everything it finds is a warning: it never fails `make verify`, the CI or the pre-commit hook (in GitHub Actions it is shown as a warning annotation); whether the documentation is written is the developer's decision. An empty section of a hand-written page is named with what belongs there. Without `docs/documentation.json` no language is selected yet; nothing is checked and the result says `documentation: not_created`.
Source: skills/_shared/scripts/verify/docs.py
Test: tests/contracts/verify/test_ci_checks.py
Test: tests/contracts/verify/test_standards.py

## R38: Writing styles of a plugin

Status: confirmed
Acceptance: Two optional files say how a repository writes; both belong to the repository and the Manager never changes or overwrites them. `docs/style.md` says how the documentation is written: a new plugin or marketplace receives it as a seed; `setup` does not ask for it, no skill is stopped without it and no check requires it. `skills/_shared/references/style.md` says how the plugin talks with its user, is optional, is read by every skill after the language rules when present, and never overrides the standards, the operator language or the message layout.
Source: skills/setup/scripts/state/reporting.py
Source: skills/_shared/templates/plugin/seed/docs/style.md
Source: skills/_shared/templates/plugin/sync/docs/standards/skills.md
Test: tests/contracts/verify/test_standards.py

## R39: The Manager is a separate plugin in its own repository

Status: confirmed
Acceptance: The Plugin Manager lives in its own repository (`ai.plugin.plugin-manager`) and is a plugin like any other: `setup`, `docs` and the other skills may target it, only the installation the running Manager was loaded from is never a target. No marketplace embeds a plugin: a marketplace entry with a local `path` is rejected by `verify` and by the catalog script with a concrete reason, never converted.
Source: skills/setup/scripts/state/detection.py
Source: skills/_shared/scripts/verify/structure.py
Source: skills/_shared/templates/marketplace/sync/scripts/marketplace.py
Test: tests/integration/project_setup/test_setup.py


## R40: The tests of the marketplace scripts are delivered with them

Status: confirmed
Acceptance: A marketplace receives, as synced files under `tests/contracts/`, the tests of the scripts the Manager keeps in sync there: catalog generation, local development install, plugin packaging and the test runner. They use fictional data only and never read the marketplace's own `marketplace.json`, so adding or removing a catalog entry cannot break them. `setup` delivers and updates them like the other synced files, and the Manager runs the same files against its own templates, so there is one source. The person's own tests stay untouched.
Source: skills/_shared/templates/marketplace/sync/tests/contracts/test_marketplace_catalogs.py
Source: skills/_shared/templates/marketplace/sync/tests/contracts/test_local_plugins.py
Source: skills/_shared/templates/marketplace/sync/tests/contracts/test_plugin_payload.py
Source: skills/_shared/templates/marketplace/sync/tests/contracts/test_run_tests.py
Source: skills/_shared/manifests/marketplace.sync.json
Test: tests/integration/marketplace_create/test_managed_tests.py
Test: tests/integration/project_setup/test_manifest.py

## R41: Every marketplace has the same managed scope

Status: confirmed
Acceptance: Every marketplace has the same task, so its `SCOPE.md` is not written per repository: the Manager delivers it as a synced file (purpose, non-goals and the requirements for catalog, host catalogs, local development and current formats, each pointing to the synced script and test that cover it), together with `AGENTS.md`, which tells to read it and imports it and `CUSTOM.AGENTS.md` for Claude Code. Both follow the keep/adopt/delete rules of R12. What distinguishes a marketplace (name, owner, listed plugins) is stated in `marketplace.json`; `CUSTOM.AGENTS.md` is created once and holds only what is specific to the marketplace. `verify` reports, read-only, a missing or changed `SCOPE.md` or `AGENTS.md` and scope text copied into `CUSTOM.AGENTS.md`; it does not apply this to the catalog a plugin repository reads from its marketplace. An existing `SCOPE.md` or `AGENTS.md` that differs gets the per-file decision of `setup`; nothing is converted silently.
Source: skills/_shared/templates/marketplace/sync/SCOPE.md
Source: skills/_shared/templates/marketplace/sync/AGENTS.md
Source: skills/_shared/templates/marketplace/seed/CUSTOM.AGENTS.md
Source: skills/_shared/scripts/verify/structure.py
Test: tests/contracts/verify/test_marketplace_standard.py
Test: tests/integration/project_setup/test_manifest.py

## R42: The development page is generated

Status: confirmed
Acceptance: `docs/<lang>/development.md` (German and English, one text per kind, identical in every repository of the kind) tells a developer what is needed and how a marketplace and a plugin are set up, tested locally and published. `:docs` generates it anew on every run; the footer says that the page is created automatically by `:docs`. It is linked in the navigation of every documentation page, and `verify` requires its headings of level 1 to 3 one to one and in order. It is not a synced file.
Source: skills/_shared/scripts/documentation.py
Source: skills/_shared/templates/documentation/plugin/docs/en/development.md
Source: skills/_shared/templates/documentation/marketplace/docs/en/development.md
Test: tests/contracts/shared_files/test_shared_files_page.py

## R43: Managed Makefiles; local installation only in the marketplace

Status: confirmed
Acceptance: The `Makefile` of a plugin and of a marketplace is a synced file per kind; own targets and variables belong into `CUSTOM.mk`, which the Makefile includes when present and which is created once. Both have `sync`, `check`, `test` and `verify`; a plugin adds `test-behavior` and `install-hooks`, a marketplace adds `install-local`. The local installation runs only in the marketplace: a plugin repository has no `install-local`, and its `scripts/plugin.py` only generates and checks its host metadata. The packaging of a plugin checkout lies in the marketplace's `scripts/plugin_payload.py` alone. The association of a plugin with its marketplace (R21) stays. An existing differing `Makefile` gets the per-file decision of `setup`.
Source: skills/_shared/templates/plugin/sync/Makefile
Source: skills/_shared/templates/marketplace/sync/Makefile
Source: skills/_shared/templates/plugin/sync/scripts/plugin.py
Source: skills/_shared/templates/marketplace/sync/scripts/plugin_payload.py
Source: skills/_shared/scripts/plugin_audit.py
Test: tests/integration/project_setup/test_manifest.py
Test: tests/integration/distribution/test_plugin.py

## R44: The CI workflow and the generic documents are managed

Status: confirmed
Acceptance: What is the same in every repository of a kind is synced, not created once: `.github/workflows/dm-verify.yml` (tests, host manifest or catalog check and `verify`, calling the Python scripts directly so that it does not depend on the Makefile), `docs/prerequisites.md` and `tests/README.md`. Own CI steps go into another file under `.github/workflows/`. What belongs to the repository stays seeded. A former `validate.yml` was never managed: the Manager neither changes nor removes it. The local development package holds every template, the workflow under `.github/` included, and an incomplete or inconsistent template set is reported with its own message.
Source: skills/_shared/templates/plugin/sync/.github/workflows/dm-verify.yml
Source: skills/_shared/templates/marketplace/sync/.github/workflows/dm-verify.yml
Source: skills/_shared/manifests/plugin.sync.json
Source: skills/_shared/templates/marketplace/sync/scripts/plugin_payload.py
Test: tests/integration/project_setup/test_manifest.py
Test: tests/contracts/verify/test_standards.py
Test: tests/contracts/payload/test_payload_complete.py

## R45: A file kept on purpose can be taken back

Status: confirmed
Acceptance: `status` lists the files with an accepted deviation under `kept` with the current source and local hash. When the person asks for one back, `setup` names the file, asks once and only after "Adopt template" replaces it by the template for exactly that pair (`sync --decision adopt`), recording both hashes; no content or diff is shown (R18). A file without an open question and without an accepted deviation, or a changed pair, is refused with its own message, never as an unknown cause.
Source: skills/setup/scripts/state/syncing.py
Source: skills/setup/scripts/state/inspection.py
Source: skills/setup/flows/sync.md
Source: skills/setup/scripts/state/messages.py
Test: tests/integration/project_setup/test_take_back.py

## R46: The documentation explains the shared files

Status: confirmed
Acceptance: Every plugin has the page `docs/<lang>/files.md` "Shared files" (German and English), linked in the navigation of every documentation page. `:docs` generates it, anew on every run: the explanation of synced and seed files, the introduction of each tree and the footer are the same in every repository; the trees of the synced and seed files of a plugin and of a marketplace come from what the Manager delivers (hash files and seed folders). The footer says that the page is created automatically by `:docs`. `verify` requires its headings of level 1 to 3 one to one and in order. It is not a synced file.
Source: skills/_shared/scripts/documentation.py
Source: skills/_shared/scripts/verify/docs.py
Source: skills/_shared/templates/documentation/plugin/docs/de/files.md
Test: tests/contracts/shared_files/test_shared_files_page.py

## R47: verify checks the hash files of sync templates

Status: confirmed
Acceptance: A plugin that keeps files in sync for others uses the structure `skills/<skill>/templates/<kind>/sync/` with the hash file `skills/<skill>/manifests/<kind>.sync.json`. Every plugin receives the tools as synced scripts: `scripts/build_hashes.py` (`make build-skeleton-hashes`) builds the hash files and `scripts/verify/hashes.py` fails when a file is missing in the hash file or in the folder, its hash or executable bit differs, a path is listed as file and as removed, the format is not canonical or the hash file is missing. A plugin without such a structure is not affected. Open: a seed and sync process that other plugins can offer themselves (creating, updating and asking).
Source: skills/_shared/scripts/verify/hashes.py
Source: scripts/build_hashes.py
Test: tests/contracts/verify/test_ci_checks.py
Test: tests/unit/skeleton_hashes/test_skeleton_hashes.py

## R48: The developer pages describe commands and CI

Status: confirmed
Acceptance: The development page of each kind (German and English) has a section on the `make` commands with their purpose and variables and a section on `dm-verify.yml` with every step and when it fails, and says where own commands and own CI steps belong. A test compares both sections with the managed Makefile and workflow of the kind, so a new or removed target, variable or step fails until the pages follow. Own commands of a repository are not listed there.
Source: skills/_shared/templates/documentation/plugin/docs/de/development.md
Source: skills/_shared/templates/documentation/marketplace/docs/de/development.md
Test: tests/contracts/shared_files/test_development_page.py

## R50: setup asks before the skeleton flow writes and lists what it wrote

Status: confirmed
Acceptance: When the skeleton flow is about to write, `status` returns a finished question that names every file with what happens to it (create, change, delete) and asks "May I write?"; the flow shows it unchanged, with no text before it, and runs `setup` only after an explicit yes. The whole question, every file line included, is the text of the question itself, because a dialog may be all the person sees. This includes untouched copies that are updated without a per-file decision. On no, nothing is written. After writing, the helper returns the finished list of updated, created and removed files (also after adopting or deleting by a sync decision); the final answer shows these lists unchanged, above the ready line, instead of a sentence. The helper's own evidence file is bookkeeping: it is never asked about or listed. When it is all a run would write, `status` returns no question and the flow runs `setup` directly. Questions per deviating file stay as they are. Helper commands are run as plain single commands. Both texts are built in the helper, German and English. The same holds for the generators `create` and `associate`: a call with `--plan` writes nothing and answers with the question that names every file the call would write, also in the marketplace repository; the flow runs the writing call only after an explicit yes and shows the list of what was written. Files a generator creates get the usual file mode of the machine, and a changed file keeps its own. These questions are the case of R56 in which the order does not reveal which files a script changes.
Source: skills/setup/scripts/state/messages.py
Source: skills/setup/scripts/state/reporting.py
Source: skills/setup/scripts/state/syncing.py
Source: skills/setup/flows/skeleton.md
Source: skills/setup/flows/entry.md
Source: skills/_shared/scripts/workflows.py
Source: skills/setup/flows/configure.md
Source: skills/setup/flows/marketplace.md
Source: skills/setup/flows/associate.md
Test: tests/integration/project_setup/test_write_request.py
Test: tests/integration/plugin_create/test_generator_question.py

## R51: One script per check, called alike by make, CI and pre-commit

Status: confirmed
Acceptance: The checks of a repository are separate scripts in `scripts/verify/`: `structure.py`, `standards.py`, `docs.py` and for a plugin also `conventions.py` and `hashes.py`; `scope.py` collects the review evidence (`REVIEW=1`). Each runs alone, writes nothing and reports its own result. `make verify`, `dm-verify.yml` and (plugin) the pre-commit hook call exactly the same scripts, which a test compares; the verify skill runs the same ones. The former `scripts/verify.py` and `scripts/docs_rules.py` are listed as removed, so setup deletes untouched copies.
Source: skills/_shared/scripts/verify/structure.py
Source: skills/_shared/templates/plugin/sync/Makefile
Source: skills/_shared/templates/plugin/sync/githooks/pre-commit
Test: tests/contracts/verify/test_check_scripts.py

## R52: Each skill loads its own rules, and instructions name only existing scripts

Status: confirmed
Acceptance: `skills/_shared/WORKFLOWS.md` holds only what every action shares. The rules of `modify` and `verify` stand in their `SKILL.md`, those of `docs` in `skills/docs/references/workflow.md`, so a skill does not load the rules of another one. Repository layout and distribution are a reference read only when needed. Every Python script an instruction or reference file names exists, checked by a test. Every `SKILL.md` of the Manager has the title ``# <skill> (`/plugin-manager:<skill>`)`` and the sections Read first, Start, Steps, Boundaries and Messages in this order.
Source: skills/_shared/WORKFLOWS.md
Source: skills/docs/references/workflow.md
Source: skills/modify/SKILL.md
Source: skills/verify/SKILL.md
Test: tests/contracts/test_instruction_references.py
Test: tests/contracts/test_skill_layout.py

## R53: docs creates structure and reports, it writes no texts

Status: confirmed
Acceptance: The docs skill selects the languages, runs the helper, which writes the generated pages anew and creates missing hand-written pages, validates and reports what is still to be written. It never writes or changes text of a person, never asks for a missing fact (the page states it as open, the report names it) and treats every finding as a warning. One command does it and returns the finished answer: the pages rewritten and created, the sections still to be written, missing facts, every other warning, then one status line; no warning is dropped except the repetition in `skills.md` of what is listed as open on a skill page; the whole answer, warning texts included, is in the operator language (the check itself reports in English, as in CI) (`<Kind> <name> docs: complete` or the number of warnings), in the operator language; with nothing to report only that line, without a summary card.
Source: skills/docs/SKILL.md
Source: skills/docs/references/workflow.md
Source: skills/_shared/scripts/documentation.py
Test: tests/contracts/verify/test_ci_checks.py
Test: tests/integration/update/test_docs_result.py

## R54: The documentation of a marketplace

Status: confirmed
Acceptance: A marketplace has the start page, Installation, Concepts and Development, linked in this navigation on every page; it has no page per plugin, no plugin list page, no page about skills and none about shared files. The start page is written by hand: a free introduction and a section Plugins with one entry per listed plugin linking the README of its repository. A newly created marketplace receives it once in this structure (German and English) together with a neutral icon, and with it the generated pages Installation, Concepts and Development in German and English, so the start page has no dead link; the documentation languages are recorded, existing settings and pages are kept. Installation is generated and only adds, updates and removes the marketplace, saying that adding it installs no plugin; Concepts is the same page as in a plugin; Development is generated and explains how plugins are connected and how the local installation with make works. Findings are warnings; former pages are reported, never deleted.
Source: skills/_shared/templates/documentation/marketplace/docs/de/installation.md
Source: skills/_shared/templates/documentation/marketplace/docs/de/development.md
Source: skills/_shared/scripts/verify/docs.py
Source: skills/_shared/scripts/workflows.py
Test: tests/integration/update/test_marketplace_docs.py
Test: tests/integration/marketplace_create/test_workflows.py


## R55: Fixed questions and terms

Status: confirmed
Acceptance: The questions the skills ask stand once, in German and English, in one catalogue (`state/questions.py`); `setup_state.py questions` returns them write-free in the saved operator language, and the flows show question and choices unchanged, replacing only the placeholders. The first language question is bilingual. `modify` asks before writing with the same file list as the generators and lists what it wrote. The skill pages show the same wording, which a test compares. For people the terms are: publisher (Herausgeber), technical name, display name, marketplace folder, shared file, template, operator language, documentation languages.
Source: skills/setup/scripts/state/questions.py
Source: skills/setup/scripts/state/cli.py
Source: skills/modify/scripts/modify.py
Source: skills/modify/SKILL.md
Source: skills/setup/flows/configure.md
Test: tests/contracts/test_questions.py
Test: tests/integration/modify/test_modify.py
\n

## R56: When a skill asks before it writes

Status: confirmed
Acceptance: The skill standard delivered to every plugin states it: an order that names the change is the approval for that change, and the skill reports afterwards; what is missing is asked for as a fact. A yes is required first, with files or effect named, in three cases only: a script changes files that the order does not reveal, content of the person would be lost, or something happens outside the working copy, such as commit, push, publication, installation or cost. The Manager's own questions before writing (R50, modify) fall under the first case.
Source: skills/_shared/templates/plugin/sync/docs/standards/skills.md
Test: tests/contracts/verify/test_standards.py
