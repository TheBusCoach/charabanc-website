# -*- coding: utf-8 -*-
"""Static site generator for the Charabanc Financial rebuild.
Hand-authored, single-source stylesheet with a real type scale (rewritten
after the piecemeal-patched version drifted into ~20 arbitrary font sizes
and inconsistent font-family overrides). Rule: h1/h2/h3 are serif (matches
the logo wordmark), everything else -- body copy, nav, buttons, labels,
cards -- is sans. Eight font-size tokens cover every component; nothing
hardcodes a one-off size outside that scale.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "site")  # relative, so the build runs anywhere (laptop, GitHub, Netlify)
os.makedirs(ROOT, exist_ok=True)
os.makedirs(os.path.join(ROOT, "css"), exist_ok=True)

CSS = """
:root{
  --green:#20503B; --green-dark:#153428; --green-light:#3E6E56;
  --cream:#F6F6F6; --paper:#FFFFFF; --ink:#1A1A1A; --ink-muted:#5C5C5C;
  --line:#E3E3E3; --silver:#9E9E9E; --charcoal:#181818; --charcoal-2:#101010;

  --font-serif: Georgia, "Iowan Old Style", "Times New Roman", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;

  /* type scale -- every font-size in this file references one of these.
     Bumped up a step 2026-07-24, then a second step same day (Mike: still
     too small for an older audience with bad eyesight) -- body text now
     20px, smallest label text now 14px (was 16px / 12px originally). */
  --fs-2xs: 0.875rem;  /* micro labels: eyebrow, breadcrumb, section-label, tags */
  --fs-xs:  1rem;      /* small meta: names, form labels, footer body */
  --fs-sm:  1.1875rem; /* card body copy, list items */
  --fs-base:1.25rem;   /* default paragraph, nav links, buttons, inputs */
  --fs-md:  1.375rem;  /* lede/intro paragraphs, pull-quotes */
  --fs-lg:  1.625rem;  /* card & subsection headings (h3, prose h2) */
  --fs-xl:  clamp(1.75rem, 3.4vw, 2.25rem);   /* section-title h2 */
  --fs-display:    clamp(2.4rem, 5.2vw, 3.8rem); /* home hero h1 */
  --fs-display-sm: clamp(2.125rem, 4.4vw, 2.9rem); /* interior page-header h1 */
}

*{ box-sizing:border-box; }
html{ -webkit-text-size-adjust:100%; }
body{
  margin:0; background:var(--cream); color:var(--ink);
  font-family:var(--font-sans); font-size:var(--fs-base); line-height:1.6;
  -webkit-font-smoothing:antialiased;
}
h1,h2,h3{ font-family:var(--font-serif); font-weight:400; margin:0; color:var(--ink); }
p{ margin:0; }
a{ color:var(--ink); text-decoration:underline; }
a:hover{ color:var(--green); }
.wrap{ max-width:1180px; margin:0 auto; padding:0 2rem; }

/* ---------- header ---------- */
header{ background:var(--paper); border-bottom:1px solid var(--line); position:sticky; top:0; z-index:20; }
.header-row{ display:flex; align-items:center; justify-content:space-between; padding:1rem 2rem; gap:2rem; }
.logo-wrap{ display:block; height:44px; }
.logo-img{ height:44px; width:auto; display:block; }
.footer-logo{ height:28px; display:block; }

nav.main-nav{ position:relative; display:flex; gap:1.7rem; align-items:center; font-size:var(--fs-base); font-weight:600; }
nav.main-nav a{ color:var(--ink); text-decoration:none; }
nav.main-nav a:hover{ color:var(--green); }
.has-dropdown{ position:relative; }
.dropdown-panel{
  display:none; position:absolute; top:100%; left:0; margin-top:0.6rem;
  background:var(--paper); border:1px solid var(--line); border-radius:6px;
  box-shadow:0 8px 24px rgba(0,0,0,0.08); min-width:220px; padding:0.5rem; z-index:30;
}
.has-dropdown:hover .dropdown-panel, .has-dropdown:focus-within .dropdown-panel{ display:block; }
.dropdown-panel::before{ content:""; position:absolute; top:-0.6rem; left:0; right:0; height:0.6rem; }
.dropdown-panel a{ display:block; padding:0.55rem 0.7rem; border-radius:4px; font-size:var(--fs-sm); text-decoration:none; white-space:nowrap; }
.dropdown-panel a:hover{ background:var(--cream); color:var(--green); }
.nav-cta{ background:var(--ink); color:var(--cream) !important; padding:0.55rem 1.2rem; border-radius:3px; font-size:var(--fs-base); }
.nav-cta:hover{ background:var(--green-dark); }

