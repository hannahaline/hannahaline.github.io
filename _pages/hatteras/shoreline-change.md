---
layout: page
title: Historic shoreline change
permalink: /hatteras/shoreline-change/
description: Where Hatteras Island's shoreline has retreated or grown since 1996, and the events that show up in the record.
nav: false
---

{% include hatteras/subnav.liquid %}
{% include hatteras/shoreline_tabs.liquid %}

<p class="hat-lead">
Satellites have photographed Hatteras Island many times a year since the 1980s.
By tracing the {% include hatteras/term.liquid id="shoreline" text="shoreline" %} in each image, we can see where the beach has moved landward, where it has grown, and when the big changes happened.
</p>

## Three ways to look at the record

<div class="hat-cards">
  <a class="hat-card" href="{{ '/hatteras/shoreline-change/survey-lines/' | relative_url }}">
    <h3>Survey lines</h3>
    <p>A map of every survey line across the beach, coloured by how fast the shoreline there has moved. Click a line to see its whole record, or press play to watch the shoreline year by year.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/shoreline-change/along-the-island/' | relative_url }}">
    <h3>Along the island</h3>
    <p>The same measurements as one chart, from Cape Point north to Oregon Inlet, so the patterns between villages are easy to compare.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/shoreline-change/through-time/' | relative_url }}">
    <h3>Shorelines through time</h3>
    <p>The average shoreline every ten years since the 1980s, drawn over aerial photos from 1993 to 2024.</p>
  </a>
</div>

## What the record shows


Over the whole satellite record, the island as a whole has held roughly steady: about half of the beach has moved landward and half seaward.
That average hides large differences from place to place.

- **Cape Point** has grown seaward faster than anywhere else, by about 2.4 m per year on average (roughly 24 m per decade).
- **Buxton** lost ground through the 1990s and 2000s, about 1.4 m per year from 1996 to 2015. Since then, {% include hatteras/term.liquid id="beach-nourishment" text="beach nourishment" %} in 2017 and 2022 has added sand, and the record shows growth.
- **Avon** sits on a shoreline that swings between eroding and growing stretches a few kilometres apart. Its nourished stretch jumped seaward after the 2022 fill.
- **The long stretch between Avon and Salvo** has changed least, staying within a metre per year of no change along about three-quarters of its length.
- **Salvo, Waves and Rodanthe** have moved landward on average, about 0.5 m per year over the whole record, with local hot spots of 2 to 3 m per year.
- **Pea Island** has the most persistent erosion: about 0.9 m per year over the whole record, and faster since 2010.

Rates that include the last few years are pushed seaward by an island-wide shift in 2021 (described below). That is why the 2010–2026 view shows more growth than the earlier period.

<details class="hat-deeper" markdown="1">
<summary>Go deeper: how shoreline change is measured</summary>

Shoreline positions come from CoastSat Live ([coastsat.space](https://coastsat.space)), a public dataset made with [CoastSat](https://github.com/kvos/CoastSat), an open-source toolkit that finds the water's edge in Landsat and Sentinel-2 satellite images. Each position is corrected for the tide, using a beach slope estimated at each transect.
Positions are measured along {% include hatteras/term.liquid id="transect" text="transects" %}, shore-normal lines spaced every 50 m along the island.
The rate at each transect is the slope of a straight-line fit through every position in the period (a *linear regression rate*), reported in metres per year.
Negative rates mean {% include hatteras/term.liquid id="erosion" text="erosion" %}, and positive rates mean {% include hatteras/term.liquid id="accretion" text="accretion" %}.
A rate is shown as "no clear trend" when it is smaller than its 95% uncertainty.
The smoothed line on the chart is a LOWESS fit over about 3.5 km (seven 500 m model domains). Near Cape Point (the first 5 km) it is replaced by the average of each 500 m stretch, because the shoreline there changes too sharply to smooth.
Periods run from 1 January of the first year to 31 December of the last.

</details>
## Events that stand out

The shoreline does not change smoothly. Storms take sand away in days, and nourishment projects add it back in weeks.
The big storms have [their own page]({{ '/hatteras/storms/' | relative_url }}); two other events stand out in the satellite record.

### Beach nourishment, 2014 to 2022

Beach nourishment shows up in the satellite record as a sudden seaward jump in the year after the sand is placed, on that stretch of beach only.
Compared with the rest of the island, the shoreline jumped about 15 m at Rodanthe after the 2014 fill, 33 m at Buxton after the 2017 fill, 11 m at Avon after 2022, and 8 m at Buxton after 2022.
The Buxton 2022 jump is smallest; that project placed less than half as much sand per metre of beach as the 2017 one.

The added width does not last equally everywhere.
At Rodanthe it held for about three years and had worn away by 2021–22. The shoreline there then moved seaward again, to about 13 m ahead of the rest of the island by 2025.
At Buxton, about 40% of the 2017 jump was gone within a year, and the rest held until the 2022 fill added to it.
Avon still had about three-quarters of its 2022 jump in 2025, while the smaller Buxton 2022 jump had mostly disappeared.
The [nourishment explorer]({{ '/hatteras/management/' | relative_url }}#beach-nourishment) on the Management page shows each stretch year by year.
Click a nourished stretch on the [survey-line map]({{ '/hatteras/shoreline-change/survey-lines/' | relative_url }}) to see its jump, marked in gold, in the full record.

### The 2021 shift

Between 2020 and 2021, the shoreline moved seaward by about 17 m almost everywhere on the island, in a single year.
We are writing up what this shift was, and will share it here once it is published.
Because it falls near the end of the record, this one event has a large effect on any rate that includes it, so it is worth keeping in mind when reading the 2010–2026 rates and the year-by-year views.

## Explore further

For a closer look, the [shoreline windows explorer](https://hannahaline.github.io/hatteras-shoreline-windows/) shows how the measured rate at any stretch of beach depends on which years you include.

{% include hatteras/todo.liquid text="The explorer is still private, so this link 404s until it launches. Launch both together." %}

{% include hatteras/pager.liquid %}
