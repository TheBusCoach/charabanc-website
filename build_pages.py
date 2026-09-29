# -*- coding: utf-8 -*-
"""Generates every page of the Charabanc Financial site from shared
header/footer + per-page content. Run build_site.py first (writes css/style.css)."""
import os
import re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "site")  # relative, so the build runs anywhere (laptop, GitHub, Netlify)
ASSETS_SRC = os.path.join(HERE, "assets")

def build_favicon():
    """Crops the wheel icon out of the full logo (bbox found once via alpha-channel
    column-gap detection: wheel spans x 180-1021 of the 6001x1200 source, with a
    60+ column transparent gap before the CHARABANC wordmark starts) and writes
    favicon.ico + PNG sizes into site/. Re-run whenever the source logo changes."""
    src = Image.open(os.path.join(ASSETS_SRC, "logo_transparent.png")).convert("RGBA")
    pad = 15
    x0, y0, x1, y1 = 180 - pad, 180 - pad, 1021 + pad, 1020 + pad
    wheel = src.crop((x0, y0, x1, y1))
    wheel.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    for s in (32, 180):
        wheel.resize((s, s), Image.LANCZOS).save(os.path.join(ROOT, f"favicon-{s}.png"))
    print("wrote favicon.ico, favicon-32.png, favicon-180.png")

build_favicon()

# Google Analytics 4 Measurement ID (e.g. "G-XXXXXXXXXX"). Leave blank until
# Alex creates the GA4 property at analytics.google.com and provides the ID --
# the snippet below is simply omitted from every page while this is empty.
GA_MEASUREMENT_ID = "G-EPCRL21KWQ"

# Moved up from near build_sitemap() — write() needs this at every call, and
# write() is called starting well before the old definition point.
SITE_URL = "https://charabancfinancial.com"

def canonical_url(fname: str) -> str:
    """index.html -> SITE_URL + '/' ; everything else -> SITE_URL + '/slug' (no .html)."""
    slug = fname[:-5] if fname.endswith(".html") else fname
    return f"{SITE_URL}/" if slug == "index" else f"{SITE_URL}/{slug}"

NAV = [
    ("Home", "index.html", None),
    ("About", "about.html", [
        ("About & Team", "about.html"),
        ("Testimonials", "testimonials.html"),
    ]),
    ("Industries", "industries.html", [
        ("All Industries", "industries.html"),
        ("Transportation", "transportation.html"),
        ("Motorcoach Financing", "motorcoach-financing.html"),
        ("Church Bus Financing", "church-bus-financing.html"),
        ("Construction / Forestry", "construction-forestry.html"),
        ("Manufacturing / Printing", "manufacturing-printing.html"),
        ("Audio / Video", "audio-video.html"),
        ("Professional Firms", "professional-firms.html"),
        ("Capital Markets", "capital-markets.html"),
    ]),
    ("Services", "services.html", [
        ("All Services", "services.html"),
        ("Commercial Financing", "commercial-financing.html"),
        ("Corporate Services", "corporate-services.html"),
    ]),
    ("Resources", "resources.html", None),
]

def header_html(active):
    items = []
    for label, href, dropdown in NAV:
        cls = ""
        if dropdown:
            panel = "".join(f'<a href="{h}">{l}</a>' for l, h in dropdown)
            items.append(
                f'<div class="has-dropdown" tabindex="0"><a href="{href}">{label}</a>'
                f'<div class="dropdown-panel">{panel}</div></div>'
            )
        else:
            items.append(f'<a href="{href}">{label}</a>')
    nav_links = "\n      ".join(items)
    return f"""<header>
  <div class="header-row wrap">
    <a href="index.html" class="logo-wrap" style="text-decoration:none;">
      <img class="logo-img" src="assets/logo.png" alt="Charabanc Financial">
    </a>
    <input type="checkbox" id="nav-toggle" class="nav-toggle-checkbox">
    <label for="nav-toggle" class="nav-toggle-label">&#9776;</label>
    <nav class="main-nav">
      {nav_links}
      <a href="contact.html" class="nav-cta">Contact Us</a>
    </nav>
  </div>
</header>"""

FOOTER = """<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="assets/logo-white.png" alt="Charabanc Financial">
        <p style="max-width:280px; color:#999999;">Equipment and corporate finance, structured around your business. Lavonia, Georgia.</p>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About &amp; Team</a></li>
          <li><a href="testimonials.html">Testimonials</a></li>
          <li><a href="industries.html">Industries</a></li>
          <li><a href="services.html">Services</a></li>
        </ul>
      </div>
      <div>
        <h4>Resources</h4>
        <ul>
          <li><a href="resources.html">Credit Applications</a></li>
          <li><a href="resources.html">Personal Financial Statement</a></li>
          <li><a href="resources.html">Equipment Inventory</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li>65 Ayers St., Lavonia, GA 30553</li>
          <li>Phone: <a href="tel:7064605231">706-460-5231</a></li>
          <li>Fax: 706-460-5232</li>
          <li><a href="mailto:info@charabancfinancial.com">info@charabancfinancial.com</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Charabanc Financial. All rights reserved.</span>
      <span>65 Ayers St., Lavonia, GA 30553</span>
    </div>
  </div>
</footer>"""

def _ga_snippet():
    if not GA_MEASUREMENT_ID:
        return ""
    return f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}');
</script>
"""

# Organization/FinancialService structured data — one shared block, every page.
# NAP confirmed correct by Alex 2026-08-11: 65 Ayers St., Lavonia, GA 30553 /
# 706-460-5231. This is the site's real address; it's Google Business Profile
# and 7+ third-party directories that have stale data (a Cumming, GA address
# from a former office), not this site — see project_charabanc_website.md.
ORG_SCHEMA = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FinancialService",
  "name": "Charabanc Financial",
  "url": "{SITE_URL}/",
  "logo": "{SITE_URL}/assets/logo.png",
  "image": "{SITE_URL}/assets/logo.png",
  "telephone": "+1-706-460-5231",
  "faxNumber": "+1-706-460-5232",
  "email": "info@charabancfinancial.com",
  "foundingDate": "2002",
  "areaServed": {{ "@type": "Country", "name": "United States" }},
  "knowsAbout": ["Motorcoach financing", "Bus financing", "Equipment financing", "TRAC leases", "Municipal leases", "Vendor financing", "Business valuation", "Mergers and acquisitions", "Loan syndication"],
  "description": "Motorcoach, bus, and equipment financing since 2002 \\u2014 loans, TRAC and municipal leases, vendor finance programs, and corporate advisory services.",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "65 Ayers St.",
    "addressLocality": "Lavonia",
    "addressRegion": "GA",
    "postalCode": "30553",
    "addressCountry": "US"
  }}
}}
</script>
"""

def page(title, description, active, body, extra_head=""):
    # escape bare ampersands (e.g. "M&A") so titles/descriptions are valid HTML
    title = re.sub(r"&(?![a-zA-Z]+;|#)", "&amp;", title)
    description = re.sub(r"&(?![a-zA-Z]+;|#)", "&amp;", description)
    full_title = f"{title} | Charabanc Financial"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="favicon-32.png" sizes="32x32">
<link rel="icon" type="image/png" href="favicon-180.png" sizes="180x180">
<link rel="apple-touch-icon" href="favicon-180.png">
<link rel="stylesheet" href="css/style.css">
{ORG_SCHEMA}{_ga_snippet()}{extra_head}</head>
<body>
{header_html(active)}
{body}
{FOOTER}
</body>
</html>
"""

def page_header(eyebrow, h1, lede, breadcrumb=None, narrow=False):
    bc = f'<div class="breadcrumb wrap">{breadcrumb}</div>' if breadcrumb else ""
    cls = "page-header narrow" if narrow else "page-header"
    return f"""{bc}
