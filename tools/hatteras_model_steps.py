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
    offset the shape of the coast  each stretch's shoreline set back from the model's straight axis (the BRIE offset
                                 file the run reads), drawn as the model's coastline; Hannah asked for it 2026-10-03
    3 storms                     every storm event in the run, by how high the water reached
    4 waves and sea level        the Duck sea-level record with the run's rate, and the wave settings
    5 what people did            the road's distance back from the dunes, the managed villages, the 1999 move, the 2014 fill
    6 what we compare with       the measured shoreline change rate per stretch, 1996-2015

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-04
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
H_SCALE = 1.0                   # the phone pass sets a narrower width and taller panels (see main)
SUFFIX = ""
STORM_NAME_M = 3.0              # named tropical storms at or above this water level, as on the Storms page
SMALL_STORM_M = 2.5             # storms below this, and not tropical, are drawn small and pale so the big ones stand out
# Dune tops for the storm figure (Hannah, 2026-10-04): the island the 1996 run starts from, the 10 m grids of the
# 2009-2014-1996 elevation product; on every 10 m row the highest point within DUNE_ZONE_M of the ocean shoreline, and per
# 500 m stretch the LOWEST of those, the gap or saddle water gets through first. A first version drew the median per
# stretch as one island-wide band, which made it look as if no storm could wash over; Hannah caught it.
DUNE_PRODUCT = "2009-2014-1996"
DUNE_ZONE_M = 150
MHW_NAVD = 0.36                 # as in tools/hatteras_model_stretch.py
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
        # names stagger over two rows, three on phones where Salvo, Waves and Rodanthe crowd together
        rows = {"Waves": 1, "Buxton": 1, "Rodanthe": 2 if SUFFIX else 0}
        ax.text(p["km"], 1.01 + 0.07 * rows.get(p["name"], 0), p["name"], transform=ax.get_xaxis_transform(),
                ha="left" if p["km"] < 1 else "center", va="bottom", fontsize=9.5, color=INK)


def frame(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9.5)


def save(fig, n):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"step{n}{SUFFIX}.png", dpi=150, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(f"wrote step{n}{SUFFIX}.png")


def step2(canvas, cmap, norm, ticks, water):
    fig, ax = plt.subplots(figsize=(W_IN, 3.1 * H_SCALE))
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
    # the stretch shown in step 1 and step 5
    from hatteras_model_stretch import GIS as EXAMPLE
    ax.add_patch(Rectangle(((EXAMPLE - 1) * DOMAIN_KM, 0.02), DOMAIN_KM, rows_km - 0.04, fill=False, ec="#ffd23f", lw=2.2,
                           path_effects=[pe.withStroke(linewidth=3.6, foreground=INK)]))
    ax.annotate("the stretch\nin step 1", xy=((EXAMPLE - 0.5) * DOMAIN_KM, rows_km * 0.75), xytext=((EXAMPLE + 6) * DOMAIN_KM, rows_km * 0.72),
                fontsize=9.5, color="white", va="center", path_effects=[pe.withStroke(linewidth=3, foreground=INK)],
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.4, path_effects=[pe.withStroke(linewidth=3, foreground=INK)]))
    cb = fig.colorbar(im, ax=ax, ticks=ticks, pad=0.01, fraction=0.03, aspect=10)
    cb.set_label("height above\nhigh tide (m)", fontsize=9.5)
    cb.ax.tick_params(labelsize=9)
    frame(ax)
    save(fig, 2)


def step_offset():
    """The model's coastline: how far each stretch's shoreline sits landward of the straight axis the model lines the
    stretches up along, from the offset file the run reads."""
    padded = np.loadtxt(io.tv.INIT_ROOT / HATTERAS_PERIODS[START]["island_offset_file"], skiprows=1, delimiter=",")
    off = padded[io.init.START_REAL_INDEX:io.init.END_REAL_INDEX] / 1000          # km landward
    x = km(io.GIS)
    fig, ax = plt.subplots(figsize=(W_IN, 3.6 * H_SCALE))
    top = off.max() + 1.2
    ax.fill_between(x, off, top, color="#ecdfb9", lw=0)                          # land, landward of the shoreline
    ax.fill_between(x, -0.8, off, color="#cfe0ec", lw=0)                          # ocean
    ax.plot(x, off, color=INK, lw=2)
    ax.axhline(0, color=SEA, lw=1.4, ls=(0, (6, 4)))
    ax.text(8, -0.25, "the model's straight axis", ha="left", va="top", fontsize=9.5, color=SEA)
    for g in (1, 26, 70):
        ax.annotate("", xy=(km(g), off[g - 1]), xytext=(km(g), 0),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, shrinkA=0, shrinkB=0))
        if g < 60:
            ax.text(km(g) + 0.5, off[g - 1] / 2, f"{off[g - 1]:.1f} km", va="center", fontsize=10, color=INK, path_effects=halo)
        else:                                      # too short an arrow to label beside it: the label goes under the axis
            ax.text(km(g), -0.45, f"{off[g - 1]:.1f} km", ha="center", va="center", fontsize=10, color=INK, path_effects=halo)
    ax.text(1, top - 0.4, "island", va="top", fontsize=10, color=INK)
    ax.text(20, 1.0, "Atlantic Ocean", fontsize=10, color=SEA, va="center")
    ax.set_xlim(0, 45)
    ax.set_ylim(-0.8, top)
    ax.set_xlabel("km north of Cape Point", fontsize=10)
    ax.set_ylabel("km landward of the axis", fontsize=10)
    villages(ax)
    frame(ax)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"step_offset{SUFFIX}.png", dpi=150, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(f"wrote step_offset{SUFFIX}.png")


