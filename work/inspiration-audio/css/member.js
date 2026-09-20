/* Inspiration Audio — member accounts.
   Talks to the client's own PocketBase. Sign in with Google, Facebook or email.
   Social buttons only render for providers actually configured on the server, so
   the page never shows a button that cannot work. */
(function () {
  'use strict';
  var BASE = (window.IA_FORMS_ENDPOINT || '').replace(/\/$/, '');
  if (!BASE) return;
  var C = BASE + '/api/collections/members';
  var KEY = 'ia_member';

  var M = window.IAMember = {
    get: function () { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; } },
    set: function (a) { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} },
    clear: function () { try { localStorage.removeItem(KEY); } catch (e) {} },
    token: function () { var a = M.get(); return a && a.token; },
    record: function () { var a = M.get(); return a && a.record; }
  };

  function api(path, opts) {
    opts = opts || {};
    opts.headers = Object.assign({ 'Content-Type': 'application/json' }, opts.headers || {});
    var t = M.token(); if (t) opts.headers.Authorization = t;
    return fetch(BASE + path, opts).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok) {
          // A token for an account that no longer exists, or an expired one,
          // otherwise leaves the nav cheerfully greeting someone who cannot do
          // anything. Drop the session so the site stops pretending.
          if (r.status === 401 && M.token()) { M.clear(); }
          var e = new Error(j.message || ('HTTP ' + r.status)); e.data = j.data; e.status = r.status; throw e;
        }
        return j;
      });
    });
  }
  M.api = api;

  function say(el, msg, ok) {
    if (!el) return;
    el.textContent = msg;
    el.className = 'formstatus ' + (ok ? 'is-ok' : 'is-err');
    el.hidden = false;
  }

  // ---- nav: show Account / Sign in depending on state
  function paintNav() {
    var menus = document.querySelectorAll('#navmenu');
    Array.prototype.forEach.call(menus, function (ul) {
      if (ul.querySelector('[data-member-link]')) return;
      var li = document.createElement('li');
      li.setAttribute('data-member-link', '');
      var r = M.record();
      li.innerHTML = r
        ? '<a href="account.html">' + (r.name ? String(r.name).split(' ')[0] : 'Account') + '</a>'
        : '<a href="login.html">Sign in</a>';
      var cta = ul.querySelector('.navcta');
      if (cta && cta.parentNode) ul.insertBefore(li, cta.parentNode); else ul.appendChild(li);
    });
  }

  // ---- social providers, only if the server has them configured
  function providers() {
    return fetch(C + '/auth-methods').then(function (r) { return r.json(); })
      .then(function (j) {
        var list = (j.oauth2 && j.oauth2.enabled && j.oauth2.providers) || [];
        return list;
      }).catch(function () { return []; });
  }

  var LABEL = { google: 'Google', facebook: 'Facebook', apple: 'Apple', microsoft: 'Microsoft' };

  // Official brand marks. Each provider's guidelines require their own logo on a
  // sign-in button, so these are the real ones rather than a generic icon.
  var MARK = {
    google: '<svg class="pmark" viewBox="0 0 48 48" aria-hidden="true" focusable="false">' +
      '<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>' +
      '<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>' +
      '<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>' +
      '<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>',
    facebook: '<svg class="pmark" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path fill="#1877F2" d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.09 10.12 24v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.69 4.54-4.69 1.31 0 2.69.24 2.69.24v2.97h-1.51c-1.49 0-1.96.93-1.96 1.88v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.09 24 18.1 24 12.07z"/></svg>',
    microsoft: '<svg class="pmark" viewBox="0 0 23 23" aria-hidden="true" focusable="false">' +
      '<path fill="#F25022" d="M1 1h10v10H1z"/><path fill="#7FBA00" d="M12 1h10v10H12z"/>' +
      '<path fill="#00A4EF" d="M1 12h10v10H1z"/><path fill="#FFB900" d="M12 12h10v10H12z"/></svg>',
    apple: '<svg class="pmark" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path fill="#fff" d="M17.05 12.53c-.02-2.2 1.8-3.26 1.88-3.31-1.03-1.5-2.62-1.71-3.19-1.73-1.36-.14-2.65.8-3.34.8-.69 0-1.75-.78-2.88-.76-1.48.02-2.85.86-3.61 2.18-1.54 2.67-.39 6.62 1.11 8.79.73 1.06 1.6 2.25 2.75 2.21 1.1-.05 1.52-.71 2.85-.71 1.33 0 1.71.71 2.88.69 1.19-.02 1.94-1.08 2.66-2.15.84-1.23 1.19-2.42 1.21-2.48-.03-.01-2.32-.89-2.34-3.53zM14.9 5.2c.61-.74 1.02-1.77.91-2.8-.88.04-1.94.59-2.57 1.32-.56.65-1.05 1.7-.92 2.7.98.08 1.98-.5 2.58-1.22z"/></svg>'
  };

  function mountSocial(hostId, statusEl) {
    var host = document.getElementById(hostId);
    if (!host) return;
    providers().then(function (list) {
      if (!list.length) { host.hidden = true; return; }
      host.hidden = false;
      host.innerHTML = list.map(function (p) {
        return '<button type="button" class="btn oauth oauth-' + p.name + '" data-provider="' + p.name + '">' +
               (MARK[p.name] || '') + '<span>Continue with ' + (LABEL[p.name] || p.name) + '</span></button>';
      }).join('') + '<div class="oauthsep"><span>or use your email</span></div>';

      Array.prototype.forEach.call(host.querySelectorAll('.oauth'), function (b) {
        b.addEventListener('click', function () {
          var p = list.filter(function (x) { return x.name === b.getAttribute('data-provider'); })[0];
          if (!p) return;
          try {
            sessionStorage.setItem('ia_oauth', JSON.stringify({
              provider: p.name, codeVerifier: p.codeVerifier, state: p.state,
              next: location.pathname.indexOf('account') !== -1 ? 'account.html' : 'account.html'
            }));
          } catch (e) { say(statusEl, 'Your browser is blocking storage, so sign-in cannot continue.', false); return; }
          var redirect = location.origin + location.pathname.replace(/[^/]*$/, '') + 'oauth.html';
          location.href = p.authURL + encodeURIComponent(redirect);
        });
      });
    });
  }
  M.mountSocial = mountSocial;

  // ---- email signup / login
  M.wireSignup = function (formId, statusId) {
    var f = document.getElementById(formId); if (!f) return;
    var st = document.getElementById(statusId);
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (typeof f.reportValidity === 'function' && !f.reportValidity()) return;
      var btn = f.querySelector('[type=submit]'), label = btn && btn.textContent;
      var pw = f.querySelector('[name=password]').value;
      var pw2 = f.querySelector('[name=passwordConfirm]').value;
      if (pw !== pw2) { say(st, 'Those two passwords do not match.', false); return; }
      if (pw.length < 8) { say(st, 'Please use at least 8 characters.', false); return; }
      if (btn) { btn.disabled = true; btn.textContent = 'Creating…'; }
      var body = {
        email: f.querySelector('[name=email]').value.trim(),
        password: pw, passwordConfirm: pw2,
        name: f.querySelector('[name=name]').value.trim(),
        phone: (f.querySelector('[name=phone]') || {}).value || '',
        instrument: (f.querySelector('[name=instrument]') || {}).value || ''
      };
      api('/api/collections/members/records', { method: 'POST', body: JSON.stringify(body) })
        .then(function () {
          return api('/api/collections/members/auth-with-password', {
            method: 'POST', body: JSON.stringify({ identity: body.email, password: pw })
          });
        })
        .then(function (a) { M.set(a); location.href = 'account.html'; })
        .catch(function (err) {
          var d = err.data || {};
          say(st, d.email ? 'That email already has an account. Try signing in instead.'
                          : (err.message || 'That did not work. Please try again.'), false);
          if (btn) { btn.disabled = false; btn.textContent = label; }
        });
    });
  };

  M.wireLogin = function (formId, statusId) {
    var f = document.getElementById(formId); if (!f) return;
    var st = document.getElementById(statusId);
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (typeof f.reportValidity === 'function' && !f.reportValidity()) return;
      var btn = f.querySelector('[type=submit]'), label = btn && btn.textContent;
      if (btn) { btn.disabled = true; btn.textContent = 'Signing in…'; }
      api('/api/collections/members/auth-with-password', {
        method: 'POST',
        body: JSON.stringify({
          identity: f.querySelector('[name=email]').value.trim(),
          password: f.querySelector('[name=password]').value
        })
      }).then(function (a) { M.set(a); location.href = 'account.html'; })
        .catch(function () {
          say(st, 'That email and password did not match. Try again, or create an account.', false);
          if (btn) { btn.disabled = false; btn.textContent = label; }
        });
    });
  };

  M.requireLogin = function () {
    if (!M.token()) { location.href = 'login.html'; return false; }
    return true;
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', paintNav);
  else paintNav();
})();