<div class="{cls}">
  <div class="wrap">
    <div class="eyebrow sans">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</div>"""

def write(fname, html):
    if "</head>" in html:
        url = canonical_url(fname)

        # Self-referencing canonical — declares the extensionless URL as
        # authoritative even though Netlify also serves the .html path (both
        # return 200 with no rel=canonical was the actual bug: Google had
        # nothing telling it which URL to index, and the sitemap it was
        # reading disagreed with what the nav actually links to).
        tags = f'<link rel="canonical" href="{url}">\n'

        # Open Graph / Twitter Card — pulled from the <title>/<meta description>
        # already rendered into this page rather than threaded as new params
        # through every page() call site. No OG/Twitter tags existed before,
        # so shares (LinkedIn, Slack, email previews) showed no title, no
        # description, no image at all.
        title_m = re.search(r"<title>(.*?)</title>", html, re.S)
        desc_m = re.search(r'name="description" content="(.*?)"', html, re.S)
        og_title = title_m.group(1) if title_m else "Charabanc Financial"
        og_desc = desc_m.group(1) if desc_m else ""
        og_image = f"{SITE_URL}/assets/logo.png"
        tags += f"""<meta property="og:type" content="website">
<meta property="og:site_name" content="Charabanc Financial">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="{og_image}">
"""
        html = html.replace("</head>", tags + "</head>", 1)
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname, len(html), "bytes")

CONTACT_INFO_BLOCK = """<h2 class="sans">Get in Touch</h2>
      <ul>
        <li>65 Ayers St., Lavonia, GA 30553</li>
        <li>Phone: <a href="tel:7064605231">706-460-5231</a></li>
        <li>Fax: 706-460-5232</li>
        <li><a href="mailto:info@charabancfinancial.com">info@charabancfinancial.com</a></li>
      </ul>"""

INDUSTRY_GRID = """<div class="industry-grid">
      <a class="industry-tile" href="transportation.html"><span class="num">01</span><span class="name">Transportation</span><span class="cap">App-only to $750K &middot; more with financials</span></a>
      <a class="industry-tile" href="construction-forestry.html"><span class="num">02</span><span class="name">Construction / Forestry</span><span class="cap">Up to $250,000</span></a>
      <a class="industry-tile" href="manufacturing-printing.html"><span class="num">03</span><span class="name">Manufacturing / Printing</span><span class="cap">Up to $250,000</span></a>
      <a class="industry-tile" href="audio-video.html"><span class="num">04</span><span class="name">Audio / Video</span><span class="cap">Up to $250,000</span></a>
      <a class="industry-tile" href="professional-firms.html"><span class="num">05</span><span class="name">Professional Firms</span><span class="cap">Custom Solutions</span></a>
      <a class="industry-tile" href="capital-markets.html"><span class="num">06</span><span class="name">Capital Markets</span><span class="cap">Syndicated Deals</span></a>
    </div>"""

# ============================================================ HOME
home_body = """<section class="hero-carousel">
  <div class="hero-slide">
    <div class="wrap">
      <h1 class="eyebrow sans">Motorcoach &amp; Equipment Financing Since 2002</h1>
      <h2 class="hero-title">Competitive. Creative. <span class="accent">Comprehensive.</span></h2>
      <p class="hero-sub">We know your business. Charabanc structures loans, leases, and vendor finance programs for operators, manufacturers, and professional firms across the country.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="contact.html">Contact Us</a>
        <a class="btn btn-ghost" href="industries.html">See Industries We Serve</a>
      </div>
    </div>
  </div>
  <div class="hero-slide">
    <div class="wrap">
      <div class="eyebrow sans">Commercial Financing</div>
      <h2 class="hero-title">Financing Built <span class="accent">Around the Deal.</span></h2>
      <p class="hero-sub">From application-only financing under $150,000 to complex transactions with public companies and municipalities &mdash; equipment loans, vendor programs, and TRAC &amp; municipal leases.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="commercial-financing.html">Explore Commercial Financing</a>
        <a class="btn btn-ghost" href="contact.html">Contact Us</a>
      </div>
    </div>
  </div>
  <div class="hero-slide">
    <div class="wrap">
      <div class="eyebrow sans">Corporate Services</div>
      <h2 class="hero-title">Beyond Financing. <span class="accent">Real Advisory.</span></h2>
      <p class="hero-sub">Business valuation, financial and operational analysis, and hands-on support for mergers and acquisitions &mdash; Charabanc helps you grow with more than capital.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="corporate-services.html">Explore Corporate Services</a>
        <a class="btn btn-ghost" href="contact.html">Contact Us</a>
      </div>
    </div>
  </div>
  <div class="hero-slide">
    <div class="wrap">
      <div class="eyebrow sans">Capital Markets</div>
      <h2 class="hero-title">Syndicated Deals. <span class="accent">Serious Scale.</span></h2>
      <p class="hero-sub">As administrative agent for syndicated loan transactions, Charabanc structures revolvers, term loans, and acquisition financing across small, medium, and large ticket markets.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="capital-markets.html">See Capital Markets</a>
        <a class="btn btn-ghost" href="contact.html">Contact Us</a>
      </div>
    </div>
  </div>
  <div class="hero-slide">
    <div class="wrap">
      <div class="eyebrow sans">Twenty Years of Specialization</div>
      <h2 class="hero-title">Six Industries. <span class="accent">One Partner.</span></h2>
      <p class="hero-sub">From transportation to capital markets, Charabanc brings deep sector expertise to every deal &mdash; with application-only approvals up to $750,000 and much larger deals with full financials.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="industries.html">See Industries We Serve</a>
        <a class="btn btn-ghost" href="contact.html">Contact Us</a>
      </div>
    </div>
  </div>
  <div class="hero-dots" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></div>
</section>

<div class="pillars wrap">
  <div class="pillar">
    <div class="pillar-word">Competitive</div>
    <div class="pillar-desc sans">Pricing structured to match the deal, not a rate card.</div>
  </div>
  <div class="pillar">
    <div class="pillar-word">Creative</div>
    <div class="pillar-desc sans">Twenty years of structuring complex, non-standard transactions.</div>
  </div>
  <div class="pillar">
    <div class="pillar-word">Comprehensive</div>
    <div class="pillar-desc sans">From application-only financing to syndicated capital markets deals.</div>
  </div>
</div>

