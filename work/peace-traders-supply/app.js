/* Peace Traders Supply: menu, lightbox, catalog filter, hero video. No dependencies. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var burger = document.getElementById('burger'), nav = document.getElementById('nav');
  if (burger && nav) {
    var setMenu = function (open) { nav.classList.toggle('open', open); burger.setAttribute('aria-expanded', open ? 'true' : 'false'); burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu'); };
    burger.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
    nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); burger.focus(); } });
  }

  var lb = document.getElementById('lb'), lbImg = document.getElementById('lb-img'), lbCap = document.getElementById('lb-cap'), lbClose = document.getElementById('lb-close'), lastFocus = null;
  function openLb(href, cap, alt) {
    lastFocus = document.activeElement; lbImg.src = href; lbImg.alt = alt || ''; lbCap.textContent = cap || '';
    lb.hidden = false; document.body.style.overflow = 'hidden';
    requestAnimationFrame(function () { lb.classList.add('is-open'); }); lbClose.focus();
  }
  function closeLb() {
    lb.classList.remove('is-open');
    var done = function () { lb.hidden = true; lbImg.src = ''; document.body.style.overflow = ''; if (lastFocus && lastFocus.focus) lastFocus.focus(); };
    if (reduce) done(); else setTimeout(done, 160);
  }
  if (lb) {
    document.querySelectorAll('[data-lb]').forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); var img = a.querySelector('img'); openLb(a.getAttribute('href'), a.getAttribute('data-cap'), img ? img.alt : ''); });
    });
    lbClose.addEventListener('click', closeLb);
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) closeLb(); });
  }

  /* catalog filter: instant, no animation (used repeatedly) */
  var chips = document.querySelectorAll('.chip[data-filter]');
  if (chips.length) {
    var items = document.querySelectorAll('.item[data-cat]');
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var f = chip.getAttribute('data-filter');
        chips.forEach(function (c) { var on = c === chip; c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', on ? 'true' : 'false'); });
        items.forEach(function (it) { it.hidden = !(f === 'all' || it.getAttribute('data-cat') === f); });
      });
    });
  }

  /* hero video over the real photo: desktop, motion allowed, no data saver */
  var media = document.querySelector('.hero-media'), hero = document.querySelector('.hero[data-video]');
  var conn = navigator.connection || {};
  if (media && hero && !reduce && !conn.saveData) {
    var v = document.createElement('video');
    v.className = 'hero-video'; v.muted = true; v.loop = true; v.playsInline = true; v.autoplay = true; v.setAttribute('aria-hidden', 'true'); v.setAttribute('preload', 'auto');
    var s = document.createElement('source'); s.src = hero.getAttribute('data-video'); s.type = 'video/mp4'; v.appendChild(s);
    v.addEventListener('playing', function () { v.classList.add('on'); });
    media.appendChild(v);
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  }
})();
