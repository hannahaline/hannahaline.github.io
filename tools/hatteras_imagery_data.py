"""
Aerial photos for the before/after slider on the Hatteras stakeholder pages, saved once and served from the site.

    python tools/hatteras_imagery_data.py [--only SPOT] [--force]

Reads the places and layers in _data/hatteras_imagery.yml and writes one JPEG per place and layer to
assets/hatteras/img/compare/<spot>/<layer>.jpg, all on the same Web Mercator box, plus
assets/hatteras/data/imagery_compare.json listing what was saved. NC OneMap year services render on
request and can take a minute or fail, so each export is retried and existing files are kept unless --force.
All layers are public domain (NC OneMap: free to use without restriction; NOAA NGS: US government work).

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-02
"""
import argparse
import io
import json
import math
import time
import urllib.request
from pathlib import Path

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
                        img = (export_xyz(layer["xyz"], b, size) if layer.get("xyz")
                               else export_nconemap(layer["nconemap"], b, size))
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
