#!/usr/bin/env python3
"""Marlene Baldinger campaign site - 'local paper' editorial design.
Content verbatim from her 2023 door hanger (scanned 2026-08-15) and the
2026-08-14 meeting transcript. Do not invent facts. Sidecar: .claims.json
Design: warm broadsheet. Fraunces display + Public Sans. Cream paper, ink navy,
teal accent, gold hairlines. Real 2023 door-hanger crop as the receipts artifact."""
import os, json
OUT = os.path.dirname(os.path.abspath(__file__))
ASSET_V = "104496"

CSS = r"""
:root{
 --paper:#f8f4ea;--ink:#202d3a;--navy:#1c3447;--teal:#2e7d6e;--gold:#c69c6d;
 --wine:#722727;--line:#ddd3bf;--muted:#5d6a74;
 --disp:'Fraunces',Baskerville,Georgia,serif;
 --body:'Public Sans',-apple-system,'Segoe UI',Helvetica,sans-serif;
 --s1:8px;--s2:16px;--s3:24px;--s4:36px;--s5:56px;--s6:88px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:var(--body);color:var(--ink);background:var(--paper);font-size:17.5px;line-height:1.7}
body::after{content:"";position:fixed;inset:0;pointer-events:none;opacity:.5;mix-blend-mode:multiply;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3CfeColorMatrix values='0 0 0 0 0.55 0 0 0 0 0.51 0 0 0 0 0.44 0 0 0 .05 0'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)'/%3E%3C/svg%3E")}
h1,h2,h3,figcaption{font-family:var(--disp);color:var(--navy);text-wrap:balance}
p{text-wrap:pretty}
a{color:var(--teal);text-decoration-thickness:1.5px;text-underline-offset:3px;transition:color .2s}
a:hover{color:var(--navy)}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.wrap{max-width:1000px;margin:0 auto;padding:0 var(--s3)}
.skip{position:absolute;left:-9999px}.skip:focus{position:static;display:block;background:var(--gold);color:var(--navy);padding:10px}

/* masthead */
.masthead{text-align:center;padding:var(--s4) var(--s3) 0}
.dateline{font-size:.72rem;letter-spacing:.24em;text-transform:uppercase;color:var(--wine)}
.masthead h1,.masthead .mast{font-family:var(--disp);font-weight:900;font-size:clamp(2.2rem,6vw,3.4rem);line-height:1.05;margin:.18em 0 .1em;color:var(--navy);letter-spacing:-.01em}
.mastsub{font-family:var(--disp);font-style:italic;color:var(--teal);font-size:1.05rem}
.mast a{color:var(--navy);text-decoration:none}
nav.paper{margin-top:var(--s3);border-top:1px solid var(--line);border-bottom:1px solid var(--line);position:relative}
nav.paper::after{content:"";position:absolute;left:0;right:0;bottom:3px;border-bottom:1px solid var(--line)}
nav.paper ul{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:2px 0;padding:9px 0 12px}
nav.paper a{font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:var(--ink);padding:4px 13px;border-right:1px solid var(--line)}
nav.paper li:last-child a{border-right:0}
nav.paper a:hover{color:var(--teal)}
nav.paper a.on{color:var(--wine);font-weight:700}

/* stagger reveal */
@media(prefers-reduced-motion:no-preference){
 .rise{opacity:0;transform:translateY(14px);animation:rise .6s cubic-bezier(.2,.7,.3,1) forwards}
 .rise:nth-child(2){animation-delay:.08s}.rise:nth-child(3){animation-delay:.16s}
 .rise:nth-child(4){animation-delay:.24s}.rise:nth-child(5){animation-delay:.32s}
 @keyframes rise{to{opacity:1;transform:none}}
}

/* hero */
.hero{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:var(--s5);align-items:center;padding:var(--s6) 0 var(--s5)}
.kick{font-size:.74rem;letter-spacing:.22em;text-transform:uppercase;color:var(--wine);font-weight:600}
.hero h2{font-size:clamp(2.6rem,5.6vw,4.3rem);font-weight:600;line-height:1.06;margin-top:var(--s2);letter-spacing:-.015em}
.hero h2 em{font-style:italic;color:var(--teal);font-weight:400}
.deck{font-size:1.16rem;line-height:1.65;color:var(--ink);margin-top:var(--s3);max-width:30em}
.deck strong{color:var(--navy)}
.hero .actions{margin-top:var(--s4);display:flex;gap:var(--s3);align-items:center;flex-wrap:wrap}
.btn{display:inline-block;font-family:var(--body);font-weight:700;font-size:.85rem;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:#fff;background:var(--teal);padding:15px 24px;border:0;border-radius:3px;cursor:pointer;transition:background .2s,transform .15s}
.btn:hover{background:var(--navy);color:#fff;transform:translateY(-1px)}
.btn:active{transform:translateY(1px)}
.textlink{font-weight:600}
figure.portrait{margin:0}
figure.portrait img{width:100%;height:auto;display:block;border:1px solid var(--line)}
figcaption{font-size:.8rem;color:var(--muted);font-family:var(--body);margin-top:10px;padding-top:8px;border-top:2px solid var(--gold);line-height:1.5}
figcaption .credit{display:block;font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;margin-top:2px;color:#8a8474}

/* section furniture */
section.sec{padding:var(--s5) 0;border-top:1px solid var(--line)}
.sechead{display:flex;align-items:baseline;gap:14px;margin-bottom:var(--s4)}
.sechead .star{color:var(--gold);font-size:.9rem}
.sechead h3{font-size:clamp(1.7rem,3.4vw,2.3rem);font-weight:600}
.sechead h3 em{font-style:italic;color:var(--teal);font-weight:400}
.sechead .rule{flex:1;border-top:1px solid var(--line);transform:translateY(-6px)}

/* receipts */
.receipt{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:var(--s5);align-items:center}
.artifact{position:relative;transform:rotate(-1.4deg);margin:var(--s2)}
.artifact img{width:100%;display:block;border:6px solid #fff;box-shadow:0 14px 40px rgba(31,44,56,.22)}
.stamp{position:absolute;right:-14px;top:-20px;transform:rotate(6deg);font-family:var(--body);font-weight:800;font-size:.78rem;letter-spacing:.14em;color:var(--teal);border:3px double var(--teal);padding:8px 12px;background:rgba(248,244,234,.92);text-transform:uppercase}
.receipt .story p{margin-bottom:var(--s2)}
.receipt .story .big{font-family:var(--disp);font-size:1.3rem;line-height:1.5;color:var(--navy)}

/* record columns */
.record{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:var(--s5)}
.record h4{font-family:var(--disp);font-style:italic;font-weight:600;font-size:1.35rem;color:var(--navy);border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:6px}
ul.ledger{list-style:none}
ul.ledger li{padding:11px 0 11px 26px;position:relative;border-bottom:1px solid var(--line);font-size:.98rem;line-height:1.6}
ul.ledger li::before{content:"\2605";position:absolute;left:0;top:13px;color:var(--gold);font-size:.72rem}
.morelink{display:inline-block;margin-top:var(--s2);font-size:.9rem}

/* ask */
.ask .note{color:var(--muted);font-size:.95rem;max-width:34em}
form.f{display:grid;gap:var(--s2);max-width:36rem;margin-top:var(--s3)}
form.f label{font-weight:600;color:var(--navy);font-size:.88rem;letter-spacing:.02em}
form.f input,form.f textarea{width:100%;padding:13px;border:1px solid #b9c2c9;border-radius:3px;font-size:1rem;font-family:var(--body);background:#fffdf8;transition:border-color .2s}
form.f input:focus,form.f textarea:focus{border-color:var(--teal);outline:3px solid rgba(46,125,110,.25)}
.flash{padding:14px;border-radius:3px;display:none;font-weight:600;font-size:.95rem}
.flash.ok{display:block;background:#e7f0e9;color:#1d5c4e}.flash.err{display:block;background:#f5e9e7;color:#7c2d2d}
.qa{border-left:3px solid var(--gold);padding:var(--s2) var(--s3);margin-top:var(--s3);background:rgba(255,253,248,.7)}
.qa .q{font-family:var(--disp);font-weight:600;color:var(--navy)}
.qa .a{margin-top:8px;font-size:.97rem}
.note{font-size:.9rem;color:var(--muted)}

/* involved strip */
.strip{list-style:none}
.strip li{border-top:1px solid var(--line)}
.strip a{display:flex;justify-content:space-between;align-items:baseline;gap:var(--s3);padding:var(--s3) 4px;text-decoration:none;transition:background .2s}
.strip a:hover{background:rgba(198,156,109,.08)}
.strip .t{font-family:var(--disp);font-size:1.25rem;color:var(--navy)}
.strip .d{color:var(--muted);font-size:.9rem;flex:1}
.strip .arrow{color:var(--gold);font-size:1.3rem}

/* generic inner-page blocks */
.prose{max-width:44rem}
.prose p{margin-bottom:var(--s2)}
.lead{font-size:1.12rem;max-width:38em}
.grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:var(--s4)}
.panel{border:1px solid var(--line);background:rgba(255,253,248,.75);padding:var(--s3)}
.panel h3{font-size:1.3rem;margin-bottom:.4em}
.goal{border-top:1px solid var(--line);padding:var(--s3) 0}
.goal .n{font-family:var(--disp);font-style:italic;color:var(--gold);font-size:1.6rem;margin-right:10px}
.goal h3{display:inline;font-size:1.35rem}
.goal p{margin-top:10px;max-width:40em}

/* footer */
footer.paper{margin-top:var(--s6);border-top:1px solid var(--line);position:relative;text-align:center;padding:var(--s4) var(--s3) var(--s5);color:var(--muted);font-size:.85rem}
footer.paper::before{content:"";position:absolute;left:0;right:0;top:3px;border-top:1px solid var(--line)}
footer.paper .fstars{color:var(--gold);letter-spacing:.5em;font-size:.8rem}
footer.paper .elec{margin-top:var(--s2);font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--ink)}
footer.paper .links{margin-top:10px}

@media(max-width:820px){
 .hero{grid-template-columns:minmax(0,1fr);gap:var(--s4);padding:var(--s4) 0}
 .hero figure.portrait{max-width:430px;margin:0 auto;width:100%}
 .receipt,.record,.grid2{grid-template-columns:minmax(0,1fr);gap:var(--s4)}
 .record>div+div{border-top:1px solid var(--line);padding-top:var(--s3)}
}
@media(max-width:600px){
 body{font-size:16.5px}
 section.sec{padding:var(--s4) 0}
 .hero .actions{flex-direction:column;align-items:stretch;text-align:center}
 .artifact{transform:rotate(-1deg);margin:var(--s2) 0}
 .stamp{right:-4px;top:-16px;font-size:.7rem}
 nav.paper a{padding:4px 9px;font-size:.68rem}
}
"""

