"""
Before-and-after photos of each beach fill, for the nourishment explorer on the Management pages of the Hatteras
stakeholder pages.

    python tools/hatteras_nourishment_photos.py

For each fill, two USDA NAIP aerial photos (public domain, flown every two years in summer or autumn) of the same
300 m x 300 m frame: the last flight before sand placement started and the first one after it finished, weeks to
months after for every fill (NC OneMap flies Dare County only once in four years, so its nearest photos were one to
three years away). Each photo carries the CoastSat shoreline of its own date, the average of the three satellite shorelines
nearest the flight (none more than 130 days away), so the line describes the beach in the photo (dashed: before, on both photos; solid:
after). Lines are placed along the transects as in tools/hatteras_groin_photos.py. CoastSat marks mean sea level, so
the line sits a little landward of the wet edge in a photo flown at low tide. Hannah asked (2026-10-04) for real
photos with the shorelines, one pair per fill, a tight frame, thin lines, the fill clearly visible and the lines
matching the imagery. The lines are raw positions, not the explorer's comparison with the rest of the island, and they need not
match the water's edge in the photos, which were flown on other dates and tides.
The frame goes where the fill shows most clearly: the 300 m of beach (7 transects) with the largest shoreline change
between the two photo dates, keeping 500 m clear of each end of the stretch. Hannah first chose the typical spot
(change closest to the stretch average), then asked (2026-10-04) for the spot where the fill is clearly visible; the
caption says how the spot was chosen and the JSON keeps both the spot's change and the stretch average.
Below the pair, every later photo of the same frame (NAIP to 2022, NC OneMap March 2024), each with its own satellite
shoreline and the before line dashed, so the added beach can be watched wearing back on real photos. The headline
numbers for the explorer come from here too, on the placement dates: the jump is the change on the nourished stretch
from the 12 months before sand went on to the 12 months after it was finished, minus the median change on the rest of
the island (every transect more than 500 m from any fill) over the same months; what is left uses the last 12 months of
the record in place of the 12 months after. Hannah asked
(2026-10-04) for the headline, card, and figures to follow the placement dates instead of calendar years.
Writes assets/hatteras/img/nourishment/<stretch>_<year>.jpg and assets/hatteras/data/nourishment_photos.json (keyed
"<stretch> <year>" as the explorer names its fills). Photos are saved under tools/data/nourishment_photos/ so a re-run
only redraws; pass --fetch to download them again. Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-04
"""
import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

import hatteras_imagery_data as img
import hatteras_shoreline_data as sd
import hatteras_fig_style as style

SITE = Path(__file__).resolve().parents[1]
PHOTOS = SITE / "tools/data/nourishment_photos"
OUT_IMG = SITE / "assets/hatteras/img/nourishment"
OUT_JSON = SITE / "assets/hatteras/data/nourishment_photos.json"
HALF_M = 150                             # ground metres: a 300 m square frame
PX = 800
NC_ONEMAP_2024 = "Orthoimagery_20242027"   # the last of the later photos, March 2024
NOURISHMENT = SITE / "assets/hatteras/data/nourishment.json"   # the stretches, from tools/hatteras_nourishment_data.py
# Sand placement, first and last load: Hannah's table of 2026-10-04, shared with the CASCADE session. Rodanthe is the
# weakest (pumping "about to start" 29 July, "completed" reported 20 September; neither is a placement record). Avon 2022: first load 1:40 pm 19 June, last 11 pm 26 July (Dare County bulletins 31da538, 32561a3; checked 2026-10-04).
# Buxton 2017: county updates relayed by local news, last load confirmed.
# Buxton and Avon 2022: Dare County bulletins (govdelivery 31da538, 31fd603, 32561a3, 32653c5).
PLACED = {("Rodanthe", 2014): ("2014-07-29", "2014-09-20"), ("Buxton", 2017): ("2017-06-21", "2018-02-27"),
          ("Buxton", 2022): ("2022-06-30", "2022-08-16"), ("Avon", 2022): ("2022-06-19", "2022-07-26")}
