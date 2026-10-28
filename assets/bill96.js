/* NorthLedger Tools: Québec French checklist + language-signal estimator.
   Runs entirely in the browser. No network requests, no storage, no cookies. Data comes from the JSON block #b96-data. */
(function (root) {
  "use strict";
  // Same tokenizer and thresholds as gapcheck.py (WORD_RE, lang_estimate). t_bill96.js checks the two agree.
  var WORD_RE = /[a-zàâçéèêëîïôûùüÿœ]+/g;
  function langEstimate(text, FR, EN) {
    var w = String(text || "").toLowerCase().match(WORD_RE) || [];
    var fs = {}, es = {}, i, fr = 0, en = 0;
    for (i = 0; i < FR.length; i++) fs[FR[i]] = 1;
    for (i = 0; i < EN.length; i++) es[EN[i]] = 1;
    for (i = 0; i < w.length; i++) { if (fs[w[i]] === 1) fr++; if (es[w[i]] === 1) en++; }
    var n = fr + en;
    if (n < 25) return { kind: "few", fr: fr, en: en, n: n, share_fr: null };
    var s = fr / n;
    return { kind: s >= 0.65 ? "fr" : s <= 0.35 ? "en" : "mix", fr: fr, en: en, n: n, share_fr: Math.round(s * 1000) / 1000 };
  }
  root.B96 = { langEstimate: langEstimate };
  if (typeof module !== "undefined" && module.exports) module.exports = root.B96;
  if (typeof document === "undefined") return;

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  var D = JSON.parse(document.getElementById("b96-data").textContent), U = D.ui;
  var NB = D.lang === "fr" ? "\u00a0" : " ";  // non-breaking space inside guillemets in French (OQLF)
  var $ = function (id) { return document.getElementById(id); };
  var lastText = "";
  (function () { var d = new Date(); D.today = d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); })();

  function answerOf(id) { var r = document.querySelector('input[name="q_' + id + '"]:checked'); return r ? r.value : ""; }

  function buildList() {
    var groups = { review: [], none: [], yes: [], na: [] };
    D.rules.forEach(function (r) {
      var a = answerOf(r.id);
      (a === "no" || a === "unsure" ? groups.review : a === "yes" ? groups.yes : a === "na" ? groups.na : groups.none).push({ r: r, a: a });
    });
    var h = [], t = [];
    h.push("<h3>" + esc(U.list_title) + "</h3>"); t.push(U.list_title.toUpperCase());
    t.push(U.list_date + " " + D.today); t.push("");
    function sec(key, title, intro, withDetail) {
      var g = groups[key]; if (!g.length) return;
      h.push("<h4>" + esc(title) + " (" + g.length + ")</h4>"); t.push(title + " (" + g.length + ")");
      if (intro) { h.push("<p class=\"hint\">" + esc(intro) + "</p>"); t.push(intro); }
      h.push("<ol>");
      g.forEach(function (x, i) {
        var r = x.r, ans = x.a ? " <span class=\"hint\">(" + esc(U.your_answer) + " " + esc(U.ans[x.a]) + ")</span>" : "";
        var li = "<li><b>" + esc(r.label) + "</b>" + ans;
        t.push((i + 1) + ". " + r.label + (x.a ? " (" + U.your_answer + " " + U.ans[x.a] + ")" : ""));
        if (withDetail) {
          li += "<br>" + esc(r.todo);
          t.push("   " + r.todo);
          li += "<br><span class=\"hint\">" + esc(U.sources) + " " + r.sources.map(function (s) { return "<a href=\"" + esc(s.url) + "\" rel=\"noopener\">" + esc(s.label) + "</a>"; }).join("; ") + "</span>";
          t.push("   " + U.sources + " " + r.sources.map(function (s) { return s.label + " <" + s.url + ">"; }).join("; "));
          li += "<details><summary>" + esc(U.quotes) + "</summary>" + r.quotes.map(function (q) {
            return "<blockquote>" + esc(q.text) + "<br><span class=\"hint\">" + esc(q.src) + (q.note ? " — " + esc(q.note) : "") + "</span></blockquote>"; }).join("") + "</details>";
          r.quotes.forEach(function (q) { t.push("   «" + NB + q.text + NB + "» (" + q.src + (q.note ? ", " + q.note : "") + ")"); });
        }
        h.push(li + "</li>");
      });
      h.push("</ol>"); t.push("");
    }
    sec("review", U.g_review, U.g_review_intro, true);
    sec("none", U.g_none, U.g_none_intro, true);
    sec("yes", U.g_yes, U.g_yes_intro, false);
    sec("na", U.g_na, "", false);
    h.push("<p class=\"disc\">" + esc(U.disclaimer) + "</p>"); t.push(U.disclaimer);
    $("b96-out").innerHTML = h.join(""); $("b96-out-card").hidden = false;
    $("b96-out-card").scrollIntoView && $("b96-out-card").scrollIntoView({ behavior: "smooth", block: "start" });
    lastText = t.join("\n");
    $("b96-status").textContent = "";
  }

  function copyList() {
    if (!lastText) return;
    function done(ok) { $("b96-status").textContent = ok ? U.copied : U.copy_failed; }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(lastText).then(function () { done(true); }, function () { done(false); });
    else { var ta = document.createElement("textarea"); ta.value = lastText; document.body.appendChild(ta); ta.select(); var ok = false; try { ok = document.execCommand("copy"); } catch (e) {} document.body.removeChild(ta); done(ok); }
  }

  function runEstimate() {
    var r = langEstimate($("b96-text").value, D.words.fr, D.words.en), o = $("b96-est-out");
    var kind = U.kinds[r.kind];
    var pct = r.share_fr === null ? "" : " " + U.est_share + " " + (r.share_fr * 100).toFixed(1).replace(".", U.dec) + " %.";
    o.textContent = U.est_counts.replace("{fr}", r.fr).replace("{en}", r.en) + pct + " " + U.est_reading + " " + kind + ".";
  }

  $("b96-make").addEventListener("click", buildList);
  $("b96-copy").addEventListener("click", copyList);
  $("b96-print").addEventListener("click", function () { window.print(); });
  $("b96-est").addEventListener("click", runEstimate);
  $("b96-reset").addEventListener("click", function () {
    document.querySelectorAll("#b96-form input[type=radio]").forEach(function (x) { x.checked = false; });
    $("b96-out-card").hidden = true; lastText = "";
  });
})(typeof window !== "undefined" ? window : globalThis);