def dune_crests():
    """The lowest dune top above high tide on each of the 90 stretches, from the model's starting grids."""
    import rasterio
    from site_layer.hat_elevation_products import product
    prod = product(DUNE_PRODUCT)
    out = []
    for g in io.GIS:
        with rasterio.open(prod.resampled_10m / f"resampled_domain_{g}_filled.tif") as r:
            z = r.read(1).astype(float)
            z[z == r.nodata] = np.nan
        z -= MHW_NAVD
        crests = []
        for row in z:
            land = np.where(row > 0)[0]
            if len(land):
                east = land.max()                         # ocean on the east (right) side of every grid
                crests.append(np.nanmax(row[max(0, east - DUNE_ZONE_M // 10 + 1):east + 1]))
        out.append(np.nanmin(crests) if crests else np.nan)
    return np.array(out)


def step3():
    """The lowest dune top along the island against the water levels of Isabel, Irene and a large nor'easter. The same
    image goes on the Storms page (Hannah, 2026-10-04: keep this panel only, and show it on both pages)."""
    t = json.loads((DATA / "timeline.json").read_text(encoding="utf-8"))
    s = [e for e in t["storms"] if START <= e["y"] < END + 1]
    fig, bx = plt.subplots(figsize=(W_IN, 3.9 * H_SCALE))

    def level(name):
        return max(e["wl"] for e in s if e["name"] and e["name"].startswith(name))
    low = dune_crests()
    bx.bar(km(io.GIS), low, width=DOMAIN_KM * 0.9, color="#d9c08c", zorder=2)
    levels = [(level("Isabel"), "Isabel", "#b2182b"), (level("Irene"), "Irene and Earl", "#e08214"),
              (3.0, "a large nor'easter", OTHER)]
    for wl, name, col in levels:
        bx.axhline(wl, color=col, lw=1.6, zorder=3)
        n = int(np.sum(low < wl))
        text = f"{name}, {wl:.1f} m: {n} of 90 stretches" if SUFFIX else f"{name}, {wl:.1f} m: over the low point on {n} of 90 stretches"
        bx.text(45.3, wl + 0.06, text, ha="right", va="bottom",
                fontsize=9, color=col, path_effects=halo, zorder=4)
    bx.set_xlim(0, 45.5)
    bx.set_ylim(0, max(np.nanmax(low), levels[0][0]) + 0.6)
    bx.set_xlabel("km north of Cape Point", fontsize=10)
    bx.set_ylabel("lowest dune top on\neach stretch (m)", fontsize=10)
    bx.grid(axis="y", color=GRID, lw=0.6)
    villages(bx)
    frame(bx)
    print("  lowest dune tops: " + ", ".join(f"{nm} {int(np.sum(low < wl))}" for wl, nm, _ in levels))
    save(fig, 3)

def step4():
    sl, fit = io.sea_level(START, END)
    waves = {k: field_default(k) for k in ("hs", "wave_period_s", "wave_asymmetry", "wave_angle_high_fraction")}
    if SUFFIX:
        fig, (a, b) = plt.subplots(2, 1, figsize=(W_IN, 7.2), gridspec_kw={"height_ratios": [1, 1], "hspace": 0.35})
    else:
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


def step6():
    target, _ = io.observed_target(START, END)
    fig, ax = plt.subplots(figsize=(W_IN, 3.6 * H_SCALE))
    v = target.reindex(io.GIS).values
    cols = np.where(v < 0, "#d6604d", "#4393c3")
    ax.bar(km(io.GIS), v, width=DOMAIN_KM * 0.9, color=cols)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xlim(0, 45)
    ax.set_xlabel("km north of Cape Point", fontsize=10)
    ax.set_ylabel(f"shoreline change,\nm per year ({START}–{END})", fontsize=10)
    ax.text(0.5, 0.97, "growing (seaward)", transform=ax.transAxes, ha="center", va="top", fontsize=9.5, color="#2166ac")
    ax.text(0.5, 0.03, "eroding (landward)", transform=ax.transAxes, ha="center", va="bottom", fontsize=9.5, color="#b2182b")
    ax.grid(axis="y", color=GRID, lw=0.6)
    villages(ax)
    frame(ax)
    save(fig, 6)


def main():
    """Draws every step twice: for wide screens, and narrower and taller for phones (<name>_phone.png, which the page
    swaps in below 576 px; Hannah, 2026-10-04, after the phone check found the text unreadable at a third of its size)."""
    global W_IN, H_SCALE, SUFFIX
    plt.rcParams.update({"font.family": "DejaVu Sans"})
    canvas = io.init.detrended_canvas(START, include_buffers=False)
    cmap, norm, ticks, water = io.init.scheme_colours(io.ELEVATION_SCHEME)
    for W_IN, H_SCALE, SUFFIX in ((10.0, 1.0, ""), (5.2, 1.45, "_phone")):
        step2(canvas, cmap, norm, ticks, water)
        step_offset()
        step3()
        step4()
        step6()


if __name__ == "__main__":
    main()
