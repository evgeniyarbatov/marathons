VENV_PATH := .venv

PYTHON := $(VENV_PATH)/bin/python
PIP := $(VENV_PATH)/bin/pip
REQUIREMENTS := requirements.txt

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@$(PIP) install --disable-pip-version-check -q --upgrade pip
	@$(PIP) install --disable-pip-version-check -q -r $(REQUIREMENTS)

SHELL := /bin/bash

PYTHON = $(VENV_PATH)/bin/python
PIP = $(VENV_PATH)/bin/pip

KAGGLE_DATASET = evgenyarbatov/marathon-running-times

DATA_DIR = data
SITE_DIR = site
PUBLIC_DIR = $(SITE_DIR)/public
TERRAFORM_DIR = terraform

data:
	kaggle datasets download --force -d $(KAGGLE_DATASET) -p $(DATA_DIR)
	find $(DATA_DIR) -name "*.zip" | xargs -I {} unzip -o {} -d $(DATA_DIR)

metadata: install
	@$(PYTHON) scripts/metadata.py $(DATA_DIR)/marathon.csv $(PUBLIC_DIR)/marathons.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/latest_times.json

links: install
	@$(PYTHON) scripts/links.py $(PUBLIC_DIR)/latest_times.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/links.json 

update-timestamp:
	./scripts/update_timestamp.sh

site-build:
	cd $(SITE_DIR) && rm -rf node_modules && npm ci && npm run build

deploy:
	cd $(TERRAFORM_DIR) && terraform init -reconfigure -input=false && \
	terraform apply -auto-approve

.PHONY: venv install data metadata links update-timestamp site-build deploy 

cleanvenv:
	@rm -rf .venv
