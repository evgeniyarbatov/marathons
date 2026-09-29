# Marathons

Static site to render marathon records with Wiki links to each athlete.

Data comes from Kaggle dataset of marathon records scraped from World Athletics.

Site - [https://evgeniyarbatov.github.io/marathons/](https://evgeniyarbatov.github.io/marathons/)

## How to run

```bash
make install    # uv sync deps
make data       # download and unzip Kaggle dataset
make metadata   # build marathons/best_times/latest_times JSON
make links      # build links.json (Wikipedia links per athlete)
make run        # site dev server (site/, npm run dev)
make build      # build site into site/dist
```

`make data` needs `KAGGLE_API_TOKEN` (or `kaggle auth login`).

The `refresh-data` workflow runs this pipeline daily, commits any changed JSON and
deploys to GitHub Pages.