<section class="block">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">What We Do</div>
      <h2 class="section-title">Services</h2>
      <p class="section-desc">CHARABANC's success is based on its industry specialization and a strong commitment to our customers.</p>
    </div>
    <div class="service-grid">
      <div class="service-card">
        <h3>Commercial Financing</h3>
        <p>From application-only deals under $150,000 to complex transactions with large public companies and municipalities.</p>
        <ul>
          <li>Equipment Financing</li>
          <li>Vendor Financing (floorplan &amp; retail)</li>
          <li>Loans, Capitalized &amp; Operating Leases</li>
          <li>TRAC &amp; Municipal Leases</li>
        </ul>
      </div>
      <div class="service-card">
        <h3>Corporate Services</h3>
        <p>Value-driven financial and operational analysis to help your business grow.</p>
        <ul>
          <li>Financial &amp; Operational Analysis</li>
          <li>Business Valuation</li>
          <li>Mergers &amp; Acquisitions</li>
          <li>Corporate Advising</li>
        </ul>
      </div>
      <div class="service-card">
        <h3>Capital Markets</h3>
        <p>Administrative agent for syndicated loan transactions across small, medium, and large ticket markets.</p>
        <ul>
          <li>Loan Syndications</li>
          <li>Revolvers &amp; Term Loans</li>
          <li>Acquisition Financing</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Who We Serve</div>
      <h2 class="section-title">Industries</h2>
      <p class="section-desc">Deep specialization across six sectors &mdash; click through for financing details specific to each.</p>
    </div>
    """ + INDUSTRY_GRID + """
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Twenty Year History</div>
      <h2 class="section-title">What Our Clients Say</h2>
    </div>
    <div class="testi-grid">
      <div class="testi-card">
        <p class="testi-quote">&ldquo;Charabanc financed many motor coaches for me over the years and gave me sage business advice.&rdquo;</p>
        <div class="testi-name">David Bolen</div>
        <div class="testi-co">Academy Bus</div>
      </div>
      <div class="testi-card">
        <p class="testi-quote">&ldquo;Their ingenuity, creativity and understanding of solving difficult problems is unique. I am proud to be their vendor.&rdquo;</p>
        <div class="testi-name">Ward Hicken</div>
        <div class="testi-co">Temsa North America</div>
      </div>
      <div class="testi-card">
        <p class="testi-quote">&ldquo;His tenacity and creativity should be contagious. Charabanc is a special breed that proves being a friend and business partner are not mutually exclusive.&rdquo;</p>
        <div class="testi-name">Kyle Smith</div>
        <div class="testi-co">State Bank &amp; Trust</div>
      </div>
      <div class="testi-card">
        <p class="testi-quote">&ldquo;They are extremely creative and have vast experience and knowledge. When we need advice, they are on speed dial.&rdquo;</p>
        <div class="testi-name">Assad Dakkak</div>
        <div class="testi-co">Dynamic Tours &amp; Transportation</div>
      </div>
    </div>
  </div>
</section>

<div class="resources-band">
  <div class="wrap">
    <div>
      <h2>Credit Applications &amp; Forms</h2>
      <p class="sans">Full-financials and application-only credit applications, personal financial statements, and our church application &mdash; ready to download.</p>
    </div>
    <a class="btn btn-primary" href="resources.html">View Resources</a>
  </div>
</div>"""

write("index.html", page(
    "Motorcoach & Equipment Financing", "Motorcoach, bus, and equipment financing since 2002. Loans, TRAC and municipal leases. App-only approvals to $750K in hours; larger deals with financials.",
    "index.html", home_body
))

# ============================================================ ABOUT
about_body = page_header(
    "Twenty Year History", "About Charabanc",
    "A dynamic financial support company serving the commercial equipment lending market &mdash; competitive pricing, creative deal structure, and comprehensive knowledge of the finance industry.",
    narrow=True,
) + """
<section class="block">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Our Approach</div>
      <h2 class="section-title">Mission &amp; Vision</h2>
    </div>
    <div class="mv-grid">
      <div class="mv-card">
        <div class="mv-label">Mission</div>
        <p class="mv-statement">To provide value-driven Financial Analysis, Operational Analysis and Business Valuation services for our clients.</p>
      </div>
      <div class="mv-card">
        <div class="mv-label">Vision</div>
        <p class="mv-statement">Everyone wants to provide value for someone else. We do it a deal, a phone call, a client, and a friend at a time.</p>
      </div>
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Leadership</div>
      <h2 class="section-title">Team</h2>
    </div>
    <div class="team-grid">
      <div class="team-card">
        <img class="team-photo" src="assets/headshots/jason-cash.jpg" alt="Jason Cash">
        <h3>Jason Cash</h3>
        <div class="role">CEO</div>
        <p>After 10 years working for domestic and foreign banks, he created Charabanc in 2002. He has held roles in credit, management, syndication, and sales within equipment finance, plus ownership experience in manufacturing and dealerships. He serves as Corporate Advisor to multiple large and small companies throughout the United States and Canada.</p>
      </div>
      <div class="team-card">
        <img class="team-photo" src="assets/headshots/mike-cash.jpg" alt="Mike Cash">
        <h3>Mike Cash</h3>
        <div class="role">GM</div>
        <p>Retired US Coast Guard Captain with 30 years of distinguished service. His background includes expertise as Chief Information Officer, Cyber Commander, and Strategic Organization Transformation Leader.</p>
      </div>
      <div class="team-card">
        <img class="team-photo" src="assets/headshots/mike-sims.jpg" alt="Mike Sims">
        <h3>Mike Sims</h3>
        <div class="role">CFO</div>
        <p>With the company since 2010, handling the internal and external accounting for motor coach clients. Over 30 years of experience as Controller across industries; Accounting degree from the University of Alabama in Birmingham.</p>
      </div>
      <div class="team-card">
        <img class="team-photo" src="assets/headshots/frank-deutsch.jpg" alt="Frank Deutsch">
        <h3>Frank Deutsch</h3>
        <div class="role">Director of Project Management</div>
        <p>Working for Charabanc for ten years with 25 years of experience in the bus and motor coach market. A mechanical engineer with multilingual capabilities.</p>
      </div>
    </div>
  </div>
</section>"""
write("about.html", page(
    "About Us & Leadership Team", "Charabanc Financial has structured equipment and motorcoach financing since 2002. Meet the team behind twenty years of deals across the U.S. and Canada.",
    "about.html", about_body
))

# ============================================================ TESTIMONIALS
testimonials_body = page_header(
    "Client Stories", "Testimonials",
    "Twenty years of relationships built one deal, one phone call, one client at a time.",
) + """
<section class="block">
  <div class="wrap">
    <div class="testi-grid">
      <div class="testi-card">
        <p class="testi-quote">&ldquo;Charabanc financed many motor coaches for me over the years and gave me sage business advice.&rdquo;</p>
        <div class="testi-name">David Bolen</div>
        <div class="testi-co">Academy Bus</div>
      </div>
      <div class="testi-card">
        <p class="testi-quote">&ldquo;Their ingenuity, creativity and understanding of solving difficult problems is unique. I am proud to be their vendor.&rdquo;</p>
        <div class="testi-name">Ward Hicken</div>
        <div class="testi-co">Temsa North America</div>
      </div>
      <div class="testi-card">
        <p class="testi-quote">&ldquo;His tenacity and creativity should be contagious. Charabanc is a special breed that proves being a friend and business partner are not mutually exclusive.&rdquo;</p>
        <div class="testi-name">Kyle Smith</div>
        <div class="testi-co">State Bank &amp; Trust</div>
      </div>
      <div class="testi-card">
        <p class="testi-quote">&ldquo;They are extremely creative and have vast experience and knowledge. When we need advice, they are on speed dial.&rdquo;</p>
        <div class="testi-name">Assad Dakkak</div>
        <div class="testi-co">Dynamic Tours &amp; Transportation</div>
      </div>
    </div>
  </div>
