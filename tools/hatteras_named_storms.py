"""
The biggest named storms at Hatteras since 1984, ranked by how high the water reached, for the Storms page of the
Hatteras stakeholder pages.

    python tools/hatteras_named_storms.py

Each bar is one named storm's peak water level at the shore (tide, surge and wave run-up, from
assets/hatteras/data/timeline.json, the same storm record as the model), coloured by its Saffir-Simpson category at its
closest approach to Cape Hatteras in HURDAT2 and labelled with that distance. The highest nor'easter in the record is
drawn as a line for comparison. The 1991 "Perfect Storm" is the unnamed subtropical storm in HURDAT2. Storms after the
wave record ends (2025) are drawn hollow, as on the timeline they replace. Hannah asked (2026-10-04) for a storm figure
that shows the named storms' categories, in place of the every-event timeline; the ranking shows that category near
Hatteras says little about how high the water got.
Writes assets/hatteras/img/named_storms.png and assets/hatteras/data/named_storms.json.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-04
"""
import json
import math
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

SITE = Path(__file__).resolve().parents[1]
HURDAT = SITE.parent / "CASCADE/data/hatteras_init/3-env-forcings/1-records/hurdat2/hurdat2-1851-2025-091226.txt"
TIMELINE = SITE / "assets/hatteras/data/timeline.json"
OUT_IMG = SITE / "assets/hatteras/img/named_storms.png"
OUT_JSON = SITE / "assets/hatteras/data/named_storms.json"
CAPE = (35.25, -75.52)
TOP_N = 15
INK, MUTED, GRID = "#1a1a1a", "#5b6469", "#e6e9eb"
COLOURS = {"tropical storm": "#fdd49e", "Cat 1": "#fdae6b", "Cat 2": "#f16913", "Cat 3": "#d94801", "Cat 4": "#8c2d04",
           "Cat 5": "#4a1402", "subtropical": "#bdbdbd", "post-tropical": "#bdbdbd"}
STATUS = {"EX": "post-tropical", "SS": "subtropical", "SD": "subtropical", "LO": "post-tropical", "DB": "post-tropical",
          "WV": "post-tropical"}
# HURDAT2 names for storms the record names differently
ALIASES = {"Subtropical storm 1991": ("Unnamed", 1991, "the Perfect Storm")}


def km_to_cape(lat, lon):
    p1, p2 = math.radians(CAPE[0]), math.radians(lat)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon - CAPE[1]) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(a))


def category(status, wind_kt):
    if status not in ("HU", "TS", "TD"):
        return STATUS.get(status, "post-tropical")
    for limit, name in ((64, "tropical storm"), (83, "Cat 1"), (96, "Cat 2"), (113, "Cat 3"), (137, "Cat 4")):
        if wind_kt < limit:
            return name
    return "Cat 5"


def hurdat():
    """{(Name, year): [(status, lat, lon, wind_kt)]}; the one malformed line in the file is skipped."""
    lines = HURDAT.read_text().splitlines()
    out, i = {}, 0
    while i < len(lines):
        head = [x.strip() for x in lines[i].split(",")]
        n, key = int(head[2]), (head[1].title(), int(head[0][4:8]))
        for line in lines[i + 1:i + 1 + n]:
            f = [x.strip() for x in line.split(",")]
            la, lo = re.search(r"(\d+\.\d)([NS])", line), re.search(r"(\d+\.\d)([EW])", line)
            try:
                wind = int(f[6])
            except (IndexError, ValueError):
                continue
            if la and lo:
                out.setdefault(key, []).append((f[3], float(la.group(1)) * (1 if la.group(2) == "N" else -1),
                                                float(lo.group(1)) * (-1 if lo.group(2) == "W" else 1), wind))
        i += 1 + n
    return out


def main():
    tracks = hurdat()
    storms = json.loads(TIMELINE.read_text(encoding="utf-8"))["storms"]
    named = {}
    for e in storms:
        if e["name"] and e["type"] == "tropical" and (e["name"] not in named or e["wl"] > named[e["name"]]["wl"]):
            named[e["name"]] = e
    rows = []
    for name, e in named.items():
        if name in ALIASES:
            key, label = ALIASES[name][:2], ALIASES[name][2]
        else:
            base, year = name.rsplit(" ", 1)
            key, label = (base.title(), int(year)), base
        pts = tracks.get(key)
        if not pts:
            print(f"  no HURDAT2 track for {name}; left out")
            continue
        status, lat, lon, wind = min(pts, key=lambda p: km_to_cape(p[1], p[2]))
        rows.append({"name": label, "year": int(e["t"][:4]), "water_m": e["wl"], "category": category(status, wind),
                     "wind_kt": wind, "km": round(km_to_cape(lat, lon)), "after_wave_record": bool(e.get("unchecked"))})
    rows.sort(key=lambda r: -r["water_m"])
    top = rows[:TOP_N]
    noreaster = max((e for e in storms if e["type"] != "tropical"), key=lambda e: e["wl"])

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, ax = plt.subplots(figsize=(9.5, 0.38 * len(top) + 1.4))
    y = list(range(len(top)))[::-1]
    for yi, r in zip(y, top):
        col = COLOURS[r["category"]]
        ax.barh(yi, r["water_m"], color="white" if r["after_wave_record"] else col, edgecolor=col if r["after_wave_record"] else "none",
                hatch="////" if r["after_wave_record"] else None, lw=1.2, height=0.72)
        where = "passed almost overhead" if r["km"] < 25 else f"{r['km']} km away"
        ax.text(r["water_m"] + 0.05, yi, f"{r['category']}, {where}", va="center", fontsize=9, color=MUTED, zorder=4,
                path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    ax.set_yticks(y)
    ax.set_yticklabels([f"{r['name']} {r['year']}" for r in top], fontsize=9.5)
    ax.axvline(noreaster["wl"], color="#4393c3", lw=1.4, ls=(0, (5, 3)), zorder=1)
    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
             "December"][int(noreaster["t"][5:7]) - 1]
    ax.text(noreaster["wl"] + 0.04, len(top) - 0.35, f"highest nor'easter, {month} {noreaster['t'][:4]}: {noreaster['wl']:.1f} m",
            fontsize=9, color="#2166ac", va="bottom")
    ax.set_xlim(0, max(r["water_m"] for r in top) + 1.6)
    ax.set_ylim(-0.6, len(top) + 0.2)
    ax.set_xlabel("how high the water reached at the shore (m above high tide)", fontsize=10)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    shown = [c for c in COLOURS if any(r["category"] == c for r in top)]
    seen, handles = set(), []
    for c in shown:
        lab = "subtropical or post-tropical" if c in ("subtropical", "post-tropical") else c
        if lab not in seen:
            seen.add(lab)
            handles.append(Patch(color=COLOURS[c], label=lab))
    ax.legend(handles=handles, title="category when closest to Hatteras", title_fontsize=9, fontsize=9, frameon=False,
              loc="lower right", ncol=1)
    fig.savefig(OUT_IMG, dpi=160, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    OUT_JSON.write_text(json.dumps({"source": "HURDAT2 closest approach to Cape Hatteras; water levels from timeline.json",
                                    "highest_noreaster": {"year": int(noreaster["t"][:4]), "water_m": noreaster["wl"]},
                                    "storms": rows}, indent=1), encoding="utf-8")
    for r in top:
        print(f"  {r['water_m']:.2f}  {r['name']} {r['year']}: {r['category']}, {r['km']} km")
    print(f"wrote {OUT_IMG.relative_to(SITE)}")


if __name__ == "__main__":
    main()