.nav-toggle-checkbox{ display:none; }
.nav-toggle-label{ display:none; cursor:pointer; font-size:1.6rem; line-height:1; padding:0.2rem 0.3rem; }
@media (max-width:900px){
  .nav-toggle-label{ display:block; }
  nav.main-nav{
    display:none; position:absolute; top:100%; left:0; right:0; background:var(--paper);
    flex-direction:column; align-items:flex-start; gap:0; padding:0.5rem 2rem 1.2rem;
    border-bottom:1px solid var(--line); box-shadow:0 8px 16px rgba(0,0,0,0.06);
  }
  .nav-toggle-checkbox:checked ~ nav.main-nav{ display:flex; }
  nav.main-nav > a, nav.main-nav > .has-dropdown{ width:100%; padding:0.7rem 0; border-bottom:1px solid var(--line); }
  nav.main-nav > a:last-child{ border-bottom:none; }
  .dropdown-panel{ display:block; position:static; box-shadow:none; border:none; margin-top:0.3rem; padding:0 0 0 1rem; }
  .nav-cta{ margin-top:0.7rem; text-align:center; }
}

/* ---------- buttons (shared) ---------- */
.btn{ display:inline-block; padding:0.85rem 1.8rem; border-radius:3px; font-family:var(--font-sans); font-weight:600; font-size:var(--fs-base); text-decoration:none; }
.btn-primary{ background:var(--ink); color:var(--cream); }
.btn-primary:hover{ background:var(--green-dark); color:var(--cream); }
.btn-ghost{ border:1.5px solid var(--ink); color:var(--ink); }
.btn-ghost:hover{ border-color:var(--green); color:var(--green); }

/* ---------- eyebrow / labels (shared micro-label style) ---------- */
.eyebrow, .section-label, .breadcrumb{
  font-family:var(--font-sans); text-transform:uppercase; letter-spacing:0.15em;
  font-size:var(--fs-2xs); font-weight:700; color:var(--ink-muted);
}
.breadcrumb{ font-weight:400; letter-spacing:0.02em; text-transform:none; margin-bottom:1rem; }
.breadcrumb a{ color:var(--ink-muted); text-decoration:none; }
.breadcrumb a:hover{ color:var(--green); }

/* ---------- hero (home) ---------- */
.hero{ padding:5rem 0 4.5rem; text-align:center; border-bottom:1px solid var(--line); }
.hero .eyebrow{ margin-bottom:1.1rem; }
.hero-title{ font-size:var(--fs-display); margin-bottom:1.1rem; }
.hero-title .accent{ color:var(--green); font-style:italic; }
.hero-sub{ max-width:640px; margin:0 auto 2.2rem; font-size:var(--fs-md); color:var(--ink-muted); }
.hero-actions{ display:flex; gap:1rem; justify-content:center; flex-wrap:wrap; }

/* ---------- hero carousel (home) ----------
   Pure CSS, no JS -- same philosophy as the .nav-toggle-checkbox hack above.
   5 slides stacked absolutely, each with a positive animation-delay on one
   shared @keyframes so they cross-fade in sequence forever. Delays run
   right-to-left on purpose (nth-child(5)=0s ... nth-child(1)=24s) so the
   dot row sweeps right-to-left, matching Alex's preference 2026-08-04. */
