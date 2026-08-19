#!/usr/bin/env python3
"""Generates the Marlene Baldinger campaign demo. Content is verbatim from her
2023 door hanger (scanned 2026-08-15) and the 2026-08-14 meeting transcript.
Do not invent facts. Sidecar: .claims.json"""
import os, json
OUT = os.path.dirname(os.path.abspath(__file__))
CSS = """
:root{--navy:#1c3447;--teal:#2e8b7a;--gold:#c69c6d;--red:#722727;--bg:#fdfcfa;--ink:#22303c}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);font-size:18px;line-height:1.65}
h1,h2,h3,.serif{font-family:Baskerville,Georgia,'Times New Roman',serif}
a{color:var(--teal)}
.wrap{max-width:1060px;margin:0 auto;padding:0 20px}
header.site{background:var(--navy);color:#fff;border-bottom:4px solid var(--gold)}
.brand{display:flex;align-items:center;justify-content:space-between;padding:14px 0;gap:12px;flex-wrap:wrap}
.brand .name{font-family:Baskerville,Georgia,serif;font-size:1.5rem;letter-spacing:.06em;color:#fff;text-decoration:none}
.brand .name small{display:block;font-size:.72rem;letter-spacing:.22em;color:var(--gold);font-family:inherit}
.stars{color:var(--teal);letter-spacing:.3em;font-size:.9rem}
nav.main{background:#16293a}
nav.main ul{display:flex;flex-wrap:wrap;list-style:none;gap:2px}
nav.main a{display:block;padding:11px 14px;color:#e8edf2;text-decoration:none;font-size:.92rem}
nav.main a:hover,nav.main a.on{background:var(--teal);color:#fff}
.hero{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:36px;align-items:center;padding:52px 0}
.hero .kicker{color:var(--teal);letter-spacing:.18em;font-weight:600;font-size:.95rem}
.hero h1{font-size:clamp(2.4rem,6vw,4rem);line-height:1.05;color:var(--navy);margin:.2em 0 .35em}
.hero h1 em{color:var(--teal);font-style:italic}
.hero .sub{color:var(--red);font-weight:600;letter-spacing:.04em}
.hero img{width:100%;height:auto;border-radius:8px;box-shadow:0 12px 34px rgba(28,52,71,.25)}
.rule{border:none;border-top:3px solid var(--gold);width:130px;margin:26px 0}
.btnrow{display:flex;gap:14px;flex-wrap:wrap;margin-top:26px}
.btn{display:inline-block;padding:14px 22px;border-radius:6px;text-decoration:none;font-weight:700;font-size:1rem}
.btn.teal{background:var(--teal);color:#fff}.btn.navy{background:var(--navy);color:#fff}.btn.ghost{border:2px solid var(--navy);color:var(--navy)}
.band{background:var(--navy);color:#fff;padding:34px 0;font-size:1.25rem}
.band .gold{color:var(--gold);font-style:italic}
section.block{padding:54px 0}
section.alt{background:#f2efe9}
h2.sec{font-size:2rem;color:var(--navy);margin-bottom:.35em}
.lead{max-width:46rem}
.grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:34px}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
ul.stats{list-style:none;margin-top:14px}
ul.stats li{padding:10px 0 10px 30px;position:relative;border-bottom:1px solid #e4ded4}
ul.stats li::before{content:"\\2605";position:absolute;left:2px;color:var(--teal);font-size:.85rem;top:13px}
.card{background:#fff;border:1px solid #e4ded4;border-radius:8px;padding:26px}
.card h3{color:var(--navy);margin-bottom:.4em}
.promise{border-left:5px solid var(--gold);background:#fff;padding:26px;border-radius:0 8px 8px 0;margin-top:22px}
.promise .tag{display:inline-block;background:var(--teal);color:#fff;font-size:.8rem;font-weight:700;letter-spacing:.08em;padding:4px 10px;border-radius:4px;margin-bottom:10px}
form.f{display:grid;gap:14px;max-width:34rem}
form.f label{font-weight:600;color:var(--navy);font-size:.95rem}
form.f input,form.f textarea{width:100%;padding:12px;border:2px solid #cfd8de;border-radius:6px;font-size:1rem;font-family:inherit}
form.f input:focus,form.f textarea:focus{outline:3px solid var(--teal);border-color:var(--teal)}
.note{font-size:.9rem;color:#5c6b76}
.flash{padding:14px;border-radius:6px;display:none;font-weight:600}
.flash.ok{display:block;background:#e5f2ee;color:#1d5c4e}.flash.err{display:block;background:#f7e8e8;color:#7c2d2d}
.qa{background:#fff;border:1px solid #e4ded4;border-radius:8px;padding:22px;margin-top:16px}
.qa .q{font-weight:700;color:var(--navy)}
.qa .a{margin-top:8px}
footer.site{background:var(--navy);color:#cfd8de;margin-top:60px;padding:34px 0;font-size:.92rem}
footer.site .elec{color:#fff;font-weight:600;margin-top:10px}
.skip{position:absolute;left:-9999px}.skip:focus{position:static;display:block;background:var(--gold);color:var(--navy);padding:10px}
@media(max-width:760px){
 .brand .name{font-size:1.15rem}
 .brand .name small{letter-spacing:.12em}
 .hero{grid-template-columns:minmax(0,1fr);padding:34px 0}
 .hero img{max-width:340px;justify-self:center;order:-1}
 .grid2,.grid3{grid-template-columns:minmax(0,1fr)}
 nav.main ul{justify-content:center}
 body{font-size:17px}
}

/* ==== GPT-mock layout ==== */
.lockup{display:flex;align-items:center;gap:14px;text-decoration:none}
.lockup .runner{width:46px;height:56px;color:var(--gold)}
.lockup .lines{line-height:1.1}
.lockup .l1{color:var(--gold);font-family:Baskerville,Georgia,serif;letter-spacing:.30em;font-size:.95rem}
.lockup .l2{color:#fff;font-family:Baskerville,Georgia,serif;font-size:1.9rem;letter-spacing:.05em}
.lockup .l3{color:var(--gold);letter-spacing:.28em;font-size:.66rem;border-top:1px solid rgba(198,156,109,.6);border-bottom:1px solid rgba(198,156,109,.6);padding:2px 0;margin-top:3px}
.lockup .l4{color:#fff;letter-spacing:.18em;font-size:.62rem;margin-top:3px}
.burger{background:none;border:0;cursor:pointer;padding:10px}
.burger span{display:block;width:30px;height:3px;background:#fff;margin:6px 0;border-radius:2px}
#menu{display:none;background:#16293a}
#menu.open{display:block}
#menu ul{list-style:none;display:flex;flex-direction:column}
#menu a{display:block;padding:13px 20px;color:#e8edf2;text-decoration:none;border-top:1px solid rgba(255,255,255,.07)}
#menu a:hover{background:var(--teal)}
.hero2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:stretch}
.hero2 .txt{padding:56px 6% 56px max(20px,calc((100vw - 1060px)/2));background:var(--bg)}
.hero2 .pic{position:relative;min-height:420px}
.hero2 .pic img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:top center}
.hero2 .kicker{color:var(--teal);letter-spacing:.2em;font-weight:700;font-size:1rem;font-family:Baskerville,Georgia,serif}
.hero2 h1{font-size:clamp(2.6rem,5.4vw,4.2rem);line-height:1.02;color:var(--navy);margin:.15em 0 .3em}
.hero2 h1 em{color:var(--teal);font-style:italic}
.goldrule{display:flex;align-items:center;gap:10px;margin:18px 0;color:var(--gold)}
.goldrule::before,.goldrule::after{content:"";flex:0 0 120px;border-top:2px solid var(--gold)}
.hero2 .who{font-family:Baskerville,Georgia,serif;font-size:1.25rem;color:var(--navy)}
.hero2 .meta1{color:var(--teal);font-weight:700;letter-spacing:.06em;font-size:.95rem;margin-top:8px}
.hero2 .meta2{color:var(--navy);letter-spacing:.06em;font-size:.9rem}
.btn .ic{width:20px;height:20px;vertical-align:-4px;margin-right:9px}
.band2{background:var(--navy);color:#fff;padding:36px 0}
.band2 .wrap{display:flex;align-items:center;gap:26px;justify-content:space-between;flex-wrap:wrap}
.band2 .t1{font-family:Baskerville,Georgia,serif;font-size:1.45rem}
.band2 .t2{color:var(--gold);font-style:italic;font-family:Baskerville,Georgia,serif;font-size:1.3rem;margin-top:6px}
.band2 .runner{width:110px;height:78px;color:var(--teal);flex:0 0 auto}
.statsrow{display:grid;grid-template-columns:minmax(0,1fr) 60px minmax(0,1fr);gap:10px;align-items:center;padding:46px 0}
.statcell{display:flex;gap:18px;align-items:flex-start}
.statcell .ic{width:74px;height:74px;color:var(--teal);flex:0 0 auto}
.statcell .k{color:var(--teal);letter-spacing:.12em;font-weight:700;font-size:.95rem}
.statcell h3{font-family:Baskerville,Georgia,serif;font-size:1.7rem;color:var(--navy)}
.statcell p{color:#5c6b76;margin-top:6px}
.statdiv{display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--gold)}
.statdiv::before,.statdiv::after{content:"";width:2px;height:52px;background:var(--gold)}
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;padding:10px 0 40px}
.tile{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid #e4ded4;border-radius:10px;padding:18px 16px;text-decoration:none;color:var(--navy);font-weight:700;font-size:.95rem;box-shadow:0 2px 6px rgba(28,52,71,.06)}
.tile .ic{width:34px;height:34px;color:var(--teal);flex:0 0 auto}
.tile .chev{margin-left:auto;color:var(--gold);font-size:1.2rem}
.tile:hover{border-color:var(--teal)}
.ctaband{background:var(--teal);color:#fff;border-radius:12px;padding:30px;display:flex;align-items:center;gap:24px;flex-wrap:wrap;margin:10px 0 26px}
.ctaband .ic{width:72px;height:72px;flex:0 0 auto;opacity:.9}
.ctaband h3{font-size:1.4rem;letter-spacing:.04em}
.ctaband p{margin-top:6px;max-width:34rem}
.ctaband .btn{background:#fff;color:var(--teal);margin-left:auto;white-space:nowrap}
.signcard{background:#fff;border:1px solid #e4ded4;border-radius:12px;padding:30px;display:flex;gap:26px;align-items:center;flex-wrap:wrap;margin-bottom:40px}
.minisign{flex:0 0 190px;border:2px solid #d8d2c6;border-radius:4px;padding:14px 10px;text-align:center;background:#fff;box-shadow:0 4px 10px rgba(28,52,71,.10)}
.minisign .m1{font-family:Baskerville,Georgia,serif;color:var(--navy);font-size:1rem;letter-spacing:.04em}
.minisign .m2{color:var(--gold);font-size:.55rem;letter-spacing:.2em;border-top:1px solid var(--gold);border-bottom:1px solid var(--gold);padding:2px 0;margin:4px 6px}
.minisign .m3{color:var(--teal);font-size:.55rem;letter-spacing:.08em;margin-top:5px}
.minisign .legs{display:flex;justify-content:space-around;margin-top:10px}
.minisign .legs i{width:5px;height:22px;background:#b9b2a5;display:block}
.signcard h3{font-family:Baskerville,Georgia,serif;color:var(--navy);font-size:1.5rem}
.signcard .sub{color:var(--teal);font-weight:700;letter-spacing:.1em;font-size:.95rem}
.signcard .btn{margin-left:auto;white-space:nowrap}
footer.site{text-align:center;border-top:4px solid var(--gold)}
footer.site .elec{letter-spacing:.18em;font-size:.8rem;text-transform:uppercase}
.socials{display:flex;gap:14px;justify-content:center;margin-top:16px}
.socials a{display:flex;width:40px;height:40px;border-radius:50%;background:#243c52;color:#fff;align-items:center;justify-content:center;text-decoration:none}
.socials svg{width:18px;height:18px}
@media(max-width:860px){
 .hero2{grid-template-columns:minmax(0,1fr)}
 .hero2 .pic{min-height:340px;order:-1}
 .tiles{grid-template-columns:repeat(2,minmax(0,1fr))}
 .statsrow{grid-template-columns:minmax(0,1fr)}
 .statdiv{flex-direction:row}.statdiv::before,.statdiv::after{width:52px;height:2px}
 .ctaband .btn,.signcard .btn{margin-left:0}
}
"""
JS = """
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
wire('askForm','questions','Thank you! Marlene reads every question and answers here on this page.');
wire('signForm','sign_requests','Thank you! Your yard sign request is in.');
wire('joinForm','signups','Thanks for signing up! You are on the list.');
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
document.getElementById('burger')?.addEventListener('click',()=>{
  const m=document.getElementById('menu'); m.classList.toggle('open');
  document.getElementById('burger').setAttribute('aria-expanded', m.classList.contains('open'));
});
function esc(s){const d=document.createElement('div');d.textContent=s||'';return d.innerHTML;}
"""

