# ROADMAP — marathons

Static site rendering marathon records (from the marathon-finish-times Kaggle dataset) with
Wikipedia links to each athlete, deployed to marathons.gritcuriosityandperseverance.org via
Terraform.

## Where it is

Data pipeline (data -> metadata -> links) feeds a Vite site with dark-mode support and Google-
friendly prerendering, deployed by `make deploy`.

## Near-term direction (from TODO.md, roughly in order)

1. Fix the Airflow pipeline that deploys this site — currently broken (same underlying pipeline as
   marathon-finish-times, which has the same open item).
2. Search bar for city/athlete.
3. Richer per-marathon content: YouTube videos of the race and of specific runners, GPX files per
   course, dates + weather per location, OSM-based course sightlines, future event dates.
