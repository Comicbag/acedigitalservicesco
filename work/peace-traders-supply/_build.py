#!/usr/bin/env python3
"""Peace Traders Supply: full multi page site generator.
Every visible fact is sourced (Instagram captions, Google listing, Facebook posts, ATF list, NJSP FAQ)
or wrapped in a visible [Confirm with Kyle: ...] placeholder. No dashes in visible copy."""
import json, os, re, html, time

W = os.path.expanduser("~/ace-sites-v3/acedigitalservicesco-clone/work/peace-traders-supply")
V = str(int(time.time()))[-6:]
BASE = "https://acedigitalservicesco.com/work/peace-traders-supply/"
PHONE_TEL = "tel:+19088943943"; PHONE = "(908) 894 3943"; EMAIL = "sales@peacetradersguns.com"
IG = "https://www.instagram.com/peacetraderssupply/"; FB = "https://www.facebook.com/profile.php?id=61594466365061"
MAPS = "https://www.google.com/maps/place/Peace+Traders+Supply/@40.6431431,-74.831248,17z/data=!4m6!3m5!1s0x89c38de651d5385b:0x65684cffaf1bc046!8m2!3d40.6431431!4d-74.831248!16s%2Fg%2F11zh69ydqp"
DIRECTIONS = "https://www.google.com/maps/dir/?api=1&destination=1271+US+Highway+22+East+Unit+W-1+Lebanon+NJ+08833"
NJSP_FAQ = "https://njsp.njoag.gov/firearms-faqs/"; FARS = "https://www.njportal.com/NJSP/fars"
RVTA = "https://www.roundvalleytroutassociation.com/"

def esc(s): return html.escape(s, quote=True)
def slug_confirm(text): return f'<span class="todo">[Confirm with Kyle: {esc(text)}]</span>'

# ---------- the 17 posts (verbatim captions in captures/ig/posts*.tsv) ----------
POSTS = [
 dict(code="DdXRdUEGqW-", kind="p", date="September 16, 2026", cat="aows", title="Heckler & Koch SP5K AOW", spec="9mm, UTG Pro monolithic handguard, B&T telescopic brace, Gearhead Works Mod 1C", w=1000, h=1333),
 dict(code="DdT1WsIREtA", kind="p", date="September 15, 2026", cat="aows", title="Palmetto State Armory Sabre Enhanced Mixtape Vol. 1", spec="8 inch, 300 BLK, Maxim Defense CQB brace, Magpul M-Lok SVG", w=1000, h=1333),
 dict(code="DdEgNZ5x-Wi", kind="p", date="September 9, 2026", cat="rifles", title="Henry Big Boy Hush", spec=".357 Mag / .38 Spl, threaded carbon fiber barrel", w=1000, h=1000),
 dict(code="Dc4kp1-vjOm", kind="p", date="September 4, 2026", cat="aows", title="Palmetto State Armory Sabre Enhanced AOW", spec="300 BLK, Maxim Defense CQB brace", w=1000, h=1000),
 dict(code="Dc3irtyR5O7", kind="reel", date="September 4, 2026", cat="handguns", title="Kimber 1911 DS Warrior Stealth", spec="9mm, Hillbilly223 Cerakote, Vortex Venom 3 MOA enclosed dot", w=1000, h=1778),
 dict(code="Dc1Ix8jRLuJ", kind="reel", date="September 3, 2026", cat="handguns", title="Stealth Arms 1911 Platypus", spec="Integrated comp, takes Glock mags, Trijicon SRO, SureFire X300U", w=1000, h=1778),
 dict(code="Dc0-NPNxL9_", kind="p", date="September 3, 2026", cat="handguns", title="Stealth Arms 1911 Platypus", spec="Integrated comp with Acro cut, takes Glock mags", w=1000, h=1000),
 dict(code="DczYaaIPqZT", kind="p", date="September 2, 2026", cat="aows", title="Heckler & Koch SP5K AOW", spec="9mm, green, Midwest Industries handguard and optic mount, Holosun HE515CT, SB Tactical brace", w=1000, h=1000),
 dict(code="Dcy-dzMP2eC", kind="p", date="September 2, 2026", cat="aows", title="Palmetto State Armory AK V AOW", spec="9mm, Soviet Arms, EOTech EXPS3", w=1000, h=1000),
 dict(code="Dcr1mKTPlxU", kind="p", date="August 30, 2026", cat="aows", title="Heckler & Koch MR556 A4", spec="11 inch, Non NFA Other, SB Tactical SBA6 brace", w=1000, h=1256),
 dict(code="DcrzsPZPohv", kind="p", date="August 30, 2026", cat="aows", title="Daniel Defense DD4 MK18, a pair", spec="Left: Non NFA Other with SureFire SOCOM 3 prong. Right: AOW", w=1000, h=1241),
 dict(code="DcnoGn8vDez", kind="p", date="August 29, 2026", cat="aows", title="Springfield Armory Kuna AOW", spec="9mm", w=1000, h=1000),
 dict(code="Dcl7jJCvZo7", kind="p", date="August 28, 2026", cat="aows", title="Geissele Super Duty Mod 1", spec="11.5 inch, 5.56, Non NFA Other", w=1000, h=1191),
 dict(code="Dcj8qa8PIIk", kind="p", date="August 27, 2026", cat="aows", title="Sig Sauer MPX K AOW", spec="9mm", w=1000, h=1000),
 dict(code="Dci9TgARWbN", kind="p", date="August 27, 2026", cat="aows", title="Q Honey Badger AOW", spec="5.56, Die Free Co Kung Fu grip", w=1000, h=1333),
 dict(code="DcW3MBTvxH8", kind="reel", date="August 22, 2026", cat="handguns", title="Beretta 92G Elite LTT II", spec="Langdon Tactical, Trijicon RMR HD, SureFire X300", w=1000, h=1778),
 dict(code="DcWqzI-Puvf", kind="reel", date="August 22, 2026", cat="handguns", title="Kimber 2K11 Pro Comp", spec="9mm, Holosun 507 Comp", w=1000, h=1778),
 dict(code="DcWqa4pv3Zj", kind="reel", date="August 22, 2026", cat="handguns", title="Smith & Wesson 629", spec=".44 Magnum revolver", w=1000, h=1778),
]
for p in POSTS:
    p["url"] = f"https://www.instagram.com/{'reel' if p['kind']=='reel' else 'p'}/{p['code']}/"
    p["img"] = f"assets/{p['code']}-1000.webp"
    p["img2x"] = f"assets/{p['code']}-1600.webp" if os.path.exists(f"{W}/assets/{p['code']}-1600.webp") else None
