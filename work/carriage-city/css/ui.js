/* Inspiration Audio — nav + scroll reveal. No scroll listeners.

   Reveal rule: content must NEVER end up permanently invisible. The animation is
   a nicety; legibility is not. So an element reveals if it intersects OR if it
   has already been scrolled past, and a failsafe reveals anything still hidden
   a few seconds in. If any of this fails, CSS still shows the content because
   the hidden state is only applied under .js. */
(function () {
  'use strict';

  // ---- mobile nav
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('navmenu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        menu.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        menu.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        burger.focus();
      }
    });
  }

  // ---- reveal
  var targets = Array.prototype.slice.call(document.querySelectorAll('.rv'));
  if (!targets.length) return;

  function showAll() {
    for (var i = 0; i < targets.length; i++) targets[i].classList.add('in');
  }

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reduce.matches || !('IntersectionObserver' in window)) { showAll(); return; }
  if (reduce.addEventListener) reduce.addEventListener('change', function (e) { if (e.matches) showAll(); });

  var pending = targets.slice();

  // Sweep with LIVE geometry. The entry rects handed to an IntersectionObserver
  // callback are captured at queue time and go stale when the viewport jumps
  // (fling scroll, anchor jump, restored scroll position), which used to leave
  // whole sections invisible. Measuring here instead is always correct. Only
  // runs on observer callbacks, so it is not a per-frame cost.
  function sweep() {
    var vh = window.innerHeight || document.documentElement.clientHeight;
    for (var i = pending.length - 1; i >= 0; i--) {
      var el = pending[i];
      if (el.getBoundingClientRect().top < vh + 420) {
        el.classList.add('in');
        io.unobserve(el);
        pending.splice(i, 1);
      }
    }
    if (!pending.length && io) io.disconnect();
  }

  var io = new IntersectionObserver(sweep, { rootMargin: '200px 0px 420px 0px', threshold: 0 });
  targets.forEach(function (t) { io.observe(t); });
  sweep();

  // The observer alone is not enough: an instant viewport jump (fling scroll,
  // in-page anchor, browser-restored position) can land after the callback was
  // queued, leaving sections blank behind the user. scrollend catches that where
  // it exists, and a self-terminating poll covers browsers where it does not.
  // Both stop completely once everything is visible, so there is no idle cost.
  document.addEventListener('scrollend', sweep);
  var poll = window.setInterval(function () {
    if (!pending.length) { window.clearInterval(poll); return; }
    sweep();
  }, 400);

  // backstops: nothing stays invisible, whatever happens above
  window.setTimeout(showAll, 4000);
  window.addEventListener('beforeprint', showAll);
  window.addEventListener('pageshow', sweep);
})();
