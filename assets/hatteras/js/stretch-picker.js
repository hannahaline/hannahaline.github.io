// "Your stretch of beach" on /hatteras/your-beach/ (markup in _includes/hatteras/stretch_picker.liquid; data from
// tools/hatteras_stretch_data.py and tools/hatteras_island_outline.py). Pick a place: where it is on the island, the
// shoreline rate in plain words, the fills, road moves and bridges there, the overwash
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
  // Rows for village names: each takes the lowest row where it clears the last name in that row
  function labelRows(places, X, size) {
    var ends = [];
    return places.map(function (p) {
      var w = p.name.length * size * 0.56 + 6, x0 = X(p.km) - w / 2, r = 0;
      while (ends[r] !== undefined && ends[r] > x0) r++;
      ends[r] = x0 + w;
      return r;
    });
  }
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
        window.addEventListener("resize", function () { if (root.clientWidth !== w) { w = root.clientWidth; self.drawMap(); } });
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
    this.drawPhotos();
  };

  // The island turned so north runs right, ocean side down; the chosen place in teal along the ocean shore
  Picker.prototype.drawMap = function () {
    var box = this.root.querySelector(".hat-sp-map"), o = this.outline, p = this.data.places[this.i];
    var W = Math.max(box.clientWidth, 300), L = 8, R = 8, kmMax = 60;
    var pxkm = (W - L - R) / kmMax, X = function (km) { return L + km * pxkm; };
    var villages = (this.data.villages || []).filter(function (v) { return v.km <= kmMax && v.name !== "Cape Point"; });   // Cape Point is already named at the corner
    var vrow = labelRows(villages, X, 10.5), nrows = villages.length ? Math.max.apply(null, vrow) + 1 : 0;
    var top = 22 + nrows * 12;
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
    // the villages in small grey type, stacked so close ones do not collide; the picked place in bold teal above them
    villages.forEach(function (v, i) {
      var y = 22 + (nrows - 1 - vrow[i]) * 12 + 9;
      el("line", { x1: X(v.km), x2: X(v.km), y1: y + 2, y2: top + 2, stroke: MUTED, "stroke-width": 0.6, "stroke-dasharray": "2 2" }, svg);
      text(svg, X(v.km), y, v.name, { "text-anchor": "middle", fill: MUTED, "font-size": 10.5, "paint-order": "stroke", stroke: "#fff", "stroke-width": 3 });
    });
    var mid = (p.km[0] + p.km[1]) / 2;
    text(svg, Math.min(Math.max(X(mid), L + 40), W - R - 40), 14, p.name, { "text-anchor": "middle", fill: TEAL, "font-size": 12.5, "font-weight": 600 });
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
    cards.push('<div class="hat-sp-card"><h3>Road, bridges and groins</h3>' + (p.events.length ? "<ul>" + p.events.map(function (e) {
      return "<li><b>" + e.year + "</b>: " + esc(e.title) + ". " + esc(e.detail) + "</li>";
    }).join("") + "</ul>" : "<p>No road moves, bridges or groins on record here.</p>") +
      '<p class="hat-sp-note"><a href="' + link("nc12") + '">The history of NC-12</a></p></div>');
    var ow;
    if (p.overwash === null) {
      ow = "<p>Outside the overwash record, which runs from Cape Point to just north of Rodanthe.</p>";
    } else if (!p.overwash.length) {
      ow = "<p>None seen in " + d.overwash_images + " aerial images, 1984–2024.</p>";
    } else {
      ow = "<p>Seen in " + p.overwash.length + " of " + d.overwash_images + " aerial images, 1984–2024:</p><ul class=\"hat-sp-tight\">" +
        p.overwash.map(function (o) {
          var storms = o.storms.map(function (n) { return esc(n.replace(/ \((\d{4})\)$/, " $1")); }).join(", ");
          return "<li><b>" + month(o.image).replace(/^(\w{3})\w*/, "$1") + "</b>" + (storms ? ": " + storms : "") + "</li>";
        }).join("") + "</ul>";
    }
    cards.push('<div class="hat-sp-card"><h3>Storm overwash</h3>' + ow +
      '<p class="hat-sp-note"><a href="' + link("storms") + '">All storms since 1984</a></p></div>');
    this.root.querySelector(".hat-sp-cards").innerHTML = cards.join("");
  };

  Picker.prototype.drawPhotos = function () {
    var fig = this.root.querySelector(".hat-sp-photos"), p = this.data.places[this.i], asset = this.asset, ys = this.data.photo_years;
    if (!p.photos || !p.photos[ys[0]]) { fig.hidden = true; return; }
    fig.hidden = false;
    [fig.querySelector(".hat-sp-before"), fig.querySelector(".hat-sp-after")].forEach(function (im, k) {
      im.src = asset(p.photos[ys[k]]);
      im.alt = "Aerial photo of the beach at " + p.name + " in " + ys[k];
    });
    // the 2024 photo sits on top, clipped at the divider; the range input moves the divider
    var range = fig.querySelector(".hat-sp-range"), after = fig.querySelector(".hat-sp-after"), divider = fig.querySelector(".hat-sp-divider");
    var clip = function () { after.style.clipPath = "inset(0 0 0 " + range.value + "%)"; divider.style.left = range.value + "%"; };
    if (!range.hasAttribute("data-wired")) { range.addEventListener("input", clip); range.setAttribute("data-wired", ""); }
    clip();
    fig.querySelectorAll(".hat-sp-photo-year").forEach(function (s, k) { s.textContent = ys[k] === 1993 ? "1993 (black and white)" : "March " + ys[k]; });
    fig.querySelector(".hat-sp-photo-name").textContent = p.name;
  };

  function start() { document.querySelectorAll(".hat-sp").forEach(function (r) { new Picker(r); }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
