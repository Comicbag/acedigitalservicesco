/* RMC Staging: form delivery (same kit as Inspiration Audio).

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
  var SITE = 'rmc-staging';
  var forms = document.querySelectorAll('form[data-ia-form]');
  if (!BASE || !forms.length) return;
  var LOADED = Date.now();
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
      if (typeof v === 'string') v = v.trim().slice(0, 5000);
      if (out[k] === undefined) out[k] = v;
      else if (Array.isArray(out[k])) out[k].push(v);
      else out[k] = [out[k], v];
    });
    return out;
  }

  // The question each answer belongs to, taken from the form itself, so the
  // dashboard can show "What ignited your interest in music?" rather than "why".
  function questions(form) {
    var labels = {}, order = [];
    Array.prototype.forEach.call(form.querySelectorAll('[name]'), function (el) {
      var n = el.name; if (!n || labels[n] !== undefined) return;
      var t = '';
      if (el.type === 'radio' || el.type === 'checkbox') {
        var fs = el.closest('fieldset'), lg = fs && fs.querySelector('legend');
        t = lg ? lg.textContent : '';
      } else if (el.id) {
        var lb = form.querySelector('label[for="' + el.id + '"]');
        t = lb ? lb.textContent : '';
      }
      labels[n] = t.replace(/\s+/g, ' ').replace(/\s*\*\s*$/, '').trim(); order.push(n);
    });
    return { labels: labels, order: order };
  }

  // Lift name/email/phone out of whatever this particular form calls them,
  // without losing anything: the complete set still goes into payload.
  function pick(p, keys) {
    for (var i = 0; i < keys.length; i++) if (p[keys[i]]) return String(p[keys[i]]);
    return '';
  }

  // Fill in what we already know about a signed-in member.
  function prefill(form) {
    var r = (window.IAMember && window.IAMember.record && window.IAMember.record()) || null;
    if (!r) return;
    var parts = String(r.name || '').split(' ');
    var set = function (n, v) {
      var el = form.querySelector('[name=' + n + ']');
      if (el && !el.value && v) el.value = v;
    };
    set('first', parts[0]); set('last', parts.slice(1).join(' '));
    set('name', r.name); set('email', r.email); set('phone', r.phone);
  }

  Array.prototype.forEach.call(forms, function (form) {
    prefill(form);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      // HARDENED: automated spam fills and sends a form within a second or two of
      // the page loading. A person cannot. Those are thanked and quietly dropped.
      if (Date.now() - LOADED < 2500) { form.reset(); say(form, form.getAttribute('data-success') || 'Thank you. We have got it and will be in touch.', true); return; }
      if (typeof form.reportValidity === 'function' && !form.reportValidity()) return;
      // A checkbox question marked data-required needs at least one box ticked;
      // browsers have no built-in rule for "one of these".
      var groups = form.querySelectorAll('fieldset[data-required]');
      for (var g = 0; g < groups.length; g++) {
        if (!groups[g].querySelector('input:checked')) {
          say(form, 'Please answer: ' + (groups[g].querySelector('legend') || {}).textContent, false);
          var first = groups[g].querySelector('input'); if (first) first.focus();
          return;
        }
      }

      var btn = form.querySelector('[type=submit]');
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

      var p = collect(form);
      var q = questions(form); p._labels = q.labels; p._order = q.order;
      // If they are signed in, attach the submission to their account so it
      // shows on their own account page. Signed-out submissions still work.
      var member = (window.IAMember && window.IAMember.record && window.IAMember.record()) || null;
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
      if (member && member.id) body.member = member.id;

      // Prefill is friendlier than making a signed-in person retype their name.
      

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
