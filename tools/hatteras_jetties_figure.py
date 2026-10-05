"""
The Charleston Harbor jetties, Morris Island and Folly Beach, for the Groins page of the Hatteras stakeholder pages.

    python tools/hatteras_jetties_figure.py

A USDA NAIP aerial (public domain; 18 April 2023, the few tiles it lacks offshore filled from 26 April 2021) of the
harbour entrance, with the two jetties, the Morris Island Lighthouse, Morris Island, Lighthouse Inlet and the north end
of Folly Beach labelled. Facts behind the labels: the jetties were authorised in 1878 and built 1882-1895 (US Army Corps
of Engineers, Charleston District); the lighthouse was completed on Morris Island in 1876 and by 1982 stood "completely
surrounded by water about 500 feet off the shore", the erosion put down to the jetties (National Register nomination,
1982); a 1987 Corps of Engineers Section 111 study put about 57% of Folly Beach's erosion down to the harbour's
navigation works. Hannah asked (2026-10-04) for an annotated aerial of the jetties for the "elsewhere" examples.
The jetty and place positions were read off the photo; the lighthouse is placed from its coordinates.
Writes assets/hatteras/img/charleston_jetties.jpg; the photo mosaic is cached in tools/data/charleston_naip.jpg.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-04
"""
import json
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import hatteras_imagery_data as img
import hatteras_fig_style as style

SITE = Path(__file__).resolve().parents[1]
CACHE = SITE / "tools/data/charleston_naip.jpg"
OUT = SITE / "assets/hatteras/img/charleston_jetties.jpg"
LON0, LAT0, LON1, LAT1 = -79.925, 32.668, -79.800, 32.758
W = 1400
FLIGHTS = ["2023-04-18", "2021-04-26"]          # the first fills the frame; the second fills its gaps
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
TOKEN = "https://planetarycomputer.microsoft.com/api/sas/v1/token/naip"   # one read token for every tile
LIGHTHOUSE = (32.6953, -79.8836)                 # lat, lon
# px in the W-wide frame, read off the 2023 photo
NORTH_JETTY = (1080, 200)
CROP = (0, 0, 1290, 960)                         # NAIP is not flown over open water: keep the part both flights cover
SOUTH_JETTY = (940, 372)


def mosaic():
    import rasterio
    from rasterio.transform import from_bounds
    from rasterio.warp import Resampling, reproject
    x0, y0 = img.merc(LAT0, LON0)
    x1, y1 = img.merc(LAT1, LON1)
    h = int(W * (y1 - y0) / (x1 - x0))
    dst = np.zeros((3, h, W), np.uint8)
    t = from_bounds(x0, y0, x1, y1, W, h)
    token = json.load(urllib.request.urlopen(TOKEN, timeout=120))["token"]
    for day in FLIGHTS:
        body = json.dumps({"collections": ["naip"], "bbox": [LON0, LAT0, LON1, LAT1],
                           "datetime": f"{day}T00:00:00Z/{day}T23:59:59Z", "limit": 50}).encode()
        req = urllib.request.Request(STAC, data=body, headers={"Content-Type": "application/json"})
        for it in json.load(urllib.request.urlopen(req, timeout=120))["features"]:
            href = it["assets"]["image"]["href"] + "?" + token
            with rasterio.open(href, OVERVIEW_LEVEL=2) as src:
                part = np.zeros_like(dst)
                for b in range(3):
                    reproject(rasterio.band(src, b + 1), part[b], dst_transform=t, dst_crs="EPSG:3857",
                              resampling=Resampling.bilinear)
                empty = dst.sum(axis=0) == 0
                dst[:, empty] = part[:, empty]
    return Image.fromarray(np.moveaxis(dst, 0, -1))


def px(lat, lon, h):
    x0, y0 = img.merc(LAT0, LON0)
    x1, y1 = img.merc(LAT1, LON1)
    x, y = img.merc(lat, lon)
    return (x - x0) / (x1 - x0) * W, (y1 - y) / (y1 - y0) * h


def main():
    style.apply()
    if not CACHE.exists():
        mosaic().save(CACHE, quality=90)
    full_h = Image.open(CACHE).height
    photo = Image.open(CACHE).crop(CROP)
    h = photo.height
    x0, y0 = img.merc(LAT0, LON0)
    x1, _ = img.merc(LAT1, LON1)
    m_per_px = (x1 - x0) / W * np.cos(np.radians((LAT0 + LAT1) / 2))
    halo = [pe.withStroke(linewidth=3, foreground="#1a1a1a")]
    t = dict(color="white", path_effects=halo)
    arrow = dict(arrowstyle="-|>", color="white", lw=1.4, path_effects=halo)
    fig, ax = plt.subplots(figsize=(8, 8 * h / photo.width))
    ax.imshow(photo, interpolation="lanczos")
    ax.set_xlim(0, photo.width)
    ax.set_ylim(h, 0)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#1a1a1a")
        s.set_linewidth(1.2)
    lx, ly = px(*LIGHTHOUSE, full_h)
    ax.add_patch(plt.Circle((lx, ly), 16, fill=False, ec="#ffd23f", lw=2.2, path_effects=halo))
    ax.annotate("Morris Island Lighthouse:\nbuilt on the island in 1876,\nnow standing in the water", xy=(lx + 14, ly + 10),
                xytext=(600, 880), ha="left", va="center", fontsize=10, fontweight="bold", arrowprops=arrow, **t)
    ax.annotate("", xy=NORTH_JETTY, xytext=(1060, 600), arrowprops=arrow)
    ax.annotate("", xy=SOUTH_JETTY, xytext=(1030, 600), arrowprops=arrow)
    ax.text(1045, 610, "Charleston Harbor jetties,\nbuilt 1882–1895", ha="center", va="top", fontsize=10.5,
            fontweight="bold", **t)
    ax.text(820, 210, "harbor\nentrance", ha="center", va="center", fontsize=9.5, fontstyle="italic", **t)
    ax.text(870, 40, "Sullivan's Island", ha="center", va="center", fontsize=9.5, **t)
    ax.text(520, 560, "Morris\nIsland", ha="center", va="center", fontsize=10.5, fontweight="bold", **t)
    ax.annotate("Folly Beach\n(continues south)", xy=(425, 952), xytext=(250, 900), ha="center", va="center", fontsize=10.5,
                fontweight="bold", arrowprops=arrow, **t)
    ax.annotate("Lighthouse\nInlet", xy=(385, 850), xytext=(220, 780), ha="center", va="center", fontsize=9.5,
                arrowprops=arrow, **t)
    bar = 1000 / m_per_px
    bx = photo.width - 40 - bar                    # open water, bottom right
    ax.plot([bx, bx + bar], [h - 40, h - 40], color="white", lw=3.5, solid_capstyle="butt", path_effects=halo)
    ax.text(bx + bar / 2, h - 52, "1 km", ha="center", va="bottom", fontsize=9.5, **t)
    ax.annotate("N", xy=(1245, 30), xytext=(1245, 95), ha="center", va="center", fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.6, path_effects=halo), **t)
    fig.savefig(OUT, dpi=170, bbox_inches="tight", pad_inches=0.03, pil_kwargs={"quality": 85, "optimize": True})
    print(f"wrote {OUT.relative_to(SITE)} ({h} px tall, {m_per_px:.1f} m/px)")


if __name__ == "__main__":
    main()