</section>"""
write("testimonials.html", page(
    "Client Testimonials", "What motorcoach operators, manufacturers, and banking partners say about working with Charabanc Financial.",
    "about.html", testimonials_body
))

# ============================================================ SERVICES (overview)
services_body = page_header(
    "What We Do", "Services",
    "CHARABANC's success is based on its industry specialization and a strong commitment to our customers. Through our commitment, we strive to create long-term business relationships.",
) + """
<section class="block">
  <div class="wrap">
    <div class="service-grid cols-2">
      <div class="service-card">
        <h3>Commercial Financing</h3>
        <p>From application-only deals under $150,000 to complex transactions with large public companies and municipalities.</p>
        <ul>
          <li>Equipment Financing</li>
          <li>Vendor Financing (floorplan &amp; retail)</li>
          <li>Loans, Capitalized &amp; Operating Leases</li>
          <li>TRAC &amp; Municipal Leases</li>
        </ul>
        <a href="commercial-financing.html" class="card-link">Learn more &rarr;</a>
      </div>
      <div class="service-card">
        <h3>Corporate Services</h3>
        <p>Value-driven financial and operational analysis to help your business grow.</p>
        <ul>
          <li>Financial &amp; Operational Analysis</li>
          <li>Business Valuation</li>
          <li>Mergers &amp; Acquisitions</li>
          <li>Corporate Advising</li>
        </ul>
        <a href="corporate-services.html" class="card-link">Learn more &rarr;</a>
      </div>
    </div>
  </div>
</section>"""
write("services.html", page(
    "Equipment Finance & Advisory Services", "Equipment loans, leases, and vendor finance programs, plus business valuation, M&amp;A, and corporate advisory services from Charabanc Financial.",
    "services.html", services_body
))

# ============================================================ COMMERCIAL FINANCING
cf_body = page_header(
    "Services", "Commercial Financing",
    "CHARABANC facilitates transactions of the most complex structure with large public companies and municipalities. Conversely, we assist small operators with a simple, application-only transaction under $150,000.",
    breadcrumb='<a href="services.html">Services</a> / Commercial Financing',
    narrow=True,
) + """
<section class="block">
  <div class="wrap prose">
    <h2>Equipment Financing</h2>
    <p>We finance new and used equipment with structures tailored to the size and complexity of the deal &mdash; from application-only transactions to large public company and municipal financings.</p>
    <ul class="feature-list">
      <li>Loans</li>
      <li>Capitalized Leases</li>
      <li>Operational Leases</li>
      <li>TRAC Leases</li>
      <li>Municipal Leases</li>
    </ul>
    <h2>Vendor Financing</h2>
    <p>CHARABANC develops vendor programs that are competitive, easy, straightforward and tailored to your industry &mdash; all of which help you and your organization meet your business objectives.</p>
    <ul class="feature-list">
      <li>Floorplan Financing</li>
      <li>Retail Financing</li>
    </ul>
    <p><a href="contact.html" class="btn btn-primary">Contact Us</a></p>
  </div>
</section>"""
write("commercial-financing.html", page(
    "Equipment Loans & TRAC Leases", "Commercial equipment financing: loans, capital and operating leases, TRAC and municipal leases, and floorplan and retail vendor programs. Application-only under $150,000.",
    "services.html", cf_body
))

# ============================================================ CORPORATE SERVICES
cs_body = page_header(
    "Services", "Corporate Services",
    "We provide equipment financing, mergers and acquisitions, corporate advisory services, and accounting services.",
    breadcrumb='<a href="services.html">Services</a> / Corporate Services',
    narrow=True,
) + """
<section class="block">
  <div class="wrap prose">
    <h2>Financial Analysis</h2>
    <p>We review the quality of your financial statements; accounting and bookkeeping practices, cash flow analysis, operational expenditures, financial planning, and exit strategy.</p>
    <h2>Operational Analysis</h2>
    <p>We help you identify best practices in fleet management, safety, RFP preparation, hardware/software solutions, and the latest in regulatory changes impacting the industry.</p>
    <h2>Business Valuation</h2>
    <p>This is a comprehensive Business Solutions package, encompassing Financial Analysis, Operational Analysis, and additional customized programs for you and your company.</p>
    <h2>Mergers and Acquisitions</h2>
    <p>We maintain an extensive database on thousands of public and private companies, buying groups, lenders, mezzanine equity sources, attorneys, accountants, appraisers and other professionals associated with successful deal-making.</p>
    <ul class="feature-list">
      <li>Business Valuation</li>
      <li>Financial Planning</li>
      <li>Buyer Representation</li>
      <li>Seller Representation</li>
      <li>Corporate Advising</li>
      <li>Operational Efficiency</li>
      <li>RFP Preparation</li>
      <li>Cyber &amp; Logistics</li>
    </ul>
    <p><a href="contact.html" class="btn btn-primary">Contact Us</a></p>
  </div>
</section>"""
write("corporate-services.html", page(
    "Business Valuation & M&A Advisory", "Financial and operational analysis, business valuation, and buy-side and sell-side M&amp;A advisory for transportation and equipment-intensive businesses.",
    "services.html", cs_body
))

# ============================================================ INDUSTRIES (overview)
INDUSTRY_CARDS = [
    ("01", "transportation.html", "Transportation", "App-only to $750K &middot; more with financials",
     "Motor coaches, transit and paratransit buses, dump trucks, and specialty vocational vehicles."),
    ("02", "construction-forestry.html", "Construction / Forestry", "Up to $250,000",
     "Feller bunchers, knuckleboom loaders, backhoe loaders, skidders, and excavators."),
    ("03", "manufacturing-printing.html", "Manufacturing / Printing", "Up to $250,000",
     "Fabricating systems, punch presses, weld cells, machine tools, and lasers."),
    ("04", "audio-video.html", "Audio / Video", "Up to $250,000",
     "Professional audio, video monitoring, recording, projection, and conferencing equipment."),
    ("05", "professional-firms.html", "Professional Firms", "Custom Solutions",
     "Working capital, term loans, and leasing for legal, medical, accounting, and consulting practices."),
    ("06", "capital-markets.html", "Capital Markets", "Syndicated Deals",
     "Administrative agent for syndicated loan transactions across small, medium, and large ticket markets."),
]
industry_cards_html = "\n      ".join(
    f'''<a class="industry-card" href="{href}">
        <span class="num">{num}</span>
        <h3>{name}</h3>
        <p>{desc}</p>
        <span class="cap-pill">{cap}</span>
      </a>''' for num, href, name, cap, desc in INDUSTRY_CARDS
)

industries_body = page_header(
    "Who We Serve", "Industries",
    "Deep specialization across six sectors. Click through for financing details specific to each.",
) + f"""
<section class="block">
  <div class="wrap">
    <div class="industry-cards">
      {industry_cards_html}
    </div>
    <div class="cap-banner" style="margin-top:2.5rem;">
      <div>
        <div class="cap-value">Need more details?</div>
      </div>
      <a class="btn btn-primary" href="contact.html">Contact Us</a>
    </div>
  </div>
</section>"""
write("industries.html", page(
    "Industries We Finance", "Financing for motorcoaches and buses, trucks, construction and forestry equipment, manufacturing and printing equipment, audio/video, professional firms, and syndicated deals.",
    "industries.html", industries_body
))

def industry_page(fname, title, cap, intro, equipment, extra_features=None,
                  seo_title=None, seo_desc=None, extra_html="", cap_label="Financing Available",
                  cap_note="", cap_feature=None):
    features = [
        "New and used equipment financing",
        "90-day deferred payment options",
        "Seasonal payments (skip up to 3 consecutive payments annually)",
        "100% financing available",
        cap_feature or f"Applications up to {cap}",
        "Municipal leasing options",
        "Wide credit approval window (A+ to C)",
        "Start-up underwriting with good credit",
    ]
    if extra_features:
        features = extra_features
    feat_html = "\n      ".join(f"<li>{x}</li>" for x in features)
    tags_html = "\n      ".join(f'<span class="equip-tag">{x}</span>' for x in equipment)
    body = page_header(
        "Industries", title,
        intro,
        breadcrumb=f'<a href="industries.html">Industries</a> / {title.replace(" Financing", "")}'
    ) + f"""
