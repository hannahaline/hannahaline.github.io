# Hatteras stakeholder pages (/hatteras/)

Public-facing pages on Hatteras Island shoreline change, management, and the CASCADE model, written for
Cape Hatteras National Seashore, NCDOT, Dare County and residents, and the Mountains to Sea Fellowship (NC WRRI + NC Sea Grant).
This file is excluded from the build.

## Where things are

| What | Where |
|---|---|
| Pages | `_pages/hatteras/*.md` (permalinks under `/hatteras/`, `nav: false`) |
| Section menu order, ready flags | `_data/hatteras_pages.yml` |
| Section menu, pager, panel placeholder, to-do note | `_includes/hatteras/` |
| Styles (scoped `.hat-*`) | `_sass/_hatteras.scss`, loaded from `assets/css/main.scss` |
| Panel data and scripts (when built) | `assets/hatteras/data/`, `assets/hatteras/js/` |
| Images | `assets/hatteras/img/` |
| Draft switch | `hatteras_draft` in `_config.yml` (banner + to-do notes + panel plans) |

## Decisions (2026-10-02 interview)

- Lives on the `hatteras-site` branch. `deploy.yml` only builds `main`, so nothing here is public until it merges.
- Organised by topic, not chapter. Plain text up front, with "Go deeper" boxes for technical readers.
- Hindcast only for now. "Looking ahead" holds the forecast runs later (`ready: false` until then).
- Key message: a model that reproduces the past helps plan the future.
- Contact by email only. The split-windows explorer is linked from the shoreline page, not folded in.
- Model results are unpublished: keep them out of the public site until the paper is accepted.

## Panels to build

1. `shoreline-map`: Leaflet map, CoastSat LRR 1996–2024 by transect, RdBu, click for a time series.
2. `events-timeline` / `management-timeline`: one timeline engine with storms (HURDAT2 type colours) and management actions.
3. `imagery-compare`: before/after swipe slider at four spots. Sources pending the online search; D: drive as the fallback.
4. `model-vs-observed`: with and without management, canonical windows 1996–2015 and 2010–2026.
5. `nourishment-explorer`, `forecast-explorer`: later.

Panel data is exported from CASCADE as small JSON (per transect or per domain), never raw runs. GitHub Pages has a 1 GB site limit.

## Imagery sources (searched 2026-10-02)

All public domain unless noted. The slider can load the live services directly, so nothing needs re-hosting.

| Years | Source | Access |
|---|---|---|
| 1993 B&W, 1996, 1998 CIR, 2002, 2007, 2010, 2012, 2016, 2020, 2024 | NC OneMap (free without restriction; credit NC OneMap / NC CGIA / NC 911 Board) | `https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_<YEAR>/ImageServer`, `DOQQ_NC_1993`, `DOQQ_NC_CIR_1998`, plus WMS |
| 2008, 2014, 2016; USACE 2017 (4 cm) and 2018 (5 cm) | NOAA Digital Coast | coast.noaa.gov/dataviewer, `coast.noaa.gov/arcgisimg/rest/services/Imagery/...` |
| Irene 2011, Dorian 2019, Erin 2025 | NOAA NGS emergency imagery | Dorian tiles `https://stormscdn.ngs.noaa.gov/20190907a-rgb/{z}/{x}/{y}`; Irene comes as UTM JPEG zips, so re-tile it |
| 2012–2022 every 2 yr | USDA NAIP | EarthExplorer, Planetary Computer |
| 1980s | USGS NHAP/NAPP film, not georeferenced (or the D: drive frames) | EarthExplorer; the NRCS NHAP mosaic is unverified |
| Isabel 2003 | NOAA unrectified frames + USGS obliques only (no ortho) | storms.ngs.noaa.gov, pubs.usgs.gov/ds/761 |

Do not use Esri Wayback or Google Earth: their licences forbid it. Cross-origin loading from NC OneMap and NOAA is untested.

## Preview

    bundle exec jekyll serve --config _config.yml,_config_local.yml

Then open http://localhost:4000/hatteras/.

## Launch checklist

- [ ] Papers accepted, or Hannah has signed off on every number shown
- [ ] `hatteras_draft: false`
- [ ] Every to-do note resolved (search `hatteras/todo.liquid`)
- [ ] NC Sea Grant / WRRI acknowledgement wording and logos checked
- [ ] Imagery licences recorded on the About page
- [ ] Split-windows explorer made public at the same time
- [ ] Add "hatteras" to the main nav, or link it from Research
- [ ] Merge `hatteras-site` into `main`