JS = r"""
async function pbPost(col, data, flash){
  try{
    const r = await fetch('pb/api/collections/'+col+'/records',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    if(!r.ok) throw new Error(await r.text());
    flash.className='flash ok'; return true;
  }catch(e){ flash.className='flash err'; return false; }
}
function wire(id, col, okMsg){
  const f=document.getElementById(id); if(!f) return;
  f.addEventListener('submit', async ev=>{
    ev.preventDefault();
    const fl=f.querySelector('.flash'); fl.textContent='Sending...'; fl.className='flash ok';
    const data=Object.fromEntries(new FormData(f).entries());
    if(await pbPost(col,data,fl)){ fl.textContent=okMsg; f.reset(); }
    else fl.textContent='Something went wrong sending that. Please try again, or email MarleneforLebanon@gmail.com';
  });
}
wire('askForm','questions','Thank you. Marlene reads every question and answers here on this page.');
wire('signForm','sign_requests','Thank you. Your yard sign request is in.');
wire('joinForm','signups','Thanks for signing up. You are on the list.');
wire('contactForm','messages','Message sent. Marlene will get back to you.');
(async ()=>{
  const box=document.getElementById('answered'); if(!box) return;
  try{
    const r=await fetch('pb/api/collections/questions/records?filter=(answered=true)&sort=-created&perPage=20');
    const j=await r.json();
    if(!j.items||!j.items.length){ box.innerHTML='<p class="note">Questions and answers will appear here as they come in.</p>'; return; }
    box.innerHTML=j.items.map(i=>'<div class="qa"><div class="q">Q: '+esc(i.question)+'</div><div class="a"><strong>Marlene:</strong> '+esc(i.answer)+'</div></div>').join('');
  }catch(e){ box.innerHTML='<p class="note">Questions and answers will appear here as they come in.</p>'; }
})();
function esc(s){const d=document.createElement('div');d.textContent=s||'';return d.innerHTML;}
"""

