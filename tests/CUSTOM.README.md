# Tests im Plugin Manager / Tests in the Plugin Manager

Ergänzt die verwaltete [README.md](README.md). / Adds to the managed [README.md](README.md).

Im Manager wählt `make test TEST_GROUP=plugin-create` eine Komponente aus. `make test-native` (aus `CUSTOM.mk`) führt die Hosttests aus, ohne persönliche Installationen zu verändern. Modelltests: `make test-behavior`, `make test-behavior-review` und `make test-behavior-skills`; sie können Credits verbrauchen und laufen nie mit dem normalen Testlauf.

In the Manager, `make test TEST_GROUP=plugin-create` selects a component. `make test-native` (from `CUSTOM.mk`) runs the host tests without changing personal installations. Model tests: `make test-behavior`, `make test-behavior-review` and `make test-behavior-skills`; they may consume credits and never run with the default suite.

Native selection uses only `--kind native` / `make test-native`; the runner sets `AI_PLUGIN_TEST_NATIVE`. Previous native gate names are not consumed.

## Testebenen des Skeleton-Syncs (setup_state) / Test layers of the skeleton sync

- **Regeltests / rule tests** (`tests/integration/project_setup/test_sync.py`, `test_removal.py`): `FictionalSandbox` fuehrt die echten Skripte unveraendert aus; der minimale fiktive Parent mit festen, im Test definierten Bytes kommt als Kontext (`docs/architecture.md`). Keine Funktion wird gemockt, kein Konfigurationsframework. Erwartungen stammen aus Literalen und `hashlib`, nie aus Produktionsvorlagen oder der echten Dateiliste. Fehler (Schreiben, `rmdir`, `unlink`) werden gezielt gemockt, alle Dateioperationen laufen echt in Temp-Verzeichnissen. / Run the real scripts unchanged; the minimal fictional parent is given as context; expectations come from literals and `hashlib`; failures are mocked selectively.
- **Auslieferungs-/Integrationstests / delivery and integration** (`test_setup.py`, `test_fresh.py`): `Sandbox` kopiert die echten Parent-Daten (Manifeste, Vorlagen) und gibt sie als Kontext mit (kanonische Vorlagenauslieferung, Zielerkennung, Konflikte, Races). Sie pruefen nur die stabile Liste `FILES`; `keep.md`/`remove.md` (manuelle Synctest-Quellen) duerfen aus dem echten Parent verschwinden, ohne dass diese Tests brechen. / Isolated copy of the real parent data, given as context, for canonical template delivery.
- **Aufrufwege / call paths:** `fx.load_state(**box.ctx_args)` ruft das Paket im Prozess auf (Fehlerinjektion per Patch auf das jeweilige Modul). `box.call(...)` startet die echte Kommandozeile im isolierten Modus ueber `tests/support/run_state.py`, das den Kontext im Code mitgibt. Die ausgelieferte Einstiegsdatei prueft `test_context.py` ohne Kontext. / In-process calls for fault injection, the isolated command line through the driver, and the shipped entry file without a context.
- **Generator-Integration** (`GeneratorCooperationTests`, `GuidedConfigurationTests`): echter Generator und echte Vorlagen sind der Gegenstand und klar getrennt von den Regeltests. / Real generator and real templates are the subject.
- **Texttests / text tests** (`tests/contracts/test_plugin_manager_entry.py`): belegen Anweisungstexte, kein Modell- oder Hostverhalten. / Instruction evidence only.