BY = {p["code"]: p for p in POSTS}
MONTHS = {"January":"Jan","February":"Feb","March":"Mar","April":"Apr","May":"May","June":"Jun","July":"Jul","August":"Aug","September":"Sep","October":"Oct","November":"Nov","December":"Dec"}
def sd(d):
    m = re.match(r"(\w+) (\d+), (\d{4})", d); return f"{MONTHS[m.group(1)]} {m.group(2)}"
CATS = {
 "handguns": dict(name="Handguns", path="firearms/handguns/", blurb="Pistols and revolvers. Every handgun in New Jersey needs its own Permit to Purchase."),
 "rifles": dict(name="Rifles", path="firearms/rifles/", blurb="Lever actions and long guns. A Firearms Purchaser ID Card covers the purchase."),
 "shotguns": dict(name="Shotguns", path="firearms/shotguns/", blurb="Field and defensive shotguns."),
 "aows": dict(name="AOWs and Others", path="firearms/aows-and-others/", blurb="Short configurations built as AOWs or Non NFA Others. The shop's specialty."),
 "ammo": dict(name="Ammo", path="firearms/ammo/", blurb="It says Guns and Ammo on the sign."),
 "optics": dict(name="Optics and Accessories", path="firearms/optics-and-accessories/", blurb="What the builds in the case wear: Trijicon, Holosun, EOTech, Vortex, SureFire, SB Tactical."),
}
BRANDS = ["Heckler &amp; Koch", "Sig Sauer", "Daniel Defense", "Geissele", "Kimber", "Beretta", "Smith &amp; Wesson", "Springfield Armory", "Henry", "Q", "Palmetto State Armory", "Stealth Arms", "Langdon Tactical", "Trijicon", "EOTech", "Holosun", "Vortex", "SureFire", "SB Tactical", "Maxim Defense", "Midwest Industries", "Magpul"]