ELEC = "Paid for by Baldinger for Lebanon, 61 Brunswick Avenue, Lebanon NJ."
NAV = [("index.html","Home"),("meet-marlene.html","Meet Marlene"),
       ("promises.html","Her Record"),("priorities.html","Priorities"),
       ("articles.html","Articles"),("ask.html","Ask Marlene"),
       ("get-involved.html","Get Involved"),("contact.html","Contact")]

def page(fname, title, body, desc):
    links = "".join(f'<li><a href="{h}"{" class=\"on\"" if h==fname else ""}>{t}</a></li>' for h,t in NAV)
    mast_inner = 'Marlene Baldinger' if fname=="index.html" else '<a href="index.html">Marlene Baldinger</a>'
    mast = f'<h1 class="mast">{mast_inner}</h1>' if fname=="index.html" else f'<p class="mast">{mast_inner}</p>'
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%231c3447'/%3E%3Ctext x='16' y='23' font-size='18' text-anchor='middle' fill='%23c69c6d'%3E%E2%98%85%3C/text%3E%3C/svg%3E">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://acedigitalservicesco.com/work/marlene-baldinger/assets/marlene-portrait.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,900;1,9..144,400;1,9..144,600&family=Public+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={ASSET_V}"></head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <p class="dateline">Lebanon Borough &middot; Hunterdon County, New Jersey</p>
  {mast}
  <p class="mastsub">for Common Council &middot; Election Day is Tuesday, November 3, 2026</p>
  <nav class="paper" aria-label="Main"><ul>{links}</ul></nav>
