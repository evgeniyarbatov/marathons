# Uses uv (https://docs.astral.sh/uv) for dependency management — uv sync creates/updates .venv; run commands via uv run, no manual activation.

SCRIPTS_DIR = scripts
PYTHON_FILES := $(shell find $(SCRIPTS_DIR) -name "*.py")

KAGGLE_DATASET = evgenyarbatov/marathon-running-times

DATA_DIR = data
SITE_DIR = site
PUBLIC_DIR = $(SITE_DIR)/public

install:
	@uv sync --dev

lock:
	@uv lock

data: install
	@uv run kaggle datasets download --force --unzip -p $(DATA_DIR) $(KAGGLE_DATASET)

metadata: install
	@uv run python scripts/metadata.py $(DATA_DIR)/marathon.csv $(PUBLIC_DIR)/marathons.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/latest_times.json

links: install
	@uv run python scripts/links.py $(PUBLIC_DIR)/latest_times.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/links.json

test: install
	@uv run python -m unittest discover -s tests -p 'test_*.py' -v

update-timestamp:
	./scripts/update_timestamp.sh

run:
	cd $(SITE_DIR) && npm run dev

build:
	cd $(SITE_DIR) && npm ci && npm run build

clean:
	rm -rf .venv

help:
	@echo "install           - uv sync deps into .venv"
	@echo "lock              - refresh uv.lock"
	@echo "data              - download and unzip Kaggle dataset"
	@echo "metadata          - build marathons/best_times/latest_times JSON"
	@echo "links             - build links.json"
	@echo "test              - run unit tests"
	@echo "update-timestamp  - update site timestamp"
	@echo "run               - run site dev server"
	@echo "build             - build site into site/dist"
	@echo "clean             - remove .venv"

.PHONY: data build clean help
