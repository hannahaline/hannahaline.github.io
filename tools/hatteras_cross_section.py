"""
Cross-section diagram of Hatteras Island for the stakeholder pages, from Pamlico Sound to the Atlantic.

    python tools/hatteras_cross_section.py

A schematic in the style of a textbook figure, not to scale: zones bracketed along the top (sound, marsh,
island interior, dune, beach, ocean), stippled sand, and outline symbols for marsh grass, shrubs,
maritime forest, beach houses on pilings, dune grass and NC-12 behind the dune. West on the left and
east on the right, as on the study-area map. Writes _includes/hatteras/cross_section.svg, an inline SVG
so it takes the page's font.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-02
"""
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "_includes/hatteras/cross_section.svg"

W, H = 1000, 380
SEA = 250                         # mean high water, svg y
TOP = 72                          # the drawing starts here; the zone brackets sit just below
INK, MUTED, LINE = "#2b2f31", "#5b6469", "#3a3f42"
WATER_TOP, WATER_DEEP = "#cfe0ec", "#9fbfd6"
GROUND, SAND = "#d9c89a", "#ecdfb9"
CANOPY, CANOPY_DARK, MARSH_C, GRASS_C = "#7d9467", "#5f7a4d", "#93a86c", "#7f9455"
ROOF, WALL = "#6b7378", "#f7f5f0"
ROAD, ROAD_LINE = "#3a3f42", "#ffd23f"

# The island surface, west to east (x, y); y grows downward. Vertical scale exaggerated.
SURFACE = [(0, 300), (90, 292), (170, 272), (205, 256), (250, 249), (300, 244), (360, 239), (430, 236),
           (500, 234), (555, 233), (588, 229), (618, 196), (646, 160), (666, 155), (688, 174), (712, 216),
           (740, 233), (790, 243), (830, 255), (900, 288), (1000, 336)]

# Zones bracketed along the top: (label, x0, x1)
ZONES = [("Pamlico Sound", 0, 202), ("Marsh", 206, 296), ("Island interior", 300, 588),
         ("Dune", 592, 712), ("Beach", 716, 828), ("Atlantic Ocean", 832, 1000)]


def smooth(pts):
    """Catmull-Rom through the points, as SVG cubic Beziers."""
    d = [f"M{pts[0][0]},{pts[0][1]}"]
    for i in range(len(pts) - 1):
        p0, p1, p2 = pts[max(i - 1, 0)], pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}")
    return " ".join(d)


