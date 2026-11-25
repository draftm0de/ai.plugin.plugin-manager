# Gemeinsame Dateien

[Installation](installation.md) · [Skills](skills.md) · [Begriffe](concepts.md) · [Entwicklung](development.md)

Plugin Manager legt in jedem Plugin und Marketplace Dateien an. Es gibt zwei Arten, und davon hängt ab, was du ändern kannst.

| | Sync-Datei | Seed-Datei |
| --- | --- | --- |
| Gehört | Plugin Manager, in allen Repositorys gleich | dem Repository |
| Angelegt | von `setup`, auch wenn sie später fehlt | einmal beim Erstellen des Repositorys |
| Neue Vorlage | wird übernommen, bei eigener Änderung nach Rückfrage | wirkt sich nicht aus |
| Eigene Änderung | führt zu einer Rückfrage | bleibt, ohne Rückfrage |
| Gelöscht | `setup` legt sie wieder an | bleibt gelöscht |

Ausnahme: Fehlt `docs/style.md`, fragt `setup` nach der Vorlage oder nach deinem eigenen Stil.

## Eine Sync-Datei ändern

Ändere sie nicht, wenn es eine eigene Datei dafür gibt:

| Statt | Nimm |
| --- | --- |
| `AGENTS.md` | `CUSTOM.AGENTS.md` |
| `Makefile` | `CUSTOM.mk` |
| `.github/workflows/dm-verify.yml` | eine weitere Datei unter `.github/workflows/` |

Änderst du sie trotzdem, fragt das nächste `setup` je Datei:

- **Lokal behalten:** Deine Fassung bleibt. Gefragt wird erst wieder, wenn sich deine Datei oder die Vorlage ändert.
- **Vorlage übernehmen:** Deine Fassung wird ersetzt. Sichere vorher, was du behalten willst.

Dateiinhalte oder ein Diff zeigt `setup` nicht; vergleiche vorher mit Git.

**Behalten hat Grenzen:** `AGENTS.md`, bei Plugins die Standards unter `docs/standards/` und bei Marketplaces `SCOPE.md` sind verbindlich. Weichen sie ab, schlagen `verify` und die CI fehl, auch wenn du „behalten“ gewählt hast.

## Zurück in den Sync

Bitte `setup` darum, zum Beispiel „Nimm das Makefile wieder in den Sync“. Nach deinem Ja ersetzt die Vorlage deine Fassung. Oder lösche die Datei und rufe `setup` auf.

## Wenn eine Vorlage entfällt

Eine unveränderte Kopie entfernt `setup` selbst. Hast du sie geändert, entscheidest du: behalten oder löschen.

## Dateien eines Plugins

**Sync:** `AGENTS.md`, `CLAUDE.md`, `Makefile`, `.github/workflows/dm-verify.yml`, `docs/<lang>/concepts.md`, `docs/<lang>/development.md`, `docs/prerequisites.md`, `docs/standards/coding.md`, `docs/standards/messages.md`, `docs/standards/skills.md`, `docs/standards/testing.md`, `githooks/pre-commit`, `scripts/plugin.py`, `scripts/run_tests.py`, `scripts/verify.py`, `skills/_shared/references/operator-language-helper.md`, `skills/_shared/references/operator-language.md`, `skills/_shared/scripts/messages_base.py`, `skills/_shared/scripts/operator_language.py`, `tests/README.md`, `tests/behavior/run_cases.py`, `tests/contracts/test_operator_language.py`

**Seed:** `.gitignore`, `CUSTOM.AGENTS.md`, `CUSTOM.mk`, `SCOPE.md`, `assets/icon.png`, `docs/architecture.md`, `docs/style.md`, `tests/__init__.py`, `tests/contracts/__init__.py`, `tests/contracts/test_structure.py`

## Dateien eines Marketplace

**Sync:** `AGENTS.md`, `CLAUDE.md`, `Makefile`, `SCOPE.md`, `.github/workflows/dm-verify.yml`, `docs/<lang>/concepts.md`, `docs/<lang>/development.md`, `docs/prerequisites.md`, `scripts/local_plugins.py`, `scripts/marketplace.py`, `scripts/plugin_payload.py`, `scripts/run_tests.py`, `scripts/verify.py`, `tests/README.md`, `tests/contracts/test_local_plugins.py`, `tests/contracts/test_marketplace_catalogs.py`, `tests/contracts/test_plugin_payload.py`, `tests/contracts/test_run_tests.py`

**Seed:** `CUSTOM.AGENTS.md`, `CUSTOM.mk`, `local-marketplace.example.json`, `docs/architecture.md`, `docs/style.md`, `tests/__init__.py`, `tests/contracts/__init__.py`, `tests/contracts/test_structure.py`

`<lang>` steht für jede gewählte Dokumentationssprache. In `.gitignore` werden nur fehlende Regeln ergänzt.
