"""
Data for the nourishment explorer on the Management page of the Hatteras stakeholder pages.

    python tools/hatteras_nourishment_data.py

For each nourished stretch (Rodanthe, Buxton, Avon; projects from HATTERAS_NOURISHMENT_PROJECTS), the yearly mean
CoastSat shoreline position on the stretch and on the rest of the island (every other transect on the shoreline map,
Cape Point to Oregon Inlet), each set to zero in the year before the stretch's first fill. Their difference is the
"relative to the island" view: storms and island-wide shifts such as 2021 move both and cancel. A fill's jump is
the difference from the year before the fill to the year after. Hannah's choice (2026-10-03): plain yearly means,
not CASCADE's detrended medians, so the relative view is exactly the gap between the two lines; the steps differ
from coastsat_position_attribution by under 1 m except Buxton 2022 (8.3 here, 5.0 there).
Writes assets/hatteras/data/nourishment.json. Uses the loaders of tools/hatteras_shoreline_data.py; needs the
CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import json

import pandas as pd

import hatteras_shoreline_data as sd
from site_layer.hatteras_site_config import HATTERAS_NOURISHMENT_PROJECTS

OUT = sd.OUT / "nourishment.json"
LAST_YEAR = 2025                     # the record ends in January 2026, so 2026 is left out
M3_PER_CY = 0.764555
STRETCHES = [("Rodanthe", "Rodanthe"), ("Buxton", "Buxton"), ("Avon", "Avon")]   # label, name prefix in the config


def main():
    rates = json.loads((sd.OUT / "shoreline_rates.json").read_text(encoding="utf-8"))
    T = rates["transects"]
    yearly = {}
    for t in T:
        date, pos = sd.load_series(t["id"])
        yearly[t["id"]] = pd.Series(pos.values, index=date.dt.year.values).groupby(level=0).mean()
    Y = pd.DataFrame(yearly).sort_index().loc[:LAST_YEAR]
    dom = pd.Series({t["id"]: t["d"] for t in T})
    km = pd.Series({t["id"]: t["km"] for t in T})

    out = []
    for label, prefix in STRETCHES:
        projects = sorted((p for p in HATTERAS_NOURISHMENT_PROJECTS if p.name.startswith(prefix) and p.enabled),
                          key=lambda p: p.year)
        doms = set(projects[0].gis_domains)
        assert all(set(p.gis_domains) == doms for p in projects), f"{label}: fills cover different domains"
        inside = dom.isin(doms)
        ids = inside[inside].index
        filled, rest = Y[ids].mean(axis=1), Y[inside[~inside].index].mean(axis=1)
        base = projects[0].year - 1
        filled, rest = filled - filled.loc[base], rest - rest.loc[base]
        rel = filled - rest
        length_m = round(float(km[ids].max() - km[ids].min()) * 1000 + 50)
        fills = []
        for p in projects:
            step = float(rel.loc[p.year + 1] - rel.loc[p.year - 1])
            after = {int(y): round(float(rel.loc[y] - rel.loc[p.year - 1]), 1) for y in rel.loc[p.year + 1:].index}
            fills.append({"name": p.name, "year": p.year, "volume_cy": p.volume_cubic_yards,
                          "m3_per_m": round(p.volume_cubic_yards * M3_PER_CY / length_m),
                          "step_m": round(step, 1), "since_before_m": after})
            print(f"{p.name} {p.year}: step {step:+.1f} m; latest ({LAST_YEAR}) {after[LAST_YEAR]:+.1f} m")
        out.append({"name": label, "km": [round(float(km[ids].min()), 2), round(float(km[ids].max()), 2)],
                    "length_m": length_m, "n_transects": int(len(ids)), "base_year": base,
                    "years": [int(y) for y in Y.index],
                    "filled": [None if pd.isna(v) else round(float(v), 1) for v in filled],
                    "rest": [None if pd.isna(v) else round(float(v), 1) for v in rest],
                    "fills": fills})
    doc = {"source": "CoastSat (Vos et al.) shorelines: yearly mean position per transect, averaged over the stretch and "
                     "over the rest of the island, each zero in the year before the first fill",
           "record_end": rates["record_end"], "last_year": LAST_YEAR, "island_km": [0, round(max(km), 1)],
           "places": rates["places"], "stretches": out}
    OUT.write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT.name} ({OUT.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
