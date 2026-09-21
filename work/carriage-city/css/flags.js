/* Coming soon or open. Reads the switch EJ and Liz flip in their dashboard and
   shows the matching wording. Anything marked data-when="soon" shows until the
   switch says open; data-when="open" shows after. The last answer is remembered
   in this browser so a repeat visitor does not see the wording flicker. */
(function () {
  'use strict';
  var root = document.documentElement, KEY = 'cc_open';
  try { if (localStorage.getItem(KEY) === '1') root.classList.add('is-open'); } catch (e) {}
  fetch('https://acedigitalservicesco.com/rmc-pb/api/collections/site_flags/records?filter=' +
        encodeURIComponent('site="carriage-city" && flag="open"'))
    .then(function (r) { return r.json(); })
    .then(function (j) {
      var on = !!(j.items && j.items[0] && j.items[0].on);
      root.classList.toggle('is-open', on);
      try { localStorage.setItem(KEY, on ? '1' : '0'); } catch (e) {}
    }).catch(function () {});
})();
