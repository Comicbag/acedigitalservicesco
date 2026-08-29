/* ============================================================================
   Ace Digital — Accessibility Menu (self-hosted, no dependencies, no subscription)
   A drop-in replacement for UserWay-style overlays. ONE line per page:
       <script src="a11y.js" defer></script>
   It injects its own styles + button + panel. All toggles are client-side and
   persist in localStorage. The widget lives OUTSIDE the page wrapper so contrast
   filters never invert/grey the menu itself.

   HONEST SCOPE: this is an assist menu (display preferences + reading aids). It does
   NOT make a site "ADA compliant" or "certified" on its own — real compliance is the
   underlying site built to WCAG (semantic HTML, alt text, contrast, keyboard nav),
   which Ace Digital builds + verifies separately. This complements that; it doesn't
   replace it. Never advertise this widget as "certification".
   ============================================================================ */
(function () {
  "use strict";
  if (window.__aceA11yLoaded) return;
  window.__aceA11yLoaded = true;

  var KEY = "aceA11y";
  var FONT_URL = (document.currentScript && document.currentScript.src
      ? document.currentScript.src.replace(/[^/]*$/, "")
      : "") + "a11y-opendyslexic.woff2";

  // ---- state ---------------------------------------------------------------
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { state = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }

  // ---- styles --------------------------------------------------------------
  var BIG_CURSOR = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 32 32'%3E%3Cpath d='M6 2l20 12-8 2 5 10-4 2-5-10-6 6z' fill='black' stroke='white' stroke-width='1.5'/%3E%3C/svg%3E\") 4 2, auto";
  var css = [
    "@font-face{font-family:'AceOpenDyslexic';src:url('" + FONT_URL + "') format('woff2');font-display:swap}",
    // page wrapper (everything except the widget)
    "html.ace-fs-1{font-size:112%}html.ace-fs-2{font-size:125%}html.ace-fs-3{font-size:140%}html.ace-fs-4{font-size:160%}",
    // contrast filters on the page wrapper only
    "#ace-page.ax-invert{filter:invert(1) hue-rotate(180deg)}",
    "#ace-page.ax-contrast{filter:contrast(1.42) saturate(1.12)}",
    "#ace-page.ax-grayscale{filter:grayscale(1)}",
    // text/spacing/links/cursor
    "#ace-page.ax-spacing *{letter-spacing:.12em!important;word-spacing:.16em!important;line-height:2!important}",
    "#ace-page.ax-dyslexic *{font-family:'AceOpenDyslexic','Comic Sans MS','Atkinson Hyperlegible',sans-serif!important}",
    "#ace-page.ax-links a{outline:2px solid #ffbf00!important;outline-offset:1px;background:#fff8d6!important;color:#161514!important;text-decoration:underline!important}",
    "#ace-page.ax-cursor,#ace-page.ax-cursor *{cursor:" + BIG_CURSOR + "!important}",
    "#ace-page.ax-noanim *{animation:none!important;transition:none!important;scroll-behavior:auto!important}",
    "#ace-page.ax-noimg img,#ace-page.ax-noimg picture,#ace-page.ax-noimg video{opacity:0!important}",
    "#ace-page.ax-noimg [style*='background-image'],#ace-page.ax-noimg .bg{background-image:none!important}",
    // read-aloud: highlight the line currently being read
    "#ace-page .ace-reading{background:#fff3a8!important;color:#161514!important;box-shadow:0 0 0 5px #fff3a8!important;border-radius:2px}",
    // reading aids (overlays, outside wrapper)
    "#ace-rguide{position:fixed;left:0;right:0;height:0;border-top:3px solid #1a73c4;box-shadow:0 0 0 1px #fff;z-index:2147483640;pointer-events:none;display:none}",
    "#ace-rmask-t,#ace-rmask-b{position:fixed;left:0;right:0;background:rgba(0,0,0,.62);z-index:2147483639;pointer-events:none;display:none}",
    // ---- the widget (all px so page font-scaling never touches it) ----
    "#ace-a11y *{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif}",
    "#ace-a11y-btn{position:fixed;bottom:20px;left:20px;width:54px;height:54px;border-radius:50%;background:#1a73c4;border:none;cursor:pointer;z-index:2147483646;box-shadow:0 4px 14px rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;padding:0;transition:transform .15s}",
    "#ace-a11y-btn:hover{transform:scale(1.06)}",
    "#ace-a11y-btn:focus-visible{outline:3px solid #fff;outline-offset:2px}",
    "#ace-a11y-btn svg{width:32px;height:32px;fill:#fff}",
    "#ace-a11y-panel{position:fixed;bottom:84px;left:20px;width:330px;max-width:calc(100vw - 40px);max-height:calc(100vh - 110px);overflow-y:auto;background:#fff;color:#16181d;border-radius:14px;box-shadow:0 10px 40px rgba(0,0,0,.32);z-index:2147483646;display:none;padding:0;border:1px solid #e3e6ea}",
    "#ace-a11y-panel.open{display:block}",
    "#ace-a11y-hd{display:flex;align-items:center;justify-content:space-between;padding:16px 18px;border-bottom:1px solid #eceff2;position:sticky;top:0;background:#fff;border-radius:14px 14px 0 0}",
    "#ace-a11y-hd h2{margin:0;font-size:17px;font-weight:700;color:#16181d}",
    "#ace-a11y-hd .sub{font-size:11px;color:#6a7178;font-weight:500;margin-top:2px}",
    "#ace-a11y-close{background:#f0f2f5;border:none;width:30px;height:30px;border-radius:8px;cursor:pointer;font-size:18px;line-height:1;color:#444;flex:none}",
    "#ace-a11y-close:hover{background:#e3e6ea}",
    "#ace-a11y-body{padding:14px}",
    ".ace-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}",
    ".ace-grp{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#8a9099;font-weight:700;margin:12px 4px 6px}",
    ".ace-tg{display:flex;flex-direction:column;align-items:center;gap:6px;padding:12px 6px;border:1.5px solid #e3e6ea;border-radius:10px;background:#fff;cursor:pointer;font-size:12.5px;font-weight:600;color:#2a2f36;text-align:center;line-height:1.25;transition:.12s}",
    ".ace-tg:hover{border-color:#1a73c4;background:#f5f9ff}",
    ".ace-tg:focus-visible{outline:2px solid #1a73c4;outline-offset:1px}",
    ".ace-tg[aria-pressed='true']{background:#1a73c4;border-color:#1a73c4;color:#fff}",
    ".ace-tg svg{width:22px;height:22px;fill:currentColor}",
    ".ace-step{display:flex;align-items:center;justify-content:space-between;border:1.5px solid #e3e6ea;border-radius:10px;padding:8px 10px;margin-bottom:8px}",
    ".ace-step .lbl{font-size:12.5px;font-weight:600;color:#2a2f36;display:flex;align-items:center;gap:8px}",
    ".ace-step .lbl svg{width:20px;height:20px;fill:#2a2f36}",
    ".ace-step .ctrl{display:flex;align-items:center;gap:8px}",
    ".ace-step button{width:30px;height:30px;border-radius:8px;border:1px solid #d4d8dd;background:#f5f7f9;font-size:17px;cursor:pointer;color:#16181d;line-height:1}",
    ".ace-step button:hover{background:#e9edf1}",
    ".ace-step .val{font-size:12.5px;font-weight:700;min-width:42px;text-align:center;color:#1a73c4}",
    "#ace-reset{width:100%;margin-top:8px;padding:11px;border:1.5px solid #e3e6ea;border-radius:10px;background:#fff;cursor:pointer;font-size:13px;font-weight:700;color:#b3261e}",
    "#ace-reset:hover{background:#fdecea;border-color:#f3b4ae}",
    "#ace-a11y-foot{font-size:10.5px;color:#9aa0a7;text-align:center;padding:0 14px 14px;line-height:1.4}",
    "@media(max-width:520px){#ace-a11y-panel{left:10px;bottom:78px}#ace-a11y-btn{left:14px;bottom:14px}}"
  ].join("\n");

  var styleEl = document.createElement("style");
  styleEl.id = "ace-a11y-style";
  styleEl.textContent = css;

  // ---- SVG icons -----------------------------------------------------------
  var I = {
    access: "<svg viewBox='0 0 24 24'><circle cx='12' cy='3.5' r='2'/><path d='M21 7.5c0 .6-.5 1-1 1.1l-4.5.7v3.2l1.9 6.4c.2.7-.2 1.4-.9 1.6-.6.2-1.3-.2-1.5-.8L12.6 15h-1.2l-1.9 5.7c-.2.6-.9 1-1.5.8-.7-.2-1.1-.9-.9-1.6l1.9-6.4V9.3L4.5 8.6C3.8 8.5 3.3 7.9 3.4 7.2 3.5 6.6 4.1 6.2 4.8 6.3L9 7h6l4.2-.7c.7-.1 1.3.3 1.4 1 .4.1.4.2.4.2z'/></svg>",
    contrast: "<svg viewBox='0 0 24 24'><path d='M12 2a10 10 0 100 20V2z'/><path d='M12 2a10 10 0 010 20' fill='none' stroke='currentColor' stroke-width='1.6'/></svg>",
    invert: "<svg viewBox='0 0 24 24'><path d='M12 3v18a9 9 0 000-18z'/><circle cx='12' cy='12' r='9' fill='none' stroke='currentColor' stroke-width='1.6'/></svg>",
    gray: "<svg viewBox='0 0 24 24'><circle cx='12' cy='12' r='9' fill='none' stroke='currentColor' stroke-width='1.8'/><path d='M9 8h6M9 12h6M9 16h4' stroke='currentColor' stroke-width='1.6' fill='none'/></svg>",
    text: "<svg viewBox='0 0 24 24'><path d='M5 5h14v2H5zM9 9h6v10h-2v-8h-2v8H9z'/></svg>",
    spacing: "<svg viewBox='0 0 24 24'><path d='M4 5h16v2H4zM4 11h16v2H4zM4 17h16v2H4z'/></svg>",
    dys: "<svg viewBox='0 0 24 24'><path d='M4 18 9 6h2l5 12h-2.2l-1.1-2.8H7.3L6.2 18zm4-4.6h3.9L10 8z'/></svg>",
    link: "<svg viewBox='0 0 24 24'><path d='M10.6 13.4a3 3 0 010-4.2l3-3a3 3 0 014.2 4.2l-1.5 1.5-1.4-1.4 1.5-1.5a1 1 0 00-1.4-1.4l-3 3a1 1 0 000 1.4zM13.4 10.6a3 3 0 010 4.2l-3 3a3 3 0 11-4.2-4.2l1.5-1.5 1.4 1.4-1.5 1.5a1 1 0 001.4 1.4l3-3a1 1 0 000-1.4z'/></svg>",
    cursor: "<svg viewBox='0 0 24 24'><path d='M5 2l14 8-5.6 1.4L17 19l-2.8 1.4L11 13l-4 4z'/></svg>",
    anim: "<svg viewBox='0 0 24 24'><path d='M8 5v14l11-7z'/><path d='M5 5h2v14H5z'/></svg>",
    image: "<svg viewBox='0 0 24 24'><path d='M21 5H3v14h18zM5 17l3.5-4.5 2.5 3 3.5-4.5L19 17z'/><circle cx='8' cy='9' r='1.5'/></svg>",
    guide: "<svg viewBox='0 0 24 24'><path d='M3 11h18v2H3z'/><path d='M3 6h18v1.5H3zM3 16.5h18V18H3z' opacity='.5'/></svg>",
    mask: "<svg viewBox='0 0 24 24'><path d='M2 3h20v6H2zM2 15h20v6H2z' opacity='.55'/><path d='M2 10h20v4H2z'/></svg>",
    speak: "<svg viewBox='0 0 24 24'><path d='M4 9v6h4l5 5V4L8 9zM16 8.5a4 4 0 010 7M18.5 6a7 7 0 010 12' fill='none' stroke='currentColor' stroke-width='1.8'/></svg>"
  };

  // ---- build DOM -----------------------------------------------------------
  var root = document.createElement("div");
  root.id = "ace-a11y";
  root.innerHTML =
    "<button id='ace-a11y-btn' aria-label='Accessibility menu' aria-expanded='false' aria-haspopup='dialog'>" + I.access + "</button>" +
    "<div id='ace-a11y-panel' role='dialog' aria-modal='true' aria-label='Accessibility menu' tabindex='-1'>" +
      "<div id='ace-a11y-hd'><div><h2>Accessibility</h2><div class='sub'>Adjust the page to suit you</div></div>" +
        "<button id='ace-a11y-close' aria-label='Close accessibility menu'>&times;</button></div>" +
      "<div id='ace-a11y-body'>" +
        "<div class='ace-step'><span class='lbl'>" + I.text + "Text size</span>" +
          "<span class='ctrl'><button id='ace-fs-dn' aria-label='Decrease text size'>&minus;</button>" +
          "<span class='val' id='ace-fs-val'>100%</span>" +
          "<button id='ace-fs-up' aria-label='Increase text size'>+</button></span></div>" +
        "<div class='ace-grp'>Contrast &amp; color</div>" +
        "<div class='ace-row'>" +
          tg("invert", I.invert, "Invert colors") +
          tg("contrast", I.contrast, "High contrast") +
        "</div><div class='ace-row'>" +
          tg("grayscale", I.gray, "Grayscale") +
          tg("links", I.link, "Highlight links") +
        "</div>" +
        "<div class='ace-grp'>Reading</div>" +
        "<div class='ace-row'>" +
          tg("spacing", I.spacing, "Text spacing") +
          tg("dyslexic", I.dys, "Dyslexia font") +
        "</div><div class='ace-row'>" +
          tg("guide", I.guide, "Reading guide") +
          tg("mask", I.mask, "Reading mask") +
        "</div>" +
        "<div class='ace-grp'>Other</div>" +
        "<div class='ace-row'>" +
          tg("cursor", I.cursor, "Big cursor") +
          tg("noanim", I.anim, "Pause motion") +
        "</div><div class='ace-row'>" +
          tg("noimg", I.image, "Hide images") +
          tg("speak", I.speak, "Read aloud") +
        "</div>" +
        "<button id='ace-reset'>Reset all settings</button>" +
      "</div>" +
      "<div id='ace-a11y-foot'>Display preferences only. This site is also built to accessibility standards.</div>" +
    "</div>";

  function tg(key, icon, label) {
    return "<button class='ace-tg' data-tg='" + key + "' aria-pressed='false'>" + icon + "<span>" + label + "</span></button>";
  }

  // ---- wrap page content so contrast filters never touch the widget --------
  function init() {
    document.head.appendChild(styleEl);
    var page = document.createElement("div");
    page.id = "ace-page";
    while (document.body.firstChild) page.appendChild(document.body.firstChild);
    document.body.appendChild(page);
    document.body.appendChild(root);

    var guide = document.createElement("div"); guide.id = "ace-rguide";
    var mt = document.createElement("div"); mt.id = "ace-rmask-t";
    var mb = document.createElement("div"); mb.id = "ace-rmask-b";
    document.body.appendChild(guide); document.body.appendChild(mt); document.body.appendChild(mb);

    wire(page, guide, mt, mb);
    apply(page);
  }

  // ---- behavior ------------------------------------------------------------
  var FILTERS = ["invert", "contrast", "grayscale"]; // mutually exclusive
  var fsClasses = ["", "ace-fs-1", "ace-fs-2", "ace-fs-3", "ace-fs-4"];
  var fsPct = ["100%", "112%", "125%", "140%", "160%"];

  function wire(page, guide, mt, mb) {
    var btn = root.querySelector("#ace-a11y-btn");
    var panel = root.querySelector("#ace-a11y-panel");
    var closeBtn = root.querySelector("#ace-a11y-close");

    function openPanel() {
      panel.classList.add("open"); btn.setAttribute("aria-expanded", "true");
      panel.focus();
      document.addEventListener("keydown", onKey);
    }
    function closePanel() {
      panel.classList.remove("open"); btn.setAttribute("aria-expanded", "false");
      document.removeEventListener("keydown", onKey); btn.focus();
    }
    function onKey(e) {
      if (e.key === "Escape") return closePanel();
      if (e.key === "Tab") {
        var f = panel.querySelectorAll("button");
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    }
    btn.addEventListener("click", function () { panel.classList.contains("open") ? closePanel() : openPanel(); });
    closeBtn.addEventListener("click", closePanel);

    // toggle buttons
    root.querySelectorAll(".ace-tg").forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-tg");
        if (FILTERS.indexOf(k) > -1) {
          var turningOn = !state[k];
          FILTERS.forEach(function (f) { state[f] = false; });
          state[k] = turningOn;
        } else {
          state[k] = !state[k];
        }
        save(); apply(page); syncToggles();
        if (k === "speak") toggleSpeak();
      });
    });

    // text size stepper
    root.querySelector("#ace-fs-up").addEventListener("click", function () {
      state.fs = Math.min(4, (state.fs || 0) + 1); save(); apply(page);
    });
    root.querySelector("#ace-fs-dn").addEventListener("click", function () {
      state.fs = Math.max(0, (state.fs || 0) - 1); save(); apply(page);
    });

    root.querySelector("#ace-reset").addEventListener("click", function () {
      stopReading();
      state = {}; save(); apply(page); syncToggles();
    });

    // reading guide / mask follow the cursor
    document.addEventListener("mousemove", function (e) {
      if (state.guide) { guide.style.top = e.clientY + "px"; }
      if (state.mask) {
        var h = 130;
        mt.style.height = Math.max(0, e.clientY - h / 2) + "px"; mt.style.top = "0";
        mb.style.top = (e.clientY + h / 2) + "px"; mb.style.bottom = "0";
      }
    });
  }

  function syncToggles() {
    root.querySelectorAll(".ace-tg").forEach(function (b) {
      b.setAttribute("aria-pressed", state[b.getAttribute("data-tg")] ? "true" : "false");
    });
  }

  function apply(page) {
    // contrast filters + feature classes on the wrapper
    ["ax-invert", "ax-contrast", "ax-grayscale", "ax-spacing", "ax-dyslexic", "ax-links", "ax-cursor", "ax-noanim", "ax-noimg"]
      .forEach(function (c) { page.classList.remove(c); });
    if (state.invert) page.classList.add("ax-invert");
    if (state.contrast) page.classList.add("ax-contrast");
    if (state.grayscale) page.classList.add("ax-grayscale");
    if (state.spacing) page.classList.add("ax-spacing");
    if (state.dyslexic) page.classList.add("ax-dyslexic");
    if (state.links) page.classList.add("ax-links");
    if (state.cursor) page.classList.add("ax-cursor");
    if (state.noanim) page.classList.add("ax-noanim");
    if (state.noimg) page.classList.add("ax-noimg");
    // text size on <html> (rem-based), widget is px so unaffected
    document.documentElement.classList.remove("ace-fs-1", "ace-fs-2", "ace-fs-3", "ace-fs-4");
    var fc = fsClasses[state.fs || 0];
    if (fc) document.documentElement.classList.add(fc);
    var v = root.querySelector("#ace-fs-val"); if (v) v.textContent = fsPct[state.fs || 0];
    // reading aids visibility
    var g = document.getElementById("ace-rguide"); if (g) g.style.display = state.guide ? "block" : "none";
    var mt = document.getElementById("ace-rmask-t"); var mb = document.getElementById("ace-rmask-b");
    if (mt) mt.style.display = state.mask ? "block" : "none";
    if (mb) mb.style.display = state.mask ? "block" : "none";
    syncToggles();
  }

  // ---- read aloud — plays a PRE-GENERATED narration MP3 (audio/<page>.mp3, made at build time by
  //      gen_audio.py + Piper) so it works identically on EVERY device, with the line being read
  //      highlighted in sync to the audio. Falls back to the browser voice only if no MP3 is present.
  var SS = window.speechSynthesis;
  if (SS) { try { SS.getVoices(); SS.onvoiceschanged = function () { SS.getVoices(); }; } catch (e) {} }
  function pickVoice() {
    var vs = (SS && SS.getVoices && SS.getVoices()) || [];
    if (!vs.length) return null;
    var lang = (document.documentElement.getAttribute("lang") || "en").slice(0, 2).toLowerCase();
    var byLang = vs.filter(function (v) { return v.lang && v.lang.toLowerCase().indexOf(lang) === 0; });
    return (byLang.filter(function (v) { return v.default; })[0]) || byLang[0] ||
           (vs.filter(function (v) { return v.default; })[0]) || vs[0];
  }
  // the content the audio narrates / the widget highlights — same nodes, same order as gen_audio.py
  function gatherNodes() {
    var out = [];
    document.querySelectorAll("h1,h2,h3,h4,p,li,figcaption,blockquote").forEach(function (n) {
      if (n.closest("header,footer,nav,.topstrip,#ace-a11y")) return;
      if (n.offsetParent === null) return;
      var t = (n.innerText || n.textContent || "").replace(/\s+/g, " ").trim();
      if (t && t.length > 1) out.push({ el: n, t: t });
    });
    return out;
  }
  function clearHighlight() {
    var p = document.getElementById("ace-page");
    if (p) p.querySelectorAll(".ace-reading").forEach(function (e) { e.classList.remove("ace-reading"); });
  }

  // -- pre-generated audio (primary path) --
  var audioEl = null, segNodes = null, segStarts = null, lastIdx = -1;
  function audioPaths() {
    var p = location.pathname, slash = p.lastIndexOf("/");
    var dir = p.substring(0, slash + 1), file = p.substring(slash + 1) || "index.html";
    var slug = file.replace(/\.html?$/, "") || "index";
    return { mp3: dir + "audio/" + slug + ".mp3", json: dir + "audio/" + slug + ".json" };
  }
  function syncHighlight() {
    if (!audioEl || !segStarts) return;
    var t = audioEl.currentTime, idx = -1;
    for (var i = 0; i < segStarts.length; i++) { if (segStarts[i] <= t + 0.05) idx = i; else break; }
    if (idx >= 0 && idx !== lastIdx && segNodes[idx]) {
      lastIdx = idx; clearHighlight(); segNodes[idx].el.classList.add("ace-reading");
      try { segNodes[idx].el.scrollIntoView({ block: "center", behavior: "smooth" }); } catch (e) {}
    }
  }
  function cleanupAudio() {
    if (audioEl) { audioEl.pause(); audioEl.removeEventListener("timeupdate", syncHighlight); audioEl = null; }
    lastIdx = -1; clearHighlight();
  }

  // -- browser-voice fallback (only if no MP3) --
  function speakSeq(items) {
    var i = 0, voice = pickVoice(), lang = document.documentElement.getAttribute("lang") || "en-US";
    function next() {
      clearHighlight();
      if (!state.speak || i >= items.length) { state.speak = false; save(); syncToggles(); return; }
      var it = items[i];
      it.el.classList.add("ace-reading");
      try { it.el.scrollIntoView({ block: "center", behavior: "smooth" }); } catch (e) {}
      var u = new SpeechSynthesisUtterance(it.t);
      u.rate = 1; u.lang = lang;
      try { if (voice) u.voice = voice; } catch (e) {}
      u.onend = function () { i++; next(); };
      u.onerror = function () { i++; next(); };
      SS.speak(u);
    }
    next();
  }
  function ttsFallback(items) {
    if (!SS) { state.speak = false; syncToggles(); return; }
    SS.cancel(); setTimeout(function () { if (state.speak) speakSeq(items); }, 90);
  }

  function startReading() {
    var items = gatherNodes();
    if (!items.length) { state.speak = false; syncToggles(); return; }
    var paths = audioPaths();
    fetch(paths.json).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (meta) {
      segNodes = items; segStarts = meta.starts || []; lastIdx = -1;
      audioEl = new Audio(paths.mp3);
      audioEl.addEventListener("timeupdate", syncHighlight);
      audioEl.addEventListener("ended", function () { state.speak = false; cleanupAudio(); save(); syncToggles(); });
      var pr = audioEl.play();
      if (pr && pr.catch) pr.catch(function () { cleanupAudio(); ttsFallback(items); });
    }).catch(function () { ttsFallback(items); });
  }
  function stopReading() { cleanupAudio(); if (SS) SS.cancel(); }
  function toggleSpeak() { if (state.speak) startReading(); else stopReading(); }
  // Chrome stops long browser-TTS after ~15s; nudge it (no-op for the MP3 path)
  setInterval(function () { if (state.speak && SS && SS.speaking) { try { SS.resume(); } catch (e) {} } }, 9000);

  // read-aloud stays available everywhere: the MP3 path works in any browser, and browser-TTS is the
  // fallback. Only hide it if BOTH are impossible (no <audio> AND no speechSynthesis — effectively never).
  function pruneUnsupported() {
    var canAudio = !!window.HTMLAudioElement, canTTS = ("speechSynthesis" in window);
    if (!canAudio && !canTTS) {
      var b = root.querySelector("[data-tg='speak']"); if (b) b.style.display = "none";
    }
  }
  window.addEventListener("beforeunload", stopReading);

  // read-aloud is an ACTION, not a saved preference — never auto-start on load
  state.speak = false;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { init(); pruneUnsupported(); });
  } else { init(); pruneUnsupported(); }
})();