PLACED_TEXT = {("Rodanthe", 2014): "late July to mid-September 2014", ("Buxton", 2017): "21 June 2017 to 27 February 2018",
               ("Buxton", 2022): "30 June to 16 August 2022", ("Avon", 2022): "19 June to 26 July 2022"}
# The dates must match CASCADE's record of placement dates; the script stops if they drift apart.
DATES_CSV = SITE.parent / "CASCADE/data/hatteras_init/4-mgmt-forcing/nourishment/datasets/nourishment_placement_dates.csv"
DATES_NAMES = {("Rodanthe", 2014): "Rodanthe emergency fill", ("Buxton", 2017): "Buxton beach nourishment",
               ("Buxton", 2022): "Buxton shore protection", ("Avon", 2022): "Avon shore protection"}
# stretch, fill year, NAIP flight dates before and after (Planetary Computer STAC, searched 2026-10-04)
FILLS = [("Rodanthe", 2014, "2012-06-28", "2014-10-17"), ("Buxton", 2017, "2016-09-10", "2018-10-29"),
         ("Buxton", 2022, "2020-10-18", "2022-10-07"), ("Avon", 2022, "2020-10-18", "2022-10-07")]
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
SIGN = "https://planetarycomputer.microsoft.com/api/sas/v1/sign?href="
LATER_PHOTOS = [("naip", "2014-10-17"), ("naip", "2016-09-10"), ("naip", "2018-10-29"), ("naip", "2020-10-18"),
                ("naip", "2022-10-07"), ("nconemap", "2024-03-12")]   # NAIP dates as flown over Buxton/Avon; Rodanthe's below
NAIP_DATE_AT = {"Rodanthe": {"2016-09-10": "2016-09-11", "2020-10-18": "2020-05-16"}}
PHOTO_NEAREST = 3                        # a photo's line: the mean of the satellite shorelines nearest its flight
PHOTO_MAX_DAYS = 130                     # ... none further than this (the sparse 2012 and 2020 passes reach ~4 months)
WINDOW = 7                               # transects, 50 m apart: the frame's 300 m
END_CLEAR_KM = 0.5
LINE, REF_LINE = "#ffd23f", "#ffffff"


def frame(transect, w):
    """A square frame centred just seaward of the transect's average shoreline in the before window."""
    (lx, ly), (sx, sy) = transect["line"]
    a, b = np.array(img.merc(ly, lx)), np.array(img.merc(sy, sx))
    u = (b - a) / np.linalg.norm(b - a)
    k = 1 / math.cos(math.radians(sy))
    x, y = a + u * (mean_in(transect, w) + 30) * k
    return [x - HALF_M * k, y - HALF_M * k, x + HALF_M * k, y + HALF_M * k], k


def windows(stretch, year):
    """The 12 months before placement started and the 12 months after it finished, as (start, end) timestamps."""
    s, e = (pd.Timestamp(d, tz="UTC") for d in PLACED[(stretch, year)])
    return (s - pd.DateOffset(years=1), s), (e + pd.Timedelta(days=1), e + pd.Timedelta(days=1) + pd.DateOffset(years=1))


_SERIES = {}


def series(tid):
    if tid not in _SERIES:
        _SERIES[tid] = sd.load_series(tid)
    return _SERIES[tid]


GAPS = []                                # days from each photo line's shorelines to its flight, for the caption


def mean_in(t, w):
    """Mean shoreline position on one transect inside a window, or None with fewer than three shorelines. A window
    given as a flight date takes the PHOTO_NEAREST shorelines closest to it instead."""
    date, pos = series(t["id"])
    if isinstance(w, str):
        gap = np.abs((date - pd.Timestamp(w, tz="UTC")).dt.days.values)
        order = np.argsort(gap)[:PHOTO_NEAREST]
        if len(order) < PHOTO_NEAREST or gap[order[-1]] > PHOTO_MAX_DAYS:
            return None
        GAPS.append(int(gap[order[-1]]))
        return float(pos.values[order].mean())
    sel = pos[(date >= w[0]) & (date < w[1])]
    return float(sel.mean()) if len(sel) >= 3 else None