<section class="block">
  <div class="wrap">
    <div class="cap-banner">
      <div>
        <div class="cap-label sans">{cap_label}</div>
        <div class="cap-value">Up to {cap}</div>{f'<div class="cap-note sans">{cap_note}</div>' if cap_note else ""}
      </div>
      <a class="btn btn-primary" href="contact.html">Apply Now</a>
    </div>
    <div class="prose" style="max-width:none;">
      <h2>Features</h2>
      <ul class="feature-list">
      {feat_html}
      </ul>
      <h2>Equipment We Finance</h2>
      <div class="equip-tags">
      {tags_html}
      </div>
      {extra_html}
      <p><a href="resources.html" class="btn btn-ghost">View Credit Applications</a></p>
    </div>
  </div>
</section>"""
    write(fname, page(seo_title or title,
                      seo_desc or f"{title} up to {cap} &mdash; fast, affordable financing from Charabanc Financial.",
                      "industries.html", body))

industry_page(
    "transportation.html", "Transportation Financing", "$750,000",
    "CHARABANC's transportation financing is fast, affordable and reputable. Our streamlined process can approve application-only requests of up to $750,000 within a few hours, and we finance much larger deals with full financials.",
    ["Motor Coaches", "Dump &amp; Hauling Trucks", "Cutaway Buses", "Transit Buses", "Paratransit Buses",
     "Delivery &amp; Box Trucks", "Food &amp; Catering Trucks", "Crane Trucks", "School Buses", "Specialty Trucks"],
    seo_title="Bus & Commercial Truck Financing",
    seo_desc="Motorcoach, cutaway, transit, school bus and specialty truck financing. App-only approvals to $750K in hours; larger deals with full financials.",
    extra_html="""<h2>Specialized Bus Financing</h2>
      <p>Buses are where Charabanc started, and they remain the core of what we do. See our dedicated pages for <a href="motorcoach-financing.html">motorcoach financing</a> for charter and tour operators, and <a href="church-bus-financing.html">church bus financing</a> for houses of worship.</p>""",
    cap_label="Application Only",
    cap_note="Much larger amounts with full financials",
    cap_feature="Application-only up to $750,000; larger deals with full financials",
)

industry_page(
    "construction-forestry.html", "Construction / Forestry Financing", "$250,000",
    "CHARABANC finances heavy construction and forestry equipment quickly and affordably, with a streamlined approval process.",
    ["Feller Bunchers", "Knuckleboom Loaders", "Backhoe Loaders", "Skidders", "Compact Excavators", "Attachments &amp; Implements"],
    seo_title="Logging & Construction Equipment Loans",
    seo_desc="Financing for feller bunchers, knuckleboom loaders, skidders, backhoes and excavators. New and used, up to $250,000, with seasonal and deferred payment options.",
)

industry_page(
    "manufacturing-printing.html", "Manufacturing / Printing Financing", "$250,000",
    "CHARABANC's manufacturing and printing financing is fast, affordable and reputable, covering all types of production equipment.",
    ["Scanners", "Fabricating Systems", "38&ndash;350 Ton Punch Presses", "Weld Cells", "Press Brakes", "Machine Tools", "Lasers", "Shuttle Systems"],
    seo_title="Manufacturing & Printing Equipment Loans",
    seo_desc="Financing for punch presses, press brakes, weld cells, lasers, machine tools and printing equipment. New and used, up to $250,000, with 100% financing available.",
)

industry_page(
    "audio-video.html", "Audio / Video Financing", "$250,000",
    "CHARABANC's audio and video financing is fast, affordable and reputable, through a straightforward credit application process.",
    ["Converters", "Professional Audio Equipment", "Switches", "Software", "Video Monitoring Systems",
     "Recording Equipment", "Projectors", "Music Systems", "Post-Production Editing Equipment", "Video Conference Systems", "Wireless System Packages"],
    seo_title="Audio & Video Equipment Financing",
    seo_desc="Leasing and loans for professional audio, recording, projection, video monitoring and conferencing systems. Up to $250,000 with a simple credit application.",
)

industry_page(
    "professional-firms.html", "Professional Firms Financing", "Custom Solutions",
    "Professionals in Legal, Accounting, Medical, Engineering, Architecture, Consulting and other practices face unique challenges. Financial and operational issues require third-party support from a firm that understands the solutions you need. After many years of analyzing companies over a wide spectrum of industry segments, CHARABANC can customize a creative solution that will ensure your business grows.",
    ["Legal", "Accounting", "Medical", "Engineering", "Architecture", "Consulting"],
    extra_features=[
        "Working capital lines of credit",
        "Term loans",
        "A variety of leasing options",
        "Organic and inorganic growth options",
        "Growth Funding",
        "Capital for Acquisitions",
        "Refinances / Debt Consolidations",
    ],
    seo_title="Financing for Professional Firms",
    seo_desc="Working capital lines, term loans, leasing, acquisition capital and debt consolidation for legal, medical, accounting, engineering and consulting practices.",
)

industry_page(
    "capital-markets.html", "Capital Markets Financing", "Syndicated Facilities",
    "CHARABANC is an administrative agent for syndicated loan transactions for borrowers and lessees in small, medium, and large ticket markets, structuring customized solutions through regional banks, industrial finance companies, and independent leasing companies.",
    ["Revolvers", "Term Loans (Secured &amp; Unsecured)", "Acquisition Financing"],
    extra_features=[
        "Practical, efficient means of accessing large pools of committed credit",
        "Reduces time-consuming negotiation of multiple transactions",
        "Strategic, exclusive, and comprehensive funding options",
        "Supports working capital, capital expenditures, acquisitions, and recapitalization",
    ],
    seo_title="Loan Syndication & Capital Markets",
    seo_desc="Charabanc acts as administrative agent for syndicated revolvers, term loans and acquisition financing through regional banks and independent leasing companies.",
)

# ============================================================ BUS LANDING PAGES (SEO, added 2026-09-28)
# Keyword landing pages carved out of Transportation, using the .lp-* / .stat /
# .reason / .steps / .compare / .faq / .cta-band blocks in build_site.py.
# Every claim is taken from existing site copy (transportation features,
# resources page, testimonials, team bios). New claims need Alex/Mike sign-off.
import json as _json

def _strip_tags(t):
    t = re.sub(r"<[^>]+>", "", t)
    for a, b in (("&amp;", "&"), ("&mdash;", "—"), ("&rsquo;", "’"), ("&ndash;", "–")):
        t = t.replace(a, b)
    return t

def _ld(data):
    return f'<script type="application/ld+json">\n{_json.dumps(data, indent=2)}\n</script>\n'

def faq_block(faqs):
    """Accordion FAQ + matching FAQPage JSON-LD (structured data must mirror on-page text)."""
    html = "\n      ".join(
        f'<details><summary>{q}</summary><div class="answer">{a}</div></details>' for q, a in faqs)
    ld = _ld({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": _strip_tags(q),
                        "acceptedAnswer": {"@type": "Answer", "text": _strip_tags(a)}} for q, a in faqs],
    })
    return f'<div class="faq">\n      {html}\n    </div>', ld

def breadcrumb_ld(trail):
    return _ld({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": canonical_url(f)}
                            for i, (n, f) in enumerate(trail)],
    })

def lp_hero(crumb, eyebrow, h1, lede, primary, secondary):
    return f"""<section class="lp-hero">
  <div class="wrap">
    <div class="breadcrumb"><a href="industries.html">Industries</a> / <a href="transportation.html">Transportation</a> / {crumb}</div>
    <div class="eyebrow sans">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{primary[1]}">{primary[0]}</a>
      <a class="btn btn-ghost" href="{secondary[1]}">{secondary[0]}</a>
    </div>
  </div>
