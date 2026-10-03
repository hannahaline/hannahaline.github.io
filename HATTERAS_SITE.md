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

1. `shoreline-map`: **BUILT 2026-10-02.** Cape Point to Oregon Inlet (GIS 1–120, 1222 transects), with windows for the whole record (1996–2026), 1996–2015 and 2010–2026.
   - Map: transects coloured in 9 RdBu classes, with NC-12, the villages and the groins. Background is NC OneMap over USGS imagery, or the plain map.
   - Clicking a transect shows plain-language rates for all three windows and the full CoastSat time series with the window's fit. The profile shows the 7-domain LOWESS (GIS 1–10 as domain means), and there is a table view.
   - Share links: `#t=<transect id>`.
   - Data: `python tools/hatteras_shoreline_data.py`. It refits the LRR from the time series and refuses to write if the fit differs from the published `lrr/<window>/` tables. GIS 91–120 is refit only; it matches `lrr/1996_2024/ext` for 1996–2024.
2. `events-timeline` / `management-timeline`: one timeline engine with storms (HURDAT2 type colours) and management actions.
3. `imagery-compare`: **BUILT 2026-10-02.** A swipe slider. Layers and places live in `_data/hatteras_imagery.yml`, which you can edit by hand.
   - Layers: 11 public layers, all loaded live with nothing re-hosted. NC OneMap gives 1993, 1996, 1998 CIR, 2002, 2007, 2010, Feb–Mar 2012, Jan–Feb 2016, Feb 2020 and Mar 2024 (mosaic dates read from the Dare County tile names). NOAA adds Dorian, 7 Sep 2019.
   - Places: the S-curves and Jug Handle Bridge, New Inlet (located on the 2012 photo), Avon, and Buxton.
   - Every caption fact comes from the timeline xlsx or the config. Links like `#spot=<id>` open a given place.
   - Not added: Irene 2011 (NOAA zips would need re-tiling), the 1980s film, and Buxton 2017 (waiting on Hannah's model update).
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

**Local catch:** jekyll-terser minifies the site's own JS. With no Node installed, ExecJS falls back to Windows JScript, which can't run Terser, so `assets/hatteras/js/*.js` is silently missing from local builds. The GitHub build is fine. To fix it locally, install Node LTS (`winget install OpenJS.NodeJS.LTS`). The alternative is to copy `assets/hatteras/js/` into `_site/assets/hatteras/js/` after each build.

## Launch checklist

- [ ] Papers accepted, or Hannah has signed off on every number shown
- [ ] `hatteras_draft: false`
- [ ] Every to-do note resolved (search `hatteras/todo.liquid`)
- [ ] NC Sea Grant / WRRI acknowledgement wording and logos checked
- [ ] Imagery licences recorded on the About page
- [ ] Split-windows explorer made public at the same time
- [ ] Add "hatteras" to the main nav, or link it from Research
- [ ] Merge `hatteras-site` into `main`
