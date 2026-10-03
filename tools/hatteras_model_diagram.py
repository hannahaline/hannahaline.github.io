"""
"How the model works" diagram for the Hatteras stakeholder pages (The model).

    python tools/hatteras_model_diagram.py

A schematic plan view, not to scale: three neighbouring 500 m stretches of island seen from above, ocean at the
bottom and Pamlico Sound at the top, with numbered badges for the four parts the page lists underneath
(1 the starting island on a 10 m lidar grid, 2 storms and overwash, 3 sand moved along the shore between
stretches, 4 people: nourishment, rebuilt dunes, the road). Same palette as the cross-section. Writes
_includes/hatteras/model_diagram.svg, an inline SVG so it takes the page's font.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "_includes/hatteras/model_diagram.svg"

W, H = 1000, 560
INK, MUTED = "#2b2f31", "#5b6469"
WATER_TOP, WATER_DEEP = "#cfe0ec", "#9fbfd6"
GROUND, SAND, SAND_ADDED = "#d9c89a", "#ecdfb9", "#f6e3b8"
CANOPY, MARSH_C, GRASS_C = "#7d9467", "#93a86c", "#7f9455"
ROAD, ROAD_LINE = "#3a3f42", "#ffd23f"
BADGE = "#2f7f93"           # site teal
ARROW = "#1a1a1a"
FILL_EDGE = "#c8880f"       # house ADDED

X0, X1 = 70, 930            # island ends (fading out at both sides)
B1, B2 = 357, 643           # stretch boundaries: three stretches
Y_SOUND, Y_MARSH, Y_ROAD, Y_DUNE, Y_BEACH, Y_SURF = 96, 140, 238, 286, 330, 392


def badge(x, y, n):
    return (f'<circle cx="{x}" cy="{y}" r="15" fill="{BADGE}" stroke="#fff" stroke-width="2"/>'
            f'<text x="{x}" y="{y + 5.5}" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">{n}</text>')


def label(x, y, text, anchor="start", size=14, color=INK, weight=400, box=False):
    """Text at (x, y); box=True sets it on a white rounded box (for labels over the island)."""
    lines = text.split("\n")
    spans = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else 1.2}em">{t}</tspan>' for i, t in enumerate(lines))
    out = ""
    if box:
        w = max(len(t) for t in lines) * size * 0.53 + 14
        h = len(lines) * size * 1.2 + 8
        bx = x - 7 if anchor == "start" else x - w / 2 if anchor == "middle" else x - w + 7
        out = f'<rect x="{bx:.0f}" y="{y - size - 1:.0f}" width="{w:.0f}" height="{h:.0f}" rx="5" fill="#fff" fill-opacity="0.92"/>'
    return out + (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}" '
                  f'font-weight="{weight}">{spans}</text>')


def arrow(x0, y0, x1, y1, w=2.6, color=ARROW, head=9):
    return (f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{color}" stroke-width="{w}" '
            f'marker-end="url(#md-head)"/>')


def main():
    s = [f'<svg class="hat-model-diagram" viewBox="0 0 {W} {H}" role="img" '
         f'aria-labelledby="md-title md-desc" xmlns="http://www.w3.org/2000/svg">',
         '<title id="md-title">How the model works</title>',
         '<desc id="md-desc">Three neighbouring stretches of island seen from above, ocean at the bottom and the '
         'sound at the top. 1: each stretch starts from lidar elevation on a 10 metre grid. 2: storms push water '
         'and sand over a low dune and inland. 3: waves carry sand along the beach from one stretch to the next. '
         '4: people add sand to the beach, rebuild the dunes, and protect or move the road.</desc>',
         '<defs><marker id="md-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
         f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ARROW}"/></marker>',
         f'<linearGradient id="md-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WATER_TOP}"/>'
         f'<stop offset="1" stop-color="{WATER_DEEP}"/></linearGradient>',
         f'<linearGradient id="md-fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="1"/>'
         f'<stop offset="0.07" stop-color="#fff" stop-opacity="0"/><stop offset="0.93" stop-color="#fff" stop-opacity="0"/>'
         f'<stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>',
         '<pattern id="md-grid" width="12" height="12" patternUnits="userSpaceOnUse">'
         '<path d="M12,0 L0,0 0,12" fill="none" stroke="#ffffff" stroke-width="0.8" opacity="0.7"/></pattern>',
         '</defs>']

    # water: sound above, ocean below
    s.append(f'<rect x="0" y="40" width="{W}" height="{Y_MARSH - 40}" fill="{WATER_TOP}"/>')
    s.append(f'<rect x="0" y="{Y_BEACH}" width="{W}" height="{H - Y_BEACH - 40}" fill="url(#md-sea)"/>')
    # island bands, sound side to ocean side
    s.append(f'<rect x="{X0}" y="{Y_MARSH - 14}" width="{X1 - X0}" height="18" fill="{MARSH_C}"/>')
    s.append(f'<rect x="{X0}" y="{Y_MARSH}" width="{X1 - X0}" height="{Y_DUNE - Y_MARSH}" fill="{CANOPY}"/>')
    s.append(f'<rect x="{X0}" y="{Y_DUNE}" width="{X1 - X0}" height="24" fill="{GROUND}"/>')
    s.append(f'<rect x="{X0}" y="{Y_DUNE + 24}" width="{X1 - X0}" height="{Y_SURF - Y_DUNE - 24}" fill="{SAND}"/>')
    # dune grass ticks
    for x in range(X0 + 6, X1 - 4, 11):
        s.append(f'<path d="M{x},{Y_DUNE + 20} l2,-9 M{x + 4},{Y_DUNE + 20} l-1,-8" stroke="{GRASS_C}" stroke-width="1.4" fill="none"/>')
    # surf line
    s.append(f'<path d="M{X0},{Y_SURF} ' + " ".join(f"Q{x + 15},{Y_SURF + 7} {x + 30},{Y_SURF}" for x in range(X0, X1, 30))
             + f'" stroke="#fff" stroke-width="2.5" fill="none" opacity="0.9"/>')
    # NC-12
    s.append(f'<rect x="{X0}" y="{Y_ROAD - 7}" width="{X1 - X0}" height="14" fill="{ROAD}"/>')
    s.append(f'<line x1="{X0}" y1="{Y_ROAD}" x2="{X1}" y2="{Y_ROAD}" stroke="{ROAD_LINE}" stroke-width="2" stroke-dasharray="10 8"/>')
    s.append(label(X0 + 10, Y_ROAD + 26, "NC-12", size=13, color="#fff", weight=600))

    # 1. the starting island: a 10 m grid over the left stretch
    s.append(f'<rect x="{X0}" y="{Y_MARSH - 14}" width="{B1 - X0}" height="{Y_SURF - Y_MARSH + 14}" fill="url(#md-grid)"/>')

    # 2. storms and overwash: a low dune in the middle stretch and a sand fan spreading inland
    cx = (B1 + B2) / 2
    s.append(f'<path d="M{cx - 70},{Y_DUNE + 24} Q{cx},{Y_DUNE - 70} {cx + 70},{Y_DUNE + 24} Z" fill="{SAND}" stroke="{GROUND}" stroke-width="1.5"/>')
    s.append(f'<rect x="{cx - 46}" y="{Y_DUNE - 2}" width="92" height="28" fill="{SAND}"/>')
    s.append(arrow(cx, Y_SURF + 34, cx, Y_DUNE - 34, w=3.2))
    s.append(arrow(cx - 18, Y_SURF + 30, cx - 52, Y_DUNE - 22, w=2.2))
    s.append(arrow(cx + 18, Y_SURF + 30, cx + 52, Y_DUNE - 22, w=2.2))

    # 3. sand along the shore: arrows across both stretch boundaries on the beach
    yb = (Y_DUNE + 24 + Y_SURF) / 2 + 4
    for b in (B1, B2):
        s.append(arrow(b - 48, yb, b + 48, yb, w=3))

    # 4. people, on the right stretch: added sand widening the beach, a rebuilt dune, the road moved inland
    rx0, rx1 = B2 + 40, X1 - 40
    s.append(f'<path d="M{rx0},{Y_SURF} L{rx0 + 20},{Y_SURF + 26} L{rx1 - 20},{Y_SURF + 26} L{rx1},{Y_SURF} Z" '
             f'fill="{SAND_ADDED}" stroke="{FILL_EDGE}" stroke-width="1.5" stroke-dasharray="5 3"/>')
    s.append(f'<rect x="{rx0}" y="{Y_DUNE - 4}" width="{rx1 - rx0}" height="10" rx="4" fill="{GROUND}" stroke="{FILL_EDGE}" stroke-width="1.2"/>')

    # stretch boundaries and the 500 m bracket
    for b in (B1, B2):
        s.append(f'<line x1="{b}" y1="{Y_MARSH - 18}" x2="{b}" y2="{Y_SURF + 6}" stroke="#fff" stroke-width="2" stroke-dasharray="6 5"/>')
    s.append(f'<path d="M{B1 + 4},70 v-8 H{B2 - 4} v8" fill="none" stroke="{MUTED}" stroke-width="1.4"/>')
    s.append(label(cx, 54, "one stretch of island, 500 m along the shore", anchor="middle", size=15, color=MUTED))

    # place names
    s.append(label(X1 - 6, Y_MARSH - 26, "Pamlico Sound", anchor="end", size=15, color=MUTED))
    s.append(label(X1 - 6, H - 54, "Atlantic Ocean", anchor="end", size=15, color=MUTED))
    s.append(f'<rect x="0" y="40" width="{W}" height="{H - 80}" fill="url(#md-fade)"/>')

    # badges and short labels
    s.append(badge(X0 + 30, Y_MARSH + 34, 1))
    s.append(label(X0 + 54, Y_MARSH + 40, "lidar elevation,\n10 m grid", size=16, box=True))
    s.append(badge(cx + 64, Y_SURF + 52, 2))
    s.append(label(cx + 88, Y_SURF + 58, "storm water and\nsand over the dune", size=16, box=True))
    s.append(badge(B1 - 64, yb + 30, 3))
    s.append(label(B1 - 40, yb + 36, "sand moves along the beach", size=16, box=True))
    s.append(badge(rx0 - 2, Y_ROAD - 51, 4))
    s.append(label(rx0 + 22, Y_ROAD - 46, "dune rebuilt, sand added,\nroad protected or moved", size=16, box=True))

    s.append('</svg>')
    OUT.write_text("\n".join(s) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