</header>
<main id="main">{body}</main>
<footer class="paper"><div class="wrap">
  <div class="fstars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;</div>
  <div class="links"><a href="mailto:MarleneforLebanon@gmail.com">MarleneforLebanon@gmail.com</a> &middot; Facebook and Instagram coming soon</div>
  <div class="elec">{ELEC}</div>
</div></footer>
<script src="app.js?v={ASSET_V}"></script>
</body></html>"""
    open(os.path.join(OUT,fname),"w").write(html)

RUNSTATS = ["Elected Member of the Lebanon Borough Council for Nine Years",
"Lebanon Council Committee Memberships: Public Safety, Office of Emergency Management, Communication, Liaison to the School Board, Board of Health, Historical Committee",
"Lebanon Borough School Safety Team Member for Four Years",
"NYU Graduate and Critical Care Trained Registered Nurse",
"Director of Risk Management, Safety and Compliance, with Expertise in Health Care, Senior Care and Disabilities",
"Board Chair and Chair of the Risk Financing Committee for a NJ Health Care Organization",
"Public Lecturer on Health Care Quality and Patient Safety",
"Two Daughters, Graduates of LBS and North Hunterdon High School in 2022",
"Lebanon Borough Resident for 36 Years","Runner and Stand-Up Comedian"]
SERVICE = ["Respectful, Responsive and Timely Advocacy for ALL Residents",
"Worked Collaboratively and in Partnership with Mayor and Council for Critical Borough Improvements",
"Advanced Quality of Life Issues from Speeders to Signage",
"Budget Review: Asked Clarifying Questions. Only Council Member to Vote Against the Property Tax Increase for the Borough in 2022",
"Ensured Accurate and Timely Sharing of Information between Council and the Lebanon Borough Board of Education. Student, Family and Taxpayer Advocate",
"Outstanding Attendance at All Regularly Scheduled Council Meetings"]
VALUES = ["Trust, Integrity and Transparency Matter","Leadership and Experience Matter",
"Fiscal Accountability Matters","Public Safety and Security Matter",
"Our School and our Seniors Matter","Your Voice, Your Family, Our Community Matters"]
li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)

ASK_FORM = """<form class="f" id="askForm">
  <div><label for="qname">Your name</label><input id="qname" name="name" required maxlength="120"></div>
  <div><label for="qemail">Email (only so Marlene can follow up, never published)</label>
  <input id="qemail" name="email" type="email" required maxlength="200"></div>
  <div><label for="qq">Your question</label><textarea id="qq" name="question" rows="4" required maxlength="2000"></textarea></div>
  <button class="btn" type="submit">Submit your question</button>
  <div class="flash" role="status"></div>
