/* gate.js — client-side unlock for set-text study content.
 *
 * The scene map, quote bank and deck ship as AES-GCM ciphertext (see
 * tools/encrypt_content.py). This asks for the passphrase once, derives the key with
 * PBKDF2 using the same parameters, and decrypts in the browser. The derived key is
 * held in sessionStorage so a reload doesn't re-prompt.
 *
 * THIS IS OBFUSCATION, NOT SECURITY. The ciphertext is served publicly and the
 * passphrase is short and shared — anyone who learns it can decrypt everything, and
 * anyone can read this file to see exactly how. It stops a passer-by reading personal
 * study notes. It is not access control, and nothing sensitive belongs behind it.
 *
 * Exposes window.ContentGate.getJSON(baseUrl, name) -> Promise<object>, which returns
 * plaintext JSON when the folder is unencrypted and decrypted JSON when it is not, so
 * callers don't need to care which mode they're in.
 */
(function () {
  "use strict";

  var KEY_PREFIX = "ptsgate:";      // sessionStorage key per content folder
  var keyCache = {};                // baseUrl -> CryptoKey
  var gateCache = {};               // baseUrl -> gate.json (or null when absent)
  var pending = null;               // in-flight prompt, so parallel loads ask once

  function b64ToBytes(b64) {
    var bin = atob(String(b64).trim());
    var out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  function bytesToB64(bytes) {
    var s = "";
    for (var i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
    return btoa(s);
  }

  function loadGate(base) {
    if (Object.prototype.hasOwnProperty.call(gateCache, base)) return Promise.resolve(gateCache[base]);
    return fetch(base + "gate.json", { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
      .then(function (g) { gateCache[base] = g; return g; });
  }

  function importKey(raw) {
    return crypto.subtle.importKey("raw", raw, { name: "AES-GCM" }, false, ["decrypt"]);
  }

  function deriveKey(passphrase, gate) {
    var enc = new TextEncoder();
    return crypto.subtle.importKey("raw", enc.encode(passphrase), "PBKDF2", false, ["deriveBits"])
      .then(function (base) {
        return crypto.subtle.deriveBits({
          name: "PBKDF2",
          salt: b64ToBytes(gate.salt),
          iterations: gate.iterations || 150000,
          hash: "SHA-256",
        }, base, 256);
      });
  }

  function cachedKeyBits(base) {
    try {
      var v = sessionStorage.getItem(KEY_PREFIX + base);
      return v ? b64ToBytes(v) : null;
    } catch (e) { return null; }
  }
  function cacheKeyBits(base, bits) {
    try { sessionStorage.setItem(KEY_PREFIX + base, bytesToB64(new Uint8Array(bits))); } catch (e) {}
  }

  function decrypt(key, b64) {
    var blob = b64ToBytes(b64);
    var iv = blob.slice(0, 12), body = blob.slice(12);
    return crypto.subtle.decrypt({ name: "AES-GCM", iv: iv }, key, body)
      .then(function (buf) { return JSON.parse(new TextDecoder().decode(buf)); });
  }

  // Ask once, verify against a real file, and keep asking until it works or is cancelled.
  function unlock(base, gate, probeFile) {
    if (pending) return pending;
    pending = (function ask(msg) {
      var phrase = window.prompt(msg ||
        "This study content is locked.\nEnter your unlock phrase:");
      if (phrase === null) return Promise.reject(new Error("cancelled"));
      return deriveKey(phrase, gate)
        .then(function (bits) {
          return importKey(bits).then(function (key) {
            return fetch(base + probeFile, { cache: "no-store" })
              .then(function (r) { return r.text(); })
              .then(function (t) { return decrypt(key, t); })
              .then(function () { cacheKeyBits(base, bits); keyCache[base] = key; return key; });
          });
        })
        .catch(function (e) {
          if (e && e.message === "cancelled") throw e;
          return ask("That phrase didn't work.\nTry again:");
        });
    })().then(function (k) { pending = null; return k; },
             function (e) { pending = null; throw e; });
    return pending;
  }

  function getKey(base, gate, probeFile) {
    if (keyCache[base]) return Promise.resolve(keyCache[base]);
    var bits = cachedKeyBits(base);
    if (bits) {
      return importKey(bits).then(function (k) { keyCache[base] = k; return k; });
    }
    return unlock(base, gate, probeFile);
  }

  /** Fetch `name` from `base`, decrypting if that folder is gated. */
  function getJSON(base, name) {
    return loadGate(base).then(function (gate) {
      if (!gate || !gate.files || gate.files.indexOf(name + ".enc") === -1) {
        // Not gated (local dev, or this file wasn't encrypted) — plain fetch.
        return fetch(base + name, { cache: "no-store" }).then(function (r) {
          if (!r.ok) throw new Error(name + ": HTTP " + r.status);
          return r.json();
        });
      }
      return getKey(base, gate, gate.files[0]).then(function (key) {
        return fetch(base + name + ".enc", { cache: "no-store" })
          .then(function (r) {
            if (!r.ok) throw new Error(name + ".enc: HTTP " + r.status);
            return r.text();
          })
          .then(function (t) { return decrypt(key, t); });
      });
    });
  }

  function lock() {
    keyCache = {};
    try {
      Object.keys(sessionStorage)
        .filter(function (k) { return k.indexOf(KEY_PREFIX) === 0; })
        .forEach(function (k) { sessionStorage.removeItem(k); });
    } catch (e) {}
  }

  window.ContentGate = { getJSON: getJSON, lock: lock };
})();
