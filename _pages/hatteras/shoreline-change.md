---
layout: page
title: Historic shoreline change
permalink: /hatteras/shoreline-change/
description: Where Hatteras Island's shoreline has retreated or grown since 1996, and the events that show up in the record.
nav: false
map: true
chart:
  chartjs: true
---

{% include hatteras/subnav.liquid %}

<p class="hat-lead">
Satellites have photographed Hatteras Island many times a year since the 1980s.
By tracing the {% include hatteras/term.liquid id="shoreline" text="shoreline" %} in each image, we can see where the beach has moved landward, where it has grown, and when the big changes happened.
</p>

## Where is the shoreline eroding or growing?

Each coloured line on the map is a survey line across the beach, from Cape Point to Oregon Inlet.
Red lines show where the shoreline has moved landward, and blue lines show where it has moved seaward.
Use the buttons to compare the whole satellite record with the two periods the model recreates.

{% include hatteras/shoreline_map.liquid %}

### What the record shows

Over the whole satellite record, the island as a whole has held roughly steady: about half of the beach has moved landward and half seaward.
That average hides large differences from place to place.

- **Cape Point** has grown seaward faster than anywhere else, by about 2.4 m per year on average (roughly 24 m per decade).
- **Buxton** lost ground through the 1990s and 2000s, about 1.4 m per year from 1996 to 2015. Since then, {% include hatteras/term.liquid id="beach-nourishment" text="beach nourishment" %} in 2017 and 2022 has added sand, and the record shows growth.
- **Avon** sits on a shoreline that swings between eroding and growing stretches a few kilometres apart. Its nourished stretch jumped seaward after the 2022 fill.
- **The long stretch between Avon and Salvo** has changed least, staying within a metre per year of no change along about three-quarters of its length.
- **Salvo, Waves and Rodanthe** have moved landward on average, about 0.5 m per year over the whole record, with local hot spots of 2 to 3 m per year.
- **Pea Island** has the most persistent erosion: about 0.9 m per year over the whole record, and faster since 2010.

Rates that include the last few years are pushed seaward by an island-wide shift in 2021 (described below). That is why the 2010–2026 view shows more growth than the earlier period.

{% include hatteras/todo.liquid text="Check these village summaries against your own reading. Numbers are means of the transect rates in each reach (GIS 1–5, 6–15, 21–31, 32–67, 68–83, 91–120), from shoreline_rates.json." %}

<details class="hat-deeper" markdown="1">
<summary>Go deeper: how shoreline change is measured</summary>

Shoreline positions come from [CoastSat](https://github.com/kvos/CoastSat), an open-source toolkit that finds the water's edge in Landsat and Sentinel-2 satellite images and corrects it for the tide.
Positions are measured along {% include hatteras/term.liquid id="transect" text="transects" %}, shore-normal lines spaced every 50 m along the island.
The rate at each transect is the slope of a straight-line fit through every position in the period (a *linear regression rate*), reported in metres per year.
Negative rates mean {% include hatteras/term.liquid id="erosion" text="erosion" %}, and positive rates mean {% include hatteras/term.liquid id="accretion" text="accretion" %}.
A rate is shown as "no clear trend" when it is smaller than its 95% uncertainty.
The smoothed line on the chart is a LOWESS fit over about 3.5 km (seven 500 m model domains). Near Cape Point (the first 5 km) it is replaced by the average of each 500 m stretch, because the shoreline there changes too sharply to smooth.
Periods run from 1 January of the first year to 31 December of the last.

{% include hatteras/todo.liquid text="Confirm the tide and beach-slope correction settings against the CoastSat run." %}

</details>
## Events that stand out

The shoreline does not change smoothly. Storms take sand away in days, and nourishment projects add it back in weeks.
The big storms have [their own page]({{ '/hatteras/storms/' | relative_url }}); two other events stand out in the satellite record.

### Beach nourishment, 2014 to 2022

Beach nourishment shows up in the satellite record as a sudden seaward jump in the year after the sand is placed, on that stretch of beach only.
Compared with the rest of the island, the shoreline jumped about 15 m at Rodanthe after the 2014 fill, 11 m at Avon after 2022, and 5 m at Buxton after 2022.
The Buxton 2022 jump is smallest because less sand was placed per metre of beach.
Click a nourished stretch on the map to see its jump, marked in gold, in the full record.

{% include hatteras/todo.liquid text="Buxton 2017's step, and how long each fill's added width lasts: not yet measured." %}

### The 2021 shift

Between 2020 and 2021, the shoreline moved seaward by about 17 m almost everywhere on the island, in a single year.
This was twice as large as any other year-to-year change in the record. It happened on beaches that were never nourished, a year before the 2022 projects.
Several checks show that it is a real change in the beach, not a quirk of the satellite images:

- the {% include hatteras/term.liquid id="dune-line" text="dune line" %}, traced separately from aerial photos, moved seaward by the same amount between 2009 and 2023;
- the jump appears in every season of imagery on its own;
- neighbouring stretches of beach agree closely, while stretches farther apart differ.

The shoreline has since drifted part of the way back. We have not yet tested what caused it; recovery after Hurricanes Dorian (2019) and Isaias (2020) is one possibility.
Because it falls near the end of the record, this one event has a large effect on any rate that includes it.

{% include hatteras/todo.liquid text="Decide how much of this to show before the paper is out. Source: 5-scr/1-observations/detrended_position/README.md." %}

## Explore further

For a closer look, the [shoreline windows explorer](https://hannahaline.github.io/hatteras-shoreline-windows/) shows how the measured rate at any stretch of beach depends on which years you include.

{% include hatteras/todo.liquid text="The explorer is still private, so this link 404s until it launches. Launch both together." %}

{% include hatteras/pager.liquid %}