RUNNER = """<svg class="{cls}" viewBox="0 0 90 64" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="57" cy="10" r="6.5" fill="currentColor" stroke="none"/><path d="M53 18 43 30l12 8-4 16"/><path d="M43 30l-9 6-10-2M55 26l12 4 9-3M51 38 38 50l-11 3"/><path d="M4 22h14M2 34h10M6 46h12" stroke-width="3.5" opacity=".75"/></svg>"""
IC = {
 "ask": '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/></svg>',
 "sign": '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 4h18v9H3zM7 13h2v7H7zM15 13h2v7h-2z"/></svg>',
 "person": '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="12" cy="7" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7z"/></svg>',
 "check": '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm-1.2 14.6-4.3-4.3 1.7-1.7 2.6 2.6 5.8-5.8 1.7 1.7z"/></svg>',
 "flag": '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 2h2v20H5zM9 3h11l-3 4.5L20 12H9z"/></svg>',
 "news": '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 4h15v14a2 2 0 0 0 2 2H5a2 2 0 0 1-2-2zm18 4h-2v10a1 1 0 0 0 2 0zM6 7h9v4H6zm0 6h9v2H6zm0 3.5h9v2H6z"/></svg>',
 "q": '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 3h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H10l-6 5v-5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm7.1 10.6h2v2h-2zm3.6-6.1c0 1.3-.7 2-1.6 2.7-.7.5-1 .8-1 1.6h-2c0-1.5.7-2.2 1.6-2.9.6-.5 1--.8 1-1.4 0-.8-.6-1.3-1.5-1.3s-1.6.6-1.7 1.5H7.4c.1-2 1.7-3.4 3.8-3.4 2.1 0 3.5 1.3 3.5 3.2z"/></svg>',
 "people": '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="8" cy="8" r="3.4"/><circle cx="16.5" cy="9" r="2.8"/><path d="M1.5 20c0-3.4 2.9-5.8 6.5-5.8s6.5 2.4 6.5 5.8zM15.4 20c0-2 .9-3.7 2.3-4.8 2.7.4 4.8 2.4 4.8 4.8z"/></svg>',
 "mail": '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M2 5h20v14H2zm2 2 8 6 8-6"/><path d="M4 7l8 6 8-6" fill="none" stroke="#fff" stroke-width="1.6"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.1c0-.9.3-1.5 1.6-1.5h1.3V4.9c-.3 0-1.1-.1-2-.1-2.1 0-3.5 1.3-3.5 3.6V11H8.5v3h2.4v7z"/></svg>',
}

