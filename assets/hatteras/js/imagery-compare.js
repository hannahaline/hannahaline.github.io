// Before/after aerial photo slider for /hatteras/shoreline-change/ (markup in _includes/hatteras/imagery_compare.liquid).
// Layers and spots come from _data/hatteras_imagery.yml; the right-hand photo is clipped at the divider.
(function () {
  "use strict";

  var root = document.getElementById("imgcompare");
  if (!root) return;
  var cfg = JSON.parse(document.getElementById("imgcompare-data").textContent);
  var NCONEMAP = "https://services.nconemap.gov/secure/rest/services/Imagery/";
  var NC_CREDIT = "NC OneMap / NC Center for Geographic Information and Analysis";

  var map, spot = cfg.spots[0], left, right, pct = 50;
  var byId = {};
  cfg.layers.forEach(function (l) { byId[l.id] = l; });

  // NC OneMap year services are not cached, so each 256 px tile is an exportImage of its Web Mercator box;
  // jpgpng returns PNG where a tile has no data, so the water colour shows through instead of black
  var ExportLayer = L.TileLayer.extend({
    getTileUrl: function (c) {
      var size = 2 * Math.PI * 6378137 / Math.pow(2, c.z);  // tile width in metres
      var x0 = -Math.PI * 6378137 + c.x * size, y1 = Math.PI * 6378137 - c.y * size;
      return this._url + "?bbox=" + [x0, y1 - size, x0 + size, y1].map(function (v) { return v.toFixed(2); }).join(",") +
        "&bboxSR=3857&imageSR=3857&size=256,256&format=jpgpng&f=image";
    }
  });

  function makeLayer(id, pane) {
    var l = byId[id];
    if (l.xyz) return L.tileLayer(l.xyz, { pane: pane, maxZoom: 19, maxNativeZoom: 19 });
    return new ExportLayer(NCONEMAP + l.nconemap + "/ImageServer/exportImage", { pane: pane, maxZoom: 19 });
  }

  function credit(id) { return byId[id].credit || NC_CREDIT; }

  function fillSelect(sel, value) {
    sel.innerHTML = cfg.layers.map(function (l) {
      return '<option value="' + l.id + '"' + (l.id === value ? " selected" : "") + ">" + l.label + "</option>";
    }).join("");
  }

  function setLayers(beforeId, afterId) {
    if (left) map.removeLayer(left);
    if (right) map.removeLayer(right);
    left = makeLayer(beforeId, "hatBefore").addTo(map);
    right = makeLayer(afterId, "hatAfter").addTo(map);
    document.getElementById("imgcompare-tag-before").textContent = byId[beforeId].label;
    document.getElementById("imgcompare-tag-after").textContent = byId[afterId].label;
    var credits = [credit(beforeId), credit(afterId)].filter(function (c, i, a) { return a.indexOf(c) === i; });
    document.getElementById("imgcompare-credit").textContent = "Imagery: " + credits.join("; ") + ".";
    clip();
  }

  function setSpot(s) {
    spot = s;
    document.querySelectorAll("#imgcompare-spots button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-id") === s.id); });
    fillSelect(document.getElementById("imgcompare-before"), s.before);
    fillSelect(document.getElementById("imgcompare-after"), s.after);
    document.getElementById("imgcompare-caption").textContent = s.caption;
    map.setView(s.centre, s.zoom);
    pct = s.split || 50;
    document.getElementById("imgcompare-range").value = pct;
    setLayers(s.before, s.after);
  }

  // Clip both panes at the divider; panes move with the map, so work in layer points
  function clip() {
    var size = map.getSize(), x = size.x * pct / 100;
    var nw = map.containerPointToLayerPoint([0, 0]), se = map.containerPointToLayerPoint(size);
    var cx = nw.x + x;
    map.getPane("hatBefore").style.clip = "rect(" + [nw.y, cx, se.y, nw.x].join("px,") + "px)";
    map.getPane("hatAfter").style.clip = "rect(" + [nw.y, se.x, se.y, cx].join("px,") + "px)";
    document.getElementById("imgcompare-divider").style.left = x + "px";
  }

  function start() {
    if (typeof L === "undefined") return setTimeout(start, 100);
    map = L.map("imgcompare-map", { scrollWheelZoom: false, zoomSnap: 0.5, minZoom: 12, maxZoom: 19, attributionControl: false });
    map.createPane("hatBefore").style.zIndex = 200;
    map.createPane("hatAfter").style.zIndex = 201;
    map.on("move zoom resize", clip);

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
    // #spot=<id> opens a given place, for links from other pages
    var m = /spot=(\w+)/.exec(location.hash);
    cfg.spots.forEach(function (s) { if (m && s.id === m[1]) spot = s; });
    setSpot(spot);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
