"""
Data for the storms and management timeline on the Hatteras stakeholder pages.

    python tools/hatteras_timeline_data.py

Writes assets/hatteras/data/timeline.json: every high-water event 1984-2025 from the hindcast storm
series (peak run-up water level, duration, HURDAT2 type and name, via storm_figures.py) and the management
events (fills, NC-12 moves, bridges, the groins) from the site config and Hatteras_Management_Timelines.xlsx.
Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-02
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
sys.path.insert(0, str(CASCADE / "scripts"))
from site_layer import hat_env_forcings as env  # noqa: E402
from site_layer.hatteras_site_config import (  # noqa: E402
    HATTERAS_NOURISHMENT_PROJECTS, HATTERAS_ROAD_EVENTS)
from cascade_pipeline.roadway import BridgeEvent, RelocationEvent  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "storm_figures", CASCADE / "scripts/input_prep/3-env-forcings/3-storms/storm_figures.py")
sf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sf)

OUT = SITE / "assets/hatteras/data/timeline.json"
RATES = SITE / "assets/hatteras/data/shoreline_rates.json"
# The 2025 gauge record, so the 2010-2026 series' last year can be checked like the rest
DUCK_THROUGH_2025 = env.WATER_LEVEL_DIR / "8651370_DUCK_19840101_20251231_NAVD.csv"
# Which window's series supplies each span of years (the earliest window that holds them)
SPANS = [((1984, 2004), 1984, 1995), ((1996, 2015), 1996, 2009), ((2010, 2026), 2010, 2026)]
DOMAIN_KM = 0.5


def km(gis_first, gis_last):
    """[south, north] km north of Cape Point for an inclusive GIS domain range."""
    return [round((gis_first - 1) * DOMAIN_KM, 2), round(gis_last * DOMAIN_KM, 2)]


def load_storms(forcing):
    """All events, each from the window that covers its year; peaks and the Rhigh check as in storm_figures."""
    parts = []
    for (a, b), first, last in SPANS:
        df = pd.read_csv(env.storm_summary_file(a, b), parse_dates=["StartTime", "EndTime"])
        parts.append(df[df.calendar_year.between(first, last)])
    df = pd.concat(parts, ignore_index=True).rename(columns={"period": "tp_s"})
    df["rhigh_m"] = df.Rhigh * 10.0
    # The WIS waves end with 2024, so later events keep the series' own peak level, placed at their midpoint
    df["checked"] = df.EndTime <= forcing.index.max()
    df["peak"] = [forcing.TWL.loc[s:e].idxmax() if ok else (s + (e - s) / 2).floor("h")
                  for s, e, ok in zip(df.StartTime, df.EndTime, df.checked)]
    chk = df[df.checked]
    rebuilt = forcing.TWL.loc[chk.peak].values - sf.MHW_NAVD88
    bad = ~np.isclose(rebuilt, chk.rhigh_m, atol=0.01)
    if bad.any():
        raise RuntimeError(f"{bad.sum()} events' rebuilt water level misses the summary Rhigh: "
                           f"{chk.loc[bad, 'peak'].dt.date.tolist()[:5]}")
    trimmed = df["trimmed_from"] if "trimmed_from" in df else pd.Series(0, index=df.index)
    df["raw_hours"] = np.where(trimmed > 0, trimmed, df.duration)
    # classify reads the wave direction at the peak, which needs the forcing; unchecked events get no direction
    on = df.checked.values
    out = sf.classify(df[on].copy(), forcing)
    late = df[~on].copy()
    if len(late):
        h = sf.load_hurdat2()
        win = pd.Timedelta(hours=sf.TC_WINDOW_H)
        for col in ("tc_name", "tc_status", "tc_km", "type", "name"):
            late[col] = None
        for i, t in late.peak.items():
            c = h[(h.t >= t - win) & (h.t <= t + win)]
            if not c.empty:
                r = c.loc[c.km.idxmin()]
                late.loc[i, ["tc_name", "tc_status", "tc_km"]] = [r.tc_name, r.status, r.km]
        late["type"] = np.where(late.tc_km.astype(float) <= sf.TC_NEAR_KM, "tropical", "other")
        late["name"] = np.where(late.type == "tropical", late.tc_name, None)
        out = pd.concat([out, late], ignore_index=True)
    return out


def storm_rows(df):
    rows = []
    for _, r in df.sort_values("peak").iterrows():
        rows.append({
            "t": r.peak.strftime("%Y-%m-%dT%H:00"),
            "y": round(r.peak.year + (r.peak.dayofyear - 1 + r.peak.hour / 24) / 365.25, 4),
            "wl": round(float(r.rhigh_m), 2),
            "h": int(r.raw_hours),
            "type": r["type"],
            "name": sf.label_text(r) if r["type"] == "tropical" else None,
            **({} if r.checked else {"unchecked": True}),
        })
    return rows


def bridge_rows():
    """Bridge openings from the timeline sheet's Active_Bridge_Notes column, keyed by year."""
    x = pd.read_excel(CASCADE / "data/hatteras_init/4-mgmt-forcing/Hatteras_Management_Timelines.xlsx",
                      sheet_name="Bridge_Timeline", header=None)
    head = x.index[x.iloc[:, 0].astype(str) == "Year"][0]
    notes = {}
    for _, r in x.iloc[head + 1:].iterrows():
        y, note = str(r.iloc[0])[:4], r.iloc[1]
        if y.isdigit() and isinstance(note, str) and note.strip():
            notes[int(y)] = note.strip()
    return notes


