# ROADMAP — marathons

Static site rendering marathon records (from the marathon-finish-times Kaggle dataset) with
Wikipedia links to each athlete, deployed to GitHub Pages.

## Where it is

Data pipeline (data -> metadata -> links) feeds a Vite site with dark-mode support and Google-
friendly prerendering; a daily GitHub Actions job pulls Kaggle updates and redeploys.

## Near-term direction (from TODO.md, roughly in order)

1. Search bar for city/athlete.
2. Richer per-marathon content: YouTube videos of the race and of specific runners, GPX files per
   course, dates + weather per location, OSM-based course sightlines, future event dates.
