"""
Ocean City and Assateague Island across Ocean City Inlet, for the Dune building page of the Hatteras stakeholder pages.

    python tools/hatteras_assateague_figure.py

A developed, held shoreline next to a natural one that is free to overwash and roll landward: USGS National Map imagery (public domain) of Ocean City Inlet,
Maryland, with Ocean City's shoreline carried south as a dashed line so the landward offset of Assateague's north
end shows. The inlet opened in a 1933 hurricane and was fixed with jetties; they cut off the sand drifting south,
and Assateague's north end retreated faster (Pendleton, Williams and Thieler, 2004, USGS Open-File Report 2004-1020).
Hannah asked for this example on 2026-10-03, to show an island allowed to overwash and roll over beside a developed one. The dashed line is drawn by eye along Ocean City's water's edge in the
photo; it shows the offset, it does not measure it. Writes assets/hatteras/img/assateague_offset.jpg.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-04
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np

import hatteras_imagery_data as img

SITE = Path(__file__).resolve().parents[1]
CACHE = SITE / "tools/data/assateague_usgs.jpg"
OUT = SITE / "assets/hatteras/img/assateague_offset.jpg"
CENTRE = (38.318, -75.095)
HALF_W_M, HALF_H_M = 2200, 2600          # ground metres, before the crop
PX = (1100, 1300)
CROP = (0, 0, 860, 850)                  # px: drops the dark mosaic seams offshore and in the south
TILES = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
# Ocean City's water's edge, traced by eye on a 20 px grid over the photo (2026-10-04, Hannah: the old two-point line
# sat 50-60 m up the dry beach); above y 150 the edge runs off the right of the frame
OC_EDGE = [(860, 150), (857, 175), (847, 200), (837, 250), (823, 300), (803, 350), (787, 400), (767, 450), (762, 470)]
CARRY_FROM_Y = 300                       # the dashed line carries on the straight trend of the edge south of this row
ASSA_EDGE_X = 482                        # px: Assateague's water's edge on the offset row (y 700), read off the photo


def main():
    if not CACHE.exists():
        x, y = img.merc(*CENTRE)
        k = 1 / math.cos(math.radians(CENTRE[0]))
        b = [x - HALF_W_M * k, y - HALF_H_M * k, x + HALF_W_M * k, y + HALF_H_M * k]
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        img.export_xyz(TILES, b, PX).convert("RGB").save(CACHE, quality=90)
    from PIL import Image
    photo = Image.open(CACHE).crop(CROP)
    m_per_px = 2 * HALF_W_M / PX[0]

    halo = [pe.withStroke(linewidth=3, foreground="#1a1a1a")]
    fig, ax = plt.subplots(figsize=(7.2, 7.2 * photo.height / photo.width))
    ax.imshow(photo, interpolation="lanczos")
    ax.set_xlim(0, photo.width)
    ax.set_ylim(photo.height, 0)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#1a1a1a")
        s.set_linewidth(1.2)

    # Ocean City's shoreline, carried south past the inlet
    xs, ys = zip(*OC_EDGE)
    south = [(x, y) for x, y in OC_EDGE if y >= CARRY_FROM_Y]
    slope = np.polyfit([y for _, y in south], [x for x, _ in south], 1)[0]
    x1, y1 = OC_EDGE[-1]
    ax.plot(xs, ys, color="#ffd23f", lw=2.2, path_effects=halo)
    ax.plot([x1, x1 + slope * (photo.height - y1)], [y1, photo.height], color="#ffd23f", lw=2, ls=(0, (5, 3)), path_effects=halo)
    xe, ye = x1 + slope * (700 - y1), 700
    ax.annotate("", xy=(ASSA_EDGE_X, ye), xytext=(xe - 4, ye), arrowprops=dict(arrowstyle="<->", color="white", lw=1.6, path_effects=halo))
    t = dict(color="white", path_effects=halo)
    arrow = dict(arrowstyle="-|>", color="white", lw=1.3, path_effects=halo)
    ax.text((ASSA_EDGE_X + xe) / 2, ye - 14, "offset", ha="center", va="bottom", fontsize=10, fontweight="bold", **t)
    ax.text(x1 + slope * (780 - y1) + 8, 780, "Ocean City's shoreline,\ncarried south", ha="left", va="center", fontsize=9, **t)

    ax.text(800, 175, "Ocean City\n(developed;\nbeach nourished)", ha="right", va="center", fontsize=10.5, fontweight="bold", **t)
    ax.annotate("Assateague Island\n(natural: free to\noverwash and roll\nlandward)", xy=(415, 625), xytext=(200, 585), ha="center", va="center",
                fontsize=10.5, fontweight="bold", arrowprops=arrow, **t)
    ax.text(95, 215, "mainland", ha="center", va="center", fontsize=9.5, fontstyle="italic", **t)
    ax.annotate("overwash fan:\nsand washed across\nthe island", xy=(292, 730), xytext=(115, 697), ha="center", va="center",
                fontsize=9.5, arrowprops=arrow, **t)
    ax.annotate("south jetty", xy=(690, 513), xytext=(730, 590), ha="left", fontsize=10, arrowprops=arrow, **t)
    ax.annotate("Ocean City Inlet,\nopened 1933", xy=(600, 445), xytext=(470, 300), ha="center", fontsize=9.5, arrowprops=arrow, **t)
    ax.annotate("", xy=(752, 400), xytext=(782, 262), arrowprops=dict(arrowstyle="-|>", color="white", lw=1.6, path_effects=halo))
    ax.text(778, 250, "sand drifts south", ha="right", va="bottom", fontsize=9.5, **t)

    # scale bar and north arrow
    bar = 1000 / m_per_px
    ax.plot([30, 30 + bar], [815, 815], color="white", lw=3.5, solid_capstyle="butt", path_effects=halo)
    ax.text(30 + bar / 2, 800, "1 km", ha="center", va="bottom", fontsize=9.5, **t)
    ax.annotate("N", xy=(40, 30), xytext=(40, 85), ha="center", va="center", fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.6, path_effects=halo), **t)
    fig.savefig(OUT, dpi=190, bbox_inches="tight", pad_inches=0.03, pil_kwargs={"quality": 86, "optimize": True})
    print(f"wrote {OUT.relative_to(SITE)}")


if __name__ == "__main__":
    main()
