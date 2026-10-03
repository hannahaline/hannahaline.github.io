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
By tracing the shoreline in each image, we can see where the beach has moved landward, where it has grown, and when the big changes happened.
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
- **Buxton** lost ground through the 1990s and 2000s, about 1.4 m per year from 1996 to 2015. Since then, beach nourishment in 2017 and 2022 has added sand, and the record shows growth.
- **Avon** sits on a shoreline that swings between eroding and growing stretches a few kilometres apart. Its nourished stretch jumped seaward after the 2022 fill.
- **The long stretch between Avon and Salvo** has changed least, staying within a metre per year of no change along about three-quarters of its length.
- **Salvo, Waves and Rodanthe** have moved landward on average, about 0.5 m per year over the whole record, with local hot spots of 2 to 3 m per year.
- **Pea Island** has the most persistent erosion: about 0.9 m per year over the whole record, and faster since 2010.

Rates that include the last few years are pushed seaward by an island-wide shift in 2021 (described below). That is why the 2010–2026 view shows more growth than the earlier period.

{% include hatteras/todo.liquid text="Check these village summaries against your own reading. Numbers are means of the transect rates in each reach (GIS 1–5, 6–15, 21–31, 32–67, 68–83, 91–120), from shoreline_rates.json." %}

<details class="hat-deeper" markdown="1">
<summary>Go deeper: how shoreline change is measured</summary>

