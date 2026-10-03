"""
Map of the Virginia Coast Reserve barrier islands, drawn in the Hatteras study-area map style.

    python tools/vcr_islands_map.py

(a) The barrier islands on Esri World Imagery, north up, UTM 18N; (b) locator on the
Mid-Atlantic coast; (c) an American Oystercatcher. Island positions from OpenStreetMap
(Nominatim/Overpass, queried 2026-10-02). Needs the CASCADE repo beside this one for the
house style and the Natural Earth states file.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-02
"""

import math
import sys
from pathlib import Path

import contextily as cx
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle
from PIL import Image
from pyproj import Transformer
from rasterio.warp import transform_bounds

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
sys.path.insert(0, str(CASCADE / "scripts"))
from site_layer.hat_figure_style import apply_style, INK, INK_MUTED, spines_for_image  # noqa: E402
from site_layer.hat_map_layers import NE_STATES  # noqa: E402

OUT = SITE / "assets" / "img" / "research" / "vcr_barrier_islands.jpg"
PHOTO = SITE / "assets" / "img" / "photos" / "oystercatchers.jpg"

# --- CONFIG ------------------------------------------------------------------
ISLANDS = [  # name, lat, lon (OpenStreetMap)
    ("Assawoman Island", 37.7918, -75.5191),
    ("Metompkin Island", 37.7524, -75.5446),
    ("Cedar Island", 37.6321, -75.6127),
    ("Parramore Island", 37.5387, -75.6280),
    ("Hog Island", 37.4162, -75.6910),
    ("Cobb Island", 37.3276, -75.7492),
    ("Little Cobb Island", 37.3040, -75.7869),
    ("Wreck Island", 37.2732, -75.7962),
    ("Ship Shoal Island", 37.2196, -75.8021),
    ("Myrtle Island", 37.1932, -75.8166),
    ("Smith Island", 37.1440, -75.8696),
    ("Fishermans Island", 37.0973, -75.9603),
]
LAT0, LAT1, LON0, LON1 = 37.05, 37.90, -76.10, -75.28
CRS = "EPSG:32618"
TEAL = "#1b7f8c"
WATER_MAP, LAND, LAND_EDGE = "#e9eff4", "#ede9df", "0.55"
HALO = [mpl.patheffects.withStroke(linewidth=1.2, foreground="0.12")]
TEXT = dict(color="white", fontsize=8, zorder=8, path_effects=HALO)
TILE_CACHE = CASCADE / "data" / "hatteras_init" / "map_elements" / "tile_cache"
# -----------------------------------------------------------------------------

to_utm = Transformer.from_crs("EPSG:4326", CRS, always_xy=True).transform


# Water bodies in upright letter-spaced capitals
def spaced_caps(text):
    return "   ".join(" ".join(w.upper()) for w in text.split())


