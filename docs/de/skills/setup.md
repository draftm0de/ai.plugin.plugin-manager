# 🛠 :setup

**Deutsch** | [English](../../en/skills/setup.md)

[Start](../../../README.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Begriffe](../concepts.md) · [Entwicklung](../development.md) · [Gemeinsame Dateien](../files.md)

## Beschreibung

Hier beginnst du. `setup` konfiguriert dein geklontes Repository als Plugin oder als Marketplace und fragt dich dafür Schritt für Schritt, was es wissen muss. Danach hält es die gemeinsamen Dateien im Sync. Bevor es schreibt, nennt es die Dateien. Hast du eine davon selbst geändert, entscheidest du, ob deine Fassung bleibt oder die Vorlage übernommen wird. Du kannst es jederzeit erneut aufrufen.

## Ablauf

1. Sprache klären.
2. Plugin oder Marketplace konfigurieren.
3. Gemeinsame Dateien anlegen und aktualisieren: erst nennt es die Dateien und schreibt nach deinem Ja; für geänderte Dateien entscheidest du je Datei. Danach listet es auf, was es geschrieben hat.
4. Eine Zeile „vollständig konfiguriert“.

Welche Dateien gemeinsam sind und was eine eigene Änderung bedeutet, steht unter [Gemeinsame Dateien](../files.md).

Eine Datei, die du behalten hast, holst du zurück, indem du `setup` darum bittest, zum Beispiel „Nimm das Makefile wieder in den Sync“.

Jedes Plugin gehört zu genau einem Marketplace. Willst du ihn wechseln oder liegt sein Ordner jetzt woanders, bitte `setup` darum.

In Plugins liegt auch ein Git-Hook, der die Standards vor jedem Commit prüft. Er läuft erst, wenn du ihn einmal pro Klon aktivierst: `git config core.hooksPath githooks`.

## Beispiel

`/plugin-manager:setup` in einem leeren, geklonten Repository.

## Liest und schreibt

Liest den Ordner und den ausgewählten Marketplace. Schreibt Verwaltungsdateien unter `.project/`, eine Regel in `.gitignore`, die gemeinsamen Dateien, den Schreibstil und beim Anlegen das Gerüst. Beim Anlegen eines Plugins und beim Wechsel des Marketplace ändert es auch den ausgewählten Marketplace-Ordner, beim Wechsel zusätzlich den bisherigen. Gelöscht werden nur gemeinsame Dateien, deren Vorlage entfallen ist: unveränderte von selbst, geänderte nur nach deiner Entscheidung.

---

Dokumentation mit Plugin Manager erstellt.
