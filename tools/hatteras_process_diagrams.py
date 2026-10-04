"""
Two process diagrams for "How the island works" on the Hatteras stakeholder pages.

    python tools/hatteras_process_diagrams.py

longshore.svg: Hatteras Island from above (the OpenStreetMap coastline in tools/data/), waves from the northeast and
southeast, sand drifting south along the east-facing shore (arrow widths schematic, from the shoreline record) and
ending at Cape Point, with a close-up of the zig-zag path
sand takes up and down the beach face. overwash.svg: a slice across the island in a storm, the water level raised above normal
high tide, waves running over a low dune, and a new layer of sand (an overwash fan) spread across the island
toward the sound. groin.svg: a groin seen from above, sand piled on the side the drift comes from and the far
side cut back. dunes.svg: two slices in the same storm, after Sallenger's (2000) storm impact scale: collision, where
the run-up stays below a tall dune's crest and cuts its face, and overwash, where it tops a low one. Simplified, in the palette of the cross-section. Written to _includes/hatteras/
as inline SVGs so they take the page's font.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import math
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
OUTLINE = SITE / "tools/data/hatteras_outline_osm.json"
OUT = SITE / "_includes/hatteras"

INK, MUTED = "#2b2f31", "#5b6469"
WATER_TOP, WATER_DEEP = "#cfe0ec", "#9fbfd6"
GROUND, SAND, SAND_NEW = "#d9c89a", "#ecdfb9", "#f6e3b8"
CANOPY, GRASS_C = "#7d9467", "#7f9455"
ADDED, ERODE = "#c8880f", "#b2182b"     # house ADDED and the RdBu red
ARROW = "#1a1a1a"


def head(id_, color=ARROW):
    return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')


def label(x, y, text, anchor="start", size=15, color=INK, weight=400, box=False):
    """Plain text at (x, y), journal style: no box, a thin white halo so it reads over any fill. box is ignored and
    kept only so older calls still run."""
    lines = text.split("\n")
    spans = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else 1.2}em">{t}</tspan>' for i, t in enumerate(lines))
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}" font-weight="{weight}" '
            f'paint-order="stroke" stroke="#fff" stroke-width="3" stroke-opacity="0.85" stroke-linejoin="round">'
            f'{spans}</text>')


def svg_open(cls, w, h, title, desc):
    return [f'<svg class="hat-process {cls}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{cls}-t {cls}-d" '
            f'xmlns="http://www.w3.org/2000/svg">', f'<title id="{cls}-t">{title}</title>', f'<desc id="{cls}-d">{desc}</desc>']


def svg_close(s, w, h):
    """The thin black frame of a journal figure panel, then close."""
    s.append(f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" fill="none" stroke="#1a1a1a" stroke-width="1.5"/>')
    s.append("</svg>")
    return "\n".join(s) + "\n"


def island_outline():
    """Hatteras Island (Hatteras Inlet to Oregon Inlet) as [(lon, lat)]: the OpenStreetMap coastline
    (natural=coastline, fetched 2026-10-03 through the Overpass API, polygonized, largest piece, simplified to
    ~0.001 deg). © OpenStreetMap contributors, ODbL; the page caption carries the credit."""
    import json
    return json.loads(OUTLINE.read_text(encoding="utf-8"))


def longshore():
    W, H = 1000, 660
    s = svg_open("longshore", W, H, "Waves move sand along the coast",
                 "A map of Hatteras Island from Oregon Inlet south to Cape Point and west to Hatteras Inlet. Waves arrive "
                 "from the northeast and from the southeast. Along the east-facing shore, sand drifts south, more of it "
                 "where the beach is eroding, and the drift ends at Cape Point, where the sand builds up. A close-up shows how each wave "
                 "pushes sand up the beach at an angle and it slides straight back down, so the sand creeps along the shore.")
    s.append(f'<defs>{head("ls-h")}<marker id="ls-hd" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="2.6" '
             f'markerHeight="2.6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ADDED}"/></marker>'
             f'<linearGradient id="ls-sea" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{WATER_TOP}"/>'
             f'<stop offset="1" stop-color="{WATER_DEEP}"/></linearGradient></defs>')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{WATER_TOP}"/>')

    # map frame: lon/lat to svg, equal-area at this latitude
    LON0, LAT1, PX_PER_KM = -75.80, 35.83, 8.4
    kx = 111.32 * math.cos(math.radians(35.5))
    def xy(lon, lat):
        return 300 + (lon - LON0) * kx * PX_PER_KM, 16 + (LAT1 - lat) * 110.57 * PX_PER_KM
    ring = [xy(lon, lat) for lon, lat in island_outline()]
    s.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in ring) + f' Z" fill="{SAND}" stroke="{SAND}" '
             'stroke-width="3" stroke-linejoin="round"/>')

    from shapely.geometry import LineString, Polygon
    poly = Polygon(ring)

    def east_shore(lat):  # where a line at this latitude leaves the island on the ocean side
        y = xy(LON0, lat)[1]
        return poly.intersection(LineString([(0, y), (W, y)])).bounds[2], y

    def south_shore(x):   # where a line at this x leaves the island on the south side
        return x, poly.intersection(LineString([(x, 0), (x, H)])).bounds[3]

    cape = max((p for p in ring if p[0] > xy(-75.60, 35.5)[0]), key=lambda p: p[1])  # Cape Point: southernmost east of Frisco

    # waves from the northeast (heading south-west) and from the southeast (heading north-west): crests and arrows
    def wave_field(cx, cy, heading_deg, n=4, half=60, gap=22):
        h = math.radians(heading_deg)                     # direction of travel, svg frame (y down)
        tx, ty = math.cos(h), math.sin(h)
        nx, ny = -ty, tx                                 # along the crest
        for k in range(n):
            ox, oy = cx - tx * gap * k, cy - ty * gap * k
            s.append(f'<line x1="{ox - nx * half:.0f}" y1="{oy - ny * half:.0f}" x2="{ox + nx * half:.0f}" '
                     f'y2="{oy + ny * half:.0f}" stroke="#fff" stroke-width="3" stroke-linecap="round" '
                     f'opacity="{0.95 - 0.15 * k:.2f}"/>')
        s.append(f'<line x1="{cx - tx * gap * (n + 1):.0f}" y1="{cy - ty * gap * (n + 1):.0f}" x2="{cx + tx * 30:.0f}" '
                 f'y2="{cy + ty * 30:.0f}" stroke="{ARROW}" stroke-width="1.8" marker-end="url(#ls-h)"/>')
    wave_field(720, 230, 135)        # from the north-east, travelling south-west
    s.append(label(770, 110, "waves from\nthe northeast", size=15))
    wave_field(840, 520, 225)        # from the south-east, travelling north-west
    s.append(label(850, 600, "waves from\nthe southeast", size=15))

    # drift along the east-facing shore: south, toward the cape. Widths are schematic, read from the shoreline
    # record: the drift grows where the beach erodes (Pea Island, Rodanthe: more sand leaves than arrives),
    # holds where it is steady (Salvo to Avon), grows again toward Buxton, and ends at Cape Point, where sand is laid down
    DRIFT = [(35.765, 3.0), (35.69, 4.5), (35.615, 6.0), (35.54, 7.0), (35.465, 7.0), (35.39, 7.0), (35.315, 9.0)]
    for lat, w in DRIFT:
        x0, y0 = east_shore(lat)
        x1, y1 = east_shore(lat - 0.055)
        s.append(f'<line x1="{x0 + 26:.0f}" y1="{y0:.0f}" x2="{x1 + 26:.0f}" y2="{y1:.0f}" stroke="{ADDED}" '
                 f'stroke-width="{w}" marker-end="url(#ls-hd)"/>')
    xs, ys = east_shore(35.50)
    s.append(label(xs + 50, ys + 4, "sand drifts south;\nthicker arrow = more sand", size=15))

    s.append(label(cape[0] + 30, cape[1] + 40, "the drift ends at Cape Point,\nwhere sand builds up", size=15))

    # places
    for name, lon, lat, dx, anchor in (("Oregon Inlet", -75.53, 35.79, -14, "end"), ("Rodanthe", -75.47, 35.59, -16, "end"),
                                       ("Avon", -75.51, 35.35, -16, "end"), ("Buxton", -75.53, 35.27, -16, "end"),
                                       ("Hatteras Inlet", -75.74, 35.19, 0, "end")):
        x, y = xy(lon, lat)
        s.append(label(x + dx, y + (30 if name == "Hatteras Inlet" else 5), name, anchor=anchor, size=14, color=INK, box=False,
                       weight=600))
    s.append(label(30, 40, "Pamlico Sound", size=16, color=MUTED, box=False))
    s.append(label(W - 20, 40, "Atlantic Ocean", anchor="end", size=16, color=MUTED, box=False))

    # close-up: the zig-zag that moves each grain
    bx, by, bw, bh = 24, 300, 250, 210
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#fff" fill-opacity="0.95" stroke="#1a1a1a" stroke-width="1"/>')
    s.append(f'<rect x="{bx + 10}" y="{by + 34}" width="{bw - 20}" height="70" fill="{SAND}"/>')
    s.append(f'<rect x="{bx + 10}" y="{by + 104}" width="{bw - 20}" height="66" fill="{WATER_TOP}"/>')
    zz, x = [], bx + 22
    while x < bx + bw - 50:
        zz.append(f"M{x},{by + 98} L{x + 26},{by + 54} L{x + 26},{by + 98}")
        x += 30
    s.append(f'<path d="{" ".join(zz)}" stroke="{ADDED}" stroke-width="2" fill="none" stroke-linejoin="round"/>')
    for k in range(3):
        s.append(f'<line x1="{bx + 30 + k * 60}" y1="{by + 166}" x2="{bx + 90 + k * 60}" y2="{by + 112}" stroke="#fff" '
                 f'stroke-width="2.5" stroke-linecap="round"/>')
    s.append(label(bx + 12, by + 22, "Close-up of the beach", size=14, color=INK, weight=600, box=False))
    s.append(label(bx + 12, by + 190, "each wave pushes sand up the beach at\nan angle; it slides straight back down",
                   size=12, color=MUTED, box=False))
    return svg_close(s, W, H)


def overwash():
    W, H = 1000, 360
    s = svg_open("overwash", W, H, "Storms move sand across the island",
                 "A slice across the island in a storm, sound on the left and ocean on the right. The water is raised "
                 "well above normal high tide, and waves run over a low dune. The sand they carry is laid down as a new "
                 "layer, an overwash fan, across the island interior and toward the sound.")
    s.append(f'<defs>{head("ow-h")}<linearGradient id="ow-sea" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{WATER_TOP}"/><stop offset="1" stop-color="{WATER_DEEP}"/></linearGradient>'
             '<pattern id="ow-dots" width="7" height="7" patternUnits="userSpaceOnUse">'
             f'<circle cx="2" cy="2" r="1" fill="{ADDED}" opacity="0.7"/></pattern></defs>')

    HT, STORM, SOUND = 252, 218, 246              # normal high tide, storm water level, the sound (svg y)
    ground = [(0, 266), (80, 258), (140, 242), (200, 214), (260, 197), (360, 191), (460, 189), (560, 187),
              (620, 180), (660, 158), (700, 142), (735, 152), (765, 186), (820, 222), (900, 254), (1000, 292)]

    def gy(x):
        for (x0, y0), (x1, y1) in zip(ground, ground[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return ground[-1][1]
    gpath = "M" + " L".join(f"{x},{y}" for x, y in ground) + f" L{W},{H} L0,{H} Z"

    # water: the sound a little up on the left, the ocean at the storm level on the right
    s.append(f'<rect x="0" y="{SOUND}" width="420" height="{H - SOUND}" fill="{WATER_TOP}"/>')
    s.append(f'<rect x="600" y="{STORM}" width="{W - 600}" height="{H - STORM}" fill="{WATER_TOP}"/>')
    s.append(f'<path d="{gpath}" fill="{SAND}" stroke="{GROUND}" stroke-width="1.5"/>')
    # the island interior: vegetation on the old surface
    for x in range(250, 620, 34):
        s.append(f'<ellipse cx="{x}" cy="{gy(x) - 8:.0f}" rx="15" ry="9" fill="{CANOPY}" opacity="0.85"/>')
    # the overwash fan: a new sand layer from the dune back across the interior, thinning toward the sound
    xs = list(range(700, 219, -20))
    top = [(x, gy(x) - (2 + 12 * (x - 220) / 480)) for x in xs]
    bottom = [(x, gy(x)) for x in reversed(xs)]
    fpath = "M" + " L".join(f"{x},{y:.0f}" for x, y in top + bottom) + " Z"
    s.append(f'<path d="{fpath}" fill="{SAND_NEW}" stroke="{ADDED}" stroke-width="1.5"/>')
    s.append(f'<path d="{fpath}" fill="url(#ow-dots)"/>')

    # water levels, on the ocean side
    s.append(f'<line x1="790" y1="{HT}" x2="{W}" y2="{HT}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="6 5"/>')
    s.append(label(W - 12, HT + 24, "normal high tide", anchor="end", size=14, color=MUTED, box=False))
    s.append(f'<line x1="770" y1="{STORM}" x2="{W}" y2="{STORM}" stroke="#2166ac" stroke-width="2"/>')
    s.append(label(W - 46, STORM + 21, "storm water level, raised by surge", anchor="end", size=15, color="#2166ac"))
    s.append(f'<line x1="975" y1="{HT - 2}" x2="975" y2="{STORM + 6}" stroke="#2166ac" stroke-width="2" marker-end="url(#ow-h)"/>')

    # waves running up the beach, over the dune, and on across the island
    s.append(f'<path d="M995,{STORM - 3} C860,{STORM - 30} 760,90 690,110 S520,150 430,166" stroke="{ARROW}" '
             f'stroke-width="2" fill="none" marker-end="url(#ow-h)"/>')
    s.append(label(560, 76, "storm waves run over the dune,\ncarrying sand inland", anchor="middle"))
    s.append(label(400, 236, "overwash fan: a new layer of sand on the island", anchor="middle", size=15))
    s.append(label(14, 40, "Pamlico Sound", size=15, color=MUTED, box=False))
    s.append(label(W - 14, 40, "Atlantic Ocean", anchor="end", size=15, color=MUTED, box=False))
    return svg_close(s, W, H)


def groin():
    W, H = 1000, 460
    s = svg_open("groin", W, H, "How a groin traps sand",
                 "A beach seen from above, land at the top and ocean below, with sand drifting along the shore from left "
                 "to right. A groin, a short wall, runs from the beach out into the surf. On the left, the side the sand "
                 "comes from, sand piles up against the groin and the beach is wider. On the right, the far side, the "
                 "beach is cut off from that sand, so it is narrower and erodes.")
    s.append(f'<defs>{head("gr-h")}<marker id="gr-hd" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="2.6" '
             f'markerHeight="2.6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ADDED}"/></marker>'
             f'<linearGradient id="gr-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WATER_TOP}"/>'
             f'<stop offset="1" stop-color="{WATER_DEEP}"/></linearGradient></defs>')
    GX = 500                                    # the groin
    base = 220                                  # the shoreline far from the groin

    def shore(x):
        if x <= GX:                             # updrift: builds out toward the groin
            return base + 70 * math.exp(-(GX - x) / 150)
        return base - 55 * math.exp(-(x - GX) / 170)   # downdrift: cut back next to the groin

    pts = [(x, shore(x)) for x in range(0, GX + 1, 10)] + [(x, shore(x)) for x in range(GX, W + 1, 10)]
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{WATER_TOP}"/>')
    s.append('<path d="M0,0 H{W} V{y} '.format(W=W, y=pts[-1][1]) + " ".join(f"L{x},{y:.1f}" for x, y in reversed(pts))
             + f' Z" fill="{SAND}"/>')
    s.append(f'<rect x="0" y="0" width="{W}" height="64" fill="{GROUND}"/>')
    s.append(f'<rect x="0" y="0" width="{W}" height="30" fill="{CANOPY}"/>')
    # the original shoreline, dashed, for comparison
    s.append(f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="7 6"/>')
    s.append(label(W - 14, base - 10, "shoreline without the groin", anchor="end", size=14, color=MUTED, box=False))
    # surf along the new shoreline
    s.append('<path d="M' + " L".join(f"{x},{y + 4:.1f}" for x, y in pts) + '" stroke="#fff" stroke-width="5" '
             'fill="none" opacity="0.85" stroke-linecap="round"/>')
    # the groin: a rock wall from the dunes' toe out past the surf
    s.append(f'<rect x="{GX - 9}" y="120" width="18" height="{shore(GX - 1) - 120 + 110:.0f}" rx="4" fill="#8a8f93" '
             f'stroke="#5b6469" stroke-width="2"/>')
    for y in range(128, int(shore(GX - 1) + 100), 16):
        s.append(f'<circle cx="{GX - 3 + (y % 3)}" cy="{y}" r="4" fill="#a3a8ab" stroke="#6b7378" stroke-width="1"/>')
    s.append(label(GX + 20, 112, "groin", size=17, weight=600))
    # longshore drift: arriving from the left, stopped at the groin; little passes to the right
    s.append(f'<line x1="60" y1="{base + 62}" x2="{GX - 40}" y2="{base + 62}" stroke="{ADDED}" stroke-width="9" '
             f'marker-end="url(#gr-hd)"/>')
    s.append(f'<line x1="{GX + 40}" y1="{base + 40}" x2="{W - 80}" y2="{base + 40}" stroke="{ADDED}" stroke-width="3" '
             f'marker-end="url(#gr-hd)" stroke-dasharray="10 6"/>')
    s.append(label(60, base + 104, "sand drifting along the shore", size=15))
    s.append(label(GX + 40, base + 84, "little sand gets past", size=15))
    # what happens on each side
    s.append(label(70, 150, "sand piles up:\nthe beach grows wider", size=16, color="#2166ac"))
    s.append(label(W - 60, 150, "cut off from the sand:\nthe beach erodes", anchor="end", size=16, color=ERODE))
    s.append(label(14, H - 16, "Atlantic Ocean", size=15, color=MUTED, box=False))
    return svg_close(s, W, H)


def dunes():
    W, H = 1000, 350
    PW = 490                                     # each panel's width; panel b starts at W - PW
    s = svg_open("dunes", W, H, "Dunes are the island's first defence",
                 "Two slices across the island, sound on the left and ocean on the right, in the same storm. "
                 "(a) Collision: the highest reach of the waves stays below a tall dune's crest. The waves cut into the "
                 "front of the dune and carry that sand offshore, and the island behind stays dry. (b) Overwash: the waves "
                 "reach higher than a low dune's crest, run over it, and leave a layer of sand across the island and the road.")
    s.append(f'<defs>{head("du-h")}<pattern id="du-dots" width="6" height="6" patternUnits="userSpaceOnUse">'
             f'<circle cx="2" cy="2" r="0.9" fill="{ADDED}"/></pattern>'
             f'<pattern id="du-cut" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             f'<line x1="0" y1="0" x2="0" y2="6" stroke="{ERODE}" stroke-width="1.1"/></pattern></defs>')
    MSL, SURGE, TOE = 268, 238, 226              # y of mean sea level, storm water level, the dune's landward toe

    def ground(crest, cut=None):
        """Profile from the sound (x 0) to the ocean (x PW). cut: the x of a scarp cut into the dune's seaward face."""
        g = [(0, 300), (40, 284), (80, 262), (130, 244), (200, 236), (260, TOE)]
        face = [(282, TOE - 6), (304, (TOE + crest) / 2), (322, crest + 5), (333, crest), (346, crest + 6),
                (360, (crest + 222) / 2 + 4), (374, 222)]
        if cut is not None:                      # crest kept, face cut back to a near-vertical scarp
            face = [p for p in face if p[0] < cut] + [(cut, crest + 18), (cut + 4, 216), (378, 222)]
        return g + face + [(402, 238), (426, MSL), (PW, 322)]

    def path(pts, x0):
        return "M" + " L".join(f"{x0 + x:.1f},{y:.1f}" for x, y in pts)

    def level(x0, xa, xb, y, text, dash, color, side="end", below=False):
        s.append(f'<line x1="{x0 + xa}" y1="{y}" x2="{x0 + xb}" y2="{y}" stroke="{color}" stroke-width="1.3" '
                 f'stroke-dasharray="{dash}"/>')
        s.append(label(x0 + (xb - 4 if side == "end" else xa + 4), y + 15 if below else y - 5, text, anchor=side, size=12.5, color=color))

    def panel(x0, crest, runup, tag, title, over):
        pre = ground(crest)
        post = ground(crest, cut=None if over else 352)
        # water: open ocean and sound below mean sea level, the storm's raised water on the ocean side only
        s.append(f'<rect x="{x0}" y="{MSL}" width="{PW}" height="{H - MSL}" fill="{WATER_DEEP}"/>')
        s.append(f'<rect x="{x0 + 340}" y="{SURGE}" width="{PW - 340}" height="{MSL - SURGE}" fill="{WATER_TOP}"/>')
        s.append(f'<path d="{path(post, x0)} L{x0 + PW},{H} L{x0},{H} Z" fill="{SAND}" stroke="#a8925e" stroke-width="1.6"/>')
        # the road on the island interior
        s.append(f'<rect x="{x0 + 214}" y="{233.5}" width="26" height="3.5" fill="#4a4f52"/>')
        s.append(label(x0 + 227, 256, "NC-12", anchor="middle", size=12, color=MUTED))
        if over:
            deposit = [(345, crest + 6), (333, crest - 3), (300, TOE - 18), (262, TOE - 7), (200, 230), (150, 239)]
            under = [(150, 242), (200, 236), (260, TOE), (282, TOE - 6), (304, (TOE + crest) / 2), (322, crest + 5), (333, crest)]
            d = path(deposit + under, x0) + " Z"
            s.append(f'<path d="{d}" fill="{SAND_NEW}" stroke="{ADDED}" stroke-width="1.2"/><path d="{d}" fill="url(#du-dots)"/>')
            s.append(f'<path d="M{x0 + 470},{SURGE - 10} C{x0 + 420},{runup - 4} {x0 + 360},{runup - 12} {x0 + 318},{runup - 4} '
                     f'S{x0 + 230},{TOE - 30} {x0 + 178},{TOE - 4}" stroke="{ARROW}" stroke-width="1.8" fill="none" marker-end="url(#du-h)"/>')
            s.append(label(x0 + 40, 226, "overwash deposit", size=12.5, color="#8a5d06"))
        else:
            # the sand cut from the dune face (hatched), shown against the pre-storm outline, and carried offshore
            cutzone = [p for p in pre if 340 <= p[0] <= 378]
            s.append(f'<path d="{path([(352, crest + 18)] + [p for p in cutzone if p[0] > 352] + [(378, 222), (356, 216)], x0)} Z" '
                     f'fill="url(#du-cut)" stroke="none"/>')
            s.append(f'<path d="{path([p for p in pre if 333 <= p[0] <= 378], x0)}" fill="none" stroke="{ERODE}" '
                     f'stroke-width="1.2" stroke-dasharray="4 3"/>')
            s.append(f'<path d="M{x0 + 470},{SURGE - 12} C{x0 + 430},{SURGE - 34} {x0 + 395},{runup - 4} {x0 + 362},{runup + 4}" '
                     f'stroke="{ARROW}" stroke-width="1.8" fill="none" marker-end="url(#du-h)"/>')
            s.append(f'<path d="M{x0 + 380},{226} Q{x0 + 402},{262} {x0 + 432},{290}" stroke="{ERODE}" stroke-width="1.5" '
                     f'fill="none" marker-end="url(#du-r)"/>')
            s.append(label(x0 + PW - 10, 312, "sand moved offshore", anchor="end", size=12.5, color=ERODE))
        # levels: the dune crest and the highest reach of the waves (run-up)
        level(x0, 120, 333, crest, "dune crest", "1.5 3", INK, side="start")
        level(x0, 290 if over else 352, PW, runup, "highest wave run-up", "6 3", "#2166ac", below=over)
        level(x0, 400, PW, SURGE, "storm water level", "none", "#2166ac")
        level(x0, 0, 120, MSL, "mean sea level", "2 3", MUTED, side="start")
        s.append(label(x0 + 12, 314, "Sound", size=13, color=MUTED))
        s.append(label(x0 + PW - 12, 338, "Ocean", anchor="end", size=13, color=MUTED))
        s.append(label(x0 + 12, 26, tag, size=15, weight=700))
        s.append(label(x0 + 40, 26, title, size=14.5))
        s.append(f'<rect x="{x0 + 0.75}" y="0.75" width="{PW - 1.5}" height="{H - 1.5}" fill="none" stroke="#1a1a1a" stroke-width="1.5"/>')

    s[-1] = s[-1].replace("</defs>", f'<marker id="du-r" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
                                      f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ERODE}"/></marker></defs>')
    panel(0, 112, 170, "(a)", "Collision: run-up stays below the crest", over=False)
    panel(W - PW, 196, 176, "(b)", "Overwash: run-up overtops the crest", over=True)
    s.append("</svg>")
    return "\n".join(s) + "\n"


def main():
    for name, make in (("longshore.svg", longshore), ("overwash.svg", overwash), ("groin.svg", groin), ("dunes.svg", dunes)):
        (OUT / name).write_text(make(), encoding="utf-8")
        print(f"wrote {OUT / name}")


if __name__ == "__main__":
    main()