ELEC = "Paid for by Baldinger for Lebanon, 61 Brunswick Avenue, Lebanon NJ."
def page(fname, title, active, body, desc):
    nav = [("index.html","Home"),("meet-marlene.html","Meet Marlene"),
           ("promises.html","Promises Made, Promises Kept"),("priorities.html","Priorities"),
           ("articles.html","Articles"),("ask.html","Ask Marlene"),
           ("get-involved.html","Get Involved"),("contact.html","Contact")]
    links = "".join(f'<li><a href="{h}"{" class=\"on\"" if h==fname else ""}>{t}</a></li>' for h,t in nav)
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="style.css?v=100781"></head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap brand">
  <a class="lockup" href="index.html" aria-label="Marlene Baldinger home">
    {RUNNER.format(cls="runner")}
    <span class="lines">
      <span class="l1">MARLENE</span><br>
      <span class="l2">BALDINGER</span>
      <span class="l3" style="display:block">COUNCIL PRESIDENT</span>
      <span class="l4" style="display:block">LEBANON BOROUGH COMMON COUNCIL</span>
    </span>
  </a>
  <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
</div>
<nav id="menu" aria-label="Main"><ul>{links}</ul></nav>
</header>
<main id="main">{body}</main>
<footer class="site"><div class="wrap">
  <div class="elec">{ELEC}</div>
  <div class="socials">
    <a href="#" aria-label="Facebook (coming soon)">{IC["fb"]}</a>
    <a href="mailto:MarleneforLebanon@gmail.com" aria-label="Email">{IC["mail"]}</a>
  </div>
