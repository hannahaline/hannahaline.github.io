"""
The model's inputs, one simple figure per step, for the stepper on The model page of the Hatteras stakeholder pages.

    python tools/hatteras_model_steps.py

Hannah's choice (2026-10-03): simplified versions of CASCADE's input figures (output/figures/3-model-inputs), for
the 1996-2015 run, with plain labels. Every panel reads the same files the run reads, through the loaders of
scripts/figure_making/pipeline/inputs_overview_figure.py in the CASCADE repo beside this one; the storms come from
this site's timeline.json (the same hindcast storm record), because CASCADE's storm loader has no 1996-2015 period.
Writes assets/hatteras/img/model_steps/step2.png ... step6.png; step1.png (one stretch as photo, lidar and grid) and
step5_road.png come from tools/hatteras_model_stretch.py.

    2 the whole island           elevation of every 10 m cell at the start of the run, 90 stretches of 500 m
    3 storms                     every storm event in the run, by how high the water reached
    4 waves and sea level        the Duck sea-level record with the run's rate, and the wave settings
    5 what people did            the road's distance back from the dunes, the managed villages, the 1999 move, the 2014 fill
    6 what we compare with       the measured shoreline change rate per stretch, 1996-2015

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

SITE = Path(__file__).resolve().parents[1]
CASCADE = SITE.parent / "CASCADE"
for p in ("scripts", "scripts/figure_making/island", "scripts/hatteras_ms", "scripts/input_prep/3-env-forcings/3-storms",
          "scripts/figure_making/pipeline"):
    sys.path.insert(0, str(CASCADE / p))
import inputs_overview_figure as io  # noqa: E402
from HAT_hindcast_config import field_default  # noqa: E402
from site_layer.hatteras_site_config import (  # noqa: E402
    HATTERAS_PERIODS, HATTERAS_COMMUNITY_ZONES, HATTERAS_ROAD_EVENTS, HATTERAS_NOURISHMENT_PROJECTS,
)

START = 1996
END = HATTERAS_PERIODS[START]["end_year"]
OUT = SITE / "assets/hatteras/img/model_steps"
DATA = SITE / "assets/hatteras/data"
INK, MUTED, GRID = "#1a1a1a", "#5b6469", "#e6e9eb"
FILL, ROAD, TROP, OTHER, SEA = "#c8880f", "#d55e00", "#c8880f", "#6baed6", "#2166ac"
DOMAIN_KM = 0.5
W_IN = 10.0
STORM_NAME_M = 3.0              # named tropical storms at or above this water level, as on the Storms page
halo = [pe.withStroke(linewidth=3, foreground="white")]


def km(gis):
    """km north of Cape Point at the middle of a GIS domain."""
    return (np.asarray(gis) - 0.5) * DOMAIN_KM


def villages(ax, top=True):
    places = json.loads((DATA / "shoreline_rates.json").read_text(encoding="utf-8"))["places"]
    for i, p in enumerate(places):
        if p["km"] > 45.5:
            continue
        ax.axvline(p["km"], color=MUTED, lw=0.6, ls=":", zorder=0)
        ax.text(p["km"], 1.01 + (0.07 if p["name"] in ("Waves", "Buxton") else 0), p["name"], transform=ax.get_xaxis_transform(),
                ha="left" if p["km"] < 1 else "center", va="bottom", fontsize=9.5, color=INK)


def frame(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9.5)


def save(fig, n):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"step{n}.png", dpi=150, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(f"wrote step{n}.png")


def step2(canvas, cmap, norm, ticks, water):
    fig, ax = plt.subplots(figsize=(W_IN, 3.1))
    rows_km = canvas.shape[0] * io.init.CELL_SIZE_M / 1000
    im = ax.imshow(np.ma.masked_less(np.ma.masked_invalid(canvas), 0.0), cmap=cmap, norm=norm, origin="lower",
                   extent=(0, canvas.shape[1] * io.init.CELL_SIZE_M / 1000, 0, rows_km), interpolation="nearest", aspect="auto")
    ax.set_facecolor(water)
    ax.set_ylim(0, rows_km)
    ax.set_xlim(0, 45)
    ax.set_yticks([])
    ax.set_xlabel("km north of Cape Point", fontsize=10)
    ax.text(0.995, 0.03, "beach (ocean side)", transform=ax.transAxes, ha="right", fontsize=9.5, color=INK, path_effects=halo)
    ax.text(0.995, 0.93, "Pamlico Sound", transform=ax.transAxes, ha="right", va="top", fontsize=9.5, color="white")
    villages(ax)
    for g in range(1, 91):                       # the 500 m stretches, as ticks along the beach edge
        ax.plot([g * DOMAIN_KM] * 2, [0, 0.08], color="white", lw=0.6)
    cb = fig.colorbar(im, ax=ax, ticks=ticks, pad=0.01, fraction=0.03, aspect=10)
    cb.set_label("height above\nhigh tide (m)", fontsize=9.5)
    cb.ax.tick_params(labelsize=9)
    frame(ax)
    save(fig, 2)


def step3():
    t = json.loads((DATA / "timeline.json").read_text(encoding="utf-8"))
    s = [e for e in t["storms"] if START <= e["y"] < END + 1]
    fig, ax = plt.subplots(figsize=(W_IN, 3.6))
    for kind, col, size in (("other", OTHER, 14), ("tropical", TROP, 26)):
        d = [e for e in s if (e["type"] == "tropical") == (kind == "tropical")]
        ax.scatter([e["y"] for e in d], [e["wl"] for e in d], s=size, color=col, edgecolors="white", linewidths=0.4, zorder=3,
                   label="hurricanes and tropical storms" if kind == "tropical" else "other storms, mostly nor'easters")
    best = {}
    for e in s:
        if e["name"] and e["type"] == "tropical" and e["wl"] >= STORM_NAME_M and (e["name"] not in best or e["wl"] > best[e["name"]]["wl"]):
            best[e["name"]] = e
    for e in best.values():
        ax.annotate(e["name"].rsplit(" ", 1)[0], (e["y"], e["wl"]), xytext=(0, 6), textcoords="offset points", ha="center",
                    fontsize=9, color=INK, path_effects=halo)
    ax.set_xlim(START, END + 1)
    ax.set_xticks(range(2000, END + 1, 5))
    ax.set_ylabel("how high the water\nreached (m above high tide)", fontsize=10)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=9.5, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
    ax.set_ylim(1, max(e["wl"] for e in s) + 0.7)
    ax.text(0.01, 0.95, f"{len(s)} storms, {START}–{END}", transform=ax.transAxes, fontsize=10, va="top", color=INK)
    frame(ax)
    save(fig, 3)


def step4():
    sl, fit = io.sea_level(START, END)
    waves = {k: field_default(k) for k in ("hs", "wave_period_s", "wave_asymmetry", "wave_angle_high_fraction")}
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 3.6), gridspec_kw={"width_ratios": [1.6, 1]})
    a.plot(sl.t, sl.msl, color="#bdbdbd", lw=0.8, label="monthly average, Duck tide gauge")
    xs = np.array([START, END])
    rate = HATTERAS_PERIODS[START]["sea_level_rise_rate"]
    yfit = fit.intercept_m + fit.slope_m_yr * xs
    a.plot(xs, yfit, color=SEA, lw=2.4, label=f"the run: sea level rising {rate * 1000:g} mm a year")
    a.set_ylabel("sea level (m)", fontsize=10)
    a.set_xlim(START, END)
    a.set_xticks(range(2000, END + 1, 5))
    a.legend(frameon=False, fontsize=9, loc="upper left")
    a.set_title("Sea level", fontsize=11, loc="left")
    frame(a)
    # waves: a coastline with arrows from the north-east and south-east, widths by their share
    b.set_xlim(0, 10)
    b.set_ylim(0, 10)
    b.axis("off")
    b.fill([0, 3.2, 4.2, 0], [0, 0, 10, 10], color="#ecdfb9", ec="#a8925e", lw=1.2)
    b.text(1.2, 5, "island", rotation=84, ha="center", va="center", fontsize=9.5, color=INK)
    north = waves["wave_asymmetry"]
    for share, (x0, y0), (x1, y1), label in ((north, (9.3, 8.6), (4.6, 6.4), f"{round(north * 100)}% of waves\nfrom the north-east"),
                                            (1 - north, (9.3, 1.4), (4.4, 3.4), f"{round((1 - north) * 100)}% from\nthe south-east")):
        b.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=18, lw=2 + 10 * share, color=SEA))
        b.text(x0 + 0.2, y0 + (0.7 if y0 > 5 else -0.7), label, ha="right", va="center", fontsize=9, color=INK)
    b.text(6.8, 5.0, f"typical wave\n{waves['hs']:g} m high,\none every {waves['wave_period_s']:g} s", ha="center", va="center",
           fontsize=9.5, color=INK)
    b.set_title("Waves", fontsize=11, loc="left")
    save(fig, 4)


def step5():
    setback = io.two_row(io.tv.INIT_ROOT / HATTERAS_PERIODS[START]["road_setback_file"]).reindex(io.GIS)
    fig, ax = plt.subplots(figsize=(W_IN, 3.6))
    for lo, hi in HATTERAS_COMMUNITY_ZONES:
        ax.axvspan(km(lo) - 0.25, km(hi) + 0.25, color="#e8edf0", zorder=0)
    ax.axvspan(-1, -1, color="#e8edf0", label="villages: dunes rebuilt, overwash cleared from streets")
    ax.step(km(setback.index), setback.values, where="mid", color=INK, lw=1.8, label="NC-12: distance back from the front of the dunes (m)")
    for e in HATTERAS_ROAD_EVENTS:
        if hasattr(e, "displacement_m") and START <= e.year < END:
            g = list(e.displacement_m)
            ax.axvspan(km(min(g)) - 0.25, km(max(g)) + 0.25, ymin=0, ymax=0.12, color=ROAD, zorder=2)
            ax.text(km(np.mean(g)), 0.15, f"road moved\ninland, {e.year}", transform=ax.get_xaxis_transform(), ha="center",
                    fontsize=9, color=ROAD, path_effects=halo)
    for p in HATTERAS_NOURISHMENT_PROJECTS:
        if START <= p.year < END:
            g = p.gis_domains
            ax.axvspan(km(min(g)) - 0.25, km(max(g)) + 0.25, ymin=0.88, ymax=1, color=FILL, zorder=2)
            ax.text(km(np.mean(g)), 0.84, f"beach\nnourishment, {p.year}", transform=ax.get_xaxis_transform(), ha="center",
                    va="top", fontsize=9, color="#8a5d06", path_effects=halo)
    ax.set_xlim(0, 45)
    ax.set_ylim(0, np.nanmax(setback) * 1.25)
    ax.set_xlabel("km north of Cape Point", fontsize=10)
    ax.set_ylabel("metres", fontsize=10)
    ax.legend(frameon=False, fontsize=9.5, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2)
    villages(ax)
    frame(ax)
    save(fig, 5)


def step6():
    target, _ = io.observed_target(START, END)
    fig, ax = plt.subplots(figsize=(W_IN, 3.6))
    v = target.reindex(io.GIS).values
    cols = np.where(v < 0, "#d6604d", "#4393c3")
    ax.bar(km(io.GIS), v, width=DOMAIN_KM * 0.9, color=cols)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xlim(0, 45)
    ax.set_xlabel("km north of Cape Point", fontsize=10)
    ax.set_ylabel(f"shoreline change,\nm per year ({START}–{END})", fontsize=10)
    ax.text(0.995, 0.97, "growing (seaward)", transform=ax.transAxes, ha="right", va="top", fontsize=9.5, color="#2166ac")
    ax.text(0.995, 0.03, "eroding (landward)", transform=ax.transAxes, ha="right", va="bottom", fontsize=9.5, color="#b2182b")
    ax.grid(axis="y", color=GRID, lw=0.6)
    villages(ax)
    frame(ax)
    save(fig, 6)


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans"})
    canvas = io.init.detrended_canvas(START, include_buffers=False)
    cmap, norm, ticks, water = io.init.scheme_colours(io.ELEVATION_SCHEME)
    step2(canvas, cmap, norm, ticks, water)
    step3()
    step4()
    step5()
    step6()


if __name__ == "__main__":
    main()
