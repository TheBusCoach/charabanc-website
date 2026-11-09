# Charabanc Financial — SEO Log

## 2026-10-26 — New landing page: TRAC Lease vs. Loan

**What changed:** Added `/trac-lease-vs-loan` using the existing landing-page building
blocks (`lp_hero`, `stat_strip`, `reasons`, the `.compare` block, `finance_tiles`, `steps`,
`faq_block`, `cta_band`), targeting "TRAC lease vs loan" / "equipment loan vs TRAC lease"
searches. It lays out the loan-vs-TRAC-lease comparison that previously only lived as a
small block on the motorcoach page, plus a mention of municipal leases for public fleets.
Added to the Industries nav dropdown, a new "Loan or TRAC Lease?" cross-link section on
the Transportation page, `sitemap.xml`, and `_redirects`. FAQPage + BreadcrumbList JSON-LD
included, consistent with the other landing pages.

**Why:** Backlog item #4 (more landing pages) — the last of the originally-listed pages
other than motorcoach refinancing (used bus, shuttle/cutaway, start-up charter, and school
bus financing all shipped in prior weeks). The "Loan or TRAC lease: which is better for a
[coach/shuttle/bus/truck]?" FAQ on the start-up charter, shuttle/cutaway, school bus, and
tow truck pages previously linked to the motorcoach page's comparison block; those four
links now point to this dedicated page instead, since it's the canonical resource.

**All claims reused from existing site copy:** the equipment-loan vs. TRAC-lease
descriptions (ownership/equity vs. residual value and lower payment) are taken verbatim
from the existing `.compare` block on `motorcoach-financing.html`; municipal, capital, and
operating lease mentions reuse language already on the transportation and
commercial-financing pages; A+ to C credit, start-up underwriting, and the $750K
application-only path reuse the site-wide `APPLY_STEPS`/`BUS_STATS` copy. No new rates,
terms, approval stats, lender claims, or client names were introduced.

**Needs Alex:** none — this page only restates financing-structure facts already live
elsewhere on the site. Nothing here needs a fact check beyond the usual read-through.

**Validated:** JSON-LD parses on every page, exactly one `<h1>` per page, no broken
internal `.html` links (checked site-wide), new page's title is 41 characters with the
" | Charabanc Financial" suffix. Screenshotted at desktop (1440px) and mobile (390px)
widths — layout matches the other landing pages, large font scale preserved. (Separately,
and out of scope for this PR: `motorcoach-financing.html`'s existing title tag is 68
characters, over the ~60-char guideline — pre-existing, not introduced by this change,
flagged here for a future cleanup pass.)

**What's next:** The one remaining backlog landing page is motorcoach refinancing — worth
checking first whether a standalone page is still useful now that "Refinancing" already
appears as a `finance_tiles` entry on the motorcoach, used-bus, shuttle/cutaway, school
bus, and tow truck pages. Items still blocked on Alex/Mike/Steven or external access:
Search Console baseline pull, Google Business Profile address fix + directory cleanup,
expanding the thin industry pages, and the footer "Equipment Inventory" link decision.

## 2026-10-19 — New landing page: School Bus Financing

**What changed:** Added `/school-bus-financing` using the existing landing-page
building blocks (`lp_hero`, `stat_strip`, `reasons`, `finance_tiles`, `steps`, `faq_block`,
`cta_band`), targeting "school bus financing" searches from private schools, daycares,
Head Start programs, and student transportation contractors &mdash; explicitly not public
school district fleets, since the site has no claims or application process built for
district procurement. Added to the Industries nav dropdown, the home/Industries
"Specialized Bus Financing" card grid, the Transportation page's cross-link paragraph,
`sitemap.xml`, and `_redirects`. FAQPage + BreadcrumbList JSON-LD included, consistent
with the other bus landing pages.

**Why:** Backlog item #4 (more landing pages) &mdash; of the remaining pages listed
(TRAC lease vs. loan, school bus financing, motorcoach refinancing), this was the
clearest fit for the existing keyword-landing-page template: a distinct buyer segment
with real site content to draw on (school buses are already named as financeable
equipment on the Transportation and Used Bus Financing pages).

**All claims reused from existing site copy:** 100% financing available, 90-day deferred
payment options, A+ to C credit window, start-up underwriting, $750K application-only
approvals, new/used vehicles, TRAC-vs-loan comparison (linked to the motorcoach page),
and The Bus Coach affiliate callout. No new rates, terms, approval stats, lender claims,
or client names were introduced.

**Needs Alex (flagged on the PR):** the buyer-segment list (private/parochial schools,
daycare/Head Start, special-needs/paratransit contractors, student transportation
contractors) is new wording for the site &mdash; please confirm these are segments
Charabanc actually wants to target, and confirm it's correct to exclude public school
district fleets from this page.

**Validated:** JSON-LD parses, single `<h1>`, no broken internal links, title 52 chars
with suffix, screenshots taken at desktop and ~390px widths.

**What's next:** Remaining backlog landing pages &mdash; TRAC lease vs. loan (dedicated
page; currently only a comparison block on the motorcoach page) and motorcoach
refinancing. Items still blocked on Alex/Mike/Steven or external access: Search Console
baseline pull, Google Business Profile address fix + directory cleanup, expanding the
thin industry pages, and the footer "Equipment Inventory" link decision.

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

## 2026-10-19 (follow-up)
- School bus page now includes public school districts (Alex confirmed Charabanc finances districts). District wording reuses the existing municipal-lease copy; title changed from "Private School Bus Financing" to "School Bus Financing".

## 2026-10-20 (follow-up)
- Frank: "school-style buses" changed to "school buses" everywhere; italics removed from heading accents site-wide (green color kept).

## 2026-10-22 (interactive, Alex)
- New `/tow-truck-financing` landing page for Charabanc's tow truck finance expansion. Added to the Industries nav, sitemap, and a short link section on the Transportation page.
- Facts from Alex: any truck size; trucks generally under 10 years old. Everything else reuses the site-wide industry features and APPLY_STEPS. Truck-type tiles (wreckers, rollbacks, rotators, integrated) are standard categories, flagged for review.
- Validated: JSON-LD parses, single `<h1>`, no broken internal links. Screenshots not taken (Playwright not installed locally); check the Deploy Preview at desktop and phone width.