</div></footer>
<script src="app.js?v=100781"></script>
</body></html>"""
    open(os.path.join(OUT,fname),"w").write(html)

VALUES = ["Trust, Integrity and Transparency Matter","Leadership and Experience Matter",
"Fiscal Accountability Matters","Public Safety and Security Matter",
"Our School and our Seniors Matter","Your Voice, Your Family, Our Community Matters"]
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

li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)

page("index.html","Marlene Baldinger for Lebanon Borough Council","index.html",f"""
<div class="hero2">
 <div class="txt">
  <div class="kicker">RUNNING FOR</div>
  <h1>What&rsquo;s<br>Important<br><em>to You</em></h1>
  <div class="goldrule">&#9733;</div>
  <p class="who">Council President Marlene Baldinger</p>
  <p class="meta1">RUNNING FOR RE-ELECTION &bull; NOVEMBER 2026</p>
  <p class="meta2">LEBANON BOROUGH &bull; HUNTERDON COUNTY, NEW JERSEY</p>
  <div class="btnrow">
   <a class="btn teal" href="ask.html">{IC["ask"]}ASK MARLENE A QUESTION</a>
   <a class="btn navy" href="get-involved.html#sign">{IC["sign"]}REQUEST A YARD SIGN</a>
  </div>
 </div>
 <div class="pic"><img src="assets/marlene-portrait.jpg" alt="Marlene Baldinger outside the Lebanon Borough municipal building"></div>
