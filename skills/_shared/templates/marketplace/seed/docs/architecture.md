<!--
How this marketplace is laid out. AGENTS.md tells the assistant to read this file before it changes anything.
-->

# Marketplace architecture

- `marketplace.json`: the only catalog edited by hand.
- `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`: generated with `make sync`, never edited.
- `scripts/`: managed development and check scripts.
- `tests/<layer>/`: deterministic tests with fictional data.
- `docs/`: documentation; `/plugin-manager:docs` generates the installation, concepts and development pages.
- `.local/marketplace.json`: ignored paths of local plugin checkouts, never committed.

A marketplace contains no plugin and no skill: every plugin lives in its own repository.
