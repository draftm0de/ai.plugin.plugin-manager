# Plugin Manager

**Deutsch** | [English](README.en.md)

<img src="assets/icon.png" alt="draftmode.io" width="48">

[Installation](docs/de/installation.md) · [Skills](docs/de/skills.md) · [Begriffe](docs/de/concepts.md) · [Entwicklung](docs/de/development.md)

Mit dem Plugin Manager entstehen Plugins, die alle gleich aufgebaut sind: eingerichtet, dokumentiert, geprüft und gepflegt.

## Was es tut

Der Manager richtet Plugin- und Marketplace-Repositories ein und hält ihre gemeinsamen Dateien aktuell. Er gibt jedem Plugin dieselben Standards für Code, Meldungen, Tests und Skills, schreibt die Dokumentation aus den Quellen, ändert Namen und Beschreibung und prüft die Struktur.

## Für wen

Für Entwickler und Teams, die Skills als installierbare Plugins für Claude oder Codex pflegen und wollen, dass alle ihre Plugins denselben Regeln folgen.

## Welches Problem es löst

Jedes neue Plugin beginnt sonst von vorn: eigene Ordner, eigene Regeln, eigene Fehlermeldungen, Doku, die dem Code hinterherläuft. Der Manager legt die gemeinsame Grundlage an, zieht Änderungen daran nach und meldet, was abweicht.

## Daten und Datenschutz

Der Manager schreibt in das Repository, das du auswählst, und, wenn ein Plugin angelegt, umbenannt, beschrieben oder zugeordnet wird, in den Ordner seines Marketplace. Dazu gehören: Verwaltungsdateien unter `.project/`, die gemeinsamen Dateien, Dokumentation und, nach deinem Ja, Änderungen an Name oder Beschreibung. Er commitet, pusht und veröffentlicht nie und liest keine Zugangsdaten oder privaten Daten. Was ein Skill liest und schreibt, steht bei jedem Skill. Der KI-Host verarbeitet die Quellen nach seinen eigenen Bedingungen.

## Dokumentation

[Installation](docs/de/installation.md) · [Skills](docs/de/skills.md) · [Begriffe](docs/de/concepts.md) · [Entwicklung](docs/de/development.md)

Lizenz: [MIT](LICENSE).

---

Dokumentation mit Plugin Manager erstellt.