</div>
<div class="band2"><div class="wrap">
 <div>
  <div class="t1">A registered nurse. A 36 year resident. I knock on every door.</div>
  <div class="t2">I run through our town, and I run for you.</div>
 </div>
 {RUNNER.format(cls="runner")}
</div></div>
<div class="wrap statsrow">
 <div class="statcell">{RUNNER.format(cls="ic")}<div>
  <div class="k">PERSONAL</div><h3>RUNNING STATS</h3>
  <p>Nurse, mom, 36 year resident, and yes, trained stand-up comedian.
  <a href="meet-marlene.html">Meet Marlene &rarr;</a></p></div></div>
 <div class="statdiv">&#9733;</div>
 <div class="statcell"><svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2 2 8h20zM4 10h3v8H4zm6.5 0h3v8h-3zM17 10h3v8h-3zM2 20h20v2H2z"/></svg><div>
  <div class="k">COUNCIL SERVICE</div><h3>STATS</h3>
  <p>Nine years on council, and a promise she printed in 2023 delivered in 2026.
  <a href="promises.html">See the record &rarr;</a></p></div></div>
</div>
<div class="wrap">
 <div class="tiles">
  <a class="tile" href="meet-marlene.html">{IC["person"]}MEET MARLENE<span class="chev">&rsaquo;</span></a>
  <a class="tile" href="promises.html">{IC["check"]}PROMISES MADE, PROMISES KEPT<span class="chev">&rsaquo;</span></a>
  <a class="tile" href="priorities.html">{IC["flag"]}PRIORITIES<span class="chev">&rsaquo;</span></a>
  <a class="tile" href="articles.html">{IC["news"]}ARTICLES<span class="chev">&rsaquo;</span></a>
  <a class="tile" href="ask.html">{IC["q"]}ASK MARLENE A QUESTION<span class="chev">&rsaquo;</span></a>
  <a class="tile" href="get-involved.html#sign">{IC["sign"]}GET A YARD SIGN<span class="chev">&rsaquo;</span></a>
  <a class="tile" href="get-involved.html">{IC["people"]}GET INVOLVED<span class="chev">&rsaquo;</span></a>
  <a class="tile" href="contact.html">{IC["mail"]}CONTACT<span class="chev">&rsaquo;</span></a>
 </div>
 <div class="ctaband">
  {IC["q"].replace('class="ic"','class="ic" style="width:72px;height:72px"')}
  <div><h3>ASK MARLENE A QUESTION</h3>
  <p>Have a question about our town or council decisions? Submit it and Marlene will
  answer it here for everyone.</p></div>
  <a class="btn" href="ask.html">SUBMIT A QUESTION</a>
 </div>
 <div class="signcard">
  <div class="minisign" aria-hidden="true">
   <div class="m1">MARLENE<br>BALDINGER</div>
   <div class="m2">COUNCIL PRESIDENT</div>
   <div class="m3">RUNNING FOR WHAT&rsquo;S<br>IMPORTANT TO YOU</div>
   <div class="legs"><i></i><i></i></div>
  </div>
  <div><h3>HELP SPREAD THE WORD</h3>
  <div class="sub">REQUEST A YARD SIGN</div>
  <p style="margin-top:8px;max-width:26rem">Yard signs help more neighbors learn about
  the campaign. Request yours today!</p></div>
  <a class="btn navy" href="get-involved.html#sign">REQUEST A YARD SIGN</a>
 </div>
