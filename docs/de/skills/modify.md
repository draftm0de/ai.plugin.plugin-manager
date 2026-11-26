# 🛠 :modify

**Deutsch** | [English](../../en/skills/modify.md)

[Start](../../../README.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Begriffe](../concepts.md) · [Entwicklung](../development.md) · [Gemeinsame Dateien](../files.md)

## Beschreibung

Mit `modify` änderst du, was dein Repository über sich sagt: den technischen Namen, den Anzeigenamen und die Beschreibung. Ein Marketplace hat keine Beschreibung. Zuerst siehst du, welche Dateien sich ändern würden, auch im Eintrag des Marketplace. Geschrieben wird erst nach deinem Ja. Name und Adresse des Repositorys bleiben, die Dokumentation schreibt `modify` nicht um.

## Ablauf

1. Prüft, ob das Repository eingerichtet ist.
2. Fragt, was sich ändern soll.
3. Zeigt alle betroffenen Dateien, ohne zu schreiben.
4. Schreibt erst nach deinem Ja.
5. Nennt die nächsten Schritte: Dokumentation mit `docs` auffrischen, Änderungen selbst committen und pushen.

### Fragen aus dem Ablauf

| Frage | Was ist das? | Worauf achten |
| --- | --- | --- |
| Soll ich /plugin-manager:setup jetzt ausführen? | Die Einrichtung fehlt oder ist unvollständig | `modify` ändert erst, wenn sie abgeschlossen ist. Rufe es danach erneut auf. |
| Was soll sich ändern? | Technischer Name, Anzeigename oder Beschreibung | Ein Marketplace hat keine Beschreibung. |
| Neuer Wert für „`<Feld>`“ (bisher: `<Wert>`)? | Der neue Name oder Text | Ein neuer technischer Name ändert die Aufrufe und die Installation. |
| Darf ich schreiben? | Darüber steht die Liste der Dateien, die sich ändern, auch im Marketplace | Bei „Nein“ bleibt alles, wie es ist. |

## Beispiel

„Gib dem Plugin den Anzeigenamen Bewerbungs-Coach.“

## Liest und schreibt

Liest die Konfiguration und den zugehörigen Marketplace. Schreibt die Manifeste und, beim Plugin, den Eintrag im Marketplace, wenn dessen Ordner auf deinem Rechner verfügbar ist. Benennst du einen Marketplace um, werden die betroffenen Plugins nur genannt, nicht verändert.