</form>"""

page("index.html","Marlene Baldinger for Lebanon Borough Council",f"""
<div class="wrap">
 <div class="hero">
  <div>
   <p class="kick rise">Re-elect the Council President</p>
   <h2 class="rise">Running for what&rsquo;s <em>important to you.</em></h2>
   <p class="deck rise">A <strong>registered nurse</strong>, a <strong>36 year resident</strong>,
   and the neighbor who literally runs through town. She knocks on every door in the
   borough herself, and this year she is asking for your vote a third time.</p>
   <div class="actions rise">
    <a class="btn" href="ask.html">Ask Marlene a question</a>
    <a class="textlink" href="get-involved.html#sign">Request a yard sign &rarr;</a>
   </div>
  </div>
  <figure class="portrait rise">
   <img src="assets/marlene-portrait.jpg" alt="Marlene Baldinger outside the Lebanon Borough municipal building" width="1000" height="1502">
   <figcaption>Marlene outside the municipal building at Six High Street, August 2026.
   <span class="credit">Photograph: Ace Photography Co.</span></figcaption>
  </figure>
 </div>

 <section class="sec">
  <div class="sechead"><span class="star">&#9733;</span><h3>Promises made. <em>Promises kept.</em></h3><span class="rule"></span></div>
  <div class="receipt">
   <div class="artifact">
    <img src="assets/doorhanger-2023-goals.jpg" alt="The goals section of Marlene's 2023 door hanger, listing: Improve Communication, Livestream Council Meetings and have them accessible on the Borough Website">
    <span class="stamp">Delivered &middot; Aug 19, 2026</span>
   </div>
   <div class="story">
    <p class="big">This is her 2023 door hanger. Goal two reads: livestream council
    meetings and put them on the borough website.</p>
    <p>She was the only member of council pushing for it, and she kept pushing for nine
    years. On August 19, 2026, Lebanon Borough livestreamed a council meeting for the
    first time. You can now watch meetings live, or afterward, from home.</p>
    <p><a href="promises.html">Read her full record &rarr;</a></p>
   </div>
  </div>
 </section>

 <section class="sec">
  <div class="sechead"><span class="star">&#9733;</span><h3>The <em>record.</em></h3><span class="rule"></span></div>
  <div class="record">
   <div>
    <h4>Personal running stats</h4>
    <ul class="ledger">{li(RUNSTATS[:5])}</ul>
    <a class="morelink" href="meet-marlene.html">Meet Marlene, comedy training included &rarr;</a>
   </div>
   <div>
    <h4>Council service stats</h4>
    <ul class="ledger">{li(SERVICE[:5])}</ul>
    <a class="morelink" href="promises.html">The full ledger &rarr;</a>
   </div>
  </div>
 </section>

 <section class="sec ask">
  <div class="sechead"><span class="star">&#9733;</span><h3>Ask Marlene <em>anything.</em></h3><span class="rule"></span></div>
  <p class="note">Questions are answered here in public, like letters to the editor,
  so a neighbor wondering the same thing can see the answer too.</p>
  {ASK_FORM}
  <div id="answered" style="margin-top:var(--s4)"><p class="note">Loading&hellip;</p></div>
 </section>

 <section class="sec">
  <div class="sechead"><span class="star">&#9733;</span><h3>Lend a <em>hand.</em></h3><span class="rule"></span></div>
  <ul class="strip">
   <li><a href="get-involved.html#sign"><span class="t">Request a yard sign</span><span class="d">Signs go up in October. Ask now and yours will be there.</span><span class="arrow">&rarr;</span></a></li>
   <li><a href="get-involved.html"><span class="t">Get campaign updates</span><span class="d">An email now and then. No spam, stop any time.</span><span class="arrow">&rarr;</span></a></li>
   <li><a href="get-involved.html#donate"><span class="t">Support the campaign</span><span class="d">Almost entirely self run, door to door. Every bit helps with printing and signs.</span><span class="arrow">&rarr;</span></a></li>
  </ul>
 </section>
