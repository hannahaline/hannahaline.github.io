"""
Year-by-year shoreline positions for the time player on the Hatteras shoreline map (/hatteras/shoreline-change/).

    python tools/hatteras_shoreline_years.py

Writes assets/hatteras/data/shoreline_years.json: for every transect on the rate map, how far its shoreline sat
seaward (+) or landward (-) of its 1984-86 average in each calendar year 1984-2025. Each value is the mean of
that year's CoastSat positions, smoothed along the island exactly as the rate profile is (7-domain LOWESS,
GIS 1-10 as domain means). A year with fewer than MIN_PER_YEAR shorelines at a transect is left empty. The
baseline is three years because 1984 alone has about five shorelines per transect. 2026 is left out (only
January). Uses the loaders of tools/hatteras_shoreline_data.py, so the transects match shoreline_rates.json.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import json

import numpy as np

import hatteras_shoreline_data as sd

YEARS = list(range(1984, 2026))
BASELINE = (1984, 1986)
MIN_PER_YEAR = 2
OUT = sd.OUT / "shoreline_years.json"


def main():
    frame = sd.load_frame()
    lines = sd.load_lines(frame.transect_id)
    frame = frame[frame.transect_id.isin(lines)].reset_index(drop=True)  # the rate map drops the same ones
    ids = frame.transect_id.tolist()

    raw = np.full((len(YEARS), len(ids)), np.nan)
    for k, tid in enumerate(ids):
        date, pos = sd.load_series(tid)
        yr = date.dt.year.values
        base = pos[(yr >= BASELINE[0]) & (yr <= BASELINE[1])]
        if len(base) < MIN_PER_YEAR:
            continue
        ref = base.mean()
        for i, y in enumerate(YEARS):
            p = pos[yr == y]
            if len(p) >= MIN_PER_YEAR:
                raw[i, k] = p.mean() - ref

    domains = frame.domain_number.values
    along = sd.along_coast(domains)
    smoothed = np.vstack([sd.smooth(domains, along, raw[i]) for i in range(len(YEARS))])

    rates = json.loads((sd.OUT / "shoreline_rates.json").read_text(encoding="utf-8"))
    if [t["id"] for t in rates["transects"]] != ids:
        raise SystemExit("transects differ from shoreline_rates.json; re-run hatteras_shoreline_data.py first")

    finite = smoothed[np.isfinite(smoothed)]
    out = {
        "source": "CoastSat (Vos et al.) shorelines: yearly mean position minus the transect's 1984-86 mean, "
                  "smoothed alongshore with a 7-domain (3.5 km) LOWESS, GIS 1-10 domain means",
        "years": YEARS,
        "baseline": list(BASELINE),
        "v": [[None if not np.isfinite(x) else round(float(x), 1) for x in row] for row in smoothed],
    }
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    empty = int(np.isnan(smoothed).sum())
    print(f"{OUT.name}: {len(YEARS)} years x {len(ids)} transects, {empty} empty cells, "
          f"range {finite.min():+.0f} to {finite.max():+.0f} m, {OUT.stat().st_size / 1e3:.0f} kB")
    for y in (1990, 2000, 2010, 2020, 2025):
        row = smoothed[YEARS.index(y)]
        print(f"  {y}: median {np.nanmedian(row):+.1f} m, 5th {np.nanpercentile(row, 5):+.1f}, 95th {np.nanpercentile(row, 95):+.1f}")


if __name__ == "__main__":
    main()
