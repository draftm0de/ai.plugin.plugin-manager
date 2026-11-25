# Own targets of the Manager; the managed Makefile includes this file.
CASE ?=
BEHAVIOR_OUTPUT ?=
OUTPUT ?=
LANGUAGES ?=
DEFAULT_LANGUAGE ?=
TITLE ?=

.PHONY: test-native test-behavior-review test-behavior-skills inspect scaffold validate-docs build-skeleton-hashes check-skeleton-hashes
test-native:
	$(PYTHON) -B scripts/run_tests.py --kind native $(if $(TEST_GROUP),--group "$(TEST_GROUP)",)
test-behavior-review:
	$(PYTHON) -B tests/behavior/run_review.py --cli "$(CLI)" $(if $(CASE),--case "$(CASE)",) $(if $(BEHAVIOR_OUTPUT),--output-dir "$(BEHAVIOR_OUTPUT)",)
test-behavior-skills:
	$(PYTHON) -B tests/behavior/run_skills.py --cli "$(CLI)" $(if $(CASE),--case "$(CASE)",) $(if $(BEHAVIOR_OUTPUT),--output-dir "$(BEHAVIOR_OUTPUT)",)
inspect:
	$(PYTHON) skills/_shared/scripts/documentation.py inspect --source "$(SOURCE)"
scaffold:
	@test -n "$(OUTPUT)" || (echo "OUTPUT is required" >&2; exit 2)
	$(PYTHON) skills/_shared/scripts/documentation.py scaffold --source "$(SOURCE)" --output "$(OUTPUT)" $(if $(TITLE),--title "$(TITLE)",) $(if $(LANGUAGES),--languages $(LANGUAGES),) $(if $(DEFAULT_LANGUAGE),--default-language $(DEFAULT_LANGUAGE),)
validate-docs:
	@test -n "$(OUTPUT)" || (echo "OUTPUT is required" >&2; exit 2)
	$(PYTHON) skills/_shared/scripts/documentation.py validate --output "$(OUTPUT)"
build-skeleton-hashes:
	$(PYTHON) -B scripts/skeleton_hashes.py build
check-skeleton-hashes:
	$(PYTHON) -B scripts/skeleton_hashes.py check
