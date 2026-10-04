# Hatteras stakeholder pages (/hatteras/)

Public-facing pages on Hatteras Island shoreline change, management, and the CASCADE model, written for
Cape Hatteras National Seashore, NCDOT, Dare County and residents, and the Mountains to Sea Fellowship (NC WRRI + NC Sea Grant).
This file is excluded from the build.

## Where we left off (2026-10-03)

**State:** everything below is committed on `hatteras-site` (last commit 9464eb7). Nothing is pushed or public. The private preview (claude.ai/artifact/TAn39uBqS5KyRtN43pHvDE) is at version 16 and is behind the branch; see to-do 1.

**Pages now:** The basics (Overview, How the island works), What happened (Shoreline change + 3 sub-pages, Storms, Then and now), What we can do (Management, The model, Looking ahead - hidden), More (Glossary, About).

**Done 10-03 (latest session):**
- Overview Figure 1: lighthouse before/after pair (USAF Jan 1999 by the surf; NPS 2004 at the new site).
- Shoreline change split into an intro (`/hatteras/shoreline-change/`) and three sub-pages with tabs (`shoreline_tabs.liquid`): Survey lines (map), Along the island (profile + table), Shorelines through time (new). Sub-pages set `section:` so the menu and pager treat them as Shoreline change. One script, `shoreline-map.js`, builds whichever part is on the page (`shoreline_map.liquid part="map|profile"`).
- Shorelines through time: calendar-year mean shorelines for 1985/1995/2005/2015/2025 (`tools/hatteras_decadal_shorelines.py`), YlOrRd gradient with a colour bar, photo switch (latest / 1993 / 2002 / 2016 / 2024, one NC OneMap exportImage per view), and zoom buttons from the data: biggest changes (Cape Point +70, Buxton -75, North of Avon +95, Rodanthe -145, Pea Island -110 m) and stable stretches to compare (South of Avon 0, Avon to Salvo -15, North of Rodanthe +20 m; within ~20 m in all five years).
- How the island works:
  - Longshore section: USGS photos (dye in the surf, Cape Point) replace the diagram. `longshore.svg` is still generated but no longer used.
  - Overwash section: the USGS Isabel photo of sand over NC-12 (DS 761 frame r045s18) replaces the Buxton/Sandy pair. The Sandy files are kept in `img/sandy/`, unused.
  - Dunes diagram: redrawn as collision vs overwash (Sallenger 2000), with the water levels labelled.
  - New 2x2 photo figure of built dunes: CCC sand fence 1936, no dune at the S-curves 2008 (USGS baseline survey), the dune rebuilt there in 2011 (NCDOT, CC BY 2.0), and the Rodanthe breach in 2020.
  - The Key terms drop-down was removed in favour of a pointer to the glossary.
- Rejected on purpose:
  - USGS North Core Banks Dorian photos: those channels were cut by sound-side outflow, not overwash.
  - The Hatteras Village Isabel pair on the island page: it is already on Storms.

## To do next time

**Needs Hannah:**
1. Collaborators' full names and affiliations for About (to-do note in `about.md`).
2. Check the model-page draft paragraph against the 2026-window matrix (to-do note in `model.md`, behind `hatteras_draft`).
3. Review the glossary definitions on `/hatteras/glossary/` (berm, transect and surge are approved; the other 20 are drafts).
4. CoastSat Live download date for the About page: she wasn't sure; find it.
5. Reference author lists on the model page.
6. Decide whether the Sandy pair (Buxton 2011/2012) goes on the Storms page or is dropped.

**Can do without her:**
7. Refresh the private preview: build, copy the JS in by hand, run `make_preview.py`, then publish changed files to the same URL. It is missing everything from the dunes diagram onward.
8. Model-vs-observed panel: the matrix was re-run on the 2026 windows (CASCADE eac55c59, Rodanthe 2014 at 1.62 M cy). Re-run `tools/hatteras_model_data.py` and check that its bias/RMSE check still passes.
9. CASCADE fill outputs (`attribution_nourishment.csv` + figures) still list 3 fills, not Buxton 2017. Re-run once the other session's uncommitted work in that folder is committed.
10. Phone-width check of the new pages: the shoreline tabs, the through-time zoom-button rows, and the 2x2 dune grid. Only the dune grid's stacking was checked, by CSS.
11. Overview card and the Explore text for Shoreline change: make sure they still describe the split pages.
12. Stale `HATTERAS_SITE.md` sections below: the glossary entry still mentions the Key terms box, and the figures list lacks the new photos (longshore/, dunes/, isabel/overwash_nc12_2003.jpg, lighthouse_1999.jpg).
13. Optional: delete `longshore.svg` from the generator and the includes if the photos stay.

