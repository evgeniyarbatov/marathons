# marathons

## What it does

Static site rendering world marathon records (from a Kaggle dataset scraped
from World Athletics), with Wikipedia links to each athlete. Deployed to
https://evgeniyarbatov.github.io/marathons/ via GitHub Pages.

## Key files / entry points

- `Makefile` — pipeline steps: `data` -> `metadata` -> `links` -> `build`.
- `scripts/metadata.py` — builds `site/public/{marathons,best_times,latest_times}.json` from the raw CSV.
- `scripts/links.py` — builds `site/public/links.json` (Wikipedia lookups per athlete).
- `site/` — Vue 3 + Vite frontend, prerendered at build time (`site/scripts/prerender.mjs`).
- `.github/workflows/refresh-data.yml` — daily Kaggle pull; commits changed JSON and calls `deploy.yml`.
- `.github/workflows/deploy.yml` — builds `site/` and publishes to GitHub Pages.
- `cache/` — committed Nominatim geocoding cache; keeps CI from re-geocoding every city.

## How to run

```bash
make install    # uv sync deps
make data       # download and unzip Kaggle dataset -> data/
make metadata   # regenerate the JSON files consumed by the site
make links      # regenerate links.json
make run        # site dev server (npm run dev)
make build      # build site into site/dist
```

## Conventions / gotchas

- Python deps via `uv` (`uv sync`, `uv run`); Node deps in `site/` via `npm`.
- `make data` requires `KAGGLE_API_TOKEN` (repo secret in CI) or `kaggle auth login` locally.
- Site is served under `/marathons/` (Vite `base`); fetch public files via `import.meta.env.BASE_URL`, not `/`.
- `site/public/*.json` and `cache/` are committed on purpose: `links.py` and geocoding only look up entries missing from them.
- Tests: `make test` (unittest, `tests/`).