Shoreline positions come from [CoastSat](https://github.com/kvos/CoastSat), an open-source toolkit that finds the water's edge in Landsat and Sentinel-2 satellite images and corrects it for the tide.
Positions are measured along transects, shore-normal lines spaced every 50 m along the island.
The rate at each transect is the slope of a straight-line fit through every position in the period (a *linear regression rate*), reported in metres per year.
Negative rates mean erosion, and positive rates mean accretion.
A rate is shown as "no clear trend" when it is smaller than its 95% uncertainty.
The smoothed line on the chart is a LOWESS fit over about 3.5 km (seven 500 m model domains). Near Cape Point (the first 5 km) it is replaced by the average of each 500 m stretch, because the shoreline there changes too sharply to smooth.
Periods run from 1 January of the first year to 31 December of the last.

{% include hatteras/todo.liquid text="Confirm the tide and beach-slope correction settings against the CoastSat run." %}

</details>

## Events in the record

The shoreline does not change smoothly. Storms take sand away in days, and nourishment projects add it back in weeks.
These events stand out in the record.

Each dot is one high-water event: a time when tide, storm surge and waves together pushed water high up the beach. The taller the stem, the higher the water reached. Below are the management projects that changed the beach and the road. Hover over a project to see its stretch of beach on the map above.

{% include hatteras/timeline.liquid %}

### Hurricane Isabel, 2003

Isabel brought the highest water of the whole record: an estimated 5.2 m above mean high water at the shore in September 2003, almost a metre higher than any storm since.
There are no map-ready aerial photos from just after Isabel, so the photo comparison further down jumps from 2002 to 2007. Oblique photos taken from a plane fill that gap.

The worst damage was just south-west of Cape Point, beyond the stretch this research models. There, Isabel cut a new breach about 500 m wide that completely severed the island, and it overwashed the villages of Frisco and Hatteras Village.
The U.S. Geological Survey photographed the same places before the storm and three days after it.

{% assign isabel = '/assets/hatteras/img/isabel/' | relative_url %}
<figure class="hat-photo-wide">
<img src="{{ isabel }}breach_2003.jpg" alt="Oblique aerial photo of Hatteras Island after Hurricane Isabel, with ocean water running through a wide breach that cuts the island in two" loading="lazy">
<figcaption class="hat-caption">21 September 2003, three days after Isabel: the breach that cut Hatteras Island in two, between Frisco and Hatteras Village. Photo: U.S. Geological Survey.</figcaption>
</figure>

<div class="hat-pairs">
<figure class="hat-pair">
<div class="hat-pair-photos">
<figure><img src="{{ isabel }}frisco_1999.jpg" alt="Frisco from the air in 1999: houses behind vegetated dunes and a wide beach" loading="lazy"><figcaption>8 Sep 1999, before</figcaption></figure>
<figure><img src="{{ isabel }}frisco_2003.jpg" alt="The same houses in Frisco after Isabel: the dunes are gone and sand covers the ground between the houses" loading="lazy"><figcaption>21 Sep 2003, after</figcaption></figure>
</div>
<figcaption class="hat-caption"><b>Frisco.</b> Storm surge and waves washed over the dunes in front of the first row of houses and spread that sand across the island. The dunes were completely removed.</figcaption>
</figure>
<figure class="hat-pair">
<div class="hat-pair-photos">
<figure><img src="{{ isabel }}hatteras_village_1999.jpg" alt="Hatteras Village from the air in 1999: hotels behind a dune line, with the water tower behind them" loading="lazy"><figcaption>8 Sep 1999, before</figcaption></figure>
<figure><img src="{{ isabel }}hatteras_village_2003.jpg" alt="The same hotels in Hatteras Village after Isabel: the dunes are gone and sand covers the roads and lots" loading="lazy"><figcaption>21 Sep 2003, after</figcaption></figure>
</div>
<figcaption class="hat-caption"><b>Hatteras Village.</b> Surge and waves destroyed the dunes protecting the hotels, washed buildings from their foundations and covered roads with sand.</figcaption>
</figure>
</div>

<p class="hat-caption">Photos and descriptions: Karen L. M. Morgan, U.S. Geological Survey, <a href="https://pubs.usgs.gov/publication/fs20093025">Coastal Change During Hurricane Isabel 2003</a> (Fact Sheet 2009-3025). Public domain.</p>

### Hurricane Irene, 2011

In August 2011, Irene cut through Pea Island, opening a breach now called New Inlet. NC-12 was carried across it by a temporary bridge from October 2011, replaced by the permanent Etheridge Bridge in 2017.
You can see the breach in the "New Inlet" comparison below, and the bridges on the [management page]({{ '/hatteras/management/' | relative_url }}).

Irene cut five breaches through the island between Cape Hatteras and Oregon Inlet, severing NC-12 in several places. The U.S. Geological Survey photographed two of the breach sites before and after the storm.

{% assign irene = '/assets/hatteras/img/irene/' | relative_url %}
<figure class="hat-storm-place">
<div class="hat-storm-grid">
<figure class="hat-storm-over"><img src="{{ irene }}rodanthe_overview_2011.jpg" alt="Oblique aerial photo looking along Rodanthe after Hurricane Irene, with NC-12 broken where water cut across the island beside a line of sandbags" loading="lazy"></figure>
<div class="hat-storm-pair">
<figure><img src="{{ irene }}rodanthe_2008.jpg" alt="Rodanthe in May 2008: houses behind the road, with a wide beach in front" loading="lazy"></figure>
<figure><img src="{{ irene }}rodanthe_2011.jpg" alt="The same houses in August 2011: water has cut a channel across the island and the road" loading="lazy"></figure>
</div>
</div>
<figcaption class="hat-caption"><b>Rodanthe.</b> A breach was carved through the island here, severing NC-12. Left: looking along the coast on 30 August 2011. Right: the same spot on 6 May 2008 and 31 August 2011; the yellow arrow points to the same cottage.</figcaption>
</figure>

<figure class="hat-storm-place">
<div class="hat-storm-grid">
<figure class="hat-storm-over"><img src="{{ irene }}pea_island_overview_2011.jpg" alt="Oblique aerial photo looking north along Pea Island after Hurricane Irene, with channels cut across the island and the road" loading="lazy"></figure>
<div class="hat-storm-pair">
<figure><img src="{{ irene }}pea_island_2008.jpg" alt="Buildings and a parking area on Pea Island in May 2008, behind a wide beach" loading="lazy"></figure>
<figure><img src="{{ irene }}pea_island_2011.jpg" alt="The same buildings in August 2011, cut off by channels of water on both sides" loading="lazy"></figure>
</div>
</div>
<figcaption class="hat-caption"><b>Pea Island National Wildlife Refuge.</b> Two breaches were carved through the island here, severing NC-12. Left: looking north on 30 August 2011. Right: the same spot on 6 May 2008 and 31 August 2011; the yellow arrow points to the same building.</figcaption>
</figure>

<p class="hat-caption">Photos: Karen Morgan, U.S. Geological Survey St. Petersburg Coastal and Marine Science Center, from <a href="https://www.usgs.gov/centers/spcmsc/news/aerial-photographs-outer-banks-show-coastal-damage-hurricane-irene">Aerial Photographs of Outer Banks Show Coastal Damage from Hurricane Irene</a>. Public domain.</p>

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

- the dune line, traced separately from aerial photos, moved seaward by the same amount between 2009 and 2023;
- the jump appears in every season of imagery on its own;
- neighbouring stretches of beach agree closely, while stretches farther apart differ.

The shoreline has since drifted part of the way back. We have not yet tested what caused it; recovery after Hurricanes Dorian (2019) and Isaias (2020) is one possibility.
Because it falls near the end of the record, this one event has a large effect on any rate that includes it.

{% include hatteras/todo.liquid text="Decide how much of this to show before the paper is out. Source: 5-scr/1-observations/detrended_position/README.md." %}

## Then and now

Drag the handle across each photo to compare two years. Use the buttons to move between places, and the menus to pick any two years from 1993 to 2024.

{% include hatteras/imagery_compare.liquid %}

## Explore further

For a closer look, the [shoreline windows explorer](https://hannahaline.github.io/hatteras-shoreline-windows/) shows how the measured rate at any stretch of beach depends on which years you include.

{% include hatteras/todo.liquid text="The explorer is still private, so this link 404s until it launches. Launch both together." %}

{% include hatteras/pager.liquid %}
