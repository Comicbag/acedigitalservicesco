/* Coach Eric SanDa — shell behaviour: mobile nav + demo banner dismiss. */
(function () {
  var toggle = document.querySelector('.navtoggle');
  var nav = document.getElementById('primary-nav');
  var mq = window.matchMedia('(max-width:900px)');

  function collapse() {
    if (!nav || !toggle) return;
    if (mq.matches) {
      nav.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
    } else {
      nav.hidden = false;
      toggle.setAttribute('aria-expanded', 'false');
    }
  }
  collapse();
  if (mq.addEventListener) mq.addEventListener('change', collapse);

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.hidden;
      nav.hidden = !open;
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mq.matches && !nav.hidden) {
        collapse();
        toggle.focus();
      }
    });
  }

  var bar = document.querySelector('.demobar');
  var close = bar && bar.querySelector('button');
  if (bar && close) {
    close.addEventListener('click', function () { bar.hidden = true; });
  }
})();