**Later:**
14. Nourishment explorer panel; the Looking ahead page (forecasts), then set `ready: true`.
15. Launch: the checklist at the end of this file, only when Hannah says so. The split-windows explorer launches at the same time; its link 404s until then.

**Loose ends (unchanged):**
- CASCADE's `HATTERAS_ROAD_EVENTS` calls the 1989 move "Pea Island"; the timeline sheet says S-curves. Flagged, not changed.
- Dorian: Category 2 from HURDAT2 (85 kt); the CASCADE match table still says Cat 1.
- Local builds drop `assets/hatteras/js/*.js` (no Node, so Terser fails); copy it in after each build.
- Leave the `_projects/*.md` edits alone and commit by path.

## Earlier session notes (2026-10-02 to 10-03; superseded by the to-do list above where they differ)

**Done and committed on `hatteras-site` (not pushed, not public):**
- Nine pages, in menu groups (since 10-03): The basics (Overview, How the island works), What happened (Shoreline change, Storms, Then and now), What we can do (Management, The model, Looking ahead - hidden), More (About). Groups live in `_data/hatteras_pages.yml`; the island page's URL is still /hatteras/island/.
- The shoreline page was split three ways on 10-02: Shoreline change (map, record, fills, 2021 shift), Storms (timeline, Isabel, Irene, Dorian), and Then and now (photo slider).
- Built so far: the shoreline map, the storms and management timeline, the photo slider (saved photos), the study-area map with the Jug Handle Bridge, the cross-section (textbook style), the Isabel and Irene USGS photos, and a first draft of all page text.

**Dorian: DONE 2026-10-03, written as text with no photo pair.**
- Checked the NOAA 7 Sep 2019 photos (the only Dorian flight over NC-12) against NC OneMap 2016: the four slider spots, NC-12 every 2 km from Buxton to Oregon Inlet, and close-ups at km 18-24, 44, 46, 50 and 54. No fresh washover anywhere, which matches OBS-024. The 2019 photo at the S-curves shows equipment on NC-12; the cause is unknown, so don't caption it.
- The page gives the landfall (HURDAT2), the water level and hours above the berm (storm record), the "largely intact" finding, and a pointer to the 2019 photo in Then and now. Sources are in a Liquid comment under the section.
- Category 2 from HURDAT2 (85 kt), Hannah's call 10-03; the CASCADE match table still says Cat 1. Left out on purpose: the 4-7 ft surge (no citable link in the repo), and the storm sheet's "NC-12 closed ~3 months" (possibly Ocracoke; unchecked).
- Don't use the USGS "Cape Hatteras" Dorian pair: its photos are North Core Banks.

