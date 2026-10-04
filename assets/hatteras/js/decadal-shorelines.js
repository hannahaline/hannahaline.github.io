// Shorelines through time, /hatteras/shoreline-change/through-time/ (markup in _includes/hatteras/decadal_map.liquid).
// Data: assets/hatteras/data/decadal_shorelines.json, from tools/hatteras_decadal_shorelines.py: the average shoreline
// of one calendar year per decade, and the zoom spots with their change. Background photos are NC OneMap orthoimagery, drawn as one exportImage per view (re-requested after each
// pan or zoom), so any year can sit under the lines at any scale.
(function () {
  "use strict";

  var root = document.getElementById("decadal");
  if (!root) return;
  var NCONEMAP = "https://services.nconemap.gov/secure/rest/services/Imagery/";
  // one sequential gradient (YlOrRd), oldest light to newest dark, so the order reads without the key
  var RAMP = ["#ffeda0", "#feb24c", "#fd8d3c", "#e31a1c", "#800026"];
  var COLORS = {};
  var PHOTOS = {
    latest: null,
    1993: { service: "DOQQ_NC_1993", label: "1993 (black and white)" },
    2002: { service: "Orthoimagery_2002", label: "2002" },
    2016: { service: "Orthoimagery_2016_2019", label: "Jan–Feb 2016" },
    2024: { service: "Orthoimagery_20242027", label: "Mar 2024" }
  };

  var map, data, latest, photo = null, overlay = null, request = 0, lines = {};

  // One image for the whole view from an ImageServer; jpgpng keeps areas outside the flight transparent
  function drawPhoto() {
    if (!photo) return;
    var b = map.getBounds(), size = map.getSize(), crs = L.CRS.EPSG3857;
    var sw = crs.project(b.getSouthWest()), ne = crs.project(b.getNorthEast());
    var scale = Math.min(window.devicePixelRatio || 1, 2);
    var url = NCONEMAP + PHOTOS[photo].service + "/ImageServer/exportImage?bbox=" + [sw.x, sw.y, ne.x, ne.y].map(function (v) { return v.toFixed(1); }).join(",") +
      "&bboxSR=3857&imageSR=3857&size=" + Math.round(size.x * scale) + "," + Math.round(size.y * scale) + "&format=jpgpng&f=image";
    var mine = ++request, img = new Image();
    root.classList.add("loading");
    img.onload = function () {
      if (mine !== request || !photo) return;
      if (overlay) map.removeLayer(overlay);
      overlay = L.imageOverlay(url, b, { pane: "photo", interactive: false, attribution: "Imagery: NC OneMap" }).addTo(map);
      root.classList.remove("loading");
    };
    img.onerror = function () { if (mine === request) root.classList.remove("loading"); };
    img.src = url;
  }

  function setPhoto(id) {
    photo = id === "latest" ? null : id;
    root.querySelectorAll("#decadal-photos button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-photo") === id); });
    if (overlay) { map.removeLayer(overlay); overlay = null; }
    request++;
    root.classList.remove("loading");
    // older flights stop short of the open ocean: the map's water colour shows there
    if (photo) { map.removeLayer(latest); drawPhoto(); }
    else latest.addTo(map);
  }

  function setYear(y, on) {
    if (on) lines[y].addTo(map); else map.removeLayer(lines[y]);
  }

  function span(y) {
    return data.half_window ? (y - data.half_window) + "–" + Math.min(y + data.half_window, 2026) : String(y);
  }

  function build() {
    map = L.map("decadal-map", { scrollWheelZoom: false, zoomSnap: 0.5, preferCanvas: false });
    map.createPane("photo").style.zIndex = 250;
    latest = L.layerGroup([
      L.tileLayer("https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 16, attribution: "USGS The National Map"
      }),
      L.tileLayer("https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_Latest_cached/ImageServer/tile/{z}/{y}/{x}", {
        minZoom: 12, maxZoom: 19, attribution: "Imagery: NC OneMap / NC Center for Geographic Information and Analysis"
      })
    ]).addTo(map);

    var all = [];
    data.years.forEach(function (y, i) {
      COLORS[y] = RAMP[Math.round(i * (RAMP.length - 1) / Math.max(data.years.length - 1, 1))];
      var segs = data.lines[String(y)];
      // a thin dark casing under each line keeps the pale early years visible on bright sand
      var group = L.layerGroup([].concat.apply([], segs.map(function (seg) {
        return [L.polyline(seg, { color: "#1a1a1a", weight: 4.5, opacity: 0.55, interactive: false }),
          L.polyline(seg, { color: COLORS[y], weight: 2.5, opacity: 1 })
            .bindTooltip("Average shoreline, " + span(y), { sticky: true, className: "hat-tip" })];
      })));
      lines[y] = group.addTo(map);
      segs.forEach(function (seg) { all = all.concat(seg); });
    });
    data.places.forEach(function (p) {
      L.marker(p.ll, { icon: L.divIcon({ className: "hat-place", html: "<span>" + p.name + "</span>", iconSize: null }), interactive: false }).addTo(map);
    });
    map.fitBounds(L.latLngBounds(all), { padding: [20, 20] });
    map.on("moveend", drawPhoto);

    var key = root.querySelector("#decadal-years");
    key.innerHTML = '<div class="hat-decadal-bar" style="background:linear-gradient(to right,' + RAMP.join(",") + ')"></div>' +
      '<div class="hat-decadal-ticks">' + data.years.map(function (y) {
        return '<label><input type="checkbox" data-year="' + y + '" checked>' + span(y) + "</label>";
      }).join("") + "</div>";
    key.querySelectorAll("input").forEach(function (c) {
      c.addEventListener("change", function () { setYear(+c.getAttribute("data-year"), c.checked); });
    });
    root.querySelectorAll("#decadal-photos button").forEach(function (b) {
      b.addEventListener("click", function () { setPhoto(b.getAttribute("data-photo")); });
    });
    // zoom buttons, labelled with their change: the stretches with the most, and stable ones to compare with
    var first = data.years[0], last = data.years[data.years.length - 1], all = root.querySelectorAll("[data-spots]");
    data.spots.forEach(function (p) {
      var spots = root.querySelector('[data-spots="' + p.kind + '"]');
      spots.setAttribute("title", "Change in the average shoreline from " + first + " to " + last);
      var b = document.createElement("button");
      b.type = "button";
      b.innerHTML = p.name + " <span>" + (p.change > 0 ? "+" : p.change < 0 ? "−" : "") + Math.abs(p.change) + " m</span>";
      b.addEventListener("click", function () {
        all.forEach(function (g) { g.querySelectorAll("button").forEach(function (o) { o.classList.toggle("on", o === b); }); });
        map.setView(p.ll, 16);
        root.querySelector("#decadal-map").scrollIntoView({ behavior: "smooth", block: "center" });
      });
      spots.appendChild(b);
    });
  }

  function start() {
    if (typeof L === "undefined") return setTimeout(start, 100);
    fetch(root.getAttribute("data-src")).then(function (r) { return r.json(); }).then(function (d) { data = d; build(); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
