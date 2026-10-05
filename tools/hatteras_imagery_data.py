"""
Aerial photos for the before/after slider on the Hatteras stakeholder pages, saved once and served from the site.

    python tools/hatteras_imagery_data.py [--only SPOT] [--force]

Reads the places and layers in _data/hatteras_imagery.yml and writes one JPEG per place and layer to
assets/hatteras/img/compare/<spot>/<layer>.jpg, all on the same Web Mercator box, plus
assets/hatteras/data/imagery_compare.json listing what was saved. NC OneMap year services render on
request and can take a minute or fail, so each export is retried and existing files are kept unless --force.
All layers are public domain (NC OneMap: free to use without restriction; NOAA NGS: US government work;
USGS film frames: public domain, credit USGS).

USGS film layers (usgs_frames: <year>) are read from the local copy of the Henderson release (scanned
1978-2002 frames, one zip per frame, NC State Plane feet), so they only build where that drive is mounted.
The frames a place needs are unzipped once into FRAME_CACHE, then warped onto the place's box.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-05
"""
import argparse
import glob
import io
import json
import math
import os
import time
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import yaml
from PIL import Image

SITE = Path(__file__).resolve().parents[1]
CONFIG = SITE / "_data/hatteras_imagery.yml"
IMG = SITE / "assets/hatteras/img/compare"
OUT = SITE / "assets/hatteras/data/imagery_compare.json"
NCONEMAP = "https://services.nconemap.gov/secure/rest/services/Imagery/"
R = 6378137.0
VIEW_PX = (1200, 720)   # the slider's view at the place's zoom, in screen pixels
SCALE = 1.5             # saved sharper than the view, for wide screens
QUALITY = 82
TRIES, TIMEOUT_S = 4, 180
FRAME_CACHE = Path.home() / ".cascade/usgs_frames"  # unzipped film frames, ~170 MB each
FRAME_TRIM = 0.07      # share of each film edge dropped: black border, fiducials, date and scale strip
FRAME_TRIM_YEAR = {"1978": 0.035}  # 1978 frames barely overlap and carry no strip, so take less
FRAME_DARK = 25        # grey level below which a blob touching the kept edge is film, not photo
FRAME_SIZE_PX = 11500  # typical frame width; only used to pick candidate frames from the world file


def merc(lat, lon):
    return R * math.radians(lon), R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def box(spot):
    """Web Mercator [x0, y0, x1, y1] of the slider view for a place."""
    x, y = merc(*spot["centre"])
    res = 2 * math.pi * R / (256 * 2 ** spot["zoom"])
    hw, hh = VIEW_PX[0] * res / 2, VIEW_PX[1] * res / 2
    return [x - hw, y - hh, x + hw, y + hh]


def fetch(url):
    last = None
    for k in range(TRIES):
        try:
            data = urllib.request.urlopen(url, timeout=TIMEOUT_S).read()
            return Image.open(io.BytesIO(data)).convert("RGBA")
        except Exception as e:  # slow or failed render: wait and retry
            last = e
            time.sleep(10 * (k + 1))
    raise RuntimeError(f"{url[:100]}... failed {TRIES} times: {last}")


def export_nconemap(service, b, size):
    url = (f"{NCONEMAP}{service}/ImageServer/exportImage?bbox={','.join(f'{v:.2f}' for v in b)}"
           f"&bboxSR=3857&imageSR=3857&size={size[0]},{size[1]}&format=png&f=image")
    return fetch(url)


