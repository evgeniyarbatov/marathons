VENV_PATH := .venv
PYTHON := $(VENV_PATH)/bin/python
PIP := $(VENV_PATH)/bin/pip
REQUIREMENTS := requirements.txt

SCRIPTS_DIR = scripts
PYTHON_FILES := $(shell find $(SCRIPTS_DIR) -name "*.py")

KAGGLE_DATASET = evgenyarbatov/marathon-running-times

DATA_DIR = data
SITE_DIR = site
PUBLIC_DIR = $(SITE_DIR)/public
TERRAFORM_DIR = terraform

default: deploy

venv:
	@uv venv $(VENV_PATH)

install: venv
	@uv pip install -q -r $(REQUIREMENTS)

data:
	kaggle datasets download --force -d $(KAGGLE_DATASET) -p $(DATA_DIR)
	find $(DATA_DIR) -name "*.zip" | xargs -I {} unzip -o {} -d $(DATA_DIR)

metadata: install
	@$(PYTHON) scripts/metadata.py $(DATA_DIR)/marathon.csv $(PUBLIC_DIR)/marathons.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/latest_times.json
links: install
	@$(PYTHON) scripts/links.py $(PUBLIC_DIR)/latest_times.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/links.json
update-timestamp:
	./scripts/update_timestamp.sh

run:
	cd $(SITE_DIR) && npm run dev

deploy:
	cd $(SITE_DIR) && npm run build
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve

.PHONY: data