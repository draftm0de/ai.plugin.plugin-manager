# 🛠 Skills

**Deutsch** | [English](../en/skills.md)

[Start](../../README.md) · [Installation](installation.md) · [Skills](skills.md) · [Begriffe](concepts.md) · [Entwicklung](development.md) · [Gemeinsame Dateien](files.md)

Ein Skill ist vergleichbar mit einer Arbeitsanleitung für einen Mitarbeiter.

Er beschreibt, wie der KI-Assistent eine bestimmte Aufgabe erledigen soll, welche Regeln dabei gelten und welche Schritte einzuhalten sind.

Plugin Manager bringt die folgenden Skills mit, je einen pro Aufgabe. In Claude Code rufst du sie mit ihrem Namen auf. In Codex und ChatGPT beschreibst du die Aufgabe oder wählst den Skill aus.

## 📖 Skills

### docs

`/plugin-manager:docs`

`docs` kümmert sich um den Aufbau deiner Dokumentation. Einen Teil der Seiten erstellt es selbst, bei den anderen schreibst du die Texte und es kommt nur auf die Struktur an. Fehlende Seiten legt es an. Was nicht passt, bekommst du gemeldet.

Welche Seiten das sind und was geprüft wird, hängt davon ab, ob dein Repository ein Plugin oder ein Marketplace ist. `docs` erkennt das selbst.

📖 [/plugin-manager:docs – Mehr dazu](skills/docs.md)

### modify

`/plugin-manager:modify`

Mit `modify` änderst du, was dein Repository über sich sagt: den technischen Namen, den Anzeigenamen und die Beschreibung. Ein Marketplace hat keine Beschreibung. Zuerst siehst du, welche Dateien sich ändern würden, auch im Eintrag des Marketplace. Geschrieben wird erst nach deinem Ja. Name und Adresse des Repositorys bleiben, die Dokumentation schreibt `modify` nicht um.

📖 [/plugin-manager:modify – Mehr dazu](skills/modify.md)

### setup

`/plugin-manager:setup`

Hier beginnst du. `setup` konfiguriert dein geklontes Repository als Plugin oder als Marketplace und fragt dich dafür Schritt für Schritt, was es wissen muss. Danach hält es die gemeinsamen Dateien im Sync. Bevor es schreibt, nennt es die Dateien. Hast du eine davon selbst geändert, entscheidest du, ob deine Fassung bleibt oder die Vorlage übernommen wird. Du kannst es jederzeit erneut aufrufen.

📖 [/plugin-manager:setup – Mehr dazu](skills/setup.md)

### verify

`/plugin-manager:verify`

`verify` sagt dir, ob dein Repository den Regeln entspricht. Es erkennt selbst, ob es ein Plugin oder ein Marketplace ist, und prüft Aufbau, gemeinsame Standards und Dokumentation. Auf Wunsch vergleicht es auch `SCOPE.md` mit dem Quellcode. Es liest nur: Es ändert nichts und führt keinen Code deines Repositorys aus.

📖 [/plugin-manager:verify – Mehr dazu](skills/verify.md)

<hr>

Diese Seite wird automatisch über `/plugin-manager:docs` erstellt. Ändere sie nicht von Hand.
