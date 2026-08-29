#!/usr/bin/env python3
"""Inspiration Audio — static site generator.

Copy is Inspiration Audio's own, carried over from inspirationaudio.org (captured
2026-08-29) at the client's request. Nothing about the studio, its gear, its
scholarship or its people is invented here. Anything unconfirmed is marked with
a TODO comment in the HTML rather than guessed at.

Run:  python3 build.py
"""
import json, os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://acedigitalservicesco.com/work/inspiration-audio/"
TODAY = "2026-08-29"

ARTISTS = json.load(open(os.path.join(HERE, "artists.json")))
GEAR = json.load(open(os.path.join(HERE, "gear.json")))

# ---------------------------------------------------------------- nav / chrome
NAV = [
    ("about.html",       "About"),
    ("artists.html",     "Artists"),
    ("gallery.html",     "Gallery"),
    ("studio.html",      "Studio"),
    ("gear.html",        "Gear"),
    ("tutorials.html",   "Tutorials"),
    ("scholarship.html", "Scholarship"),
    ("contact.html",     "Contact"),
]

ICON = {
 "spotify":'<path d="M12 2a10 10 0 100 20 10 10 0 000-20zm4.6 14.4a.62.62 0 01-.86.21c-2.35-1.44-5.3-1.76-8.8-.96a.62.62 0 11-.28-1.22c3.82-.87 7.1-.5 9.73 1.11.3.18.39.57.21.86zm1.23-2.74a.78.78 0 01-1.07.26c-2.69-1.65-6.79-2.13-9.97-1.17a.78.78 0 11-.45-1.5c3.63-1.1 8.15-.56 11.24 1.34.36.22.48.7.25 1.07zm.1-2.85C14.7 8.9 9.4 8.73 6.32 9.67a.94.94 0 11-.54-1.8c3.53-1.07 9.38-.86 13.08 1.33a.94.94 0 01-.95 1.62z"/>',
 "apple":'<path d="M16.3 12.7c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.15-2.8.85-3.5.85s-1.8-.83-3-.8c-1.5.02-2.9.9-3.7 2.25-1.6 2.75-.4 6.8 1.1 9 .75 1.1 1.6 2.3 2.8 2.25 1.1-.04 1.5-.72 2.9-.72s1.7.72 2.9.7c1.2-.02 2-1.1 2.7-2.2.85-1.25 1.2-2.5 1.22-2.55-.03-.02-2.35-.9-2.37-3.55zM14.1 5.9c.6-.75 1-1.8.9-2.85-.87.04-1.93.58-2.56 1.32-.56.65-1.05 1.72-.92 2.73.97.08 1.96-.5 2.58-1.2z"/>',
 "instagram":'<path d="M12 2.2c3.2 0 3.6 0 4.85.07 1.17.05 1.8.25 2.23.42.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.42 2.23.06 1.25.07 1.62.07 4.8s-.01 3.56-.07 4.8c-.06 1.18-.26 1.81-.42 2.24-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.43.16-1.06.36-2.23.42-1.25.06-1.63.07-4.85.07s-3.6-.01-4.85-.07c-1.17-.06-1.8-.26-2.23-.42a3.8 3.8 0 01-1.38-.9 3.8 3.8 0 01-.9-1.38c-.16-.43-.36-1.06-.42-2.24C2.21 15.56 2.2 15.2 2.2 12s.01-3.55.07-4.8c.06-1.17.26-1.81.42-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.43-.17 1.06-.37 2.23-.42C8.45 2.2 8.8 2.2 12 2.2zm0 1.8c-3.14 0-3.5.01-4.74.07-1.14.05-1.76.24-2.17.4-.55.21-.94.47-1.35.88-.41.41-.66.8-.88 1.35-.16.41-.35 1.03-.4 2.17-.05 1.24-.07 1.6-.07 4.74s.02 3.5.07 4.74c.05 1.14.24 1.76.4 2.17.22.55.47.94.88 1.35.41.41.8.66 1.35.88.41.16 1.03.35 2.17.4 1.24.05 1.6.07 4.74.07s3.5-.02 4.74-.07c1.14-.05 1.76-.24 2.17-.4.55-.22.94-.47 1.35-.88.41-.41.66-.8.88-1.35.16-.41.35-1.03.4-2.17.05-1.24.07-1.6.07-4.74s-.02-3.5-.07-4.74c-.05-1.14-.24-1.76-.4-2.17a3.6 3.6 0 00-.88-1.35 3.6 3.6 0 00-1.35-.88c-.41-.16-1.03-.35-2.17-.4C15.5 4.01 15.14 4 12 4zm0 3.06a4.94 4.94 0 110 9.88 4.94 4.94 0 010-9.88zm0 8.15a3.21 3.21 0 100-6.42 3.21 3.21 0 000 6.42zm6.3-8.35a1.16 1.16 0 11-2.31 0 1.16 1.16 0 012.31 0z"/>',
 "youtube":'<path d="M21.6 7.2s-.2-1.36-.8-1.96c-.76-.8-1.6-.8-2-.85C16 4.2 12 4.2 12 4.2h-.01s-4 0-6.8.2c-.4.04-1.24.04-2 .84-.6.6-.8 1.96-.8 1.96S2.2 8.8 2.2 10.4v1.5c0 1.6.2 3.2.2 3.2s.2 1.36.8 1.96c.76.8 1.76.77 2.2.86 1.6.15 6.8.2 6.8.2s4 0 6.8-.21c.4-.05 1.24-.05 2-.85.6-.6.8-1.96.8-1.96s.2-1.6.2-3.2v-1.5c0-1.6-.2-3.2-.2-3.2zM9.94 14.2V8.7l5.15 2.76-5.15 2.74z"/>',
 "tiktok":'<path d="M16.6 5.82A4.28 4.28 0 0115.54 3h-3.1v12.4a2.59 2.59 0 01-2.6 2.5 2.6 2.6 0 01-2.6-2.6 2.6 2.6 0 013.3-2.5v-3.13a5.7 5.7 0 00-6.4 5.63A5.7 5.7 0 009.85 21a5.7 5.7 0 005.7-5.7V9.01a7.35 7.35 0 004.3 1.38V7.3a4.3 4.3 0 01-3.25-1.48z"/>',
 "twitter":'<path d="M18.2 2.5h3.3l-7.2 8.2 8.4 11.1h-6.6l-5.2-6.8-5.9 6.8H1.7l7.7-8.8L1.4 2.5h6.8l4.7 6.2 5.3-6.2zm-1.2 17.4h1.8L7.1 4.3H5.2l11.8 15.6z"/>',
 "facebook":'<path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.52 1.5-3.91 3.77-3.91 1.1 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.78l-.45 2.91h-2.33V22c4.78-.79 8.44-4.93 8.44-9.94z"/>',
 "site":'<path d="M12 2a10 10 0 100 20 10 10 0 000-20zM4.06 13h3.02c.1 1.62.4 3.14.87 4.42A8.03 8.03 0 014.06 13zm3.02-2H4.06a8.03 8.03 0 013.9-4.42c-.48 1.28-.78 2.8-.88 4.42zm4.92-6.75c.72.7 1.5 2.42 1.73 4.75h-3.46c.23-2.33 1-4.05 1.73-4.75zM9.07 11c.1-1.5.4-2.83.83-3.86.3-.72.63-1.2.92-1.47V11H9.07zm1.75 2v5.33c-.29-.27-.62-.75-.92-1.47-.43-1.03-.73-2.36-.83-3.86h1.75zm2.36 5.33V13h1.75c-.1 1.5-.4 2.83-.83 3.86-.3.72-.63 1.2-.92 1.47zM13.18 11V5.67c.29.27.62.75.92 1.47.43 1.03.73 2.36.83 3.86h-1.75zm2.87 2h3.02a8.03 8.03 0 01-3.9 4.42c.48-1.28.78-2.8.88-4.42zm0-2c-.1-1.62-.4-3.14-.87-4.42A8.03 8.03 0 0119.94 11h-3.02z"/>',
}

