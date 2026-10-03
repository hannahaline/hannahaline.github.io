"""
Study-area map for the Hatteras stakeholder pages, in the house map style.

    python tools/hatteras_stakeholder_map.py

Hatteras Island from Cape Point to Oregon Inlet on Esri World Imagery, north up, UTM 18N, with the
villages, NC-12 (current alignment), the beach nourishment reaches the model is forced with, and the
Buxton groins; a locator inset of the Mid-Atlantic coast. Reaches and labels are placed on the CoastSat
transects in assets/hatteras/data/shoreline_rates.json, so run hatteras_shoreline_data.py first.
Writes assets/hatteras/img/study_area_map.jpg. Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-02
"""
import json
import math
import sys
from pathlib import Path

import contextily as cx
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from pyproj import Transformer
from rasterio.warp import transform_bounds

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
sys.path.insert(0, str(CASCADE / "scripts"))
from site_layer.hat_figure_style import (  # noqa: E402
    INK, INK_MUTED, MAP_LEGEND, apply_style, groin_handle, groin_marker, north_dart, scale_bar_km,
    spines_for_image)
from site_layer.hat_map_layers import NE_STATES  # noqa: E402

RATES = SITE / "assets/hatteras/data/shoreline_rates.json"
NC12 = CASCADE / "data/hatteras_init/4-mgmt-forcing/road_offset/raw_offset/current/nc12_current.geojson"
OUT = SITE / "assets/hatteras/img/study_area_map.jpg"
TILE_CACHE = CASCADE / "data/hatteras_init/map_elements/tile_cache"

LAT0, LAT1, LON0, LON1 = 35.19, 35.80, -75.72, -75.36
CRS = "EPSG:32618"
TEAL = "#1b7f8c"                    # house LOCATOR
ROAD = "#ffd23f"                    # house: NC-12 on imagery
SAND, SAND_EDGE = "#f6e3b8", "#c8880f"  # house ADDED_FILL / ADDED
WATER_MAP, LAND, LAND_EDGE = "#e9eff4", "#ede9df", "0.55"
HALO = [mpl.patheffects.withStroke(linewidth=1.4, foreground="0.12")]
TEXT = dict(color="white", fontsize=8.5, zorder=8, path_effects=HALO)
REACH_OFFSET_M = 450.0              # reaches are drawn this far seaward of the transect ends

to_utm = Transformer.from_crs("EPSG:4326", CRS, always_xy=True).transform


def spaced_caps(text):
    return "   ".join(" ".join(w.upper()) for w in text.split())


def imagery(ax, window):
    cx.set_cache_dir(str(TILE_CACHE))
    w, s, e, n = transform_bounds(CRS, "EPSG:3857", *window)
    img, ext = cx.bounds2img(w, s, e, n, zoom=12, source=cx.providers.Esri.WorldImagery, ll=False)
    img, ext = cx.warp_tiles(img, ext, t_crs=CRS)
    ax.imshow(img, extent=ext, interpolation="bilinear", zorder=0)


def seaward_ends(transects, g0, g1):
    """UTM seaward ends of the transects in GIS g0..g1, south to north, pushed a little further offshore."""
    pts = []
    for t in transects:
        if g0 <= t["d"] <= g1:
            (lx, ly), (sx, sy) = t["line"]
            a, b = np.array(to_utm(lx, ly)), np.array(to_utm(sx, sy))
            u = (b - a) / np.linalg.norm(b - a)
            pts.append(b + u * REACH_OFFSET_M)
    return np.array(pts)


def locator(ax, box_ll):
    states = gpd.read_file(NE_STATES)
    lon0, lon1, lat0, lat1 = -80.2, -74.0, 33.8, 38.2
    ax.set_facecolor(WATER_MAP)
    states.plot(ax=ax, facecolor=LAND, edgecolor="white", lw=0.5, zorder=1)
    states.dissolve().plot(ax=ax, facecolor="none", edgecolor=LAND_EDGE, lw=0.4, zorder=2)
    for x in (-80, -78, -76):
        ax.axvline(x, color="white", lw=0.5, zorder=3)
    for y in (34, 36, 38):
        ax.axhline(y, color="white", lw=0.5, zorder=3)
    bl0, bl1, bt0, bt1 = box_ll
    ax.add_patch(Rectangle((bl0, bt0), bl1 - bl0, bt1 - bt0, facecolor=TEAL, alpha=0.35, edgecolor=TEAL,
                           lw=1.6, zorder=5))
    ax.text(-78.9, 35.55, "North\nCarolina", ha="center", va="center", fontsize=8, color=INK_MUTED, zorder=6)
    ax.text(-78.3, 37.45, "Virginia", ha="center", va="center", fontsize=8, color=INK_MUTED, zorder=6)
    ax.text(-74.9, 35.0, "Atlantic\nOcean", ha="center", va="center", fontsize=8, color=INK_MUTED,
            fontstyle="italic", zorder=6)
    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.set_aspect(1.0 / math.cos(math.radians((lat0 + lat1) / 2)))
    ax.set_anchor("NE")
    ax.set_xticks([])
    ax.set_yticks([])
    spines_for_image(ax)


