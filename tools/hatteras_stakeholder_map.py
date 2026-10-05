"""
Study-area map for the Hatteras stakeholder pages, in the house map style.

    python tools/hatteras_stakeholder_map.py

Hatteras Island from Cape Point to Oregon Inlet on Esri World Imagery, north up, UTM 18N, with the
villages, NC-12 today (over the 2022 Jug Handle Bridge) with the 2008 beach road it bypassed dashed, the
beach nourishment reaches the model is forced with, and the Buxton groins; a locator inset of the
Mid-Atlantic coast. Reaches and labels are placed on the CoastSat
transects in assets/hatteras/data/shoreline_rates.json, so run hatteras_shoreline_data.py first.
Writes assets/hatteras/img/study_area_map.jpg. Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
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
from shapely.geometry import Point
from shapely.ops import linemerge, substring
from rasterio.warp import transform_bounds

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
sys.path.insert(0, str(CASCADE / "scripts"))
from site_layer.hat_figure_style import (  # noqa: E402
    C, INK, INK_MUTED, MAP_LEGEND, apply_style, north_dart, scale_bar_km, spines_for_image)
from site_layer.hat_map_layers import NE_STATES  # noqa: E402
sys.path.insert(0, str(SITE / "tools"))
import hatteras_shoreline_data as shoreline  # noqa: E402
import hatteras_fig_style as style  # noqa: E402

RATES = SITE / "assets/hatteras/data/shoreline_rates.json"
NC12 = CASCADE / "data/hatteras_init/4-mgmt-forcing/road_offset/raw_offset/current/nc12_current.geojson"
NC12_2008 = CASCADE / "data/hatteras_init/4-mgmt-forcing/road_offset/raw_offset/2008/nc12_2008.geojson"
# The Jug Handle Bridge: nc12_current follows it (within 3 m of OpenStreetMap, checked 2026-10-02);
# the 2008 line still runs along the beach there. Ends of the bridge stretch on the current line:
BRIDGE_ENDS_LL = [(-75.471925, 35.633187), (-75.467351, 35.598803)]
OUT = SITE / "assets/hatteras/img/study_area_map.jpg"
TILE_CACHE = CASCADE / "data/hatteras_init/map_elements/tile_cache"

LAT0, LAT1, LON0, LON1 = 35.19, 35.80, -75.72, -75.36
CRS = "EPSG:32618"
TEAL = style.TEAL                   # the site's highlight colour (was house LOCATOR #1b7f8c)
ROAD = "#ffd23f"                    # house: NC-12 on imagery
SAND = "#f6e3b8"                    # house ADDED_FILL
WATER_MAP, LAND, LAND_EDGE = "#e9eff4", "#ede9df", "0.55"
HALO = [mpl.patheffects.withStroke(linewidth=1.4, foreground="0.12")]
TEXT = dict(color="white", fontsize=8.5, zorder=8, path_effects=HALO)
REACH_OFFSET_M = 280.0              # reaches are drawn this far seaward of today's shoreline, just off the beach and clear of NC-12
BEACH_YEARS = (2020, 2025)          # "today's shoreline": the median CoastSat position over these years
GROIN = C["GROIN"]
GROIN_LEN_M = 900.0                 # the groins drawn as one short shore-normal line, out from the beach

to_utm = Transformer.from_crs("EPSG:4326", CRS, always_xy=True).transform


def spaced_caps(text):
    return "   ".join(" ".join(w.upper()) for w in text.split())


def imagery(ax, window):
    cx.set_cache_dir(str(TILE_CACHE))
    w, s, e, n = transform_bounds(CRS, "EPSG:3857", *window)
    img, ext = cx.bounds2img(w, s, e, n, zoom=12, source=cx.providers.Esri.WorldImagery, ll=False)
    img, ext = cx.warp_tiles(img, ext, t_crs=CRS)
    ax.imshow(img, extent=ext, interpolation="bilinear", zorder=0)


def beach_points(transects, g0, g1):
    """UTM points on today's beach for the transects in GIS g0..g1, south to north: each transect's median
    CoastSat shoreline position over BEACH_YEARS, measured along it from its landward end."""
    pts = []
    for t in transects:
        if g0 <= t["d"] <= g1:
            date, pos = shoreline.load_series(t["id"])
            recent = pos[date.dt.year.between(*BEACH_YEARS)]
            if recent.empty:
                continue
            (lx, ly), (sx, sy) = t["line"]
            a, b = np.array(to_utm(lx, ly)), np.array(to_utm(sx, sy))
            u = (b - a) / np.linalg.norm(b - a)
            pts.append(a + u * (float(recent.median()) + REACH_OFFSET_M))
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
    ax.set_anchor("NW")
    ax.set_xticks([])
    ax.set_yticks([])
    spines_for_image(ax)


def main() -> None:
    apply_style()
    style.apply(size=None)        # the site's font over the house sizes
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

    # NC-12 today (State Plane feet in the source), which crosses the sound on the Jug Handle Bridge,
    # and, dashed, the 2008 road it bypassed along the beach at the S-curves
    road = linemerge(list(gpd.read_file(NC12).to_crs(CRS).geometry))
    xs, ys = road.xy
    ax.plot(xs, ys, color="0.1", lw=3.0, solid_capstyle="round", zorder=4)
    ax.plot(xs, ys, color=ROAD, lw=1.6, solid_capstyle="round", zorder=5)
    ends = [Point(to_utm(*ll)) for ll in BRIDGE_ENDS_LL]
    old = linemerge(list(gpd.read_file(NC12_2008).to_crs(CRS).geometry))
    a, b = sorted(old.project(p) for p in ends)
    former = substring(old, a, b)
    xs, ys = former.xy
    ax.plot(xs, ys, color="0.1", lw=2.6, zorder=4)
    ax.plot(xs, ys, color="white", lw=1.3, ls=(0, (2.5, 2)), zorder=5)
    a, b = sorted(road.project(p) for p in ends)
    mid = substring(road, a, b).interpolate(0.5, normalized=True)
    ax.annotate("Jug Handle\nBridge, 2022", (mid.x, mid.y), xytext=(-16, 0), textcoords="offset points",
                ha="right", va="center", **TEXT,
                arrowprops=dict(arrowstyle="-", color="white", lw=0.6, shrinkA=0, shrinkB=3))

    # Nourishment reaches: a gold band along the beach they cover, labelled to the east with place and years
    for n in data["nourishments"]:
        p = beach_points(data["transects"], *n["gis"])
        ax.plot(p[:, 0], p[:, 1], color="0.1", lw=5.4, solid_capstyle="round", zorder=6)
        ax.plot(p[:, 0], p[:, 1], color=SAND, lw=3.6, solid_capstyle="round", zorder=7)
        mid = p[len(p) // 2]
        where = "Rodanthe S-curves" if n["name"] == "Rodanthe" else n["name"]
        ax.annotate(where + "\n" + " and ".join(str(y) for y in n["years"]), mid, xytext=(22, 0),
                    textcoords="offset points", va="center", ha="left", linespacing=1.15, **TEXT,
                    arrowprops=dict(arrowstyle="-", color=SAND, lw=0.9, shrinkA=0, shrinkB=4))

    # Groins: a short horizontal line out from the beach at the GIS 5-6 boundary (the shore runs north-south here)
    g = beach_points(data["transects"], 5, 6)
    bx, by = g[len(g) // 2] - np.array([REACH_OFFSET_M, 0])  # from the shoreline itself
    ax.plot([bx, bx + GROIN_LEN_M], [by, by], color="white", lw=4.2, solid_capstyle="butt", zorder=8)
    ax.plot([bx, bx + GROIN_LEN_M], [by, by], color=GROIN, lw=2.4, solid_capstyle="butt", zorder=9)
    ax.annotate("Buxton groins", (bx + GROIN_LEN_M, by), xytext=(12, 0), textcoords="offset points", ha="left",
                va="center", **TEXT, arrowprops=dict(arrowstyle="-", color="white", lw=0.7, shrinkA=0, shrinkB=2))

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
    ax.text(0.22, 0.42, spaced_caps("Pamlico Sound"), transform=ax.transAxes, ha="center", rotation=90, **TEXT)

    handles = [
        Line2D([], [], color=ROAD, lw=2.2, label="NC-12", path_effects=[mpl.patheffects.withStroke(linewidth=3.6, foreground="0.1")]),
        Line2D([], [], color="white", lw=1.3, ls=(0, (2.5, 2)), label="NC-12 before the 2022 bridge",
               path_effects=[mpl.patheffects.withStroke(linewidth=2.6, foreground="0.35")]),
        Line2D([], [], color=SAND, lw=3.6, solid_capstyle="round", label="Beach nourishment (years labelled)",
               path_effects=[mpl.patheffects.withStroke(linewidth=5.4, foreground="0.1")]),
        Line2D([], [], color=GROIN, lw=2.4, label="Buxton groins",
               path_effects=[mpl.patheffects.withStroke(linewidth=4.2, foreground="white")]),
        Line2D([], [], marker="o", ls="none", ms=5, mfc="white", mec="0.1", label="Village"),
    ]
    ax.legend(handles=handles, loc="lower right", bbox_to_anchor=(0.985, 0.015), **MAP_LEGEND)
    # scale bar under the locator (upper left), north arrow above the legend (lower right)
    on_water = dict(color="white", path_effects=HALO)
    scale_bar_km(ax, 10_000, x=0.035, y=0.795, text_kw=on_water)
    north_dart(ax, (x0 + 0.93 * (x1 - x0), y0 + 0.16 * (y1 - y0)), arrow_m=3000, text_kw=on_water)
    ax.text(0.015, 0.006, "Imagery: Esri World Imagery",
            transform=ax.transAxes, ha="left", va="bottom",
            fontsize=6, color="white", path_effects=HALO, zorder=12)

    inset = fig.add_axes([0.02, 0.70, 0.36, 0.28])
    locator(inset, (LON0, LON1, LAT0, LAT1))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=220, pil_kwargs={"quality": 88})
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
