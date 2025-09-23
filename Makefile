SHELL := /bin/bash

PROJECT_NAME := $(shell basename $(PWD))
VENV_PATH = ~/.venv/$(PROJECT_NAME)

KAGGLE_DATASET = evgenyarbatov/marathon-running-times

DATA_DIR = data
SITE_DIR = site
PUBLIC_DIR = $(SITE_DIR)/public
TERRAFORM_DIR = terraform

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@source $(VENV_PATH)/bin/activate && \
	pip install --disable-pip-version-check -q -r requirements.txt

data:
	kaggle datasets download --force -d $(KAGGLE_DATASET) -p $(DATA_DIR)
	find $(DATA_DIR) -name "*.zip" | xargs -I {} unzip -o {} -d $(DATA_DIR)

metadata: install
	@source $(VENV_PATH)/bin/activate && \
	python3 scripts/metadata.py $(DATA_DIR)/marathon.csv $(PUBLIC_DIR)/marathons.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/latest_times.json

links: install
	python3 scripts/links.py $(PUBLIC_DIR)/latest_times.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/links.json 

deploy:
	./scripts/update_timestamp.sh
	cd $(SITE_DIR) && npm install --force && npm run build
	cd $(TERRAFORM_DIR) && terraform init -reconfigure -input=false && \
	terraform apply -auto-approve

.PHONY: venv install data metadata deploy