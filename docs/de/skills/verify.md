# 🛠 :verify

**Deutsch** | [English](../../en/skills/verify.md)

[Start](../../../README.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Begriffe](../concepts.md) · [Entwicklung](../development.md) · [Gemeinsame Dateien](../files.md)

## Beschreibung

`verify` sagt dir, ob dein Repository den Regeln entspricht. Es erkennt selbst, ob es ein Plugin oder ein Marketplace ist, und prüft Aufbau, gemeinsame Standards und Dokumentation. Auf Wunsch vergleicht es auch `SCOPE.md` mit dem Quellcode. Es liest nur: Es ändert nichts und führt keinen Code deines Repositorys aus.

## Ablauf

1. Erkennt selbst, ob Plugin oder Marketplace.
2. Prüft die Struktur, bei Plugins auch die Standards und gemeinsamen Anweisungen, und die Dokumentation.
3. Meldet eine noch offene Einrichtung, ohne sie auszuführen.
4. Auf Wunsch vergleicht es `SCOPE.md` mit dem Quellcode.

### Was im Bericht steht

| Begriff | Was heißt das? |
| --- | --- |
| Struktur gültig | Manifeste, Kataloge, Skills und Ordner passen zu den Regeln. Es sagt nichts darüber, ob dein Skill das Richtige tut. |
| Lokale Zuordnung unvollständig | Auf diesem Rechner fehlt der Pfad zum Marketplace oder zu den Plugins. Nach einem frischen Klon ist das normal; zum lokalen Installieren braucht es ihn. |
| Standards | `AGENTS.md`, die gemeinsamen Standards und beim Marketplace `SCOPE.md` sind unverändert. |
| Warnungen zur Doku | Fehlende Seiten, Überschriften oder Links. Sie lassen nichts scheitern. |
| Einrichtung offen | Eine gemeinsame Datei fehlt oder ist veraltet: `/plugin-manager:setup` ausführen. |
| Bereit für das Source-Review | Alle in `SCOPE.md` genannten Belege sind lesbar. Ob die Anforderungen erfüllt sind, ist damit nicht gesagt. |
| Nicht geprüft | Ob Claude oder Codex das Plugin laden und wie sich der Skill dort verhält. |

## Beispiel

`/plugin-manager:verify` vor dem Pushen.

## Liest und schreibt

Liest das Repository. Schreibt nichts und führt keinen Code des Repositorys aus. Dieselbe Prüfung läuft in der CI, samt Doku-Struktur und, wo ein Plugin Dateien im Sync hält, den Hash-Dateien.
