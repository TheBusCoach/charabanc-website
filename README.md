# charabancfinancial.com

Static site for Charabanc Financial, hosted on Netlify.

## How it's built
- `build_site.py` writes `site/css/style.css`
- `build_pages.py` writes every page, plus `sitemap.xml`, `robots.txt`, and `_redirects`, into `site/`
- Never hand-edit files in `site/`. Change the build scripts and re-run them.

```
python build_site.py
python build_pages.py
```
(`build_pages.py` needs Pillow: `pip install pillow`)

## How it deploys
Netlify is linked to this repo and publishes the `site/` folder (see `netlify.toml`).
Push to `main` and the live site updates in about a minute. A pull request gets its own
Netlify preview link, so changes can be reviewed before they go live.

## Approvals
Content and pricing/terms changes are approved by Alex, Mike, or Steven before merging to `main`.