def change(t, w0, w1):
    a, b = mean_in(t, w0), mean_in(t, w1)
    return None if a is None or b is None else b - a


def shorelines(transects, box, wins):
    """{window index: [(x, y) in Web Mercator]} from the transects crossing the frame, as in hatteras_groin_photos."""
    out = {i: [] for i in range(len(wins))}
    for t in transects:
        (lx, ly), (sx, sy) = t["line"]
        a, b = np.array(img.merc(ly, lx)), np.array(img.merc(sy, sx))
        if not (box[1] <= (a[1] + b[1]) / 2 <= box[3] and box[0] - 2000 <= a[0] <= box[2]):
            continue
        u = (b - a) / np.linalg.norm(b - a)
        k = 1 / math.cos(math.radians(sy))
        for i, w in enumerate(wins):
            m = mean_in(t, w)
            if m is not None:
                out[i].append(tuple(a + u * m * k))
    return out


def naip_export(date, box, size):
    """The NAIP photo flown on `date`, warped onto the Web Mercator box (tiles that meet in the frame are combined)."""
    import urllib.request
    import rasterio
    from rasterio.warp import reproject, Resampling, transform_bounds
    from rasterio.transform import from_bounds
    lon0, lat0, lon1, lat1 = transform_bounds("EPSG:3857", "EPSG:4326", *box)
    body = json.dumps({"collections": ["naip"], "bbox": [lon0, lat0, lon1, lat1], "datetime": f"{date}T00:00:00Z/{date}T23:59:59Z",
                       "limit": 20}).encode()
    req = urllib.request.Request(STAC, data=body, headers={"Content-Type": "application/json"})
    items = json.load(urllib.request.urlopen(req, timeout=120))["features"]
    assert items, f"no NAIP flight on {date} over the frame"
    dst = np.zeros((3, size, size), dtype=np.uint8)
    dst_t = from_bounds(*box, size, size)
    for it in items:
        href = json.load(urllib.request.urlopen(SIGN + it["assets"]["image"]["href"], timeout=120))["href"]
        with rasterio.open(href) as src:
            part = np.zeros_like(dst)
            for b in range(3):
                reproject(rasterio.band(src, b + 1), part[b], dst_transform=dst_t, dst_crs="EPSG:3857",
                          resampling=Resampling.bilinear)
            empty = dst.sum(axis=0) == 0
            dst[:, empty] = part[:, empty]
    return Image.fromarray(np.moveaxis(dst, 0, -1)).convert("RGBA")


def photo_window(date):
    """A photo's 'window' is its flight date; mean_in() then takes the nearest shorelines instead of a date range."""
    return str(date)


