# Plugin Manager

**Deutsch** | [English](README.en.md)

<img src="assets/icon.png" alt="draftmode.io" width="48">

[Start](README.md) · [Installation](docs/de/installation.md) · [Skills](docs/de/skills.md) · [Begriffe](docs/de/concepts.md) · [Entwicklung](docs/de/development.md) · [Gemeinsame Dateien](docs/de/files.md)

Der Plugin Manager ist ein Plugin, mit dem du standardisiert

- **Plugins** und
- **Marketplaces**

erstellst, entwickelst und wartest.

Eigene Skills (`:setup`, `:docs`, `:modify`, `:verify`) führen dich durch die einzelnen Schritte.

Was dein Repository dafür braucht, rollt der Manager mit aus: gemeinsame Dateien und Ordner, Standards, Prüfskripte, `Makefile` und die GitHub-CI. Bevor er schreibt, nennt er die Dateien und fragt dich.

## ⚡ Schnellstart

### Installation

Du fügst den Marketplace einmal hinzu und installierst daraus den Plugin Manager.

#### Claude

- [Claude CLI](docs/de/installation.md#claude-cli)
- [Claude Desktop App](docs/de/installation.md#claude-desktop-app)

#### ChatGPT

- [Codex CLI](docs/de/installation.md#codex-cli)
- [ChatGPT Desktop App](docs/de/installation.md#chatgpt-desktop-app)

### Einrichtung

`/plugin-manager:setup`

Führe `:setup` aus, um deinen verbundenen Ordner als Plugin oder Marketplace zu konfigurieren. Der Skill führt dich mit Fragen durch die Konfiguration.

In Claude Code rufst du die Skills wie oben auf. In Codex und ChatGPT beschreibst du die Aufgabe oder wählst den Skill aus.

### Ein Plugin bauen

Zum Entwickeln brauchst du keinen eigenen Skill-Aufruf. Nach der Einrichtung öffnest du den Ordner deines Plugins und beschreibst einfach, was du haben möchtest. Dein Repository bringt dem Assistenten die Spielregeln mit: Er liest `AGENTS.md`, deine Anforderungen in `SCOPE.md` und die gemeinsamen Standards für Code, Meldungen, Tests und Skills.

Zuerst klärt ihr, was das Plugin können soll und was nicht, und haltet das in `SCOPE.md` fest. Was du nicht bestätigt hast, gilt nicht als Anforderung. Erst danach baut der Assistent die Skills unter `skills/`, samt Tests. Mit `make verify` oder `/plugin-manager:verify` prüfst du jederzeit, ob alles noch den Regeln entspricht.

Ein Beispielprompt:

```text
Ich möchte ein Plugin, das aus meinen Meeting-Notizen eine Aufgabenliste erstellt.
Jede Aufgabe soll eine verantwortliche Person und, wenn genannt, einen Termin haben.
Frag mich zuerst, was unklar ist, und halte die Anforderungen in SCOPE.md fest.
Baue den Skill erst, wenn ich die Anforderungen bestätigt habe.
```

## 🛠 Features

### :setup

Konfiguriert dein Repository als Plugin oder Marketplace und hält dessen gemeinsame Dateien im Sync. Vor dem Schreiben nennt es die Dateien und fragt dich.

📖 [/plugin-manager:setup – Mehr dazu](docs/de/skills/setup.md)

### :docs

Prüft die Struktur der Dokumentation und legt fehlende Seiten `skills/<skill>.md` an. Du bekommst einen Bericht, was wo fehlt und was jeder Bereich enthalten soll.

📖 [/plugin-manager:docs – Mehr dazu](docs/de/skills/docs.md)

### :modify

Ändert Name, Anzeigename und Beschreibung. Zeigt zuerst, was sich ändert, und schreibt erst nach deinem Ja.

📖 [/plugin-manager:modify – Mehr dazu](docs/de/skills/modify.md)

### :verify

Prüft nur lesend, ob Aufbau, Standards und Dokumentation den Regeln entsprechen.

📖 [/plugin-manager:verify – Mehr dazu](docs/de/skills/verify.md)

Lizenz: [MIT](LICENSE).

---

Dokumentation mit Plugin Manager erstellt.
