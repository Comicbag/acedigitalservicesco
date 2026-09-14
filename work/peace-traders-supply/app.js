/* Peace Traders Supply demo: menu, scroll reveal, lightbox, optional hero video. No dependencies. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* hamburger */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-label', 'Open menu');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        burger.focus();
      }
    });
  }

  /* scroll reveal */
  var items = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* lightbox */
  var lb = document.getElementById('lb');
  var lbImg = document.getElementById('lb-img');
  var lbCap = document.getElementById('lb-cap');
  var lbClose = document.getElementById('lb-close');
  var lastFocus = null;
  function openLb(href, cap, alt) {
    lastFocus = document.activeElement;
    lbImg.src = href; lbImg.alt = alt || ''; lbCap.textContent = cap || '';
    lb.hidden = false; document.body.style.overflow = 'hidden';
    lbClose.focus();
  }
  function closeLb() {
    lb.hidden = true; lbImg.src = ''; document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  if (lb) {
    document.querySelectorAll('[data-lb]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var img = a.querySelector('img');
        openLb(a.getAttribute('href'), a.getAttribute('data-cap'), img ? img.alt : '');
      });
    });
    lbClose.addEventListener('click', closeLb);
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) closeLb(); });
  }

  /* hero video: desktop only, motion allowed, saves data respected */
  var hero = document.querySelector('.hero');
  var conn = navigator.connection || {};
  if (hero && !reduce && !conn.saveData && window.matchMedia('(min-width: 900px)').matches && hero.getAttribute('data-video')) {
    var v = document.createElement('video');
    v.className = 'hero-video'; v.muted = true; v.loop = true; v.playsInline = true; v.autoplay = true;
    v.setAttribute('aria-hidden', 'true'); v.setAttribute('preload', 'metadata');
    var s = document.createElement('source'); s.src = hero.getAttribute('data-video'); s.type = 'video/mp4';
    v.appendChild(s);
    v.addEventListener('canplay', function () { v.classList.add('on'); });
    hero.insertBefore(v, hero.firstChild);
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  }
})();