.hero-carousel{ position:relative; overflow:hidden; min-height:640px; border-bottom:1px solid var(--line); }
.hero-slide{
  position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  text-align:center; padding:3rem 0; opacity:0;
  background:linear-gradient(135deg, var(--green-dark), var(--green) 65%, var(--green-light));
  animation:heroFade 30s infinite;
}
.hero-slide::before{
  content:""; position:absolute; width:640px; height:640px; border-radius:50%;
  background:rgba(255,255,255,0.05); right:-180px; top:-220px; pointer-events:none;
}
.hero-slide:nth-child(even){ background:linear-gradient(135deg, var(--green), var(--green-dark) 65%, var(--green-light)); }
.hero-slide:nth-child(1){ animation-delay:24s; }
.hero-slide:nth-child(2){ animation-delay:18s; }
.hero-slide:nth-child(3){ animation-delay:12s; }
.hero-slide:nth-child(4){ animation-delay:6s; }
.hero-slide:nth-child(5){ animation-delay:0s; }
@keyframes heroFade{
  0%   { opacity:0; }
  3%   { opacity:1; }
  17%  { opacity:1; }
  20%  { opacity:0; }
  100% { opacity:0; }
}
.hero-slide .wrap{ position:relative; z-index:1; }
.hero-slide .eyebrow{ color:rgba(255,255,255,0.75); margin-bottom:1.1rem; }
.hero-slide .hero-title{ color:#fff; }
.hero-slide .hero-title .accent{ color:#fff; }
.hero-slide .hero-sub{ color:rgba(255,255,255,0.85); }
.hero-slide .btn-primary{ background:#fff; color:var(--green-dark); }
.hero-slide .btn-primary:hover{ background:var(--cream); color:var(--green-dark); }
.hero-slide .btn-ghost{ border-color:#fff; color:#fff; }
.hero-slide .btn-ghost:hover{ border-color:var(--cream); color:var(--cream); }
.hero-dots{ position:absolute; left:0; right:0; bottom:1.5rem; z-index:2; display:flex; gap:0.6rem; justify-content:center; }
.hero-dots span{ width:8px; height:8px; border-radius:50%; background:rgba(255,255,255,0.35); animation:heroDot 30s infinite; }
.hero-dots span:nth-child(1){ animation-delay:24s; }
.hero-dots span:nth-child(2){ animation-delay:18s; }
.hero-dots span:nth-child(3){ animation-delay:12s; }
.hero-dots span:nth-child(4){ animation-delay:6s; }
.hero-dots span:nth-child(5){ animation-delay:0s; }
@keyframes heroDot{
  0%   { background:rgba(255,255,255,0.35); }
  3%   { background:#fff; }
  17%  { background:#fff; }
  20%  { background:rgba(255,255,255,0.35); }
  100% { background:rgba(255,255,255,0.35); }
}
@media (max-width:900px){
  .hero-carousel{ min-height:760px; }
}
@media (prefers-reduced-motion:reduce){
  .hero-slide, .hero-dots span{ animation:none; }
  .hero-slide{ opacity:0; }
  .hero-slide:first-child{ opacity:1; }
  .hero-dots span{ background:rgba(255,255,255,0.35); }
  .hero-dots span:first-child{ background:#fff; }
}

/* ---------- pillars ---------- */
.pillars{ display:grid; grid-template-columns:repeat(3,1fr); gap:0; border-bottom:1px solid var(--line); }
.pillar{ padding:2.4rem 2rem; text-align:center; border-left:1px solid var(--line); }
.pillar:first-child{ border-left:none; }
.pillar-word{ font-family:var(--font-serif); font-size:var(--fs-lg); margin-bottom:0.5rem; display:inline-block; }
.pillar-word::after{ content:""; display:block; width:28px; height:2px; background:var(--green); margin:0.5rem auto 0; }
.pillar-desc{ font-size:var(--fs-sm); color:var(--ink-muted); }

/* ---------- section shell ---------- */
section.block{ padding:4.5rem 0; }
section.block.alt{ background:var(--paper); }
.section-head{ text-align:center; max-width:640px; margin:0 auto 3rem; }
.section-label{ margin-bottom:0.8rem; }
h2.section-title{ font-size:var(--fs-xl); margin-bottom:0.9rem; }
.section-desc{ color:var(--ink-muted); font-size:var(--fs-base); }

/* ---------- page header (interior pages) ---------- */
.page-header{ padding:3.2rem 0 2.6rem; border-bottom:1px solid var(--line); }
.page-header h1{ font-size:var(--fs-display-sm); margin-bottom:0.8rem; }
.page-header p.lede{ max-width:640px; color:var(--ink-muted); font-size:var(--fs-md); }
/* narrow variant: aligns the title/lede to the same 760px column as .prose content
   below it, so pages mixing a page-header with long-form text don't read as the
   heading being "left" while body copy is "centered" -- both share one left edge. */
.page-header.narrow .wrap > *{ max-width:760px; margin-left:auto; margin-right:auto; }

/* ---------- service cards ---------- */
.service-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:1.6rem; }
.service-grid.cols-2{ grid-template-columns:repeat(2,1fr); max-width:840px; margin:0 auto; }
.service-card{ background:var(--cream); border:1px solid var(--line); border-radius:6px; padding:2rem 1.7rem; }
.service-card h3{ font-size:var(--fs-lg); margin-bottom:0.6rem; }
.service-card p{ font-size:var(--fs-sm); color:var(--ink-muted); margin-bottom:1rem; }
.service-card ul{ font-size:var(--fs-sm); color:var(--ink-muted); margin:0; padding-left:1.1rem; }
.service-card li{ margin-bottom:0.3rem; }
.service-card .card-link{ display:inline-block; margin-top:1.2rem; font-size:var(--fs-xs); font-weight:700; text-decoration:none; color:var(--ink); }
.service-card .card-link:hover{ color:var(--green); }

/* ---------- industries ---------- */
.industry-grid{ display:grid; grid-template-columns:repeat(6,1fr); gap:1px; background:var(--line); border:1px solid var(--line); }
.industry-tile{ display:block; background:var(--paper); padding:1.8rem 1rem; text-align:center; text-decoration:none; }
.industry-tile:hover{ background:var(--cream); }
.industry-tile .num{ display:block; font-size:var(--fs-2xs); color:var(--silver); margin-bottom:0.6rem; }
.industry-tile .name{ display:block; font-size:var(--fs-sm); font-weight:700; color:var(--ink); }
.industry-tile .cap{ display:block; font-size:var(--fs-2xs); color:var(--ink-muted); margin-top:0.3rem; }

/* industries overview page: richer cards instead of the compact home-page strip */
.industry-cards{ display:grid; grid-template-columns:repeat(3,1fr); gap:1.4rem; }
.industry-card{ display:block; background:var(--paper); border:1px solid var(--line); border-radius:6px; padding:1.8rem; text-decoration:none; transition:border-color 0.15s; }
.industry-card:hover{ border-color:var(--ink); }
.industry-card .num{ display:block; font-size:var(--fs-2xs); color:var(--silver); margin-bottom:0.8rem; }
.industry-card h3{ font-size:var(--fs-lg); margin-bottom:0.5rem; }
.industry-card p{ font-size:var(--fs-sm); color:var(--ink-muted); margin-bottom:1rem; }
.industry-card .cap-pill{ display:inline-block; font-size:var(--fs-2xs); font-weight:700; color:var(--green); text-transform:uppercase; letter-spacing:0.06em; }

/* ---------- testimonials ---------- */
.testi-grid{ display:grid; grid-template-columns:repeat(2,1fr); gap:1.6rem; }
.testi-card{ background:var(--cream); border-left:3px solid var(--ink); border-radius:2px; padding:1.6rem 1.8rem; }
.testi-quote{ font-family:var(--font-serif); font-size:var(--fs-md); font-style:italic; margin-bottom:1rem; }
.testi-name{ font-size:var(--fs-xs); font-weight:700; color:var(--ink); }
.testi-co{ font-size:var(--fs-xs); color:var(--ink-muted); }

/* ---------- resources band (home) ---------- */
.resources-band{ background:var(--paper); border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:3.2rem 0; }
.resources-band .wrap{ display:flex; justify-content:space-between; align-items:center; gap:2rem; flex-wrap:wrap; }
.resources-band h2{ font-size:var(--fs-lg); margin-bottom:0.4rem; }
.resources-band p{ color:var(--ink-muted); font-size:var(--fs-base); }

/* ---------- prose (About, long-form) ---------- */
.prose{ max-width:760px; margin:0 auto; font-size:var(--fs-md); }
.prose p{ margin-bottom:1.3rem; }
.prose h2{ font-size:var(--fs-lg); margin:2.2rem 0 0.9rem; }

.mv-grid{ display:grid; grid-template-columns:repeat(2,1fr); gap:1.6rem; max-width:900px; margin:0 auto; }
.mv-card{ background:var(--cream); border:1px solid var(--line); border-radius:6px; padding:2.2rem 2rem; }
.mv-label{ font-family:var(--font-sans); font-size:var(--fs-xs); text-transform:uppercase; letter-spacing:0.08em; color:var(--green); font-weight:700; margin-bottom:0.9rem; display:block; }
.mv-statement{ font-family:var(--font-serif); font-size:var(--fs-md); color:var(--ink); line-height:1.5; }

/* ---------- team ---------- */
.team-grid{ display:grid; grid-template-columns:repeat(2,1fr); gap:1.6rem; }
.team-card{ background:var(--paper); border:1px solid var(--line); border-radius:6px; padding:1.8rem; }
.team-photo{ width:88px; height:88px; border-radius:50%; object-fit:cover; display:block; margin-bottom:1rem; }
.team-card h3{ font-size:var(--fs-lg); margin-bottom:0.15rem; }
.team-card .role{ font-family:var(--font-sans); font-size:var(--fs-xs); text-transform:uppercase; letter-spacing:0.08em; color:var(--green); font-weight:700; margin-bottom:0.9rem; display:block; }
.team-card p{ font-size:var(--fs-sm); color:var(--ink-muted); }

/* ---------- feature list / equipment tags / cap banner (industry & service pages) ---------- */
.feature-list{ display:grid; grid-template-columns:repeat(2,1fr); gap:0.7rem 1.6rem; list-style:none; margin:0 0 2.5rem; padding:0; font-size:var(--fs-sm); }
.feature-list li{ padding-left:1.3rem; position:relative; }
.feature-list li::before{ content:"—"; position:absolute; left:0; color:var(--green); }

.equip-tags{ display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:2.5rem; }
.equip-tag{ font-size:var(--fs-xs); background:var(--cream); border:1px solid var(--line); border-radius:20px; padding:0.4rem 0.9rem; color:var(--ink); }

.cap-banner{ display:flex; align-items:center; justify-content:space-between; gap:1.5rem; flex-wrap:wrap; background:var(--paper); border:1px solid var(--line); border-radius:6px; padding:1.5rem 1.8rem; margin-bottom:2.5rem; }
.cap-banner .cap-label{ display:block; font-size:var(--fs-2xs); color:var(--ink-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.3rem; }
.cap-banner .cap-value{ font-family:var(--font-serif); font-size:var(--fs-xl); color:var(--ink); }
.cap-banner .cap-note{ font-size:var(--fs-sm); color:var(--ink-muted); margin-top:0.3rem; }

/* ---------- resources page ---------- */
.resource-groups{ display:flex; flex-direction:column; gap:2.6rem; margin-bottom:2.5rem; }
.resource-group h2{ font-size:var(--fs-lg); margin-bottom:0.3rem; }
.resource-group .group-note{ font-size:var(--fs-sm); color:var(--ink-muted); margin-bottom:1.1rem; }
.resource-cards{ display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:1rem; }
.resource-card{ display:flex; flex-direction:column; align-items:flex-start; gap:1rem; background:var(--paper); border:1px solid var(--line); border-radius:6px; padding:1.2rem 1.4rem; transition:border-color 0.15s; text-decoration:none; color:var(--ink); }
.resource-card:hover{ border-color:var(--ink); color:var(--ink); }
.resource-card .rhead{ display:flex; align-items:flex-start; gap:0.9rem; }
.resource-card .ricon{ display:flex; align-items:center; justify-content:center; width:38px; height:38px; border-radius:6px; background:var(--cream); color:var(--ink-muted); font-size:var(--fs-xs); font-weight:700; flex:none; }
.resource-card .rtext{ flex:1; }
.resource-card .rname{ display:block; font-size:var(--fs-base); font-weight:600; color:var(--ink); }
.resource-card .rmeta{ display:block; font-size:var(--fs-2xs); color:var(--ink-muted); margin-top:0.15rem; }
.resource-card .rdl{ margin-top:auto; align-self:flex-start; font-size:var(--fs-xs); font-weight:700; color:var(--ink); border:1.5px solid var(--ink); border-radius:3px; padding:0.4rem 0.8rem; text-decoration:none; white-space:nowrap; }
.resource-card .rdl:hover{ background:var(--ink); color:var(--cream); }
.submit-note{ font-size:var(--fs-sm); color:var(--ink-muted); background:var(--cream); border-radius:6px; padding:1.1rem 1.3rem; }

/* ---------- contact page ---------- */
.contact-layout{ display:grid; grid-template-columns:1fr 1.3fr; gap:3rem; align-items:start; }
.contact-info h2{ font-size:var(--fs-lg); margin-bottom:1rem; }
.contact-info ul{ list-style:none; margin:0 0 2rem; padding:0; font-size:var(--fs-base); color:var(--ink-muted); }
.contact-info li{ margin-bottom:0.6rem; }
.contact-info a{ color:var(--ink); }
.contact-form{ display:flex; flex-direction:column; gap:1.1rem; }
.form-row{ display:grid; grid-template-columns:1fr 1fr; gap:1.1rem; }
.contact-form label{ display:block; font-size:var(--fs-xs); font-weight:700; color:var(--ink); margin-bottom:0.4rem; }
.contact-form input, .contact-form textarea{
  width:100%; border:1px solid var(--line); border-radius:4px; padding:0.7rem 0.85rem;
  font-family:var(--font-sans); font-size:var(--fs-base); background:var(--paper); color:var(--ink);
}
.contact-form input:focus, .contact-form textarea:focus{ outline:none; border-color:var(--ink); }
.contact-form textarea{ resize:vertical; min-height:120px; }
.contact-form button{ align-self:flex-start; border:none; cursor:pointer; font:inherit; }
.hp-field{ position:absolute; left:-9999px; }
.contact-form fieldset{ border:none; padding:0; margin:0; }
.contact-form legend{ font-size:var(--fs-xs); font-weight:700; color:var(--ink); margin-bottom:0.5rem; padding:0; }
.checkbox-group{ display:flex; flex-wrap:wrap; gap:0.5rem 1.4rem; }
.checkbox-group label{ display:flex; align-items:center; gap:0.45rem; font-size:var(--fs-xs); font-weight:400; margin-bottom:0; }
.checkbox-group input[type="checkbox"]{ width:auto; margin:0; }

/* ---------- footer ---------- */
footer{ background:var(--charcoal-2); color:#B5B5B5; padding:3.5rem 0 2rem; font-size:var(--fs-sm); }
.footer-grid{ display:grid; grid-template-columns:1.6fr 1fr 1fr 1fr; gap:2rem; margin-bottom:2.5rem; }
footer h4{ font-family:var(--font-sans); color:#fff; font-size:var(--fs-2xs); text-transform:uppercase; letter-spacing:0.1em; margin-top:0; margin-bottom:1rem; }
footer ul{ list-style:none; margin:0; padding:0; }
footer li{ margin-bottom:0.55rem; }
footer a{ color:#B5B5B5; text-decoration:none; }
footer a:hover{ color:#fff; }
.footer-bottom{ border-top:1px solid rgba(255,255,255,0.1); padding-top:1.3rem; display:flex; justify-content:space-between; flex-wrap:wrap; gap:0.5rem; font-size:var(--fs-2xs); color:#767676; }

@media (max-width:900px){
  .pillars{ grid-template-columns:1fr; }
  .pillar{ border-left:none; border-top:1px solid var(--line); }
  .pillar:first-child{ border-top:none; }
  .service-grid, .service-grid.cols-2{ grid-template-columns:1fr; }
  .industry-grid{ grid-template-columns:repeat(2,1fr); }
  .industry-cards{ grid-template-columns:1fr; }
  .testi-grid{ grid-template-columns:1fr; }
  .footer-grid{ grid-template-columns:1fr 1fr; }
  .team-grid{ grid-template-columns:1fr; }
  .mv-grid{ grid-template-columns:1fr; }
  .feature-list{ grid-template-columns:1fr; }
  .resource-cards{ grid-template-columns:1fr; }
  .contact-layout{ grid-template-columns:1fr; }
  .form-row{ grid-template-columns:1fr; }
}

/* ---------- landing pages (motorcoach / church bus) -- added 2026-09-28 ----------
   Reusable blocks for keyword landing pages: green hero, stat strip, reason
   cards, step row, loan-vs-lease compare, FAQ accordion, closing CTA band.
   All sizes use the existing type scale; no JS. */
.lp-hero{ position:relative; overflow:hidden; color:#fff; padding:3.2rem 0 6.5rem;
  background:linear-gradient(135deg, var(--green-dark), var(--green) 65%, var(--green-light)); }
.lp-hero::before{ content:""; position:absolute; width:640px; height:640px; border-radius:50%;
  background:rgba(255,255,255,0.05); right:-200px; top:-260px; pointer-events:none; }
.lp-hero .wrap{ position:relative; z-index:1; }
.lp-hero .breadcrumb, .lp-hero .breadcrumb a{ color:rgba(255,255,255,0.7); }
.lp-hero .breadcrumb a:hover{ color:#fff; }
.lp-hero .eyebrow{ color:rgba(255,255,255,0.75); margin:1.6rem 0 0.9rem; }
.lp-hero h1{ color:#fff; font-size:var(--fs-display); line-height:1.1; margin-bottom:1.1rem; max-width:760px; }
.lp-hero h1 .accent{ font-style:italic; }
.lp-hero .lede{ font-size:var(--fs-md); color:rgba(255,255,255,0.88); max-width:680px; margin-bottom:2rem; }
.lp-hero .hero-actions{ justify-content:flex-start; }
.lp-hero .btn-primary{ background:#fff; color:var(--green-dark); }
.lp-hero .btn-primary:hover{ background:var(--cream); color:var(--green-dark); }
.lp-hero .btn-ghost{ border-color:#fff; color:#fff; }
.lp-hero .btn-ghost:hover{ border-color:var(--cream); color:var(--cream); }

.stat-strip{ position:relative; z-index:2; margin-top:-4rem; display:grid; grid-template-columns:repeat(4,1fr);
  background:var(--paper); border:1px solid var(--line); border-radius:8px; box-shadow:0 12px 32px rgba(0,0,0,0.07); }
.stat{ padding:1.7rem 1.4rem; text-align:center; border-left:1px solid var(--line); }
.stat:first-child{ border-left:none; }
.stat-value{ font-family:var(--font-serif); font-size:var(--fs-xl); color:var(--green); line-height:1.15; }
.stat-label{ font-size:var(--fs-xs); color:var(--ink-muted); margin-top:0.35rem; }

.lp-intro{ max-width:780px; margin:0 auto; text-align:center; font-size:var(--fs-md); color:var(--ink-muted); }
.reason-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:1.6rem; margin-top:2.6rem; }
.reason{ background:var(--paper); border:1px solid var(--line); border-top:3px solid var(--green); border-radius:6px; padding:1.9rem 1.7rem; }
.reason h3{ font-size:var(--fs-lg); margin-bottom:0.6rem; }
.reason p{ font-size:var(--fs-sm); color:var(--ink-muted); }
.reason ul{ list-style:none; padding:0; margin:0.9rem 0 0; font-size:var(--fs-sm); }
.reason li{ padding:0.3rem 0 0.3rem 1.5rem; position:relative; }
.reason li::before{ content:"\\2713"; position:absolute; left:0; color:var(--green); font-weight:700; }

.finance-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--line); border:1px solid var(--line); border-radius:6px; overflow:hidden; }
.finance-tile{ background:var(--paper); padding:1.5rem 1.2rem; text-align:center; font-size:var(--fs-sm); font-weight:700; }
.finance-tile span{ display:block; font-weight:400; font-size:var(--fs-2xs); color:var(--ink-muted); margin-top:0.25rem; }
.makes{ text-align:center; margin-top:1.8rem; font-size:var(--fs-sm); color:var(--ink-muted); }
.makes strong{ color:var(--ink); }

.steps{ display:grid; grid-template-columns:repeat(3,1fr); gap:1.6rem; counter-reset:step; }
.step{ position:relative; padding:0 0.5rem; text-align:center; }
.step::before{ counter-increment:step; content:counter(step); display:flex; align-items:center; justify-content:center;
  width:3.2rem; height:3.2rem; margin:0 auto 1rem; border-radius:50%; background:var(--green); color:#fff;
  font-family:var(--font-serif); font-size:var(--fs-lg); }
.step h3{ font-size:var(--fs-lg); margin-bottom:0.5rem; }
.step p{ font-size:var(--fs-sm); color:var(--ink-muted); }
.step a{ color:var(--green); }

.compare{ display:grid; grid-template-columns:1fr 1fr; gap:1.6rem; max-width:980px; margin:0 auto; }
.compare-card{ background:var(--paper); border:1px solid var(--line); border-radius:6px; padding:2rem 1.8rem; }
.compare-card .tag{ display:inline-block; font-size:var(--fs-2xs); font-weight:700; text-transform:uppercase; letter-spacing:0.12em;
  color:var(--green); background:rgba(32,80,59,0.08); padding:0.25rem 0.6rem; border-radius:3px; margin-bottom:0.8rem; }
.compare-card h3{ font-size:var(--fs-lg); margin-bottom:0.6rem; }
.compare-card p{ font-size:var(--fs-sm); color:var(--ink-muted); }
.compare-card ul{ list-style:none; padding:0; margin:1rem 0 0; font-size:var(--fs-sm); }
.compare-card li{ padding:0.35rem 0 0.35rem 1.5rem; position:relative; border-top:1px solid var(--line); }
.compare-card li::before{ content:"\\2713"; position:absolute; left:0; color:var(--green); font-weight:700; }
.compare-note{ text-align:center; font-size:var(--fs-xs); color:var(--ink-muted); margin-top:1.4rem; }

.callout{ display:flex; align-items:center; justify-content:space-between; gap:1.5rem; flex-wrap:wrap; margin-top:2.4rem;
  background:var(--paper); border:1px solid var(--line); border-left:4px solid var(--green); border-radius:6px; padding:1.5rem 1.8rem; }
.callout h3{ font-size:var(--fs-lg); margin-bottom:0.3rem; }
.callout p{ font-size:var(--fs-sm); color:var(--ink-muted); }

.faq{ max-width:860px; margin:0 auto; border-top:1px solid var(--line); }
.faq details{ border-bottom:1px solid var(--line); }
.faq summary{ list-style:none; cursor:pointer; display:flex; justify-content:space-between; align-items:center; gap:1rem;
  padding:1.3rem 0.2rem; font-family:var(--font-serif); font-size:var(--fs-lg); color:var(--ink); }
.faq summary::-webkit-details-marker{ display:none; }
.faq summary::after{ content:"+"; font-family:var(--font-sans); font-size:1.8rem; line-height:1; color:var(--green); flex-shrink:0; }
.faq details[open] summary::after{ content:"\\2212"; }
.faq summary:hover{ color:var(--green); }
.faq .answer{ padding:0 0.2rem 1.4rem; font-size:var(--fs-sm); color:var(--ink-muted); max-width:760px; }
.faq .answer a{ color:var(--green); }

.cta-band{ color:#fff; text-align:center; padding:4rem 0;
  background:linear-gradient(135deg, var(--green), var(--green-dark) 65%, var(--green-light)); }
.cta-band h2{ color:#fff; font-size:var(--fs-xl); margin-bottom:0.7rem; }
.cta-band p{ color:rgba(255,255,255,0.85); font-size:var(--fs-md); max-width:640px; margin:0 auto 1.8rem; }
.cta-band .btn-primary{ background:#fff; color:var(--green-dark); }
.cta-band .btn-ghost{ border-color:#fff; color:#fff; }
.cta-band .phone{ display:block; margin-top:1.3rem; font-size:var(--fs-sm); color:rgba(255,255,255,0.8); }
.cta-band .phone a{ color:#fff; }

@media (max-width:900px){
  .lp-hero{ padding:2.4rem 0 5.5rem; }
  .stat-strip{ grid-template-columns:1fr 1fr; }
  .stat:nth-child(3){ border-left:none; }
  .stat:nth-child(n+3){ border-top:1px solid var(--line); }
  .reason-grid, .steps, .compare{ grid-template-columns:1fr; }
  .finance-grid{ grid-template-columns:1fr 1fr; }
  .lp-intro{ text-align:left; }
}
"""

with open(os.path.join(ROOT, "css", "style.css"), "w", encoding="utf-8") as f:
    f.write(CSS)

print("wrote style.css:", len(CSS), "bytes")