SOCIAL = [
    ("instagram", "https://www.instagram.com/inspiration.audio/", "Instagram"),
    ("youtube",   "https://www.youtube.com/@inspirationaudio1676", "YouTube"),
    ("tiktok",    "https://www.tiktok.com/@inspiration.audio", "TikTok"),
    ("facebook",  "https://m.facebook.com/Inspiration.Audio", "Facebook"),
]

DONATE = "https://givebutter.com/inspiration-audio-create-opportunity"


def svg(kind, label):
    return (f'<svg viewBox="0 0 24 24" role="img" aria-label="{label}" '
            f'focusable="false">{ICON[kind]}</svg>')


def nav(active):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    items.append(f'<li><a class="navcta" href="{DONATE}" rel="noopener" target="_blank">Donate</a></li>')
    return f"""<header class="nav">
  <div class="bar">
    <a class="brand" href="index.html" aria-label="Inspiration Audio, home">
      <img src="img/logo.png" width="600" height="600" alt="Inspiration Audio">
    </a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="navmenu" aria-label="Menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" focusable="false" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav aria-label="Main"><ul id="navmenu">{''.join(items)}</ul></nav>
  </div>
</header>"""


def footer():
    soc = "".join(f'<a href="{u}" rel="noopener" target="_blank" aria-label="{l}">{svg(k,l)}</a>'
                  for k, u, l in SOCIAL)
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="grid">
      <div>
        <img class="mark" src="img/logo.png" width="600" height="600" alt="Inspiration Audio">
        <p style="max-width:30ch;font-size:.92rem">A 501(c)(3) nonprofit in Rahway, New Jersey, building a music ecosystem where creativity can thrive.</p>
        <div class="soc">{soc}</div>
      </div>
      <div>
        <h2>Make music</h2>
        <ul>
          <li><a href="studio.html">The studio</a></li>
          <li><a href="gear.html">Gear list</a></li>
          <li><a href="artists.html">IA artists</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="listen.html">Listen</a></li>
        </ul>
      </div>
      <div>
        <h2>Take part</h2>
        <ul>
          <li><a href="scholarship.html">IA Scholarship</a></li>
          <li><a href="training.html">Train as an engineer</a></li>
          <li><a href="tutorials.html">Free tutorials</a></li>
          <li><a href="events.html">Events</a></li>
          <li><a href="support.html">Support us</a></li>
        </ul>
      </div>
      <div>
        <h2>Get in touch</h2>
        <ul>
          <li><a href="tel:+19089000229">(908) 900-0229</a></li>
          <li><a href="mailto:info@inspirationaudio.org">info@inspirationaudio.org</a></li>
          <li><a href="contact.html">Contact form</a></li>
          <li><a href="team.html">Who we are</a></li>
          <li><a href="about.html">About IA</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>&copy; 2026 Inspiration Audio. A registered 501(c)(3) nonprofit organization. Rahway, NJ.</span>
      <span><a href="accessibility.html">Accessibility</a></span>
    </div>
  </div>
</footer>"""


def page(slug, title, desc, body, og="img/hero.webp", preview=True):
    banner = ('<div class="pvw"><strong>Preview build</strong> for Inspiration Audio, '
              'by Ace Digital. Not published, not indexed. Content carried from '
              'inspirationaudio.org.</div>') if preview else ""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{BASE}{'' if slug=='index.html' else slug}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Inspiration Audio">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{'' if slug=='index.html' else slug}">
<meta property="og:image" content="{BASE}{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}{og}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%230a0a0d'/%3E%3Crect x='6' y='9' width='3' height='14' fill='%23e8384f'/%3E%3Crect x='12' y='5' width='3' height='22' fill='%23f4f4f7'/%3E%3Crect x='18' y='12' width='3' height='8' fill='%23f4f4f7'/%3E%3Crect x='24' y='8' width='3' height='16' fill='%23e8384f'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800;900&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="css/site.css?v=1">
</head>
<body>
{banner}
<a class="skip" href="#main">Skip to content</a>
{nav(slug)}
<main id="main">
{body}
</main>
{footer()}
<script src="css/ui.js?v=1" defer></script>
</body>
</html>
"""
    open(os.path.join(HERE, slug), "w", encoding="utf-8").write(html)
    return slug


def phead(h1, lede, img=None, alt=""):
    if img:
        return f"""<section class="phead withimg">
  <div class="bg"><img src="{img}" alt="{alt}" fetchpriority="high" width="1600" height="1067"></div>
  <div class="wrap"><h1>{h1}</h1><p class="lede">{lede}</p></div>
</section>"""
    return f"""<section class="phead">
  <div class="wrap"><h1>{h1}</h1><p class="lede">{lede}</p></div>
</section>"""


