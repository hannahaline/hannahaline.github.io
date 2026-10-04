// Nourishment explorer on /hatteras/management/ (markup in _includes/hatteras/nourishment_explorer.liquid; data from
// tools/hatteras_nourishment_data.py). For the chosen stretch: a strip showing where it is on the island, the yearly
// shoreline on the stretch and on the rest of the island (or their difference), the fills marked, and a card per fill.
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
    this.strip = root.querySelector(".hat-nx-strip");
    this.tip = root.querySelector(".hat-tl-tip");
    this.k = 0;
    this.view = "relative";
    var self = this;
    fetch(root.getAttribute("data-src")).then(function (r) { return r.json(); }).then(function (d) {
      self.data = d;
      self.controls();
      self.draw();
      var w = self.chart.clientWidth;
      window.addEventListener("resize", function () { if (self.chart.clientWidth !== w) { w = self.chart.clientWidth; self.draw(); } });
    });
  }

  Explorer.prototype.controls = function () {
    var self = this, seg = this.root.querySelector(".hat-nx-stretches");
    this.data.stretches.forEach(function (s, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = s.name + " (" + s.fills.map(function (f) { return f.year; }).join(", ") + ")";
      if (i === 0) b.className = "on";
      b.addEventListener("click", function () {
        self.k = i;
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
        self.draw();
      });
    });
  };

  Explorer.prototype.draw = function () {
    this.drawStrip();
    this.drawChart();
    this.drawCards();
  };

  // Where the stretch is: the island from Cape Point to Oregon Inlet as a bar, villages above, the fills in gold
  Explorer.prototype.drawStrip = function () {
    var d = this.data, s = d.stretches[this.k], W = Math.max(this.strip.clientWidth, 300), H = 54, L = 8, R = 8;
    var X = function (km) { return L + km / d.island_km[1] * (W - L - R); };
    this.strip.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H, role: "img",
      "aria-label": s.name + " stretch, " + s.km[0].toFixed(1) + " to " + s.km[1].toFixed(1) + " km north of Cape Point" }, this.strip);
    el("rect", { x: L, y: 30, width: W - L - R, height: 8, rx: 4, fill: "#e8dcb8" }, svg);
    d.stretches.forEach(function (o) {
      el("rect", { x: X(o.km[0]), y: 27, width: Math.max(X(o.km[1]) - X(o.km[0]), 3), height: 14, rx: 2,
        fill: o === s ? FILL : "rgba(200, 136, 15, 0.35)", stroke: o === s ? INK : "none", "stroke-width": 1 }, svg);
    });
    // neighbouring names alternate between two rows so close villages (Salvo, Waves, Rodanthe) do not collide
    d.places.forEach(function (p, i) {
      var row = i % 2;
      el("line", { x1: X(p.km), x2: X(p.km), y1: 12 + row * 12, y2: 30, stroke: MUTED }, svg);
      text(svg, X(p.km), 9 + row * 12, p.name, { "text-anchor": p.km < 2 ? "start" : p.km > d.island_km[1] - 3 ? "end" : "middle",
        fill: INK, "font-size": 11.5, "paint-order": "stroke", stroke: "#fff", "stroke-width": 3 });
    });
    text(svg, W - R, H - 2, "Oregon Inlet", { fill: MUTED, "font-size": 10.5, "text-anchor": "end" });
  };

  Explorer.prototype.drawChart = function () {
    var self = this, d = this.data, s = d.stretches[this.k], rel = this.view === "relative";
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
    var d = this.data, s = d.stretches[this.k], km = s.length_m / 1000;
    this.root.querySelector(".hat-nx-cards").innerHTML = s.fills.map(function (f) {
      var left = f.since_before_m[String(d.last_year)];
      var pct = Math.round(left / f.step_m * 100);
      return '<div class="hat-nx-card"><h4>' + s.name + " " + f.year + "</h4><dl>" +
        "<dt>Sand placed</dt><dd>" + (f.volume_cy / 1e6).toFixed(1) + " million cubic yards</dd>" +
        "<dt>Beach length</dt><dd>about " + km.toFixed(1) + " km (" + (km / 1.609).toFixed(1) + " miles)</dd>" +
        "<dt>Sand per metre of beach</dt><dd>about " + f.m3_per_m + " cubic metres</dd>" +
        "<dt>Jump the year after</dt><dd><b>" + signed(f.step_m) + " m</b> compared with the rest of the island</dd>" +
        "<dt>Left in " + d.last_year + "</dt><dd>" + signed(left) + " m" + (f.step_m > 0 && left > 0 ? " (about " + pct + "% of the jump)" : "") + "</dd>" +
        "</dl></div>";
    }).join("");
  };

  function start() { document.querySelectorAll(".hat-nx").forEach(function (r) { new Explorer(r); }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
