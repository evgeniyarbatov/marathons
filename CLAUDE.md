# marathons

## What it does

Static site rendering world marathon records (from a Kaggle dataset scraped
from World Athletics), with Wikipedia links to each athlete. Deployed to
https://marathons.gritcuriosityandperseverance.org via S3 + Terraform.

## Key files / entry points

- `Makefile` — pipeline steps: `data` -> `metadata` -> `links` -> site build/deploy.
- `scripts/metadata.py` — builds `site/public/{marathons,best_times,latest_times}.json` from the raw CSV.
- `scripts/links.py` — builds `site/public/links.json` (Wikipedia lookups per athlete).
- `site/` — Vue 3 + Vite frontend, prerendered at build time (`site/scripts/prerender.mjs`).
- `terraform/` — S3 bucket + policy for static hosting.

## How to run

```bash
make install    # uv sync deps
make data       # download and unzip Kaggle dataset -> data/
make metadata   # regenerate the JSON files consumed by the site
make links      # regenerate links.json
make run        # site dev server (npm run dev)
make deploy     # build site + terraform apply (publishes live)
```

## Conventions / gotchas

- Python deps via `uv` (`uv sync`, `uv run`); Node deps in `site/` via `npm`.
- `make data` requires Kaggle CLI credentials configured (`kaggle datasets download`).
- `make deploy` runs `terraform apply -auto-approve` — it publishes to production, don't run casually.
- Tests: `make test` (unittest, `tests/`).