def new_inlet_km():
    """km north of Cape Point of the transect nearest New Inlet (located on the 2012 photo, 35.6838 N)."""
    t = json.loads(RATES.read_text(encoding="utf-8"))["transects"]
    k = min(t, key=lambda s: abs((s["line"][0][1] + s["line"][1][1]) / 2 - 35.6838))
    return round(k["km"], 2)


def management_rows():
    rows = [{"year": 1969, "kind": "structure", "title": "Buxton groins built",
             "detail": "Built by the Navy at the lighthouse.", "km": km(5, 6), "model": True,
             "source": "Groin module documentation (hard-structures/groin)"}]
    for e in HATTERAS_ROAD_EVENTS:
        if isinstance(e, RelocationEvent):
            g = sorted(e.displacement_m)
            rows.append({"year": e.year, "kind": "road", "title": "NC-12 moved landward",
                         "detail": "The road was rebuilt farther from the ocean along this stretch.",
                         "km": km(g[0], g[-1]), "model": True, "source": "Site config, HATTERAS_ROAD_EVENTS"})
        elif isinstance(e, BridgeEvent):
            g = sorted(e.gis_domains)
            rows.append({"year": e.year, "kind": "bridge", "title": "Jug Handle Bridge opens",
                         "detail": "Opened 28 July 2022. NC-12 now crosses Pamlico Sound around the S-curves.",
                         "km": km(g[0], g[-1]), "model": True, "source": "Site config + timeline sheet"})
    for p in HATTERAS_NOURISHMENT_PROJECTS:
        g = sorted(p.gis_domains)
        rows.append({"year": p.year, "kind": "fill", "title": p.name,
                     "detail": f"About {p.volume_cubic_yards / 1e6:.1f} million cubic yards of sand.",
                     "km": km(g[0], g[-1]), "model": True, "source": "Site config, HATTERAS_NOURISHMENT_PROJECTS"})
    notes = bridge_rows()
    ni = new_inlet_km()
    rows.append({"year": 2011, "kind": "bridge", "title": "Temporary bridge over New Inlet",
                 "detail": "Hurricane Irene breached Pea Island; a temporary bridge carried NC-12 from October 2011.",
                 "km": [ni - 0.3, ni + 0.3], "model": False, "source": f"Timeline sheet: {notes.get(2011, '')}"})
    rows.append({"year": 2017, "kind": "bridge", "title": "Etheridge Bridge replaces the temporary bridge",
                 "detail": "A permanent bridge over New Inlet.",
                 "km": [ni - 0.3, ni + 0.3], "model": False, "source": f"Timeline sheet: {notes.get(2017, '')}"})
    rows.append({"year": 2019, "kind": "bridge", "title": "Basnight Bridge opens at Oregon Inlet",
                 "detail": "Replaced the Bonner Bridge at the north end of the island.",
                 "km": None, "model": False, "source": f"Timeline sheet: {notes.get(2019, '')}"})
    return sorted(rows, key=lambda r: (r["year"], r["kind"]))


def main():
    sf.env.DUCK_GAUGE_FILE = DUCK_THROUGH_2025 if DUCK_THROUGH_2025.exists() else env.DUCK_GAUGE_FILE
    forcing = sf.load_forcing()
    storms = load_storms(forcing)
    data = {
        "storms": storm_rows(storms),
        "storm_note": "Peak water level at the shore (tide, surge and wave run-up), estimated from the Duck "
                      "tide gauge and the WIS wave hindcast; metres above mean high water. 2025 events are "
                      "placed at their midpoint, because the wave record used to locate peaks ends with 2024.",
        "tc_km": sf.TC_NEAR_KM,
        "management": management_rows(),
        "range": [1984, 2026],
    }
    OUT.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    print(storms.type.value_counts().to_string())
    print(f"{len(data['storms'])} events {storms.peak.min().date()} to {storms.peak.max().date()}, "
          f"{len(data['management'])} management events -> {OUT}")


if __name__ == "__main__":
    main()
