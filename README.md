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
aws cloudfront get-invalidation --id I22WU2PGASW8AX07JVW7GNORPP --distribution-id E2ABRC7WI48APW
```
