# 🛠 :docs

**Deutsch** | [English](../../en/skills/docs.md)

[Start](../../../README.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Begriffe](../concepts.md) · [Entwicklung](../development.md) · [Gemeinsame Dateien](../files.md)

## Beschreibung

`docs` kümmert sich um den Aufbau deiner Dokumentation. Einen Teil der Seiten erstellt es selbst, bei den anderen schreibst du die Texte und es kommt nur auf die Struktur an. Fehlende Seiten legt es an. Was nicht passt, bekommst du gemeldet.

Welche Seiten das sind und was geprüft wird, hängt davon ab, ob dein Repository ein Plugin oder ein Marketplace ist. `docs` erkennt das selbst.

### Plugins

#### Automatisch erstellt

| Datei | Wodurch der Inhalt entsteht |
| --- | --- |
| `docs/<lang>/installation.md` | fester Text, dazu der Name deines Plugins aus `plugin.json` sowie Name und Adresse deines Marketplace |
| `docs/<lang>/skills.md` | fester Text, dazu je Skill der Abschnitt „Beschreibung“ aus seiner Skill-Seite |
| `docs/<lang>/concepts.md` | fester Text |
| `docs/<lang>/development.md` | fester Text |
| `docs/<lang>/files.md` | fester Text, dazu die Dateibäume aus dem, was der Plugin Manager ausliefert |

#### Von dir geschrieben

Vorgeschrieben sind nur die Überschriften. Alles darunter ist frei.

**`README.md`** (und je weitere Sprache `README.<lang>.md`)

```text
# <Titel>                  Pflicht, genau eine
│   Vorstellung            frei
├── ## ⚡ Schnellstart      Pflicht
│   └── ### …              frei
└── ## 🛠 Features          Pflicht
    └── ### :<skill>       Pflicht, eine je Skill
            Erklärung      höchstens 200 Zeichen
            Link           auf docs/<lang>/skills/<skill>.md
```

**`docs/<lang>/skills/<skill>.md`** (eine Datei je Skill, Dateiname gleich Skill-Name)

```text
# <Titel>                  Pflicht, genau eine
├── ## Beschreibung        Pflicht
│   └── ### …              frei
├── ## Ablauf              Pflicht
├── ## Beispiel            Pflicht
└── ## Liest und schreibt  Pflicht
```

Die `##`-Überschriften müssen genau so heißen und in dieser Reihenfolge stehen. In der README darf vor ihnen ein Icon stehen. Unter „Beschreibung“ erscheint in `skills.md` nur der Text bis zur ersten Unterüberschrift.

#### Geprüft wird

- Alle Seiten sind da, und die erzeugten Seiten haben genau ihre Überschriften.
- Die README hat Schnellstart und Features, mit genau einem Eintrag je Skill, kurz genug und verlinkt.
- `skills.md` hat einen Eintrag je Skill, und jede Skill-Seite hat ihre vier Abschnitte.

### Marketplaces

#### Automatisch erstellt

| Datei | Wodurch der Inhalt entsteht |
| --- | --- |
| `docs/<lang>/installation.md` | fester Text, dazu Name und Adresse des Marketplace; nur hinzufügen, aktualisieren, entfernen |
| `docs/<lang>/concepts.md` | fester Text, derselbe wie bei Plugins |
| `docs/<lang>/development.md` | fester Text: Plugins verbinden, lokal testen, Befehle und CI |

Es gibt keine Seite je Plugin, keine Plugin-Liste und keine Seite „Gemeinsame Dateien“.

#### Von dir geschrieben

Vorgeschrieben sind nur die Überschriften. Alles darunter ist frei.

**`README.md`** (und je weitere Sprache `README.<lang>.md`)

```text
# <Titel>                  Pflicht, genau eine
│   Einleitung             frei, kein Schnellstart
└── ## 📦 Plugins          Pflicht
    └── ### <Anzeigename>  Pflicht, eines je Plugin aus marketplace.json
            Erklärung      frei
            Link           auf die README im Repository des Plugins
```

Vor `## Plugins` darf ein Icon stehen.

#### Geprüft wird

- Alle Seiten sind da, und die erzeugten Seiten haben genau ihre Überschriften.
- Die README hat genau einen Eintrag je gelistetem Plugin, jeder mit Link in dessen Repository.
- Alte Seiten `plugins.md` oder `files.md` werden gemeldet, aber nicht gelöscht.

### Für beide

Die erzeugten Seiten schreibt `/plugin-manager:docs` bei jedem Lauf neu. Ändere sie nicht von Hand, deine Änderungen gingen verloren; jede trägt unten einen Hinweis darauf. Deine eigenen Seiten legt es nur an, wenn sie fehlen, und überschreibt sie nie.

Fehlt eine Angabe, zum Beispiel die Adresse des Marketplace, steht auf der Seite „(noch nicht festgelegt)“, und der Befehl meldet es.

`/plugin-manager:verify`, `make verify` und die CI prüfen außerdem, ob jede Sprache verlinkt ist und keine internen Links ins Leere führen. Alles, was sie finden, ist eine **Warnung**: Die CI bleibt grün. Ob und wie du deine Dokumentation schreibst, ist deine Entscheidung.

`<lang>` steht für jede gewählte Dokumentationssprache.

## Ablauf

1. Prüft, ob das Repository eingerichtet ist, und klärt beim ersten Mal die Doku-Sprachen.
2. Schreibt die automatisch erstellten Seiten neu und legt fehlende Seiten an.
3. Prüft Struktur und Links.
4. Berichtet kurz, was geschrieben wurde und was noch offen ist. Texte schreibt es nicht.

## Beispiel

`/plugin-manager:docs` nach einem neuen Skill: Die Skills-Seite bekommt seinen Abschnitt.

## Liest und schreibt

Liest die Angaben deines Repositorys, zum Beispiel `plugin.json`, ohne Code auszuführen. Schreibt README und Seiten unter `docs/`; vorhandene eigene Texte ändert es nicht.