</section>"""

def stat_strip(stats):
    cells = "\n      ".join(f'<div class="stat"><div class="stat-value">{v}</div><div class="stat-label">{l}</div></div>' for v, l in stats)
    return f"""<div class="wrap"><div class="stat-strip">
      {cells}
    </div></div>"""

def section(inner, label, title, desc="", alt=False):
    d = f'\n      <p class="section-desc">{desc}</p>' if desc else ""
    return f"""<section class="block{' alt' if alt else ''}">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">{label}</div>
      <h2 class="section-title">{title}</h2>{d}
    </div>
    {inner}
  </div>
</section>"""

def reasons(items):
    out = []
    for h, p, bullets in items:
        lis = "".join(f"<li>{b}</li>" for b in bullets)
        out.append(f'<div class="reason"><h3>{h}</h3><p>{p}</p><ul>{lis}</ul></div>')
    return '<div class="reason-grid">\n      ' + "\n      ".join(out) + "\n    </div>"

def finance_tiles(items):
    return '<div class="finance-grid">\n      ' + "\n      ".join(
        f'<div class="finance-tile">{n}<span>{s}</span></div>' for n, s in items) + "\n    </div>"

def steps(items):
    return '<div class="steps">\n      ' + "\n      ".join(
        f'<div class="step"><h3>{h}</h3><p>{p}</p></div>' for h, p in items) + "\n    </div>"

def cta_band(h, p, primary, secondary):
    return f"""<section class="cta-band">
  <div class="wrap">
    <h2>{h}</h2>
    <p>{p}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{primary[1]}">{primary[0]}</a>
      <a class="btn btn-ghost" href="{secondary[1]}">{secondary[0]}</a>
    </div>
    <span class="phone">Or call us at <a href="tel:7064605231">706-460-5231</a></span>
  </div>
