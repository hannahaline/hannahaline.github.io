"""
The overwash diagram for "How the island works" on the Hatteras stakeholder pages.

    python tools/hatteras_process_diagrams.py

overwash.svg: a slice across the island in a storm, the water level raised above normal high tide, waves running
over a low dune, and a new layer of sand (an overwash fan) spread across the island toward the sound. Simplified, in
the palette of the cross-section. Written to _includes/hatteras/ as an inline SVG so it takes the page's font. The
longshore, groin and dune diagrams it also drew were replaced by photos and figures and removed (2026-10-04).

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-04
"""
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
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


def main():
    for name, make in (("overwash.svg", overwash),):
        (OUT / name).write_text(make(), encoding="utf-8")
        print(f"wrote {OUT / name}")


if __name__ == "__main__":
    main()
