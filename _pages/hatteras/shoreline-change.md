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

{% include hatteras/todo.liquid text="Two or three plain-language sentences per village (Rodanthe, Avon, Buxton, Pea Island) once the map is in. Keep numbers in metres per year AND 'about the length of a ... per decade'." %}

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

{% include hatteras/panel.liquid id="events-timeline" title="Storms and management, 1996–2024" plan="Timeline of the major storms (HURDAT2 tropical cyclones and nor'easters, coloured as in the storm figures) alongside the nourishments, NC-12 relocations, and bridge openings. Hovering an event highlights the reach it affected on the map above." %}

### Hurricane Isabel, 2003

{% include hatteras/todo.liquid text="Isabel cut a new inlet near Hatteras Village. Describe what the shoreline record shows, and pair it with a before/after image." %}

### Hurricane Irene, 2011

{% include hatteras/todo.liquid text="Irene breached the island at Pea Island and near Rodanthe. Describe what the record shows, and link to the management page for the bridges that followed." %}

### Beach nourishment, 2014 and 2022

{% include hatteras/todo.liquid text="How the Buxton, Rodanthe, and Avon fills show up as sudden seaward jumps, and how long the added width lasts." %}

### The 2021 shift

{% include hatteras/todo.liquid text="Explain the island-wide seaward jump of the satellite shoreline around 2021, which the dune line confirms is real, in plain language. Decide how much to say before the paper is out." %}

## Then and now

Drag the handle across each photo to compare two years. Use the buttons to move between places, and the menus to pick any two years from 1993 to 2024.

{% include hatteras/imagery_compare.liquid %}

## Explore further

For a closer look, the [shoreline windows explorer](https://hannahaline.github.io/hatteras-shoreline-windows/) shows how the measured rate at any stretch of beach depends on which years you include.

{% include hatteras/todo.liquid text="The explorer is still private, so this link 404s until it launches. Launch both together." %}

{% include hatteras/pager.liquid %}