# ---------- building blocks ----------
def photo(p, rel, cls="", sizes="(max-width: 900px) 100vw, 50vw", eager=False):
    label = p["title"]; cap = f'{p["title"]}. {p["spec"]}. Posted {p["date"]} on Instagram.'
    src = rel + p["img"]; srcset = f'{src} 1000w' + (f', {rel + p["img2x"]} 1600w' if p.get("img2x") else '')
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    reel = '<span class="reel-tag">Reel</span>' if p["kind"] == "reel" else ''
    return (f'<a class="ph {cls}" href="{rel + (p["img2x"] or p["img"])}" data-lb data-cap="{esc(cap)}" aria-label="Enlarge photo: {esc(label)}" style="aspect-ratio:{p["w"]}/{p["h"]}">'
            f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{p["w"]}" height="{p["h"]}" alt="{esc(label)}, photographed in the shop" {load} decoding="async">{reel}</a>')

def item(p, rel, i=0, big=False):
    link_label = "Watch the reel on Instagram" if p["kind"] == "reel" else "See the post on Instagram"
    return f'''
      <figure class="item{' item-big' if big else ''} reveal" style="--i:{i}" data-cat="{p["cat"]}">
        {photo(p, rel, "item-ph", "(max-width: 640px) 100vw, (max-width: 1100px) 50vw, 33vw")}
        <figcaption>
          <p class="kicker">Posted {sd(p["date"])}</p>
          <h3>{esc(p["title"])}</h3>
          <p class="spec">{esc(p["spec"])}</p>
          <a class="textlink" href="{p["url"]}" target="_blank" rel="noopener">{link_label}</a>
        </figcaption>
      </figure>'''

def masonry(posts, rel):
    return '<div class="masonry">' + "".join(item(p, rel, i % 6) for i, p in enumerate(posts)) + '</div>'

def confirm_block(title, lines):
    lis = "".join(f"<li>{esc(l)}</li>" for l in lines)
    return f'''<aside class="confirm" aria-label="Details to confirm with the shop">
      <p class="confirm-label">To confirm with the shop</p>
      <p class="confirm-title">{esc(title)}</p>
      <ul>{lis}</ul>
    </aside>'''

def head(title, desc, rel, path, og_image="assets/DczYaaIPqZT-1600.webp", extra=""):
    canonical = BASE + path
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0e1012">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE + og_image}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE + og_image}">
<link rel="icon" type="image/png" sizes="64x64" href="{rel}assets/favicon.png?v={V}">
<link rel="apple-touch-icon" href="{rel}assets/apple-touch-icon.png?v={V}">
<link rel="preload" as="font" type="font/woff2" href="{rel}fonts/Cinzel-var.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{rel}fonts/Archivo-var.woff2" crossorigin>
<link rel="stylesheet" href="{rel}css/fonts.css?v={V}">
<link rel="stylesheet" href="{rel}css/site.css?v={V}">
<script>document.documentElement.classList.add('js')</script>
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

NAV = [("the-case/", "The case"), ("firearms/", "Firearms"), ("services/", "Services"), ("about/", "About"), ("buying-in-nj/", "Buying in NJ"), ("visit/", "Visit")]
def header(rel, current):
    links = "".join(f'<a href="{rel}{p}"{" aria-current=\"page\"" if p == current else ""}>{t}</a>' for p, t in NAV)
    return f'''<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="{rel}" aria-label="Peace Traders Supply, home"><img src="{rel}assets/logo-white.png?v={V}" width="218" height="80" alt="Peace Traders Supply"></a>
    <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn btn-accent nav-call" href="{PHONE_TEL}">Call {PHONE}</a></nav>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="main">
'''

def footer(rel, page_slug):
    cats = "".join(f'<a href="{rel}{c["path"]}">{c["name"]}</a>' for c in CATS.values())
    return f'''</main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <img src="{rel}assets/logo-white.png?v={V}" width="218" height="80" alt="Peace Traders Supply" loading="lazy">
      <p>Licensed FFL / SOT. Lebanon Plaza, 1271 US Highway 22 East, Unit W-1, Lebanon, NJ 08833.</p>
      <p><a href="{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="foot-hours">Tue to Fri 9 AM to 6 PM. Sat 9 AM to 5 PM. Sun 9 AM to 3 PM. Closed Monday.</p>
    </div>
    <nav class="foot-col" aria-label="Firearms"><p class="foot-h">Firearms</p>{cats}</nav>
    <nav class="foot-col" aria-label="Shop"><p class="foot-h">Shop</p><a href="{rel}the-case/">The case</a><a href="{rel}services/">Services</a><a href="{rel}about/">About</a><a href="{rel}buying-in-nj/">Buying in New Jersey</a><a href="{rel}faq/">FAQ</a><a href="{rel}visit/">Visit</a></nav>
    <nav class="foot-col" aria-label="Social"><p class="foot-h">Follow</p><a href="{IG}" target="_blank" rel="noopener">Instagram</a><a href="{FB}" target="_blank" rel="noopener">Facebook</a><a href="{MAPS}" target="_blank" rel="noopener">Google</a></nav>
    <p class="foot-note">Affiliate sponsor of the Round Valley Trout Association. Photos are the shop's own, from its Instagram and Google listing. Legal notes summarize the NJSP FAQ and ATF; confirm details in store. Site by <a href="https://acedigitalservicesco.com/" target="_blank" rel="noopener">Ace Digital</a>.</p>
  </div>
</footer>
<div class="mobile-bar" aria-label="Quick actions"><a href="{PHONE_TEL}">Call</a><a href="{DIRECTIONS}" target="_blank" rel="noopener">Directions</a></div>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Photo" hidden><button class="lb-close" id="lb-close" aria-label="Close photo">×</button><figure><img id="lb-img" src="" alt=""><figcaption id="lb-cap"></figcaption></figure></div>
<script src="{rel}app.js?v={V}" defer></script>
<script src="{rel}a11y.js?v={V}" defer></script>
<script defer src="https://mc.acedigitalservicesco.com/analytics/track.js" data-site="peace-traders-supply" data-page="{page_slug}"></script>
</body>
</html>
'''

def page_hero(title, lead, rel=None, side=None, amp=False):
    t = title.replace("&", '<span class="amp">&amp;</span>') if amp else esc(title)
    return f'''<section class="page-hero">
  <div class="wrap page-hero-in">
    <div class="page-hero-copy"><h1>{t}</h1><p class="lead">{lead}</p></div>
    {side or ''}
  </div>
</section>
'''

def cta_row(rel):
    return f'<div class="cta-row"><a class="btn btn-accent" href="{PHONE_TEL}">Call the shop</a><a class="btn btn-ghost" href="{DIRECTIONS}" target="_blank" rel="noopener">Get directions</a></div>'

STORE_JSONLD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Store","name":"Peace Traders Supply","description":"Licensed FFL and SOT gun store in Lebanon Plaza on Route 22 East in Lebanon, New Jersey.","image":"https://acedigitalservicesco.com/work/peace-traders-supply/assets/storefront-1600.webp","telephone":"+1-908-894-3943","email":"sales@peacetradersguns.com","url":"https://acedigitalservicesco.com/work/peace-traders-supply/","address":{"@type":"PostalAddress","streetAddress":"1271 US Highway 22 East, Unit W-1","addressLocality":"Lebanon","addressRegion":"NJ","postalCode":"08833","addressCountry":"US"},"geo":{"@type":"GeoCoordinates","latitude":40.6431431,"longitude":-74.831248},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"18:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"09:00","closes":"17:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Sunday","opens":"09:00","closes":"15:00"}],"sameAs":["https://www.instagram.com/peacetraderssupply/","https://www.facebook.com/profile.php?id=61594466365061"]}
</script>'''

pages = {}

# ---------------- HOME ----------------
rel = ""
from datetime import datetime as _dt
# newest four by post date, so a new entry in POSTS lands on the home page by itself
newest = sorted(POSTS, key=lambda q: _dt.strptime(q["date"], "%B %d, %Y"), reverse=True)[:4]
tiles = [
 ("handguns", BY["DcWqzI-Puvf"]), ("aows", BY["Dc4kp1-vjOm"]), ("rifles", BY["DdEgNZ5x-Wi"]), ("shotguns", None), ("ammo", None), ("optics", BY["DcW3MBTvxH8"]),
]
counts = {k: sum(1 for p in POSTS if p["cat"] == k) for k in CATS}

_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
def nword(n):
    """Numbers in prose are written out and computed from POSTS, so a new post never leaves a stale count."""
    if n < 20: return _ONES[n]
    t, o = divmod(n, 10)
    return _TENS[t] + ("" if o == 0 else " " + _ONES[o])
def tile(key, p, rel):
    c = CATS[key]; n = counts.get(key, 0)
    count = f'<span class="tile-count">{n} in the case</span>' if n else '<span class="tile-count">Ask at the counter</span>'
    if p:
        media = f'<img src="{rel}{p["img"]}" width="{p["w"]}" height="{p["h"]}" alt="{esc(p["title"])}" loading="lazy" decoding="async">'
    else:
        media = f'<div class="tile-type" aria-hidden="true">{c["name"][0]}</div>'
    return f'<a class="tile tile-{key} reveal" href="{rel}{c["path"]}"><div class="tile-media">{media}</div><div class="tile-copy"><h3>{c["name"]}</h3>{count}</div></a>'
home = head("Peace Traders Supply | Guns and Ammo, Lebanon Plaza, Lebanon NJ",
            "Licensed FFL and SOT gun store in Lebanon Plaza on Route 22 East, Lebanon NJ. Handguns, rifles, AOWs and Non NFA Others, new arrivals posted on Instagram.",
            rel, "", extra=f'<link rel="preload" as="image" href="assets/DczYaaIPqZT-1000.webp" imagesrcset="assets/DczYaaIPqZT-1000.webp 1000w, assets/DczYaaIPqZT-1600.webp 1600w" imagesizes="(max-width: 900px) 100vw, 560px">\n' + STORE_JSONLD)
home += header(rel, "")
sp5k = BY["DczYaaIPqZT"]
home += f'''<section class="hero" aria-labelledby="hero-h" data-video="assets/hero.mp4?v={V}">
  <img class="hero-mark" src="assets/monogram-white.png?v={V}" width="429" height="522" alt="" aria-hidden="true" decoding="async">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <a class="rating" href="{MAPS}" target="_blank" rel="noopener" aria-label="Rated 5.0 on Google. Open the Google listing"><span class="stars" aria-hidden="true">★★★★★</span><span>5.0 on Google</span></a>
      <h1 id="hero-h">Guns <span class="amp">&amp;</span> Ammo.</h1>
      <p class="hero-sub">Lebanon Plaza, Route 22 East, Lebanon, New Jersey. Licensed FFL and SOT dealer. New arrivals posted on Instagram most days.</p>
      {cta_row(rel)}
    </div>
    <figure class="hero-photo">
      <div class="hero-media">{photo(sp5k, rel, "hero-ph", "(max-width: 900px) 100vw, 560px", True)}</div>
      <figcaption><span class="kicker">In the case</span><a class="textlink" href="{sp5k["url"]}" target="_blank" rel="noopener">Heckler &amp; Koch SP5K AOW, see the post</a></figcaption>
    </figure>
  </div>
</section>
<section class="brand-band" aria-label="Peace Traders Supply"><div class="wrap"><img src="assets/brand-lockup.png?v={V}" width="1425" height="522" alt="Peace Traders Supply" loading="lazy" decoding="async"></div></section>
<section class="brands" aria-label="Brands seen in the case">
  <div class="wrap"><p class="kicker center">Seen in the case since August 22</p></div>
  <div class="marquee" aria-hidden="true"><div class="marquee-track">{"".join(f"<span>{b}</span>" for b in BRANDS)}{"".join(f"<span>{b}</span>" for b in BRANDS)}</div></div>
  <ul class="brands-static">{"".join(f"<li>{b}</li>" for b in BRANDS)}</ul>
</section>
<section class="browse" aria-labelledby="browse-h">
  <div class="wrap">
    <div class="sec-head reveal"><h2 id="browse-h">Browse by type.</h2><p>Six ways into the case. Counts are what the shop has posted since it opened.</p></div>
    <div class="tiles">{"".join(tile(k, p, rel) for k, p in tiles)}</div>
  </div>
</section>
<section class="latest" aria-labelledby="latest-h">
  <div class="wrap">
    <div class="sec-head reveal"><h2 id="latest-h">New in the case.</h2><p>The four most recent posts. Inventory moves, so call to confirm what is still here.</p></div>
    <div class="masonry masonry-4">{"".join(item(p, rel, i) for i, p in enumerate(newest))}</div>
    <p class="more reveal"><a class="btn btn-ghost" href="the-case/">See everything in the case</a></p>
  </div>
</section>
<section class="aow-teaser" aria-labelledby="aowt-h">
  <div class="wrap aow-grid">
    <div class="aow-copy reveal">
      <h2 id="aowt-h">AOWs <span class="amp">&amp;</span> Others.</h2>
      <p class="lead">{nword(counts['aows']).capitalize()} of the shop's posts are AOW or Non NFA Other builds, the short configurations New Jersey buyers ask about most. As a licensed SOT, Peace Traders can sell and transfer AOWs in store.</p>
      <div class="cta-row"><a class="btn btn-accent" href="firearms/aows-and-others/">See the AOWs and Others</a><a class="btn btn-ghost" href="buying-in-nj/">How buying works in NJ</a></div>
    </div>
    <figure class="aow-photo reveal" style="--i:1">{photo(BY["DcrzsPZPohv"], rel, "aow-ph")}<figcaption><span class="kicker">Posted Aug 30</span><a class="textlink" href="{BY["DcrzsPZPohv"]["url"]}" target="_blank" rel="noopener">Daniel Defense DD4 MK18 pair, see the post</a></figcaption></figure>
  </div>
</section>
<section class="community" aria-labelledby="comm-h">
  <div class="wrap community-in">
    <div class="community-copy reveal">
      <h2 id="comm-h">Part of the outdoor community.</h2>
      <blockquote>“This brand-new firearms dealer in Lebanon, New Jersey, is already supporting the Round Valley Trout Association and the outdoor community. We can’t believe how polished and professional you look, already your store is sharp, your setup is strong, and you’re just getting started.”</blockquote>
      <p class="attrib">Round Valley Trout Association, welcoming Peace Traders Supply as an affiliate sponsor. <a href="{RVTA}" target="_blank" rel="noopener">roundvalleytroutassociation.com</a></p>
    </div>
    <div class="community-mark reveal" style="--i:1"><img src="assets/rvta-logo.png?v={V}" width="400" height="400" alt="Round Valley Trout Association" loading="lazy" decoding="async"><span class="kicker">Affiliate sponsor</span></div>
  </div>
</section>
<section class="reviews" id="reviews" aria-labelledby="rev-h">
  <div class="wrap">
    <div class="sec-head center reveal"><h2 id="rev-h">5.0 on Google.</h2><p><span class="stars" aria-hidden="true">★★★★★</span> 2 reviews, both five stars.</p></div>
    <div class="rev-grid">
      <article class="rev reveal" style="--i:0"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div><blockquote>“Great place!!”</blockquote><div class="who"><span class="avatar" aria-hidden="true">J</span><div><strong>Jeff B</strong><small>✓ Google review</small></div></div></article>
      <article class="rev reveal" style="--i:1"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div><blockquote>Left a five star rating.</blockquote><div class="who"><span class="avatar" aria-hidden="true">E</span><div><strong>Erik Doyle</strong><small>✓ Google review</small></div></div></article>
      <article class="rev rev-cta reveal" style="--i:2"><p>Been in? Tell people what it was like.</p><a class="btn btn-ghost" href="{MAPS}" target="_blank" rel="noopener">Review on Google</a></article>
    </div>
  </div>
</section>
<section class="visit-strip" aria-labelledby="vs-h">
  <img class="visit-bg" src="assets/storefront-1600.webp" width="1600" height="838" alt="" aria-hidden="true" loading="lazy" decoding="async">
  <div class="wrap visit-strip-in">
    <div class="visit-panel reveal">
      <h2 id="vs-h">Visit the shop.</h2>
      <address>Lebanon Plaza<br>1271 US Highway 22 East, Unit W-1<br>Lebanon, NJ 08833</address>
      <table class="hours" aria-label="Hours"><tbody><tr><th scope="row">Monday</th><td>Closed</td></tr><tr><th scope="row">Tuesday to Friday</th><td>9 AM to 6 PM</td></tr><tr><th scope="row">Saturday</th><td>9 AM to 5 PM</td></tr><tr><th scope="row">Sunday</th><td>9 AM to 3 PM</td></tr></tbody></table>
      <div class="cta-row"><a class="btn btn-accent" href="{DIRECTIONS}" target="_blank" rel="noopener">Get directions</a><a class="btn btn-ghost" href="visit/">Everything about visiting</a></div>
    </div>
  </div>
</section>
'''
home += footer(rel, "home")
pages["index.html"] = home

# ---------------- THE CASE ----------------
rel = "../"
chips = [("all", "Everything", len(POSTS)), ("handguns", "Handguns", counts["handguns"]), ("rifles", "Rifles", counts["rifles"]), ("aows", "AOWs and Others", counts["aows"])]
case = head("The case | Peace Traders Supply, Lebanon NJ", "Every firearm Peace Traders Supply has posted since opening: handguns, rifles, AOWs and Non NFA Others, with the shop's own photos.", rel, "the-case/")
case += header(rel, "the-case/")
case += page_hero("The case.", f"Everything the shop has posted since August 22, {nword(len(POSTS))} firearms so far. Tap a type to narrow it down. Inventory moves, so <a href=\"{PHONE_TEL}\">call</a> to confirm what is still in the case.")
case += '<section class="catalog"><div class="wrap">'
case += '<div class="chips" role="group" aria-label="Filter by type">' + "".join(f'<button class="chip{" is-on" if k=="all" else ""}" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{n} <span>{c}</span></button>' for k, n, c in chips) + '</div>'
case += masonry(POSTS, rel)
case += f'<p class="case-foot reveal">Follow <a href="{IG}" target="_blank" rel="noopener">@peacetraderssupply</a> for new arrivals, or <a href="{PHONE_TEL}">call the shop</a> about anything you do not see here.</p></div></section>'
case += footer(rel, "the-case")
pages["the-case/index.html"] = case

# ---------------- FIREARMS (tiles) ----------------
fire = head("Firearms by type | Peace Traders Supply", "Browse Peace Traders Supply by type: handguns, rifles, shotguns, AOWs and Others, ammo, optics and accessories.", rel, "firearms/")
fire += header(rel, "firearms/")
fire += page_hero("Firearms by type.", "Pick a lane. Each page shows what the shop has posted in that category and what to bring to buy it in New Jersey.")
fire += '<section class="browse"><div class="wrap"><div class="tiles tiles-big">' + "".join(tile(k, p, rel) for k, p in tiles) + '</div></div></section>'
fire += footer(rel, "firearms")
pages["firearms/index.html"] = fire

# ---------------- CATEGORY PAGES ----------------
rel2 = "../../"
def category_page(key, intro_html, confirm, nj_note, extra_html=""):
    c = CATS[key]; posts = [p for p in POSTS if p["cat"] == key]
    pg = head(f"{c['name']} | Peace Traders Supply, Lebanon NJ", f"{c['name']} at Peace Traders Supply in Lebanon Plaza, Lebanon NJ. {c['blurb']}", rel2, c["path"])
    pg += header(rel2, "firearms/")
    pg += page_hero(c["name"] + ".", intro_html, amp=False)
    pg += '<section class="catalog"><div class="wrap">'
    if posts:
        pg += f'<p class="count-line reveal">{len(posts)} posted since the shop opened.</p>' + masonry(posts, rel2)
    else:
        pg += '<div class="empty reveal"><p>Nothing in this category has been posted yet. That does not mean it is not in the case.</p>' + cta_row(rel2) + '</div>'
    pg += extra_html
    pg += f'<div class="two-col">{confirm_block(*confirm)}<aside class="nj-note"><p class="confirm-label">New Jersey</p><p>{nj_note}</p><a class="textlink" href="{rel2}buying-in-nj/">Read the buying guide</a></aside></div>'
    pg += f'<p class="case-foot reveal">Not in the case? <a href="{PHONE_TEL}">Call the shop</a>. ' + slug_confirm("special orders and how long they take") + '</p></div></section>'
    pg += footer(rel2, "firearms-" + key)
    pages[c["path"] + "index.html"] = pg

category_page("handguns",
    "Six handguns posted so far, from a 2K11 with a comp to a .44 Magnum revolver. Each handgun sale in New Jersey runs on its own Permit to Purchase.",
    ("Handgun inventory", ["Brands regularly stocked, beyond what has been posted", "Whether the Kimber, Beretta and Stealth Arms pieces above are still in the case", "Layaway or deposit policy"]),
    "Each handgun needs its own electronic Permit to Purchase a Handgun, issued through FARS. Bring the permit, a valid photo ID with your residence address, and the dealer completes the NICS check at the time of transfer.")
category_page("rifles",
    "The lever action in the case is a Henry Big Boy Hush with a threaded carbon fiber barrel. The short barreled builds live on the AOWs and Others page.",
    ("Rifle inventory", ["Hunting rifles and bolt actions stocked", "Whether the Henry Big Boy Hush is still in the case", "Brands the shop can order"]),
    "A New Jersey Firearms Purchaser Identification Card is required before you can obtain a rifle or shotgun. The dealer completes the NICS check at the time of transfer.")
category_page("shotguns",
    "Nothing posted in this category yet, so this page is waiting on the shop. What it will cover: field and defensive shotguns, and what to bring to buy one.",
    ("Shotgun inventory", ["Shotguns stocked and the brands carried", "Whether the shop orders shotguns on request", "Gauges kept in stock"]),
    "A Firearms Purchaser Identification Card covers a shotgun purchase in New Jersey. The dealer completes the NICS check at the time of transfer.")
category_page("aows",
    f"{nword(counts['aows']).capitalize()} posts and counting: two SP5Ks, MPX K, Kuna, AK V, two Sabre Enhanced builds, Honey Badger, MR556 and a Geissele Super Duty, plus a matched pair of Daniel Defense DD4 MK18s. As a licensed SOT, the shop can sell and transfer AOWs in store.",
    ("AOW and Other builds", ["Whether the builds above were configured in house", "Turnaround on an AOW transfer", "Braces, handguards and optics available for a custom configuration"]),
    "An AOW is an NFA item: the transfer runs on an ATF Form 4. The federal transfer tax on an AOW dropped to zero on January 1, 2026, though the registration and ATF approval still apply. A Non NFA Other is configured to stay outside the National Firearms Act, so no stamp is involved. New Jersey still requires your Firearms Purchaser Identification Card or Permit to Purchase as the item requires.",
    extra_html='''<section class="glossary-wrap reveal"><h2>Three terms, in plain words.</h2><dl class="glossary">
      <div><dt>AOW</dt><dd>Any other weapon, a category under the National Firearms Act. The federal transfer tax on an AOW dropped to <strong>zero</strong> on January 1, 2026. The ATF paperwork and approval still apply.</dd></div>
      <div><dt>Non NFA Other</dt><dd>A firearm configured to stay outside the National Firearms Act, so no tax stamp is involved.</dd></div>
      <div><dt>SOT</dt><dd>Special Occupational Taxpayer. Peace Traders Supply is a licensed SOT, so AOWs can be sold and transferred in store.</dd></div>
    </dl></section>''')
category_page("ammo",
    "It says Guns and Ammo on the sign. The shop has not posted its ammo shelf yet, so this page is a frame waiting for calibers and brands.",
    ("Ammo", ["Calibers kept in stock (9mm, 5.56, .300 BLK, .357 and .44 Magnum would match the case)", "Brands carried and whether bulk pricing exists", "What New Jersey requires to buy ammunition at the counter"]),
    "Ammunition rules are not covered by the NJSP FAQ summarized on this site, so the shop confirms what to bring at the counter.")
opt_brands = ["Trijicon SRO and RMR HD", "Holosun HE515CT and 507 Comp", "EOTech EXPS3", "Vortex Venom", "SureFire X300, X300U and SOCOM 3 prong", "SB Tactical braces", "Maxim Defense CQB brace", "Midwest Industries handguards and mounts", "Magpul furniture", "Langdon Tactical work on the Beretta", "Die Free Co Kung Fu grip", "Hillbilly223 Cerakote on the Kimber DS Warrior"]
category_page("optics",
    "Every build the shop posts wears something: enclosed dots, weapon lights, braces, handguards. This is what has been seen in the case, by name.",
    ("Optics and accessories", ["Which of these are sold separately versus mounted on a build", "Mounting and zeroing service and its price", "Brands the shop can order"]),
    "Optics and accessories are not firearms under New Jersey law, but braces and magazines have their own rules: magazines are limited to 10 rounds for most owners.",
    extra_html='<section class="seen reveal"><h2>Seen on builds in the case.</h2><ul class="seen-list">' + "".join(f"<li>{b}</li>" for b in opt_brands) + '</ul></section>')

# ---------------- SERVICES ----------------
rel = "../"
svc = head("Services | Peace Traders Supply, Lebanon NJ", "What Peace Traders Supply does beyond the case: AOW and NFA transfers as a licensed SOT, Non NFA Other builds, transfers, special orders and help with New Jersey permits.", rel, "services/")
svc += header(rel, "services/")
svc += page_hero("Services.", "What the shop does beyond the case. The first three are on the record; the rest are marked for Kyle to confirm.")
def service(title, body, sourced=True, i=0):
    tag = '<span class="src-tag">On the record</span>' if sourced else '<span class="src-tag src-tag-todo">To confirm</span>'
    return f'<article class="service reveal" style="--i:{i}"><div class="service-head"><h2>{title}</h2>{tag}</div><p>{body}</p></article>'
svc += '<section class="services"><div class="wrap"><div class="service-list">'
svc += service("AOW and NFA transfers", "Peace Traders Supply is a licensed SOT, so AOWs can be sold and transferred in store. An AOW transfer runs on an ATF Form 4. The federal transfer tax dropped to zero on January 1, 2026, and ATF approval is still required.", True, 0)
svc += service("Non NFA Others", "Short configurations built to stay outside the National Firearms Act, like the MR556, the Geissele Super Duty and one of the Daniel Defense MK18s in the case. No tax stamp involved.", True, 1)
svc += service("New Jersey permit guidance", "Firearms Purchaser ID Cards and handgun permits are applied for online through FARS with your local police department. The shop runs the NICS check at the time of transfer. " + f'<a class="textlink" href="{rel}buying-in-nj/">Read the guide</a>.', True, 2)
svc += service("FFL transfers", "A firearm bought online or out of state has to ship to a licensed New Jersey dealer. " + slug_confirm("transfer fee and what to bring"), False, 3)
svc += service("Special orders", "If it is not in the case, the shop can look for it. " + slug_confirm("how special orders work and typical lead time"), False, 4)
svc += service("Custom finishes and mounting", "The Kimber DS Warrior in the case wears a Hillbilly223 Cerakote, and every posted build arrives with its optic and light mounted. " + slug_confirm("Cerakote, optic mounting and zeroing offered through the shop"), False, 5)
svc += service("Gunsmithing", slug_confirm("gunsmithing work offered in house (a directory listing mentions it, the shop has not)"), False, 6)
svc += '</div>' + cta_row(rel) + '</div></section>'
svc += footer(rel, "services")
pages["services/index.html"] = svc

# ---------------- ABOUT ----------------
about = head("About | Peace Traders Supply, Lebanon NJ", "Peace Traders Supply opened in summer 2026 in Lebanon Plaza on Route 22 East: a licensed FFL and SOT gun store with a glass case, white slatwall and an acid stained floor.", rel, "about/", og_image="assets/storefront-1600.webp")
about += header(rel, "about/")
about += page_hero("A new counter on Route 22.", "Peace Traders Supply opened in the summer of 2026 in Lebanon Plaza, Lebanon, New Jersey, as a licensed FFL and SOT dealer.")
about += f'''<section class="about">
  <div class="wrap about-grid">
    <figure class="about-photo reveal"><a class="ph" href="{rel}assets/storefront-1600.webp" data-lb data-cap="Peace Traders Supply in Lebanon Plaza, from the shop's Google listing." aria-label="Enlarge photo: the storefront" style="aspect-ratio:1600/838"><img src="{rel}assets/storefront-960.webp" srcset="{rel}assets/storefront-960.webp 960w, {rel}assets/storefront-1600.webp 1600w" sizes="(max-width: 900px) 100vw, 60vw" width="960" height="503" alt="Peace Traders Supply storefront in Lebanon Plaza with the Guns and Ammo sign" loading="lazy" decoding="async"></a><figcaption>Unit W-1, under the Guns and Ammo sign. The shop's first Instagram post, June 18, 2026.</figcaption></figure>
    <div class="about-copy reveal" style="--i:1">
      <h2>The shop.</h2>
      <p>Two thousand one hundred square feet in the west building of Lebanon Plaza, just off Interstate 78 at exit 20A. Inside: a long glass case, white slatwall behind it, and an acid stained concrete floor finished in Espresso and Beechnut by a Hunterdon County flooring contractor before the doors opened.</p>
      <p>The license is a Type 07 FFL with SOT status, which is why the case leans toward AOWs and Non NFA Others alongside the handguns and long guns.</p>
      <p>{slug_confirm("the story in your words: how Peace Traders started, why Lebanon, what you want the shop known for")}</p>
    </div>
  </div>
</section>
<section class="about-people">
  <div class="wrap two-col">
    <div class="reveal"><h2>Who you will meet.</h2><p>Kyle Quick is the shop's contact. {slug_confirm("title, a short bio and a photo for this page")}</p></div>
    <div class="reveal" style="--i:1"><h2>What the shop posts.</h2><p>{nword(len(POSTS) + 1).capitalize()} posts of its own since June 18, 2026: {nword(len(POSTS))} firearms and the storefront. New arrivals go up on Instagram most days, with the brand, the caliber and what is mounted on it.</p><p><a class="textlink" href="{IG}" target="_blank" rel="noopener">Instagram</a><br><a class="textlink" href="{FB}" target="_blank" rel="noopener">Facebook</a></p></div>
  </div>
</section>
<section class="community" aria-labelledby="comm2-h">
  <div class="wrap community-in">
    <div class="community-copy reveal">
      <h2 id="comm2-h">Affiliate sponsor, Round Valley Trout Association.</h2>
      <blockquote>“A big thank-you to a brand new affiliate sponsor, PEACE TRADERS SUPPLY! This brand-new firearms dealer in Lebanon, New Jersey, is already supporting the Round Valley Trout Association and the outdoor community. We can’t believe how polished and professional you look, already your store is sharp, your setup is strong, and you’re just getting started. Welcome to the family we’re excited to see you grow.”</blockquote>
      <p class="attrib">Round Valley Trout Association, on Facebook. The association has supplemented the trout stocking of Round Valley Reservoir since 1980. <a href="{RVTA}" target="_blank" rel="noopener">roundvalleytroutassociation.com</a></p>
    </div>
    <div class="community-mark reveal" style="--i:1"><img src="{rel}assets/rvta-logo.png?v={V}" width="400" height="400" alt="Round Valley Trout Association" loading="lazy" decoding="async"><span class="kicker">Affiliate sponsor</span></div>
  </div>
</section>
<section class="about-gallery"><div class="wrap"><div class="sec-head reveal"><h2>Inside.</h2><p>The case, the slatwall and the floor, as the shop photographs them.</p></div>
  <div class="masonry masonry-4">{"".join(item(BY[c], rel, i) for i, c in enumerate(["DczYaaIPqZT", "Dcr1mKTPlxU", "DcW3MBTvxH8", "DdEgNZ5x-Wi"]))}</div></div></section>
'''
about += footer(rel, "about")
pages["about/index.html"] = about

# ---------------- BUYING IN NJ ----------------
nj = head("Buying a firearm in New Jersey | Peace Traders Supply", "The New Jersey State Police rules in plain words: the Firearms Purchaser ID Card, handgun permits through FARS, the NICS check, what ID to bring, transfers, private sales, magazines and more.", rel, "buying-in-nj/")
nj += header(rel, "buying-in-nj/")
nj += page_hero("Buying a firearm in New Jersey.", f"The New Jersey State Police rules, summarized from the official FAQ. The shop confirms current requirements when you visit. Source: <a href=\"{NJSP_FAQ}\" target=\"_blank\" rel=\"noopener\">NJSP firearms FAQ</a>.")
steps = [
 ("Get your Firearms Purchaser ID Card.", "New Jersey requires a Firearms Purchaser Identification Card before you can obtain a rifle or shotgun. Apply online through FARS with your local police department."),
 ("Handguns need a permit for each one.", "Each handgun needs its own electronic Permit to Purchase a Handgun, also issued through FARS."),
 ("The dealer runs your NICS check.", "Firearm transactions in New Jersey require a NICS background check completed by a licensed dealer at the time of transfer."),
]
nj += '<section class="steps-wrap"><div class="wrap"><ol class="steps">' + "".join(f'<li class="reveal" style="--i:{i}"><h2>{t}</h2><p>{d}</p></li>' for i, (t, d) in enumerate(steps)) + f'</ol><div class="nj-links reveal"><a class="btn btn-ghost" href="{FARS}" target="_blank" rel="noopener">Apply through FARS</a><a class="textlink" href="{NJSP_FAQ}" target="_blank" rel="noopener">Read the full NJSP FAQ</a></div></div></section>'
rules = [
 ("What ID to bring", "The identification document presented by the person receiving the firearm must have their photograph, name, residence address and date of birth. A P.O. box is not accepted as an address."),
 ("Bought online or out of state?", "It is illegal to buy a firearm out of state and bring it home; the purchase goes through a licensed dealer in New Jersey. Firearms may only be shipped to a licensed dealer, or to yourself at another residence."),
 ("Private sales", "Person to person transfers are only eligible to be executed if both individuals reside in New Jersey, and the sale still runs through the permit and NICS process."),
 ("Moving to New Jersey", "New residents register their handguns within 60 days of moving in."),
 ("Magazines", "Large capacity magazines are illegal for most owners. The limit is 10 rounds."),
 ("Hollow points", "Legal to possess at home, on your land and at the range. Not for concealed carry."),
 ("Inherited firearms", "No permit is required to inherit a firearm, as long as the firearm is legal to possess in New Jersey."),
 ("Transporting a firearm", "Unloaded, in a locked case or the trunk, while traveling to and from the range or the shop. Federal law covers interstate travel the same way: unloaded and locked."),
]
nj += '<section class="rules"><div class="wrap"><div class="sec-head reveal"><h2>The rest of the rules, short.</h2><p>Each line is a summary of an NJSP FAQ answer, not legal advice.</p></div><div class="rule-grid">' + "".join(f'<article class="rule reveal" style="--i:{i%4}"><h3>{t}</h3><p>{d}</p></article>' for i, (t, d) in enumerate(rules)) + '</div>'
nj += confirm_block("At the counter", ["Whether the shop helps first time buyers start a FARS application in store", "The shop's ORI number, if customers should enter it on the application", "What to bring for ammunition purchases"]) + '</div></section>'
nj += footer(rel, "buying-in-nj")
pages["buying-in-nj/index.html"] = nj

# ---------------- FAQ ----------------
faq = head("FAQ | Peace Traders Supply, Lebanon NJ", "Hours, parking, what to bring, AOWs and Others, transfers and special orders at Peace Traders Supply in Lebanon Plaza.", rel, "faq/")
faq += header(rel, "faq/")
faq += page_hero("Questions.", "The short answers. Anything marked to confirm is waiting on the shop.")
qa = [
 ("When are you open?", "Tuesday to Friday 9 AM to 6 PM, Saturday 9 AM to 5 PM, Sunday 9 AM to 3 PM. Closed Monday.", True),
 ("Where do I park?", "In front of the store in Lebanon Plaza, in the customer parking spots. The lot exits to the rear.", True),
 ("Where exactly are you?", "Unit W-1 in Lebanon Plaza, 1271 US Highway 22 East, Lebanon, NJ 08833, under the Guns and Ammo sign, just off Interstate 78 at exit 20A.", True),
 ("What is an AOW, and can I buy one here?", "Any other weapon, a category under the National Firearms Act, transferred on an ATF Form 4. The federal transfer tax dropped to zero on January 1, 2026, though ATF approval is still required. Peace Traders Supply is a licensed SOT, so AOWs can be sold and transferred in store.", True),
 ("What do I bring to buy a handgun?", "Your electronic Permit to Purchase a Handgun from FARS, one per handgun, and a valid photo ID with your residence address. The dealer runs the NICS check at the time of transfer.", True),
 ("What do I bring to buy a rifle or shotgun?", "Your New Jersey Firearms Purchaser Identification Card and a valid photo ID with your residence address.", True),
 ("Do you accept transfers from other dealers or online sellers?", slug_confirm("transfer policy and fee"), False),
 ("Can you order something that is not in the case?", slug_confirm("special orders and lead time"), False),
 ("Do you buy or take trades?", slug_confirm("used firearms, trades and consignment"), False),
 ("Is there a range?", slug_confirm("range access, a directory listing mentions one and the shop has not"), False),
]
faq += '<section class="faq"><div class="wrap faq-wrap">' + "".join(f'<details class="qa reveal" style="--i:{i%5}"{" open" if i==0 else ""}><summary>{esc(q)}{"" if s else " <span class=\"src-tag src-tag-todo\">To confirm</span>"}</summary><div class="qa-body"><p>{a}</p></div></details>' for i, (q, a, s) in enumerate(qa)) + f'<p class="case-foot reveal">Something else? <a href="{PHONE_TEL}">Call {PHONE}</a> or <a href="mailto:{EMAIL}">email the shop</a>.</p></div></section>'
faq += footer(rel, "faq")
pages["faq/index.html"] = faq

# ---------------- VISIT ----------------
visit = head("Visit | Peace Traders Supply, Lebanon Plaza, Lebanon NJ", "Hours, address, parking and directions to Peace Traders Supply, Unit W-1, Lebanon Plaza, 1271 US Highway 22 East, Lebanon NJ 08833.", rel, "visit/", og_image="assets/storefront-1600.webp", extra=STORE_JSONLD)
visit += header(rel, "visit/")
visit += f'''<section class="visit-page">
  <div class="wrap visit-grid2">
    <div class="visit-panel reveal">
      <h1>Visit the shop.</h1>
      <address>Lebanon Plaza<br>1271 US Highway 22 East, Unit W-1<br>Lebanon, NJ 08833</address>
      <p class="visit-note">West building of the plaza, under the Guns and Ammo sign. Customer parking is in front; the lot exits to the rear. Just off Interstate 78 at exit 20A.</p>
      <table class="hours" aria-label="Hours"><tbody><tr><th scope="row">Monday</th><td>Closed</td></tr><tr><th scope="row">Tuesday to Friday</th><td>9 AM to 6 PM</td></tr><tr><th scope="row">Saturday</th><td>9 AM to 5 PM</td></tr><tr><th scope="row">Sunday</th><td>9 AM to 3 PM</td></tr></tbody></table>
      <div class="contact-rows"><a href="{PHONE_TEL}">{PHONE}</a><a href="mailto:{EMAIL}?subject=Question%20for%20Peace%20Traders%20Supply">{EMAIL}</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a><a href="{FB}" target="_blank" rel="noopener">Facebook</a></div>
      <div class="cta-row"><a class="btn btn-accent" href="{DIRECTIONS}" target="_blank" rel="noopener">Get directions</a><a class="btn btn-ghost" href="{PHONE_TEL}">Call the shop</a></div>
    </div>
    <figure class="visit-photo reveal" style="--i:1"><a class="ph" href="{rel}assets/storefront-1600.webp" data-lb data-cap="Peace Traders Supply in Lebanon Plaza, from the shop's Google listing." aria-label="Enlarge photo: the storefront" style="aspect-ratio:1600/838"><img src="{rel}assets/storefront-960.webp" srcset="{rel}assets/storefront-960.webp 960w, {rel}assets/storefront-1600.webp 1600w" sizes="(max-width: 900px) 100vw, 55vw" width="960" height="503" alt="Peace Traders Supply storefront in Lebanon Plaza with the Guns and Ammo sign" loading="lazy" decoding="async"></a><figcaption>Unit W-1, under the Guns and Ammo sign.</figcaption></figure>
  </div>
  <div class="wrap map-wrap reveal"><div class="map-frame"><iframe title="Map to Peace Traders Supply" src="https://www.google.com/maps?q=Peace+Traders+Supply+1271+US+Highway+22+East+Lebanon+NJ+08833&output=embed" width="1200" height="480" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div>
</section>
'''
visit += footer(rel, "visit")
pages["visit/index.html"] = visit

# ---------------- write + QA ----------------
bad_all = []
for path, content in pages.items():
    full = os.path.join(W, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(content)
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", content, flags=re.S); text = re.sub(r"<[^>]+>", " ", body)
    bad = [m.group(0) for m in re.finditer(r"[^\s]{0,16}[—–][^\s]{0,16}", text)]
    hy = [m.group(0) for m in re.finditer(r"\b\w+-\w+\b", text) if not re.match(r"W-1|Form\b|brand-new|thank-you|P\.O\.", m.group(0))]
    bad_all.append((path, len(content), bad, sorted(set(hy))[:8]))
for path, n, bad, hy in bad_all: print(f"{path:40s} {n:6d}B  em/en: {bad}  hyphens: {hy}")
sm = [BASE + p.replace("index.html", "") for p in pages]
open(f"{W}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc></url>" for u in sm) + "</urlset>\n")
open(f"{W}/robots.txt", "w").write("User-agent: *\nDisallow: /work/peace-traders-supply/\n")
json.dump(POSTS, open(f"{W}/assets/posts.json", "w"), indent=1)
print("pages:", len(pages), "| v", V)