# ================================================================== HOME
home_body = f"""
<section class="hero">
  <div class="bg"><img src="img/hero.webp" alt="A session underway in the Rahway studio, engineer at the desk under magenta light" fetchpriority="high" width="2000" height="1125"></div>
  <div class="wrap inner">
    <p class="eyebrow">501(c)(3) nonprofit &middot; Rahway, NJ</p>
    <h1>Talent is everywhere. Opportunity isn't.</h1>
    <p>A working studio that doubles as a training floor, so New Jersey musicians and engineers can build a career without the financial strain.</p>
    <div class="btns">
      <a class="btn btn-primary" href="contact.html">Book a session</a>
      <a class="btn btn-ghost" href="scholarship.html">Apply for a scholarship</a>
    </div>
  </div>
</section>

<section class="rule">
  <div class="wrap">
    <div class="split wide-left">
      <div class="rv">
        <h2>We use a professional studio as a classroom.</h2>
        <p class="narrow" style="margin-top:20px">Inspiration Audio is a nonprofit creative workforce development organization that uses professional studio operations as a platform for training, mentorship, artist development, and career readiness. Through hands-on experience, participants create professional-quality work, build technical and creative skills, and develop pathways into the modern creative economy.</p>
        <p class="narrow">From professional recording sessions and music technology programs to live events and workforce development opportunities, we are building a music ecosystem where creativity can thrive.</p>
      </div>
      <div class="rv"><p class="pull">Record here, keep every right to your music, and pay nothing you cannot afford.</p></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="track">
    <span>Recording</span><span>Mixing</span><span>Mastering</span><span>Live sound</span><span>Podcasts</span><span>Livestreams</span><span>Video editing</span><span>Dolby spatial audio</span><span>Masterclasses</span><span>Photo and video studio</span>
    <span>Recording</span><span>Mixing</span><span>Mastering</span><span>Live sound</span><span>Podcasts</span><span>Livestreams</span><span>Video editing</span><span>Dolby spatial audio</span><span>Masterclasses</span><span>Photo and video studio</span>
  </div>
</div>

<section class="tint">
  <div class="wrap">
    <h2 class="rv">Three ways in</h2>
    <div class="bento rv" style="margin-top:34px">
      <a class="panel b-3" href="artists.html" style="text-decoration:none">
        <h3>You make music</h3>
        <p>Record a project of any size without breaking the bank, and keep all the rights to it. Then use the photo and video studio to build the artwork and promo around it.</p>
        <p style="color:var(--accent-hot);font-weight:700;margin:0">See the IA artists</p>
      </a>
      <div class="panel media b-3"><img src="img/for-artists.webp" alt="Musicians tracking together in the live room" loading="lazy" width="1600" height="1067"></div>
      <div class="panel media b-2"><img src="img/for-engineers.webp" alt="An engineer working at the console" loading="lazy" width="1600" height="1067"></div>
      <a class="panel b-4" href="training.html" style="text-decoration:none">
        <h3>You want to engineer</h3>
        <p>Learn recording, mixing, mastering and live sound with your hands on real equipment, rather than paying for a degree first. Podcasts, livestreams, video editing and Dolby spatial audio are part of it, because that is what the work actually looks like now.</p>
        <p style="color:var(--accent-hot);font-weight:700;margin:0">How the training works</p>
      </a>
      <a class="panel accent b-6" href="scholarship.html" style="text-decoration:none">
        <h3>You cannot pay for any of it</h3>
        <p style="margin-bottom:0">Apply to be an IA Scholar and get everything offered to IA artists and engineers for free. Studio access, masterclasses, the photo and video studio, the performance space, and the people. All inquiries are accepted.</p>
      </a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split">
      <div class="rv">
        <h2>Not only for people who already call themselves musicians</h2>
        <p style="margin-top:20px">The studio is also a classroom for the wider community. Recent sessions have included STEM nights and class visits from local schools, and Scout groups recording in the room.</p>
        <p><a class="btn btn-ghost" href="about.html">Read our story</a></p>
      </div>
      <div class="cols2 rv" style="gap:14px">
        <figure class="figure" style="margin:0"><img src="img/outreach-wilson.webp" alt="Students at a STEM night hosted in the studio" loading="lazy" width="1100" height="825"><figcaption>Wilson STEM night</figcaption></figure>
        <figure class="figure" style="margin:0"><img src="img/outreach-scouts.webp" alt="A Scout group recording in the studio" loading="lazy" width="1100" height="825"><figcaption>Scouts in the studio</figcaption></figure>
      </div>
    </div>
  </div>
</section>

<section class="tint rule">
  <div class="wrap" style="text-align:center">
    <h2 class="rv">Help us keep the door open</h2>
    <p class="rv narrow" style="margin:18px auto 26px">We are a registered 501(c)(3) New Jersey nonprofit dedicated to aiding and assisting underrepresented members of our community. Your donation helps us make dreams and futures a reality.</p>
    <div class="btns rv" style="justify-content:center">
      <a class="btn btn-primary" href="{DONATE}" rel="noopener" target="_blank">Donate</a>
      <a class="btn btn-ghost" href="support.html">Other ways to help</a>
    </div>
  </div>
</section>
"""

# ================================================================== ABOUT
about_body = f"""
{phead("Our mission", "We're all about lifting up New Jersey's homegrown talent; musicians and engineers alike.", "img/story-1.webp", "Inside the Inspiration Audio studio")}

<section>
  <div class="wrap narrow">
    <p class="rv">We're here to give you the chance to create original music, meet other artists and industry pros, and boost your skills and knowledge. And the best part? We make sure you can do it all without financial strain.</p>
  </div>
</section>

<section class="tint rule">
  <div class="wrap">
    <h2 class="rv">What we offer</h2>
    <div class="path rv" style="margin-top:30px">
      <div class="step"><div class="k">01</div><div>
        <h3>Recording and multi-media services</h3>
        <p>Musicians are welcome to record projects of any size without breaking the bank, and while retaining all rights to their music. Plus, you get access to our on-site photo and video studio to make awesome promo materials for marketing your music, building your brand, or designing your merch.</p>
      </div></div>
      <div class="step"><div class="k">02</div><div>
        <h3>Training and mentoring</h3>
        <p>Aspiring audio engineers can get hands-on experience in our studio, Carriage City, learning about recording, mixing and mastering, and live sound engineering. Gain real-world, hands-on experience and training for today's audio-visual needs, like podcasts, livestreams, video editing, and Dolby's spatial audio.</p>
      </div></div>
      <div class="step"><div class="k">03</div><div>
        <h3>DIY performance venue</h3>
        <p>In our new studio, Carriage City, our entire community is welcome to participate and attend our all-ages music concerts, cultural and community-based events, yoga and music classes, masterclasses, and workshops held year-round. The space is not only a recording studio, it's a home for our NJ music community to gather together.</p>
      </div></div>
    </div>
    <p class="rv narrow" style="margin-top:30px">Through these experiences, aspiring artists and recording engineers will be able to accumulate a portfolio of work that they can take with them as they pursue higher-education institutions or use for directly launching their careers in the industry.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2 class="rv">Our story</h2>
    <div class="split rv" style="margin-top:30px;align-items:start">
      <div class="narrow">
        <p>IA started the way our founder EJ initiated his other business: completely backwards! But that business is celebrating its 20th anniversary this year, so who can judge?</p>
        <p>IA was created with a "ready, fire, aim" mentality. We saw a huge need in the music community. Bands were struggling to find places to record, couldn't afford studio time, and weren't getting the personal care their projects deserved. Engineers were also having to choose between going to school for an audio engineering degree, which is also costly, or trying to learn on their own.</p>
        <p>Through a general love and curiosity about the mystifying world of audio engineering, EJ amassed a collection of recording equipment comparable to many major studios and started offering to record local bands for next to nothing.</p>
        <p>After the pandemic, the struggles in the music community became even more apparent. It seemed like an organization like IA could make a significant impact on many individuals. So, ready, fire, aim. EJ gathered a small team and got to work immediately.</p>
      </div>
      <figure class="figure" style="margin:0"><img src="img/story-2.webp" alt="A session in progress at Inspiration Audio" loading="lazy" width="1400" height="933"></figure>
    </div>
  </div>
</section>

<section class="tint rule">
  <div class="wrap">
    <div class="split">
      <div class="rv"><p class="pull">If we had to choose between hunting down high-profile board members or doing the real work, we'd choose the real work every day.</p></div>
      <div class="rv narrow">
        <p>IA is undoubtedly a New Jersey group. We are no frills. And just so you know, when someone comes into the studio with an egg, cheese, and ham sandwich, we call it "pork roll." If you call it Taylor Ham, you might find your session cut short!</p>
        <p>All kidding aside, IA is a gritty, DIY operation aimed at building a space of acceptance, creativity, education, and, most of all, opportunity for those who want it and are willing to put the time in. That's New Jersey to us, and that's punk. If you want to help, cool. If not, we're moving ahead anyway.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap narrow">
    <h2 class="rv">Where we're heading</h2>
    <div class="rv" style="margin-top:22px">
      <!-- TODO (EJ / Liz): the live site still says Carriage City opens Winter 2025. Confirm the current status and we will correct this paragraph. -->
      <p>IA is in motion to open its official home, Carriage City, which will house our recording studio and double as a performance venue and community space for cultural, art, yoga, and music events. We are partnering with Dolby Atmos and have invested in a spatial audio system so that we can provide these mixes for artists and also provide career-based training and experience for aspiring engineers, as New Jersey expands its involvement in the television and film industry. We also have our YouTube broadcast, Rainy Night Records, which we created to share music and stories from original New Jersey bands.</p>
      <p>We hope our work gives artists a voice and a home. We aspire to provide resources to everyone who interacts with us that say, "You belong here, you are welcome as you are." It's something we all want to feel, especially those bold enough to share their most intimate and personal thoughts and dare to step outside traditional social constructs like school, higher education, and stable, reliable jobs.</p>
      <p>We hope that the work we do provides a foundation for our artists and engineers to follow their dreams as far as they'd like to go. Whether it's performing at a major music festival, cultivating a small local following, or working at a major recording studio, we just want to help each individual we come across find a path and a community that supports them, and know that they belong here.</p>
    </div>
    <div class="btns rv" style="margin-top:26px">
      <a class="btn btn-primary" href="team.html">Meet the people</a>
      <a class="btn btn-ghost" href="studio.html">See the studio</a>
    </div>
  </div>
</section>
"""


