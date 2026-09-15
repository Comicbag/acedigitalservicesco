const { chromium } = require('/Users/coreysmithagents/.openclaw/workspace/projects/mission-control/node_modules/playwright');
const B = 'http://127.0.0.1:8799/work/peace-traders-supply/';
const KILL = '*{animation:none!important;transition:none!important}.reveal{opacity:1!important;transform:none!important;filter:none!important}';
const hard = setTimeout(() => { console.log('HARD TIMEOUT'); process.exit(2); }, 180000);
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const errs = [];
  for (const [w, h, tag] of [[1440, 900, 'desk'], [440, 956, 'mob']]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, isMobile: w < 700, hasTouch: w < 700 });
    const page = await ctx.newPage(); page.setDefaultTimeout(20000);
    await page.route('**mc.acedigitalservicesco.com**', r => r.abort());
    await page.route('**/*.mp4', r => r.abort());
    page.on('pageerror', e => errs.push(tag + ': ' + e));
    page.on('console', m => { if (m.type() === 'error') errs.push(tag + ': ' + m.text()); });
    const prep = async () => {
      await page.addStyleTag({ content: KILL });
      await page.evaluate(() => document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; i.decoding = 'sync'; i.removeAttribute('decoding'); }));
      await page.evaluate(() => new Promise(done => {           // bounded: never hangs on a lazy image
        const imgs = [...document.images].filter(i => !i.complete);
        if (!imgs.length) return done();
        let left = imgs.length; const tick = () => { if (--left <= 0) done(); };
        imgs.forEach(i => { i.addEventListener('load', tick, { once: true }); i.addEventListener('error', tick, { once: true }); });
        setTimeout(done, 10000);
      }));
      await page.evaluate(() => Promise.race([                  // paint them: decode only what actually loaded
        Promise.all([...document.images].filter(i => i.complete && i.naturalWidth).map(i => i.decode().catch(() => {}))),
        new Promise(r => setTimeout(r, 10000)),
      ]));
      await page.waitForTimeout(500);
    };
    const shot = async (sel, file) => {
      const box = await page.evaluate(s => {
        const e = document.querySelector(s); const r = e.getBoundingClientRect();
        return { x: 0, y: Math.max(0, r.top + window.scrollY - 8), width: window.innerWidth, height: Math.min(r.height + 16, 2400) };
      }, sel);
      await page.screenshot({ path: file, fullPage: true, clip: box });
    };
    await page.goto(B, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await prep(); await shot('.latest', `qa-shots/new-latest-${tag}.png`);
    await page.goto(B + 'firearms/aows-and-others/', { waitUntil: 'domcontentloaded', timeout: 25000 });
    await prep(); await shot('.masonry', `qa-shots/new-aow-${tag}.png`);
    console.log(tag, JSON.stringify(await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth, broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')) }))));
    await ctx.close();
  }
  console.log('errors:', errs.length ? errs : 'none');
  await browser.close(); clearTimeout(hard);
})().catch(e => { console.log('FAIL', e.message); process.exit(1); });