</section>"""

BUS_STATS = [
    ("$750K", "On the application alone, more with financials"),
    ("Hours", "Approval turnaround, not weeks"),
    ("A+ to C", "Wide credit approval window"),
    ("Since 2002", "Financing buses and coaches"),
]

APPLY_STEPS = [
    ("Apply", 'Download a <a href="resources.html">credit application</a>. Smaller requests can go application-only: the application, recent bank statements, and a short company overview.'),
    ("Get a Decision", "Application-only requests up to $750,000 can be approved within a few hours. Larger deals are structured with full financials."),
    ("Hit the Road", "We structure payments around your calendar, including seasonal skips and 90-day deferred first payments."),
]

# ---------- Motorcoach financing ----------
mc_faqs = [
    ("How fast can a motorcoach loan be approved?",
     "Application-only requests of up to $750,000 can be approved within a few hours once we have a complete application. Larger deals, submitted with full financials, take a little longer because we structure them individually."),
    ("Do you finance used motorcoaches?",
     "Yes. We finance both new and used motorcoaches, as well as cutaway, transit, paratransit, and school buses."),
    ("What credit do I need to finance a coach?",
     "We work across a wide credit window, from A+ to C, and can underwrite start-up operators who have good personal credit."),
    ("Can I skip payments during my slow season?",
     "Yes. Seasonal payment structures let charter and tour operators skip up to three consecutive payments each year, and 90-day deferred first payments are also available."),
    ("What is a TRAC lease, and is it right for a motorcoach?",
     "A TRAC (Terminal Rental Adjustment Clause) lease is designed for over-the-road vehicles: you and the lessor agree on the coach&rsquo;s residual value up front, which can lower monthly payments compared with a loan. Whether a TRAC lease or a loan is better depends on your tax position and how long you plan to run the coach. We walk through both with you, and you should confirm the tax treatment with your accountant."),
    ("What do I need to apply?",
     'Smaller requests can go application-only: a credit application, recent bank statements, and a short company overview. Larger requests use our full-financials application with business tax returns and financial statements. Both are on our <a href="resources.html">Resources page</a>.'),
]
mc_faq_html, mc_faq_ld = faq_block(mc_faqs)

mc_body = (
    lp_hero("Motorcoach Financing", "Motorcoach Loans &amp; TRAC Leases",
            'Motorcoach Financing <span class="accent">Built by Coach People.</span>',
            "Loans and leases for charter, tour, and line-run operators, from a single used coach to a full fleet refresh. Application-only approvals up to $750,000 in as little as a few hours, and larger deals with full financials.",
            ("Start Your Application", "resources.html"), ("Talk to Us", "contact.html"))
    + stat_strip(BUS_STATS)
    + section(
        '<p class="lp-intro">Motorcoaches are where Charabanc started. For more than twenty years we have financed coaches for charter companies, tour operators, and scheduled-service carriers across the country. Our team includes people with decades in the bus and motorcoach market, so we understand how a coach earns money, how it holds value, and how seasonality hits your cash flow.</p>\n    '
        + reasons([
            ("Built for Seasonality", "Charter and tour revenue isn't flat, and your payments don't have to be either.",
             ["Skip up to 3 consecutive payments a year", "90-day deferred first payment", "100% financing available"]),
            ("Flexible Structures", "We structure the deal around your business, not a standard equipment-loan template.",
             ["Equipment loans", "TRAC, capital &amp; operating leases", "Municipal leases for public fleets"]),
            ("A Wide Credit Window", "From established fleets to operators just getting started.",
             ["A+ to C credit considered", "Start-up underwriting with good credit", "New and used coaches"]),
        ]),
        "Why Charabanc", "Financing From People Who Know Coaches")
    + section(
        finance_tiles([
            ("New Motorcoaches", "Single units or fleet orders"), ("Used Motorcoaches", "Pre-owned coaches of any age"),
            ("Fleet Refreshes", "Add or replace multiple units"), ("Refinancing", "Existing coaches"),
            ("Cutaway &amp; Shuttle", "Mid-size and shuttle buses"), ("Transit Buses", "Fixed-route fleets"),
            ("Paratransit", "ADA and lift-equipped"), ("School Buses", "Private and contract fleets"),
        ])
        + '\n    <p class="makes">We finance coaches from the major manufacturers, including <strong>Prevost, MCI, Van Hool, Temsa,</strong> and <strong>Setra</strong>.</p>'
        + '''
    <div class="callout">
      <div>
        <h3>Still shopping for a coach?</h3>
        <p>Our affiliate, The Bus Coach, buys, sells, and consigns pre-owned motorcoaches and buses. We can have financing lined up before you pick a unit.</p>
      </div>
      <a class="btn btn-ghost" href="https://thebuscoach.com">Browse The Bus Coach</a>
    </div>''',
        "What We Finance", "Every Kind of Coach and Bus", alt=True)
    + section(
        '''<div class="compare">
      <div class="compare-card">
        <span class="tag">Build equity</span>
        <h3>Equipment Loan</h3>
        <p>You own the coach from day one and build equity with every payment.</p>
        <ul><li>Ownership from the start</li><li>No residual at the end of term</li><li>Good fit if you run coaches for the long haul</li></ul>
      </div>
      <div class="compare-card">
        <span class="tag">Lower payment</span>
        <h3>TRAC Lease</h3>
        <p>You and the lessor agree on a residual value up front, which usually means a lower monthly payment.</p>
        <ul><li>Designed for over-the-road vehicles</li><li>Can carry tax advantages</li><li>Good fit for managing monthly cash flow</li></ul>
      </div>
    </div>
    <p class="compare-note">Municipalities and transit agencies can also use municipal leases. Confirm tax treatment with your accountant.</p>''',
        "Loan or Lease?", "Pick the Structure That Fits",
        "We&rsquo;ll lay out both options side by side for your coach and your numbers.")
    + section(steps(APPLY_STEPS), "How It Works", "Three Steps to Your Next Coach", alt=True)
    + section(
        '''<div class="testi-grid">
      <div class="testi-card">
        <p class="testi-quote">&ldquo;Charabanc financed many motor coaches for me over the years and gave me sage business advice.&rdquo;</p>
        <div class="testi-name">David Bolen</div>
        <div class="testi-co">Academy Bus</div>
      </div>
      <div class="testi-card">
        <p class="testi-quote">&ldquo;They are extremely creative and have vast experience and knowledge. When we need advice, they are on speed dial.&rdquo;</p>
        <div class="testi-name">Assad Dakkak</div>
        <div class="testi-co">Dynamic Tours &amp; Transportation</div>
      </div>
    </div>''',
        "What Operators Say", "Trusted by Charter and Tour Operators")
    + section(mc_faq_html, "Questions", "Motorcoach Financing FAQ", alt=True)
    + cta_band("Ready to Finance Your Next Coach?",
               "Send us an application or give us a call. We&rsquo;ll lay out your options, usually within hours.",
               ("Download a Credit Application", "resources.html"), ("Contact Us", "contact.html"))
)
write("motorcoach-financing.html", page(
    "Motorcoach Financing: Loans & TRAC Leases",
    "Motorcoach loans and TRAC leases for charter and tour operators. New and used coaches, app-only approvals to $750K in hours, larger deals with financials.",
    "industries.html", mc_body,
    extra_head=mc_faq_ld + breadcrumb_ld([("Industries", "industries.html"), ("Transportation", "transportation.html"), ("Motorcoach Financing", "motorcoach-financing.html")]),
))

# ---------- Church bus financing ----------
ch_faqs = [
    ("Can a church finance a bus?",
     "Yes. We finance buses for churches, ministries, and other houses of worship, and we have a dedicated Church Application for religious organizations."),
    ("What types of church buses do you finance?",
     "Shuttle and cutaway buses, mid-size buses, school-style buses, and full-size motorcoaches for longer trips, new or used."),
    ("What does our church need to apply?",
     'Start with our <a href="resources.html">Church Application Form</a>. We&rsquo;ll let you know if we need anything else for your request.'),
    ("Is 100% financing available?",
     "Yes, 100% financing is available for qualified borrowers, along with 90-day deferred first payments."),
]
ch_faq_html, ch_faq_ld = faq_block(ch_faqs)

ch_body = (
    lp_hero("Church Bus Financing", "For Churches &amp; Ministries",
            'Church Bus Financing <span class="accent">for Your Congregation.</span>',
            "Financing for churches and ministries buying a shuttle, bus, or motorcoach, with a dedicated church application and flexible payment options.",
            ("Get the Church Application", "resources.html"), ("Talk to Us", "contact.html"))
    + stat_strip([
        ("100%", "Financing available"),
        ("90 Days", "Deferred first payment option"),
        ("New &amp; Used", "Shuttles, buses, and coaches"),
        ("Since 2002", "Financing buses and coaches"),
    ])
    + section(
        '<p class="lp-intro">Youth trips, senior outings, Sunday pick-up routes, mission travel: a reliable bus is often one of the biggest purchases a church makes. Charabanc has financed buses since 2002, and we know churches don&rsquo;t look like typical commercial borrowers. That&rsquo;s why we have a separate church application instead of forms designed for businesses.</p>\n    '
        + reasons([
            ("A Church Application", "A dedicated application for houses of worship and religious organizations.",
             ["Built for religious organizations", "Download and send by email or fax", "We&rsquo;ll tell you if anything else is needed"]),
            ("Easy on the Budget", "Payment options that respect a ministry budget.",
             ["100% financing available", "90-day deferred first payment", "Seasonal payment options"]),
            ("The Right Bus", "From a small shuttle to a full-size coach for longer trips.",
             ["Shuttle &amp; cutaway buses", "Mid-size and school-style buses", "New or used"]),
        ]),
        "Why Charabanc", "Getting Your Congregation on the Road")
    + section(
        finance_tiles([
            ("Shuttle Buses", "Sunday pick-up routes"), ("Cutaway Buses", "Youth and senior trips"),
            ("Mid-Size Buses", "Larger groups"), ("Motorcoaches", "Mission and long-distance travel"),
        ])
        + '''
    <div class="callout">
      <div>
        <h3>Need help finding a bus?</h3>
        <p>Our affiliate, The Bus Coach, sells pre-owned buses and motorcoaches and can help you find the right size for your congregation.</p>
      </div>
      <a class="btn btn-ghost" href="https://thebuscoach.com">Browse The Bus Coach</a>
    </div>''',
        "What We Finance", "Buses for Every Ministry", alt=True)
    + section(steps([
        ("Apply", 'Download the <a href="resources.html">Church Application Form</a> and send it by email or fax.'),
        ("Get a Decision", "Our streamlined transportation process moves quickly once we have a complete application."),
        ("Pick Up Your Bus", "Choose a payment structure that fits your budget, including a 90-day deferred first payment."),
      ]), "How It Works", "Three Simple Steps")
    + section(ch_faq_html, "Questions", "Church Bus Financing FAQ", alt=True)
    + cta_band("Let&rsquo;s Get Your Church on the Road",
               "Download the church application or call us to talk through your options.",
               ("Get the Church Application", "resources.html"), ("Contact Us", "contact.html"))
)
write("church-bus-financing.html", page(
    "Church Bus Financing",
    "Bus and motorcoach financing for churches and ministries. Dedicated church application, new and used buses, 100% financing and deferred payments available.",
    "industries.html", ch_body,
    extra_head=ch_faq_ld + breadcrumb_ld([("Industries", "industries.html"), ("Transportation", "transportation.html"), ("Church Bus Financing", "church-bus-financing.html")]),
))

# ============================================================ RESOURCES
def resource_card(name, meta, href):
    return f"""<a class="resource-card" href="{href}" download>
            <span class="rhead">
              <span class="ricon">PDF</span>
              <span class="rtext">
                <span class="rname">{name}</span>
                <span class="rmeta">{meta}</span>
              </span>
            </span>
            <span class="rdl">Download</span>
          </a>"""

resources_body = page_header(
    "Download our PDF Forms", "Resources",
    "Credit applications and financial statement forms. Each credit application includes a cover sheet listing everything to send with it.",
) + f"""
<section class="block">
  <div class="wrap">
    <div class="resource-groups">
      <div class="resource-group">
        <h2>Full Financials</h2>
        <p class="group-note">Credit application with business tax returns and financial statements.</p>
        <div class="resource-cards">
          {resource_card("Credit App &ndash; Full Financials", "PDF &middot; cover sheet + application", "assets/resources/Credit-App-Full-Financials.pdf")}
          {resource_card("Personal Financial Statement Form", "PDF &middot; required for guarantors", "assets/resources/Personal-Financial-Statement.pdf")}
        </div>
      </div>
      <div class="resource-group">
        <h2>Application Only</h2>
        <p class="group-note">A streamlined path: credit application with bank statements and a company overview.</p>
        <div class="resource-cards">
          {resource_card("Credit App &ndash; Application Only", "PDF &middot; cover sheet + application", "assets/resources/Credit-App-Application-Only.pdf")}
        </div>
      </div>
      <div class="resource-group">
        <h2>Specialized Application</h2>
        <p class="group-note">For houses of worship and religious organizations.</p>
        <div class="resource-cards">
          {resource_card("Church Application Form", "PDF &middot; houses of worship", "assets/resources/Church-Application.pdf")}
        </div>
      </div>
    </div>
    <p class="submit-note">Completed forms can be submitted by fax to <strong>706-460-5232</strong> or by email to <strong><a href="mailto:info@charabancfinancial.com">info@CharabancFinancial.com</a></strong>.</p>
  </div>
