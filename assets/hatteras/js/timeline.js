// Storms and management timeline (markup in _includes/hatteras/timeline.liquid; data from tools/hatteras_timeline_data.py).
// One SVG: high-water events above, management lanes below, on a shared year axis. mode "storms" or "management" draws
// only that half. Hovering a management event sends "hat:reach" with its km range, which the shoreline map draws.
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var INK = "#1a1a1a", MUTED = "#6b7378", GRID = "#e6e9eb";
  var TROPICAL = "#c8880f", OTHER = "#6baed6", SAND = "#f6e3b8";  // house ADDED, SMOOTH_RAMP[1], ADDED_FILL
  var LABEL_MIN_M = 3;  // tropical storms at or above this water level are named on the chart; the rest on hover

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }
  function text(parent, x, y, s, attrs) {
    var t = el("text", Object.assign({ x: x, y: y }, attrs || {}), parent);
    t.textContent = s;
    return t;
  }
  function reach(detail) { window.dispatchEvent(new CustomEvent("hat:reach", { detail: detail })); }

  function Timeline(root) {
    this.root = root;
    this.mode = root.getAttribute("data-mode");
    this.show = "all";
    this.chart = root.querySelector(".hat-tl-chart");
    this.tip = root.querySelector(".hat-tl-tip");
    var self = this;
    fetch(root.getAttribute("data-src")).then(function (r) { return r.json(); }).then(function (d) {
      self.data = d;
      self.legend();
      root.querySelector(".hat-tl-caption").textContent = (self.mode === "management" ? "" : d.storm_note) +
        (self.mode === "storms" ? "" : (self.mode === "management" ? "" : " ") +
          "The Navy built the Buxton groins in 1969, before this record begins. Events marked “not in the model” are shown for context only.");
      root.querySelectorAll("[data-show]").forEach(function (b) {
        b.addEventListener("click", function () {
          self.show = b.getAttribute("data-show");
          root.querySelectorAll("[data-show]").forEach(function (o) { o.classList.toggle("on", o === b); });
          self.draw();
        });
      });
      self.draw();
      var w = self.chart.clientWidth;
      window.addEventListener("resize", function () { if (self.chart.clientWidth !== w) { w = self.chart.clientWidth; self.draw(); } });
    });
  }

  Timeline.prototype.legend = function () {
    var items = [];
    if (this.mode !== "management") {
      items.push('<span><i class="dot" style="background:' + TROPICAL + '"></i>Tropical storm or hurricane within ' + this.data.tc_km + " km</span>");
      items.push('<span><i class="dot small" style="background:' + OTHER + '"></i>Other high-water event</span>');
    }
    if (this.mode !== "storms") {
      items.push('<span><i class="bar"></i>Beach nourishment</span>');
      items.push('<span><i class="diamond"></i>NC-12 moved landward</span>');
      items.push('<span><i class="square"></i>Bridge</span>');
      items.push('<span><i class="square open"></i>Open mark: not in the model</span>');
    }
    this.root.querySelector(".hat-tl-legend").innerHTML = items.join("");
  };

  Timeline.prototype.showTip = function (html, evt) {
    var t = this.tip, box = this.root.querySelector(".hat-shoremap-inner").getBoundingClientRect();
    t.innerHTML = html;
    t.hidden = false;
    var x = evt.clientX - box.left + 14, y = evt.clientY - box.top + 14;
    if (x + t.offsetWidth > box.width) x = box.width - t.offsetWidth - 4;
    t.style.left = x + "px";
    t.style.top = y + "px";
  };
  Timeline.prototype.hideTip = function () { this.tip.hidden = true; };

  Timeline.prototype.draw = function () {
    var self = this, d = this.data;
    var W = Math.max(this.chart.clientWidth, 320), small = W < 640;
    var left = small ? 8 : 132, right = 14;
    var storms = this.mode === "management" ? [] : d.storms.filter(function (s) { return self.show === "all" || s.type === "tropical"; });
    var stormH = storms.length ? 230 : 0, laneH = 44, top = storms.length ? 26 : 6;
    var fills = d.management.filter(function (m) { return m.kind === "fill"; });
    var roads = d.management.filter(function (m) { return m.kind === "road" || m.kind === "bridge"; });
    var lanes = this.mode === "storms" ? [] : [{ name: "Beach nourishment", items: fills }, { name: "NC-12 and bridges", items: roads }];
    var x0 = d.range[0], x1 = d.range[1] + 1;
    var X = function (y) { return left + (y - x0) / (x1 - x0) * (W - left - right); };

    // place every lane's labels first (row per overlap), so each lane is as tall as its rows
    lanes.forEach(function (lane) {
      var rows = [];
      lane.placed = lane.items.map(function (m) {
        var cx = X(m.year + 0.5), label = labelFor(m), tw = label.length * 6.2;
        // label to the right of the mark, or to its left where it would run off the chart
        var markR = m.kind === "fill" ? X(m.year + 1) : cx + 7, markL = m.kind === "fill" ? X(m.year) : cx - 7;
        var flip = markR + 4 + tw > W - right, tx = flip ? markL - 4 : markR + 4;
        var a = flip ? tx - tw : markL, b = flip ? markR : tx + tw, row = 0;
        while (rows.some(function (r) { return r.row === row && a < r.x1 + 6 && b > r.x0 - 6; })) row++;
        rows.push({ row: row, x0: a, x1: b });
        return { m: m, cx: cx, label: label, flip: flip, tx: tx, row: row };
      });
      var n = lane.placed.reduce(function (k, p) { return Math.max(k, p.row + 1); }, 1);
      lane.h = Math.max(laneH * 1.5, n * 16 + 30);
    });
    var lanesH = lanes.reduce(function (k, l) { return k + l.h; }, 0);
    var H = top + stormH + (storms.length ? 18 : 0) + lanesH + 34;

    this.chart.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H }, this.chart);

    // year grid and axis
    var axisY = H - 24;
    for (var yr = x0; yr <= x1; yr++) {
      var major = yr % 5 === 0;
      if (!major && small) continue;
      el("line", { x1: X(yr), x2: X(yr), y1: top - 6, y2: axisY, stroke: major ? GRID : "#f2f4f5" }, svg);
      if (major) text(svg, X(yr), axisY + 16, yr, { "text-anchor": "middle", fill: MUTED, "font-size": 12 });
    }

    // storms: stems from mean high water, dots at the peak water level
    if (storms.length) {
      var maxWl = 5.5, base = top + stormH;
      var Y = function (m) { return base - m / maxWl * stormH; };
      [0, 1, 2, 3, 4, 5].forEach(function (m) {
        el("line", { x1: left, x2: W - right, y1: Y(m), y2: Y(m), stroke: m === 0 ? "#9aa0a3" : GRID }, svg);
        text(svg, left - 6, Y(m) + 4, m + " m", { "text-anchor": "end", fill: MUTED, "font-size": 12, display: small ? "none" : null });
      });
      if (!small) {
        var lab = text(svg, 0, 0, "Peak water level", { fill: INK, "font-size": 12, "font-weight": 600 });
        lab.setAttribute("transform", "translate(14," + (top + stormH / 2) + ") rotate(-90)");
        lab.setAttribute("text-anchor", "middle");
        var lab2 = text(svg, 0, 0, "above mean high water", { fill: MUTED, "font-size": 11 });
        lab2.setAttribute("transform", "translate(30," + (top + stormH / 2) + ") rotate(-90)");
        lab2.setAttribute("text-anchor", "middle");
      }
      var g = el("g", {}, svg);
      storms.slice().sort(function (a, b) { return (a.type === "tropical") - (b.type === "tropical"); }).forEach(function (s) {
        var cx = X(s.y), cy = Y(s.wl), trop = s.type === "tropical";
        el("line", { x1: cx, x2: cx, y1: base, y2: cy, stroke: trop ? TROPICAL : OTHER, "stroke-width": 1, opacity: 0.5 }, g);
        var c = el("circle", { cx: cx, cy: cy, r: trop ? 4.5 : 3, fill: s.unchecked ? "#fff" : (trop ? TROPICAL : OTHER),
          stroke: trop ? (s.unchecked ? TROPICAL : "#fff") : (s.unchecked ? OTHER : "none"), "stroke-width": s.unchecked ? 2 : 1.2, tabindex: 0 }, g);
        var date = new Date(s.t + ":00");
        var html = "<b>" + (s.name || "High-water event") + "</b><br>" +
          date.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" }) + "<br>" +
          "Peak water level " + s.wl.toFixed(1) + " m above mean high water<br>" +
          "Lasted about " + s.h + " hours" +
          (s.unchecked ? "<br><span class='hat-tip-hint'>2025: peak time approximate</span>" : "");
        c.addEventListener("mousemove", function (e) { self.showTip(html, e); });
        c.addEventListener("mouseleave", function () { self.hideTip(); });
        c.addEventListener("focus", function () { var r = c.getBoundingClientRect(); self.showTip(html, { clientX: r.right, clientY: r.top }); });
        c.addEventListener("blur", function () { self.hideTip(); });
      });

      // names: each tropical storm once, at its highest event, rows bumped up to avoid overlap
      var best = {};
      storms.forEach(function (s) { if (s.name && s.wl >= LABEL_MIN_M && (!best[s.name] || s.wl > best[s.name].wl)) best[s.name] = s; });
      var biggestOther = storms.filter(function (s) { return s.type === "other"; }).sort(function (a, b) { return b.wl - a.wl; })[0];
      var labels = Object.keys(best).map(function (k) { return { s: best[k], t: k, it: false }; });
      if (biggestOther) labels.push({ s: biggestOther, t: "nor’easter", it: true });
      labels.sort(function (a, b) { return a.s.y - b.s.y; });
      var placed = [];
      labels.forEach(function (L) {
        var w = L.t.length * 6.3, cx = X(L.s.y), row = 0, y;
        for (;;) {
          y = Y(L.s.wl) - 9 - row * 14;
          var hit = placed.some(function (p) { return Math.abs(p.y - y) < 13 && cx - w / 2 < p.x1 + 4 && cx + w / 2 > p.x0 - 4; });
          if (!hit) break;
          row++;
        }
        placed.push({ x0: cx - w / 2, x1: cx + w / 2, y: y });
        if (row) el("line", { x1: cx, x2: cx, y1: Y(L.s.wl) - 5, y2: y + 2, stroke: MUTED, "stroke-width": 0.6 }, svg);
        text(svg, cx, y, L.t, { "text-anchor": "middle", "font-size": 11.5, fill: INK, "font-style": L.it ? "italic" : null,
          "paint-order": "stroke", stroke: "#fff", "stroke-width": 3 });
      });
    }

    // management lanes
    var y0 = top + stormH + (storms.length ? 18 : 0);
    lanes.forEach(function (lane, i) {
      var mid = y0 + lane.h / 2;
      el("rect", { x: left, y: y0 + 4, width: W - left - right, height: lane.h - 8, fill: i % 2 ? "#f7f9fa" : "#fbfcfc" }, svg);
      if (!small) text(svg, left - 8, mid + 4, lane.name, { "text-anchor": "end", fill: INK, "font-size": 12, "font-weight": 600 });
      else text(svg, left + 4, y0 + 15, lane.name, { fill: MUTED, "font-size": 11 });
      var firstRowY = y0 + 22;
      lane.placed.forEach(function (p) {
        var m = p.m, cx = p.cx, label = p.label, flip = p.flip, tx = p.tx;
        var cy = firstRowY + p.row * 16;
        var g = el("g", { tabindex: 0, class: "hat-tl-event", "aria-label": m.year + ": " + m.title }, svg);
        if (m.kind === "fill") el("rect", { x: X(m.year), y: cy - 6, width: Math.max(X(m.year + 1) - X(m.year), 5), height: 12, rx: 2, fill: SAND, stroke: TROPICAL }, g);
        else if (m.kind === "road") el("path", { d: "M" + cx + " " + (cy - 6) + "l6 6l-6 6l-6 -6z", fill: INK }, g);
        else el("rect", { x: cx - 5, y: cy - 5, width: 10, height: 10, fill: m.model ? INK : "#fff", stroke: INK, "stroke-width": 1.5 }, g);
        text(g, tx, cy + 4, label, { "font-size": 11.5, fill: INK, "text-anchor": flip ? "end" : "start", "paint-order": "stroke", stroke: "#fff", "stroke-width": 3 });
        var html = "<b>" + m.year + ": " + m.title + "</b><br>" + m.detail +
          (m.model ? "" : "<br><span class='hat-tip-hint'>Not in the model</span>") +
          (m.km && document.getElementById("shoremap") ? "<br><span class='hat-tip-hint'>Highlighted on the map</span>" : "");
        var on = function (e) { self.showTip(html, e); if (m.km) reach({ km: m.km, label: m.year + " " + m.title }); };
        var off = function () { self.hideTip(); reach(null); };
        g.addEventListener("mousemove", on);
        g.addEventListener("mouseleave", off);
        g.addEventListener("focus", function () { var r = g.getBoundingClientRect(); on({ clientX: r.right, clientY: r.top }); });
        g.addEventListener("blur", off);
      });
      y0 += lane.h;
    });

    function labelFor(m) {
      if (m.kind === "fill") return m.title.split(" ")[0] + " " + m.year;
      if (m.kind === "road") return "NC-12 moved " + m.year;
      return m.title.replace(" replaces the temporary bridge", "").replace(" opens at Oregon Inlet", "").replace(" opens", "") + " " + m.year;
    }
  };

  function start() {
    document.querySelectorAll(".hat-timeline").forEach(function (r) { new Timeline(r); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
