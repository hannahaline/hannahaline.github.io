// Sea-level chart (markup in _includes/hatteras/sea_level.liquid; data from tools/hatteras_sealevel_data.py).
// The Duck gauge's monthly record faded, yearly means on top, NOAA's whole-record trend dashed, and the trend
// the model uses for each period. Hover or arrow keys pick a year.
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var INK = "#1a1a1a", MUTED = "#6b7378", GRID = "#e6e9eb", MONTH = "#b9bfc2", YEAR = "#3b3f42";
  var REF = "#2c6e49", PERIOD = ["#b2182b", "#2166ac"], BAND = ["#fbeee9", "#e9f1f8"];  // house REF, RdBu pair

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { if (attrs[k] !== null) e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }
  function text(parent, x, y, s, attrs) {
    var t = el("text", Object.assign({ x: x, y: y }, attrs || {}), parent);
    t.textContent = s;
    return t;
  }
  function halo(attrs) { return Object.assign({ "paint-order": "stroke", stroke: "#fff", "stroke-width": 3 }, attrs); }
  function years(a, b) { return a + "–" + b; }
  function rate(p) { return p.mm_yr.toFixed(1) + " mm a year"; }

  function SeaLevel(root) {
    this.root = root;
    this.chart = root.querySelector(".hat-sl-chart");
    this.tip = root.querySelector(".hat-tl-tip");
    var self = this;
    fetch(root.getAttribute("data-src")).then(function (r) { return r.json(); }).then(function (d) {
      self.data = d;
      self.legend();
      root.querySelector(".hat-sl-caption").textContent =
        "Monthly mean sea level at the NOAA tide gauge at Duck (station 8651370), with the seasonal cycle removed, in " +
        "centimetres relative to the gauge's mean sea level datum. The dark line averages each full year; " +
        d.partial_years.filter(function (y) { return y > 1978 && y < 2026; }).join(", ") +
        " is left out because a month is missing. Straight lines are fitted to the monthly values.";
      self.draw();
      var w = self.chart.clientWidth;
      window.addEventListener("resize", function () { if (self.chart.clientWidth !== w) { w = self.chart.clientWidth; self.draw(); } });
    });
  }

  SeaLevel.prototype.legend = function () {
    var d = this.data, items = [
      '<span><i class="line" style="border-color:' + MONTH + '"></i>Monthly average</span>',
      '<span><i class="line thick" style="border-color:' + YEAR + '"></i>Yearly average</span>',
      '<span><i class="line dashed" style="border-color:' + REF + '"></i>Trend, whole record: ' + rate(d.noaa) + "</span>"];
    d.periods.forEach(function (p, i) {
      items.push('<span><i class="line thick" style="border-color:' + PERIOD[i] + '"></i>Trend, ' + years(p.start, p.end) + ": " + rate(p) + "</span>");
    });
    this.root.querySelector(".hat-tl-legend").innerHTML = items.join("");
  };

  SeaLevel.prototype.showTip = function (html, px, py) {
    var t = this.tip, box = this.root.querySelector(".hat-shoremap-inner").getBoundingClientRect();
    t.innerHTML = html;
    t.hidden = false;
    var x = px - box.left + 14, y = py - box.top + 14;
    if (x + t.offsetWidth > box.width) x = px - box.left - t.offsetWidth - 14;
    t.style.left = x + "px";
    t.style.top = y + "px";
  };

  SeaLevel.prototype.draw = function () {
    var self = this, d = this.data;
    var W = Math.max(this.chart.clientWidth, 320), small = W < 640;
    var left = small ? 36 : 64, right = small ? 10 : 18, top = 16, H = small ? 300 : 380, bottom = 30;
    var x0 = 1978, x1 = 2027;
    var vals = d.monthly.map(function (m) { return m[1]; });
    var lo = Math.floor(Math.min.apply(null, vals) * 10) / 10, hi = Math.ceil(Math.max.apply(null, vals) * 10) / 10;
    var X = function (t) { return left + (t - x0) / (x1 - x0) * (W - left - right); };
    var Y = function (m) { return top + (hi - m) / (hi - lo) * (H - top - bottom); };

    this.chart.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H }, this.chart);

    // the model periods as faint bands behind everything
    d.periods.forEach(function (p, i) {
      el("rect", { x: X(p.start), y: top, width: X(p.end + 1) - X(p.start), height: H - top - bottom, fill: BAND[i], opacity: 0.8 }, svg);
    });

    // grid: every 10 cm, every 5 years
    for (var cm = Math.ceil(lo * 10) * 10; cm <= hi * 100; cm += 10) {
      el("line", { x1: left, x2: W - right, y1: Y(cm / 100), y2: Y(cm / 100), stroke: cm === 0 ? "#9aa0a3" : GRID }, svg);
      text(svg, left - 6, Y(cm / 100) + 4, (cm > 0 ? "+" : "") + cm + (small ? "" : " cm"), { "text-anchor": "end", fill: MUTED, "font-size": 12 });
    }
    for (var yr = 1980; yr <= 2025; yr += 5) {
      if (small && yr % 10) continue;
      el("line", { x1: X(yr), x2: X(yr), y1: H - bottom, y2: H - bottom + 4, stroke: MUTED }, svg);
      text(svg, X(yr), H - bottom + 18, yr, { "text-anchor": "middle", fill: MUTED, "font-size": 12 });
    }

    // monthly record, yearly means (broken where a year is missing)
    el("polyline", { points: d.monthly.map(function (m) { return X(m[0]).toFixed(1) + "," + Y(m[1]).toFixed(1); }).join(" "),
      fill: "none", stroke: MONTH, "stroke-width": 1 }, svg);
    var runs = [], run = [];
    d.yearly.forEach(function (y, i) {
      if (i && y[0] !== d.yearly[i - 1][0] + 1) { runs.push(run); run = []; }
      run.push(y);
    });
    runs.push(run);
    runs.forEach(function (r) {
      el("polyline", { points: r.map(function (y) { return X(y[0] + 0.5).toFixed(1) + "," + Y(y[1]).toFixed(1); }).join(" "),
        fill: "none", stroke: YEAR, "stroke-width": 2, "stroke-linejoin": "round" }, svg);
    });

    // trends: NOAA's whole record dashed, then each model period over its own years
    el("line", { x1: X(d.noaa.t0), y1: Y(d.noaa.v0), x2: X(d.noaa.t1), y2: Y(d.noaa.v1), stroke: REF, "stroke-width": 1.6, "stroke-dasharray": "6 4" }, svg);
    var lastT = d.monthly[d.monthly.length - 1][0] + 1 / 24;
    d.periods.forEach(function (p, i) {
      // the line spans the months it was fitted on: the last period stops where the record does
      var a = p.start, b = Math.min(p.end + 1, lastT), va = p.slope * a + p.intercept, vb = p.slope * b + p.intercept;
      el("line", { x1: X(a), y1: Y(va), x2: X(b), y2: Y(vb), stroke: PERIOD[i], "stroke-width": 3, "stroke-linecap": "round" }, svg);
      if (!small) {
        // labels in the empty lower part of each band: earlier at its left edge, later at its right edge
        var lx = i === 0 ? X(a) + 6 : X(p.end + 1) - 6, ly = H - bottom - 30, anchor = i === 0 ? "start" : "end";
        text(svg, lx, ly, years(p.start, p.end), halo({ "text-anchor": anchor, fill: PERIOD[i], "font-size": 12.5, "font-weight": 700 }));
        text(svg, lx, ly + 15, rate(p), halo({ "text-anchor": anchor, fill: PERIOD[i], "font-size": 12.5 }));
      }
    });

    // hover and keyboard: snap to a year
    var cross = el("line", { y1: top, y2: H - bottom, stroke: INK, "stroke-width": 1, opacity: 0, "pointer-events": "none" }, svg);
    var dot = el("circle", { r: 4.5, fill: YEAR, stroke: "#fff", "stroke-width": 1.5, opacity: 0, "pointer-events": "none" }, svg);
    var hit = el("rect", { x: left, y: top, width: W - left - right, height: H - top - bottom, fill: "transparent", tabindex: 0,
      "aria-label": "Sea level by year. Use the arrow keys to step through the years." }, svg);
    var byYear = {};
    d.yearly.forEach(function (y) { byYear[y[0]] = y[1]; });
    var first = d.yearly[0][0], last = d.yearly[d.yearly.length - 1][0], cur = null;

    function pick(year, px, py) {
      year = Math.max(first, Math.min(last, year));
      cur = year;
      var v = byYear[year], cx = X(year + 0.5);
      cross.setAttribute("x1", cx); cross.setAttribute("x2", cx); cross.setAttribute("opacity", 0.35);
      var html = "<b>" + year + "</b><br>";
      if (v === undefined) {
        dot.setAttribute("opacity", 0);
        html += "No yearly average: a month is missing";
      } else {
        dot.setAttribute("cx", cx); dot.setAttribute("cy", Y(v)); dot.setAttribute("opacity", 1);
        html += "Yearly average " + (v >= 0 ? "+" : "") + (v * 100).toFixed(1) + " cm";
      }
      d.periods.forEach(function (p, i) {
        if (year >= p.start && year <= p.end) html += "<br><span style='color:" + PERIOD[i] + "'>In the model's " + years(p.start, p.end) + " period: " + rate(p) + "</span>";
      });
      if (px === undefined) { var r = hit.getBoundingClientRect(); px = r.left + cx - left; py = r.top + (v === undefined ? 20 : Y(v) - top); }
      self.showTip(html, px, py);
    }
    function clear() { cross.setAttribute("opacity", 0); dot.setAttribute("opacity", 0); self.tip.hidden = true; }
    hit.addEventListener("mousemove", function (e) {
      var r = hit.getBoundingClientRect();
      pick(Math.floor(x0 + (e.clientX - r.left) / r.width * (x1 - x0)), e.clientX, e.clientY);
    });
    hit.addEventListener("mouseleave", clear);
    hit.addEventListener("blur", clear);
    hit.addEventListener("focus", function () { pick(cur === null ? last : cur); });
    hit.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
        e.preventDefault();
        pick((cur === null ? last : cur) + (e.key === "ArrowLeft" ? -1 : 1));
      }
    });
  };

  function start() {
    document.querySelectorAll(".hat-sealevel").forEach(function (r) { new SeaLevel(r); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
