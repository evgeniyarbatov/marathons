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

run:
	cd $(SITE_DIR) && npm run dev

build:
	cd $(SITE_DIR) && npm ci && npm run build

help:
	@echo "install   - uv sync deps into .venv"
	@echo "lock      - refresh uv.lock"
	@echo "data      - download and unzip Kaggle dataset"
	@echo "metadata  - build marathons/best_times/latest_times JSON"
	@echo "links     - build links.json"
	@echo "test      - run unit tests"
	@echo "run       - run site dev server"
	@echo "build     - build site into site/dist"

.PHONY: install lock data metadata links test run build help
