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
 .hero{grid-template-columns:minmax(0,1fr);padding:34px 0}
 .hero img{max-width:340px;justify-self:center;order:-1}
 .grid2,.grid3{grid-template-columns:minmax(0,1fr)}
 nav.main ul{justify-content:center}
 body{font-size:17px}
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
function esc(s){const d=document.createElement('div');d.textContent=s||'';return d.innerHTML;}
"""
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
<link rel="stylesheet" href="style.css"></head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap brand">
  <a class="name" href="index.html">MARLENE BALDINGER<small>COUNCIL PRESIDENT &middot; LEBANON BOROUGH</small></a>
  <div class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;</div>
</div>
<nav class="main" aria-label="Main"><div class="wrap"><ul>{links}</ul></div></nav>
</header>
<main id="main">{body}</main>
<footer class="site"><div class="wrap">
  <div>Marlene is Running for What&rsquo;s Important to You</div>
  <div>Email: <a href="mailto:MarleneforLebanon@gmail.com" style="color:#fff">MarleneforLebanon@gmail.com</a></div>
  <div class="elec">{ELEC}</div>
</div></footer>
<script src="app.js"></script>
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
<div class="wrap hero">
 <div>
  <div class="kicker">RUNNING FOR</div>
  <h1>What&rsquo;s Important <em>to You</em></h1>
  <hr class="rule">
  <p><strong>Council President Marlene Baldinger</strong><br>
  Running for re-election &middot; Tuesday, November 3, 2026<br>
  Lebanon Borough &middot; Hunterdon County, New Jersey</p>
  <div class="btnrow">
   <a class="btn teal" href="ask.html">Ask Marlene a Question</a>
   <a class="btn navy" href="get-involved.html#sign">Request a Yard Sign</a>
  </div>
 </div>
 <img src="assets/marlene-portrait.jpg" alt="Marlene Baldinger outside the Lebanon Borough municipal building">
</div>
<div class="band"><div class="wrap">A registered nurse. A 36 year resident. She knocks on every door.<br>
<span class="gold">She runs through our town, and she runs for you.</span></div></div>
<section class="block"><div class="wrap">
 <h2 class="sec">Promises Made, Promises Kept</h2>
 <div class="promise">
  <span class="tag">DELIVERED &middot; AUGUST 19, 2026</span>
  <h3>Council meetings are now livestreamed</h3>
  <p>On her 2023 campaign card, Marlene printed a promise: improve communication by
  livestreaming council meetings and making them available on the borough website.
  She pushed for it for nine years. On August 19, 2026, Lebanon Borough held its first
  livestreamed council meeting.</p>
  <p style="margin-top:10px"><a href="promises.html">See her full record &rarr;</a></p>
 </div>
</div></section>
<section class="block alt"><div class="wrap">
 <h2 class="sec">What Marlene stands for</h2>
 <ul class="stats">{li(VALUES)}</ul>
</div></section>
<section class="block"><div class="wrap grid2">
 <div class="card"><h3>Ask Marlene a Question</h3>
 <p>Have a question about our town or a council decision? Ask it here and Marlene
 answers publicly, so a neighbor with the same question can see the answer too.</p>
 <p style="margin-top:12px"><a class="btn teal" href="ask.html">Ask a question</a></p></div>
 <div class="card"><h3>Help spread the word</h3>
 <p>Yard signs go up in October. Request yours now and it will be there when the
 season starts.</p>
 <p style="margin-top:12px"><a class="btn navy" href="get-involved.html#sign">Request a yard sign</a></p></div>
</div></section>
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
