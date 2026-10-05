// Nourishment explorer on /hatteras/management/ (markup in _includes/hatteras/nourishment_explorer.liquid; data from
// tools/hatteras_nourishment_data.py). For the chosen fill: where it is on the island, a headline, one bar per year
// after the fill (how far the shoreline sat seaward of where it was the year before, compared with the rest of the
// island) and a card. The whole record for the stretch, as lines, sits in a Go deeper box and is drawn when opened.
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var INK = "#1a1a1a", MUTED = "#6b7378", GRID = "#e6e9eb", REST = "#9aa0a3", FILL = "#c8880f", FILL_BG = "rgba(246, 227, 184, 0.7)";
  var TEAL = "#2f7f93";

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { if (attrs[k] !== null) e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }
  function text(parent, x, y, s, attrs) { var t = el("text", Object.assign({ x: x, y: y }, attrs || {}), parent); t.textContent = s; return t; }
  function signed(v, d) { return (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(d === undefined ? 0 : d); }

  function Explorer(root) {
    this.root = root;
    this.chart = root.querySelector(".hat-nx-chart");
    this.bars = root.querySelector(".hat-nx-bars");
    this.more = root.querySelector(".hat-nx-more");
    this.strip = root.querySelector(".hat-nx-strip");
    this.tip = root.querySelector(".hat-tl-tip");
    this.k = 0;
    this.view = "relative";
    var self = this;
    fetch(root.getAttribute("data-src")).then(function (r) { return r.json(); }).then(function (d) {
      self.data = d;
      // one entry per fill, in date order, each pointing at its stretch
      self.fills = [];
      d.stretches.forEach(function (st, k) { st.fills.forEach(function (f) { self.fills.push({ k: k, f: f }); }); });
      self.fills.sort(function (a, b) { return a.f.year - b.f.year || a.k - b.k; });
      self.controls();
      self.draw();
      // before-and-after photos, one pair per fill (tools/hatteras_nourishment_photos.py); the panel stays hidden without them
      fetch(root.getAttribute("data-outline")).then(function (r) { return r.ok ? r.json() : null; })
        .then(function (o) { self.outline = o; self.drawStrip(); }).catch(function () {});
      fetch(root.getAttribute("data-photos")).then(function (r) { return r.ok ? r.json() : {}; })
        .then(function (p) { self.photos = p; self.drawPhoto(); }).catch(function () {});
      var w = self.chart.clientWidth;
      window.addEventListener("resize", function () { if (self.bars.clientWidth !== w) { w = self.bars.clientWidth; self.draw(); } });
      self.more.addEventListener("toggle", function () { if (self.more.open) { self.drawBars(); self.drawChart(); } });
    });
  }

  Explorer.prototype.controls = function () {
    var self = this, seg = this.root.querySelector(".hat-nx-stretches");
    this.fi = 0;
    this.fills.forEach(function (x, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = self.data.stretches[x.k].name + " " + x.f.year;
      if (i === 0) b.className = "on";
      b.addEventListener("click", function () {
        self.fi = i;
        self.k = x.k;
        seg.querySelectorAll("button").forEach(function (o, j) { o.classList.toggle("on", j === i); });
        self.draw();
      });
      seg.appendChild(b);
    });
    this.root.querySelectorAll(".hat-nx-views button").forEach(function (b) {
      b.addEventListener("click", function () {
        self.view = b.getAttribute("data-view");
        self.root.querySelectorAll(".hat-nx-views button").forEach(function (o) { o.classList.toggle("on", o === b); });
        self.root.querySelectorAll("[data-for-view]").forEach(function (c) { c.hidden = c.getAttribute("data-for-view") !== self.view; });
        self.drawChart();
      });
    });
  };

  Explorer.prototype.draw = function () {
    this.k = this.fills[this.fi].k;
    var name = this.data.stretches[this.k].name;
    this.root.querySelectorAll(".hat-nx-stretch-name").forEach(function (n) { n.textContent = name; });
    this.drawStrip();
    this.drawBars();
    this.drawCards();
    this.drawPhoto();
    if (this.more.open) this.drawChart();
  };

  // Headline and card numbers on the placement dates (tools/hatteras_nourishment_photos.py), when they are loaded
  Explorer.prototype.numbers = function () {
    var f = this.fills[this.fi].f, s = this.data.stretches[this.k];
    var p = this.photos && this.photos[s.name + " " + f.year];
    return p && p.jump_m !== undefined ? { jump: p.jump_m, left: p.left_m, year: p.left_year, refill: p.left_after_refill } :
      { jump: f.step_m, left: f.since_before_m[String(this.data.last_year)], year: this.data.last_year, refill: false };
  };

  Explorer.prototype.drawHeadline = function () {
    var f = this.fills[this.fi].f, s = this.data.stretches[this.k], n = this.numbers();
    this.root.querySelector(".hat-nx-headline").innerHTML =
      "The " + f.year + " fill at " + s.name + " moved the shoreline <b>" + Math.round(n.jump) + " m seaward</b> compared with the rest of the island. " +
      (n.left >= 1 ? "In " + n.year + ", <b>" + Math.round(n.left) + " m</b> of it was still there" + (n.refill ? ", with the later refill's sand." : ".") :
        "By " + n.year + ", it was gone.");
  };

  Explorer.prototype.drawPhoto = function () {
    this.drawHeadline();
    this.drawCards();
    var fig = this.root.querySelector(".hat-nx-photo"), f = this.fills[this.fi].f, name = this.data.stretches[this.k].name;
    var p = this.photos && this.photos[name + " " + f.year];
    fig.hidden = !p;
    if (!p) return;
    var img = fig.querySelector("img");
    var assets = this.root.getAttribute("data-assets") || "/assets/hatteras/";
    var asset = function (path) { return path.replace(/^\/assets\/hatteras\//, assets); };
    img.src = asset(p.src);
    img.alt = "Aerial photos of the same stretch of beach at " + name + ", before (" + p.before + ") and after (" + p.after +
      ") the " + f.year + " fill, with the satellite shoreline at the time of each photo drawn on them";
    fig.querySelector("figcaption").innerHTML = "The same 300 m of beach at " + name + ", photographed from the air on " + p.before +
      " and on " + p.after + ", before and after the " + f.year + " fill (sand placed " + p.placed + "). Each line is the " +
      "satellite shoreline at the time of its photo, the average of the three satellite images nearest the flight. The view " +
      "is the part of the nourished stretch where the shoreline moved furthest between the two photos, so the new sand shows " +
      "clearly. The gap between the lines includes everything that changed between the two dates, not only the fill; the " +
      "numbers above compare the fill with the rest of the island. Satellite shorelines mark mean sea level, so they sit " +
      "a little landward of the wet edge in a photo taken at low tide. Photos: USDA National Agriculture Imagery Program " +
      "(public domain), via Microsoft Planetary Computer. Shorelines: CoastSat.";
    var refill = /refill/.test(p.later_photos.join(" ") + "") ||
      this.data.stretches[this.k].fills.some(function (o) { return o.year > f.year; });
    var tt = this.root.querySelector(".hat-nx-time");
    tt.hidden = !p.years_later;
    if (p.years_later) {
      tt.querySelector("img").src = asset(p.years_later);
      tt.querySelector("img").alt = "Aerial photos of the same beach at " + name + " in the years after the " + f.year +
        " fill (" + p.later_photos.join(", ") + "), each with the satellite shoreline at the time of the photo and the shoreline before the fill";
      tt.querySelector("figcaption").innerHTML = "The same 300 m of beach in every later aerial photo, " +
        p.later_photos.join(", ").replace(/, ([^,]*)$/, " and $1") + ". The solid line is the satellite shoreline at the time " +
        "of each photo, and the dashed line is the shoreline before the fill: as the added beach wears away, the solid line " +
        "moves back toward the dashed one." + (refill ? " Photos marked as after a refill include that later fill's sand too." : "") +
        " Photos: USDA National Agriculture Imagery Program to 2022, NC OneMap / NC Center for Geographic Information and " +
        "Analysis in 2024. Shorelines: CoastSat.";
    }
  };

  // The simple view: a headline and one bar per year after the fill
  Explorer.prototype.drawBars = function () {
    var d = this.data, s = d.stretches[this.k], f = this.fills[this.fi].f;
    var ys = Object.keys(f.since_before_m).map(Number).sort(), vals = ys.map(function (y) { return f.since_before_m[y]; });
    this.drawHeadline();
    var W = Math.max(this.bars.clientWidth, 300), small = W < 640, H = small ? 240 : 270, top = 28, bottom = 44, lft = small ? 34 : 50, right = 10;
    var hi = Math.max(10, Math.ceil(Math.max.apply(null, vals.concat([0])) / 10) * 10);
    var lo = Math.min(0, Math.floor(Math.min.apply(null, vals) / 10) * 10);
    var slot = (W - lft - right) / Math.max(ys.length, 6), bw = Math.min(slot * 0.62, 70);
    var X = function (i) { return lft + slot * (i + 0.5); };
    var Y = function (v) { return top + (hi - v) / (hi - lo) * (H - top - bottom); };
    this.bars.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H, role: "img",
      "aria-label": "Bars: metres the shoreline sat seaward of where it was before the fill, each year after it" }, this.bars);
    for (var v = lo; v <= hi; v += 10) {
      el("line", { x1: lft, x2: W - right, y1: Y(v), y2: Y(v), stroke: v === 0 ? INK : GRID }, svg);
      text(svg, lft - 6, Y(v) + 4, signed(v), { "text-anchor": "end", fill: MUTED, "font-size": 12 });
    }
    // later fills on the same stretch add sand too: mark the bars they affect
    var later = s.fills.filter(function (o) { return o.year > f.year; });
    ys.forEach(function (y, i) {
      var v = vals[i], after = later.some(function (o) { return y >= o.year; });
      el("rect", { x: X(i) - bw / 2, y: Math.min(Y(v), Y(0)), width: bw, height: Math.max(Math.abs(Y(v) - Y(0)), 1),
        fill: after ? "rgba(200, 136, 15, 0.45)" : FILL }, svg);
      text(svg, X(i), v >= 0 ? Y(v) - 6 : Y(v) + 15, signed(v) + " m", { "text-anchor": "middle", fill: INK, "font-size": small ? 11 : 12.5, "font-weight": 600 });
      text(svg, X(i), H - bottom + 17, y, { "text-anchor": "middle", fill: MUTED, "font-size": 12 });
      if (i === 0) text(svg, X(i), H - bottom + 32, "year after", { "text-anchor": "middle", fill: MUTED, "font-size": 11 });
    });
    later.forEach(function (o) {
      var i = ys.indexOf(o.year);
      if (i < 0) return;
      var x = X(i) - slot / 2;
      el("line", { x1: x, x2: x, y1: top - 6, y2: H - bottom, stroke: INK, "stroke-dasharray": "4 3" }, svg);
      text(svg, x + 4, top - 10, o.year + " fill adds more sand", { fill: INK, "font-size": 11.5 });
    });
    if (!small) {
      var yl = text(svg, 0, 0, "metres seaward", { fill: MUTED, "font-size": 12, "text-anchor": "middle" });
      yl.setAttribute("transform", "translate(13," + (top + (H - top - bottom) / 2) + ") rotate(-90)");
    }
  };

  // Where the stretch is: the island from Cape Point to Oregon Inlet as a bar, villages above, the fills in gold
  Explorer.prototype.drawStrip = function () {
    var d = this.data, s = d.stretches[this.k], o = this.outline, W = Math.max(this.strip.clientWidth, 300), L = 8, R = 8, top = 34;
    var pxkm = (W - L - R) / d.island_km[1];
    var X = function (km) { return L + km * pxkm; };
    // the island turned so north runs right, ocean side down, at true scale (tools/hatteras_island_outline.py)
    var e0 = o ? o.east_m[0] : 0, h = o ? (o.east_m[1] - o.east_m[0]) / 1000 * pxkm : 8;
    var Y = function (east) { return top + (east - e0) / 1000 * pxkm; };
    var H = top + h + 18;
    this.strip.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H, role: "img",
      "aria-label": s.name + " stretch, " + s.km[0].toFixed(1) + " to " + s.km[1].toFixed(1) + " km north of Cape Point" }, this.strip);
    if (o) {
      o.rings.forEach(function (ring) {
        el("path", { d: "M" + ring.map(function (q) { return X(q[0]).toFixed(1) + "," + Y(q[1]).toFixed(1); }).join("L") + "Z",
          fill: "#e8dcb8", stroke: "#b9a67a", "stroke-width": 0.8 }, svg);
      });
    } else {
      el("rect", { x: L, y: top, width: W - L - R, height: 8, rx: 4, fill: "#e8dcb8" }, svg);
    }
    // the ocean shoreline every 250 m, from the outline tool
    var shore = function (km) {
      var sh = o.shore, n = Math.max(0, Math.min(sh.length - 1, Math.round(km * 4)));
      return sh[n][1];
    };
    d.stretches.forEach(function (st) {
      if (!o) {
        el("rect", { x: X(st.km[0]), y: top - 3, width: Math.max(X(st.km[1]) - X(st.km[0]), 3), height: 14, rx: 2,
          fill: st === s ? FILL : "rgba(200, 136, 15, 0.35)", stroke: st === s ? INK : "none", "stroke-width": 1 }, svg);
        return;
      }
      var pts = [];
      for (var k = st.km[0]; k <= st.km[1] + 1e-9; k += 0.25) pts.push(X(k).toFixed(1) + "," + (Y(shore(k)) + 3).toFixed(1));
      el("polyline", { points: pts.join(" "), fill: "none", stroke: st === s ? FILL : "rgba(200, 136, 15, 0.45)",
        "stroke-width": st === s ? 6 : 4, "stroke-linecap": "round" }, svg);
      if (st === s) el("polyline", { points: pts.join(" "), fill: "none", stroke: INK, "stroke-width": 0.8, "stroke-dasharray": "0" }, svg);
    });
    // village names alternate between two rows so close villages (Salvo, Waves, Rodanthe) do not collide
    d.places.forEach(function (p, i) {
      var row = i % 2, yb = o ? Y(shore(p.km)) - 2 : top;
      el("line", { x1: X(p.km), x2: X(p.km), y1: 12 + row * 12, y2: Math.max(yb, 14 + row * 12), stroke: MUTED, "stroke-width": 0.8 }, svg);
      text(svg, X(p.km), 9 + row * 12, p.name, { "text-anchor": p.km < 2 ? "start" : p.km > d.island_km[1] - 3 ? "end" : "middle",
        fill: INK, "font-size": 11.5, "paint-order": "stroke", stroke: "#fff", "stroke-width": 3 });
    });
    text(svg, W - R, H - 3, "Oregon Inlet", { fill: MUTED, "font-size": 10.5, "text-anchor": "end" });
    if (o) text(svg, L, H - 3, "Atlantic Ocean below, Pamlico Sound above; north is to the right", { fill: MUTED, "font-size": 10.5 });
  };

  Explorer.prototype.drawChart = function () {
    var self = this, d = this.data, s = d.stretches[this.k], rel = this.view === "relative";
    this.root.querySelectorAll(".hat-nx-stretch-name").forEach(function (n) { n.textContent = s.name; });
    var W = Math.max(this.chart.clientWidth, 320), small = W < 640;
    var left = small ? 38 : 58, right = 14, top = 46, H = small ? 320 : 380, bottom = 40;
    var y0 = s.years[0], y1 = d.last_year;
    var lines = rel ?
      [{ v: s.filled.map(function (f, i) { return f === null || s.rest[i] === null ? null : Math.round((f - s.rest[i]) * 10) / 10; }), color: INK, w: 2.6, name: s.name + " minus the rest of the island" }] :
      [{ v: s.rest, color: REST, w: 2, name: "Rest of the island" }, { v: s.filled, color: TEAL, w: 2.6, name: s.name + " (nourished stretch)" }];
    var all = [].concat.apply([], lines.map(function (l) { return l.v; })).filter(function (v) { return v !== null; });
    var lo = Math.floor(Math.min(0, Math.min.apply(null, all)) / 10) * 10, hi = Math.ceil(Math.max(0, Math.max.apply(null, all)) / 10) * 10;
    var X = function (y) { return left + (y - y0) / (y1 - y0) * (W - left - right); };
    var Y = function (v) { return top + (hi - v) / (hi - lo) * (H - top - bottom); };

    this.chart.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H }, this.chart);
    // fill years
    s.fills.forEach(function (f) {
      el("rect", { x: X(f.year - 0.5), y: top, width: X(f.year + 0.5) - X(f.year - 0.5), height: H - top - bottom, fill: FILL_BG }, svg);
      text(svg, X(f.year), top - 8, f.year + " fill", { "text-anchor": "middle", fill: "#8a5d06", "font-size": 11.5, "font-weight": 600 });
    });
    // grid, axes, ticks
    var step = (hi - lo) > 60 ? 20 : 10;
    for (var v = lo; v <= hi; v += step) {
      el("line", { x1: left, x2: W - right, y1: Y(v), y2: Y(v), stroke: v === 0 ? "#9aa0a3" : GRID }, svg);
      el("line", { x1: left - 4, x2: left, y1: Y(v), y2: Y(v), stroke: INK }, svg);
      text(svg, left - 7, Y(v) + 4, signed(v), { "text-anchor": "end", fill: MUTED, "font-size": 12 });
    }
    for (var y = Math.ceil(y0 / 5) * 5; y <= y1; y += 5) {
      el("line", { x1: X(y), x2: X(y), y1: H - bottom, y2: H - bottom + 4, stroke: INK }, svg);
      text(svg, X(y), H - bottom + 17, y, { "text-anchor": "middle", fill: MUTED, "font-size": 12 });
    }
    el("line", { x1: left, x2: left, y1: top, y2: H - bottom, stroke: INK }, svg);
    el("line", { x1: left, x2: W - right, y1: H - bottom, y2: H - bottom, stroke: INK }, svg);
    if (!small) {
      var yl = text(svg, 0, 0, rel ? "metres, stretch minus island (+ seaward)" : "metres from " + s.base_year + " (+ seaward)",
        { fill: MUTED, "font-size": 12, "text-anchor": "middle" });
      yl.setAttribute("transform", "translate(14," + (top + (H - top - bottom) / 2) + ") rotate(-90)");
    }
    // the baseline year: every line is zero here
    el("circle", { cx: X(s.base_year), cy: Y(0), r: 4, fill: "#fff", stroke: INK, "stroke-width": 1.5 }, svg);

    lines.forEach(function (l) {
      var pts = l.v.map(function (v, i) { return v === null ? null : X(s.years[i]).toFixed(1) + "," + Y(v).toFixed(1); }).filter(Boolean);
      el("polyline", { points: pts.join(" "), fill: "none", stroke: l.color, "stroke-width": l.w, "stroke-linejoin": "round" }, svg);
      l.v.forEach(function (v, i) { if (v !== null) el("circle", { cx: X(s.years[i]), cy: Y(v), r: 2.4, fill: l.color }, svg); });
    });

    // each fill's jump: from the year before to the year after, on the relative line
    if (rel) {
      var r = lines[0].v;
      s.fills.forEach(function (f) {
        var a = r[s.years.indexOf(f.year - 1)], b = r[s.years.indexOf(f.year + 1)], x = X(f.year + 1) + 8;
        if (a === null || b === null) return;
        el("path", { d: "M" + (x - 4) + "," + Y(a) + " h4 V" + Y(b) + " h-4", fill: "none", stroke: FILL, "stroke-width": 1.6 }, svg);
        text(svg, x + 5, (Y(a) + Y(b)) / 2 + 4, signed(f.step_m) + " m", { fill: "#8a5d06", "font-size": 12.5, "font-weight": 700,
          "paint-order": "stroke", stroke: "#fff", "stroke-width": 3 });
      });
    }

    // key, in the top margin and clear of the data
    var kx = left;
    lines.slice().reverse().forEach(function (l) {
      el("line", { x1: kx, x2: kx + 22, y1: 12, y2: 12, stroke: l.color, "stroke-width": l.w }, svg);
      var t = text(svg, kx + 28, 16, l.name, { fill: INK, "font-size": 12 });
      kx += 40 + t.getComputedTextLength();
    });

    // hover: the values in a year
    var cross = el("line", { y1: top, y2: H - bottom, stroke: INK, opacity: 0, "pointer-events": "none" }, svg);
    var hit = el("rect", { x: left, y: top, width: W - left - right, height: H - top - bottom, fill: "transparent" }, svg);
    hit.addEventListener("mousemove", function (e) {
      var b = hit.getBoundingClientRect(), yr = Math.round(y0 + (e.clientX - b.left) / b.width * (y1 - y0)), i = s.years.indexOf(yr);
      if (i < 0) return;
      cross.setAttribute("x1", X(yr)); cross.setAttribute("x2", X(yr)); cross.setAttribute("opacity", 0.3);
      var html = "<b>" + yr + "</b>" + lines.map(function (l) {
        return "<br><span style='color:" + l.color + "'>" + l.name + ": " + (l.v[i] === null ? "no data" : signed(l.v[i], 1) + " m") + "</span>";
      }).join("");
      var t = self.tip, box = self.root.querySelector(".hat-shoremap-inner").getBoundingClientRect();
      t.innerHTML = html;
      t.hidden = false;
      var tx = e.clientX - box.left + 14;
      if (tx + t.offsetWidth > box.width) tx = e.clientX - box.left - t.offsetWidth - 14;
      t.style.left = tx + "px";
      t.style.top = (e.clientY - box.top + 14) + "px";
    });
    hit.addEventListener("mouseleave", function () { cross.setAttribute("opacity", 0); self.tip.hidden = true; });
  };

  // One card per fill: what was placed, the jump, and what was left in the last full year
  Explorer.prototype.drawCards = function () {
    var d = this.data, s = d.stretches[this.k], km = s.length_m / 1000, n = this.numbers();
    this.root.querySelector(".hat-nx-cards").innerHTML = [this.fills[this.fi].f].map(function (f) {
      var left = n.left, pct = Math.round(left / n.jump * 100);
      return '<div class="hat-nx-card"><h4>' + s.name + " " + f.year + "</h4><dl>" +
        "<dt>Sand placed</dt><dd>" + (f.volume_cy / 1e6).toFixed(1) + " million cubic yards</dd>" +
        "<dt>Beach length</dt><dd>about " + km.toFixed(1) + " km (" + (km / 1.609).toFixed(1) + " miles)</dd>" +
        "<dt>Sand per metre of beach</dt><dd>about " + f.m3_per_m + " cubic metres</dd>" +
        "<dt>Jump after the fill</dt><dd><b>" + signed(n.jump) + " m</b> compared with the rest of the island</dd>" +
        "<dt>Left in " + n.year + "</dt><dd>" + signed(left) + " m" + (n.jump > 0 && left > 0 && !n.refill ? " (about " + pct + "% of the jump)" :
          n.refill ? " (with the later refill's sand)" : "") + "</dd>" +
        "</dl></div>";
    }).join("");
  };

  function start() { document.querySelectorAll(".hat-nx").forEach(function (r) { new Explorer(r); }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
