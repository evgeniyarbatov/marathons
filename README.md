# Visualize World Marathon Majors

UI to render info about World Marathon Majors.

## Running

```
npm run dev
npm run format
npm run build
```

## Invalidate cache

```
aws cloudfront create-invalidation --distribution-id E2ABRC7WI48APW --paths "/marathons/index.html"
aws cloudfront get-invalidation --id IB45G8GHV4QZAOI8CF9GM1GEMT --distribution-id E2ABRC7WI48APW
```
