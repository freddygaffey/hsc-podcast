/* plotmap.js — interactive plot map for English Standard set texts.
 *
 * Renders a narrative arc from content/<subject>/<text>/scenes.json: x is position
 * through the book, y is dramatic intensity derived from arcStage, so the climax
 * reads as the peak. Tapping a scene opens its summary and its quotes, and seeks
 * the audio to that point.
 *
 * Position is tracked as a PERCENTAGE through the book, never as a timestamp, so
 * the map follows whatever audio the listener supplies regardless of its length.
 *
 * The novel itself is in copyright and is not distributed with this app. The player
 * ships a short placeholder track; the listener loads their own audiobook file, which
 * is held locally in IndexedDB and never uploaded.
 */
(function () {
  "use strict";

  var TEXT_BASE = "content/english-standard/past-the-shallows/";
  var STAGE_Y = { exposition: 0.22, rising: 0.55, climax: 1.0, falling: 0.45, resolution: 0.2 };
  var STAGE_LABEL = {
    exposition: "Exposition", rising: "Rising action",
    climax: "Climax", falling: "Falling action", resolution: "Resolution",
  };

  var scenes = [], quotes = [], activeId = null, audio = null, loaded = false;
  var root, svgWrap, detailEl, statusEl, placeholderUrl = null, priv = null;

  /* ---------- tiny IndexedDB store for the listener's own audio file ---------- */
  var DB = "pts-audio", STORE = "files";
  function idb() {
    return new Promise(function (res, rej) {
      var r = indexedDB.open(DB, 1);
      r.onupgradeneeded = function () {
        if (!r.result.objectStoreNames.contains(STORE)) r.result.createObjectStore(STORE);
      };
      r.onsuccess = function () { res(r.result); };
      r.onerror = function () { rej(r.error); };
    });
  }
  function idbPut(key, val) {
    return idb().then(function (db) {
      return new Promise(function (res, rej) {
        var tx = db.transaction(STORE, "readwrite");
        tx.objectStore(STORE).put(val, key);
        tx.oncomplete = res; tx.onerror = function () { rej(tx.error); };
      });
    });
  }
  function idbGet(key) {
    return idb().then(function (db) {
      return new Promise(function (res, rej) {
        var tx = db.transaction(STORE, "readonly");
        var q = tx.objectStore(STORE).get(key);
        q.onsuccess = function () { res(q.result); };
        q.onerror = function () { rej(q.error); };
      });
    });
  }

  /* ---------- position <-> scene ---------- */
  function pctNow() {
    if (!audio || !audio.duration || !isFinite(audio.duration)) return null;
    return (audio.currentTime / audio.duration) * 100;
  }
  function sceneAtPct(p) {
    if (p == null) return null;
    for (var i = 0; i < scenes.length; i++) {
      if (p >= scenes[i].startPct && p < scenes[i].endPct) return scenes[i];
    }
    return scenes.length ? scenes[scenes.length - 1] : null;
  }

  /* ---------- rendering ---------- */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  var W = 1400, H = 300, PAD_T = 34, PAD_B = 58;

  function xOf(pct) { return (pct / 100) * (W - 40) + 20; }
  function yOf(sc) {
    var base = STAGE_Y[sc.arcStage] != null ? STAGE_Y[sc.arcStage] : 0.5;
    // Give the long "rising" stretch a gentle ramp so it climbs toward the climax.
    if (sc.arcStage === "rising") {
      var rs = scenes.filter(function (s) { return s.arcStage === "rising"; });
      var i = rs.indexOf(sc);
      if (i >= 0 && rs.length > 1) base = 0.34 + (0.44 * i) / (rs.length - 1);
    }
    return PAD_T + (1 - base) * (H - PAD_T - PAD_B);
  }

  function buildSvg() {
    var pts = scenes.map(function (s) {
      return [xOf((s.startPct + s.endPct) / 2), yOf(s)];
    });
    var path = pts.map(function (p, i) { return (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1); }).join(" ");
    var area = path + " L" + pts[pts.length - 1][0].toFixed(1) + " " + (H - PAD_B) +
               " L" + pts[0][0].toFixed(1) + " " + (H - PAD_B) + " Z";

    // Band labels. The last three stages each occupy only a few percent of the book,
    // so their labels collide on a single baseline. Lay them out with real collision
    // detection: measure each label's extent, clamp it inside the viewBox, then drop it
    // to the first row where it clears whatever is already on that row.
    var bands = "", labels = "";
    var rowRight = [];             // rightmost occupied x per row
    var seen = {};
    scenes.forEach(function (s) {
      if (seen[s.arcStage]) return;
      seen[s.arcStage] = 1;
      var group = scenes.filter(function (x) { return x.arcStage === s.arcStage; });
      var x0 = xOf(group[0].startPct), x1 = xOf(group[group.length - 1].endPct);
      bands += '<rect class="pm-band pm-band-' + s.arcStage + '" x="' + x0.toFixed(1) + '" y="' + PAD_T +
               '" width="' + Math.max(1, x1 - x0).toFixed(1) + '" height="' + (H - PAD_T - PAD_B) + '"/>';

      var label = STAGE_LABEL[s.arcStage] || s.arcStage;
      var half = (label.length * 7.5) / 2;      // ~13px uppercase with letter-spacing
      var cx = (x0 + x1) / 2;
      cx = Math.max(half + 2, Math.min(W - half - 2, cx));   // keep inside the viewBox
      var left = cx - half, right = cx + half;

      var row = 0;
      while (rowRight[row] != null && left < rowRight[row] + 8) row++;
      rowRight[row] = right;

      labels += '<text class="pm-bandlabel" x="' + cx.toFixed(1) +
                '" y="' + (H - PAD_B + 20 + row * 15) + '">' + esc(label) + "</text>";
    });
    bands += labels;

    // Both the turning point and its aftermath are tagged climax; label the run once
    // so the two captions don't overprint each other.
    var climaxScenes = scenes.filter(function (x) { return x.arcStage === "climax"; });
    var climaxLabelId = climaxScenes.length ? climaxScenes[0].id : null;

    var nodes = scenes.map(function (s, i) {
      var cx = xOf((s.startPct + s.endPct) / 2), cy = yOf(s);
      var cls = "pm-node" + (s.arcStage === "climax" ? " pm-node-climax" : "") +
                (s.id === activeId ? " pm-node-active" : "");
      return '<g class="' + cls + '" data-scene="' + esc(s.id) + '" tabindex="0" role="button" ' +
             'aria-label="' + esc(s.order + ". " + s.title) + '">' +
             '<circle cx="' + cx.toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="' +
             (s.arcStage === "climax" ? 11 : 7) + '"/>' +
             '<text class="pm-nodenum" x="' + cx.toFixed(1) + '" y="' + (cy + 4).toFixed(1) + '">' +
             (s.arcStage === "climax" ? "" : s.order) + "</text>" +
             (s.arcStage === "climax" && s.id === climaxLabelId
               ? '<text class="pm-climaxlabel" x="' + cx.toFixed(1) + '" y="' + (cy - 20).toFixed(1) + '">CLIMAX</text>'
               : "") +
             "</g>";
    }).join("");

    return '<svg class="pm-svg" viewBox="0 0 ' + W + " " + H + '" preserveAspectRatio="xMinYMid meet" role="img">' +
      bands +
      '<path class="pm-area" d="' + area + '"/>' +
      '<path class="pm-line" d="' + path + '"/>' +
      '<line class="pm-playhead" id="pm-playhead" x1="0" y1="' + PAD_T + '" x2="0" y2="' + (H - PAD_B) + '" style="display:none"/>' +
      nodes +
      "</svg>";
  }

  function quoteCards(sc) {
    var qs = quotes.filter(function (q) { return q.sceneId === sc.id; });
    if (!qs.length) return '<p class="pm-noquotes">No quotes pinned to this scene yet.</p>';
    return '<ul class="pm-quotes">' + qs.map(function (q) {
      return '<li class="pm-quote pm-pri-' + esc(q.priority) + '">' +
        '<blockquote>&ldquo;' + esc(q.quote) + '&rdquo;</blockquote>' +
        '<div class="pm-qmeta">' + esc(q.theme || "") +
        (q.chapter != null ? " &middot; ch " + esc(q.chapter) : "") +
        (q.pdfPage != null ? " &middot; p" + esc(q.pdfPage) : "") + "</div>" +
        (q.mnemonic ? '<div class="pm-qmnemonic">' + esc(q.mnemonic) + "</div>" : "") +
        "</li>";
    }).join("") + "</ul>";
  }

  function renderDetail(sc) {
    if (!sc) { detailEl.innerHTML = '<p class="pm-hint">Pick a scene on the arc above.</p>'; return; }
    var chap = sc.chapters && sc.chapters.length
      ? "ch " + sc.chapters.join(", ")
      : '<span class="pm-unverified" title="The source text has no chapter markers; this scene is not pinned to a verified chapter">chapter not pinned</span>';
    detailEl.innerHTML =
      '<div class="pm-dhead">' +
        '<span class="pm-stage pm-stage-' + esc(sc.arcStage) + '">' + esc(STAGE_LABEL[sc.arcStage] || sc.arcStage) + "</span>" +
        "<h3>" + esc(sc.order + ". " + sc.title) + "</h3>" +
      "</div>" +
      '<div class="pm-dmeta">' + chap + " &middot; p" + esc(sc.pdfPageStart) + "&ndash;" + esc(sc.pdfPageEnd) +
        " &middot; " + sc.startPct.toFixed(1) + "%&ndash;" + sc.endPct.toFixed(1) + "% through" +
        (sc.verified ? "" : ' &middot; <span class="pm-unverified">unverified</span>') +
      "</div>" +
      "<p class=\"pm-summary\">" + esc(sc.summary) + "</p>" +
      '<div class="pm-tags">' +
        (sc.characters || []).map(function (c) { return '<span class="pm-tag pm-tag-char">' + esc(c) + "</span>"; }).join("") +
        (sc.themes || []).map(function (t) { return '<span class="pm-tag pm-tag-theme">' + esc(t) + "</span>"; }).join("") +
      "</div>" +
      '<button class="pm-jump" data-jump="' + esc(sc.id) + '">Jump to this scene</button>' +
      "<h4 class=\"pm-qhead\">Quotes here</h4>" + quoteCards(sc);
  }

  function select(id, seek) {
    var sc = scenes.filter(function (s) { return s.id === id; })[0];
    if (!sc) return;
    activeId = id;
    svgWrap.innerHTML = buildSvg();
    renderDetail(sc);
    if (seek && audio && audio.duration && isFinite(audio.duration)) {
      audio.currentTime = (sc.startPct / 100) * audio.duration;
    }
    var node = svgWrap.querySelector('[data-scene="' + id + '"]');
    if (node && node.scrollIntoView) node.scrollIntoView({ inline: "center", block: "nearest", behavior: "smooth" });
  }

  function tick() {
    var p = pctNow();
    var head = document.getElementById("pm-playhead");
    if (p == null || !head) return;
    var x = xOf(p);
    head.setAttribute("x1", x); head.setAttribute("x2", x);
    head.style.display = "";
    var sc = sceneAtPct(p);
    if (sc && sc.id !== activeId) {
      activeId = sc.id;
      svgWrap.innerHTML = buildSvg();
      document.getElementById("pm-playhead").setAttribute("x1", x);
      document.getElementById("pm-playhead").setAttribute("x2", x);
      document.getElementById("pm-playhead").style.display = "";
      renderDetail(sc);
    }
    if (statusEl) {
      statusEl.textContent = sc ? "Now: " + sc.order + ". " + sc.title + "  (" + p.toFixed(1) + "% through)" : "";
    }
  }

  /* ---------- audio source ---------- */
  function setStatus(msg, cls) {
    var el = document.getElementById("pm-source-msg");
    if (el) { el.textContent = msg; el.className = "pm-source-msg " + (cls || ""); }
  }

  function useFile(file) {
    if (!file) return;
    if (!/^audio\//.test(file.type) && !/\.(m4a|m4b|mp3|aac|ogg|opus|wav)$/i.test(file.name)) {
      setStatus("That doesn't look like an audio file.", "pm-err");
      return;
    }
    idbPut("audiobook", file).catch(function () {});
    attachBlob(file);
    setStatus("Loaded: " + file.name + " — stays on this device.", "pm-ok");
  }

  function attachBlob(blob) {
    if (!audio) return;
    try { if (audio.src && audio.src.indexOf("blob:") === 0) URL.revokeObjectURL(audio.src); } catch (e) {}
    audio.src = URL.createObjectURL(blob);
    audio.load();
    loaded = true;
    document.body.classList.add("pm-has-audio");
  }

  // No local file yet: fall back to the placeholder track so the transport behaves like
  // a normal player instead of dying silently. It says the novel isn't included and to
  // load your own file. Picking a file replaces this source entirely.
  function usePlaceholder() {
    if (!audio || loaded || !placeholderUrl) return;
    audio.src = placeholderUrl;
    audio.load();
    document.body.classList.remove("pm-has-audio");
  }

  var TOKEN_KEY = "pts:audiotoken";

  function privUrl(token) {
    return priv.worker.replace(/\/+$/, "") + "/" + priv.key.replace(/^\/+/, "") +
           "?t=" + encodeURIComponent(token);
  }

  // A stored token is good until it expires; only prompt when there isn't a live one.
  function storedToken() {
    try {
      var v = JSON.parse(localStorage.getItem(TOKEN_KEY) || "null");
      return v && v.exp > Math.floor(Date.now() / 1000) + 60 ? v.token : null;
    } catch (e) { return null; }
  }

  function unlockPrivate() {
    if (!priv) return Promise.resolve(false);
    var tok = storedToken();
    if (tok) { attachPrivate(tok); return Promise.resolve(true); }

    var pin = window.prompt("Enter your 4-digit PIN to unlock your audiobook:");
    if (!pin) return Promise.resolve(false);
    setStatus("Checking PIN\u2026", "");
    return fetch(priv.worker.replace(/\/+$/, "") + "/session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pin: String(pin).trim() }),
    }).then(function (r) {
      return r.json().then(function (j) { return { ok: r.ok, status: r.status, body: j }; });
    }).then(function (res) {
      if (res.ok && res.body.token) {
        try { localStorage.setItem(TOKEN_KEY, JSON.stringify(res.body)); } catch (e) {}
        attachPrivate(res.body.token);
        setStatus("Unlocked \u2014 streaming your own copy.", "pm-ok");
        return true;
      }
      if (res.status === 429) {
        setStatus("Too many attempts. Locked out for a few minutes.", "pm-err");
      } else {
        var left = res.body && res.body.attemptsRemaining;
        setStatus("Wrong PIN." + (left != null ? " " + left + " attempts left before lockout." : ""), "pm-err");
      }
      return false;
    }).catch(function (e) {
      setStatus("Could not reach the audio server: " + (e && e.message), "pm-err");
      return false;
    });
  }

  function attachPrivate(token) {
    if (!audio) return;
    audio.src = privUrl(token);
    audio.load();
    loaded = true;
    document.body.classList.add("pm-has-audio");
  }

  function restore() {
    return idbGet("audiobook").then(function (f) {
      if (f) {
        attachBlob(f);
        setStatus("Loaded: " + (f.name || "your file") + " — stays on this device.", "pm-ok");
        return true;
      }
      if (priv && storedToken()) { attachPrivate(storedToken()); return true; }
      usePlaceholder();
      return false;
    }).catch(function () { usePlaceholder(); return false; });
  }

  /* ---------- public ---------- */
  // cfg is the subject manifest entry; we read audioBaseUrl + setTexts[..].placeholderAudio
  // from it so the R2 location lives in subject.json, not hard-coded here.
  function render(container, audioEl, cfg) {
    root = container; audio = audioEl;
    placeholderUrl = null;
    if (cfg && cfg.setTexts) {
      var base = (cfg.audioBaseUrl || "content").replace(/\/+$/, "");
      Object.keys(cfg.setTexts).forEach(function (k) {
        var t = cfg.setTexts[k];
        if (t && t.plotMap && !placeholderUrl) {
          if (t.placeholderAudio) placeholderUrl = base + "/" + String(t.placeholderAudio).replace(/^\/+/, "");
          if (t.privateAudio && t.privateAudio.worker) priv = t.privateAudio;
          if (t.slug) TEXT_BASE = "content/" + cfg.id + "/" + t.slug + "/";
        }
      });
    }
    root.innerHTML =
      '<div class="pm-wrap">' +
        '<div class="pm-source">' +
          '<button class="pm-pick" id="pm-pick">Choose your audiobook file</button>' +
          '<button class="pm-pick pm-pick-alt" id="pm-unlock" hidden>Unlock my audiobook (PIN)</button>' +
          '<input type="file" id="pm-file" accept="audio/*,.m4b,.m4a,.mp3" hidden>' +
          '<div class="pm-source-msg" id="pm-source-msg">Past the Shallows is in copyright, so no recording ships with this app. ' +
            'Load your own file — it stays on this device and is never uploaded.</div>' +
        "</div>" +
        '<div class="pm-status" id="pm-status"></div>' +
        '<div class="pm-svgwrap" id="pm-svgwrap"></div>' +
        '<div class="pm-detail" id="pm-detail"></div>' +
      "</div>";
    svgWrap = document.getElementById("pm-svgwrap");
    detailEl = document.getElementById("pm-detail");
    statusEl = document.getElementById("pm-status");

    if (priv) {
      var ub = document.getElementById("pm-unlock");
      ub.hidden = false;
      ub.addEventListener("click", function () { unlockPrivate(); });
    }
    document.getElementById("pm-pick").addEventListener("click", function () {
      document.getElementById("pm-file").click();
    });
    document.getElementById("pm-file").addEventListener("change", function (e) {
      useFile(e.target.files && e.target.files[0]);
    });
    svgWrap.addEventListener("click", function (e) {
      var g = e.target.closest && e.target.closest("[data-scene]");
      if (g) select(g.getAttribute("data-scene"), true);
    });
    svgWrap.addEventListener("keydown", function (e) {
      if (e.key !== "Enter" && e.key !== " ") return;
      var g = e.target.closest && e.target.closest("[data-scene]");
      if (g) { e.preventDefault(); select(g.getAttribute("data-scene"), true); }
    });
    detailEl.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-jump]");
      if (b) select(b.getAttribute("data-jump"), true);
    });

    // ContentGate transparently handles both plaintext (local dev) and the encrypted
    // build produced by tools/encrypt_content.py, prompting once if the folder is gated.
    var get = (window.ContentGate && window.ContentGate.getJSON)
      ? function (n) { return window.ContentGate.getJSON(TEXT_BASE, n); }
      : function (n) { return fetch(TEXT_BASE + n, { cache: "no-store" }).then(function (r) { return r.json(); }); };

    var load = Promise.all([get("scenes.json"), get("quotes.json")]).then(function (res) {
      scenes = res[0].scenes || [];
      quotes = res[1].quotes || [];
      svgWrap.innerHTML = buildSvg();
      renderDetail(null);
    }).catch(function (err) {
      svgWrap.innerHTML = '<p class="pm-err">Could not load the scene map. ' + esc(err && err.message) + "</p>";
    });

    if (audio && !audio.__pmBound) {
      audio.__pmBound = true;
      audio.addEventListener("timeupdate", tick);
      audio.addEventListener("seeked", tick);
    }
    restore();
    return load;
  }

  window.PlotMap = { render: render, select: select, hasAudio: function () { return loaded; } };
})();