**Next, in order:**
1. ~~Finish Dorian~~ (done 10-03).
2. Private preview: claude.ai/artifact/TAn39uBqS5KyRtN43pHvDE is **version 13 (10-03)**: everything through the phone-width fixes. To refresh: `jekyll build -d <scratch>/site_new`, copy `assets/hatteras/js/` in by hand (no Node), run `make_preview.py` (10-03 session scratchpad; it now keeps `#fragments` in page links and lists `glossary`), then publish the changed files to the same URL. Files left out of a publish are kept.
2b. **10-03 to-do pass, done:** citations confirmed with DOIs (CASCADE is published, Earth's Future 2024, Parts 1 and 2); dune-line history and the Buxton groins + 1999 lighthouse move written with sources (the groins protected the Navy facility; the lighthouse is not the stated purpose); lidar sources and CoastSat Live on About; village numbers re-checked; model cards turned into a diagram; longshore (OSM outline, `tools/data/hatteras_outline_osm.json`) and overwash diagrams on the island page; study-area map redrawn (inset upper left, sand bands, groin line, scale bar and north arrow moved); headline "Living with a changing coast"; NPS Buxton houses photo on the overview.
   - Photo candidates still to choose from (all public domain): overwash at Buxton after Sandy (USGS, usgs.gov/media/images/oblique-aerial-photographs-buxton-north-carolina); NC-12 behind a low dune has no public-domain match (Ken Lund's Mirlo Beach photos are CC BY-SA 2.0); hero: NPS lighthouse drone photos on Wikimedia Commons, or a 1999 USAF aerial of the lighthouse before its move.
2c. **10-03, items 6-9:**
   - Fill steps: `python tools/hatteras_fill_steps.py` (read-only on CASCADE's detrended matrix, same method as coastsat_position_attribution; writes tools/data/fill_steps.csv). Buxton 2017 = +33.0 m; it reproduces the CASCADE table for the other three. CASCADE's `NOURISHED` list has included Buxton 2017 since d896eecb (10-02), but its outputs (attribution_nourishment.csv and the figures) do not include it yet; that folder has another session's uncommitted work, so they were not rerun from here.
   - NC-12 photo: NC OneMap 2016 aerial at the S-curves (public), not the CC BY-SA Mirlo Beach photo.
   - Model paragraph: drafted inside `{% if site.hatteras_draft %}`, so it never shows publicly until Hannah checks it against the 2026-window matrix.
   - Phone width (checked in a 390 px frame): `html:has(.hat-bleed)` clips the 100vw scrollbar overflow; diagrams have a 720 px minimum width and scroll sideways, opening at `data-scroll-start`; play-bar labels are spaced by measured width, at most 3 rows, the rest as ticks.
3. Work through the to-do notes (`grep -rn "hatteras/todo.liquid" _pages/hatteras`), starting with the ones only Hannah can answer:
   - collaborators' full names;
   - the reference author lists;
   - NC Sea Grant acknowledgement wording;
   - how much of the 2021 shift to show before the paper.
4. Remaining panels: model-vs-observed (unpublished; waits on the model update with Buxton 2017), the nourishment explorer, and Looking ahead (forecasts).
5. Launch checklist (below), only when Hannah says so.

**Loose ends to remember:**
- `HATTERAS_ROAD_EVENTS` in CASCADE's config says "Pea Island" for the 1989 move. The timeline sheet calls it the S-curves relocation (GIS 84–87). Flagged to Hannah, not changed.
- Local previews: Terser drops `assets/hatteras/js/*.js` without Node (see Preview). The review server was `python -m http.server 4123` in the scratchpad build folder; it stops when the session ends.
- Another session left uncommitted edits in `_projects/*.md` in this repo. Leave them alone and commit by path.

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

## Figures

- `assets/hatteras/img/study_area_map.jpg`, from `tools/hatteras_stakeholder_map.py`: north-up, Esri imagery, villages, NC-12, nourishment reaches (read from shoreline_rates.json), groins, and a locator. NC-12 is `nc12_current.geojson`, which already follows the Jug Handle Bridge (within 3 m of OpenStreetMap); the dashed beach road it bypassed is cut from `nc12_2008.geojson` between the bridge's ends.
- `_includes/hatteras/cross_section.svg`, from `tools/hatteras_cross_section.py`: a schematic sound-to-ocean slice, inline so it takes the page font.

- `assets/hatteras/img/isabel/`: USGS oblique photos, public domain.
  - The 1999 and 2003 pairs for Frisco and Hatteras Village were extracted from the high-resolution PDF of Fact Sheet 2009-3025 with `pdfimages`. The PDF stores them flipped top to bottom, so they were flipped back; check that the camera date stamp reads "21 16 27".
  - `breach_2003.jpg` is from usgs.gov/media/images/hatteras-island-post-hurricane-isabel.
  - Both places are south-west of Cape Point, outside the modelled reach; the page says so.

- `assets/hatteras/img/irene/`: USGS oblique photos (Karen Morgan, SPCMSC), public domain. Each place is cut from one USGS composite into its three panels (overview 30 Aug 2011, 6 May 2008, 31 Aug 2011) by finding the white separator rows. Sources: usgs.gov/media/images/oblique-aerial-photograph-rodanthe-nc-enlarged-details and ...-pea-island-nc-enlarged-details.
- The cross-section was redrawn 2026-10-02 in a textbook style: zone brackets, stippled sand, and outline symbols (houses on pilings, maritime oaks, shrubs, dune and marsh grass).

## Panels to build

1. `shoreline-map`: **BUILT 2026-10-02.** Cape Point to Oregon Inlet (GIS 1–120, 1222 transects), with windows for the whole record (1996–2026), 1996–2015 and 2010–2026.
   - Map: transects coloured in 9 RdBu classes, with NC-12, the villages and the groins. Background is NC OneMap over USGS imagery, or the plain map.
   - Clicking a transect shows plain-language rates for all three windows and the full CoastSat time series with the window's fit. The profile shows the 7-domain LOWESS (GIS 1–10 as domain means), and there is a table view.
   - Share links: `#t=<transect id>`.
   - Data: `python tools/hatteras_shoreline_data.py`. It refits the LRR from the time series and refuses to write if the fit differs from the published `lrr/<window>/` tables. GIS 91–120 is refit only; it matches `lrr/1996_2024/ext` for 1996–2024.
2. `timeline`: **BUILT 2026-10-02.** One SVG engine, `_includes/hatteras/timeline.liquid`. The shoreline page shows everything; the management page uses `mode="management"` and shows management events only.
   - Storms: 421 high-water events, 1984–2025. They come from the hindcast series (1984_2004 up to 1995, 1996_2015 for 1996–2009, 2010_2026 from 2010), with peaks rebuilt and Rhigh-checked through `storm_figures.py`, and HURDAT2 classes and names in the house colours.
   - 2025 events (Erin among them) are drawn hollow, at their midpoint: the WIS record ends in 2024, so their peaks can't be checked.
   - Management: from `HATTERAS_ROAD_EVENTS`, `HATTERAS_NOURISHMENT_PROJECTS` and the bridge rows of the timeline sheet. Open marks are not in the model.
   - Hovering a management event fires `hat:reach`, which lights its km range on the shoreline map and profile.
   - Data: `python tools/hatteras_timeline_data.py`, run with the CASCADE venv.
   - Map fill bands now also read `HATTERAS_NOURISHMENT_PROJECTS`; fills on the same reach share a band. Re-run both tools whenever the config changes.
3. `imagery-compare`: **BUILT 2026-10-02.** A swipe slider. Layers and places live in `_data/hatteras_imagery.yml`, which you can edit by hand.
   - Layers: 11 public layers, all loaded live with nothing re-hosted. NC OneMap gives 1993, 1996, 1998 CIR, 2002, 2007, 2010, Feb–Mar 2012, Jan–Feb 2016, Feb 2020 and Mar 2024 (mosaic dates read from the Dare County tile names). NOAA adds Dorian, 7 Sep 2019.
   - Places: the S-curves and Jug Handle Bridge, New Inlet (located on the 2012 photo), Avon, and Buxton.
   - Every caption fact comes from the timeline xlsx or the config.
   - **Since 2026-10-02 the photos are saved, not live.** NC OneMap renders year layers on request and slowed to 15–60 s per tile, so old years never loaded. `python tools/hatteras_imagery_data.py` saves one JPEG per place and layer into `assets/hatteras/img/compare/` (44 images, about 10 MB). The slider clips the right-hand image; Leaflet is no longer used. Re-run it after changing places or layers in the yml.
   - Not added: Irene 2011 (NOAA zips would need re-tiling), the 1980s film, and Buxton 2017 (waiting on Hannah's model update).
3a. Shoreline map "Change year by year" mode: **BUILT 2026-10-03** (Hannah's picks: position not rate, 1984-2025, a mode on the map, 2021 decided before launch).
   - `python tools/hatteras_shoreline_years.py` writes `shoreline_years.json`: each transect's yearly mean CoastSat position minus its 1984-86 mean, smoothed with the same 7-domain LOWESS (GIS 1-10 domain means) as the rate profile; <2 shorelines in a year = empty. The 1984 baseline alone has ~5 shorelines, hence 1984-86.
   - Map colours in metres (5/25/50/75 classes, same RdBu), the profile on a fixed axis, a play bar with fill years and named storms of at least 3.5 m from timeline.json. The data loads only when the mode opens. Run it after `hatteras_shoreline_data.py`; it refuses to write if the transects differ.
   - Not a sliding-window rate: short windows are unstable on Hatteras (window convergence work), so a rate per year would mostly animate noise.
   - Cape Point reads -50 m in 2020 and about +190 m in 2025; that is the post-2021 growth, consistent with its positive 1996-2026 rate.
3b. `sea-level`: **BUILT 2026-10-03** on the How the island works page (Hannah's picks: record + trends, interactive SVG, model periods).
   - The Duck monthly record (faded), yearly means for full years (2012 is missing a month, so the line breaks), NOAA's whole-record trend dashed, and the 1996–2015 and 2010–2026 trends in the house red and blue. Hover or the arrow keys pick a year.
   - Data: `python tools/hatteras_sealevel_data.py` reads CASCADE `2-rslr/record` and `fits/duck_rslr_rates.csv`, refits each period, and refuses to write if the slope or month count differs from the table. Re-run it if the record or the periods change.
   - Text: 4.9 mm/yr and about 23 cm since 1978 (NOAA trend line), 3.8 and 5.5 mm/yr for the periods, and the point that 2010–2024 gives 6.5, so short-window rates move. The model uses 4 and 5 mm/yr (config, rounded).
3c. Storm photo slider: **TRIED AND REMOVED 2026-10-03.** A Rodanthe (Irene) slider warped the 2008 photo onto the 2011 one from hand-picked points, but Hannah judged it not working, so all storm pairs are side by side again (commit a0bcb2b has the tool if it is ever wanted). Automatic SIFT matching was unstable on these pairs too, and Frisco, Hatteras Village and Pea Island were shot from different flight lines.
3d. Glossary: **BUILT 2026-10-03** (Hannah asked for a site-wide one). `_data/hatteras_glossary.yml` (23 terms) feeds `/hatteras/glossary/` (menu: More), the Key terms box on How the island works (`glossary_list.liquid ids=...`), and in-text links (`{% include hatteras/term.liquid id="..." %}`: dotted underline, definition on hover). First plain use per page is linked; terms the sentence itself defines, headings, place names and card text are not. Definitions are drafts for Hannah to check.
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