</div>
""","Marlene Baldinger, Council President, is running for re-election to the Lebanon Borough Common Council. Running for what's important to you.")

page("meet-marlene.html","Meet Marlene | Marlene Baldinger",f"""
<div class="wrap">
 <section class="sec" style="border-top:0">
  <div class="sechead"><span class="star">&#9733;</span><h3>Meet <em>Marlene.</em></h3><span class="rule"></span></div>
  <div class="grid2">
   <div class="prose">
    <p class="lead">Marlene Baldinger has lived in Lebanon Borough for 36 years. She is a
    registered nurse, a mother of two, and the current Council President. Before she ever
    ran for office, neighbors knew her as the woman who ran through town and stopped to
    talk. That is where her theme comes from: running for what&rsquo;s important to you.</p>
    <p>When she first ran nine years ago, council seats here went uncontested. She believed
    residents deserved a choice, so she gave them one, and she has knocked on every door in
    the borough each campaign since.</p>
    <p>And yes, the last line of the list is real. Every interviewer asks about it.</p>
   </div>
   <figure class="portrait">
    <img src="assets/marlene-portrait.jpg" alt="Marlene Baldinger" width="1000" height="1502">
    <figcaption>August 2026. <span class="credit">Photograph: Ace Photography Co.</span></figcaption>
   </figure>
  </div>
  <div style="margin-top:var(--s4)">
   <h4 style="font-family:var(--disp);font-style:italic;font-size:1.35rem;color:var(--navy);border-bottom:1px solid var(--line);padding-bottom:10px">Personal running stats</h4>
   <ul class="ledger">{li(RUNSTATS)}</ul>
  </div>
 </section>
</div>
""","About Marlene Baldinger: registered nurse, 36 year Lebanon Borough resident, Council President.")

page("promises.html","Her Record | Marlene Baldinger",f"""
<div class="wrap">
 <section class="sec" style="border-top:0">
  <div class="sechead"><span class="star">&#9733;</span><h3>Promises made. <em>Promises kept.</em></h3><span class="rule"></span></div>
  <p class="lead">Anyone can print a promise. Here is what happened to the ones Marlene printed.</p>
  <div class="receipt" style="margin-top:var(--s4)">
   <div class="artifact">
    <img src="assets/doorhanger-2023-goals.jpg" alt="The goals section of Marlene's 2023 door hanger">
    <span class="stamp">Delivered &middot; Aug 19, 2026</span>
   </div>
   <div class="story">
    <p class="big">Goal two on her 2023 card: livestream council meetings and put them on
    the borough website.</p>
    <p>She was the only member of council advocating for it, and it took nine years. On
    August 19, 2026, Lebanon Borough held its first livestreamed council meeting. Meetings
    can now be watched live or afterward, and the land use board is being added as well.</p>
   </div>
  </div>
  <div style="margin-top:var(--s5)">
   <h4 style="font-family:var(--disp);font-style:italic;font-size:1.35rem;color:var(--navy);border-bottom:1px solid var(--line);padding-bottom:10px">Council service stats</h4>
   <ul class="ledger">{li(SERVICE)}</ul>
  </div>
  <div style="margin-top:var(--s5)">
   <h4 style="font-family:var(--disp);font-style:italic;font-size:1.35rem;color:var(--navy);border-bottom:1px solid var(--line);padding-bottom:10px">What she stands for</h4>
   <ul class="ledger">{li(VALUES)}</ul>
  </div>
 </section>
