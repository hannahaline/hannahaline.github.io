"""
Data for the model-versus-observed panel on The model page of the Hatteras stakeholder pages.

    python tools/hatteras_model_data.py

Writes assets/hatteras/data/model_vs_observed.json: for each model period (1996-2015, 2010-2026), the observed
shoreline change rate per 500 m stretch (GIS 1-90) and the rate in each management run of the CASCADE matrix.
Hannah's choices (2026-10-03): the zeroBE runs (no source or sink anywhere, nothing fitted), rates in m/yr (the LRR
the runner writes), the observed target smoothed over 7 stretches exactly as the runner scores it, and every
management arm. In 1996-2015 the arms with a road use the prescribed 1999 move (the road_reloc runs), so they follow
what happened; 2010-2026 has no road move. The observed target is rebuilt with CASCADE's own spliced_lowess_series and
checked against each run's recorded interior bias and RMSE; the script refuses to write on a mismatch.
Results are unpublished: the panel is shown only while hatteras_draft is on. Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
sys.path.insert(0, str(CASCADE / "scripts"))
from cascade_pipeline.coastsat_lowess import load_transect_data, spliced_lowess_series  # noqa: E402

RATES = CASCADE / "data/hatteras_init/5-scr/3-rates/coastsat/lrr"
MATRIX = CASCADE / "output/raw_runs/matrix"
SITE_RATES = SITE / "assets/hatteras/data/shoreline_rates.json"
OUT = SITE / "assets/hatteras/data/model_vs_observed.json"
WINDOW = 7
INTERIOR = range(2, 90)
TOL = 5e-4

WINDOWS = [("1996_2015", "1996–2015"), ("2010_2026", "2010–2026")]
# arm id, label, run-name token in each window
ARMS = [
    ("natural", "No management", {"1996_2015": "noroad_nobdm", "2010_2026": "noroad_nobdm"}),
    ("road", "Road kept in place", {"1996_2015": "road_reloc_nobdm", "2010_2026": "road_nobdm"}),
    ("dunes_fills", "Dunes rebuilt and beach fills, no road",
     {"1996_2015": "noroad_bdm_nourish", "2010_2026": "noroad_bdm_nourish"}),
    ("road_dunes", "Road and dunes, no beach fills",
     {"1996_2015": "road_reloc_bdm_nonourish", "2010_2026": "road_bdm_nonourish"}),
    ("full", "Full management, as it happened",
     {"1996_2015": "road_reloc_bdm_nourish", "2010_2026": "road_bdm_nourish"}),
]


def r(x, d=3):
    return None if not np.isfinite(x) else round(float(x), d)


def main():
    site = json.loads(SITE_RATES.read_text(encoding="utf-8"))
    out = {"source": "CASCADE hindcast matrix, zeroBE (no source/sink), LRR per GIS domain; observed = CoastSat LRR, "
                     f"LOWESS over {WINDOW} domains with GIS 1-10 as raw domain means (the runner's scoring target)",
           "gis": list(range(1, 91)), "km": [round((g - 0.5) * 0.5, 2) for g in range(1, 91)],
           "places": site["places"], "groin": site["groin"], "nourishments": site["nourishments"],
           "arms": [{"id": a, "label": lab} for a, lab, _ in ARMS], "windows": []}
    for key, label in WINDOWS:
        ds = SimpleNamespace(csv_path=str(RATES / key / "transect_lrr_full.csv"), domain_col="domain_number",
                             rate_col="lrr_m_yr", transect_id_col="transect_id", label=key)
        dom, lrr, along = load_transect_data(ds)
        target, _ = spliced_lowess_series(dom, along, lrr, WINDOW)
        raw = pd.Series(lrr).groupby(dom).mean().reindex(range(1, 91))
        runs = []
        for arm, _lab, token in ARMS:
            name = f"HAT_{key}_zeroBE_offsetmetres_{token[key]}_nogroin"
            d = MATRIX / key / "zeroBE" / name
            model = pd.read_csv(d / "tables/shoreline_change_rate.csv").set_index("gis_domain")["lrr_m_yr"].reindex(range(1, 91))
            skill = json.loads((d / f"{name}_run_metadata.json").read_text(encoding="utf-8"))["skill"]
            diff = model.loc[list(INTERIOR)] - target.loc[list(INTERIOR)]
            bias, rmse = float(diff.mean()), float(np.sqrt((diff ** 2).mean()))
            if abs(bias - float(skill["mean_bias_interior_m_yr"])) > TOL or abs(rmse - float(skill["rmse_interior_m_yr"])) > TOL:
                raise SystemExit(f"{name}: rebuilt target gives bias {bias:+.4f} / RMSE {rmse:.4f}, run recorded "
                                 f"{skill['mean_bias_interior_m_yr']} / {skill['rmse_interior_m_yr']}; not writing")
            runs.append({"arm": arm, "run": name, "rate": [r(v) for v in model], "bias": r(bias), "rmse": r(rmse)})
            print(f"  {key} {arm:12s} interior bias {bias:+.2f}  RMSE {rmse:.2f} m/yr")
        out["windows"].append({"key": key, "label": label, "observed": [r(v) for v in target],
                               "observed_raw": [r(v) for v in raw], "runs": runs})
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT.relative_to(SITE)} ({OUT.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
