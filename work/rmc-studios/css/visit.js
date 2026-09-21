/* Anonymous visit count for the owner's dashboard. Sends the page name, the site
   that linked here (host only) and a random id kept in this browser, so visitors
   can be told apart from page views. No cookies, no IP, nothing personal.
   Automated browsers are skipped so test runs do not inflate the numbers. */
(function () {
  'use strict';
  var el = document.currentScript, site = el && el.getAttribute('data-site');
  if (!site || navigator.webdriver) return;
  var vid = '';
  try {
    vid = localStorage.getItem('acev') || '';
    if (!vid) { vid = Math.random().toString(36).slice(2, 12) + Date.now().toString(36); localStorage.setItem('acev', vid); }
  } catch (e) {}
  var ref = '';
  try { if (document.referrer) { var u = new URL(document.referrer); if (u.host !== location.host) ref = u.host.replace(/^www\./, ''); } } catch (e) {}
  var path = (location.pathname.split('/').pop() || 'index.html').slice(0, 120);
  try {
    fetch('https://acedigitalservicesco.com/rmc-pb/api/collections/visits/records', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, keepalive: true,
      body: JSON.stringify({ site: site, path: path, ref: ref.slice(0, 120), vid: vid })
    }).catch(function () {});
  } catch (e) {}
})();
