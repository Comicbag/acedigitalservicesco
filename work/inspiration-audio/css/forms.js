/* Inspiration Audio — form delivery.

   Every form on this site posted to action="#", which silently did nothing: a
   visitor filled it in, pressed send, and the enquiry evaporated. These now
   post to the client's own PocketBase and show up in EJ and Liz's dashboard.

   Two deliberate choices:
   - Progressive. Without JS, or without an endpoint configured, the form is
     left exactly as it was. Nothing here can make it worse.
   - Nothing is cleared until the server confirms the write. Someone who hits a
     network error still has everything they typed, which matters most on the
     scholarship form. */
(function () {
  'use strict';

  var BASE = window.IA_FORMS_ENDPOINT || '';
  var SITE = 'inspiration-audio';
  var forms = document.querySelectorAll('form[data-ia-form]');
  if (!BASE || !forms.length) return;
  var ENDPOINT = BASE.replace(/\/$/, '') + '/api/collections/submissions/records';

  function say(form, msg, ok) {
    var box = form.querySelector('.formstatus');
    if (!box) {
      box = document.createElement('div');
      box.className = 'formstatus';
      box.setAttribute('role', 'status');
      box.setAttribute('aria-live', 'polite');
      form.appendChild(box);
    }
    box.textContent = msg;
    box.className = 'formstatus ' + (ok ? 'is-ok' : 'is-err');
  }

  function collect(form) {
    var out = {};
    new FormData(form).forEach(function (v, k) {
      if (out[k] === undefined) out[k] = v;
      else if (Array.isArray(out[k])) out[k].push(v);
      else out[k] = [out[k], v];
    });
    return out;
  }

  // Lift name/email/phone out of whatever this particular form calls them,
  // without losing anything: the complete set still goes into payload.
  function pick(p, keys) {
    for (var i = 0; i < keys.length; i++) if (p[keys[i]]) return String(p[keys[i]]);
    return '';
  }

  Array.prototype.forEach.call(forms, function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (typeof form.reportValidity === 'function' && !form.reportValidity()) return;

      var btn = form.querySelector('[type=submit]');
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

      var p = collect(form);
      var body = {
        site: SITE,
        kind: form.getAttribute('data-ia-form') || 'other',
        name: (pick(p, ['first', 'name']) + ' ' + pick(p, ['last'])).trim(),
        email: pick(p, ['email']),
        phone: pick(p, ['phone', 'tel']),
        message: pick(p, ['message', 'about', 'notes', 'why']),
        payload: p,
        sourceUrl: location.href,
        userAgent: navigator.userAgent.slice(0, 500)
      };

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      }).then(function () {
        form.reset();
        say(form, 'Thank you. We have got it and will be in touch.', true);
        if (btn) btn.textContent = 'Sent';
      }).catch(function () {
        say(form, 'Sorry, that did not send. Please try again, or email us directly.', false);
        if (btn) { btn.disabled = false; btn.textContent = label; }
      });
    });
  });
})();
