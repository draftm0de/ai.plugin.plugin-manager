# Entwicklung

[Installation](installation.md) · [Plugins](plugins.md) · [Begriffe](concepts.md)

Für alle, die an diesem Marketplace arbeiten. Zum Benutzen brauchst du diese Seite nicht.

## Voraussetzungen

- Git und Python 3.10 oder neuer. Make ist optional.
- Claude oder Codex mit installiertem Plugin Manager.
- Für die lokale Installation die jeweilige CLI (`claude` oder `codex`).
- Je ein GitHub-Repository für den Marketplace und für jedes Plugin, jeweils lokal geklont.

## Einrichten

1. Marketplace-Repository auf GitHub anlegen und klonen.
2. Darin `/plugin-manager:setup` ausführen und „Marketplace“ wählen.
3. Plugin-Repository anlegen und klonen, darin `/plugin-manager:setup` ausführen, „Plugin“ wählen und diesen Marketplace nennen. Der Eintrag in `marketplace.json` und die lokale Zuordnung entstehen dabei.

## Lokal testen

Im Marketplace-Ordner:

```bash
make install-local TARGET=claude
```

Das installiert die lokalen Stände aller gelisteten Plugins als eigenen Entwicklungs-Marketplace `<name>-dev`, auch nicht committete Änderungen. Danach eine neue Sitzung öffnen. Für Codex `TARGET=codex`.

## Veröffentlichen

Zuerst die Plugins committen und pushen, dann den Marketplace:

```bash
make sync
```

```bash
make check test verify
```

Installiert wird, was auf dem Standard-Branch liegt. Es gibt keine Versionen, Tags oder Releases. Wer den Marketplace schon nutzt, aktualisiert ihn wie unter [Installation](installation.md) beschrieben.