</div>
""","Marlene Baldinger's record on the Lebanon Borough Council, anchored by the delivered promise of livestreamed council meetings.")

page("priorities.html","Priorities | Marlene Baldinger",f"""
<div class="wrap">
 <section class="sec" style="border-top:0">
  <div class="sechead"><span class="star">&#9733;</span><h3>Goals for a <em>third term.</em></h3><span class="rule"></span></div>
  <div class="goal"><span class="n">1.</span><h3>Reduce municipal taxes</h3>
   <p>Present a proposal for Zero Based Budgeting, with justification and documentation
   for all budget items from &ldquo;dollar one.&rdquo;</p></div>
  <div class="goal"><span class="n">2.</span><h3>Improve communication</h3>
   <p>Livestream council meetings and keep them accessible on the borough website to
   support access and transparency. Delivered August 19, 2026, and being expanded to the
   land use board.</p></div>
  <div class="goal"><span class="n">3.</span><h3>Enhance quality of life</h3>
   <p>Create a recreational hub for town gatherings, health and wellness, to include
   walking, running and biking paths, a community garden, and athletic fields or courts.</p></div>
 </section>
</div>
""","Marlene Baldinger's goals for her third term on the Lebanon Borough Council.")

page("articles.html","Articles | Marlene Baldinger",f"""
<div class="wrap">
 <section class="sec" style="border-top:0">
  <div class="sechead"><span class="star">&#9733;</span><h3>In the <em>papers.</em></h3><span class="rule"></span></div>
  <p class="lead">Press coverage about Marlene and her work on council will be collected
  here as the campaign goes on.</p>
  <p class="note" style="margin-top:var(--s3)">Articles are being gathered for this page.</p>
 </section>
</div>
""","News articles about Marlene Baldinger and her work for Lebanon Borough.")

page("ask.html","Ask Marlene a Question | Marlene Baldinger",f"""
<div class="wrap">
 <section class="sec ask" style="border-top:0">
  <div class="sechead"><span class="star">&#9733;</span><h3>Ask Marlene <em>anything.</em></h3><span class="rule"></span></div>
  <p class="lead">Ask about our town, a council decision, or anything the borough is
  working on. Marlene answers here, publicly, like letters to the editor, so a neighbor
  wondering the same thing can see the answer too.</p>
  {ASK_FORM}
  <h4 style="font-family:var(--disp);font-style:italic;font-size:1.35rem;color:var(--navy);margin-top:var(--s5);border-bottom:1px solid var(--line);padding-bottom:10px">Answered so far</h4>
  <div id="answered" style="margin-top:var(--s2)"><p class="note">Loading&hellip;</p></div>
 </section>
