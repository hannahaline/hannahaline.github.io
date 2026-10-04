// Model versus observed shoreline change along the island (markup in _includes/hatteras/model_vs_observed.liquid;
// data from tools/hatteras_model_data.py). One SVG: the observed rate per 500 m stretch (dots) and its 7-stretch
// smoothing (black line), and the model's rate in each management run the reader switches on. Unpublished results:
// the include renders only while hatteras_draft is on.
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var INK = "#1a1a1a", MUTED = "#6b7378", GRID = "#e6e9eb", DOT = "#9aa0a3", FILL_BG = "rgba(246, 227, 184, 0.55)";
  // Okabe-Ito, colour-blind safe; full management in the strongest blue
  var COLOR = { natural: "#d55e00", road: "#e69f00", dunes_fills: "#009e73", road_dunes: "#56b4e9", full: "#0072b2" };
  var YMIN = -6, YMAX = 6;                     // m/yr; values beyond are drawn at the edge with their value
  var DEFAULT_ON = { natural: true, full: true };

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { if (attrs[k] !== null) e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }
  function text(parent, x, y, s, attrs) { var t = el("text", Object.assign({ x: x, y: y }, attrs || {}), parent); t.textContent = s; return t; }
  function fmt(v) { return (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(1); }

  function Panel(root) {
    this.root = root;
    this.chart = root.querySelector(".hat-mvo-chart");
    this.tip = root.querySelector(".hat-tl-tip");
    this.win = 0;
    this.on = Object.assign({}, DEFAULT_ON);
    var self = this;
    fetch(root.getAttribute("data-src")).then(function (r) { return r.json(); }).then(function (d) {
      self.data = d;
      self.controls();
      self.draw();
      var w = self.chart.clientWidth;
      window.addEventListener("resize", function () { if (self.chart.clientWidth !== w) { w = self.chart.clientWidth; self.draw(); } });
    });
  }

  Panel.prototype.controls = function () {
    var self = this, d = this.data;
    var seg = this.root.querySelector(".hat-mvo-windows");
    d.windows.forEach(function (w, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = w.label;
      if (i === 0) b.className = "on";
      b.addEventListener("click", function () {
        self.win = i;
        seg.querySelectorAll("button").forEach(function (o, j) { o.classList.toggle("on", j === i); });
        self.draw();
      });
      seg.appendChild(b);
    });
    var box = this.root.querySelector(".hat-mvo-arms");
    box.innerHTML = '<span class="hat-mvo-key"><i class="obs"></i>Observed (satellite shorelines)</span>' +
      d.arms.map(function (a) {
        return '<label class="hat-mvo-key"><input type="checkbox" data-arm="' + a.id + '"' + (self.on[a.id] ? " checked" : "") + ">" +
          '<i style="background:' + COLOR[a.id] + '"></i>' + a.label + "</label>";
      }).join("");
    box.querySelectorAll("input").forEach(function (c) {
      c.addEventListener("change", function () { self.on[c.getAttribute("data-arm")] = c.checked; self.draw(); });
    });
  };

  Panel.prototype.draw = function () {
    var self = this, d = this.data, w = d.windows[this.win];
    var W = Math.max(this.chart.clientWidth, 320), small = W < 640;
    var left = small ? 34 : 58, right = 12, top = 34, H = small ? 300 : 380, bottom = 38;
    var x0 = 0, x1 = 45;
    var X = function (km) { return left + (km - x0) / (x1 - x0) * (W - left - right); };
    var Y = function (v) { return top + (YMAX - Math.max(YMIN, Math.min(YMAX, v))) / (YMAX - YMIN) * (H - top - bottom); };

    this.chart.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H }, this.chart);

    // nourished stretches, as on the shoreline map
    d.nourishments.forEach(function (n) {
      if (n.km[0] > x1) return;
      el("rect", { x: X(n.km[0]), y: top, width: X(Math.min(n.km[1], x1)) - X(n.km[0]), height: H - top - bottom, fill: FILL_BG }, svg);
    });
    // grid and axes
    for (var v = YMIN; v <= YMAX; v += 2) {
      el("line", { x1: left, x2: W - right, y1: Y(v), y2: Y(v), stroke: v === 0 ? "#9aa0a3" : GRID }, svg);
      text(svg, left - 6, Y(v) + 4, fmt(v).replace("+0.0", "0").replace(".0", ""), { "text-anchor": "end", fill: MUTED, "font-size": 12 });
    }
    for (var km = 0; km <= x1; km += 5) {
      text(svg, X(km), H - bottom + 16, km, { "text-anchor": "middle", fill: MUTED, "font-size": 12 });
    }
    text(svg, X(x1 / 2), H - 6, "km north of Cape Point", { "text-anchor": "middle", fill: MUTED, "font-size": 12 });
    if (!small) {
      var yl = text(svg, 0, 0, "m per year (+ seaward, − landward)", { fill: MUTED, "font-size": 12, "text-anchor": "middle" });
      yl.setAttribute("transform", "translate(13," + (top + (H - top - bottom) / 2) + ") rotate(-90)");
    }
    // axes: left and bottom lines with outward ticks, as in a paper figure
    el("line", { x1: left, x2: left, y1: top, y2: H - bottom, stroke: INK, "stroke-width": 1 }, svg);
    el("line", { x1: left, x2: W - right, y1: H - bottom, y2: H - bottom, stroke: INK, "stroke-width": 1 }, svg);
    for (var tv = YMIN; tv <= YMAX; tv += 2) el("line", { x1: left - 4, x2: left, y1: Y(tv), y2: Y(tv), stroke: INK }, svg);
    for (var tk = 0; tk <= x1; tk += 5) el("line", { x1: X(tk), x2: X(tk), y1: H - bottom, y2: H - bottom + 4, stroke: INK }, svg);

    // places along the top
    d.places.forEach(function (p, i) {
      if (p.km > x1) return;
      el("line", { x1: X(p.km), x2: X(p.km), y1: top - 4, y2: H - bottom, stroke: "rgba(107,115,120,0.25)" }, svg);
      text(svg, X(p.km), top - 8 - (i % 2) * 12, p.name, { "text-anchor": p.km < 1.5 ? "start" : "middle", fill: INK, "font-size": 11.5 });
    });

    // observed: raw stretch means as dots, the 7-stretch smoothing as the black line
    w.observed_raw.forEach(function (v, i) {
      if (v === null) return;
      el("circle", { cx: X(d.km[i]), cy: Y(v), r: 2.4, fill: DOT, opacity: 0.8 }, svg);
    });
    function line(vals, color, width, dash) {
      var pts = vals.map(function (v, i) { return v === null ? null : X(d.km[i]).toFixed(1) + "," + Y(v).toFixed(1); }).filter(Boolean);
      el("polyline", { points: pts.join(" "), fill: "none", stroke: color, "stroke-width": width, "stroke-linejoin": "round",
        "stroke-dasharray": dash || null }, svg);
      vals.forEach(function (v, i) {        // off-scale values: a marker at the edge with the value
        if (v === null || (v <= YMAX && v >= YMIN)) return;
        var y = Y(v), up = v > YMAX;
        el("path", { d: "M" + X(d.km[i]) + "," + (up ? y - 2 : y + 2) + " l-5," + (up ? 8 : -8) + " h10 z", fill: color }, svg);
        text(svg, X(d.km[i]) + 7, up ? y + 12 : y - 6, fmt(v), { fill: color, "font-size": 11 });
      });
    }
    w.runs.forEach(function (r) { if (self.on[r.arm]) line(r.rate, COLOR[r.arm], r.arm === "full" ? 2.6 : 2); });
    line(w.observed, INK, 3);

    // hover: the values at a stretch
    var cross = el("line", { y1: top, y2: H - bottom, stroke: INK, opacity: 0, "pointer-events": "none" }, svg);
    var hit = el("rect", { x: left, y: top, width: W - left - right, height: H - top - bottom, fill: "transparent" }, svg);
    hit.addEventListener("mousemove", function (e) {
      var r = hit.getBoundingClientRect(), km = x0 + (e.clientX - r.left) / r.width * (x1 - x0);
      var i = Math.max(0, Math.min(d.km.length - 1, Math.round(km / 0.5 - 0.5)));
      cross.setAttribute("x1", X(d.km[i])); cross.setAttribute("x2", X(d.km[i])); cross.setAttribute("opacity", 0.3);
      var html = "<b>Stretch " + d.gis[i] + "</b>, " + d.km[i].toFixed(1) + " km north of Cape Point<br>" +
        "Observed: " + (w.observed[i] === null ? "no data" : fmt(w.observed[i]) + " m/yr");
      w.runs.forEach(function (rr) {
        if (self.on[rr.arm] && rr.rate[i] !== null) {
          var a = d.arms.filter(function (x) { return x.id === rr.arm; })[0];
          html += "<br><span style='color:" + COLOR[rr.arm] + "'>" + a.label + ": " + fmt(rr.rate[i]) + " m/yr</span>";
        }
      });
      var t = self.tip, box = self.root.querySelector(".hat-shoremap-inner").getBoundingClientRect();
      t.innerHTML = html;
      t.hidden = false;
      var tx = e.clientX - box.left + 14;
      if (tx + t.offsetWidth > box.width) tx = e.clientX - box.left - t.offsetWidth - 14;
      t.style.left = tx + "px";
      t.style.top = (e.clientY - box.top + 14) + "px";
    });
    hit.addEventListener("mouseleave", function () { cross.setAttribute("opacity", 0); self.tip.hidden = true; });

    // how close each run comes, away from the two ends
    var rows = w.runs.filter(function (r) { return self.on[r.arm]; }).map(function (r) {
      var a = d.arms.filter(function (x) { return x.id === r.arm; })[0];
      return "<tr><th><i style='background:" + COLOR[r.arm] + "'></i>" + a.label + "</th><td>" + fmt(r.bias) + "</td><td>" + r.rmse.toFixed(1) + "</td></tr>";
    }).join("");
    this.root.querySelector(".hat-mvo-skill").innerHTML = rows ?
      "<thead><tr><th>Model run, " + w.label + "</th><th>Average difference (m/yr)</th><th>Typical miss (m/yr)</th></tr></thead><tbody>" + rows + "</tbody>" : "";
  };

  function start() { document.querySelectorAll(".hat-mvo").forEach(function (r) { new Panel(r); }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