# ================================================================== TEAM
team_body = f"""
{phead("Who we are", "We are a collective of musicians, recording engineers, songwriters, and producers who seek to help other like-minded artists and engineers on the path to achieving their dreams.")}

<section>
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="rv">
        <p class="eyebrow">Founder's story</p>
        <h2>EJ Gaub</h2>
        <p style="color:var(--muted);margin-top:8px">Musician, recording engineer, producer</p>
        <div class="narrow" style="margin-top:22px">
          <p>Growing up in a household where playing music was not permitted, EJ Gaub began his career by hiding a set of broken drums, found in the trash, in his attic. Even from a young age, EJ felt a strong draw and connection to music and knew it would play a major influence in his life.</p>
          <p>After the better part of his late teens and 20s was spent playing in various rock bands and climbing the corporate ladder with Armstrong World Industries, he started RMC Studios in 2005 in the basement of his home in Rahway, NJ. This basement school quickly ballooned from 20 students to over 200, forcing EJ to relocate his studio to a bigger space with more accessibility. RMC Studios is a music school and recording space for young aspiring and current artists to hone their craft and create freely in a supportive and enriching environment. Today RMC Studios resides in Garwood, NJ with over 500 enrolled students.</p>
          <p>While running RMC Studios, EJ continued to play in various bands and began to realize that a major frustration of his was that the sound his band created while performing live was rarely what the group heard when hearing a playback of their recordings. Too often, as a performer and recording artist, EJ felt that the recording process did not create the music he heard in his head, that there was a disconnect between the performer and the producer, and that the artist had little influence over their work. In 2015 he bought a couple of pieces of recording gear from Vintage King, was immediately hooked, and fell in love with the entire process instantly.</p>
          <p>Being entirely self-taught, EJ has worked with hundreds of students and local artists, assisting them through the entire songwriting process from lyric crafting and orchestration to recording, mixing, and mastering the final song. With each project and artist, EJ works tirelessly to ensure that each project sounds, feels, and lives up to exactly what the artist is expecting and desires. He firmly believes there is no greater gift than watching an artist or band smile or shed tears of happiness when listening to the playback of their song. It drives everything he does.</p>
          <p>While his passion is to work with local independent artists, EJ has been fortunate enough to do mixing and mastering work for Sony, Universal India, and Universal UK, working with artists such as B-Real (Cypress Hill), Petey Pablo, Daniel Donato, and Fat Man Scoop. EJ has also recorded and produced with local bands and artists such as The Red Room, Silent Tides, The Dutch Boys, Sister Ancestor, Matt Q., and others.</p>
          <p>At RMC Studios, he recorded and produced two albums of students' original music, entitled Unplugged and Rewritten, so named after the songwriting and mentorship program that is still around today. EJ currently records out of his live room in Garwood, NJ, and his intimate project studio and mix room in Rahway, NJ.</p>
        </div>
      </div>
      <figure class="figure rv" style="margin:0;position:sticky;top:96px">
        <img src="img/team.webp" alt="The Inspiration Audio team at work" loading="lazy" width="1400" height="933">
      </figure>
    </div>
  </div>
</section>

<section class="tint rule">
  <div class="wrap">
    <h2 class="rv">Meet the team</h2>
    <!-- TODO (EJ / Liz): Liz, Diego and John have no bio on the current site, only a title and an
         email. Three or four sentences each and this section stops being a directory listing.
         Also: Diego's title differs between the old /who-we-are and /contact pages
         ("Education Coordinator & Board Secretary" vs "Managing Member"). Which is right? -->
    <div class="cols2 rv" style="margin-top:30px">
      <div class="panel">
        <h3>Liz Robbins</h3>
        <p style="color:var(--accent-hot);font-weight:600;margin:4px 0 12px">Executive Director and Board President</p>
        <p style="margin:0"><a href="mailto:Liz@inspirationaudio.org" style="color:var(--chalk-dim)">Liz@inspirationaudio.org</a></p>
      </div>
      <div class="panel">
        <h3>EJ Gaub</h3>
        <p style="color:var(--accent-hot);font-weight:600;margin:4px 0 12px">Program Director and Founder</p>
        <p style="margin:0"><a href="mailto:EJ@inspirationaudio.org" style="color:var(--chalk-dim)">EJ@inspirationaudio.org</a></p>
      </div>
      <div class="panel">
        <h3>Diego Gallardo</h3>
        <p style="color:var(--accent-hot);font-weight:600;margin:4px 0 12px">Education Coordinator and Board Secretary</p>
        <p style="margin:0"><a href="mailto:Info@inspirationaudio.org" style="color:var(--chalk-dim)">Info@inspirationaudio.org</a></p>
      </div>
      <div class="panel">
        <h3>John Pepito</h3>
        <p style="color:var(--accent-hot);font-weight:600;margin:4px 0 12px">Artist Outreach</p>
        <p style="margin:0"><a href="mailto:Info@inspirationaudio.org" style="color:var(--chalk-dim)">Info@inspirationaudio.org</a></p>
      </div>
    </div>
  </div>
</section>
"""

# ================================================================== ARTISTS
def artist_card(a):
    soc = ""
    order = ["spotify", "apple", "instagram", "youtube", "tiktok", "twitter", "facebook", "site"]
    labels = {"spotify":"Spotify","apple":"Apple Music","instagram":"Instagram","youtube":"YouTube",
              "tiktok":"TikTok","twitter":"X","facebook":"Facebook","site":"Website"}
    for k in order:
        u = a["links"].get(k)
        if u:
            soc += (f'<a href="{u}" rel="noopener" target="_blank" '
                    f'aria-label="{a["name"]} on {labels[k]}">{svg(k, labels[k])}</a>')
    pic = (f'<div class="pic"><img src="{a["img"]}" alt="{a["name"]}" loading="lazy" '
           f'width="520" height="520"></div>') if a["img"] else '<div class="pic"></div>'
    player = ""
    if a["embed"]:
        h = 152 if a["embed_type"] == "track" else 232
        player = (f'<div class="player"><iframe src="{a["embed"]}" height="{h}" '
                  f'loading="lazy" title="{a["name"]} on Spotify" '
                  f'allow="encrypted-media; clipboard-write; picture-in-picture" '
                  f'referrerpolicy="strict-origin-when-cross-origin"></iframe></div>')
    return (f'<article class="artist rv">{pic}<h3>{a["name"]}</h3>'
            f'<div class="soc">{soc}</div>{player}</article>')

