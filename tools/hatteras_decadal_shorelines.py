"""
Average shorelines every ten years, for the "Shorelines through time" page of the Hatteras stakeholder pages.

    python tools/hatteras_decadal_shorelines.py

For each transect on the shoreline map (Cape Point to Oregon Inlet), the mean CoastSat shoreline position over each
of the calendar years 1985, 1995, 2005, 2015 and 2025, placed along the transect from its landward end. A transect
needs MIN_OBS positions in a year to get a point. Points are
joined into lines south to north, broken wherever a transect has no point or neighbours are far apart (inlets).
Hannah's choice (2026-10-03): one calendar year each (was +-2 years). SPOTS are the zoom buttons: the stretches
with the largest 1985-2025 change, and stretches that stayed put in every year for comparison, each with its mean
change over the 1 km around it. Writes assets/hatteras/data/decadal_shorelines.json.
Uses the loaders of tools/hatteras_shoreline_data.py; needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import json

import numpy as np
from pyproj import Transformer

import hatteras_shoreline_data as sd

YEARS = [1985, 1995, 2005, 2015, 2025]
HALF = 0                             # years either side of each year: 0 is the calendar year alone
MIN_OBS = 3
SPOTS = [("Cape Point", 0.5, "change"), ("Buxton", 3.5, "change"), ("North of Avon", 14.5, "change"),
         ("Rodanthe", 39.5, "change"), ("Pea Island", 53.5, "change"),
         # stable for comparison: the shoreline stayed within ~20 m of its 1985 place in every one of the five years
         ("South of Avon", 10.5, "stable"), ("Avon to Salvo", 22.5, "stable"), ("North of Rodanthe", 45.5, "stable")]
MAX_GAP_M = 200.0                    # neighbours further apart than this along the shore break the line
OUT = sd.OUT / "decadal_shorelines.json"
to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32618", always_xy=True).transform
to_ll = Transformer.from_crs("EPSG:32618", "EPSG:4326", always_xy=True).transform


def main():
    rates = json.loads((sd.OUT / "shoreline_rates.json").read_text(encoding="utf-8"))
    transects = rates["transects"]              # south to north, the same order as the map
    pts = {y: [] for y in YEARS}
    counts = {y: 0 for y in YEARS}
    change = []                                 # (km, last minus first year in m, transect-middle lat, lon)
    for t in transects:
        date, pos = sd.load_series(t["id"])
        yr = date.dt.year.values
        (lx, ly), (sx, sy) = t["line"]
        a, b = np.array(to_utm(lx, ly)), np.array(to_utm(sx, sy))
        u = (b - a) / np.linalg.norm(b - a)
        means = {}
        for y in YEARS:
            sel = pos[(yr >= y - HALF) & (yr <= y + HALF)]
            if len(sel) >= MIN_OBS:
                means[y] = float(sel.mean())
                x, yy = a + u * means[y]
                pts[y].append((t["km"], x, yy))
                counts[y] += 1
            else:
                pts[y].append(None)
        if YEARS[0] in means and YEARS[-1] in means:
            change.append((t["km"], means[YEARS[-1]] - means[YEARS[0]], (ly + sy) / 2, (lx + sx) / 2))

    lines = {}
    for y in YEARS:
        segs, cur, last = [], [], None
        for p in pts[y]:
            if p is None or (last is not None and np.hypot(p[1] - last[1], p[2] - last[2]) > MAX_GAP_M):
                if len(cur) > 1:
                    segs.append(cur)
                cur, last = [], None
                if p is None:
                    continue
            lon, lat = to_ll(p[1], p[2])
            cur.append([round(lat, 6), round(lon, 6)])
            last = p
        if len(cur) > 1:
            segs.append(cur)
        lines[str(y)] = segs
        print(f"  {y}: {counts[y]} of {len(transects)} transects, {len(segs)} line pieces")

    ch = np.array(change)
    spots = []
    for name, km, kind in SPOTS:
        m = np.abs(ch[:, 0] - km) <= 0.5
        spots.append({"name": name, "kind": kind, "ll": [round(float(ch[m, 2].mean()), 5), round(float(ch[m, 3].mean()), 5)],
                      "change": int(5 * round(float(ch[m, 1].mean()) / 5))})
        print(f"  {name}: {spots[-1]['change']:+d} m from {YEARS[0]} to {YEARS[-1]}")
    out = {"source": f"CoastSat (Vos et al.) shorelines: mean position per transect over {2 * HALF + 1} year(s) centred on "
                     "each year, placed along the transect", "years": YEARS, "half_window": HALF,
           "record_end": rates["record_end"], "lines": lines, "places": rates["places"], "spots": spots}
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT.name} ({OUT.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