</div>
""","Ask Marlene Baldinger a question about Lebanon Borough and get a public answer.")

page("get-involved.html","Get Involved | Marlene Baldinger",f"""
<div class="wrap">
 <section class="sec" style="border-top:0">
  <div class="sechead"><span class="star">&#9733;</span><h3>Lend a <em>hand.</em></h3><span class="rule"></span></div>
  <div class="grid2">
   <div class="panel" id="sign"><h3>Request a yard sign</h3>
    <p class="note">Signs go up in October. Request one now and Marlene will make sure you get it.</p>
    <form class="f" id="signForm" style="margin-top:var(--s2)">
     <div><label for="sname">Name</label><input id="sname" name="name" required maxlength="120"></div>
     <div><label for="saddr">Address in Lebanon Borough</label><input id="saddr" name="address" required maxlength="240"></div>
     <div><label for="semail">Email</label><input id="semail" name="email" type="email" required maxlength="200"></div>
     <button class="btn" type="submit">Request a sign</button>
     <div class="flash" role="status"></div>
    </form></div>
   <div>
    <div class="panel"><h3>Stay in the loop</h3>
     <p class="note">Campaign updates by email. No spam, and you can stop any time.</p>
     <form class="f" id="joinForm" style="margin-top:var(--s2)">
      <div><label for="jemail">Email</label><input id="jemail" name="email" type="email" required maxlength="200"></div>
      <button class="btn" type="submit">Sign up</button>
      <div class="flash" role="status"></div>
     </form></div>
    <div class="panel" id="donate" style="margin-top:var(--s3)"><h3>Support the campaign</h3>
     <p>This campaign is almost entirely self run, door to door. Contributions help with
     printing, signs and materials.</p>
     <p style="margin-top:10px">Checks can be made out to <strong>Baldinger for Lebanon</strong>
     and mailed to 61 Brunswick Avenue, Lebanon NJ 08833.</p>
     <p class="note" style="margin-top:10px">Online contributions are coming soon. New Jersey
     election law requires every contribution to be recorded with the donor&rsquo;s name and
     address.</p></div>
   </div>
  </div>
 </section>
</div>
""","Volunteer, request a yard sign, or support Marlene Baldinger's campaign for Lebanon Borough Council.")

page("contact.html","Contact | Marlene Baldinger",f"""
<div class="wrap">
 <section class="sec" style="border-top:0">
  <div class="sechead"><span class="star">&#9733;</span><h3>Write to <em>Marlene.</em></h3><span class="rule"></span></div>
  <p class="lead">Email <a href="mailto:MarleneforLebanon@gmail.com">MarleneforLebanon@gmail.com</a>,
  talk to her at a council meeting, or catch her at your door. Or send a message here.</p>
  <form class="f" id="contactForm" style="margin-top:var(--s3)">
   <div><label for="cname">Name</label><input id="cname" name="name" required maxlength="120"></div>
   <div><label for="cemail">Email</label><input id="cemail" name="email" type="email" required maxlength="200"></div>
   <div><label for="cmsg">Message</label><textarea id="cmsg" name="message" rows="5" required maxlength="4000"></textarea></div>
   <button class="btn" type="submit">Send</button>
   <div class="flash" role="status"></div>
  </form>
 </section>
</div>
""","Contact Marlene Baldinger, Council President, Lebanon Borough NJ.")

open(os.path.join(OUT,"style.css"),"w").write(CSS)
open(os.path.join(OUT,"app.js"),"w").write(JS)
json.dump({
 "generated":"2026-08-18","status":"DEMO - not client approved yet",
 "design":"local-paper editorial, replaces the ChatGPT mock per Corey 2026-08-18 night",
 "claims":[
  {"claim":"All values, running stats, service stats, third-term goals","source":"2023 door hanger scan, transcribed verbatim in clients/marlene-baldinger/HISTORY.md"},
  {"claim":"Nine years on council","source":"2023 card said 'Six Years'; +3 years; matches her own 'nine years' on the 8/14 recording. CONFIRM with Marlene"},
  {"claim":"Election date Tuesday November 3 2026","source":"Vault session log 2026-07-11. Marlene said 'November 2nd, could be wrong'. CONFIRM"},
  {"claim":"First livestream August 19 2026 + land use board being added","source":"8/14 transcript; promo video 8/18"},
  {"claim":"Door hanger artifact image","source":"Real scan of her 2023 card (goals section crop), not a mockup"},
  {"claim":"Only council member to vote against 2022 property tax increase","source":"Her printed 2023 card, verbatim"},
  {"claim":"ELEC footer text","source":"Printed verbatim on her 2023 door hanger. CONFIRM address current"},
  {"claim":"ZIP 08833 on donate panel","source":"INFERRED, not on the card. CONFIRM"},
  {"claim":"Photo credit Ace Photography Co.","source":"Corey shot the portrait 2026-08-14"}
 ]}, open(os.path.join(OUT,".claims.json"),"w"), indent=1)
print("built", len([f for f in os.listdir(OUT) if f.endswith('.html')]), "pages, asset v", ASSET_V)
