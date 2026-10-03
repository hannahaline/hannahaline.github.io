"""
Data for the sea-level chart on the Hatteras stakeholder pages (The island).

    python tools/hatteras_sealevel_data.py

Writes assets/hatteras/data/sea_level.json: the Duck tide gauge monthly record (NOAA 8651370, seasonal cycle
removed), yearly means for complete years, NOAA's full-record trend, and the trend the model uses for each
hindcast period. Rates are read from CASCADE's fits/duck_rslr_rates.csv and refit here from the record; the
script refuses to write if the two disagree. Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
RSLR = CASCADE / "data/hatteras_init/3-env-forcings/2-rslr"
RECORD = RSLR / "record/duck_8651370_meantrend.csv"
RATES = RSLR / "fits/duck_rslr_rates.csv"
OUT = SITE / "assets/hatteras/data/sea_level.json"
PERIODS = ["1996_2015", "2010_2026"]  # the model periods, earlier first
TOL_MM_YR = 0.01


def read_record():
    # the NOAA file has four header lines before the column names
    df = pd.read_csv(RECORD, skiprows=4, skipinitialspace=True, index_col=False)  # rows end in a comma
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(subset=["Monthly_MSL"])
    df["t"] = df["Year"] + (df["Month"] - 0.5) / 12.0  # month centres, as duck_rslr_analysis.py
    return df


def main():
    df = read_record()
    rates = pd.read_csv(RATES).set_index("window")

    periods = []
    for w in PERIODS:
        r = rates.loc[w]
        fit = df[(df["Year"] >= r.start_year) & (df["Year"] <= r.end_year)]
        slope, icept = np.polyfit(fit["t"], fit["Monthly_MSL"], 1)
        if abs(slope * 1000 - r.slope_mm_yr) > TOL_MM_YR or len(fit) != r.n_months:
            raise SystemExit(f"{w}: refit {slope * 1000:.3f} mm/yr on {len(fit)} months, "
                             f"table says {r.slope_mm_yr:.3f} on {r.n_months}; not writing")
        periods.append({"id": w, "start": int(r.start_year), "end": int(r.end_year),
                        "mm_yr": round(r.slope_mm_yr, 2), "ci_mm_yr": round(r.ci95_mm_yr, 2),
                        "slope": slope, "intercept": icept, "model_m_yr": r.config_m_yr})

    noaa = df.dropna(subset=["Linear_Trend"])
    noaa_slope = np.polyfit(noaa["t"], noaa["Linear_Trend"], 1)[0]

    counts = df.groupby("Year")["Monthly_MSL"].count()
    full = counts[counts == 12].index
    yearly = df[df["Year"].isin(full)].groupby("Year")["Monthly_MSL"].mean()

    out = {
        "source": "NOAA CO-OPS station 8651370, Duck, NC: monthly mean sea level, seasonal cycle removed",
        "units": "m, relative to the station's mean sea level datum",
        "monthly": [[round(t, 3), round(v, 3)] for t, v in zip(df["t"], df["Monthly_MSL"])],
        "yearly": [[int(y), round(v, 4)] for y, v in yearly.items()],
        "partial_years": [int(y) for y in counts[counts < 12].index],
        "noaa": {"t0": round(noaa["t"].iloc[0], 3), "v0": round(noaa["Linear_Trend"].iloc[0], 4),
                 "t1": round(noaa["t"].iloc[-1], 3), "v1": round(noaa["Linear_Trend"].iloc[-1], 4),
                 "mm_yr": round(noaa_slope * 1000, 2)},
        "periods": [{k: (round(v, 8) if isinstance(v, float) else v) for k, v in p.items()} for p in periods],
    }
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"{OUT.relative_to(SITE)}: {len(out['monthly'])} months, {len(out['yearly'])} full years "
          f"({yearly.index.min()}-{yearly.index.max()}), partial {out['partial_years']}")
    for p in periods:
        print(f"  {p['id']}: {p['mm_yr']} ± {p['ci_mm_yr']} mm/yr (model uses {p['model_m_yr']} m/yr)")
    print(f"  NOAA full record: {out['noaa']['mm_yr']} mm/yr")


if __name__ == "__main__":
    main()
