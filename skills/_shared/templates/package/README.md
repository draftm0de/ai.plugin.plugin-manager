# Plugin Manager

**Deutsch** | [English](README.en.md)

Dieses Plugin dokumentiert zugängliche lokale Skills und Plugins anhand ihrer Quellen. Die Dokumentationssprachen werden pro Repository festgelegt: nur Deutsch, nur Englisch oder beide. Nutze `setup`, um einen Marketplace einzurichten oder ein separates Plugin zu erstellen und zuzuordnen, `docs` zur Erneuerung der Dokumentation, `modify` für Name und Beschreibung oder `verify` zur lesenden Strukturprüfung. Der Agent fragt bei wesentlichen Unklarheiten nach. Eine erfolgreiche Strukturprüfung bestätigt noch keine Produktionsreife. Das Plugin veröffentlicht und installiert nichts ohne Auftrag.

In Claude: `/plugin-manager:verify QUELLPFAD`, entsprechend `/plugin-manager:setup` (Einrichtung, Plugin oder Marketplace), `:docs` oder `:modify`. In ChatGPT fordere die Aktion in natürlicher Sprache an. Die Quelle muss dem Host zugänglich sein; die Helfer benötigen Python 3.10 oder neuer.

[Workflow und Grenzen](skills/_shared/WORKFLOWS.md)

## Veröffentlichen

Du committest und pushst selbst; installiert wird, was auf dem Standard-Branch liegt. Neue Plugin-Repositories vor ihren Marketplace-Einträgen pushen. Keine Versionen, Tags oder Releases.

Git und Python 3.10+ sind für die Verwaltungswerkzeuge erforderlich; Make ist nur ein Komfortzugang. Für die Verwaltung wird die Host-CLI nur bei automatischer lokaler Installation/Aktualisierung benötigt; ausdrücklich gestartete Modelltests benötigen ebenfalls eine authentifizierte CLI. Keine zusätzlichen Python-Pakete.

Lokale Snapshots lesen den aktuellen Checkout einschließlich uncommitteter Änderungen, unabhängig vom Branch. Nach Änderungen oder Branchwechsel `install-local` ausführen und eine neue Host-Sitzung öffnen. Kein Commit, Push oder PR ist für lokale Tests erforderlich. Es bleibt bei einem gemeinsamen `<marketplace-id>-dev`, ohne zusätzliche Marketplaces pro Branch.

Die lokale Zuordnung eines Plugins zu seinem einen Marketplace richtet `plugin-manager` (associate) ein und ändert sie. Der Pfad des Marketplace-Checkouts steht in der von Git ignorierten `.project/plugins/plugin-manager/local.json` des Plugins; die Checkouts der Plugins stehen unter `sources` in der von Git ignorierten `.local/marketplace.json` des Marketplace; diese Zuordnungen werden nicht committet. `local-marketplace.example.json` ist eine optionale manuelle Kopiervorlage für die Marketplace-Seite.

## Skills

`setup`, `docs`, `modify` und `verify`; die Marketplace-Zuordnung eines Plugins ist ein Flow von setup. Gemeinsame Regeln: `skills/_shared/WORKFLOWS.md`.
