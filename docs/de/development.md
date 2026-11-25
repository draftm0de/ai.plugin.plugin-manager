# Entwicklung

[Installation](installation.md) · [Skills](skills.md) · [Begriffe](concepts.md)

Für alle, die an diesem Plugin arbeiten. Zum Benutzen brauchst du diese Seite nicht.

## Voraussetzungen

- Git und Python 3.10 oder neuer. Make ist optional.
- Claude oder Codex mit installiertem Plugin Manager.
- Für die lokale Installation die jeweilige CLI (`claude` oder `codex`).
- Je ein GitHub-Repository für den Marketplace und für jedes Plugin, jeweils lokal geklont.

## Einrichten

1. Einen Marketplace haben: ein eigenes Repository, mit `/plugin-manager:setup` als „Marketplace“ eingerichtet und lokal geklont.
2. Plugin-Repository auf GitHub anlegen und klonen.
3. Darin `/plugin-manager:setup` ausführen, „Plugin“ wählen und den Marketplace nennen. Der Eintrag im Marketplace und die lokale Zuordnung entstehen dabei.
4. Anforderungen in `SCOPE.md` festhalten und die Skills unter `skills/<skill>/` bauen.

## Lokal testen

Im Ordner des Plugins:

```bash
make sync
```

```bash
make check test verify
```

Installiert wird im Ordner des Marketplace:

```bash
make -C ../<marketplace> install-local TARGET=claude
```

Danach eine neue Sitzung öffnen. Auch nicht committete Änderungen sind enthalten. Für Codex `TARGET=codex`.

## Befehle

Alle Befehle laufen im Stamm des Repositorys. `make help` listet sie auch.

| Befehl | Zweck | Variablen |
| --- | --- | --- |
| `make sync` | Host-Manifest aus `plugin.json` erzeugen | |
| `make check` | Prüfen, ob das Host-Manifest dazu passt | |
| `make test` | Deterministische Tests | `TEST_GROUP=<name>`: nur eine Komponente |
| `make verify` | Struktur nur lesend prüfen | `SOURCE=<ordner>`; `REVIEW=1`: zusätzlich Abgleich mit `SCOPE.md` |
| `make test-behavior` | Optionale Modellfälle, kann Credits kosten | `CLI=claude` oder `codex` |
| `make install-hooks` | Prüfung vor jedem Commit für diesen Klon aktivieren | |
| `make help` | Befehle anzeigen | |

Eigene Befehle stehen in `CUSTOM.mk`.

## CI

`.github/workflows/dm-verify.yml` läuft bei jedem Push, jedem Pull Request und auf Knopfdruck. Rot wird der Lauf, wenn ein Schritt fehlschlägt.

| Schritt | Rot, wenn |
| --- | --- |
| `python3 -B scripts/run_tests.py` | ein Test fehlschlägt |
| `python3 -B scripts/plugin.py check` | das Host-Manifest nicht zu `plugin.json` passt |
| `python3 -B scripts/verify.py --source . --kind plugin` | die Struktur ungültig ist, Standards oder `AGENTS.md` abweichen, eine Konvention verletzt ist (Befehlsdateien, Meldungen, Testordner, `docs/style.md`), der Doku Seiten, Überschriften oder Linkziele fehlen oder Hash-Dateien nicht zu Sync-Vorlagen passen |

Eigene Schritte stehen in einer weiteren Datei unter `.github/workflows/`. Lokal prüfst du dasselbe mit `make test check verify`.

## Gemeinsame Dateien

Plugin Manager hält einen Teil der Dateien aktuell (Sync), andere legt er nur einmal an (Seed). `.project/plugins/plugin-manager/skeleton.json` listet die Sync-Dateien. Ändere sie nicht: Eigene Regeln gehören in `CUSTOM.AGENTS.md`, eigene Befehle in `CUSTOM.mk`, eigene CI-Schritte in eine weitere Datei unter `.github/workflows/`. Änderst du eine Sync-Datei doch, fragt `/plugin-manager:setup`, ob du sie behältst oder die Vorlage übernimmst. Behältst du `AGENTS.md`, `SCOPE.md` eines Marketplace oder einen Standard unter `docs/standards/`, schlägt `verify` fehl.

## Veröffentlichen

Committen und auf den Standard-Branch pushen; installiert wird, was dort liegt. Es gibt keine Versionen, Tags oder Releases. Ein neues Plugin zuerst pushen, danach den Marketplace mit seinem Eintrag.
