"""
One stretch of the model island, seen as a photo, as lidar, and as the model's grid, and the road behind its dunes:
two figures for the model-input stepper on The model page of the Hatteras stakeholder pages.

    python tools/hatteras_model_stretch.py

Hannah asked (2026-10-03) for the elevation step to go photo -> raw elevation -> resampled grid, and for a road figure
on the real island instead of a chart, both on one stretch so the example carries through the steps (Hannah,
2026-10-03): GIS 43, between Avon and Salvo about 21 km north of Cape Point, picked for its tall, continuous dune with
the road behind it (the tallest 10th-percentile dune crest of the road stretches away from villages and road moves).
It is outlined on the whole-island map of step 2 (tools/hatteras_model_steps.py reads GIS from here).
  step1.png        (a) NC OneMap 1996 aerial photo, (b) the 1 m elevation surface, (c) the 10 m grid the model is cut
                   from; the rasters are CASCADE's 2009-2014-1996 product (clip_domain_43_*, resampled_domain_43_*),
                   as in scripts/figure_making/pipeline/0-elevation/dem_composition_figures.py.
  step5_road.png   the 2007 photo with the 2009 digitised dune line and the 2008 NC-12 line (lines and photo of the same
                   years, so they sit on each other; the 1996 photo is offset from them), and the distance between them. The model reads its own distance per stretch from the elevation grid
                   (RoadSetback_1996_dunestart.csv, 170 m here); the caption on the page says so.
Writes into assets/hatteras/img/model_steps/; the photos are cached in tools/data/model_stretch_gis<GIS>_<year>.jpg.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import io as _io
import sys
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
for p in ("scripts", "scripts/figure_making/island", "scripts/hatteras_ms", "scripts/input_prep/3-env-forcings/3-storms",
          "scripts/figure_making/pipeline"):
    sys.path.insert(0, str(CASCADE / p))
import geopandas as gpd  # noqa: E402
import rasterio  # noqa: E402
from shapely.geometry import LineString  # noqa: E402
import inputs_overview_figure as io  # noqa: E402
from site_layer.hat_elevation_products import product  # noqa: E402

GIS = 43
PRODUCT = "2009-2014-1996"
MHW_NAVD = 0.36                       # as in dem_composition_figures.py
X0, X1 = 1000, 1950                   # metres east of the raster's west edge: the island and the beach
OUT = SITE / "assets/hatteras/img/model_steps"
NCONEMAP = "https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_{year}/ImageServer/exportImage"
DUNE = CASCADE / "data/hatteras_init/2-brie-offset/dunelines/duneline_2009.geojson"
ROAD = CASCADE / "data/hatteras_init/4-mgmt-forcing/road_offset/raw_offset/2008/nc12_2008.geojson"
INK = "#1a1a1a"
halo = [pe.withStroke(linewidth=3, foreground=INK)]


def read(path):
    with rasterio.open(path) as r:
        z = r.read(1).astype(float)
        z[z == r.nodata] = np.nan
        return z, r.bounds


def photo(b, year):
    path = SITE / f"tools/data/model_stretch_gis{GIS}_{year}.jpg"
    if not path.exists():
        url = (f"{NCONEMAP.format(year=year)}?bbox={b.left + X0},{b.bottom},{b.left + X1},{b.top}&bboxSR=26918&imageSR=26918"
               f"&size={(X1 - X0)},{int(b.top - b.bottom)}&format=jpg&f=image")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        Image.open(_io.BytesIO(urllib.request.urlopen(req, timeout=180).read())).convert("RGB").save(path, quality=90)
    return Image.open(path)


def panel(ax, letter, title):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(INK)
        s.set_linewidth(1)
    ax.text(0.008, 0.95, f"({letter}) {title}", transform=ax.transAxes, va="top", fontsize=10.5, color=INK,
            bbox=dict(boxstyle="square,pad=0.3", fc="white", ec=INK, lw=0.7, alpha=0.93))


def main():
    p = product(PRODUCT)
    z1, b = read(p.gapfill_1m / f"clip_domain_{GIS}_filled.tif")
    z10, b10 = read(p.resampled_10m / f"resampled_domain_{GIS}_filled.tif")
    z1, z10 = z1 - MHW_NAVD, z10 - MHW_NAVD
    cmap, norm, ticks, water = io.init.scheme_colours(io.ELEVATION_SCHEME)
    img = photo(b, 1996)
    H = b.top - b.bottom
    ext = (0, X1 - X0, 0, H)

    # ---- step 1: photo, 1 m elevation, 10 m grid ------------------------------------------------------------------
    fig, axes = plt.subplots(3, 1, figsize=(9.5, 3 * 9.5 * H / (X1 - X0) + 0.9), gridspec_kw={"hspace": 0.06})
    axes[0].imshow(img, extent=ext)
    panel(axes[0], "a", "aerial photo, 1996")
    c1 = z1[:, X0:X1]
    axes[1].imshow(np.ma.masked_less(np.ma.masked_invalid(c1), 0), cmap=cmap, norm=norm, extent=ext, interpolation="nearest")
    axes[1].set_facecolor(water)
    panel(axes[1], "b", "laser survey (lidar): height every 1 m")
    c10 = z10[:, X0 // 10:X1 // 10]
    im = axes[2].imshow(np.ma.masked_less(np.ma.masked_invalid(c10), 0), cmap=cmap, norm=norm, extent=ext, interpolation="nearest")
    axes[2].set_facecolor(water)
    panel(axes[2], "c", "the model's grid: one height every 10 m")
    for ax in axes:
        ax.set_xlim(0, X1 - X0)
        ax.set_ylim(0, H)
        ax.text(0.995, 0.5, "ocean", transform=ax.transAxes, ha="right", va="center", rotation=90, fontsize=9.5,
                color="white", path_effects=halo)
        ax.text(0.005, 0.5, "sound", transform=ax.transAxes, ha="left", va="center", rotation=90, fontsize=9.5,
                color="white", path_effects=halo)
    bar_x = 60
    axes[2].plot([bar_x, bar_x + 200], [40, 40], color="white", lw=3, solid_capstyle="butt", path_effects=halo)
    axes[2].text(bar_x + 100, 60, "200 m", ha="center", va="bottom", fontsize=9, color="white", path_effects=halo)
    cb = fig.colorbar(im, ax=axes.tolist(), ticks=ticks, fraction=0.02, pad=0.01, aspect=22)
    cb.set_label("height above high tide (m)", fontsize=9.5)
    cb.ax.tick_params(labelsize=9)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "step1.png", dpi=150, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("wrote step1.png")

    # ---- step 5: the road behind the dunes on this stretch ------------------------------------------------------------
    dune = gpd.read_file(DUNE).to_crs(26918).geometry.union_all()
    road = gpd.read_file(ROAD).to_crs(26918).geometry.union_all()

    def local(geom):
        xs, ys = geom.xy
        return np.array(xs) - b.left - X0, np.array(ys) - b.bottom

    from shapely.geometry import box as sbox
    clip = sbox(b.left + X0, b.bottom, b.left + X1, b.top)
    fig, ax = plt.subplots(figsize=(9.5, 9.5 * H / (X1 - X0) + 0.3))
    ax.imshow(photo(b, 2007), extent=ext)
    for geom, col, lab in ((dune.intersection(clip), "#ffd23f", "front of the dunes (2009)"),
                           (road.intersection(clip), "#d55e00", "NC-12 (2008)")):
        for g in getattr(geom, "geoms", [geom]):
            x, y = local(g)
            ax.plot(x, y, color=col, lw=2.6, path_effects=halo, label=lab)
            lab = None
    # the distance, measured east-west across the middle of the stretch
    ym = b.bottom + H / 2
    ray = LineString([(b.left, ym), (b.right, ym)])
    dx = max(q.x for q in getattr(ray.intersection(dune), "geoms", [ray.intersection(dune)]))
    rx = max(q.x for q in getattr(ray.intersection(road), "geoms", [ray.intersection(road)]))
    d = 10 * round((dx - rx) / 10)
    ax.annotate("", xy=(dx - b.left - X0, H / 2), xytext=(rx - b.left - X0, H / 2),
                arrowprops=dict(arrowstyle="<->", color="white", lw=1.8, path_effects=halo))
    ax.text((dx + rx) / 2 - b.left - X0, H / 2 + 18, f"about {d} m", ha="center", va="bottom", fontsize=11,
            fontweight="bold", color="white", path_effects=halo)
    ax.set_xlim(0, X1 - X0)
    ax.set_ylim(0, H)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="lower left", fontsize=9.5, framealpha=0.92, edgecolor=INK)
    ax.plot([X1 - X0 - 260, X1 - X0 - 60], [40, 40], color="white", lw=3, solid_capstyle="butt", path_effects=halo)
    ax.text(X1 - X0 - 160, 60, "200 m", ha="center", va="bottom", fontsize=9, color="white", path_effects=halo)
    fig.savefig(OUT / "step5_road.png", dpi=150, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"wrote step5_road.png (about {d} m)")


if __name__ == "__main__":
    main()
