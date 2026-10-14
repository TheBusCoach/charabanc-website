# Charabanc Financial — SEO Log

## 2026-10-14 — New landing page: Shuttle & Cutaway Bus Financing

**What changed:** Added `/shuttle-cutaway-bus-financing` using the existing landing-page
building blocks (`lp_hero`, `stat_strip`, `reasons`, `finance_tiles`, `steps`, `faq_block`,
`cta_band`), targeting "shuttle bus financing" / "cutaway bus financing" searches from
operators running daily routes (hotel/resort, senior living, daycare/camp, airport/corporate,
paratransit) rather than seasonal charter/tour work. Added to the Industries nav dropdown,
the home/Industries "Specialized Bus Financing" card grid, the Transportation page's
cross-link paragraph, `sitemap.xml`, and `_redirects`. FAQPage + BreadcrumbList JSON-LD
included, consistent with the other bus landing pages.

**Why:** Backlog item #4 (more landing pages) — this was the next bus-financing vertical
not yet covered (motorcoach, church, used-bus, and start-up-charter pages already existed).

**All claims reused from existing site copy:** 100% financing available, 90-day deferred
payment options, seasonal payment skips, A+ to C credit window, start-up underwriting,
$750K application-only approvals, new/used vehicles, TRAC-vs-loan comparison (linked to
the motorcoach page), and The Bus Coach affiliate callout. No new rates, terms, approval
stats, lender claims, or client names were introduced.

**Needs Alex (flagged on the PR):** the buyer-segment list (hotel/resort, senior living,
daycare/camp, airport/corporate, paratransit) is new wording for the site — please confirm
these are segments Charabanc actually wants to target before merge.

**Validated:** JSON-LD parses, single `<h1>`, no broken internal links, title ~53 chars
with suffix, screenshots taken at desktop and ~390px widths.

**What's next:** Remaining backlog landing pages — TRAC lease vs. loan (dedicated page;
currently only a comparison block on the motorcoach page), school bus financing, motorcoach
refinancing. Items still blocked on Alex/Mike/Steven or external access: Search Console
baseline pull, Google Business Profile address fix + directory cleanup, expanding the thin
industry pages, and the footer "Equipment Inventory" link decision.
