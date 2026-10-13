# Marathons

Best and latest winning times for marathons worldwide, with Wikipedia links to each athlete.

**Site:** https://evgeniyarbatov.github.io/marathons/

## How it works

1. [Kaggle dataset](https://www.kaggle.com/datasets/evgenyarbatov/marathon-running-times) of World Athletics marathon results.
2. `scripts/metadata.py` aggregates per-city stats, best and latest times; cities are geocoded via Nominatim.
3. `scripts/links.py` looks up each athlete on Wikipedia.
4. The Vue + Vite site in `site/` renders the resulting JSON.

The `refresh-data` GitHub Actions workflow runs this daily, commits any changed data and deploys to GitHub Pages.

## How to run

```bash
make install    # uv sync deps
make data       # download Kaggle dataset (needs KAGGLE_API_TOKEN or `kaggle auth login`)
make metadata   # build marathons/best_times/latest_times JSON
make links      # build links.json
make test       # unit tests
make run        # site dev server
make build      # build site into site/dist
```

## License

[MIT](LICENSE.md)
