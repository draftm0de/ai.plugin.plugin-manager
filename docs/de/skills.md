# Skills

**Deutsch** | [English](../en/skills.md)

<img src="../../assets/icon.png" alt="draftmode.io" width="48">

[Start](../../README.md) · [Installation](installation.md) · [Skills](skills.md) · [Begriffe](concepts.md) · [Entwicklung](development.md)

Fünf Skills, je einer pro Aufgabe. In Claude Code rufst du sie mit `/plugin-manager:<skill>` auf.

## Überblick

| Skill | Wofür |
| --- | --- |
| [docs](#docs) | Dokumentation aus den Quellen schreiben |
| [modify](#modify) | Name, Anzeigename, Beschreibung ändern |
| [setup](#setup) | Einrichten und aktuell halten |
| [verify](#verify) | Nur lesend prüfen |

## docs

### Beschreibung

Schreibt oder aktualisiert die Dokumentation eines Plugins oder Marketplace in den gewählten Sprachen, aus `SCOPE.md`, den Skills und dem Quellcode.

### Ablauf

1. Prüft, ob das Repository eingerichtet ist und der Schreibstil `docs/style.md` vorhanden ist.
2. Liest die Quellen und klärt Offenes mit dir.
3. Schreibt README, Installation, Skills beziehungsweise Plugin-Liste und Begriffe.
4. Prüft Struktur und Links.

### Beispiel

`/plugin-manager:docs` nach einem neuen Skill: Die Skills-Seite bekommt seinen Abschnitt.

### Liest und schreibt

Liest den Schreibstil und die Quellen des Repositorys, ohne deren Code auszuführen. Schreibt README und Seiten unter `docs/`, vorhandene eigene Texte bleiben.


## modify

### Beschreibung

Ändert, was ein Repository über sich sagt: technischen Namen, Anzeigenamen und Beschreibung. Ein Marketplace hat keine Beschreibung.

### Ablauf

1. Prüft, ob das Repository eingerichtet ist.
2. Fragt, was sich ändern soll.
3. Zeigt alle betroffenen Dateien, ohne zu schreiben.
4. Schreibt erst nach deinem Ja.
5. Nennt die nächsten Schritte: Dokumentation mit `docs` auffrischen, Änderungen selbst committen und pushen.

### Beispiel

„Gib dem Plugin den Anzeigenamen Bewerbungs-Coach.“

### Liest und schreibt

Liest die Konfiguration und den zugehörigen Marketplace. Schreibt die Manifeste und, beim Plugin, den Eintrag im Marketplace, wenn dessen Ordner auf deinem Rechner verfügbar ist. Benennst du einen Marketplace um, werden die betroffenen Plugins nur genannt, nicht verändert.


## setup

### Beschreibung

Bringt ein Plugin- oder Marketplace-Repository in den eingerichteten Zustand und hält die gemeinsamen Dateien aktuell. Beliebig oft aufrufbar.

### Ablauf

1. Sprache klären.
2. Plugin oder Marketplace konfigurieren.
3. Gemeinsame Dateien anlegen und aktualisieren; unveränderte Kopien ohne Frage, geänderte nur nach deiner Entscheidung.
4. Fehlt der Schreibstil `docs/style.md`, wählst du die Vorlage oder beschreibst deinen eigenen.
5. Eine Zeile „vollständig konfiguriert“.

Eine Datei, die du behalten hast, holst du zurück, indem du `setup` darum bittest, zum Beispiel „Nimm das Makefile wieder in den Sync“.

Jedes Plugin gehört zu genau einem Marketplace. Willst du ihn wechseln oder liegt sein Ordner jetzt woanders, bitte `setup` darum.

In Plugins liegt auch ein Git-Hook, der die Standards vor jedem Commit prüft. Er läuft erst, wenn du ihn einmal pro Klon aktivierst: `git config core.hooksPath githooks`.

### Beispiel

`/plugin-manager:setup` in einem leeren, geklonten Repository.

### Liest und schreibt

Liest den Ordner und den ausgewählten Marketplace. Schreibt Verwaltungsdateien unter `.project/`, eine Regel in `.gitignore`, die gemeinsamen Dateien, den Schreibstil und beim Anlegen das Gerüst. Beim Anlegen eines Plugins und beim Wechsel des Marketplace ändert es auch den ausgewählten Marketplace-Ordner, beim Wechsel zusätzlich den bisherigen. Gelöscht werden nur gemeinsame Dateien, deren Vorlage entfallen ist: unveränderte von selbst, geänderte nur nach deiner Entscheidung.


## verify

### Beschreibung

Meldet, ob ein Repository den Regeln entspricht, und was noch nicht belegt ist.

### Ablauf

1. Erkennt selbst, ob Plugin oder Marketplace.
2. Prüft die Struktur, bei Plugins auch die Standards und gemeinsamen Anweisungen, und die Dokumentation.
3. Meldet eine noch offene Einrichtung, ohne sie auszuführen.
4. Auf Wunsch vergleicht es `SCOPE.md` mit dem Quellcode.

### Beispiel

`/plugin-manager:verify` vor dem Pushen.

### Liest und schreibt

Liest das Repository. Schreibt nichts und führt keinen Code des Repositorys aus.

---

Dokumentation mit Plugin Manager erstellt.