def clearest_spot(transects, km, w0, w1):
    """The centre transect of the 7-transect window with the largest mean change, and that change and the stretch's."""
    on = [t for t in transects if km[0] <= t["km"] <= km[1]]
    dx = [change(t, w0, w1) for t in on]
    mean = np.mean([v for v in dx if v is not None])
    best = None
    for i in range(len(on) - WINDOW + 1):
        w = dx[i:i + WINDOW]
        c = on[i + WINDOW // 2]
        if None in w or not (km[0] + END_CLEAR_KM <= c["km"] <= km[1] - END_CLEAR_KM):
            continue
        if best is None or np.mean(w) > best[0]:
            best = (float(np.mean(w)), c)
    return best[1], mean, best[0]


RECORD_END = pd.Timestamp("2026-01-13", tz="UTC")


def rest_of_island(transects, stretches):
    """Every transect more than 500 m from any nourished stretch."""
    spans = [st["km"] for st in stretches.values()]
    return [t for t in transects if not any(a - 0.5 <= t["km"] <= b + 0.5 for a, b in spans)]


def mean_change(ts, w0, w1, how=np.mean):
    v = [c for c in (change(t, w0, w1) for t in ts) if c is not None]
    return float(how(v))


def later_windows(stretch, year):
    """[(label, window)] after the fill: just after, 2 and 5 years later where they fit, and the last 12 months of the
    record, dropping any that would overlap the one before it or run past the record."""
    _, wa = windows(stretch, year)
    out = [("Just after", wa)]
    for n in (2, 5):
        w = (wa[0] + pd.DateOffset(years=n), wa[1] + pd.DateOffset(years=n))
        if w[1] <= RECORD_END - pd.DateOffset(years=1):
            out.append((f"{n} years later", w))
    last = (RECORD_END - pd.DateOffset(years=1), RECORD_END)
    if last[0] >= out[-1][1][1]:
        out.append(("Latest (2025)", last))
    refill = [f for f in FILLS if f[0] == stretch and f[1] > year]
    if refill:
        r0 = pd.Timestamp(PLACED[(stretch, refill[0][1])][0], tz="UTC")
        out = [(lab + (f", after the {refill[0][1]} refill" if w[0] > r0 else ""), w) for lab, w in out]
    return out


def years_later(stretch, year, after_date, transects, box, k, halo, fetch):
    """Every photo after the 'after' one, each with its own satellite shoreline and the before line dashed."""
    shots = [(src, NAIP_DATE_AT.get(stretch, {}).get(d, d)) for src, d in LATER_PHOTOS]
    shots = [(src, d) for src, d in shots if d > after_date]
    return shots


def draw_years_later(stretch, year, before_date, shots, transects, box, k, halo, fetch, phone=False):
    from matplotlib.lines import Line2D
    lines = shorelines(transects, box, [before_date] + [d for _, d in shots])
    n = len(shots)
    cols = min(n, 2 if phone else 3)
    rows = -(-n // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(2.75 * cols, 2.75 * rows + 0.45), squeeze=False,
                             gridspec_kw={"wspace": 0.04, "hspace": 0.06})
    refill = [f for f in FILLS if f[0] == stretch and f[1] > year]
    r0 = PLACED[(stretch, refill[0][1])][0] if refill else None
    for ax in axes.flat[n:]:
        ax.axis("off")
    for i, ((src, d), ax) in enumerate(zip(shots, axes.flat)):
        p = PHOTOS / f"{src}_{d}_{box[0]:.0f}_{box[1]:.0f}.jpg"
        if fetch or not p.exists():
            img.save(naip_export(d, box, PX) if src == "naip" else img.export_nconemap(NC_ONEMAP_2024, box, (PX, PX)), p)
        ax.imshow(Image.open(p), extent=[box[0], box[2], box[1], box[3]], interpolation="lanczos")
        if lines[0]:
            xs, ys = zip(*lines[0])
            ax.plot(xs, ys, color=REF_LINE, lw=0.9, ls=(0, (4, 2.5)), path_effects=halo)
        if lines[i + 1]:
            xs, ys = zip(*lines[i + 1])
            ax.plot(xs, ys, color=LINE, lw=1.1, path_effects=halo)
        ax.set_xlim(box[0], box[2])
        ax.set_ylim(box[1], box[3])
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#1a1a1a")
            sp.set_linewidth(1.0)
        ts = pd.Timestamp(d)
        note = f"\nafter the {refill[0][1]} refill" if r0 and d > r0 else ""
        ax.text(0.04, 0.96, f"{ts.day} {ts:%b %Y}{note}", transform=ax.transAxes, ha="left", va="top", fontsize=8.5,
                color="#1a1a1a", bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="#1a1a1a", lw=0.7, alpha=0.92))
    ax = axes.flat[0]
    x0, y0 = box[0] + 0.07 * (box[2] - box[0]), box[1] + 0.07 * (box[3] - box[1])
    ax.plot([x0, x0 + 50 * k], [y0, y0], color="white", lw=2.6, solid_capstyle="butt", path_effects=halo)
    ax.text(x0 + 25 * k, y0 + 8 * k, "50 m", ha="center", va="bottom", color="white", fontsize=8, path_effects=halo)
    fig.legend(handles=[Line2D([], [], color=REF_LINE, lw=1.1, ls=(0, (4, 2.5)), path_effects=halo, label="Shoreline before the fill"),
                        Line2D([], [], color=LINE, lw=1.3, path_effects=halo, label="Shoreline at the time of each photo")],
               loc="lower center", ncol=2, frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, -0.01), handlelength=2.6)
    name = f"{stretch.lower()}_{year}_years_later{'_phone' if phone else ''}.jpg"
    fig.savefig(OUT_IMG / name, dpi=150, bbox_inches="tight", pad_inches=0.04, pil_kwargs={"quality": 85, "optimize": True})
    plt.close(fig)
    return name, [f"{pd.Timestamp(d).day} {pd.Timestamp(d):%B %Y}" for _, d in shots]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--fetch", action="store_true")
    args = ap.parse_args()
    record = pd.read_csv(DATES_CSV).set_index("project")
    for key, name in DATES_NAMES.items():
        got = (record.loc[name, "start_date"], record.loc[name, "end_date"])
        assert got == PLACED[key], f"{key}: {PLACED[key]} here but {got} in {DATES_CSV.name}"
    rates = json.loads((sd.OUT / "shoreline_rates.json").read_text(encoding="utf-8"))
    nx = json.loads(NOURISHMENT.read_text(encoding="utf-8"))
    stretches = {s["name"]: s for s in nx["stretches"]}
    rest = rest_of_island(rates["transects"], stretches)
    PHOTOS.mkdir(parents=True, exist_ok=True)
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    style.apply()
    halo = [pe.withStroke(linewidth=2.2, foreground="#1a1a1a")]
    out = {}
    for stretch, year, yb, ya in FILLS:
        pb, pa = photo_window(yb), photo_window(ya)
        spot, mean, here = clearest_spot(rates["transects"], stretches[stretch]["km"], pb, pa)
        print(f"{stretch} {year}: {yb} -> {ya}, stretch mean {mean:+.1f} m, frame at km {spot['km']:.2f} ({here:+.1f} m)")
        box, k = frame(spot, pb)
        GAPS.clear()
        lines = shorelines(rates["transects"], box, (pb, pa))
        gap_days = max(GAPS) if GAPS else None
        lb, la = 0, 1
        for phone in (False, True):
            # stacked, one photo above the other, for phones (phone check, 2026-10-04)
            fig, axes = (plt.subplots(2, 1, figsize=(4.2, 8.9), gridspec_kw={"hspace": 0.04}) if phone else
                         plt.subplots(1, 2, figsize=(8, 4.25), gridspec_kw={"wspace": 0.03}))
            for i, (ax, y) in enumerate(zip(axes, (yb, ya))):
                p = PHOTOS / f"naip_{y}_{box[0]:.0f}_{box[1]:.0f}.jpg"
                if args.fetch or not p.exists():
                    img.save(naip_export(y, box, PX), p)
                    print(f"fetched {p.name}")
                ax.imshow(Image.open(p), extent=[box[0], box[2], box[1], box[3]], interpolation="lanczos")
                xs, ys = zip(*lines[lb])
                ax.plot(xs, ys, color=REF_LINE, lw=1.0, ls=(0, (4, 2.5)), path_effects=halo)
                if i:
                    xs, ys = zip(*lines[la])
                    ax.plot(xs, ys, color=LINE, lw=1.2, path_effects=halo)
                ax.set_xlim(box[0], box[2])
                ax.set_ylim(box[1], box[3])
                ax.set_xticks([])
                ax.set_yticks([])
                for s in ax.spines.values():
                    s.set_color("#1a1a1a")
                    s.set_linewidth(1.2)
                ax.text(0.03, 0.97, f"({'ab'[i]}) {'Before' if i == 0 else 'After'}: {pd.Timestamp(y).day} {pd.Timestamp(y):%b %Y}",
                        transform=ax.transAxes,
                        ha="left", va="top", fontsize=9.5, color="#1a1a1a",
                        bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="#1a1a1a", lw=0.8, alpha=0.92))
            ax = axes[0]
            x0, y0 = box[0] + 0.06 * (box[2] - box[0]), box[1] + 0.06 * (box[3] - box[1])
            ax.plot([x0, x0 + 50 * k], [y0, y0], color="white", lw=3, solid_capstyle="butt", path_effects=halo)
            ax.text(x0 + 25 * k, y0 + 8 * k, "50 m", ha="center", va="bottom", color="white", fontsize=9, path_effects=halo)
            ax.annotate("N", xy=(0.92, 0.97), xytext=(0.92, 0.84), xycoords="axes fraction", ha="center", va="center",
                        color="white", fontsize=10, fontweight="bold", arrowprops=dict(arrowstyle="-|>", color="white", lw=1.4),
                        path_effects=halo)
            from matplotlib.lines import Line2D
            fig.legend(handles=[Line2D([], [], color=REF_LINE, lw=1.2, ls=(0, (4, 2.5)), path_effects=halo, label="Satellite shoreline at the time of photo (a)"),
                                Line2D([], [], color=LINE, lw=1.4, path_effects=halo, label="At the time of photo (b)")],
                       loc="lower center", ncol=1 if phone else 2, frameon=False, fontsize=9.5,
                       bbox_to_anchor=(0.5, 0.0 if phone else -0.02), handlelength=3)
            name = f"{stretch.lower()}_{year}{'_phone' if phone else ''}.jpg"
            fig.savefig(OUT_IMG / name, dpi=150, bbox_inches="tight", pad_inches=0.04, pil_kwargs={"quality": 85, "optimize": True})
            plt.close(fig)
        name = f"{stretch.lower()}_{year}.jpg"
        shots = years_later(stretch, year, ya, rates["transects"], box, k, halo, args.fetch)
        tt_name, tt_labels = draw_years_later(stretch, year, yb, shots, rates["transects"], box, k, halo, args.fetch)
        draw_years_later(stretch, year, yb, shots, rates["transects"], box, k, halo, args.fetch, phone=True)
        wb, wa = windows(stretch, year)
        last = later_windows(stretch, year)[-1]
        on = [t for t in rates["transects"] if stretches[stretch]["km"][0] <= t["km"] <= stretches[stretch]["km"][1]]
        jump = mean_change(on, wb, wa) - mean_change(rest, wb, wa, np.median)
        left = mean_change(on, wb, last[1]) - mean_change(rest, wb, last[1], np.median)
        print(f"  jump {jump:+.1f} m, left {left:+.1f} m ({last[0]})")
        out[f"{stretch} {year}"] = {"src": f"/assets/hatteras/img/nourishment/{name}",
                                    "before": f"{pd.Timestamp(yb).day} {pd.Timestamp(yb):%B %Y}",
                                    "after": f"{pd.Timestamp(ya).day} {pd.Timestamp(ya):%B %Y}",
                                    "years_later": f"/assets/hatteras/img/nourishment/{tt_name}", "later_photos": tt_labels,
                                    "src_phone": f"/assets/hatteras/img/nourishment/{name.replace('.jpg', '_phone.jpg')}",
                                    "years_later_phone": f"/assets/hatteras/img/nourishment/{tt_name.replace('.jpg', '_phone.jpg')}",
                                    "jump_m": round(jump, 1), "left_m": round(left, 1), "left_year": 2025,
                                    "left_after_refill": "refill" in last[0],
                                    "placed": PLACED_TEXT[(stretch, year)], "line_gap_days": gap_days,
                                    "km": round(spot["km"], 2), "change_m": round(here, 1), "stretch_change_m": round(mean, 1)}
        print(f"wrote {name}: {len(lines[lb])} / {len(lines[la])} transects")
    OUT_JSON.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT_JSON.relative_to(SITE)}")


if __name__ == "__main__":
    main()
