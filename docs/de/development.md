# Entwicklung

[Installation](installation.md) · [Skills](skills.md) · [Begriffe](concepts.md)

Für alle, die an diesem Plugin arbeiten. Zum Benutzen brauchst du diese Seite nicht.

## Voraussetzungen

- Git und Python 3.10 oder neuer. Make ist optional.
- Claude oder Codex mit installiertem Plugin Manager.
- Für die lokale Installation die jeweilige CLI (`claude` oder `codex`).
- Je ein GitHub-Repository für den Marketplace und für jedes Plugin, jeweils lokal geklont.

## Einrichten

1. Einen Marketplace haben: ein eigenes Repository, mit `/plugin-manager:setup` als „Marketplace“ eingerichtet und lokal geklont.
2. Plugin-Repository auf GitHub anlegen und klonen.
3. Darin `/plugin-manager:setup` ausführen, „Plugin“ wählen und den Marketplace nennen. Der Eintrag im Marketplace und die lokale Zuordnung entstehen dabei.
4. Anforderungen in `SCOPE.md` festhalten und die Skills unter `skills/<skill>/` bauen.

## Lokal testen

Im Ordner des Plugins:

```bash
make sync
```

```bash
make check test verify
```

Installiert wird im Ordner des Marketplace:

```bash
make -C ../<marketplace> install-local TARGET=claude
```

Danach eine neue Sitzung öffnen. Auch nicht committete Änderungen sind enthalten. Für Codex `TARGET=codex`.

## Veröffentlichen

Committen und auf den Standard-Branch pushen; installiert wird, was dort liegt. Es gibt keine Versionen, Tags oder Releases. Ein neues Plugin zuerst pushen, danach den Marketplace mit seinem Eintrag.
