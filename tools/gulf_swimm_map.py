"""
Map of the Gulf of Mexico for the SWIMM project page, in the house map style.

    python tools/gulf_swimm_map.py

The three partner countries on Esri World Imagery with the partner institutions marked:
Harte Research Institute (Corpus Christi), UMDI-Sisal (UNAM, Yucatán) and the
Universidad de La Habana. Needs the CASCADE repo beside this one for the house style.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-02
"""

import sys
from pathlib import Path

import contextily as cx
import matplotlib.pyplot as plt
from pyproj import Transformer

SITE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SITE.parent / "CASCADE" / "scripts"))
from site_layer.hat_figure_style import (apply_style, INK_MUTED, MAP_TEXT, spaced_caps, scale_bar_km,  # noqa: E402
                                         north_dart, spines_for_image)

OUT = SITE / "assets" / "img" / "research" / "gulf_swimm_map.jpg"

# --- CONFIG ------------------------------------------------------------------
LON0, LON1, LAT0, LAT1 = -99.5, -78.5, 17.0, 31.5
SITES = [  # label, lat, lon, label offset (points)
    ("Harte Research Institute\nCorpus Christi", 27.71, -97.33, (10, -2)),
    ("UMDI-Sisal (UNAM)\nYucatán", 21.17, -90.03, (-10, -18)),
    ("Universidad de La Habana\nHavana", 23.13, -82.38, (-10, 12)),
]
COUNTRIES = [("United States", 31.0, -91.0), ("Mexico", 19.2, -98.2), ("Cuba", 21.7, -79.6)]
SITE_C = "#1b7f8c"
# -----------------------------------------------------------------------------

CRS = "+proj=lcc +lat_1=20 +lat_2=30 +lat_0=24 +lon_0=-89 +datum=WGS84 +units=m"   # true distances, north up at the centre
to_map = Transformer.from_crs("EPSG:4326", CRS, always_xy=True).transform


# Run: imagery, names, sites, scale and arrow
def main() -> None:
    apply_style()
    xs, ys = zip(*[to_map(lo, la) for lo in (LON0, -89, LON1) for la in (LAT0, LAT1)])
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    fig = plt.figure(figsize=(7.0, 7.0 * (y1 - y0) / (x1 - x0)))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    from rasterio.warp import transform_bounds
    w, s, e, n = transform_bounds(CRS, "EPSG:3857", x0, y0, x1, y1)
    img, ext = cx.bounds2img(w, s, e, n, zoom=6, source=cx.providers.Esri.WorldImagery, ll=False)
    img, ext = cx.warp_tiles(img, ext, t_crs=CRS)
    ax.imshow(img, extent=ext, interpolation="bilinear", zorder=0)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_xticks([])
    ax.set_yticks([])
    spines_for_image(ax)

    ax.text(0.40, 0.55, spaced_caps("Gulf of Mexico"), transform=ax.transAxes, ha="center", **MAP_TEXT)
    for name, lat, lon in COUNTRIES:
        x, y = to_map(lon, lat)
        ax.text(x, y, name, ha="center", va="center", fontstyle="italic", **{**MAP_TEXT, "fontsize": 9})
    for label, lat, lon, off in SITES:
        x, y = to_map(lon, lat)
        ax.plot(x, y, "o", ms=6.5, color=SITE_C, mec="white", mew=1.2, zorder=9)
        ax.annotate(label, (x, y), xytext=off, textcoords="offset points",
                    ha="left" if off[0] > 0 else "right", va="center", **MAP_TEXT)

    scale_bar_km(ax, length_m=500_000, segments=2, x=0.035, y=0.07)
    north_dart(ax, (x0 + 0.95 * (x1 - x0), y0 + 0.88 * (y1 - y0)), arrow_m=0.06 * (y1 - y0))
    ax.text(0.988, 0.012, "Imagery: Esri World Imagery", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=6.5, color=INK_MUTED, zorder=25,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", boxstyle="square,pad=0.15"))
    fig.savefig(OUT, dpi=240, pil_kwargs={"quality": 90})
    print(OUT)


if __name__ == "__main__":
    main()
