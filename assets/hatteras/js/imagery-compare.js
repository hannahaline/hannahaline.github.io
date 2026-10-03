// Before/after aerial photo slider for /hatteras/shoreline-change/ (markup in _includes/hatteras/imagery_compare.liquid).
// Places and layers come from _data/hatteras_imagery.yml; the photos are saved by tools/hatteras_imagery_data.py,
// one image per place and layer on the same box, so the right-hand photo is simply clipped at the divider.
(function () {
  "use strict";

  var root = document.getElementById("imgcompare");
  if (!root) return;
  var cfg = JSON.parse(document.getElementById("imgcompare-data").textContent);
  var BASE = root.getAttribute("data-img");
  var NC_CREDIT = "NC OneMap / NC Center for Geographic Information and Analysis";

  var spot = cfg.spots[0], pct = 50, saved = {};
  var byId = {};
  cfg.layers.forEach(function (l) { byId[l.id] = l; });
  var imgBefore = document.getElementById("imgcompare-before-img"), imgAfter = document.getElementById("imgcompare-after-img");

  function credit(id) { return byId[id].credit || NC_CREDIT; }
  function src(id) { return BASE + spot.id + "/" + id + ".jpg"; }

  function fillSelect(sel, value) {
    var have = saved[spot.id] || [];
    sel.innerHTML = cfg.layers.map(function (l) {
      var ok = have.indexOf(l.id) >= 0;
      return '<option value="' + l.id + '"' + (l.id === value ? " selected" : "") + (ok ? "" : " disabled") + ">" +
        l.label + (ok ? "" : " (not available here)") + "</option>";
    }).join("");
  }

  function setLayers(beforeId, afterId) {
    imgBefore.src = src(beforeId);
    imgAfter.src = src(afterId);
    imgBefore.alt = "Aerial photo, " + byId[beforeId].label;
    imgAfter.alt = "Aerial photo, " + byId[afterId].label;
    document.getElementById("imgcompare-tag-before").textContent = byId[beforeId].label;
    document.getElementById("imgcompare-tag-after").textContent = byId[afterId].label;
    var credits = [credit(beforeId), credit(afterId)].filter(function (c, i, a) { return a.indexOf(c) === i; });
    document.getElementById("imgcompare-credit").textContent = "Imagery: " + credits.join("; ") + ".";
  }

  function setSpot(s) {
    spot = s;
    document.querySelectorAll("#imgcompare-spots button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-id") === s.id); });
    fillSelect(document.getElementById("imgcompare-before"), s.before);
    fillSelect(document.getElementById("imgcompare-after"), s.after);
    document.getElementById("imgcompare-caption").textContent = s.caption;
    pct = s.split || 50;
    document.getElementById("imgcompare-range").value = pct;
    clip();
    setLayers(s.before, s.after);
  }

  function clip() {
    imgAfter.style.clipPath = "inset(0 0 0 " + pct + "%)";
    document.getElementById("imgcompare-divider").style.left = pct + "%";
  }

  function start() {
    var spots = document.getElementById("imgcompare-spots");
    cfg.spots.forEach(function (s) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = s.name;
      b.setAttribute("data-id", s.id);
      b.addEventListener("click", function () { setSpot(s); });
      spots.appendChild(b);
    });
    var before = document.getElementById("imgcompare-before"), after = document.getElementById("imgcompare-after");
    before.addEventListener("change", function () { setLayers(before.value, after.value); });
    after.addEventListener("change", function () { setLayers(before.value, after.value); });
    document.getElementById("imgcompare-range").addEventListener("input", function (e) { pct = +e.target.value; clip(); });
    fetch(root.getAttribute("data-index")).then(function (r) { return r.json(); }).then(function (d) {
      saved = d.saved;
      setSpot(spot);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
