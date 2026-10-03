"""
Cross-section diagram of Hatteras Island for the stakeholder pages, from Pamlico Sound to the Atlantic.

    python tools/hatteras_cross_section.py

A schematic, not to scale: sound, marsh, island interior with a village, NC-12 behind the dune, dune,
beach, ocean and shoreface, west on the left and east on the right as on the study-area map.
Writes _includes/hatteras/cross_section.svg, an inline SVG so it takes the page's font.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-02
"""
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "_includes/hatteras/cross_section.svg"

W, H = 1000, 400
SEA = 262                    # mean sea level, svg y
INK, MUTED = "#1a1a1a", "#5b6469"
WATER = "#a8c8e0"                                # house WATER
GROUND, SAND = "#cdb26f", "#efdcab"              # house PROFILE_GROUND, beach sand
MARSH, SCRUB = "#8fa86a", "#6f8a55"
ROAD, ROAD_LINE = "#3a3f42", "#ffd23f"

# The island surface, west to east (x, y); y grows downward
SURFACE = [(0, 318), (90, 306), (170, 284), (205, 266), (250, 259), (300, 252), (360, 246), (430, 243),
           (500, 241), (555, 240), (590, 236), (620, 205), (648, 168), (668, 162), (690, 182), (712, 226),
           (740, 244), (790, 254), (830, 266), (900, 300), (1000, 352)]


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


def label(x, y_text, y_point, text, sub=None, anchor="middle"):
    """A label above the profile with a thin leader down to the feature."""
    out = [f'<line x1="{x}" y1="{y_text + 8}" x2="{x}" y2="{y_point - 4}" stroke="{MUTED}" stroke-width="1"/>',
           f'<text x="{x}" y="{y_text}" text-anchor="{anchor}" class="xs-label">{text}</text>']
    if sub:
        out.append(f'<text x="{x}" y="{y_text - 17}" text-anchor="{anchor}" class="xs-sub">{sub}</text>')
    return "\n".join(out)


def house(x, w=26, h=18):
    """A village house standing on the ground at x."""
    g = y_at(x + w / 2)
    return (f'<rect x="{x}" y="{g - h}" width="{w}" height="{h}" fill="#f4f1ea" stroke="{INK}" stroke-width="1.2"/>'
            f'<path d="M{x - 3},{g - h} L{x + w / 2},{g - h - 12} L{x + w + 3},{g - h} Z" fill="#9b5d4a" '
            f'stroke="{INK}" stroke-width="1.2"/>'
            f'<rect x="{x + w / 2 - 3}" y="{g - 9}" width="6" height="9" fill="{INK}"/>')


def shrub(x, r=9):
    g = y_at(x)
    return f'<ellipse cx="{x}" cy="{g - r * 0.7}" rx="{r * 1.3}" ry="{r}" fill="{SCRUB}"/>'


def grass(x, n=4, h=12, colour=MARSH):
    g = y_at(x)
    return "".join(f'<path d="M{x + k * 4},{g} q{-2 + k},{-h / 2} {-1 + k * 0.8},{-h - (k % 2) * 3}" '
                   f'stroke="{colour}" stroke-width="1.6" fill="none"/>' for k in range(n))


def main():
    ground = smooth(SURFACE) + f" L{W},{H} L0,{H} Z"
    parts = [
        f'<svg viewBox="0 0 {W} {H}" class="hat-xsection" role="img" '
        f'aria-labelledby="xs-title xs-desc" xmlns="http://www.w3.org/2000/svg">',
        '<title id="xs-title">Cross-section of Hatteras Island</title>',
        '<desc id="xs-desc">From Pamlico Sound in the west to the Atlantic Ocean in the east: marsh at the sound\'s '
        'edge, the island interior where the villages sit, NC-12 just behind the dune, the dune, the beach, and the '
        'ocean. Not to scale.</desc>',
        # water fills to sea level; the ground drawn over it leaves water only where the bed is below sea level
        f'<rect x="0" y="{SEA}" width="{W}" height="{H - SEA}" fill="{WATER}"/>',
        f'<path d="{ground}" fill="{GROUND}"/>',
        # the dune and beach sand, a lens on the ground from behind the dune to below the waterline
        f'<path d="{smooth([p for p in SURFACE if 590 <= p[0] <= 900])} '
        f'C860,312 760,292 690,272 C650,262 615,250 590,236 Z" fill="{SAND}"/>',
        f'<path d="{smooth(SURFACE)}" fill="none" stroke="#8a7440" stroke-width="1.2"/>',
        # waves
        "".join(f'<path d="M{x},{SEA} q8,-7 16,0 q8,7 16,0" stroke="#ffffff" stroke-width="1.6" fill="none"/>'
                for x in range(830, 990, 40)),
        # mean sea level
        f'<line x1="0" y1="{SEA}" x2="{W}" y2="{SEA}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 4"/>',
        f'<text x="{W - 8}" y="{SEA + 18}" text-anchor="end" class="xs-small">mean sea level</text>',
        # marsh, scrub and village
        "".join(grass(x) for x in range(222, 300, 13)),
        "".join(shrub(x) for x in (318, 344, 476, 500, 528)),
        house(372), house(408, w=30, h=20), house(446),
        "".join(grass(x, n=3, h=10, colour="#7d9a4d") for x in (632, 655, 676, 696)),
        # NC-12 on the interior, just behind the dune
        f'<rect x="560" y="{y_at(575) - 5}" width="30" height="6" fill="{ROAD}"/>',
        f'<line x1="563" y1="{y_at(575) - 2}" x2="587" y2="{y_at(575) - 2}" stroke="{ROAD_LINE}" '
        f'stroke-width="1.4" stroke-dasharray="5 3"/>',
        # labels
        label(95, 120, SEA, "Pamlico Sound"),
        label(258, 162, y_at(258) - 10, "Marsh"),
        label(420, 92, y_at(420) - 34, "Village", sub="Island interior"),
        label(575, 132, y_at(575) - 7, "NC-12"),
        label(660, 72, 160, "Dune"),
        label(755, 132, y_at(755) - 2, "Beach"),
        label(915, 120, SEA - 10, "Atlantic Ocean"),
        f'<text x="12" y="{H - 12}" class="xs-small">West</text>',
        f'<text x="{W - 12}" y="{H - 12}" text-anchor="end" class="xs-small">East</text>',
        f'<text x="{W / 2}" y="{H - 12}" text-anchor="middle" class="xs-small">Not to scale</text>',
        "</svg>",
    ]
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