artists_body = f"""
{phead("IA artists", "The artists who record with Inspiration Audio. Every one of them keeps the rights to their music.", "img/for-artists.webp", "Musicians recording in the live room")}

<section>
  <div class="wrap">
    <h2 class="rv" style="margin-bottom:34px">Currently recording with us</h2>
    <div class="roster">
      {''.join(artist_card(a) for a in ARTISTS)}
    </div>
  </div>
</section>

<section class="tint rule">
  <div class="wrap">
    <div class="split">
      <div class="rv">
        <h2>What you get as an IA artist</h2>
        <p style="margin-top:18px">Studio time in a space where your ideas are heard, respected, and turned into reality. Sit back and let our engineers do what they do best, or jump in the driver's seat yourself.</p>
      </div>
      <div class="rv">
        <ul class="tags" style="margin-bottom:20px">
          <li>Collaborate with other artists</li>
          <li>Access to masterclasses</li>
          <li>All-ages performance venue</li>
          <li>On-site photo and video studio</li>
          <li>Keep every right to your music</li>
        </ul>
        <p>You are connected to our extended network of artists, engineers and media managers, so you can network, gain new insights, and launch your musical career. Create all the promotional materials you need for marketing your music, building your brand, and designing your merchandise, at a professional level.</p>
        <div class="btns"><a class="btn btn-primary" href="contact.html">Become an IA artist</a></div>
      </div>
    </div>
  </div>
</section>
"""

# ================================================================== LISTEN
TRACKS = [("Backseat Driver","Public Disturbances","04:55"),("Mr. Blue Sky","Beat Stu","03:15"),
          ("No Control","Super Nova 42","03:52"),("Ode to Dylan","Button","03:58"),
          ("You Wish","J. Hoffman","02:59"),("Man Against Himself","M. Hunsinger","02:12"),
          ("Anxiously Waiting","L. Cabral","04:07"),("Multiverse","J. August","02:49"),
          ("Set Free","R. Bowie","04:05")]

listen_body = f"""
{phead("The IA playlist", "Nine tracks cut at Inspiration Audio.")}

<section>
  <div class="wrap">
    <!-- TODO (EJ / Liz): on the old site these nine tracks were hosted inside Wix and only one of
         these artists (Public Disturbances) also appears on the artists page. Is this playlist
         current? We need the audio files to host them here properly. Until then this page lists
         the tracks and the player stays on the artists page. -->
    <div class="deflist rv">
      {''.join(f'<div class="row"><span class="t">{t}</span><span>{a} <span style="color:var(--muted);font-family:JetBrains Mono,monospace;font-size:.85rem;margin-left:8px">{d}</span></span></div>' for t,a,d in TRACKS)}
    </div>
    <div class="formnote rv" style="margin-top:26px">
      Audio for these nine tracks currently lives on the old Wix site. To play them here we need the
      original files, or a link to each track on Spotify or Apple Music.
    </div>
    <div class="btns rv" style="margin-top:26px">
      <a class="btn btn-primary" href="artists.html">Hear the IA artists</a>
      <a class="btn btn-ghost" href="https://open.spotify.com/playlist/7JXZhjPYF04AyPYMaOmEya" rel="noopener" target="_blank">IA playlist on Spotify</a>
    </div>
  </div>
</section>
"""

# ================================================================== STUDIO
studio_body = f"""
{phead("Our space", "Two rooms today, and a bigger home on the way.", "img/rahway-1.webp", "The Rahway recording room")}

<section>
  <div class="wrap">
    <h2 class="rv" style="margin-bottom:32px">Two rooms, open now</h2>
    <div class="cols2">
      <div class="rv">
        <figure class="figure" style="margin:0 0 20px"><img src="img/rahway-2.webp" alt="The Rahway studio control room" loading="lazy" width="1600" height="1067"></figure>
        <h3>Rahway Studio</h3>
        <p>Record in an intimate, creative space where your ideas are cultivated and supported. Sit back and let our engineers do what they do best, or jump in the driver's seat yourself.</p>
        <a class="btn btn-ghost" href="contact.html">Book a session</a>
      </div>
      <div class="rv">
        <figure class="figure" style="margin:0 0 20px"><img src="img/live-room.webp" alt="The Garwood live room set up for a full band" loading="lazy" width="1600" height="1067"></figure>
        <h3>Garwood Live Room</h3>
        <p>Studio space here is fit for larger projects and full bands to record all at the same time. Also available for rental for groups or engineers who would like to lead engineer their own projects.</p>
        <a class="btn btn-ghost" href="contact.html">Book a session</a>
      </div>
    </div>
  </div>
</section>

<section class="tint rule">
  <div class="wrap">
    <div class="split">
      <div class="rv">
        <h2>Carriage City</h2>
        <!-- TODO (EJ / Liz): the live site still says "moving in Winter 2025", which has passed.
             Are you in? Is carriagecitystudios.com the same operation or a separate business?
             We have deliberately not written a date here. -->
        <p style="margin-top:18px">Our official home will house the recording studio and double as a performance venue and community space, with all-ages concerts, cultural and community events, yoga and music classes, masterclasses and workshops through the year.</p>
        <p>We are partnering with Dolby Atmos and have invested in a spatial audio system, so we can deliver those mixes for artists and train engineers on them as New Jersey expands its involvement in television and film.</p>
      </div>
      <div class="rv"><p class="pull">Not only a recording studio. A home for the New Jersey music community to gather.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split wide-left">
      <div class="rv">
        <h2>The room is full of real equipment</h2>
        <p style="margin-top:18px">EJ has assembled a collection comparable to many major studios, and it keeps growing. Neve, API, Neumann, Coles, Royer, a Fender Rhodes, a Mellotron, a wall of amps, and a mic locker of more than sixty microphones.</p>
        <div class="btns"><a class="btn btn-primary" href="gear.html">See the full gear list</a></div>
      </div>
      <figure class="figure rv" style="margin:0"><img src="img/gear-mics.webp" alt="Microphones set up in the studio" loading="lazy" width="1600" height="900"></figure>
    </div>
  </div>
</section>
"""


# ================================================================== GEAR
def gearcard(g):
    items = "".join(f"<li>{i}</li>" for i in g["items"])
    return (f'<div class="gearcard rv"><span class="count">{len(g["items"])} items</span>'
            f'<h3>{g["name"]}</h3><ul>{items}</ul></div>')

n_gear = sum(len(g["items"]) for g in GEAR["groups"])
n_mics = sum(len(g["items"]) for g in GEAR["mics"])

gear_body = f"""
{phead("Gear list", f"{n_gear + n_mics} pieces of equipment, including a mic locker of {n_mics}. EJ is always on the hunt, so this list keeps growing.", "img/gear-room.webp", "Outboard gear racked in the studio")}

<section>
  <div class="wrap">
    <h2 class="rv">Outboard, instruments and the room</h2>
    <div class="gear" style="margin-top:30px">
      {''.join(gearcard(g) for g in GEAR["groups"])}
    </div>
  </div>
</section>

<section class="tint rule">
  <div class="wrap">
    <div class="split wide-left" style="align-items:end;margin-bottom:34px">
      <div class="rv"><h2>The mic locker</h2>
        <p style="margin-top:16px">{n_mics} microphones, from a Neumann u87 Ai and a FLEA 47 to Coles and Royer ribbons and a full set of Shure workhorses.</p></div>
      <figure class="figure rv" style="margin:0"><img src="img/gear-amps.webp" alt="Amplifiers in the studio" loading="lazy" width="1100" height="1467"></figure>
    </div>
    <div class="gear">
      {''.join(gearcard(g) for g in GEAR["mics"])}
    </div>
  </div>
</section>

<section>
  <div class="wrap" style="text-align:center">
    <h2 class="rv">Want to use it?</h2>
    <p class="rv narrow" style="margin:16px auto 26px">The Garwood live room is also available for rental to groups or engineers who want to lead engineer their own projects.</p>
    <div class="btns rv" style="justify-content:center">
      <a class="btn btn-primary" href="contact.html">Book a session</a>
      <a class="btn btn-ghost" href="studio.html">See the rooms</a>
    </div>
  </div>
</section>
"""

