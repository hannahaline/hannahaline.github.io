// Shoreline change viewers for the /hatteras/shoreline-change/ sub-pages (markup in _includes/hatteras/shoreline_map.liquid).
// One script for both: the map (Survey lines) and the profile along the island (Along the island); each part is
// built only when its element is on the page.
// Data: assets/hatteras/data/shoreline_rates.json and timeseries/d<NNN>.json, from tools/hatteras_shoreline_data.py;
// the "Change year by year" mode adds shoreline_years.json (tools/hatteras_shoreline_years.py), loaded on first use.
(function () {
  "use strict";

  var root = document.getElementById("shoremap");
  if (!root) return;
  var BASE = root.getAttribute("data-base");
  var HAS_MAP = !!document.getElementById("shoremap-map"), HAS_PROFILE = !!document.getElementById("shoremap-profile");

  // RdBu classes in m/yr, red = landward (eroding), blue = seaward (growing), grey = little change
  var BREAKS = [-3, -2, -1, -0.25, 0.25, 1, 2, 3];
  var COLORS = ["#b2182b", "#d6604d", "#f4a582", "#fddbc7", "#d9d9d9", "#d1e5f0", "#92c5de", "#4393c3", "#2166ac"];
  var LABELS = ["more than 3", "2 to 3", "1 to 2", "0.25 to 1", "less than 0.25", "0.25 to 1", "1 to 2", "2 to 3", "more than 3"];
  var INK = "#1a1a1a", MUTED = "#6b7378", GRID = "#e6e9eb", TEAL = "#2f7f93", FILL = "#c8880f", FILL_BG = "rgba(246, 227, 184, 0.55)";

  // Year-by-year mode: metres from the 1984-86 average, same colours
  var BREAKS_M = [-75, -50, -25, -5, 5, 25, 50, 75];
  var LABELS_M = ["more than 75", "50 to 75", "25 to 50", "5 to 25", "less than 5", "5 to 25", "25 to 50", "50 to 75", "more than 75"];
  var FRAME_MS = 650;
  // smoothed yearly values colour whole stretches alike, so those lines are drawn thinner to read like the rate map
  function weight() { return mode === "years" ? 3 : 4; }

  var data, map, lines = [], casing = [], highlight, win = 0, selected = null, tsChart, profileChart, bases = {};
  var mode = "rates", years = null, yi = 0, timer = null;
  var reachKm = null;  // [south, north] km lit by the timeline (hat:reach)
  var cache = {};

  function cls(r, breaks) {
    if (r === null || r === undefined) return -1;
    for (var i = 0; i < breaks.length; i++) if (r < breaks[i]) return i;
    return breaks.length;
  }
  function color(r) { var c = cls(r, mode === "years" ? BREAKS_M : BREAKS); return c < 0 ? "#9aa0a3" : COLORS[c]; }
  // the value each transect is drawn with: its rate for the period, or its position in the chosen year
  function value(k) { return mode === "years" ? years.v[yi][k] : data.transects[k].r[win]; }

  function fmt(x, d) { return Math.abs(x).toFixed(d === undefined ? 1 : d); }

  // Plain-language reading of one rate and its 95 % uncertainty
  function describe(r, u) {
    if (r === null) return "not enough satellite images to measure";
    if (u !== null && Math.abs(r) < u) return "no clear trend (the change is smaller than the measurement uncertainty)";
    if (Math.abs(r) < 0.25) return "little change (under 0.25 m per year)";
    var dir = r < 0 ? "landward (eroding)" : "seaward (growing)";
    return "<b>" + fmt(r) + " m per year " + dir + "</b>, about " + Math.round(Math.abs(r) * 10) + " m per decade";
  }

  function nearPlace(km) {
    var p = data.places.slice().sort(function (a, b) { return Math.abs(a.km - km) - Math.abs(b.km - km); });
    if (Math.abs(p[0].km - km) < 2) return "Near " + p[0].name;
    var south = null, north = null;
    data.places.forEach(function (q) {
      if (q.km <= km && (!south || q.km > south.km)) south = q;
      if (q.km > km && (!north || q.km < north.km)) north = q;
    });
    if (south && north) return "Between " + south.name + " and " + north.name;
    return (north ? "South of " + north.name : "North of " + south.name);
  }

  // ---- controls --------------------------------------------------------------------------------
  function buildControls() {
    var box = document.getElementById("shoremap-windows");
    data.windows.forEach(function (w, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = i === 0 ? "Whole record (" + w.start + "–" + w.end + ")" : w.label;
      if (i === 0) b.className = "on";
      b.addEventListener("click", function () { setWindow(i); });
      box.appendChild(b);
    });
    document.querySelectorAll("#shoremap-basemaps button").forEach(function (b) {
      b.addEventListener("click", function () { setBase(b.getAttribute("data-base")); });
    });
    document.querySelectorAll("#shoremap-modes button").forEach(function (b) {
      b.addEventListener("click", function () { setMode(b.getAttribute("data-mode")); });
    });
    document.getElementById("shoremap-year").addEventListener("input", function (e) { stop(); setYear(+e.target.value); });
    document.getElementById("shoremap-play").addEventListener("click", function () { if (timer) stop(); else play(); });
    var end = new Date(data.record_end + "T00:00:00");
    document.querySelectorAll(".shoremap-end").forEach(function (s) {
      s.textContent = end.toLocaleString("en-US", { month: "long", year: "numeric" });
    });
  }

  function buildLegend() {
    var el = document.getElementById("shoremap-legend");
    if (!el) return;
    var yr = mode === "years", labels = yr ? LABELS_M : LABELS;
    var html = '<div class="hat-legend-title">' + (yr ? "Shoreline position, metres from its 1984–86 average" : "Shoreline change, metres per year") +
      '</div><div class="hat-legend-rows">';
    html += '<div class="hat-legend-col"><span class="hat-legend-head">' + (yr ? "Landward (eroded)" : "Moving landward (eroding)") + "</span>";
    for (var i = 0; i < 4; i++) html += row(i);
    html += '</div><div class="hat-legend-col"><span class="hat-legend-head">' + (yr ? "Seaward (grown)" : "Moving seaward (growing)") + "</span>";
    for (var j = 8; j > 4; j--) html += row(j);
    html += "</div></div>" + '<div class="hat-legend-mid">' + swatch(4) + " Little change: " + labels[4] + "</div>";
    html += '<div class="hat-legend-mid"><span class="hat-key-road"></span> NC-12 &nbsp; <span class="hat-key-groin"></span> Buxton groins</div>';
    el.innerHTML = html;
    function swatch(k) { return '<span class="hat-swatch" style="background:' + COLORS[k] + '"></span>'; }
    function row(k) { return '<div class="hat-legend-row">' + swatch(k) + labels[k] + "</div>"; }
  }

  // ---- map -------------------------------------------------------------------------------------
  function buildMap() {
    map = L.map("shoremap-map", { scrollWheelZoom: false, zoomSnap: 0.5, preferCanvas: true });
    // USGS National Map imagery underneath fills the gaps in the NC OneMap cache at island scale
    bases.aerial = L.layerGroup([
      L.tileLayer("https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 16, attribution: "USGS The National Map"
      }),
      L.tileLayer("https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_Latest_cached/ImageServer/tile/{z}/{y}/{x}", {
        minZoom: 12, maxZoom: 19, attribution: "Imagery: NC OneMap / NC Center for Geographic Information and Analysis"
      })
    ]);
    bases.plain = L.layerGroup([
      L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 16, attribution: "Tiles &copy; Esri &mdash; Esri, HERE, Garmin, &copy; OpenStreetMap contributors"
      }),
      L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}", { maxZoom: 16 })
    ]);
    bases.aerial.addTo(map);

    var renderer = L.canvas({ tolerance: 6 });
    L.polyline(data.nc12.map(function (p) { return [p[1], p[0]]; }), {
      color: "#ffd23f", weight: 2.5, opacity: 0.95, interactive: false, renderer: renderer
    }).addTo(map);

    data.transects.forEach(function (t, k) {
      var ll = t.line.map(function (p) { return [p[1], p[0]]; });
      casing.push(L.polyline(ll, { color: INK, weight: 6, opacity: 0.55, interactive: false, renderer: renderer }).addTo(map));
      var line = L.polyline(ll, { color: color(t.r[win]), weight: 4, opacity: 1, renderer: renderer }).addTo(map);
      line.on("mouseover", function () { line.setStyle({ weight: 7 }); });
      line.on("mouseout", function () { line.setStyle({ weight: weight() }); });
      line.on("click", function () { select(k); });
      line.bindTooltip(function () { return tooltip(k); }, { sticky: true, direction: "top", className: "hat-tip" });
      lines.push(line);
    });

    data.places.forEach(function (p) {
      L.marker(p.ll, { icon: L.divIcon({ className: "hat-place", html: "<span>" + p.name + "</span>", iconSize: null }), interactive: false }).addTo(map);
    });
    L.circleMarker(data.groin.ll, { radius: 6, color: "#fff", weight: 2, fillColor: "#d7191c", fillOpacity: 1 })
      .bindTooltip("Buxton groins", { direction: "left", className: "hat-tip" }).addTo(map);

    map.fitBounds(L.latLngBounds(lines.map(function (l) { return l.getBounds(); })), { padding: [20, 20] });
    map.on("zoomend", setCasing);
    setCasing();
  }

  // Dark outlines help single lines read on the photo up close, but turn the whole ribbon dark at island scale
  function setCasing() {
    if (!map) return;
    var on = map.getZoom() >= 13;
    casing.forEach(function (c, k) {
      var km = data.transects[k].km, lit = reachKm && km >= reachKm[0] && km <= reachKm[1];
      c.setStyle(lit ? { color: "#fff", weight: 11, opacity: 1 } : { color: INK, weight: 6, opacity: on ? 0.55 : 0 });
    });
  }

  // A timeline event's stretch of beach: white halo on the map and a teal band on the profile
  function setReach(detail) {
    reachKm = detail ? detail.km : null;
    setCasing();
    if (profileChart) {
      profileChart.options.plugins.hatBands.bands = profileBands();
      profileChart.update();
    }
  }

  function tooltip(k) {
    var t = data.transects[k], r = value(k), what;
    if (mode === "years") what = r === null ? "no shorelines this year" : years.years[yi] + ": " + fmt(r, 0) + " m " + (r < 0 ? "landward" : "seaward") + " of 1984–86";
    else what = r === null ? "no rate" : (r < 0 ? "−" : "+") + fmt(r, 2) + " m per year";
    return "<b>" + nearPlace(t.km) + "</b><br>" + what + "<br><span class='hat-tip-hint'>click for details</span>";
  }

  function setBase(name) {
    Object.keys(bases).forEach(function (n) { if (map.hasLayer(bases[n])) map.removeLayer(bases[n]); });
    bases[name].addTo(map);
    document.querySelectorAll("#shoremap-basemaps button").forEach(function (b) {
      b.classList.toggle("on", b.getAttribute("data-base") === name);
    });
  }

  function setWindow(i) {
    win = i;
    document.querySelectorAll("#shoremap-windows button").forEach(function (b, j) { b.classList.toggle("on", j === i); });
    recolour();
    updateProfile();
    if (selected !== null) select(selected, true);
  }

  function recolour() { lines.forEach(function (l, k) { l.setStyle({ color: color(value(k)), weight: weight() }); }); }

  // ---- year-by-year mode -----------------------------------------------------------------------
  function setMode(m) {
    if (m === mode) return;
    if (m === "years" && !years) {
      fetch(BASE + "shoreline_years.json").then(function (r) { return r.json(); }).then(function (d) {
        years = d;
        yi = 0;
        years.lo = Infinity;
        years.hi = -Infinity;
        d.v.forEach(function (row) { row.forEach(function (x) { if (x !== null) { years.lo = Math.min(years.lo, x); years.hi = Math.max(years.hi, x); } }); });
        buildPlayer();
        setMode("years");
      });
      return;
    }
    stop();
    mode = m;
    document.querySelectorAll("#shoremap-modes button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-mode") === m); });
    document.getElementById("shoremap-windows").hidden = m === "years";
    document.getElementById("shoremap-player").hidden = m !== "years";
    document.querySelectorAll(".shoremap-cap-rates").forEach(function (c) { c.hidden = m === "years"; });
    document.querySelectorAll(".shoremap-cap-years").forEach(function (c) { c.hidden = m !== "years"; });
    buildLegend();
    if (m === "years") setYear(yi);
    else { recolour(); updateProfile(); }
  }

  // Ticks under the play bar: fill years (gold) and the big named storms, from the timeline data
  function buildPlayer() {
    var range = document.getElementById("shoremap-year"), n = years.years.length;
    range.max = n - 1;
    var y0 = years.years[0], span = years.years[n - 1] - y0;
    var marks = [];
    data.nourishments.forEach(function (f) { f.years.forEach(function (y) { marks.push({ y: y, t: f.name + " fill", fill: true }); }); });
    var lastW = 0;
    window.addEventListener("resize", function () {
      var w = document.getElementById("shoremap-ticks").clientWidth;
      if (w && w !== lastW) { lastW = w; draw(); }
    });
    fetch(BASE + "timeline.json").then(function (r) { return r.json(); }).then(function (d) {
      var best = {};
      d.storms.forEach(function (s) { if (s.name && s.type === "tropical" && s.wl >= 3.5 && (!best[s.name] || s.wl > best[s.name].wl)) best[s.name] = s; });
      Object.keys(best).forEach(function (k) { marks.push({ y: Math.floor(best[k].y), t: k.replace(/ [0-9]{4}$/, ""), fill: false }); });
      draw();
    }, draw);
    function draw() {
      // one label per year and kind (two fills in 2022 share one), then rows so neighbours do not overlap
      var merged = {};
      marks.filter(function (m) { return m.y >= y0 && m.y <= y0 + span; }).forEach(function (m) {
        var key = m.y + (m.fill ? "f" : "s");
        if (merged[key]) merged[key].names.push(m.t.replace(" fill", ""));
        else merged[key] = { y: m.y, fill: m.fill, names: [m.t.replace(" fill", "")] };
      });
      var list = Object.keys(merged).map(function (k) { return merged[k]; }).sort(function (a, b) { return a.y - b.y; });
      // rows by measured width: a label takes about 6.5 px a character on the track's real width; past MAX_ROWS a
      // mark keeps its tick and shows its name on hover only (narrow screens)
      var box = document.getElementById("shoremap-ticks"), MAX_ROWS = 3, PX_PER_CHAR = 6.5;
      var yearsPerPx = span / Math.max(box.clientWidth, 1);
      var rowEnd = [];
      box.innerHTML = list.map(function (m) {
        var text = m.names.join(" + ") + (m.fill ? " fill" : ""), row = 0;
        var w = (text.length * PX_PER_CHAR + 6) * yearsPerPx;
        var flip = m.y + w > y0 + span;                  // would run off the right end: sit on the tick's left
        var start = flip ? m.y - w : m.y - 2 * yearsPerPx, end = flip ? m.y + 2 * yearsPerPx : m.y + w;
        while (rowEnd[row] !== undefined && rowEnd[row] > start) row++;
        var shown = row < MAX_ROWS;
        if (shown) rowEnd[row] = end;
        return '<span class="' + (m.fill ? "fill" : "storm") + (flip ? " flip" : "") + '" style="left:' + ((m.y - y0) / span * 100) + "%;--row:" + (shown ? row : 0) +
          '" title="' + m.y + ": " + text + '"><i></i>' + (shown ? "<b>" + text + "</b>" : "") + "</span>";
      }).join("");
      rowEnd.length = Math.min(rowEnd.length, MAX_ROWS);
      document.getElementById("shoremap-ticks").style.setProperty("--rows", rowEnd.length);
    }
  }

  function setYear(i) {
    yi = Math.max(0, Math.min(years.years.length - 1, i));
    document.getElementById("shoremap-year").value = yi;
    document.getElementById("shoremap-yearlabel").textContent = years.years[yi];
    recolour();
    updateProfile();
  }

  function play() {
    if (yi >= years.years.length - 1) setYear(0);
    var btn = document.getElementById("shoremap-play");
    btn.innerHTML = "&#10073;&#10073;";
    btn.setAttribute("aria-label", "Pause");
    timer = setInterval(function () {
      if (yi >= years.years.length - 1) return stop();
      setYear(yi + 1);
    }, FRAME_MS);
  }

  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
    var btn = document.getElementById("shoremap-play");
    btn.innerHTML = "&#9654;";
    btn.setAttribute("aria-label", "Play");
  }

  // ---- selection: detail text and time series --------------------------------------------------
  function select(k, keepView) {
    selected = k;
    if (history.replaceState) history.replaceState(null, "", "#t=" + data.transects[k].id);
    var t = data.transects[k];
    if (map) {
      if (highlight) map.removeLayer(highlight);
      highlight = L.polyline(t.line.map(function (p) { return [p[1], p[0]]; }), { color: "#fff", weight: 10, opacity: 0.9, interactive: false }).addTo(map);
      lines[k].bringToFront();
      if (!keepView && !map.getBounds().contains(highlight.getBounds())) map.panTo(highlight.getBounds().getCenter());
    }

    var rows = data.windows.map(function (w, i) {
      var label = i === 0 ? "Whole record" : w.label;
      return "<tr" + (i === win ? ' class="on"' : "") + "><th>" + label + "</th><td>" + describe(t.r[i], t.u[i]) + "</td></tr>";
    }).join("");
    var fills = data.nourishments.filter(function (n) { return t.km >= n.km[0] && t.km < n.km[1]; });
    document.getElementById("shoremap-detail").innerHTML =
      "<h4>" + nearPlace(t.km) + "</h4>" +
      '<p class="hat-detail-sub">' + t.km.toFixed(1) + " km north of Cape Point</p>" +
      '<table class="hat-detail-table">' + rows + "</table>" +
      (fills.length ? '<p class="hat-detail-note">This beach was nourished in ' + [].concat.apply([], fills.map(function (n) { return n.years; })).join(" and ") + ".</p>" : "");
    updateProfile();
    loadSeries(t).then(function (s) { if (selected === k) drawSeries(t, s, fills); });
  }

  function loadSeries(t) {
    var key = "d" + ("00" + t.d).slice(-3);
    if (!cache[key]) cache[key] = fetch(BASE + "timeseries/" + key + ".json").then(function (r) { return r.json(); });
    return cache[key].then(function (d) { return d[t.id]; });
  }

  // Least-squares line through the window's points, drawn over the window only
  function fitLine(pts, w) {
    var xs = [], ys = [];
    pts.forEach(function (p) { if (Math.floor(p[0]) >= w.start && Math.floor(p[0]) <= w.end) { xs.push(p[0]); ys.push(p[1]); } });
    if (xs.length < 3) return [];
    var mx = xs.reduce(function (a, b) { return a + b; }) / xs.length, my = ys.reduce(function (a, b) { return a + b; }) / ys.length;
    var sxy = 0, sxx = 0;
    for (var i = 0; i < xs.length; i++) { sxy += (xs[i] - mx) * (ys[i] - my); sxx += (xs[i] - mx) * (xs[i] - mx); }
    var b = sxy / sxx, x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
    return [{ x: x0, y: my + b * (x0 - mx) }, { x: x1, y: my + b * (x1 - mx) }];
  }

  // Shaded spans behind a chart: {from, to, fill, label, ink} in x units
  var bandsPlugin = {
    id: "hatBands",
    beforeDatasetsDraw: function (chart, args, opts) {
      var ctx = chart.ctx, x = chart.scales.x, area = chart.chartArea;
      (opts.bands || []).forEach(function (b) {
        var a = Math.max(x.getPixelForValue(b.from), area.left), z = Math.min(x.getPixelForValue(b.to), area.right);
        if (z <= a) return;
        ctx.save();
        ctx.fillStyle = b.fill;
        ctx.fillRect(a, area.top, z - a, area.bottom - area.top);
        if (b.label) {
          ctx.fillStyle = b.ink || MUTED;
          ctx.font = "12px Roboto, sans-serif";
          ctx.fillText(b.label, a + 3, b.labelTop ? area.top + 12 : area.bottom - 5);
        }
        ctx.restore();
      });
    }
  };

  function drawSeries(t, s, fills) {
    var wrap = document.querySelector(".hat-ts-wrap");
    wrap.hidden = false;
    var w = data.windows[win];
    var pts = s.pts.map(function (p) { return { x: p[0], y: p[1] }; });
    var bands = [{ from: w.start, to: w.end + 1, fill: "rgba(47, 127, 147, 0.08)" }];
    fills.forEach(function (n) { n.years.forEach(function (y) { bands.push({ from: y, to: y + 1, fill: FILL_BG, label: "fill", ink: "#8a5d06", labelTop: true }); }); });
    var cfg = {
      type: "scatter",
      data: {
        datasets: [
          { label: "Satellite shoreline", data: pts, pointRadius: 1.6, pointHoverRadius: 4, backgroundColor: "rgba(80, 88, 92, 0.45)", borderWidth: 0 },
          { label: "Trend " + (win === 0 ? "over the whole record" : w.label), type: "line", data: fitLine(s.pts, w), borderColor: INK, borderWidth: 2, pointRadius: 0 }
        ]
      },
      options: {
        animation: false, maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          hatBands: { bands: bands },
          tooltip: { callbacks: { label: function (c) { return c.datasetIndex === 0 ? Math.floor(c.raw.x) + ": " + (c.raw.y >= 0 ? "+" : "−") + fmt(c.raw.y) + " m" : null; } } },
          title: { display: true, text: "Shoreline position, metres seaward (+) of its " + s.ref_year + " average", color: INK, font: { weight: "normal", size: 13 }, align: "start" }
        },
        scales: {
          x: { type: "linear", min: 1984, max: 2026, ticks: { stepSize: 5, color: MUTED, callback: function (v) { return v; } }, grid: { color: GRID } },
          y: { ticks: { color: MUTED }, grid: { color: function (c) { return c.tick.value === 0 ? "#9aa0a3" : GRID; } } }
        }
      },
      plugins: [bandsPlugin]
    };
    if (tsChart) tsChart.destroy();
    tsChart = new Chart(document.getElementById("shoremap-ts"), cfg);
  }

  // ---- profile along the island ----------------------------------------------------------------
  function buildProfile() {
    var cfg = {
      type: "scatter",
      data: { datasets: [
        { label: "Survey line", data: [], pointRadius: 2.5, pointHoverRadius: 5, borderWidth: 0 },
        { label: "Smoothed", type: "line", data: [], borderColor: INK, borderWidth: 2, pointRadius: 0, spanGaps: false },
        { label: "Selected", data: [], pointRadius: 7, backgroundColor: "rgba(0,0,0,0)", borderColor: TEAL, borderWidth: 2.5 }
      ] },
      options: {
        animation: false, maintainAspectRatio: false,
        onClick: function (e, els) { var el = els.filter(function (x) { return x.datasetIndex === 0; })[0]; if (el) select(el.index); },
        plugins: {
          legend: { display: false },
          hatBands: { bands: profileBands() },
          tooltip: { filter: function (c) { return c.datasetIndex === 0; }, callbacks: { label: function (c) {
            var t = data.transects[c.dataIndex];
            return nearPlace(t.km) + ": " + (c.raw.y >= 0 ? "+" : "−") + (mode === "years" ? fmt(c.raw.y, 0) + " m" : fmt(c.raw.y, 2) + " m/yr");
          } } }
        },
        scales: {
          x: { type: "linear", min: 0, max: Math.ceil(data.transects[data.transects.length - 1].km), title: { display: true, text: "km north of Cape Point", color: MUTED },
               ticks: { color: MUTED, stepSize: 5 }, grid: { color: GRID } },
          y: { title: { display: true, text: "m per year (+ seaward, − landward)", color: MUTED }, ticks: { color: MUTED },
               grid: { color: function (c) { return c.tick.value === 0 ? "#9aa0a3" : GRID; } } }
        }
      },
      plugins: [bandsPlugin, placesPlugin]
    };
    profileChart = new Chart(document.getElementById("shoremap-profile"), cfg);
    updateProfile();
  }

  function profileBands() {
    var b = data.nourishments.map(function (n) { return { from: n.km[0], to: n.km[1], fill: FILL_BG, label: n.name + " " + n.years.join(", "), ink: "#8a5d06" }; });
    if (reachKm) b.push({ from: reachKm[0], to: reachKm[1], fill: "rgba(47, 127, 147, 0.22)" });
    return b;
  }

  // Village names along the top of the profile; these drop a row to clear their neighbours
  var LOWER = { Buxton: true, Waves: true };
  var placesPlugin = {
    id: "hatPlaces",
    afterDatasetsDraw: function (chart) {
      var ctx = chart.ctx, x = chart.scales.x, area = chart.chartArea;
      ctx.save();
      ctx.font = "12px Roboto, sans-serif";
      ctx.textAlign = "center";
      data.places.forEach(function (p) {
        var px = x.getPixelForValue(p.km);
        ctx.strokeStyle = "rgba(107, 115, 120, 0.35)";
        ctx.beginPath(); ctx.moveTo(px, area.top + 18 + (LOWER[p.name] ? 13 : 0)); ctx.lineTo(px, area.bottom); ctx.stroke();
        ctx.fillStyle = INK;
        ctx.textAlign = p.km < 1.5 ? "left" : "center";
        ctx.fillText(p.name, p.km < 1.5 ? px + 3 : px, area.top + 14 + (LOWER[p.name] ? 13 : 0));
      });
      var g = x.getPixelForValue(data.groin.km);
      ctx.fillStyle = "#d7191c";
      ctx.fillRect(g - 1.5, area.bottom - 14, 3, 14);
      ctx.restore();
    }
  };

  function updateProfile() {
    if (!profileChart) return;
    var ds = profileChart.data.datasets, yr = mode === "years", y = profileChart.options.scales.y;
    ds[0].data = data.transects.map(function (t, k) { return { x: t.km, y: value(k) }; });
    ds[0].backgroundColor = data.transects.map(function (t, k) { return color(value(k)); });
    ds[0].borderColor = "rgba(26,26,26,0.35)";
    ds[0].borderWidth = 0.5;
    // the yearly values are already smoothed, so the line is the same values; rates draw their own smoothed line
    ds[1].data = data.transects.map(function (t, k) { return { x: t.km, y: yr ? value(k) : t.s[win] }; });
    ds[2].data = selected === null ? [] : [{ x: data.transects[selected].km, y: value(selected) }];
    // fixed y range while playing, so motion reads as change rather than rescaling
    y.min = yr ? Math.floor(years.lo / 25) * 25 : undefined;
    y.max = yr ? Math.ceil(years.hi / 25) * 25 : undefined;
    y.title.text = yr ? "metres from the 1984–86 average (+ seaward)" : "m per year (+ seaward, − landward)";
    profileChart.update();
  }

  // ---- table view (domain means) ---------------------------------------------------------------
  function buildTable() {
    if (!document.getElementById("shoremap-table")) return;
    var groups = {};
    data.transects.forEach(function (t) { (groups[t.d] = groups[t.d] || []).push(t); });
    var head = "<thead><tr><th>km north of Cape Point</th><th>Place</th>" +
      data.windows.map(function (w, i) { return "<th>" + (i === 0 ? "Whole record" : w.label) + " (m/yr)</th>"; }).join("") + "</tr></thead>";
    var body = Object.keys(groups).sort(function (a, b) { return a - b; }).map(function (d) {
      var ts = groups[d], km = ts.reduce(function (a, t) { return a + t.km; }, 0) / ts.length;
      var cells = data.windows.map(function (w, i) {
        var v = ts.map(function (t) { return t.r[i]; }).filter(function (r) { return r !== null; });
        if (!v.length) return "<td>–</td>";
        var m = v.reduce(function (a, b) { return a + b; }) / v.length;
        return "<td>" + (m >= 0 ? "+" : "−") + fmt(m, 2) + "</td>";
      }).join("");
      return "<tr><td>" + (+d - 1) * 0.5 + "–" + (+d) * 0.5 + "</td><td>" + nearPlace(km) + "</td>" + cells + "</tr>";
    }).join("");
    document.getElementById("shoremap-table").innerHTML = head + "<tbody>" + body + "</tbody>";
  }

  function start() {
    if ((HAS_MAP && typeof L === "undefined") || typeof Chart === "undefined") return setTimeout(start, 100);
    fetch(BASE + "shoreline_rates.json").then(function (r) { return r.json(); }).then(function (d) {
      data = d;
      buildControls();
      buildLegend();
      if (HAS_MAP) buildMap();
      if (HAS_PROFILE) buildProfile();
      buildTable();
      window.addEventListener("hat:reach", function (e) { setReach(e.detail); });
      var m = /t=([\w]+)/.exec(location.hash);
      var k = m ? data.transects.findIndex(function (t) { return t.id === m[1]; }) : -1;
      if (k >= 0) select(k);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
