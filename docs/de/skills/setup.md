# 🛠 :setup

**Deutsch** | [English](../../en/skills/setup.md)

[Start](../../../README.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Begriffe](../concepts.md) · [Entwicklung](../development.md) · [Gemeinsame Dateien](../files.md)

## Beschreibung

Hier beginnst du. `setup` konfiguriert dein geklontes Repository als Plugin oder als Marketplace und fragt dich dafür Schritt für Schritt, was es wissen muss. Das Repository braucht eine GitHub-Adresse (`origin`); fehlt sie, nennt `setup` die Befehle und hört auf. Danach hält es die gemeinsamen Dateien im Sync. Bevor es schreibt, nennt es die Dateien. Hast du eine davon selbst geändert, entscheidest du, ob deine Fassung bleibt oder die Vorlage übernommen wird. Du kannst es jederzeit erneut aufrufen.

## Ablauf

1. Sprache klären.
2. Git-Repository und `origin` prüfen.
3. Plugin oder Marketplace konfigurieren.
4. Gemeinsame Dateien anlegen und aktualisieren: erst nennt es die Dateien und schreibt nach deinem Ja; für geänderte Dateien entscheidest du je Datei. Danach listet es auf, was es geschrieben hat.
5. Eine Zeile „vollständig konfiguriert“.

Welche Dateien gemeinsam sind und was eine eigene Änderung bedeutet, steht unter [Gemeinsame Dateien](../files.md).

Eine Datei, die du behalten hast, holst du zurück, indem du `setup` darum bittest, zum Beispiel „Nimm das Makefile wieder in den Sync“.

Jedes Plugin gehört zu genau einem Marketplace. Willst du ihn wechseln oder liegt sein Ordner jetzt woanders, bitte `setup` darum.

In Plugins liegt auch ein Git-Hook, der die Standards vor jedem Commit prüft. Er läuft erst, wenn du ihn einmal pro Klon aktivierst: `git config core.hooksPath githooks`.

### Fragen aus dem Ablauf

`setup` fragt nur, was es nicht selbst wissen kann, und immer mit denselben Worten. Was die Fragen bedeuten:

#### Gilt für Beide

| Frage | Was ist das? | Worauf achten |
| --- | --- | --- |
| Welche Bediensprache soll ich verwenden? | In welcher Sprache der Plugin Manager mit dir spricht | Nur für dich, wird nicht committet. Die Doku-Sprachen sind davon unabhängig. |
| Meldung: Git-Repository oder GitHub-Adresse (`origin`) fehlt | Dein Ordner braucht beides | Führe die gezeigten Befehle aus und rufe `setup` erneut auf. Auf GitHub muss das Repository noch nicht existieren. |
| Plugin oder Marketplace? | Ein Plugin ist das Paket mit Skills, ein Marketplace das Verzeichnis, aus dem man installiert | Lege zuerst den Marketplace an, dann die Plugins. |

#### Marketplace

| Frage | Was ist das? | Worauf achten |
| --- | --- | --- |
| Wie lautet der technische Name? | Die Kennung, zum Beispiel in `plugin@marketplace` | Kleinbuchstaben, Ziffern und Bindestriche. Mit `modify` änderbar, wer den Marketplace nutzt, fügt ihn danach neu hinzu. |
| Wie lautet der Anzeigename? | Der lesbare Name | Frei wählbar, mit `modify` änderbar. |
| Wer ist der Herausgeber? | Person oder Organisation, die den Marketplace veröffentlicht | Steht im Katalog und ist damit sichtbar. |

#### Plugin

| Frage | Was ist das? | Worauf achten |
| --- | --- | --- |
| Wie lautet der technische Name? | Die Kennung, zum Beispiel in `/name:skill` | Kleinbuchstaben, Ziffern und Bindestriche. Das erste Skill-Gerüst heißt genauso; beim Bauen gibst du dem Skill seinen eigenen Namen. |
| Wie lautet der Anzeigename? | Der lesbare Name | Frei wählbar, mit `modify` änderbar. |
| Was tut das Plugin, in ein bis zwei Sätzen? | Die Beschreibung, die auch im Marketplace steht | „Noch offen“ ist erlaubt, mit `modify` änderbar. |
| Wer ist der Herausgeber? | Wer das Plugin veröffentlicht | Ist sichtbar. |
| Welche Doku-Sprachen? | Deutsch, Englisch oder beide, mit einer Standardsprache | Jede Sprache heißt eigene Texte pflegen. |
| Welche Lizenz? | Was andere mit deinem Code dürfen | MIT erlaubt fast alles. Für eine andere Lizenz brauchst du ihren vollständigen Text. „Später entscheiden“ heißt: Es sind noch keine Rechte erteilt. |
| Welches Jahr steht im Copyright? (nur MIT) | Das Jahr im Copyright-Vermerk | |
| Wer ist Rechteinhaber? (nur MIT) | Wem die Rechte gehören | Das kann jemand anderes sein als der Herausgeber, zum Beispiel deine Firma. |
| In welchen Marketplace gehört das Plugin? | Der Marketplace-Ordner, in den das Plugin eingetragen wird | Er liegt geklont auf deinem Rechner und ist mit `setup` eingerichtet. Jedes Plugin gehört zu genau einem. |

#### Beim Schreiben und später

| Frage | Was ist das? | Worauf achten |
| --- | --- | --- |
| Darf ich schreiben? | Darüber steht die Liste aller Dateien, die angelegt, geändert oder gelöscht werden. `../` meint ein anderes Repository, zum Beispiel deinen Marketplace. | Bei „Nein“ wird nichts davon geschrieben. |
| `<Datei>` weicht von der Vorlage ab. | Eine gemeinsame Datei und ihre Vorlage unterscheiden sich | „Meine Datei behalten“ lässt deine Fassung ohne Aktualisierung, bis du sie erneut änderst oder eine neue Vorlage kommt. |
| Die Vorlage zu `<Datei>` ist entfallen. | Der Plugin Manager liefert diese Datei nicht mehr | Gefragt wirst du nur, wenn du sie geändert hattest. |

## Beispiel

`/plugin-manager:setup` (Codex: `$plugin-manager:setup`) in einem leeren, geklonten Repository.

## Liest und schreibt

Liest den Ordner, seine Git-Angaben und den ausgewählten Marketplace. Schreibt Verwaltungsdateien unter `.project/`, eine Regel in `.gitignore`, die gemeinsamen Dateien, den Schreibstil und beim Anlegen das Gerüst. Beim Anlegen eines Plugins und beim Wechsel des Marketplace ändert es auch den ausgewählten Marketplace-Ordner, beim Wechsel zusätzlich den bisherigen. Gelöscht werden nur gemeinsame Dateien, deren Vorlage entfallen ist: unveränderte von selbst, geänderte nur nach deiner Entscheidung.
