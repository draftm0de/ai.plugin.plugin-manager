# 🛠 :docs

**Deutsch** | [English](../../en/skills/docs.md)

[Start](../../../README.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Begriffe](../concepts.md) · [Entwicklung](../development.md) · [Gemeinsame Dateien](../files.md)

## Beschreibung

`docs` kümmert sich um den Aufbau deiner Dokumentation. Einen Teil der Seiten erstellt es selbst, bei den anderen schreibst du die Texte und es kommt nur auf die Struktur an. Fehlende Skill-Seiten legt es an. Was nicht passt, bekommst du gemeldet.

### Automatisch erstellte Dateien

Diese Seiten schreibt `/plugin-manager:docs` bei jedem Lauf neu. Ändere sie nicht von Hand, deine Änderungen gingen verloren. Jede trägt unten einen Hinweis darauf.

| Datei | Wodurch der Inhalt entsteht |
| --- | --- |
| `docs/<lang>/installation.md` | fester Text, dazu Name deines Plugins aus `plugin.json` sowie Name und Adresse deines Marketplace |
| `docs/<lang>/skills.md` | fester Text, dazu je Skill der Abschnitt „Beschreibung“ aus seiner Skill-Seite |
| `docs/<lang>/concepts.md` | fester Text |
| `docs/<lang>/development.md` | fester Text |
| `docs/<lang>/files.md` | fester Text, dazu die Dateibäume aus dem, was der Plugin Manager ausliefert |

Fehlt eine Angabe, zum Beispiel die Adresse des Marketplace, steht auf der Seite „(noch nicht festgelegt)“, und der Befehl meldet es.

### Dateien, die du selbst schreibst

Diese Seiten legt `/plugin-manager:docs` nur an, wenn sie fehlen. Danach gehören sie dir und werden nie überschrieben. Vorgeschrieben ist nur die Struktur.

| Datei | Struktur |
| --- | --- |
| `README.md`, `README.<lang>.md` | Titel und Vorstellung, `## ⚡ Schnellstart` mit freien Unterabschnitten, `## 🛠 Features` mit je einem `### :<skill>`: höchstens 200 Zeichen und ein Link auf die Skill-Seite |
| `docs/<lang>/skills/<skill>.md` | je Skill eine Datei, Dateiname gleich Skill-Name: `## Beschreibung`, `## Ablauf`, `## Beispiel`, `## Liest und schreibt` |

Unter „Beschreibung“ erscheint in `skills.md` nur der Text bis zur ersten Unterüberschrift.

### Was geprüft wird

`/plugin-manager:verify`, `make verify` und die CI prüfen, ob alle Seiten da sind, die Überschriften stimmen, jede Sprache verlinkt ist und keine internen Links ins Leere führen. Alles, was sie finden, ist eine **Warnung**: Die CI bleibt grün. Ob und wie du deine Dokumentation schreibst, ist deine Entscheidung.

`<lang>` steht für jede gewählte Dokumentationssprache. Bei Marketplaces werden `installation.md`, `concepts.md` und `development.md` erstellt; von Hand schreibst du dort nur die README mit je einem Eintrag pro Plugin.

## Ablauf

1. Prüft, ob das Repository eingerichtet ist, und klärt beim ersten Mal die Doku-Sprachen.
2. Schreibt die automatisch erstellten Seiten neu und legt fehlende Seiten an.
3. Prüft Struktur und Links.
4. Berichtet, was noch zu schreiben ist und was in den Abschnitt gehört. Texte schreibt es nicht.

## Beispiel

`/plugin-manager:docs` nach einem neuen Skill: Die Skills-Seite bekommt seinen Abschnitt.

## Liest und schreibt

Liest die Angaben deines Repositorys, zum Beispiel `plugin.json`, ohne Code auszuführen. Schreibt README und Seiten unter `docs/`; vorhandene eigene Texte ändert es nicht.

---

Dokumentation mit Plugin Manager erstellt.