# ================================================================== TRAINING
training_body = f"""
{phead("Train as an engineer", "Hands on real equipment, rather than paying for a degree first.", "img/for-engineers.webp", "An engineer working at the console")}

<section>
  <div class="wrap narrow">
    <p class="rv">Engineers have been stuck choosing between an audio engineering degree, which is costly, or trying to learn on their own. Inspiration Audio exists to make a third option real: get hands-on experience in a working studio, learning recording, mixing and mastering, and live sound engineering.</p>
    <p class="rv">You gain real-world training for what audio-visual work actually looks like now. Podcasts, livestreams, video editing, and Dolby's spatial audio.</p>
  </div>
</section>

<section class="tint rule">
  <div class="wrap">
    <h2 class="rv">What you leave with</h2>
    <div class="cols3 rv" style="margin-top:30px">
      <div class="panel"><h3>A portfolio</h3><p>Aspiring artists and recording engineers accumulate a body of work they can take with them, whether they go on to a higher-education institution or straight into the industry.</p></div>
      <div class="panel"><h3>A network</h3><p>You are connected to our extended network of artists, engineers and media managers, so you can collaborate, gain insights and find work.</p></div>
      <div class="panel"><h3>Room to fail safely</h3><p>A space of acceptance, creativity and education for people who want it and are willing to put the time in.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split">
      <div class="rv">
        <h2>If you cannot pay for it</h2>
        <p style="margin-top:18px">Apply to be an IA Scholar and receive access to everything offered to IA artists and engineers, for free. All inquiries are accepted.</p>
        <div class="btns"><a class="btn btn-primary" href="scholarship.html">The IA Scholarship</a></div>
      </div>
      <figure class="figure rv" style="margin:0"><img src="img/session-indeyevid.webp" alt="A recording session in progress" loading="lazy" width="1100" height="825"></figure>
    </div>
  </div>
</section>
"""

# ================================================================== SCHOLARSHIP
scholarship_body = f"""
{phead("The IA Scholarship", "Our mission is to provide opportunities and experiences to all of those who have an interest, no matter their background or financial circumstances.", "img/scholarship.webp", "Inside the Inspiration Audio studio")}

<section>
  <div class="wrap">
    <div class="split wide-left" style="align-items:start">
      <div class="rv">
        <h2>What an IA Scholar gets</h2>
        <p style="margin:18px 0 24px">Everything offered to IA artists and engineers, for free.</p>
        <div class="path">
          <div class="step"><div class="k">01</div><div><h3>Access to the recording studio</h3></div></div>
          <div class="step"><div class="k">02</div><div><h3>Every masterclass and event</h3></div></div>
          <div class="step"><div class="k">03</div><div><h3>Use of the photography and video studio</h3></div></div>
          <div class="step"><div class="k">04</div><div><h3>A network to collaborate with</h3><p>Connect with other like-minded musicians and engineers.</p></div></div>
          <div class="step"><div class="k">05</div><div><h3>The all-ages performance space</h3><p>Build your fan base and get a platform to perform on.</p></div></div>
        </div>
        <p class="pull rv" style="margin-top:32px">All inquiries are accepted.</p>
      </div>
      <div class="panel accent rv" style="position:sticky;top:96px">
        <h3>Apply</h3>
        <p>Tell us who you are and what you want to do. There is no cost and no catch.</p>
        <a class="btn btn-primary" href="#apply" style="width:100%">Start the application</a>
      </div>
    </div>
  </div>
</section>

<section class="tint rule" id="apply">
  <div class="wrap">
    <h2 class="rv">Scholarship application</h2>
    <!-- TODO (EJ / Liz): where should this deliver? Right now it posts nowhere. We need an inbox,
         and we will send a real test submission and confirm it lands before this goes live. -->
    <form class="form rv" style="margin-top:28px" method="post" action="#" novalidate>
      <div class="field"><label for="s-name">First and last name</label><input id="s-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="s-phone">Phone</label><input id="s-phone" name="phone" type="tel" autocomplete="tel" required></div>
      <div class="field"><label for="s-email">Email</label><input id="s-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="s-address">Address</label><input id="s-address" name="address" type="text" autocomplete="street-address" required></div>
      <div class="field"><label for="s-dob">Date of birth</label><input id="s-dob" name="dob" type="text" inputmode="numeric" placeholder="MM/DD/YYYY" required><span class="hint">Format: MM/DD/YYYY</span></div>
      <fieldset style="border:0;padding:0;margin:0">
        <legend class="field" style="font-size:.88rem;font-weight:600;color:var(--chalk);margin-bottom:9px">I want to apply as</legend>
        <div class="radios">
          <label><input type="radio" name="role" value="artist" required><span>Artist</span></label>
          <label><input type="radio" name="role" value="engineer"><span>Engineer</span></label>
          <label><input type="radio" name="role" value="both"><span>Both</span></label>
          <label><input type="radio" name="role" value="other"><span>Other</span></label>
        </div>
      </fieldset>
      <div class="field"><label for="s-other">If other, please specify</label><input id="s-other" name="other" type="text"></div>
      <div class="field"><label for="s-school">Are you currently in school? If so, where?</label><textarea id="s-school" name="school" rows="2" required></textarea></div>
      <div class="field"><label for="s-bg">What is your music background?</label><textarea id="s-bg" name="background" rows="4" required></textarea></div>
      <div class="field"><label for="s-why">What ignited your interest in music?</label><textarea id="s-why" name="why" rows="4" required></textarea></div>
      <div><button class="btn btn-primary" type="submit">Submit application</button></div>
      <p class="formnote">This form is not connected yet in this preview. Nothing you type here is sent anywhere.</p>
    </form>
  </div>
</section>
"""

# ================================================================== SUPPORT
support_body = f"""
{phead("Support us", "Inspiration Audio is a registered 501(c)(3) New Jersey nonprofit organization dedicated to aiding and assisting underrepresented members of our community. Your donation helps us make dreams and futures a reality.", "img/support.webp", "The Inspiration Audio community at an event")}

<section>
  <div class="wrap">
    <h2 class="rv" style="margin-bottom:32px">Three ways to help</h2>
    <div class="cols3">
      <div class="panel accent rv">
        <h3>Donate</h3>
        <p>Any amount goes straight into studio time, scholarships and events for people who could not otherwise afford them.</p>
        <a class="btn btn-primary" href="{DONATE}" rel="noopener" target="_blank">Donate</a>
      </div>
      <div class="panel rv">
        <h3>Sponsorships</h3>
        <p>Back a program, an event or a scholarship place. Get in touch and we will walk you through what your support would actually pay for.</p>
        <a class="btn btn-ghost" href="contact.html">Talk to us</a>
      </div>
      <div class="panel rv">
        <h3>Donate gear</h3>
        <p>Instruments, outboard, microphones, cables. If it works and it is useful, it goes into the room and gets used by people learning on it.</p>
        <a class="btn btn-ghost" href="contact.html">Offer gear</a>
      </div>
    </div>
  </div>
</section>

<section class="tint rule">
  <div class="wrap">
    <div class="split">
      <div class="rv"><p class="pull">We decided early on that if we had to choose between chasing high-profile donors and doing the real work, we'd choose the real work every day.</p></div>
      <div class="rv narrow">
        <p>Inspiration Audio is a gritty, DIY operation. Money that comes in goes into the room, the programs and the people using them. There is no owner taking a profit, because a 501(c)(3) does not work that way.</p>
        <p>If you want to help, cool. If not, we're moving ahead anyway.</p>
      </div>
    </div>
  </div>
</section>
"""

