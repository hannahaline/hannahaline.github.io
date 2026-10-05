"""
The Buxton groins through time, for the Management page of the Hatteras stakeholder pages.

    python tools/hatteras_groin_photos.py

Six NC OneMap aerial photos of the same 800 m x 1000 m frame around the three Buxton groins (1993, 2002, 2012, 2016,
2020, 2024), each with that calendar year's average CoastSat shoreline drawn on it, and the 1993 shoreline dashed for
comparison. Each shoreline joins the mean position on every transect in the frame, placed along the transect from its
landward end, as in tools/hatteras_decadal_shorelines.py. Hannah asked (2026-10-03) for real photos of the groins over
time with the CoastSat shorelines, in place of the schematic groin diagram.
Writes assets/hatteras/img/groins_through_time.jpg. Photos are saved under tools/data/groin_photos/ so a re-run only
redraws; pass --fetch to download them again. Needs the CASCADE repo beside this one.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from PIL import Image

import hatteras_imagery_data as img
import hatteras_shoreline_data as sd
import hatteras_fig_style as style

SITE = Path(__file__).resolve().parents[1]
PHOTOS = SITE / "tools/data/groin_photos"
OUT = SITE / "assets/hatteras/img/groins_through_time.jpg"
CENTRE = (35.25525, -75.5200)        # lat, lon: the three groins and the old lighthouse site
HALF_W_M, HALF_H_M = 400, 500        # ground metres
PX = (800, 1000)
YEARS = {1993: "DOQQ_NC_1993", 2002: "Orthoimagery_2002", 2012: "Orthoimagery_2012_2015",
         2016: "Orthoimagery_2016_2019", 2020: "Orthoimagery_2020_2023", 2024: "Orthoimagery_20242027"}
NOTES = {1993: "lighthouse still here", 2002: "after the lighthouse move", 2012: "after Hurricane Irene",
         2016: "before the 2017 fill", 2020: "after the 2017 fill", 2024: "after the 2022 fill"}
# the three groins, north to south, as (root, tip) in pixels of the 800 x 1000 frame, read off the 2002 photo where all
# three are clearest; drawn in every panel so the shoreline can be read against them
GROINS = [((455, 210), (550, 232)), ((430, 410), (512, 425)), ((340, 600), (440, 612))]
GROIN = "#d7191c"
REF = 1993
LINE, REF_LINE = "#ffd23f", "#ffffff"
MIN_OBS = 3


def frame():
    x, y = img.merc(*CENTRE)
    k = 1 / math.cos(math.radians(CENTRE[0]))           # Web Mercator metres per ground metre here
    return [x - HALF_W_M * k, y - HALF_H_M * k, x + HALF_W_M * k, y + HALF_H_M * k], k


def shorelines(box):
    """{year: [(x, y) in Web Mercator]} south to north, from the transects that cross the frame's north-south span
    (their seaward ends lie offshore of it)."""
    rates = json.loads((sd.OUT / "shoreline_rates.json").read_text(encoding="utf-8"))
    out = {y: [] for y in YEARS}
    for t in rates["transects"]:
        (lx, ly), (sx, sy) = t["line"]
        a, b = np.array(img.merc(ly, lx)), np.array(img.merc(sy, sx))
        if not (box[1] <= (a[1] + b[1]) / 2 <= box[3] and box[0] - 2000 <= a[0] <= box[2]):
            continue
        u = (b - a) / np.linalg.norm(b - a)
        k = 1 / math.cos(math.radians(sy))
        date, pos = sd.load_series(t["id"])
        yr = date.dt.year.values
        for y in YEARS:
            sel = pos[yr == y]
            if len(sel) >= MIN_OBS:
                out[y].append(tuple(a + u * float(sel.mean()) * k))   # positions are ground metres along the transect
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--fetch", action="store_true")
    args = ap.parse_args()
    box, k = frame()
    PHOTOS.mkdir(parents=True, exist_ok=True)
    for y, svc in YEARS.items():
        p = PHOTOS / f"{y}.jpg"
        if args.fetch or not p.exists():
            img.save(img.export_nconemap(svc, box, PX), p)
            print(f"fetched {y}")
    lines = shorelines(box)
    for y in YEARS:
        print(f"  {y}: {len(lines[y])} transects")

    style.apply()
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 9.4), gridspec_kw={"wspace": 0.04, "hspace": 0.1})
    extent = [box[0], box[2], box[1], box[3]]
    halo = [pe.withStroke(linewidth=3.2, foreground="#1a1a1a")]
    for i, (ax, y) in enumerate(zip(axes.flat, YEARS)):
        ax.imshow(Image.open(PHOTOS / f"{y}.jpg"), extent=extent, interpolation="lanczos")
        if y != REF and lines[REF]:
            xs, ys = zip(*lines[REF])
            ax.plot(xs, ys, color=REF_LINE, lw=1.4, ls=(0, (4, 2.5)), path_effects=halo)
        if lines[y]:
            xs, ys = zip(*lines[y])
            ax.plot(xs, ys, color=LINE, lw=2.0, path_effects=halo)
        ax.set_xlim(box[0], box[2])
        ax.set_ylim(box[1], box[3])
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#1a1a1a")
            s.set_linewidth(1.2)
        # the groins, numbered north to south, at the same place in every panel
        for n, (root, tip) in enumerate(GROINS, 1):
            (rx, ry), (tx, ty) = [(box[0] + px / PX[0] * (box[2] - box[0]), box[3] - py / PX[1] * (box[3] - box[1])) for px, py in (root, tip)]
            ax.plot([rx, tx], [ry, ty], color=GROIN, lw=2.2, solid_capstyle="round",
                    path_effects=[pe.withStroke(linewidth=4, foreground="white")])
            ax.text(tx + 14 * k, ty, str(n), color=GROIN, fontsize=9, fontweight="bold", va="center",
                    bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=GROIN, lw=1))
        # panel label: letter and year, with what had just happened, in a white box
        ax.text(0.03, 0.975, f"({'abcdef'[i]}) {y}\n" + NOTES[y], transform=ax.transAxes, ha="left", va="top",
                fontsize=9.5, color="#1a1a1a", linespacing=1.35,
                bbox=dict(boxstyle="square,pad=0.35", fc="white", ec="#1a1a1a", lw=0.8, alpha=0.92))
    # scale bar and north arrow in the first panel
    ax = axes.flat[0]
    x0, y0 = box[0] + 0.06 * (box[2] - box[0]), box[1] + 0.05 * (box[3] - box[1])
    ax.plot([x0, x0 + 200 * k], [y0, y0], color="white", lw=3, solid_capstyle="butt", path_effects=halo)
    ax.text(x0 + 100 * k, y0 + 18 * k, "200 m", ha="center", va="bottom", color="white", fontsize=9.5,
            path_effects=[pe.withStroke(linewidth=2.6, foreground="#1a1a1a")])
    ax.annotate("N", xy=(0.92, 0.97), xytext=(0.92, 0.86), xycoords="axes fraction", ha="center", va="center",
                color="white", fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.6),
                path_effects=[pe.withStroke(linewidth=2.6, foreground="#1a1a1a")])
    from matplotlib.lines import Line2D
    fig.legend(handles=[Line2D([], [], color=LINE, lw=2.4, path_effects=halo, label="Average shoreline that year (satellite)"),
                        Line2D([], [], color=REF_LINE, lw=1.6, ls=(0, (4, 2.5)), path_effects=halo, label="Average shoreline in 1993"),
                        Line2D([], [], color=GROIN, lw=2.4, path_effects=[pe.withStroke(linewidth=4, foreground="white")],
                               label="Groins 1-3 (north to south)")],
               loc="lower center", ncol=3, frameon=False, fontsize=10, bbox_to_anchor=(0.5, 0.035), handlelength=3.2)
    fig.savefig(OUT, dpi=170, bbox_inches="tight", pad_inches=0.05, pil_kwargs={"quality": 86, "optimize": True})
    print(f"wrote {OUT.relative_to(SITE)}")


if __name__ == "__main__":
    main()