def main() -> None:
    apply_style()
    data = json.loads(RATES.read_text(encoding="utf-8"))
    x0, y0 = to_utm(LON0, LAT0)
    x1, y1 = to_utm(LON1, LAT1)
    window = (x0, y0, x1, y1)
    fw = 6.0
    fig = plt.figure(figsize=(fw, fw * (y1 - y0) / (x1 - x0)))
    ax = fig.add_axes([0, 0, 1, 1])
    imagery(ax, window)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_xticks([])
    ax.set_yticks([])
    spines_for_image(ax)

    # NC-12, current alignment (State Plane feet in the source)
    road = gpd.read_file(NC12).to_crs(CRS)
    for geom in road.geometry:
        lines = getattr(geom, "geoms", [geom])
        for ln in lines:
            xs, ys = ln.xy
            ax.plot(xs, ys, color="0.1", lw=3.0, solid_capstyle="round", zorder=4)
            ax.plot(xs, ys, color=ROAD, lw=1.6, solid_capstyle="round", zorder=5)

    # Nourishment reaches, offshore of the beach they cover, labelled to the east
    for n in data["nourishments"]:
        p = seaward_ends(data["transects"], *n["gis"])
        ax.plot(p[:, 0], p[:, 1], color="0.1", lw=7.5, solid_capstyle="butt", zorder=6)
        ax.plot(p[:, 0], p[:, 1], color=SAND, lw=5.5, solid_capstyle="butt", zorder=7)
        mid = p[len(p) // 2]
        where = "Rodanthe S-curves" if n["name"] == "Rodanthe" else n["name"]
        label = f"{where}\nnourishment\n{', '.join(str(y) for y in n['years'])}"
        ax.annotate(label, mid, xytext=(16, 0), textcoords="offset points", va="center", ha="left",
                    **TEXT, arrowprops=dict(arrowstyle="-", color="white", lw=0.7, shrinkA=0, shrinkB=4))

    # Groins, on the beach at the GIS 5-6 boundary
    gx, gy = to_utm(*data["groin"]["ll"][::-1])
    groin_marker(ax, gx, gy)
    ax.annotate("Buxton\ngroins", (gx, gy), xytext=(-14, -18), textcoords="offset points", ha="right",
                va="top", **TEXT, arrowprops=dict(arrowstyle="-", color="white", lw=0.7, shrinkA=0, shrinkB=5))

    # Villages and places, labelled into the sound
    for p in data["places"]:
        x, y = to_utm(p["ll"][1], p["ll"][0])
        if p["name"] == "Pea Island":
            ax.text(x - 2600, y, "Pea Island\nNational Wildlife\nRefuge", ha="right", va="center",
                    fontstyle="italic", **TEXT)
            continue
        if p["name"] == "Cape Point":
            ax.annotate("Cape Point", (x, y - 900), xytext=(0, -14), textcoords="offset points", ha="center",
                        va="top", fontstyle="italic", **TEXT)
            continue
        ax.plot(x, y, "o", ms=5, mfc="white", mec="0.1", mew=1.0, zorder=9)
        dx = {"Waves": -28, "Salvo": -14, "Rodanthe": -14}.get(p["name"], -14)
        ax.annotate(p["name"], (x, y), xytext=(dx, 0), textcoords="offset points", ha="right", va="center",
                    fontweight="bold", **TEXT,
                    arrowprops=dict(arrowstyle="-", color="white", lw=0.6, shrinkA=0, shrinkB=3))

    ox, oy = to_utm(-75.535, 35.775)
    ax.text(ox, oy, "Oregon Inlet", ha="center", va="bottom", fontstyle="italic", **TEXT)
    ax.text(0.80, 0.55, spaced_caps("Atlantic Ocean"), transform=ax.transAxes, ha="center", rotation=90, **TEXT)
    ax.text(0.22, 0.62, spaced_caps("Pamlico Sound"), transform=ax.transAxes, ha="center", rotation=90, **TEXT)

    handles = [
        Line2D([], [], color=ROAD, lw=2.2, label="NC-12", path_effects=[mpl.patheffects.withStroke(linewidth=3.6, foreground="0.1")]),
        Line2D([], [], color=SAND, lw=5.5, label="Beach nourishment", path_effects=[mpl.patheffects.withStroke(linewidth=7.5, foreground="0.1")]),
        groin_handle(),
        Line2D([], [], marker="o", ls="none", ms=5, mfc="white", mec="0.1", label="Village"),
    ]
    ax.legend(handles=handles, loc="lower right", bbox_to_anchor=(0.985, 0.015), **MAP_LEGEND)
    scale_bar_km(ax, 10_000, x=0.05, y=0.055)
    north_dart(ax, (x0 + 0.08 * (x1 - x0), y0 + 0.30 * (y1 - y0)), arrow_m=3000)
    ax.text(0.015, 0.006, "Imagery: Esri World Imagery", transform=ax.transAxes, ha="left", va="bottom",
            fontsize=6, color="white", path_effects=HALO, zorder=12)

    inset = fig.add_axes([0.62, 0.70, 0.36, 0.28])
    locator(inset, (LON0, LON1, LAT0, LAT1))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=220, pil_kwargs={"quality": 88})
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