def y_at(x):
    for (x0, y0), (x1, y1) in zip(SURFACE, SURFACE[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return SURFACE[-1][1]


def bracket(label, x0, x1, y=104):
    """A zone bracket: a thin bar with end ticks, its label centred above."""
    return (f'<path d="M{x0 + 2},{y + 6} V{y} H{x1 - 2} V{y + 6}" fill="none" stroke="{MUTED}" stroke-width="1"/>'
            f'<text x="{(x0 + x1) / 2}" y="{y - 7}" text-anchor="middle" class="xs-zone">{label}</text>')


def callout(x, y_feature, y_text, text):
    """A point label with a short leader down to the feature."""
    return (f'<line x1="{x}" y1="{y_text + 5}" x2="{x}" y2="{y_feature}" stroke="{MUTED}" stroke-width="0.8"/>'
            f'<circle cx="{x}" cy="{y_feature}" r="1.8" fill="{MUTED}"/>'
            f'<text x="{x}" y="{y_text}" text-anchor="middle" class="xs-callout">{text}</text>')


def stilt_house(x, w=30, h=17, legs=7, roof=10):
    """A beach house raised on pilings, outlined."""
    g = y_at(x + w / 2)
    base = g - legs
    piles = "".join(f'<line x1="{x + px}" y1="{base}" x2="{x + px}" y2="{g + 1}" stroke="{LINE}" stroke-width="1.1"/>'
                    for px in (3, w / 2, w - 3))
    return (piles +
            f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" fill="{WALL}" stroke="{LINE}" stroke-width="1"/>'
            f'<path d="M{x - 2.5},{base - h} L{x + w / 2},{base - h - roof} L{x + w + 2.5},{base - h} Z" '
            f'fill="{ROOF}" stroke="{LINE}" stroke-width="1" stroke-linejoin="round"/>'
            f'<rect x="{x + 5}" y="{base - h + 5}" width="6" height="6" fill="none" stroke="{LINE}" stroke-width="0.8"/>'
            f'<rect x="{x + w - 11}" y="{base - h + 5}" width="6" height="6" fill="none" stroke="{LINE}" stroke-width="0.8"/>')


def oak(x, s=1.0):
    """A wind-pruned maritime oak: short trunk, broad flat canopy."""
    g = y_at(x)
    t = 9 * s
    canopy = (f'M{x - 17 * s},{g - t} C{x - 22 * s},{g - t - 12 * s} {x - 6 * s},{g - t - 19 * s} {x + 2 * s},{g - t - 15 * s} '
              f'C{x + 10 * s},{g - t - 17 * s} {x + 17 * s},{g - t - 9 * s} {x + 13 * s},{g - t} Z')
    return (f'<path d="M{x},{g} L{x - 1.5 * s},{g - t}" stroke="{LINE}" stroke-width="{1.6 * s}"/>'
            f'<path d="{canopy}" fill="{CANOPY}" stroke="{CANOPY_DARK}" stroke-width="1"/>')


def shrub(x, s=1.0):
    g = y_at(x)
    return (f'<path d="M{x - 9 * s},{g} C{x - 10 * s},{g - 9 * s} {x + 10 * s},{g - 9 * s} {x + 9 * s},{g} Z" '
            f'fill="{CANOPY}" stroke="{CANOPY_DARK}" stroke-width="0.9"/>')


def tuft(x, h=9, colour=GRASS_C, n=5, spread=6):
    """Grass blades fanning from one point."""
    g = y_at(x)
    blades = []
    for k in range(n):
        dx = (k - (n - 1) / 2) * spread / (n - 1)
        blades.append(f'<path d="M{x},{g} Q{x + dx * 0.4},{g - h * 0.6} {x + dx},{g - h + abs(dx) * 0.5}" '
                      f'stroke="{colour}" stroke-width="1" fill="none" stroke-linecap="round"/>')
    return "".join(blades)


def main():
    surface = smooth(SURFACE)
    ground = surface + f" L{W},{H} L0,{H} Z"
    sand = (smooth([p for p in SURFACE if 588 <= p[0] <= 900]) +
            " C860,300 760,276 690,258 C650,248 615,240 588,229 Z")
    road_y = y_at(572)
    parts = [
        f'<svg viewBox="0 {TOP} {W} {H - TOP}" class="hat-xsection" role="img" aria-labelledby="xs-title xs-desc" '
        f'xmlns="http://www.w3.org/2000/svg">',
        '<title id="xs-title">Cross-section of Hatteras Island</title>',
        '<desc id="xs-desc">A schematic slice from Pamlico Sound in the west to the Atlantic Ocean in the east: '
        'marsh at the sound\'s edge, the island interior with maritime forest and a village of houses on pilings, '
        'NC-12 just behind the dune, the dune, the beach, and the ocean. Not to scale.</desc>',
        "<defs>",
        f'<linearGradient id="xs-water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WATER_TOP}"/>'
        f'<stop offset="1" stop-color="{WATER_DEEP}"/></linearGradient>',
        '<pattern id="xs-stipple" width="9" height="9" patternUnits="userSpaceOnUse">'
        '<circle cx="2" cy="2" r="0.7" fill="#a8925e"/><circle cx="6.5" cy="6" r="0.6" fill="#a8925e"/></pattern>',
        '<pattern id="xs-stipple-fine" width="7" height="7" patternUnits="userSpaceOnUse">'
        '<circle cx="1.5" cy="2" r="0.6" fill="#b89f62"/><circle cx="5" cy="5.5" r="0.55" fill="#b89f62"/></pattern>',
        "</defs>",
        # water, then ground over it, so water shows only where the bed is below mean high water
        f'<rect x="0" y="{SEA}" width="{W}" height="{H - SEA}" fill="url(#xs-water)"/>',
        f'<path d="{ground}" fill="{GROUND}"/>',
        f'<path d="{ground}" fill="url(#xs-stipple)"/>',
        f'<path d="{sand}" fill="{SAND}"/>',
        f'<path d="{sand}" fill="url(#xs-stipple-fine)"/>',
        f'<path d="{surface}" fill="none" stroke="{LINE}" stroke-width="1.3"/>',
        # mean high water
        f'<line x1="0" y1="{SEA}" x2="{W}" y2="{SEA}" stroke="#4f7a99" stroke-width="0.9" stroke-dasharray="6 4"/>',
        f'<text x="8" y="{SEA - 5}" class="xs-small">MHW</text>',
        # vegetation, village and road
        "".join(tuft(x, h=8, colour=MARSH_C, n=6, spread=5) for x in range(212, 298, 9)),
        "".join(shrub(x, s) for x, s in ((312, 0.9), (332, 1.1), (540, 1.0), (560, 0.8))),
        "".join(oak(x, s) for x, s in ((354, 1.0), (480, 1.15), (512, 0.95))),
        stilt_house(382), stilt_house(418, w=34, h=19), stilt_house(456, w=26, h=15),
        "".join(tuft(x, h=10) for x in (604, 620, 634, 650, 666, 680, 694)),
        f'<rect x="560" y="{road_y - 4}" width="26" height="5" fill="{ROAD}"/>',
        f'<line x1="563" y1="{road_y - 1.5}" x2="583" y2="{road_y - 1.5}" stroke="{ROAD_LINE}" stroke-width="1.2" '
        f'stroke-dasharray="4 3"/>',
        # labels: zone brackets along the top, callouts for the village and NC-12
        "".join(bracket(*z) for z in ZONES),
        callout(420, y_at(420) - 39, 168, "Village"),
        callout(573, road_y - 6, 186, "NC-12"),
        # direction and scale notes
        f'<text x="8" y="{H - 10}" class="xs-small">W</text>',
        f'<text x="{W - 8}" y="{H - 10}" text-anchor="end" class="xs-small">E</text>',
        f'<text x="{W / 2}" y="{H - 10}" text-anchor="middle" class="xs-small">Schematic; not to scale '
        f'(heights exaggerated)</text>',
        "</svg>",
    ]
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