</div>
""","Marlene Baldinger, Council President, is running for re-election to the Lebanon Borough Common Council. Running for what's important to you.")

page("meet-marlene.html","Meet Marlene | Marlene Baldinger","meet-marlene.html",f"""
<section class="block"><div class="wrap">
 <h2 class="sec">Meet Marlene</h2>
 <div class="grid2">
  <div>
   <p class="lead">Marlene Baldinger has lived in Lebanon Borough for 36 years. She is a
   registered nurse, a mother of two, and the current Council President. Before she ever
   ran for office, neighbors knew her as the woman who ran through town and stopped to
   talk. That is where her theme comes from: running for what&rsquo;s important to you.</p>
   <p style="margin-top:14px">When she first ran nine years ago, council seats here went
   uncontested. She believed residents deserved a choice, so she gave them one, and she
   has knocked on every door in the borough each campaign since.</p>
   <p style="margin-top:14px">And yes, the last line below is real. Every interviewer asks.</p>
  </div>
  <img src="assets/marlene-portrait.jpg" alt="Marlene Baldinger" style="border-radius:8px;max-width:340px;width:100%;justify-self:center">
 </div>
 <h3 style="margin-top:40px;color:var(--navy)">Here are my Personal Running Stats</h3>
 <ul class="stats">{li(RUNSTATS)}</ul>
</div></section>
""","About Marlene Baldinger: registered nurse, 36 year Lebanon Borough resident, Council President.")

page("promises.html","Promises Made, Promises Kept | Marlene Baldinger","promises.html",f"""
<section class="block"><div class="wrap">
 <h2 class="sec">Promises Made, Promises Kept</h2>
 <p class="lead">Anyone can print a promise. Here is what happened to the ones Marlene printed.</p>
 <div class="promise">
  <span class="tag">PROMISED 2023 &middot; DELIVERED AUGUST 19, 2026</span>
  <h3>Livestreamed council meetings</h3>
  <p>Her 2023 campaign card listed a goal, word for word: &ldquo;Improve Communication.
  Livestream Council Meetings and have them accessible on the Borough Website to support
  access and transparency.&rdquo; She was the only member of council pushing for it, and she
  kept pushing for nine years. On August 19, 2026, Lebanon Borough livestreamed a council
  meeting for the first time. Meetings are now available to watch live or afterward, and
  the land use board is being added as well.</p>
 </div>
 <h3 style="margin-top:40px;color:var(--navy)">Here are My Council Service Stats</h3>
 <ul class="stats">{li(SERVICE)}</ul>
