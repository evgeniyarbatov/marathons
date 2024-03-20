# Visualize Marathon Running Records

Making marathon running times accessible as a web page to follow the current state of world records.

[arbatov.me/marathons](arbatov.me/marathons/index.html)

## Structure

- `notebooks` contain Jupyter notebooks to parse the CSV into suitable JSON format to `public` folder
- `src` is the VueJS source for the website
- `terraform` are the terraform script to deploy website to S3 bucket with Github actions

## Data 

The data comes from [this Kaggle dataset](https://www.kaggle.com/datasets/evgenyarbatov/running-times).

## Dev

```
npm run dev
```

## Todos

- download `data` directly from Kaggle to get latest dataset version
- merge files in `public` folder to reduce size and duplicates