</section>"""
write("resources.html", page(
    "Credit Applications & Forms", "Download Charabanc Financial credit applications: full financials, application only, personal financial statement, and a church application for houses of worship.",
    "resources.html", resources_body
))

# ============================================================ CONTACT
contact_body = page_header(
    "Get In Touch", "Contact Us",
    "Reach out to us for business, questions, suggestions, and concerns.",
) + f"""
<section class="block">
  <div class="wrap contact-layout">
    <div class="contact-info">
      {CONTACT_INFO_BLOCK}
    </div>
    <form class="contact-form" name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thank-you.html">
      <input type="hidden" name="form-name" value="contact">
      <p class="hp-field"><label>Don't fill this out: <input name="bot-field"></label></p>
      <div class="form-row">
        <div>
          <label for="name">Name</label>
          <input type="text" id="name" name="name" required>
        </div>
        <div>
          <label for="phone">Phone</label>
          <input type="tel" id="phone" name="phone" required>
        </div>
      </div>
      <div class="form-row">
        <div>
          <label for="company">Company Name</label>
          <input type="text" id="company" name="company">
        </div>
        <div>
          <label for="email">Email</label>
          <input type="email" id="email" name="email">
        </div>
      </div>
      <div>
        <label for="subject">Subject</label>
        <input type="text" id="subject" name="subject">
      </div>
      <div>
        <label for="message">Message</label>
        <textarea id="message" name="message"></textarea>
      </div>
      <fieldset>
        <legend>How did you hear about us?</legend>
        <div class="checkbox-group">
          <label><input type="checkbox" name="how-heard" value="Online Search"> Online Search</label>
          <label><input type="checkbox" name="how-heard" value="Referral"> Referral</label>
          <label><input type="checkbox" name="how-heard" value="Publication Advertisement"> Publication Advertisement</label>
          <label><input type="checkbox" name="how-heard" value="Employee"> Employee</label>
          <label><input type="checkbox" name="how-heard" value="LinkedIn"> LinkedIn</label>
          <label><input type="checkbox" name="how-heard" value="Facebook"> Facebook</label>
          <label><input type="checkbox" name="how-heard" value="Other"> Other</label>
        </div>
      </fieldset>
      <button type="submit" class="btn btn-primary">Send Message</button>
    </form>
  </div>
</section>"""
write("contact.html", page(
    "Contact Us | Lavonia, GA", "Talk to Charabanc Financial about motorcoach or equipment financing. 65 Ayers St., Lavonia, GA 30553. Call 706-460-5231.",
    "contact.html", contact_body
))

# ============================================================ THANK YOU
thankyou_body = page_header(
    "Message Sent", "Thank You",
    "We've received your message and will be in touch shortly.",
) + """
<section class="block">
  <div class="wrap prose" style="text-align:center;">
    <p><a class="btn btn-primary" href="index.html">Back to Home</a></p>
  </div>
</section>"""
write("thank-you.html", page(
    "Thank You", "Your message has been sent to Charabanc Financial.",
    "", thankyou_body
))

# ============================================================ SEO: sitemap + robots + redirects
SITEMAP_PAGES = [
    "index.html", "about.html", "testimonials.html", "services.html",
    "commercial-financing.html", "corporate-services.html", "industries.html",
    "transportation.html", "motorcoach-financing.html", "church-bus-financing.html", "construction-forestry.html", "manufacturing-printing.html",
    "audio-video.html", "professional-firms.html", "capital-markets.html",
    "resources.html", "contact.html",
]  # thank-you.html deliberately excluded — a form-confirmation page, not a search destination
ALL_PAGES = SITEMAP_PAGES + ["thank-you.html"]  # for redirects — thank-you still needs a clean URL

def build_sitemap():
    # Extensionless URLs, matching the canonical tag on every page and the
    # nav's own links. Previously this listed the .html paths — the opposite
    # of what every internal link on the site actually points to, which is
    # exactly the kind of contradictory signal that splits ranking authority
    # between two URLs for the same page.
    urls = "\n".join(
        f'  <url><loc>{canonical_url(p)}</loc></url>' for p in SITEMAP_PAGES
    )
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
'''
    write("sitemap.xml", xml)

def build_robots():
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")

def build_redirects():
    """Netlify auto-detects a file literally named _redirects in the deploy root.
    Two jobs here:
      1. Force a real 301 from every /page.html to its clean /page — Netlify's
         own "both URLs return 200" behavior is what let Google index the
         .html paths in the first place with nothing telling it which was real.
      2. Send the old Wix "-1"-suffixed URLs still sitting in Google's index to
         their real modern equivalent. construction-forestry-1 and
         corporate-services-1 are CONFIRMED dead (404) as of 2026-08-11 — found
         live in a site:charabancfinancial.com search. The rest of this block
         is precautionary (same Wix collision pattern, not individually
         confirmed) — harmless if a given old slug never existed, since an
         unmatched redirect rule is just never triggered.
    """
    lines = ["# Auto-generated by build_pages.py — do not hand-edit, re-run the build instead.", ""]
    lines.append("# --- normalize .html URLs to the clean canonical form ---")
    for fname in ALL_PAGES:
        slug = fname[:-5]  # strip ".html"
        target = "/" if slug == "index" else f"/{slug}"
        lines.append(f"/{fname}  {target}  301!")
    lines.append("")
    lines.append("# --- old Wix URLs still in Google's index ---")
    OLD_WIX_SLUGS = {
        "construction-forestry-1": "construction-forestry",  # confirmed 404, found indexed 2026-08-11
        "corporate-services-1":    "corporate-services",      # confirmed 404, found indexed 2026-08-11
        "manufacturing-printing-1": "manufacturing-printing", # precautionary
        "audio-video-1":            "audio-video",            # precautionary
        "professional-firms-1":     "professional-firms",     # precautionary
        "capital-markets-1":        "capital-markets",        # precautionary
        "commercial-financing-1":   "commercial-financing",   # precautionary
        "transportation-1":         "transportation",         # precautionary
        "services-1":               "services",               # precautionary
        "industries-1":             "industries",             # precautionary
        "about-1":                  "about",                  # precautionary
    }
    for old, new in OLD_WIX_SLUGS.items():
        lines.append(f"/{old}  /{new}  301!")
    lines.append("")
    # Long/Short apps replaced by the cover-sheet versions 2026-09-28 - keep
    # any old bookmarked/emailed links working
    lines.append("# --- retired credit app PDFs ---")
    lines.append("/assets/resources/Long-Credit-Application.pdf  /assets/resources/Credit-App-Full-Financials.pdf  301!")
    lines.append("/assets/resources/Short-Credit-Application.pdf  /assets/resources/Credit-App-Application-Only.pdf  301!")
    write("_redirects", "\n".join(lines) + "\n")

build_sitemap()
build_robots()
build_redirects()

print("resources + contact done")
print("ALL PAGES BUILT")
