"""
How far each beach fill moved the shoreline, and how long the added width lasted, for the Shoreline change page.

    python tools/hatteras_fill_steps.py

Uses CASCADE's detrended CoastSat position matrix (5-scr/1-observations/detrended_position) and the same method as
coastsat_position_attribution.test_nourishment: the change in the filled domains from the year before the fill to the
year after, minus the same change over the rest of the island. Fills come from HATTERAS_NOURISHMENT_PROJECTS, so
Buxton 2017 is included (the CASCADE table, attribution_nourishment.csv, predates it). Also writes the difference for
every year after the fill. Reads CASCADE, writes only tools/data/fill_steps.csv here. Needs the CASCADE repo beside
this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import sys
from pathlib import Path

import pandas as pd

SITE = Path(__file__).resolve().parents[1]
SCRIPTS = SITE.parent / "CASCADE" / "scripts"
for p in (SCRIPTS, SCRIPTS / "input_prep/5-scr/lib", SCRIPTS / "input_prep/5-scr/1-observations/detrended_position"):
    sys.path.insert(0, str(p))
from site_layer.hatteras_site_config import HATTERAS_NOURISHMENT_PROJECTS  # noqa: E402
import coastsat_position_attribution as attribution  # noqa: E402

OUT = SITE / "tools/data/fill_steps.csv"


def main():
    M = attribution.load_matrix()
    dom = attribution.domains_of(M.columns)
    rows = []
    for p in HATTERAS_NOURISHMENT_PROJECTS:
        y = p.year
        inside = dom.isin(list(p.gis_domains)).to_numpy()
        filled, rest = M.loc[:, inside].mean(axis=1), M.loc[:, ~inside].mean(axis=1)
        base = filled.loc[y - 1] - rest.loc[y - 1]
        for t in range(y - 1, int(M.index.max()) + 1):
            rows.append({"project": p.name, "fill_year": y, "year": t, "n_transects": int(inside.sum()),
                         "filled_minus_rest_m": round(float(filled.loc[t] - rest.loc[t] - base), 1)})
    out = pd.DataFrame(rows)
    OUT.parent.mkdir(exist_ok=True)
    out.to_csv(OUT, index=False)
    for (name, y), g in out.groupby(["project", "fill_year"], sort=False):
        step = g.set_index("year")["filled_minus_rest_m"]
        print(f"{name} {y}: step {step.loc[y + 1]:+.1f} m (year after); by year " +
              " ".join(f"{t}:{v:+.0f}" for t, v in step.items()))


if __name__ == "__main__":
    main()
