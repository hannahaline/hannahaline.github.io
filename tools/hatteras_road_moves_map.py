"""
Where NC-12 has been moved, for the Management page of the Hatteras stakeholder pages.

    python tools/hatteras_road_moves_map.py

Three panels on Esri World Imagery, north up, UTM 18N, in the house map style:
(a) north of Buxton, the 1999 move inland after Hurricane Dennis; (b) the Rodanthe S-curves, the 1989 move inland
and the 2022 Jug Handle Bridge across Pamlico Sound; (c) New Inlet on Pea Island in early 2012, on the NC OneMap
2012 orthophoto, with Hurricane Irene's breach still open and the temporary bridge across it (no road lines: today's
bridge follows the old road almost exactly, and the breach has since closed). Road lines are CASCADE's NC-12 centrelines: 1978 (before the 1989
and 1999 moves), 2008 (after them) and current (the bridges). The largest measured move in each stretch is read from
road_relocation_1978_2008.csv. Writes assets/hatteras/img/road_moves_map.jpg. Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import json
import sys
from pathlib import Path

import contextily as cx
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from pyproj import Transformer
from rasterio.warp import transform_bounds
from shapely.geometry import box
from shapely.ops import linemerge

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
sys.path.insert(0, str(CASCADE / "scripts"))
from site_layer.hat_figure_style import MAP_LEGEND, apply_style, scale_bar_km, spines_for_image  # noqa: E402
import hatteras_fig_style as style  # noqa: E402

ROADS = CASCADE / "data/hatteras_init/4-mgmt-forcing/road_offset/raw_offset"
RELOC = CASCADE / "data/hatteras_init/4-mgmt-forcing/road_relocation/1978_2008/road_relocation_1978_2008.csv"
RATES = SITE / "assets/hatteras/data/shoreline_rates.json"
TILE_CACHE = CASCADE / "data/hatteras_init/map_elements/tile_cache"
OUT = SITE / "assets/hatteras/img/road_moves_map.jpg"
CRS = "EPSG:32618"

OLD, MOVED, NOW = "white", "#f28e2b", "#ffd23f"      # road before a move (dashed), after it, today (house NC-12 yellow)
HALO = [mpl.patheffects.withStroke(linewidth=1.6, foreground="0.12")]
TEXT = dict(color="white", fontsize=8.5, zorder=8, path_effects=HALO)
to_utm = Transformer.from_crs("EPSG:4326", CRS, always_xy=True).transform

# Panels: title, GIS domains whose relocation is measured, a lon/lat box, and which lines to draw
PANELS = [
    ("North of Buxton: moved inland in 1999", range(9, 15), (-75.540, 35.262, -75.505, 35.305),
     [("1978", OLD, "--"), ("2008", MOVED, "-")]),
    ("Rodanthe S-curves: moved in 1989, bridged in 2022", range(84, 88), (-75.485, 35.592, -75.455, 35.640),
     [("1978", OLD, "--"), ("2008", MOVED, "-"), ("current", NOW, "-")]),
    ("New Inlet, Pea Island, early 2012: Irene's breach", None, (-75.495, 35.672, -75.471, 35.696), []),
]
LABEL = {"1978": "Road before the move", "2008": "Road after the 1989 or 1999 move", "current": "Road today, with its bridges"}


def road(name):
    path = ROADS / name / f"nc12_{name}.geojson"
    return linemerge(list(gpd.read_file(path).to_crs(CRS).geometry))


NC_2012 = "https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_2012_2015/ImageServer/exportImage"
NEW_INLET_LL = (-75.4830, 35.6838)       # located on the 2012 photo (as in _data/hatteras_imagery.yml)


def imagery_2012(ax, window, px=1400):
    """The NC OneMap Feb-Mar 2012 orthophoto for the window, drawn in UTM 18N."""
    import io
    import urllib.request
    from PIL import Image
    w = window[2] - window[0]
    size = (px, int(px * (window[3] - window[1]) / w))
    url = (f"{NC_2012}?bbox={','.join(f'{v:.1f}' for v in window)}&bboxSR=32618&imageSR=32618"
           f"&size={size[0]},{size[1]}&format=jpgpng&f=image")
    for _ in range(4):
        try:
            img = Image.open(io.BytesIO(urllib.request.urlopen(url, timeout=180).read())).convert("RGB")
            break
        except Exception:
            continue
    ax.imshow(np.asarray(img), extent=(window[0], window[2], window[1], window[3]), interpolation="bilinear", zorder=0)


def imagery(ax, window, zoom=15):
    cx.set_cache_dir(str(TILE_CACHE))
    w, s, e, n = transform_bounds(CRS, "EPSG:3857", *window)
    img, ext = cx.bounds2img(w, s, e, n, zoom=zoom, source=cx.providers.Esri.WorldImagery, ll=False)
    img, ext = cx.warp_tiles(img, ext, t_crs=CRS)
    ax.imshow(img, extent=ext, interpolation="bilinear", zorder=0)


def main():
    apply_style()
    style.apply(size=None)        # the site's font over the house sizes
    reloc = pd.read_csv(RELOC).set_index("domain")
    lines = {k: road(k) for k in ("1978", "2008", "current")}

    fig, axes = plt.subplots(1, 3, figsize=(9.6, 5.2), layout="constrained")
    for k, (ax, (title, doms, (lon0, lat0, lon1, lat1), draw)) in enumerate(zip(axes, PANELS)):
        x0, y0 = to_utm(lon0, lat0)
        x1, y1 = to_utm(lon1, lat1)
        # equal-aspect window: widen the narrower side so the panel is 0.75 wide per 1 tall
        cxm, cym, h = (x0 + x1) / 2, (y0 + y1) / 2, y1 - y0
        w = max(x1 - x0, 0.75 * h)
        h = w / 0.75
        win = (cxm - w / 2, cym - h / 2, cxm + w / 2, cym + h / 2)
        if draw:
            imagery(ax, win)
        else:
            imagery_2012(ax, win)
            bx, by = to_utm(*NEW_INLET_LL)
            ax.annotate("the breach, with the\ntemporary bridge across it", (bx, by), xytext=(-25, -95),
                        textcoords="offset points", ha="center", va="top", **TEXT,
                        arrowprops=dict(arrowstyle="-", color="white", lw=0.8, shrinkA=0, shrinkB=4))
        clip = box(*win)
        for key, color, ls in draw:
            g = lines[key].intersection(clip)
            for part in getattr(g, "geoms", [g]):
                if part.is_empty:
                    continue
                xs, ys = part.xy
                ax.plot(xs, ys, color="0.1", lw=3.4 if ls == "-" else 3.0, zorder=3)
                ax.plot(xs, ys, color=color, lw=1.8, ls=(0, (3, 2)) if ls == "--" else "-", zorder=4)
        if doms is not None:
            most = reloc.loc[[d for d in doms if d in reloc.index], "mean_signed_landward_m"].max()
            ax.text(0.04, 0.05, f"moved up to about {5 * round(most / 5):.0f} m inland", transform=ax.transAxes,
                    ha="left", va="bottom", **TEXT)
        ax.set_xlim(win[0], win[2])
        ax.set_ylim(win[1], win[3])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"({chr(97 + k)}) {title}", fontsize=9, loc="left")
        spines_for_image(ax)
        scale_bar_km(ax, 1000, x=0.06, y=0.9, text_kw=dict(color="white", path_effects=HALO), unit="m")

    handles = [Line2D([], [], color=c, lw=1.8, ls=(0, (3, 2)) if k == "1978" else "-", label=LABEL[k],
                      path_effects=[mpl.patheffects.withStroke(linewidth=3.4, foreground="0.1")])
               for k, c in (("1978", OLD), ("2008", MOVED), ("current", NOW))]
    fig.legend(handles=handles, loc="outside lower center", ncol=3, **MAP_LEGEND)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, pil_kwargs={"quality": 88})
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
