// "Your stretch of beach" on /hatteras/your-beach/ (markup in _includes/hatteras/stretch_picker.liquid; data from
// tools/hatteras_stretch_data.py and tools/hatteras_island_outline.py). Pick a place: where it is on the island, the
// shoreline rate in plain words, its yearly position since 1984, the fills, road moves and bridges there, the overwash
// seen in the aerial record, and a then-and-now photo pair. The choice is kept in the address (#avon) for sharing.
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var INK = "#1a1a1a", MUTED = "#6b7378", GRID = "#e6e9eb", TEAL = "#2f7f93", FILL = "#c8880f", SAND = "#e8dcb8";
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { if (attrs[k] !== null) e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }
  function text(parent, x, y, s, attrs) { var t = el("text", Object.assign({ x: x, y: y }, attrs || {}), parent); t.textContent = s; return t; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function day(iso) { var p = iso.split("-"); return +p[2] + " " + MONTHS[+p[1] - 1] + " " + p[0]; }
  function month(iso) { var p = iso.split("-"); return MONTHS[+p[1] - 1] + " " + p[0]; }
  function rateWords(r) {
    if (Math.abs(r) < 0.25) return "very little, <b>less than 0.25 m a year</b> either way";
    return "about <b>" + Math.abs(r).toFixed(1) + " m a year " + (r > 0 ? "seaward" : "landward") + "</b> (" +
      (r > 0 ? "growing" : "eroding") + ", roughly " + Math.round(Math.abs(r) * 10) + " m a decade)";
  }

  function Picker(root) {
    this.root = root;
    // asset paths in the data start /assets/hatteras/; the page says where that folder is, so a copy of the site
    // with other paths still finds them. Page links come from real links in the markup for the same reason.
    var assets = root.getAttribute("data-assets") || "/assets/hatteras/";
    this.asset = function (path) { return path.replace(/^\/assets\/hatteras\//, assets); };
    this.link = function (name) { var a = root.querySelector('[data-link="' + name + '"]'); return a ? a.getAttribute("href") : "#"; };
    var self = this;
    Promise.all([fetch(root.getAttribute("data-src")).then(function (r) { return r.json(); }),
                 fetch(root.getAttribute("data-outline")).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })])
      .then(function (res) {
        self.data = res[0];
        self.outline = res[1];
        var want = (location.hash || "").slice(1);
        self.i = Math.max(0, self.data.places.findIndex(function (p) { return p.id === want; }));
        self.buttons();
        self.draw();
        var w = root.clientWidth;
        window.addEventListener("resize", function () { if (root.clientWidth !== w) { w = root.clientWidth; self.drawMap(); self.drawChart(); } });
        window.addEventListener("hashchange", function () {
          var j = self.data.places.findIndex(function (p) { return p.id === location.hash.slice(1); });
          if (j >= 0 && j !== self.i) { self.i = j; self.draw(); }
        });
      });
  }

  Picker.prototype.buttons = function () {
    var self = this, seg = this.root.querySelector(".hat-sp-places");
    this.data.places.forEach(function (p, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = p.name;
      b.addEventListener("click", function () {
        self.i = i;
        self.draw();
        // keep the choice in the address for sharing; a sandboxed frame may refuse, which must not stop the redraw
        try { if (history.replaceState) history.replaceState(null, "", "#" + p.id); } catch (e) { /* ignore */ }
      });
      seg.appendChild(b);
    });
  };

  Picker.prototype.draw = function () {
    var self = this;
    this.root.querySelectorAll(".hat-sp-places button").forEach(function (b, j) {
      b.classList.toggle("on", j === self.i);
      b.setAttribute("aria-pressed", j === self.i ? "true" : "false");
    });
    this.drawMap();
    this.drawSummary();
    this.drawChart();
    this.drawPhotos();
  };

  // The island turned so north runs right, ocean side down; the chosen place in teal along the ocean shore
  Picker.prototype.drawMap = function () {
    var box = this.root.querySelector(".hat-sp-map"), o = this.outline, p = this.data.places[this.i];
    var W = Math.max(box.clientWidth, 300), L = 8, R = 8, top = 22, kmMax = 60;
    var pxkm = (W - L - R) / kmMax, X = function (km) { return L + km * pxkm; };
    var e0 = o ? o.east_m[0] : 0, h = o ? (o.east_m[1] - o.east_m[0]) / 1000 * pxkm : 10;
    var Y = function (east) { return top + (east - e0) / 1000 * pxkm; };
    var H = top + h + 16;
    box.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H, role: "img",
      "aria-label": p.name + ": " + p.km[0] + " to " + p.km[1] + " km north of Cape Point" }, box);
    if (o) {
      o.rings.forEach(function (ring) {
        el("path", { d: "M" + ring.map(function (q) { return X(q[0]).toFixed(1) + "," + Y(q[1]).toFixed(1); }).join("L") + "Z",
          fill: SAND, stroke: "#b9a67a", "stroke-width": 0.8 }, svg);
      });
      var pts = o.shore.filter(function (q) { return q[0] >= p.km[0] && q[0] <= p.km[1]; })
        .map(function (q) { return X(q[0]).toFixed(1) + "," + (Y(q[1]) + 3).toFixed(1); });
      if (pts.length) el("polyline", { points: pts.join(" "), fill: "none", stroke: TEAL, "stroke-width": 6, "stroke-linecap": "round" }, svg);
    } else {
      el("rect", { x: L, y: top, width: W - L - R, height: 10, rx: 5, fill: SAND }, svg);
      el("rect", { x: X(p.km[0]), y: top - 2, width: X(p.km[1]) - X(p.km[0]), height: 14, rx: 3, fill: TEAL }, svg);
    }
    var mid = (p.km[0] + p.km[1]) / 2;
    text(svg, Math.min(Math.max(X(mid), L + 40), W - R - 40), 14, p.name, { "text-anchor": "middle", fill: INK, "font-size": 12.5, "font-weight": 600 });
    text(svg, L, H - 3, "Cape Point", { fill: MUTED, "font-size": 10.5 });
    text(svg, W - R, H - 3, "Oregon Inlet", { fill: MUTED, "font-size": 10.5, "text-anchor": "end" });
  };

  Picker.prototype.drawSummary = function () {
    var d = this.data, p = d.places[this.i], w = d.windows, link = this.link;
    var nourished = p.fills.length > 0;
    this.root.querySelector(".hat-sp-headline").innerHTML = "<b>" + esc(p.name) + ".</b> Since 1996 the shoreline here has moved " +
      rateWords(p.rate[w[0].key]) + "." + (nourished ? " That includes the sand added by beach fills." : "");
    this.root.querySelector(".hat-sp-what").textContent = p.what + " About " + (p.km[1] - p.km[0]).toFixed(1) + " km of beach, " +
      p.km[0].toFixed(1) + " to " + p.km[1].toFixed(1) + " km north of Cape Point.";
    var cards = [];
    cards.push('<div class="hat-sp-card"><h3>Shoreline</h3><dl>' + w.map(function (x) {
      var r = p.rate[x.key];
      return "<dt>" + esc(x.key === "1996_2026" ? "Whole record (1996–2026)" : x.label) + "</dt><dd>" + (r > 0 ? "+" : r < 0 ? "−" : "") +
        Math.abs(r).toFixed(1) + " m a year</dd>";
    }).join("") + '</dl><p class="hat-sp-note">+ seaward (growing), − landward (eroding). From satellite shorelines.</p></div>');
    cards.push('<div class="hat-sp-card"><h3>Beach fills</h3>' + (p.fills.length ? "<ul>" + p.fills.map(function (f) {
      return "<li><b>" + f.year + "</b>: " + esc(f.name) + ", about " + (f.volume_cy / 1e6).toFixed(1) + " million cubic yards" +
        " (sand placed " + month(f.placed[0]) + " to " + month(f.placed[1]) + ")" +
        (f.stretch !== p.name ? ", part of the " + esc(f.stretch) + " project" : "") + ".</li>";
    }).join("") + '</ul><p class="hat-sp-note"><a href="' + link("nourishment") + '">Each fill in photos</a></p>' :
      "<p>None on record here.</p>") + "</div>");
    cards.push('<div class="hat-sp-card"><h3>NC-12 and bridges</h3>' + (p.events.length ? "<ul>" + p.events.map(function (e) {
      return "<li><b>" + e.year + "</b>: " + esc(e.title) + ". " + esc(e.detail) + "</li>";
    }).join("") + "</ul>" : "<p>No road moves or bridges on record here.</p>") +
      '<p class="hat-sp-note"><a href="' + link("nc12") + '">The history of NC-12</a></p></div>');
    var ow;
    if (p.overwash === null) {
      ow = "<p>This stretch is outside the overwash record, which covers Cape Point to just north of Rodanthe.</p>";
    } else if (!p.overwash.length) {
      ow = "<p>No overwash seen here in any of the " + d.overwash_images + " aerial images checked, 1984–2024.</p>";
    } else {
      ow = "<p>Seen in " + p.overwash.length + " of the " + d.overwash_images + " aerial images checked, 1984–2024:</p><ul>" +
        p.overwash.map(function (o) {
          return "<li><b>" + month(o.image) + "</b>" + (o.storms.length ? ", after " + o.storms.map(esc).join(", ") : "") +
            "; " + o.domains + " of " + o.of + " half-kilometre stretches.</li>";
        }).join("") + "</ul>";
    }
    cards.push('<div class="hat-sp-card"><h3>Storm overwash</h3>' + ow +
      '<p class="hat-sp-note"><a href="' + link("storms") + '">All storms since 1984</a></p></div>');
    this.root.querySelector(".hat-sp-cards").innerHTML = cards.join("");
  };

  // Yearly position since 1984-86, fills marked in gold
  Picker.prototype.drawChart = function () {
    var box = this.root.querySelector(".hat-sp-chart"), p = this.data.places[this.i], v = p.yearly;
    var W = Math.max(box.clientWidth, 300), small = W < 560, H = small ? 220 : 250, top = 16, bottom = 30, left = small ? 36 : 46, right = 10;
    var y0 = 1984, y1 = 2025, vals = v.map(function (q) { return q[1]; });
    var vmin = Math.min(0, Math.min.apply(null, vals)), vmax = Math.max(10, Math.max.apply(null, vals));
    var step = (vmax - vmin) > 120 ? 40 : (vmax - vmin) > 60 ? 20 : 10;
    var lo = Math.floor(vmin / step) * step, hi = Math.ceil(vmax / step) * step;      // ticks land on 0
    var X = function (y) { return left + (y - y0) / (y1 - y0) * (W - left - right); };
    var Y = function (m) { return top + (hi - m) / (hi - lo) * (H - top - bottom); };
    box.innerHTML = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H, role: "img",
      "aria-label": "Chart of the yearly shoreline position at " + p.name + " since 1984, in metres seaward of where it was in 1984 to 1986" }, box);
    for (var m = lo; m <= hi; m += step) {
      el("line", { x1: left, x2: W - right, y1: Y(m), y2: Y(m), stroke: m === 0 ? INK : GRID }, svg);
      text(svg, left - 6, Y(m) + 4, (m > 0 ? "+" : m < 0 ? "−" : "") + Math.abs(m), { "text-anchor": "end", fill: MUTED, "font-size": 11.5 });
    }
    for (var y = 1985; y <= 2025; y += 5) text(svg, X(y), H - 10, y, { "text-anchor": "middle", fill: MUTED, "font-size": 11.5 });
    p.fills.forEach(function (f) {
      el("line", { x1: X(f.year + 0.5), x2: X(f.year + 0.5), y1: top, y2: H - bottom, stroke: FILL, "stroke-width": 2, "stroke-dasharray": "4 3" }, svg);
      text(svg, X(f.year + 0.5) + 4, top + 10, f.year + " fill", { fill: FILL, "font-size": 11.5, "font-weight": 600 });
    });
    el("polyline", { points: v.map(function (q) { return X(q[0]).toFixed(1) + "," + Y(q[1]).toFixed(1); }).join(" "),
      fill: "none", stroke: TEAL, "stroke-width": 2.4 }, svg);
    v.forEach(function (q) { el("circle", { cx: X(q[0]), cy: Y(q[1]), r: 2.4, fill: TEAL }, svg); });
  };

  Picker.prototype.drawPhotos = function () {
    var fig = this.root.querySelector(".hat-sp-photos"), p = this.data.places[this.i], asset = this.asset, ys = this.data.photo_years;
    if (!p.photos || !p.photos[ys[0]]) { fig.hidden = true; return; }
    fig.hidden = false;
    fig.querySelectorAll("img").forEach(function (im, k) {
      im.src = asset(p.photos[ys[k]]);
      im.alt = "Aerial photo of the beach at " + p.name + " in " + ys[k];
    });
    fig.querySelectorAll(".hat-sp-photo-year").forEach(function (s, k) { s.textContent = ys[k] === 1993 ? "1993 (black and white)" : "March " + ys[k]; });
    fig.querySelector(".hat-sp-photo-name").textContent = p.name;
  };

  function start() { document.querySelectorAll(".hat-sp").forEach(function (r) { new Picker(r); }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
