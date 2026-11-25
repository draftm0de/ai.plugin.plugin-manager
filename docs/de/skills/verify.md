# 🛠 :verify

**Deutsch** | [English](../../en/skills/verify.md)

[Start](../../../README.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Begriffe](../concepts.md) · [Entwicklung](../development.md) · [Gemeinsame Dateien](../files.md)

## Beschreibung

Meldet, ob ein Repository den Regeln entspricht, und was noch nicht belegt ist.

## Ablauf

1. Erkennt selbst, ob Plugin oder Marketplace.
2. Prüft die Struktur, bei Plugins auch die Standards und gemeinsamen Anweisungen, und die Dokumentation.
3. Meldet eine noch offene Einrichtung, ohne sie auszuführen.
4. Auf Wunsch vergleicht es `SCOPE.md` mit dem Quellcode.

## Beispiel

`/plugin-manager:verify` vor dem Pushen.

## Liest und schreibt

Liest das Repository. Schreibt nichts und führt keinen Code des Repositorys aus. Dieselbe Prüfung läuft in der CI, samt Doku-Struktur und, wo ein Plugin Dateien im Sync hält, den Hash-Dateien.

---

Dokumentation mit Plugin Manager erstellt.
