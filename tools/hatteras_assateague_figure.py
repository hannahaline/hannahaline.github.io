"""
Ocean City and Assateague Island across Ocean City Inlet, for the Dune building page of the Hatteras stakeholder pages.

    python tools/hatteras_assateague_figure.py

A developed, held shoreline next to a natural one: USGS National Map imagery (public domain) of Ocean City Inlet,
Maryland, with Ocean City's shoreline carried south as a dashed line so the landward offset of Assateague's north
end shows. The inlet opened in a 1933 hurricane and was fixed with jetties; they cut off the sand drifting south,
and Assateague's north end retreated faster (Pendleton, Williams and Thieler, 2004, USGS Open-File Report 2004-1020).
Hannah asked for this example on 2026-10-03. The dashed line is drawn by eye along Ocean City's water's edge in the
photo; it shows the offset, it does not measure it. Writes assets/hatteras/img/assateague_offset.jpg.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt

import hatteras_imagery_data as img

SITE = Path(__file__).resolve().parents[1]
CACHE = SITE / "tools/data/assateague_usgs.jpg"
OUT = SITE / "assets/hatteras/img/assateague_offset.jpg"
CENTRE = (38.318, -75.095)
HALF_W_M, HALF_H_M = 2200, 2600          # ground metres, before the crop
PX = (1100, 1300)
CROP = (0, 0, 860, 850)                  # px: drops the dark mosaic seams offshore and in the south
TILES = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
OC_EDGE = [(864, 0), (758, 470)]         # px on Ocean City's water's edge, read off the photo


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
    (x0, y0), (x1, y1) = OC_EDGE
    slope = (x1 - x0) / (y1 - y0)
    ax.plot([x0, x1], [y0, y1], color="#ffd23f", lw=2.2, path_effects=halo)
    ax.plot([x1, x1 + slope * (photo.height - y1)], [y1, photo.height], color="#ffd23f", lw=2, ls=(0, (5, 3)), path_effects=halo)
    xe, ye = x1 + slope * (700 - y1), 700
    ax.annotate("", xy=(395, ye), xytext=(xe - 4, ye), arrowprops=dict(arrowstyle="<->", color="white", lw=1.6, path_effects=halo))
    t = dict(color="white", path_effects=halo)
    ax.text((395 + xe) / 2 + 10, ye - 14, "offset", ha="center", va="bottom", fontsize=10, fontweight="bold", **t)
    ax.text(x1 + slope * (780 - y1) + 8, 780, "Ocean City's shoreline,\ncarried south", ha="left", va="center", fontsize=9, **t)

    ax.text(800, 175, "Ocean City\n(developed;\nbeach nourished)", ha="right", va="center", fontsize=10.5, fontweight="bold", **t)
    ax.text(300, 640, "Assateague\nIsland\n(natural)", ha="center", va="center", fontsize=10.5, fontweight="bold", **t)
    ax.annotate("jetties", xy=(700, 515), xytext=(760, 590), ha="left", fontsize=10, arrowprops=dict(arrowstyle="-|>", color="white", lw=1.3, path_effects=halo), **t)
    ax.annotate("Ocean City Inlet,\nopened 1933", xy=(610, 400), xytext=(470, 300), ha="center", fontsize=9.5,
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.3, path_effects=halo), **t)
    ax.annotate("", xy=(805, 340), xytext=(805, 270), arrowprops=dict(arrowstyle="-|>", color="white", lw=1.3, path_effects=halo))
    ax.text(812, 310, "sand drifts\nsouth", fontsize=9, va="center", **t)

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