# ================================================================== EVENTS
events_body = f"""
{phead("Events", "All-ages shows, masterclasses, workshops and community nights.")}

<section>
  <div class="wrap">
    <!-- TODO (EJ / Liz): the old site's events system had one listing and it has already passed.
         Send us anything coming up and we will put it here. -->
    <h2 class="rv" style="margin-bottom:30px">What's coming up</h2>
    <div class="empty rv">
      <h3>Nothing on the calendar right now</h3>
      <p>When the next show, masterclass or community night is booked, it will be listed here. Follow along on Instagram in the meantime, or get on the list.</p>
      <div class="btns" style="justify-content:center;margin-top:22px">
        <a class="btn btn-primary" href="contact.html">Get on the list</a>
        <a class="btn btn-ghost" href="https://www.instagram.com/inspiration.audio/" rel="noopener" target="_blank">Follow on Instagram</a>
      </div>
    </div>
  </div>
</section>

<section class="tint rule">
  <div class="wrap">
    <h2 class="rv">What we host</h2>
    <div class="cols3 rv" style="margin-top:28px">
      <div class="panel"><h3>All-ages concerts</h3><p>A stage for artists to showcase new work and build a following, open to every age.</p></div>
      <div class="panel"><h3>Masterclasses</h3><p>Free sessions where you learn from industry professionals and widen your skill set.</p></div>
      <div class="panel"><h3>Community nights</h3><p>Cultural and community events, plus yoga and music classes and workshops through the year.</p></div>
    </div>
  </div>
</section>
"""

# ================================================================== CONTACT
contact_body = f"""
{phead("Contact", "Tell us what you want to do and we will point you at the right door.")}

<section>
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="rv">
        <h2 style="font-size:clamp(1.4rem,1.2rem + 1vw,1.9rem)">Get in touch</h2>
        <!-- TODO (EJ / Liz): where should this form deliver, and is it one inbox or three? -->
        <form class="form" style="margin-top:24px" method="post" action="#" novalidate>
          <div class="cols2" style="gap:16px">
            <div class="field"><label for="c-first">First name</label><input id="c-first" name="first" type="text" autocomplete="given-name" required></div>
            <div class="field"><label for="c-last">Last name</label><input id="c-last" name="last" type="text" autocomplete="family-name" required></div>
          </div>
          <div class="field"><label for="c-phone">Phone</label><input id="c-phone" name="phone" type="tel" autocomplete="tel" required></div>
          <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
          <fieldset style="border:0;padding:0;margin:0">
            <legend class="field" style="font-size:.88rem;font-weight:600;color:var(--chalk);margin-bottom:9px">I am getting in touch as</legend>
            <div class="radios">
              <label><input type="radio" name="as" value="artist" required><span>IA Artist</span></label>
              <label><input type="radio" name="as" value="engineer"><span>IA Engineer</span></label>
              <label><input type="radio" name="as" value="scholar"><span>IA Scholar</span></label>
              <label><input type="radio" name="as" value="other"><span>Something else</span></label>
            </div>
          </fieldset>
          <div class="field"><label for="c-msg">How would you like to get involved with IA?</label><textarea id="c-msg" name="message" rows="5" required></textarea></div>
          <div><button class="btn btn-primary" type="submit">Send</button></div>
          <p class="formnote">This form is not connected yet in this preview. Nothing you type here is sent anywhere.</p>
        </form>
      </div>
      <div class="rv">
        <h2 style="font-size:clamp(1.4rem,1.2rem + 1vw,1.9rem)">Direct</h2>
        <div class="deflist" style="margin-top:24px">
          <div class="row"><span class="t">Phone</span><span><a href="tel:+19089000229">(908) 900-0229</a></span></div>
          <div class="row"><span class="t">General</span><span><a href="mailto:info@inspirationaudio.org">info@inspirationaudio.org</a></span></div>
          <div class="row"><span class="t">Liz Robbins</span><span>Executive Director and Studio Manager<br><a href="mailto:Liz@inspirationaudio.org">Liz@inspirationaudio.org</a></span></div>
          <div class="row"><span class="t">EJ Gaub</span><span>President, Founder and Lead Engineer<br><a href="mailto:EJ@inspirationaudio.org">EJ@inspirationaudio.org</a></span></div>
          <div class="row"><span class="t">Diego Gallardo</span><span>Managing Member<br><a href="mailto:Info@inspirationaudio.org">Info@inspirationaudio.org</a></span></div>
          <div class="row"><span class="t">Where</span><span>Rahway, New Jersey</span></div>
        </div>
        <div class="panel accent" style="margin-top:26px">
          <h3>Applying for a scholarship?</h3>
          <p style="margin-bottom:16px">There is a separate form with a few more questions on it.</p>
          <a class="btn btn-primary" href="scholarship.html#apply">Scholarship application</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# ================================================================== ACCESSIBILITY
a11y_body = f"""
{phead("Accessibility", "We want this site to work for everyone who lands on it.")}
<section>
  <div class="wrap narrow">
    <h2 class="rv" style="font-size:clamp(1.3rem,1.15rem + .8vw,1.7rem)">What we have done</h2>
    <div class="rv" style="margin-top:18px">
      <p>This site is built to meet WCAG 2.1 AA where we can. In practice that means a skip link to the main content, a single clear heading order on every page, visible focus outlines on everything you can tab to, text that meets AA contrast against its background, alt text on images that carry meaning, form labels that are real labels rather than placeholder text, and full keyboard operation including the menu.</p>
      <p>Animation on this site is limited to gentle fade-ins. If your device is set to reduce motion, they do not run at all.</p>
    </div>
    <h2 class="rv" style="font-size:clamp(1.3rem,1.15rem + .8vw,1.7rem);margin-top:36px">Where it falls short</h2>
    <div class="rv" style="margin-top:18px">
      <p>The Spotify players on the artists page are supplied by Spotify, so their internal accessibility is not something we control. Every artist also has plain links out to their music alongside the player.</p>
    </div>
    <h2 class="rv" style="font-size:clamp(1.3rem,1.15rem + .8vw,1.7rem);margin-top:36px">Tell us if something does not work</h2>
    <div class="rv" style="margin-top:18px">
      <p>If any part of this site gets in your way, email <a href="mailto:info@inspirationaudio.org" style="color:var(--accent-hot)">info@inspirationaudio.org</a> or call <a href="tel:+19089000229" style="color:var(--accent-hot)">(908) 900-0229</a> and tell us what happened. We will fix it.</p>
    </div>
  </div>