def export_xyz(template, b, size):
    """Stitch XYZ tiles over the box at the zoom closest to the requested size, then crop and resize."""
    width_m = b[2] - b[0]
    z = max(0, min(19, round(math.log2(2 * math.pi * R * size[0] / (256 * width_m)))))
    tile_m = 2 * math.pi * R / 2 ** z
    tx0, tx1 = int((b[0] + math.pi * R) // tile_m), int((b[2] + math.pi * R) // tile_m)
    ty0, ty1 = int((math.pi * R - b[3]) // tile_m), int((math.pi * R - b[1]) // tile_m)
    mosaic = Image.new("RGBA", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            try:
                t = fetch(template.replace("{z}", str(z)).replace("{x}", str(tx)).replace("{y}", str(ty)))
                mosaic.paste(t, ((tx - tx0) * 256, (ty - ty0) * 256))
            except RuntimeError:
                pass  # outside the flight: left transparent
    px = 256 / tile_m
    left = (b[0] + math.pi * R - tx0 * tile_m) * px
    top = (math.pi * R - b[3] - ty0 * tile_m) * px
    crop = mosaic.crop((round(left), round(top), round(left + width_m * px), round(top + (b[3] - b[1]) * px)))
    return crop.resize(size, Image.LANCZOS)


def frame_tif(zpath):
    """The frame's GeoTIFF + world file, unzipped once into the cache."""
    name = Path(zpath).stem
    tif = FRAME_CACHE / f"{name}.tif"
    if not tif.exists():
        FRAME_CACHE.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zpath) as zf:
            for member in zf.namelist():
                if member.lower().endswith((".tif", ".tfw")) and "__MACOSX" not in member:  # skip macOS resource forks
                    out = FRAME_CACHE / (name + Path(member).suffix.lower())
                    with zf.open(member) as src, open(f"{out}.part", "wb") as dst:
                        while chunk := src.read(1 << 24):
                            dst.write(chunk)
                    os.replace(f"{out}.part", out)
    return tif


def frame_mask(arr, trim=FRAME_TRIM):
    """Photo pixels of a scanned frame. The film sits rotated inside the raster, with its border, fiducials and
    the burned-in date and scale strip along its own edges, so the mask is the film's rotated rectangle
    shrunk by `trim` on every side."""
    from rasterio.features import rasterize
    from scipy import ndimage
    from shapely.affinity import scale
    from shapely.geometry import MultiPoint
    k = 8  # worked at 1/8 resolution, then scaled back up
    small = arr[::k, ::k]
    rows, cols = np.nonzero(small)
    film = MultiPoint(np.column_stack([cols, rows])).convex_hull.minimum_rotated_rectangle
    inner = scale(film, 1 - 2 * trim, 1 - 2 * trim, origin="centroid")
    keep = rasterize([inner], out_shape=small.shape).astype(bool) & (small > 0)
    dark, _ = ndimage.label(small < FRAME_DARK)  # fiducial marks cut into the kept edge
    edge = keep & ~ndimage.binary_erosion(keep)
    keep &= ~np.isin(dark, np.unique(dark[edge & (dark > 0)]))
    full = np.repeat(np.repeat(keep, k, 0), k, 1)
    return full[:arr.shape[0], :arr.shape[1]]


def export_usgs_frames(root, year, b, size):
    """Mosaic the year's film frames over the box: nearest frame centre first, others only fill its gaps."""
    import rasterio
    from rasterio.warp import reproject, Resampling
    from rasterio.transform import from_bounds
    from pyproj import Transformer
    to_merc = Transformer.from_crs("EPSG:2264", "EPSG:3857", always_xy=True)
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    frames = []
    for z in sorted(glob.glob(f"{root}/{year}/{year}_georef_TIF/*.zip")):
        with zipfile.ZipFile(z) as zf:
            names = [n for n in zf.namelist() if "__MACOSX" not in n]
            tfw = [n for n in names if n.lower().endswith(".tfw")]
            if not tfw or not any(n.lower().endswith(".tif") for n in names):
                continue  # a few zips hold only the world file
            a, d, bb, e, c, f = [float(v) for v in zf.read(tfw[0]).split()]
        corners = [to_merc.transform(c + a * i + bb * j, f + d * i + e * j)
                   for i, j in [(0, 0), (FRAME_SIZE_PX, 0), (FRAME_SIZE_PX, FRAME_SIZE_PX), (0, FRAME_SIZE_PX)]]
        xs, ys = [p[0] for p in corners], [p[1] for p in corners]
        if max(xs) < b[0] or min(xs) > b[2] or max(ys) < b[1] or min(ys) > b[3]:
            continue
        frames.append((math.hypot(sum(xs) / 4 - cx, sum(ys) / 4 - cy), z))
    if not frames:
        raise RuntimeError(f"no {year} frames over this place")
    dst_tr = from_bounds(*b, size[0], size[1])
    grey = np.zeros((size[1], size[0]), np.uint8)
    for _, z in sorted(frames):
        tile = np.zeros_like(grey)
        with rasterio.open(frame_tif(z)) as src:
            arr = src.read(1)
            arr[~frame_mask(arr, FRAME_TRIM_YEAR.get(str(year), FRAME_TRIM))] = 0
            reproject(arr, tile, src_transform=src.transform, src_crs="EPSG:2264", dst_transform=dst_tr,
                      dst_crs="EPSG:3857", src_nodata=0, dst_nodata=0, resampling=Resampling.average)
        gap = grey == 0
        grey[gap] = tile[gap]
        if not (grey == 0).any():
            break
    img = Image.fromarray(grey).convert("RGBA")
    img.putalpha(Image.fromarray(np.where(grey > 0, 255, 0).astype(np.uint8)))
    return img


def save(img, path):
    """No-data becomes the house water colour, so gaps read as water rather than black."""
    ground = Image.new("RGBA", img.size, (168, 200, 224, 255))
    ground.alpha_composite(img)
    path.parent.mkdir(parents=True, exist_ok=True)
    ground.convert("RGB").save(path, "JPEG", quality=QUALITY, optimize=True, progressive=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    size = (round(VIEW_PX[0] * SCALE), round(VIEW_PX[1] * SCALE))
    saved = {}
    for spot in cfg["spots"]:
        b = box(spot)
        saved[spot["id"]] = []
        for layer in cfg["layers"]:
            path = IMG / spot["id"] / f"{layer['id']}.jpg"
            if spot["id"] == args.only or args.only is None:
                if args.force or not path.exists():
                    t = time.time()
                    try:
                        if layer.get("usgs_frames"):
                            img = export_usgs_frames(cfg["usgs_frames_root"], layer["usgs_frames"], b, size)
                        elif layer.get("xyz"):
                            img = export_xyz(layer["xyz"], b, size)
                        else:
                            img = export_nconemap(layer["nconemap"], b, size)
                        save(img, path)
                        print(f"{spot['id']}/{layer['id']}: {path.stat().st_size // 1024} KB, {time.time() - t:.0f} s")
                    except RuntimeError as e:
                        print(f"{spot['id']}/{layer['id']}: NOT SAVED ({e})")
            if path.exists():
                saved[spot["id"]].append(layer["id"])
    OUT.write_text(json.dumps({"size": size, "saved": saved}, separators=(",", ":")), encoding="utf-8")
    missing = {s: [l["id"] for l in cfg["layers"] if l["id"] not in v] for s, v in saved.items()}
    print("missing:", {s: m for s, m in missing.items() if m} or "none")


if __name__ == "__main__":
    main()