# The panel letter in a white box
def letter(ax, i, x, y, ha="left"):
    ax.text(x, y, f"({'abc'[i]})", transform=ax.transAxes, ha=ha, va="top", fontsize=10,
            fontweight="bold", color=INK, zorder=20,
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", boxstyle="square,pad=0.15"))


# A black/white segmented scale bar, labels below with a gap
def scale_bar(ax, x, y, length_m=10_000, segments=2):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    h = 0.008 * (y1 - y0)
    bx, by = x0 + x * (x1 - x0), y0 + y * (y1 - y0)
    seg = length_m / segments
    ax.add_patch(Rectangle((bx, by), length_m, h, facecolor="none", edgecolor="white", lw=2.2, zorder=11))
    for i in range(segments):
        ax.add_patch(Rectangle((bx + i * seg, by), seg, h, facecolor=INK if i % 2 == 0 else "white",
                               edgecolor=INK, lw=0.6, zorder=12))
    for i in range(segments + 1):
        km = i * seg / 1000
        ax.text(bx + i * seg, by - 1.5 * h, f"{km:g} km" if i == segments else f"{km:g}",
                ha="center", va="top", **{**TEXT, "zorder": 12})


# A split-dart north arrow pointing up, its "N" beyond the tip, centred on c (data units)
def north_dart(ax, c, arrow_m=3600.0):
    n, perp = np.array([0.0, 1.0]), np.array([-1.0, 0.0])
    c = np.asarray(c, float)
    tip, back = c + n * arrow_m / 2, c - n * arrow_m / 2
    notch, w = c - n * arrow_m * 0.22, 0.28 * arrow_m
    ax.add_patch(Polygon([tip, back + perp * w, notch, back - perp * w], closed=True, facecolor="none",
                         edgecolor="white", lw=2.2, zorder=11))
    ax.add_patch(Polygon([tip, back + perp * w, notch], closed=True, facecolor=INK, edgecolor=INK,
                         lw=0.6, zorder=12))
    ax.add_patch(Polygon([tip, notch, back - perp * w], closed=True, facecolor="white", edgecolor=INK,
                         lw=0.6, zorder=12))
    lab = tip + n * 0.40 * arrow_m
    ax.text(lab[0], lab[1], "N", ha="center", va="center", fontweight="bold", **{**TEXT, "fontsize": 8.5,
                                                                                    "zorder": 12})


# Imagery for the UTM window
def imagery(ax, window):
    cx.set_cache_dir(str(TILE_CACHE))
    w, s, e, n = transform_bounds(CRS, "EPSG:3857", *window)
    img, ext = cx.bounds2img(w, s, e, n, zoom=11, source=cx.providers.Esri.WorldImagery, ll=False)
    img, ext = cx.warp_tiles(img, ext, t_crs=CRS)
    ax.imshow(img, extent=ext, interpolation="bilinear", zorder=0)


# The locator: the map's box on the Mid-Atlantic coast, the reserve in teal
def locator(ax, box_ll):
    states = gpd.read_file(NE_STATES)
    lon0, lon1, lat0, lat1 = -79.6, -73.9, 35.6, 40.0
    ax.set_facecolor(WATER_MAP)
    states.plot(ax=ax, facecolor=LAND, edgecolor="white", lw=0.5, zorder=1)
    states.dissolve().plot(ax=ax, facecolor="none", edgecolor=LAND_EDGE, lw=0.4, zorder=2)
    for x in (-78, -76, -74):
        ax.axvline(x, color="white", lw=0.5, zorder=3)
    for y in (36, 38, 40):
        ax.axhline(y, color="white", lw=0.5, zorder=3)
    bl0, bl1, bt0, bt1 = box_ll
    ax.add_patch(Rectangle((bl0, bt0), bl1 - bl0, bt1 - bt0, facecolor=TEAL, alpha=0.35, edgecolor=TEAL,
                           lw=1.6, zorder=5))
    ax.text(-77.75, 37.55, "Virginia", ha="center", va="center", fontsize=8, color=INK_MUTED, zorder=6)
    ax.text(-74.9, 36.55, "Atlantic\nOcean", ha="center", va="center", fontsize=8, color=INK_MUTED,
            fontstyle="italic", zorder=6)
    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.set_aspect(1.0 / math.cos(math.radians((lat0 + lat1) / 2)))
    ax.set_anchor("NW")
    ax.set_xticks([])
    ax.set_yticks([])
    spines_for_image(ax)


# Run: imagery, labels, corner elements, locator and photo
def main() -> None:
    apply_style()
    x0, y0 = to_utm(LON0, LAT0)
    x1, y1 = to_utm(LON1, LAT1)
    window = (x0, y0, x1, y1)
    fw = 7.0
    fig = plt.figure(figsize=(fw, fw * (y1 - y0) / (x1 - x0)))
    ax = fig.add_axes([0, 0, 1, 1])
    imagery(ax, window)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_xticks([])
    ax.set_yticks([])
    spines_for_image(ax)

    # Island names on their ocean side with short leaders, italic like place names
    for name, lat, lon in ISLANDS:
        x, y = to_utm(lon, lat)
        ax.annotate(name, (x, y), xytext=(16, 0), textcoords="offset points", va="center",
                    fontstyle="italic", **TEXT,
                    arrowprops=dict(arrowstyle="-", color="white", lw=0.6, shrinkA=0, shrinkB=0))
    ax.text(0.80, 0.50, spaced_caps("Atlantic Ocean"), transform=ax.transAxes, ha="center", **TEXT)
    ax.text(0.05, 0.21, spaced_caps("Chesapeake Bay"), transform=ax.transAxes, ha="left", rotation=62, **TEXT)
    ax.text(0.27, 0.52, "Delmarva\nPeninsula", transform=ax.transAxes, ha="center", fontstyle="italic", **TEXT)

    # Top row: the locator (b) upper left with the north arrow beside it, (a) upper right, one top margin
    top = 0.988
    letter(ax, 0, 0.988, top, ha="right")
    ih = 0.24
    iw = ih * fig.get_size_inches()[1] / fw * 1.15
    ax_in = fig.add_axes([0.012, top - ih, iw, ih])
    locator(ax_in, (LON0, LON1, LAT0, LAT1))
    ax_in.apply_aspect()
    letter(ax_in, 1, 0.03, 0.97)
    p = ax_in.get_position()
    north_dart(ax, (x0 + (p.x1 + 0.05) * (x1 - x0), y0 + (top - 0.045) * (y1 - y0)))

    # (c) the oystercatcher, framed over open ocean, lower right; the scale bar in open water beside it
    photo = Image.open(PHOTO).convert("RGB")
    pw = 0.36
    ph = pw * fw / fig.get_size_inches()[1] * photo.height / photo.width
    ax_ph = fig.add_axes([0.985 - pw, 0.045, pw, ph])
    ax_ph.imshow(photo)
    ax_ph.set_xticks([])
    ax_ph.set_yticks([])
    for s in ax_ph.spines.values():
        s.set_edgecolor("white")
        s.set_linewidth(1.6)
    letter(ax_ph, 2, 0.02, 0.97)
    ax_ph.text(0.98, 0.96, "American Oystercatcher", transform=ax_ph.transAxes, ha="right", va="top",
               fontstyle="italic", fontsize=8, color="black", zorder=8)

    scale_bar(ax, 0.40, 0.06)
    ax.text(0.988, 0.012, "Imagery: Esri World Imagery · Islands: © OpenStreetMap contributors",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=6.5, color=INK_MUTED, zorder=25,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", boxstyle="square,pad=0.15"))
    fig.savefig(OUT, dpi=240, pil_kwargs={"quality": 90})
    print(OUT)


if __name__ == "__main__":
    main()