</section>
"""

# ================================================================== TUTORIALS
# Video IDs below were confirmed by EXACT title match against Inspiration Audio's
# own YouTube channel (@inspirationaudio1676). The six long-form mixing videos on
# their old page are not on that channel, so they are listed but not embedded
# rather than guessed at.
TUTORIALS = [
 ("Mixing", [
   ("Over EQ'ing Your Mix: The Perspective Shift You're Missing", "28:49", None),
   ("Steve Albini Did This Differently With Drums", "20:45", None),
   ("Why 1 Cent Makes Vocals Sound Bigger", "12:05", None),
   ("The Emotional Side of Reverb", "17:11", None),
   ("Spectral vs Multiband vs Compression | When Each One Actually Makes Sense", "25:29", None),
   ("Do You Know What's Killing the Bass in Your Mix?", "20:46", None),
 ]),
 ("Recording", [
   ("BEST VO MICS $$$", "1:06", "-2RDda8iWas"),
   ("A Recreation of Thriller", "6:48", "mkPqo7ZkYvg"),
   ("Quick Tip 9 - Drum Muffling", "3:23", "O9mbywNNyjU"),
   ("Recording Experimentation Day @ Inspiration Audio", "1:13", "3Ew4i9rxmOI"),
   ("Quick Tip - Drum Mic Placement", "1:03", "D1A7nqNx9kU"),
   ("Quick Tip - The Pooper Time Cube", "0:54", "uhkY79pDZN8"),
 ]),
 ("Production", [
   ("Recording a Basic Drum Beat", "1:15", "2S1-pLI0wgE"),
   ("Making Beats on Your iPhone??", "1:24", "4URYO3DnVgQ"),
   ("Vital Plug-In FX Explained", "0:57", "vLfyzewwGnA"),
 ]),
]
n_vid = sum(len(v) for _, v in TUTORIALS)
n_emb = sum(1 for _, v in TUTORIALS for x in v if x[2])

def vidcard(t, dur, vid):
    if vid:
        return (f'<article class="vid rv"><div class="frame">'
                f'<iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{t}" loading="lazy"'
                f' allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"'
                f' referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
                f'<h3>{t}</h3><p class="dur">{dur}</p></article>')
    return (f'<article class="vid rv pending"><div class="frame ph"><span>On their channel</span></div>'
            f'<h3>{t}</h3><p class="dur">{dur}</p></article>')

tutorials_body = f"""
{phead("Tutorials", f"{n_vid} videos on mixing, recording and production, free to watch.")}

<section>
  <div class="wrap">
    {''.join(f'''<div class="vidgroup rv" style="margin-bottom:clamp(40px,5vw,66px)">
      <h2 style="margin-bottom:26px">{name}</h2>
      <div class="vidgrid">{''.join(vidcard(*v) for v in vids)}</div>
    </div>''' for name, vids in TUTORIALS)}
    <!-- TODO (EJ / Liz): the six Mixing videos are not on the @inspirationaudio1676 channel,
         so we have deliberately not guessed at their links. Send us where they live (a second
         channel, a playlist, or Rainy Night Records) and they get embedded like the rest. -->
    <div class="formnote rv">
      The six mixing videos are listed with the titles and run times from your own site, but they
      are not on the Inspiration Audio YouTube channel, so we have not linked them to anything. Tell
      us where they live and they will play here like the others.
    </div>
    <div class="btns rv" style="margin-top:28px">
      <a class="btn btn-primary" href="https://www.youtube.com/@inspirationaudio1676" rel="noopener" target="_blank">All videos on YouTube</a>
      <a class="btn btn-ghost" href="training.html">Train with us in person</a>
    </div>
  </div>
</section>
"""

# ================================================================== GALLERY
GALLERY = json.load(open(os.path.join(HERE, "gallery.json")))
def gitem(g, i):
    alt = g["alt"] or "Inside the Inspiration Audio studio"
    cap = f'<figcaption>{g["alt"]}</figcaption>' if g["alt"] else ""
    tall = " tall" if g["portrait"] else ""
    return (f'<figure class="gcell{tall} rv">'
            f'<a href="{g["full"]}" target="_blank" rel="noopener" aria-label="Open larger image: {alt}">'
            f'<img src="{g["thumb"]}" alt="{alt}" loading="lazy" decoding="async" '
            f'width="{g["w"]}" height="{g["h"]}"></a>{cap}</figure>')

n_named = sum(1 for g in GALLERY if g["alt"])
gallery_body = f"""
{phead("Gallery", f"{len(GALLERY)} photographs from the studio, the sessions, the gear and the community nights.")}

<section>
  <div class="wrap">
    <div class="gallery">
      {''.join(gitem(g, i) for i, g in enumerate(GALLERY))}
    </div>
    <p class="formnote rv" style="margin-top:34px">
      {n_named} of these {len(GALLERY)} photographs came across with their own captions. The rest
      have a general description for screen readers. If you tell us what is in them we will caption
      them properly.
    </p>
  </div>
</section>
"""


# ================================================================== RENDER
PAGES = [
 ("index.html","Inspiration Audio | Nonprofit recording studio in Rahway, NJ","A 501(c)(3) nonprofit studio in Rahway, NJ. Record your project, train as an engineer, or apply for a scholarship and do all of it for free.",home_body),
 ("about.html","About | Inspiration Audio","A nonprofit that uses a working studio as a training floor for New Jersey musicians and engineers. Our mission, what we offer, and how IA started.",about_body),
 ("team.html","Who we are | Inspiration Audio","Founder EJ Gaub and the team behind Inspiration Audio, a collective of musicians, engineers, songwriters and producers in Rahway, NJ.",team_body),
 ("artists.html","IA artists | Inspiration Audio","The artists who record at Inspiration Audio in Rahway, NJ. Hear them, follow them, and keep every right to your own music when you record here.",artists_body),
 ("listen.html","Listen | Inspiration Audio","Nine tracks cut at Inspiration Audio in Rahway, New Jersey.",listen_body),
 ("studio.html","The studio | Inspiration Audio","The Rahway studio, the Garwood live room, and Carriage City. Where Inspiration Audio records, rehearses and puts on shows.",studio_body),
 ("gear.html","Gear list | Inspiration Audio",f"{n_gear + n_mics} pieces of equipment at Inspiration Audio, including a {n_mics} microphone locker. Neve, API, Neumann, Coles, Royer, Rhodes and more.",gear_body),
 ("training.html","Train as an engineer | Inspiration Audio","Learn recording, mixing, mastering and live sound with your hands on real equipment at a nonprofit studio in Rahway, NJ.",training_body),
 ("scholarship.html","IA Scholarship | Inspiration Audio","Apply to be an IA Scholar and get studio access, masterclasses, the photo and video studio and the performance space for free. All inquiries are accepted.",scholarship_body),
 ("support.html","Support us | Inspiration Audio","Inspiration Audio is a registered 501(c)(3) nonprofit. Donate, sponsor a program, or donate gear that gets used by people learning on it.",support_body),
 ("events.html","Events | Inspiration Audio","All-ages concerts, masterclasses, workshops and community nights at Inspiration Audio in Rahway, New Jersey.",events_body),
 ("tutorials.html","Tutorials | Inspiration Audio","Free mixing, recording and production tutorials from the engineers at Inspiration Audio in Rahway, New Jersey.",tutorials_body),
 ("gallery.html","Gallery | Inspiration Audio","Photographs from inside Inspiration Audio: the studio, sessions, the gear and community nights in Rahway, NJ.",gallery_body),
 ("contact.html","Contact | Inspiration Audio","Get in touch with Inspiration Audio in Rahway, NJ. Call (908) 900-0229 or email info@inspirationaudio.org.",contact_body),
 ("accessibility.html","Accessibility | Inspiration Audio","How we have built this site to work for everyone, where it falls short, and how to tell us about a problem.",a11y_body),
]

built = []
for slug, title, desc, body in PAGES:
    built.append(page(slug, title, desc, body))

# sitemap (preview is noindex; kept accurate for when it goes live)
urls = "".join(f'\n  <url><loc>{BASE}{"" if s=="index.html" else s}</loc><lastmod>{TODAY}</lastmod></url>'
               for s, *_ in PAGES)
open(os.path.join(HERE, "sitemap.xml"), "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}\n</urlset>\n')

open(os.path.join(HERE, "robots.txt"), "w").write(
    "# Preview build. Not for indexing until the client approves and it moves to their domain.\n"
    "User-agent: *\nDisallow: /\n")

print(f"built {len(built)} pages")
for b in built:
    print("   ", b, f"{os.path.getsize(os.path.join(HERE,b))/1024:.0f}KB")
