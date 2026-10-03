"""
Data for the shoreline change map on the Hatteras stakeholder pages (/hatteras/shoreline-change/).

    python tools/hatteras_shoreline_data.py

Writes assets/hatteras/data/shoreline_rates.json (every transect's line, rate per window and
7-domain LOWESS, plus villages, nourishments and NC-12) and timeseries/d<NNN>.json (positions by
domain, loaded on click). Rates are refit from the CoastSat time series with the CASCADE LRR fit and
checked against the published lrr/<window>/ tables; Pea Island (GIS 91-115) has no table for these
windows, so its fit is the only one. Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-02
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer
from scipy import stats
from shapely.geometry import LineString

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
sys.path.insert(0, str(CASCADE / "scripts"))
from cascade_pipeline.coastsat_lowess import compute_domain_means, lowess_transect_values  # noqa: E402
from site_layer.hatteras_site_config import HATTERAS_NOURISHMENT_PROJECTS  # noqa: E402

SCR = CASCADE / "data/hatteras_init/5-scr"
FRAME = SCR / "2-transect-frame/transect_domains"
SERIES = SCR / "1-observations/coastsat_timeseries"
LRR = SCR / "3-rates/coastsat/lrr"
NC12 = CASCADE / "data/hatteras_init/4-mgmt-forcing/road_offset/raw_offset/current/nc12_current.geojson"
OUT = SITE / "assets/hatteras/data"

# Calendar windows, inclusive; the folder names match the model periods
WINDOWS = [
    {"key": "1996_2026", "label": "Whole record", "start": 1996, "end": 2026},
    {"key": "1996_2015", "label": "1996–2015", "start": 1996, "end": 2015},
    {"key": "2010_2026", "label": "2010–2026", "start": 2010, "end": 2026},
]
DOMAIN_M = 500.0
LOWESS_DOMAINS = 7
RAW_SOUTH = 10  # GIS 1-10 drawn as domain means, as in every project figure
FIT_TOL = 5e-4  # m/yr, against the published tables

# Labels on the map and chart, placed by GIS position (HATTERAS_ANNOTATIONS and the community zones)
PLACES = [
    {"name": "Cape Point", "gis": 1},
    {"name": "Buxton", "gis": 7.5},
    {"name": "Avon", "gis": 26},
    {"name": "Salvo", "gis": 69},
    {"name": "Waves", "gis": 74},
    {"name": "Rodanthe", "gis": 80},
    {"name": "Pea Island", "gis": 103},
]
GROIN_GIS = 5.5



def nourishments():
    """The fills the model is forced with, one band per reach: [{name, years, gis}], same-reach projects merged."""
    bands = {}
    for p in sorted(HATTERAS_NOURISHMENT_PROJECTS, key=lambda p: p.year):
        g = (min(p.gis_domains), max(p.gis_domains))
        b = bands.setdefault(g, {"name": p.name.split()[0], "years": [], "gis": list(g)})
        b["years"].append(p.year)
    return list(bands.values())


def km_north(gis):
    """Distance north of Cape Point, in km, of a GIS domain position (1 = the first domain's south edge)."""
    return (gis - 1) * DOMAIN_M / 1000.0


def load_frame():
    """Transect id and domain for GIS 1-115, ordered south to north."""
    main = pd.read_csv(FRAME / "transect_domain_lookup.csv")
    ext = pd.read_csv(FRAME / "transect_domain_lookup_ext.csv")
    t = pd.concat([main[["transect_id", "domain_number"]], ext[["transect_id", "domain_number"]]])
    t = t.dropna().drop_duplicates("transect_id")
    t["domain_number"] = t["domain_number"].astype(int)
    return t.sort_values(["domain_number", "transect_id"]).reset_index(drop=True)


def load_lines(ids):
    """Each transect's shore-normal line as [[lon, lat], ...], from the global CoastSat layer."""
    want = set(ids)
    layer = json.loads((FRAME / "CoastSat_transect_layer.geojson").read_text(encoding="utf-8"))
    lines = {}
    for f in layer["features"]:
        tid = f["properties"].get("id")
        if tid in want:
            lines[tid] = [[round(x, 5), round(y, 5)] for x, y in f["geometry"]["coordinates"]]
    return lines


def load_series(tid):
    """CoastSat positions for one transect: (decimal years, chainage m), NaNs dropped."""
    f = SERIES / f"{tid.rsplit('_', 1)[0]}_timeseries" / f"{tid}.csv"
    d = pd.read_csv(f)
    date = pd.to_datetime(d.iloc[:, 0], utc=True)
    pos = pd.to_numeric(d.iloc[:, 1], errors="coerce")
    keep = pos.notna()
    return date[keep], pos[keep]


def fit_lrr(date, pos, start, end):
    """The CASCADE LRR fit (coastsat_lrr_standalone.py): OLS slope and 95 % CI half-width, m/yr."""
    keep = date.dt.year.between(start, end)
    date, pos = date[keep], pos[keep]
    if len(pos) < 3:
        return np.nan, np.nan
    years = (date - date.min()).dt.total_seconds() / (365.25 * 86400)
    fit = stats.linregress(years, pos)
    return fit.slope, stats.t.ppf(0.975, len(pos) - 2) * fit.stderr


def along_coast(domains):
    """Chainage per transect, each domain's transects spread evenly across its 500 m (load_transect_data's rule)."""
    s = pd.Series(domains)
    rank = s.groupby(s).cumcount().values
    n = s.groupby(s).transform("count").values
    return (s.values - 1) * DOMAIN_M + (rank + 0.5) * DOMAIN_M / n


def smooth(domains, along, rates):
    """7-domain LOWESS per transect; GIS 1-10 replaced by their domain mean."""
    out, _ = lowess_transect_values(along, rates, LOWESS_DOMAINS)
    gis, means = compute_domain_means(domains, rates, 1, RAW_SOUTH)
    for g, m in zip(gis, means):
        out[domains == g] = m
    return out


def check_against_tables(frame, rates):
    """Refit vs lrr/<window>/transect_lrr_full.csv for every transect the table has; raises on a mismatch."""
    for i, w in enumerate(WINDOWS):
        pub = pd.read_csv(LRR / w["key"] / "transect_lrr_full.csv").set_index("transect_id")["lrr_m_yr"]
        mine = pd.Series(rates[:, i], index=frame["transect_id"])
        both = mine.index.intersection(pub.index)
        diff = (mine[both] - pub[both]).abs().max()
        print(f"  {w['key']}: {len(both)} transects match the published table to {diff:.1e} m/yr")
        if not diff <= FIT_TOL:
            raise ValueError(f"{w['key']} refit differs from the published LRR by {diff} m/yr")


def landward_end(frame, lines, gis):
    """[lat, lon] of the landward end of the transect nearest the middle of a GIS position, for map labels."""
    centre = (np.floor(gis) - 1) * DOMAIN_M + (gis % 1 or 0.5) * DOMAIN_M
    k = int(np.argmin(np.abs(along_coast(frame.domain_number.values) - centre)))
    lon, lat = lines[frame.transect_id[k]][0]
    return [lat, lon]


def nc12_line():
    """NC-12 (current alignment) in lon/lat, simplified to 10 ft in State Plane."""
    g = json.loads(NC12.read_text(encoding="utf-8"))["features"][0]["geometry"]
    line = LineString(g["coordinates"]).simplify(10.0)
    to_ll = Transformer.from_crs("EPSG:2264", "EPSG:4326", always_xy=True)
    return [[round(x, 5), round(y, 5)] for x, y in (to_ll.transform(*p) for p in line.coords)]


def main():
    frame = load_frame()
    print(f"{len(frame)} transects, GIS {frame.domain_number.min()}-{frame.domain_number.max()}")
    lines = load_lines(frame.transect_id)
    missing = sorted(set(frame.transect_id) - set(lines))
    if missing:
        print(f"  no line in the CoastSat layer for {len(missing)} transects, dropped: {missing[:5]}")
        frame = frame[frame.transect_id.isin(lines)].reset_index(drop=True)

    rates = np.full((len(frame), len(WINDOWS)), np.nan)
    uncs = np.full_like(rates, np.nan)
    by_domain = {}
    record_end = None
    for k, tid in enumerate(frame.transect_id):
        date, pos = load_series(tid)
        record_end = max(record_end, date.max()) if record_end is not None else date.max()
        for i, w in enumerate(WINDOWS):
            rates[k, i], uncs[k, i] = fit_lrr(date, pos, w["start"], w["end"])
        # Positions relative to the 1996 mean (or the first later year with data)
        yrs = date.dt.year
        ref_year = yrs[yrs >= 1996].min()
        ref = pos[yrs == ref_year].mean()
        dec = yrs + (date.dt.dayofyear - 1) / 365.25
        pts = [[round(float(a), 2), round(float(b), 1)] for a, b in zip(dec, pos - ref)]
        by_domain.setdefault(int(frame.domain_number[k]), {})[tid] = {"ref_year": int(ref_year), "pts": pts}

    check_against_tables(frame, rates)

    domains = frame.domain_number.values
    along = along_coast(domains)
    smoothed = np.column_stack([smooth(domains, along, rates[:, i]) for i in range(len(WINDOWS))])

    def r2(a):
        return [None if not np.isfinite(v) else round(float(v), 2) for v in a]

    transects = [
        {"id": tid, "d": int(domains[k]), "km": round(along[k] / 1000.0, 3), "line": lines[tid],
         "r": r2(rates[k]), "u": r2(uncs[k]), "s": r2(smoothed[k])}
        for k, tid in enumerate(frame.transect_id)
    ]
    data = {
        "source": "CoastSat (Vos et al.) shorelines; LRR = OLS slope of position on date; "
                  "smoothed = 7-domain (3.5 km) LOWESS, GIS 1-10 domain means",
        "record_end": record_end.strftime("%Y-%m-%d"),
        "windows": WINDOWS,
        "transects": transects,
        "places": [dict(p, km=round(km_north(p["gis"]) + 0.25, 2), ll=landward_end(frame, lines, p["gis"]))
                   for p in PLACES],
        "groin": {"km": round(km_north(GROIN_GIS) + 0.5, 2), "ll": landward_end(frame, lines, GROIN_GIS + 0.5)},
        "nourishments": [dict(n, km=[km_north(n["gis"][0]), km_north(n["gis"][1] + 1)]) for n in nourishments()],
        "nc12": nc12_line(),
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "shoreline_rates.json").write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    ts = OUT / "timeseries"
    ts.mkdir(exist_ok=True)
    for d, series in by_domain.items():
        (ts / f"d{d:03d}.json").write_text(json.dumps(series, separators=(",", ":")), encoding="utf-8")
    size = sum(f.stat().st_size for f in OUT.rglob("*.json")) / 1e6
    print(f"wrote {OUT} ({len(by_domain)} domain files, {size:.1f} MB); record ends {data['record_end']}")


if __name__ == "__main__":
    main()
