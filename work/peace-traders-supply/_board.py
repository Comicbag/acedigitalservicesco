# Design board generator (companion to _build.py). Run from a scratch dir holding the downsampled
# images; see memory reference_site_pages_to_design_artboards for the recipe.
"""Turns the built site pages into Claude Design artboards (.dc.html): same markup, site.css inlined,
fonts embedded as base64, images referenced by bare filename (canvas files keys)."""
import re, os, base64, json, html
W = os.path.expanduser("~/ace-sites-v3/acedigitalservicesco-clone/work/peace-traders-supply")
OUT = "canvas2"
css = open(f"{W}/css/site.css").read()
def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
fonts = ("@font-face{font-family:'Cinzel';font-style:normal;font-weight:600 900;font-display:block;src:url(data:font/woff2;base64,%s) format('woff2');}"
         "@font-face{font-family:'Archivo';font-style:normal;font-weight:400 700;font-display:block;src:url(data:font/woff2;base64,%s) format('woff2');}"
         % (b64(f"{W}/fonts/Cinzel-var.woff2"), b64(f"{W}/fonts/Archivo-var.woff2")))
PAGES = [("Main", "index.html", 7308), ("Firearms", "firearms/index.html", 2088), ("Handguns", "firearms/handguns/index.html", 3317),
         ("TheCase", "the-case/index.html", 5625), ("About", "about/index.html", 3561)]
used = set()
for name, rel, h in PAGES:
    src = open(f"{W}/{rel}").read()
    body = re.search(r"<body>(.*)</body>", src, re.S).group(1)
    body = re.sub(r"<script.*?</script>\s*", "", body, flags=re.S)
    body = re.sub(r'<a class="skip"[^>]*>.*?</a>\s*', "", body, flags=re.S)
    body = re.sub(r'<div class="mobile-bar".*?</div>\s*', "", body, flags=re.S)
    body = re.sub(r'<div class="lb".*?</div>\s*', "", body, flags=re.S)
    def fix_src(m):
        used.add(m.group(1)); return f'src="{m.group(1)}"'
    body = re.sub(r'src="(?:\.\./)*assets/([^"?]+)(?:\?v=\d+)?"', fix_src, body)
    body = re.sub(r'\s(?:srcset|sizes|loading|fetchpriority|decoding)="[^"]*"', "", body)
    body = re.sub(r'href="(?!https?:|tel:|mailto:|#)[^"]*"', 'href="#"', body)
    doc = f'''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>{fonts}
{css}
html,body{{background:#0e1012;}}
.reveal{{animation:none!important;opacity:1!important;transform:none!important;translate:none!important;filter:none!important}}
*{{content-visibility:visible!important}}</style>
</helmet>
<div style="width:1440px;min-height:{h}px;background:#0e1012">{body}</div>
</x-dc>
</body>
</html>'''
    open(f"{OUT}/{name}.dc.html", "w").write(doc)
    print(f"{name}.dc.html {len(doc)//1024}KB")
missing = [u for u in used if not os.path.exists(f"{OUT}/{u}")]
print("images used:", len(used), "missing:", missing)
canvas = {
 "artboards": [
  {"file": "Main.dc.html", "x": 0, "y": 0, "w": 1440, "h": 7700, "title": "Home"},
  {"file": "Firearms.dc.html", "x": 1520, "y": 0, "w": 1440, "h": 2250, "title": "Firearms, browse by type"},
  {"file": "About.dc.html", "x": 1520, "y": 2410, "w": 1440, "h": 3750, "title": "About"},
  {"file": "TheCase.dc.html", "x": 3040, "y": 0, "w": 1440, "h": 5900, "title": "The case, full catalog"},
  {"file": "Handguns.dc.html", "x": 3040, "y": 6060, "w": 1440, "h": 3500, "title": "Handguns, category page"},
 ],
 "annotations": [
  {"id": "board-note", "x": 0, "y": -170, "w": 520, "text": "Peace Traders Supply, live demo at acedigitalservicesco.com/work/peace-traders-supply/ (14 pages; five shown here). Orange [Confirm with Kyle] blocks are the questions for the walk in."}
 ],
 "launch": {"view": "focused", "file": "Main.dc.html"}
}
json.dump(canvas, open(f"{OUT}/canvas.json", "w"), indent=1)
# standalone previews (data URIs) so the artboards can be screenshotted before publishing
os.makedirs(f"{OUT}/preview", exist_ok=True)
for name, _, _ in PAGES:
    d = open(f"{OUT}/{name}.dc.html").read()
    def inline(m):
        n = m.group(1); ext = n.rsplit(".", 1)[-1]; mime = "image/webp" if ext == "webp" else "image/png"
        return f'src="data:{mime};base64,{b64(f"{OUT}/{n}")}"'
    d = re.sub(r'src="([^"/:]+\.(?:webp|png))"', inline, d)
    d = d.replace('<script src="./support.js"></script>', "").replace("<x-dc>", "").replace("</x-dc>", "").replace("<helmet>", "").replace("</helmet>", "")
    open(f"{OUT}/preview/{name}.html", "w").write(d)
print("previews written")
