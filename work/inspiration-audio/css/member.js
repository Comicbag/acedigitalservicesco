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

  function mountSocial(hostId, statusEl) {
    var host = document.getElementById(hostId);
    if (!host) return;
    providers().then(function (list) {
      if (!list.length) { host.hidden = true; return; }
      host.hidden = false;
      host.innerHTML = list.map(function (p) {
        return '<button type="button" class="btn btn-ghost oauth" data-provider="' + p.name + '">' +
               'Continue with ' + (LABEL[p.name] || p.name) + '</button>';
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