</div></section>
""","Marlene Baldinger's record on the Lebanon Borough Council, anchored by the delivered promise of livestreamed council meetings.")

page("priorities.html","Priorities | Marlene Baldinger","priorities.html",f"""
<section class="block"><div class="wrap">
 <h2 class="sec">Goals for My Third Term</h2>
 <div class="grid3" style="margin-top:22px">
  <div class="card"><h3>1. Reduce Municipal Taxes</h3>
  <p>Present a proposal for Zero Based Budgeting, with justification and documentation
  for all budget items from &ldquo;dollar one.&rdquo;</p></div>
  <div class="card"><h3>2. Improve Communication</h3>
  <p>Livestream council meetings and keep them accessible on the borough website to
  support access and transparency. Delivered August 19, 2026, and being expanded.</p></div>
  <div class="card"><h3>3. Enhance Quality of Life</h3>
  <p>Create a recreational hub for town gatherings, health and wellness, to include
  walking, running and biking paths, a community garden, and athletic fields or courts.</p></div>
 </div>
</div></section>
""","Marlene Baldinger's goals for her third term on the Lebanon Borough Council.")

page("articles.html","Articles | Marlene Baldinger","articles.html",f"""
<section class="block"><div class="wrap">
 <h2 class="sec">Articles</h2>
 <p class="lead">Press coverage about Marlene and her work on council will be collected
 here as the campaign goes on.</p>
 <div class="card" style="margin-top:22px"><h3>Coming soon</h3>
 <p class="note">Articles are being gathered for this page.</p></div>
</div></section>
""","News articles about Marlene Baldinger and her work for Lebanon Borough.")

page("ask.html","Ask Marlene a Question | Marlene Baldinger","ask.html",f"""
<section class="block"><div class="wrap">
 <h2 class="sec">Ask Marlene a Question</h2>
 <p class="lead">Ask about our town, a council decision, or anything the borough is
 working on. Marlene answers here, publicly, so neighbors with the same question can
 see the answer too. That is the point: connecting the dots between listening and leading.</p>
 <form class="f" id="askForm" style="margin-top:24px">
  <div><label for="qname">Your name</label><input id="qname" name="name" required maxlength="120"></div>
  <div><label for="qemail">Email (only so Marlene can follow up, never published)</label>
  <input id="qemail" name="email" type="email" required maxlength="200"></div>
  <div><label for="qq">Your question</label><textarea id="qq" name="question" rows="4" required maxlength="2000"></textarea></div>
  <button class="btn teal" type="submit">Submit your question</button>
  <div class="flash" role="status"></div>
 </form>
 <h3 style="margin-top:44px;color:var(--navy)">Answered so far</h3>
 <div id="answered"><p class="note">Loading&hellip;</p></div>
