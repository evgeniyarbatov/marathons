PROJECT_NAME := $(shell basename $(PWD))
VENV_PATH = ~/.venv/$(PROJECT_NAME)

KAGGLE = ~/Library/Python/3.12/bin/kaggle
KAGGLE_DATASET = evgenyarbatov/marathon-running-times

DATA_DIR = data

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@source $(VENV_PATH)/bin/activate && \
	pip install --disable-pip-version-check -q -r requirements.txt

data:
	$(KAGGLE) datasets download -d $(KAGGLE_DATASET) -p $(DATA_DIR)
	find $(DATA_DIR) -name "*.zip" | xargs -I {} unzip -o {} -d $(DATA_DIR)

.PHONY: data venv install