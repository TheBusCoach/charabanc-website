# CLAUDE.md — charabancfinancial.com

Static marketing site for **Charabanc Financial** (motorcoach/bus and equipment financing, Lavonia, GA; since 2002). Charabanc is the financing affiliate of **The Bus Coach** (thebuscoach.com), which buys, sells and consigns buses. Charabanc *brokers* deals to third-party lenders.

Owner / approver: Alex Kenney (alexkenney@charabancfinancial.com). Mike and Steven can also approve.

## Repo layout
- `build_site.py` → writes `site/css/style.css` (all CSS lives in one Python string).
- `build_pages.py` → writes every page plus `sitemap.xml`, `robots.txt`, `_redirects` into `site/`; also regenerates favicons from `assets/logo_transparent.png` (needs Pillow).
- `site/` → the published output. **Never hand-edit it**; change the scripts and rebuild. Built output IS committed (Netlify has no build step).
- `netlify.toml` → publish `site/`, no build command.
- `publish.bat` → Windows one-click: rebuild, `git add -A`, commit, push.
- `source-assets/` → original full-size headshots, logo variants, original Wix PDFs. Not published; keep for re-cropping/re-exporting.

## Build & deploy
```
python build_site.py
python build_pages.py
```
Netlify is linked to this repo: **anything that lands on `main` is live in ~1 minute.** Every pull request gets a Netlify Deploy Preview link.

**Approval = Alex (or Mike/Steven) merging the pull request.** Never push content changes straight to `main`.

Workflow for every change (scheduled or interactive):
1. `git checkout main && git pull`, then `git checkout -b seo/YYYY-MM-DD-short-topic`.
2. Edit the build scripts, rebuild, validate (below).
3. `git add -A && git commit -m "..."` then `git push -u origin <branch>`.
4. `gh pr create --base main --title "..." --body "..."`. The body lists every visible change in plain English, flags anything that needs a fact check, and points to the Netlify Deploy Preview.
5. Stop. Alex reviews the preview and clicks **Merge** on GitHub, which deploys it. Afterwards `git checkout main && git pull`.
- If Alex approves in a live chat ("ship it"), you may run `gh pr merge <n> --squash --delete-branch`.
- If a previous weekly PR is still unmerged, add to that branch instead of opening a second PR.

Before committing, validate: every JSON-LD block parses, no broken internal `.html` links, exactly one `<h1>` per page, titles ≲ 60 chars (page() appends " | Charabanc Financial"). Screenshot new/changed pages at desktop and ~390px widths.

## Ground rules (important)
- **Every content or site change needs Alex's (or Mike's/Steven's) approval before it reaches `main`.** The PR's Netlify Deploy Preview is the preview.
- Finance company: never invent rates, terms, approval stats, lender claims, or client names. Only use facts already on the site or confirmed by Alex. Avoid "we fund" wording (they broker).
- Correct NAP: 65 Ayers St., Lavonia, GA 30553 · 706-460-5231 · fax 706-460-5232 · info@charabancfinancial.com. Google Business Profile and several directories still show an old Cumming, GA address; the site is right.
- Font sizes are deliberately large (older audience; Mike asked). Use the `--fs-*` scale, don't shrink.
- Internal links use `page.html`; canonical URLs are extensionless and `_redirects` 301s `.html` → clean URL.

## Code conventions / gotchas
- `page(title, description, active, body, extra_head="")` builds every page; `write()` injects canonical + OG/Twitter tags. Bare `&` in titles/descriptions is auto-escaped.
- `industry_page(...)` accepts `seo_title`, `seo_desc`, `extra_html`.
- The CSS in `build_site.py` is a **non-raw** Python string: CSS escapes need double backslashes (`content:"\\2713"`), or Python turns them into garbage.
- New pages must be added to `NAV` (if in menu) and `SITEMAP_PAGES`.
- Landing-page building blocks (in `build_pages.py`, styled in `build_site.py`): `lp_hero()`, `stat_strip()`, `section()`, `reasons()`, `finance_tiles()`, `steps()`, `faq_block()` (accordion + FAQPage JSON-LD), `breadcrumb_ld()`, `cta_band()`; CSS classes `.lp-hero .stat-strip .reason-grid .finance-grid .compare .steps .callout .faq .cta-band`. Reuse these for any new keyword landing page — see `motorcoach-financing.html` / `church-bus-financing.html`.
- Structured data: sitewide `FinancialService` (ORG_SCHEMA); landing pages add `FAQPage` + `BreadcrumbList`.
- GA4 measurement ID: `G-EPCRL21KWQ`. Contact form is a Netlify form (`data-netlify`, honeypot) → `thank-you.html`.

## SEO status (as of 2026-09-28)
Done: canonical/OG tags, schema, clean-URL + old-Wix redirects, sitemap/robots, GA4; keyword titles & meta descriptions on all pages; keyword H1 on home; new `/motorcoach-financing` and `/church-bus-financing` landing pages.

Backlog (priority order):
1. Check Search Console: sitemap status (showed "Couldn't fetch" on 9/28 submit, normal for a new property; resubmit if still failing) and whether both landing pages are indexed. (Deploy, sitemap submit and indexing requests were done 2026-09-28.)
2. Pull a Search Console / GA4 baseline (Search Console verified 2026-09-28, so data starts then).
3. Fix Google Business Profile (Cumming → Lavonia), then directory citation cleanup.
4. More landing pages: used bus financing; TRAC lease vs. loan; shuttle/cutaway bus financing; start-up charter company financing; school bus financing; motorcoach refinancing.
5. Expand thin industry pages (~100 words each) with real detail from Alex/Frank.
6. Footer "Equipment Inventory" link points to Resources — decide: link to thebuscoach.com or remove.
7. Once The Bus Coach site is rebuilt (target Jan 2027), have listings link to Charabanc financing pages.

A weekly scheduled SEO task ("Weekly Charabanc SEO", Mondays 8:54 AM ET) opens a pull request (workflow above) and logs to the Claude project doc `claude/charabanc_seo_log.md` (project "The Bus Coach: Data and Information"). Keep that log in sync when you ship something.