</div></section>
""","Ask Marlene Baldinger a question about Lebanon Borough and get a public answer.")

page("get-involved.html","Get Involved | Marlene Baldinger","get-involved.html",f"""
<section class="block"><div class="wrap">
 <h2 class="sec">Get Involved</h2>
 <div class="grid2" style="margin-top:20px">
  <div class="card" id="sign"><h3>Request a yard sign</h3>
  <p>Signs go up in October. Request one now and Marlene will make sure you get it.</p>
  <form class="f" id="signForm" style="margin-top:16px">
   <div><label for="sname">Name</label><input id="sname" name="name" required maxlength="120"></div>
   <div><label for="saddr">Address in Lebanon Borough</label><input id="saddr" name="address" required maxlength="240"></div>
   <div><label for="semail">Email</label><input id="semail" name="email" type="email" required maxlength="200"></div>
   <button class="btn navy" type="submit">Request a sign</button>
   <div class="flash" role="status"></div>
  </form></div>
  <div>
   <div class="card"><h3>Stay in the loop</h3>
   <p>Campaign updates by email. No spam, and you can stop any time.</p>
   <form class="f" id="joinForm" style="margin-top:16px">
    <div><label for="jemail">Email</label><input id="jemail" name="email" type="email" required maxlength="200"></div>
    <button class="btn teal" type="submit">Sign up</button>
    <div class="flash" role="status"></div>
   </form></div>
   <div class="card" style="margin-top:24px"><h3>Donate</h3>
   <p>This campaign is almost entirely self run, door to door. Contributions help with
   printing, signs and materials.</p>
   <p style="margin-top:10px">Checks can be made out to <strong>Baldinger for Lebanon</strong>
   and mailed to 61 Brunswick Avenue, Lebanon NJ 08833.</p>
   <p class="note" style="margin-top:10px">Online contributions are coming soon. New Jersey
   election law requires every contribution to be recorded with the donor&rsquo;s name and
   address.</p></div>
  </div>
 </div>
</div></section>
""","Volunteer, request a yard sign, or support Marlene Baldinger's campaign for Lebanon Borough Council.")

page("contact.html","Contact | Marlene Baldinger","contact.html",f"""
<section class="block"><div class="wrap">
 <h2 class="sec">Contact Marlene</h2>
 <p class="lead">Email <a href="mailto:MarleneforLebanon@gmail.com">MarleneforLebanon@gmail.com</a>,
 talk to her at a council meeting, or catch her at your door. Or send a message here.</p>
 <form class="f" id="contactForm" style="margin-top:24px">
  <div><label for="cname">Name</label><input id="cname" name="name" required maxlength="120"></div>
  <div><label for="cemail">Email</label><input id="cemail" name="email" type="email" required maxlength="200"></div>
  <div><label for="cmsg">Message</label><textarea id="cmsg" name="message" rows="5" required maxlength="4000"></textarea></div>
  <button class="btn teal" type="submit">Send</button>
  <div class="flash" role="status"></div>
 </form>
</div></section>
""","Contact Marlene Baldinger, Council President, Lebanon Borough NJ.")

open(os.path.join(OUT,"style.css"),"w").write(CSS)
open(os.path.join(OUT,"app.js"),"w").write(JS)
json.dump({
 "generated":"2026-08-18","status":"DEMO - not client approved yet",
 "claims":[
  {"claim":"All values, running stats, service stats, third-term goals","source":"2023 door hanger, scanned 2026-08-15 (~/Desktop/marlene-doorhanger-*.jpg), transcribed verbatim in clients/marlene-baldinger/HISTORY.md"},
  {"claim":"Nine years on council","source":"2023 card said 'Six Years'; +3 years; matches her own 'nine years' in 2026-08-14 transcript. CONFIRM with Marlene before print/live"},
  {"claim":"Election date Tuesday November 3 2026","source":"Vault session log 2026-07-11 (re-election Nov 3 2026). Marlene said 'I believe November 2nd' on 8/14 - vault date used. CONFIRM"},
  {"claim":"First livestream August 19 2026","source":"2026-08-14 transcript + promo video shoot 2026-08-18"},
  {"claim":"Livestream promise printed 2023","source":"Door hanger back, Goal 2, verbatim"},
  {"claim":"Only council member to vote against 2022 property tax increase","source":"Her printed 2023 card, verbatim. Her claim, on her material"},
  {"claim":"ELEC footer 'Paid for by Baldinger for Lebanon, 61 Brunswick Avenue, Lebanon NJ.'","source":"Printed verbatim on her 2023 door hanger. CONFIRM address still current"},
  {"claim":"ZIP 08833 on donate page","source":"INFERRED from Lebanon NJ - NOT on the card. CONFIRM"}
 ]}, open(os.path.join(OUT,".claims.json"),"w"), indent=1)
print("built", len([f for f in os.listdir(OUT) if f.endswith('.html')]), "pages")
