"""
Data for the "Your stretch of beach" page of the Hatteras stakeholder pages.

    python tools/hatteras_stretch_data.py [--fetch]

For each of ten places along the island (the villages and the NC-12 stretches between them, as runs of 500 m model
domains), writes one summary: the shoreline change rate over the whole record and the two model periods (the mean of
the transect rates in assets/hatteras/data/shoreline_rates.json), the yearly mean shoreline position since 1984-86, the
beach fills and NC-12 moves and bridges that touched it (assets/hatteras/data/nourishment.json and timeline.json, fill
dates from CASCADE's placement-date record), the images in CASCADE's overwash record that show overwash there and the
named storms before each, and a then-and-now pair of NC OneMap photos (1993 and 2024) of 1.2 km of beach at the middle
of the place, centred 300 m landward of its recent shoreline (Hannah: show more of the island). The overwash record covers GIS 1-90 only, so Pea Island has none. Hannah asked (2026-10-04) for one page
where someone picks a place and gets a plain summary; she chose the places, the contents and a separate page.
Writes assets/hatteras/data/stretches.json and assets/hatteras/img/stretches/<id>_<year>.jpg; photos are cached under
tools/data/stretch_photos/. Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-04
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

import hatteras_imagery_data as img
import hatteras_shoreline_data as sd

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
DATA = SITE / "assets/hatteras/data"
OUT = DATA / "stretches.json"
OUT_IMG = SITE / "assets/hatteras/img/stretches"
PHOTOS = SITE / "tools/data/stretch_photos"
OVERWASH = CASCADE / "data/hatteras_init/8-overwash-analysis/1-observations"
DATES = CASCADE / "data/hatteras_init/4-mgmt-forcing/nourishment/datasets/nourishment_placement_dates.csv"
# id, name, GIS domains (inclusive), what it is
PLACES = [
    ("cape-point", "Cape Point", (1, 5), "The point and the beach north to the Buxton groins."),
    ("buxton", "Buxton", (6, 9), "Buxton village, from the groins at the old lighthouse site north."),
    ("buxton-avon", "Buxton to Avon", (10, 20), "NC-12 between the villages, past the Haulover day-use area."),
    ("avon", "Avon", (21, 31), "Avon village."),
    ("avon-salvo", "Avon to Salvo", (32, 67), "The long NC-12 stretch through the national seashore."),
    ("salvo", "Salvo", (68, 72), "Salvo village."),
    ("waves", "Waves", (73, 76), "Waves village."),
    ("rodanthe", "Rodanthe", (77, 83), "Rodanthe village, to the pier."),
    ("s-curves", "S-curves (Mirlo Beach)", (84, 89), "North of Rodanthe, where NC-12 ran right behind the beach until the Jug Handle Bridge."),
    ("pea-island", "Pea Island", (90, 120), "Pea Island National Wildlife Refuge, north to Oregon Inlet."),
]
FILL_NAMES = {("Rodanthe", 2014): "Rodanthe emergency fill", ("Buxton", 2017): "Buxton beach nourishment",
              ("Buxton", 2022): "Buxton shore protection", ("Avon", 2022): "Avon shore protection"}
PHOTO_YEARS = {1993: "DOQQ_NC_1993", 2024: "Orthoimagery_20242027"}
HALF_M = 600                             # a 1.2 km square frame
LANDWARD_M = 300                         # frame centre this far landward of the shoreline: about a quarter ocean
PX = 900


def km_range(gis):
    return (gis[0] - 1) * 0.5, gis[1] * 0.5


def overlaps(a, b):
    return a is not None and a[0] < b[1] and a[1] > b[0]


def words(rate):
    """A rate in m/yr as plain words."""
    if abs(rate) < 0.25:
        return "little change"
    way = "seaward (growing)" if rate > 0 else "landward (eroding)"
    return f"about {abs(rate):.1f} m a year {way}"


def yearly(transects):
    """Mean over the transects of each year's mean shoreline position minus that transect's 1984-86 mean."""
    rows = {}
    for t in transects:
        date, pos = sd.load_series(t["id"])
        s = pd.Series(pos.values, index=date.dt.year.values).groupby(level=0).mean()
        base = s.loc[1984:1986]
        if len(base):
            rows[t["id"]] = s - base.mean()
    df = pd.DataFrame(rows)
    keep = df.notna().sum(axis=1) >= max(3, df.shape[1] // 2)
    m = df[keep].mean(axis=1)
    return [[int(y), round(float(v), 1)] for y, v in m.items() if y <= 2025]


def storm_name(raw):
    """'SANDY (ET)' -> 'Sandy', 'STORM OF THE CENTURY' -> 'the Storm of the Century', 'DEC 1992 NOR'EASTER' -> 'the December 1992 nor'easter'."""
    s = raw.strip().title().replace("'E", "'e")
    for tag in (" (Et)", " (Extratropical)", " (Post-Tropical)"):
        s = s.replace(tag, "")
    s = s.replace(" Of The ", " of the ").replace("Nor'easter", "nor'easter").replace("Bomb Cyclone", "bomb cyclone")
    for short, full in (("Jan ", "January "), ("Dec ", "December ")):
        if s.startswith(short):
            s = full + s[len(short):]
    if s.startswith(("Storm of", "Perfect", "January", "December", "May ", "Ash")):
        s = "the " + s
    return s


def overwash_by_place():
    obs = pd.read_csv(OVERWASH / "overwash_observations.csv")
    storms = pd.read_csv(OVERWASH / "storms_by_image.csv")
    named = {k: [storm_name(r.storm) + ("" if any(c.isdigit() for c in r.storm) else f" ({str(r.last_day)[:4]})")
                 for r in g.itertuples()]
             for k, g in storms.groupby("first_image_obs_id")}
    dates = obs.drop_duplicates("Obs_ID").set_index("Obs_ID")["Imagery_Date"].to_dict()
    hit = obs[obs.overwash == 1]
    return hit, named, dates, obs.domain.max(), obs.Obs_ID.nunique()


def photo(place_id, year, centre, fetch):
    x, y = img.merc(*centre)
    k = 1 / math.cos(math.radians(centre[0]))
    box = [x - HALF_M * k, y - HALF_M * k, x + HALF_M * k, y + HALF_M * k]
    p = PHOTOS / f"{place_id}_{year}.jpg"
    if fetch or not p.exists():
        img.save(img.export_nconemap(PHOTO_YEARS[year], box, (PX, PX)), p)
        print(f"  fetched {p.name}")
    out = OUT_IMG / f"{place_id}_{year}.jpg"
    Image.open(p).convert("RGB").save(out, quality=82, optimize=True)
    return f"/assets/hatteras/img/stretches/{out.name}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--no-photos", action="store_true")
    args = ap.parse_args()
    rates = json.loads((DATA / "shoreline_rates.json").read_text(encoding="utf-8"))
    windows = [w["key"] for w in rates["windows"]]
    nx = json.loads((DATA / "nourishment.json").read_text(encoding="utf-8"))
    timeline = json.loads((DATA / "timeline.json").read_text(encoding="utf-8"))
    dates = pd.read_csv(DATES).set_index("project")
    hit, named, img_dates, last_domain, n_images = overwash_by_place()
    PHOTOS.mkdir(parents=True, exist_ok=True)
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    out = []
    for pid, name, gis, what in PLACES:
        km = km_range(gis)
        on = [t for t in rates["transects"] if km[0] <= t["km"] < km[1]]
        r = {w: round(float(np.mean([t["r"][i] for t in on])), 2) for i, w in enumerate(windows)}
        fills = []
        for st in nx["stretches"]:
            if overlaps(st["km"], km):
                for f in st["fills"]:
                    rec = dates.loc[FILL_NAMES[(st["name"], f["year"])]]
                    fills.append({"year": f["year"], "name": f["name"], "volume_cy": int(f["volume_cy"]),
                                  "placed": [str(rec.start_date), str(rec.end_date)], "stretch": st["name"]})
        events = [{"year": e["year"], "kind": e["kind"], "title": e["title"], "detail": e["detail"]}
                  for e in timeline["management"] if e["kind"] != "fill" and overlaps(e["km"], km)]
        if pid == "pea-island":
            events += [{"year": e["year"], "kind": e["kind"], "title": e["title"], "detail": e["detail"]}
                       for e in timeline["management"] if e["km"] is None and "Oregon Inlet" in e["title"]]
        ow = []
        covered = gis[0] <= last_domain and (min(gis[1], last_domain) - gis[0] + 1) >= (gis[1] - gis[0] + 1) / 2
        if covered:
            here = hit[(hit.domain >= gis[0]) & (hit.domain <= min(gis[1], last_domain))]
            for oid, g in here.groupby("Obs_ID"):
                ow.append({"image": str(img_dates[oid]), "domains": int(g.domain.nunique()), "of": int(min(gis[1], last_domain) - gis[0] + 1),
                           "storms": named.get(oid, [])})
            ow.sort(key=lambda o: o["image"])
        # centre the photo LANDWARD_M landward of the middle transect's recent shoreline, so the island fills most of the frame
        mid = on[len(on) // 2]
        (lx, ly), (sx, sy) = mid["line"]
        date, pos = sd.load_series(mid["id"])
        recent = float(pos[date.dt.year.values >= 2015].mean())
        frac = (recent - LANDWARD_M) / (math.hypot((sx - lx) * math.cos(math.radians(ly)), sy - ly) * 111320)
        centre = (ly + frac * (sy - ly), lx + frac * (sx - lx))
        photos = {} if args.no_photos else {str(y): photo(pid, y, centre, args.fetch) for y in PHOTO_YEARS}
        out.append({"id": pid, "name": name, "what": what, "gis": list(gis), "km": [km[0], km[1]], "n_transects": len(on),
                    "rate": r, "rate_words": words(r[windows[0]]), "yearly": yearly(on), "fills": fills,
                    "events": sorted(events, key=lambda e: e["year"]),
                    "overwash": ow if covered else None, "photos": photos, "centre": [round(centre[0], 5), round(centre[1], 5)]})
        print(f"{name:24s} GIS {gis[0]}-{gis[1]}: {r[windows[0]]:+.2f} m/yr, {len(fills)} fills, {len(events)} road events, "
              f"{'n/a' if ow is None else len(ow)} overwash images")
    OUT.write_text(json.dumps({"source": __doc__.split("\n")[1].strip(), "windows": rates["windows"],
                               "overwash_images": int(n_images), "overwash_last_gis": int(last_domain),
                               "photo_years": list(PHOTO_YEARS), "places": out}, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT.relative_to(SITE)}")


if __name__ == "__main__":
    main()
