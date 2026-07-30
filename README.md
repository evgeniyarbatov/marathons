# Marathons

Static site to render marathon records with Wiki links to each athlete.

Data comes from Kaggle dataset of marathon records scraped from World Athletics.

Site - [https://marathons.gritcuriosityandperseverance.org](https://marathons.gritcuriosityandperseverance.org)

## How to run

```bash
make install    # uv sync deps
make data       # download and unzip Kaggle dataset
make metadata   # build marathons/best_times/latest_times JSON
make links      # build links.json (Wikipedia links per athlete)
make run        # site dev server (site/, npm run dev)
```

`make deploy` builds the site and applies the Terraform stack in `terraform/`
(publishes to the live site) — the default target when running plain `make`.
