VENV_PATH := .venv

PYTHON := $(VENV_PATH)/bin/python
BLACK := $(VENV_PATH)/bin/black
FLAKE8 := $(VENV_PATH)/bin/flake8
PIP := $(VENV_PATH)/bin/pip

REQUIREMENTS := requirements.txt

SCRIPTS_DIR = scripts
PYTHON_FILES := $(shell find $(SCRIPTS_DIR) -name "*.py")

KAGGLE_DATASET = evgenyarbatov/marathon-running-times

DATA_DIR = data
SITE_DIR = site
PUBLIC_DIR = $(SITE_DIR)/public
TERRAFORM_DIR = terraform

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@$(PIP) install --disable-pip-version-check -q --upgrade pip
	@$(PIP) install --disable-pip-version-check -q -r $(REQUIREMENTS)

format:
	@if [ -n "$(PYTHON_FILES)" ]; then \
		$(BLACK) $(PYTHON_FILES); \
	else \
		echo "No Python files"; \
	fi

lint: format
	@if [ -n "$(PYTHON_FILES)" ]; then \
		$(FLAKE8) $(PYTHON_FILES); \
	else \
		echo "No Python files"; \
	fi

data:
	kaggle datasets download --force -d $(KAGGLE_DATASET) -p $(DATA_DIR)
	find $(DATA_DIR) -name "*.zip" | xargs -I {} unzip -o {} -d $(DATA_DIR)

metadata:
	@$(PYTHON) scripts/metadata.py $(DATA_DIR)/marathon.csv $(PUBLIC_DIR)/marathons.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/latest_times.json

links:
	@$(PYTHON) scripts/links.py $(PUBLIC_DIR)/latest_times.json $(PUBLIC_DIR)/best_times.json $(PUBLIC_DIR)/links.json

update-timestamp:
	./scripts/update_timestamp.sh

run:
	cd $(SITE_DIR) && npm run dev

deploy:
	cd $(SITE_DIR) && npm run build
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve

cleanvenv:
	@rm -rf $(VENV_PATH)
