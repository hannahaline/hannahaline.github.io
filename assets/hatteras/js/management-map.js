// Where and when management happened, on /hatteras/management/ (markup in _includes/hatteras/management_map.liquid).
// Data: timeline.json (management events with their km range, and the storm record) from tools/hatteras_timeline_data.py,
// and the villages from shoreline_rates.json. Years run across, place along the island runs up (Cape Point at the
// bottom, Oregon Inlet at the top, north up as on a map). Every mark links to the page about that kind of action.
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var INK = "#1a1a1a", MUTED = "#6b7378", GRID = "#e6e9eb", FILL = "#c8880f", FILL_BG = "#f2d79a", ROAD = "#d55e00", GROIN = "#d7191c";
  var Y0 = 1965, Y1 = 2026, KM_TOP = 60;
  var STORM_MIN_M = 3;                 // named tropical storms at or above this water level, as on the Storms page
  var OREGON_KM = 59.5;                // the Basnight Bridge has no km of its own: drawn at the north end

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { if (attrs[k] !== null) e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }
  function text(parent, x, y, s, attrs) { var t = el("text", Object.assign({ x: x, y: y }, attrs || {}), parent); t.textContent = s; return t; }

  function Chart(root) {
    this.root = root;
    this.box = root.querySelector(".hat-mm-chart");
    this.tip = root.querySelector(".hat-tl-tip");
    this.links = { fill: root.getAttribute("data-fill"), road: root.getAttribute("data-road"), bridge: root.getAttribute("data-road"),
      structure: root.getAttribute("data-groin") };
    var self = this;
    Promise.all([root.getAttribute("data-timeline"), root.getAttribute("data-places")].map(function (u) {
      return fetch(u).then(function (r) { return r.json(); });
    })).then(function (d) {
      self.t = d[0];
      self.places = d[1].places;
      self.draw();
      var w = self.box.clientWidth;
      window.addEventListener("resize", function () { if (self.box.clientWidth !== w) { w = self.box.clientWidth; self.draw(); } });
    });
  }

  Chart.prototype.draw = function () {
    var self = this, W = Math.max(this.box.clientWidth - 2, 720);
    var left = 96, right = 196, top = 66, bottom = 40, H = 560;
    var X = function (y) { return left + (y - Y0) / (Y1 - Y0) * (W - left - right); };
    var Y = function (km) { return top + (KM_TOP - km) / KM_TOP * (H - top - bottom); };
    this.box.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H, role: "img", style: "display:block",
      "aria-label": "Management actions on Hatteras Island by year and by place along the island" }, this.box);

    // villages: faint lines across, names on the left
    this.places.forEach(function (p) {
      el("line", { x1: left, x2: W - right, y1: Y(p.km), y2: Y(p.km), stroke: GRID }, svg);
      text(svg, left - 8, Y(p.km) + 4, p.name, { "text-anchor": "end", fill: INK, "font-size": 12.5 });
    });
    text(svg, left - 8, Y(KM_TOP) + 4, "Oregon Inlet", { "text-anchor": "end", fill: MUTED, "font-size": 12 });
    // the satellite and storm records start in 1984
    el("rect", { x: left, y: top, width: X(1984) - left, height: H - top - bottom, fill: "rgba(107, 115, 120, 0.06)" }, svg);
    text(svg, (left + X(1984)) / 2, H - bottom - 8, "before the storm record", { "text-anchor": "middle", fill: MUTED, "font-size": 11 });
    // axes
    el("line", { x1: left, x2: left, y1: top, y2: H - bottom, stroke: INK }, svg);
    el("line", { x1: left, x2: W - right, y1: H - bottom, y2: H - bottom, stroke: INK }, svg);
    for (var y = 1970; y <= 2025; y += 5) {
      el("line", { x1: X(y), x2: X(y), y1: H - bottom, y2: H - bottom + 4, stroke: INK }, svg);
      text(svg, X(y), H - bottom + 18, y, { "text-anchor": "middle", fill: MUTED, "font-size": 12 });
    }
    var yl = text(svg, 0, 0, "south  ←  along the island  →  north", { fill: MUTED, "font-size": 11.5, "text-anchor": "middle" });
    yl.setAttribute("transform", "translate(14," + (top + (H - top - bottom) / 2) + ") rotate(-90)");

    // storms along the top: a tick at the year, names in up to three rows so neighbours do not overlap
    var best = {};
    this.t.storms.forEach(function (s) {
      if (s.name && s.type === "tropical" && s.wl >= STORM_MIN_M && (!best[s.name] || s.wl > best[s.name].wl)) best[s.name] = s;
    });
    var storms = Object.keys(best).map(function (k) { return best[k]; }).sort(function (a, b) { return a.y - b.y; });
    var rowEnd = [];
    text(svg, left - 8, top - 40, "Storms", { "text-anchor": "end", fill: MUTED, "font-size": 12 });
    storms.forEach(function (s) {
      var name = s.name.replace(/ [0-9]{4}$/, "").replace("Subtropical storm", "1991 storm"), x = X(s.y), w = name.length * 6.4 + 8, row = 0;
      while (rowEnd[row] !== undefined && rowEnd[row] > x - w / 2) row++;
      rowEnd[row] = x + w / 2;
      var yy = top - 44 + row * 13;
      el("line", { x1: x, x2: x, y1: yy + 3, y2: H - bottom, stroke: "rgba(33, 102, 172, 0.22)", "stroke-dasharray": "2 3" }, svg);
      el("path", { d: "M" + x + "," + (top - 2) + " l-4,-7 h8 z", fill: "#2166ac" }, svg);
      text(svg, x, yy, name, { "text-anchor": "middle", fill: "#2166ac", "font-size": 11 });
    });

    function hover(node, e) {
      node.addEventListener("mousemove", function (ev) {
        var t = self.tip, box = self.root.querySelector(".hat-shoremap-inner").getBoundingClientRect();
        t.innerHTML = "<b>" + e.year + ": " + e.title + "</b><br>" + e.detail + (e.model ? "" : "<br><i>Shown for context; not in the model.</i>") +
          "<br><span class='hat-tip-hint'>click for more</span>";
        t.hidden = false;
        var tx = ev.clientX - box.left + 14;
        if (tx + t.offsetWidth > box.width) tx = ev.clientX - box.left - t.offsetWidth - 14;
        t.style.left = tx + "px";
        t.style.top = (ev.clientY - box.top + 14) + "px";
      });
      node.addEventListener("mouseleave", function () { self.tip.hidden = true; });
    }
    function link(e, parent) {
      var a = el("a", { href: self.links[e.kind] }, parent);
      a.setAttribute("aria-label", e.year + ": " + e.title);
      return a;
    }

    var labels = [];      // right-hand labels, nudged apart afterwards
    this.t.management.forEach(function (e) {
      var km = e.km || [OREGON_KM - 0.4, OREGON_KM + 0.4], ya = Y(km[1]), yb = Y(km[0]), a = link(e, svg);
      if (e.kind === "structure") {          // the groins: a line from when they were built to today
        var g = el("g", {}, a);
        el("rect", { x: X(e.year), y: Y(2.75) - 3, width: X(Y1) - X(e.year), height: 6, fill: GROIN }, g);
        el("circle", { cx: X(e.year), cy: Y(2.75), r: 5, fill: GROIN, stroke: "#fff", "stroke-width": 1.5 }, g);
        hover(g, e);
        labels.push({ y: Y(2.75), text: "Buxton groins, 1969", color: GROIN });
      } else if (e.kind === "fill") {
        var r = el("rect", { x: X(e.year), y: ya, width: Math.max(X(e.year + 1) - X(e.year), 6), height: yb - ya,
          fill: FILL_BG, stroke: FILL, "stroke-width": 1.5 }, a);
        hover(r, e);
      } else if (e.kind === "road") {
        var gr = el("g", {}, a);
        el("rect", { x: X(e.year + 0.5) - 3, y: ya, width: 6, height: yb - ya, fill: ROAD }, gr);
        hover(gr, e);
      } else if (e.kind === "bridge") {      // a bridge carries the road from when it opened; later ones replace earlier ones
        var next = self.t.management.filter(function (o) { return o.kind === "bridge" && o !== e && o.year > e.year && JSON.stringify(o.km) === JSON.stringify(e.km); })[0];
        var end = next ? next.year : Y1, gb = el("g", {}, a);
        el("rect", { x: X(e.year), y: ya, width: X(end) - X(e.year), height: Math.max(yb - ya, 5),
          fill: e.model ? "rgba(26, 26, 26, 0.75)" : "none", stroke: INK, "stroke-width": 1.4,
          "stroke-dasharray": e.model ? null : "3 2" }, gb);
        hover(gb, e);
      }
    });
    // right-hand labels for places with several actions
    labels.push({ y: Y(5), text: "Buxton: road moved, 2 fills", color: INK },
      { y: Y(12), text: "Avon: one fill", color: INK },
      { y: Y(42.5), text: "S-curves: road, fill, bridge", color: INK },
      { y: Y(49.9), text: "New Inlet: bridges", color: INK },
      { y: Y(OREGON_KM), text: "Oregon Inlet bridge", color: MUTED });
    labels.sort(function (a, b) { return a.y - b.y; });
    for (var i = 1; i < labels.length; i++) if (labels[i].y - labels[i - 1].y < 15) labels[i].y = labels[i - 1].y + 15;
    labels.forEach(function (l) { text(svg, W - right + 8, l.y + 4, l.text, { fill: l.color, "font-size": 11.5 }); });
  };

  function start() { document.querySelectorAll(".hat-mm").forEach(function (r) { new Chart(r); }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
