# Uses uv (https://docs.astral.sh/uv) for dependency management — uv sync creates/updates .venv; run commands via uv run, no manual activation.

SCRIPTS_DIR = scripts
PYTHON_FILES := $(shell find $(SCRIPTS_DIR) -name "*.py")

KAGGLE_DATASET = evgenyarbatov/marathon-running-times

DATA_DIR = data
SITE_DIR = site
PUBLIC_DIR = $(SITE_DIR)/public
TERRAFORM_DIR = terraform

default: deploy

install:
	@uv sync --dev

lock:
	@uv lock

data:
	kaggle datasets download --force -d $(KAGGLE_DATASET) -p $(DATA_DIR)
	find $(DATA_DIR) -name "*.zip" | xargs -I {} unzip -o {} -d $(DATA_DIR)

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

deploy:
	cd $(SITE_DIR) && npm run build
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve

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
	@echo "deploy            - build site and apply terraform"
	@echo "clean             - remove .venv"

.PHONY: data clean help
