// All pages x key widths: overflow, broken images, console errors, hero lines, nav height; full page shots at 440 and 1440 for the home page.
const { chromium } = require('/Users/coreysmithagents/.openclaw/workspace/projects/mission-control/node_modules/playwright');
const fs = require('fs');
const base = process.argv[2] || 'http://localhost:8765/work/peace-traders-supply/';
const outDir = process.argv[3] || '/private/tmp/claude-501/-Users-coreysmithagents/b18562dd-5c2e-4cc2-aebd-64d8ce25636d/scratchpad/qa-shots';
fs.mkdirSync(outDir, { recursive: true });
const pages = ['', 'the-case/', 'firearms/', 'firearms/handguns/', 'firearms/rifles/', 'firearms/shotguns/', 'firearms/aows-and-others/', 'firearms/ammo/', 'firearms/optics-and-accessories/', 'services/', 'about/', 'buying-in-nj/', 'faq/', 'visit/'];
const widths = [320, 375, 440, 768, 1024, 1440];
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  let hard = 0; const rows = [];
  for (const w of widths) {
    const ctx = await browser.newContext({ viewport: { width: w, height: w < 700 ? 844 : 900 }, deviceScaleFactor: w < 700 ? 2 : 1, isMobile: w < 700, hasTouch: w < 700 });
    for (const p of pages) {
      const page = await ctx.newPage(); const errors = [];
      page.on('pageerror', e => errors.push(String(e))); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
      const resp = await page.goto(base + p, { waitUntil: 'networkidle' });
      const m = await page.evaluate(() => {
        const wide = [...document.querySelectorAll('body *')].filter(e => { if (e.closest('.marquee') || e.classList.contains('hero-mark')) return false; const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.right > window.innerWidth + 1 && cs.position !== 'fixed' && cs.display !== 'none' && r.width > 0; }).slice(0, 4).map(e => e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : ''));
        const broken = [...document.images].filter(i => i.getAttribute('src') && i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'));
        const h1 = document.querySelector('h1'); const lh = h1 ? parseFloat(getComputedStyle(h1).lineHeight) : 1;
        return { sw: document.documentElement.scrollWidth, iw: window.innerWidth, h1lines: h1 ? Math.round(h1.getBoundingClientRect().height / lh) : 0, nav: Math.round(document.querySelector('.site-head').getBoundingClientRect().height), wide, broken, docH: document.documentElement.scrollHeight };
      });
      const bad = m.sw > m.iw || m.wide.length || m.broken.length || errors.length || resp.status() !== 200;
      if (bad) hard++;
      rows.push({ w, p: p || '/', status: resp.status(), ...m, errors: errors.slice(0, 2), bad });
      if ((w === 440 || w === 1440) && (p === '' || p === 'about/' || p === 'firearms/handguns/')) await page.screenshot({ path: `${outDir}/${w}-${(p || 'home').replace(/\//g, '_')}.png`, fullPage: true });
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  for (const r of rows.filter(r => r.bad)) console.log('BAD', JSON.stringify(r));
  const h1over = rows.filter(r => r.w >= 1024 && r.h1lines > 2).map(r => `${r.p}@${r.w}:${r.h1lines}`);
  console.log(`checked ${rows.length} page/width combos; hard failures: ${hard}; h1 over 2 lines at desktop: ${h1over.join(', ') || 'none'}`);
})();
