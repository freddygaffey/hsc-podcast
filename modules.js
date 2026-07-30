/* modules.js — module-level navigation for set-text subjects (English Standard).
 *
 * The course is four modules, so the subject hub lists those rather than a flat pile of
 * tools. Each module owns its text and its study material:
 *
 *   Common Module  ->  Past the Shallows: the book (plot map + audio) and quote flashcards
 *   Module A / B / C -> named set texts, no content built yet
 *
 * Module codes and set texts come from subject.json (groupNames + setTexts), so adding a
 * text later is a data change, not a code change.
 */
(function () {
  "use strict";

  var MODULE_ORDER = ["CM", "MA", "MB", "MC"];
  var SHORT = { CM: "Common Module", MA: "Module A", MB: "Module B", MC: "Module C" };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  var ICON = {
    book: '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5z"/><path d="M8 7h8M8 11h8"/></svg>',
    map: '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17c3-6 5 2 8-4s5 3 10-6"/><circle cx="3" cy="17" r="1.6"/><circle cx="11" cy="13" r="1.6"/><circle cx="21" cy="7" r="1.6"/></svg>',
    cards: '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="13" height="15" rx="2"/><path d="M8 3h11a2 2 0 0 1 2 2v12"/></svg>',
    lock: '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
  };

  function tile(icon, name, meta, href, dim) {
    return '<button class="subject-tile hub-tile' + (dim ? " hub-tile-dim" : "") + '"' +
      (href ? ' data-href="' + esc(href) + '"' : " disabled") + '>' +
      '<span class="hub-tile-icon">' + icon + "</span>" +
      '<span class="hub-tile-text">' +
        '<span class="subject-name">' + esc(name) + "</span>" +
        '<span class="subject-meta">' + esc(meta) + "</span>" +
      "</span>" +
      (href ? '<span class="hub-tile-chev">&#8250;</span>' : "") +
      "</button>";
  }

  function wire(container) {
    container.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-href]");
      if (b) window.location.hash = b.getAttribute("data-href");
    });
  }

  /** Four module tiles for the subject hub. */
  function renderModuleIndex(container, cfg) {
    var id = encodeURIComponent(cfg.id);
    var texts = cfg.setTexts || {}, names = cfg.groupNames || {};
    var html = '<div class="subjects-intro">' +
      '<h1 class="subjects-title">' + esc(cfg.name) + "</h1>" +
      '<p class="subjects-sub">Choose a module</p></div>' +
      '<div class="subjects-grid hub-grid">';

    MODULE_ORDER.forEach(function (code) {
      var t = texts[code] || {};
      var full = names[code] || SHORT[code] || code;
      // Strip the "Module A: " prefix the syllabus name carries, the tile shows it already.
      var elective = full.replace(/^.*?:\s*/, "");
      var ready = !!t.slug;
      var meta = t.text ? t.text + (t.author ? " · " + t.author : "") : elective;
      html += tile(ready ? ICON.book : ICON.lock,
                   SHORT[code] || code,
                   ready ? meta : meta + " · not built yet",
                   ready ? "#/s/" + id + "/m/" + code : null,
                   !ready);
    });

    container.innerHTML = html + "</div>";
    wire(container);
  }

  /** Contents of one module. */
  function renderModule(container, cfg, code) {
    var id = encodeURIComponent(cfg.id);
    var t = (cfg.setTexts || {})[code] || {};
    var full = (cfg.groupNames || {})[code] || SHORT[code] || code;

    var html = '<div class="subjects-intro">' +
      '<h1 class="subjects-title">' + esc(SHORT[code] || code) + "</h1>" +
      '<p class="subjects-sub">' + esc(full) + "</p></div>";

    if (!t.slug) {
      container.innerHTML = html +
        '<p class="pm-hint">' + esc(t.text || "This module") +
        ' has no study material in the app yet.</p>';
      return;
    }

    html += '<div class="subjects-grid hub-grid">' +
      tile(ICON.map, t.text,
           "Plot map, scenes and audio · " + (t.author || ""),
           "#/s/" + id + "/map") +
      tile(ICON.cards, "Quote flashcards",
           "Memorise the key quotes",
           "#/s/" + id + "/cards") +
      "</div>";

    container.innerHTML = html;
    wire(container);
  }

  window.SetTextModules = {
    renderModuleIndex: renderModuleIndex,
    renderModule: renderModule,
    order: MODULE_ORDER,
  };
})();
