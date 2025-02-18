# Marathons

Example of hosting static site on S3 with data from Python scripts.

### Pros

- Zero cost. Host on S3
- Build reasonably fast but struggle a bit with JS / Vue

### Cons

- A lot of data pre-processing
- Very time consuming for such lightweight project

### What can be better

- Write scripts instead of Jupyter notebooks?
- Cloudflare DNS is in the separate repo. How to keep it here?
- Time has to pass for me to see how it can be refactored. Delete a lot of code

### Todo

- LLM does not give correct Marathon dates. Fix that
- Add SEO tags and Google Analytics tracking to the page
- Reduce size. Country logos are too heavy.
- Add more marathons
- Add GPX file for each marathon