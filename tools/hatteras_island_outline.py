"""
Hatteras Island as a horizontal outline, for the locator strip of the nourishment explorer.

    python tools/hatteras_island_outline.py

Takes the OpenStreetMap outline already used for the island page's diagrams (tools/data/hatteras_outline_osm.json),
keeps Cape Point to Oregon Inlet (east of Buxton Woods' west edge, so the Hatteras Village arm is left out), and
turns it so north runs to the right: each vertex's position along the island is the km north of Cape Point of the
CoastSat transect at the same latitude, so the fills and villages, which the explorer places by km, sit on the
outline; across the island is true east-west distance in metres, ocean side down. Hannah asked (2026-10-04) for the
island's outline in place of the plain bar.
Also writes the ocean shoreline of the turned outline every 250 m ("shore": [[km, metres east], ...]), the most seaward
crossing of a line across the island, so the explorer can draw a fill along the ocean side.
Writes assets/hatteras/data/island_outline.json: {"km": [...], "east_m": [...], "rings": [...], "shore": [...]}.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-04
"""
import json
import math
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Polygon, box

import hatteras_shoreline_data as sd

SITE = Path(__file__).resolve().parents[1]
OSM = SITE / "tools/data/hatteras_outline_osm.json"
OUT = SITE / "assets/hatteras/data/island_outline.json"
WEST_LON = -75.545                       # west edge of Buxton Woods: the Hatteras Village arm lies beyond it
SIMPLIFY_KM = 0.08


def main():
    rates = json.loads((sd.OUT / "shoreline_rates.json").read_text(encoding="utf-8"))
    tr = sorted(rates["transects"], key=lambda t: t["km"])
    lat = np.array([t["line"][1][1] for t in tr])       # seaward end
    km = np.array([t["km"] for t in tr])
    keep = np.r_[True, np.diff(np.maximum.accumulate(lat)) > 0]   # latitude rises with km; drop ties for interp
    lat, km = lat[keep], km[keep]
    poly = Polygon(json.loads(OSM.read_text(encoding="utf-8"))).buffer(0)
    poly = poly.intersection(box(WEST_LON, lat[0] - 0.006, -75.3, lat[-1] + 0.01))
    lon0 = -75.5
    m_per_lon = 111320 * math.cos(math.radians(35.5))
    rings = []
    for g in getattr(poly, "geoms", [poly]):
        if g.area < 1e-6:
            continue
        g = g.simplify(SIMPLIFY_KM / 111.0)
        xs, ys = g.exterior.xy
        ring = [[round(float(np.interp(y, lat, km, left=km[0] + (y - lat[0]) * 111.0, right=km[-1] + (y - lat[-1]) * 111.0)), 3),
                 round((x - lon0) * m_per_lon)] for x, y in zip(xs, ys)]
        rings.append(ring)
    turned = Polygon(rings[0]).buffer(0) if len(rings) == 1 else Polygon(max(rings, key=len)).buffer(0)
    shore = []
    for k in np.arange(0, km[-1] + 1e-9, 0.25):
        hit = turned.intersection(LineString([(k, -1e5), (k, 1e5)]))
        if not hit.is_empty:
            shore.append([round(float(k), 2), round(hit.bounds[3])])
    allx = [p[0] for r in rings for p in r]
    ally = [p[1] for r in rings for p in r]
    OUT.write_text(json.dumps({"source": "OpenStreetMap contributors (ODbL), turned so north runs right",
                               "km": [min(allx), max(allx)], "east_m": [min(ally), max(ally)], "rings": rings,
                               "shore": shore}),
                   encoding="utf-8")
    print(f"wrote {OUT.relative_to(SITE)}: {len(rings)} ring(s), {sum(map(len, rings))} points, "
          f"km {min(allx):.1f}-{max(allx):.1f}, east {min(ally)}-{max(ally)} m")


if __name__ == "__main__":
    main()
