---
layout: page
title: Historic shoreline change
permalink: /hatteras/shoreline-change/
description: Where Hatteras Island's shoreline has retreated or grown since 1996, and the events that show up in the record.
nav: false
map: true
---

{% include hatteras/subnav.liquid %}

<p class="hat-lead">
Satellites have photographed Hatteras Island many times a year since the 1980s.
By tracing the shoreline in each image, we can see where the beach has moved landward, where it has grown, and when the big changes happened.
</p>

## Where is the shoreline eroding or growing?

{% include hatteras/panel.liquid id="shoreline-map" wide=true title="Shoreline change along Hatteras Island, 1996–2024" plan="Leaflet map of the island coloured by rate of change (RdBu: red is erosion, blue is growth), with village labels and NC-12. Clicking a stretch of beach opens its shoreline position through time. Data: CoastSat LRR 1996–2024 by transect, LOWESS 7-domain smoothing, exported to assets/hatteras/data/." %}

{% include hatteras/todo.liquid text="Two or three plain-language sentences per village (Rodanthe, Avon, Buxton, Pea Island) once the map is in. Keep numbers in metres per year AND 'about the length of a ... per decade'." %}

<details class="hat-deeper" markdown="1">
<summary>Go deeper: how shoreline change is measured</summary>

Shoreline positions come from [CoastSat](https://github.com/kvos/CoastSat), an open-source toolkit that finds the water's edge in Landsat and Sentinel-2 satellite images and corrects it for the tide.
Positions are measured along transects, shore-normal lines spaced every 100 m along the island.
The rate at each transect is the slope of a straight-line fit through every position in the period (a *linear regression rate*), reported in metres per year.
Negative rates mean erosion, and positive rates mean accretion.

{% include hatteras/todo.liquid text="Confirm the transect spacing and the tide/slope correction settings against the CoastSat run, and add the uncertainty in plain words." %}

</details>

## Events in the record

The shoreline does not change smoothly. Storms take sand away in days, and nourishment projects add it back in weeks.
These events stand out in the record.

{% include hatteras/panel.liquid id="events-timeline" title="Storms and management, 1996–2024" plan="Timeline of the major storms (HURDAT2 tropical cyclones and nor'easters, coloured as in the storm figures) alongside the nourishments, NC-12 relocations, and bridge openings. Hovering an event highlights the reach it affected on the map above." %}

### Hurricane Isabel, 2003

{% include hatteras/todo.liquid text="Isabel cut a new inlet near Hatteras Village. Describe what the shoreline record shows, and pair it with a before/after image." %}

### Hurricane Irene, 2011

{% include hatteras/todo.liquid text="Irene breached the island at Pea Island and near Rodanthe. Describe what the record shows, and link to the management page for the bridges that followed." %}

### Beach nourishment, 2017–2022

{% include hatteras/todo.liquid text="How the Buxton, Rodanthe, and Avon fills show up as sudden seaward jumps, and how long the added width lasts." %}

### The 2021 shift

{% include hatteras/todo.liquid text="Explain the island-wide seaward jump of the satellite shoreline around 2021, which the dune line confirms is real, in plain language. Decide how much to say before the paper is out." %}

## Then and now

{% include hatteras/panel.liquid id="imagery-compare" wide=true title="Aerial photos, then and now" plan="Swipe slider comparing historic and recent aerial imagery at four spots: the Rodanthe S-curves, Avon, Buxton near the old lighthouse site, and Hatteras Village / Isabel Inlet. Sources pending the online imagery search; the D: drive USGS frames are the fallback." %}

## Explore further

For a closer look, the [shoreline windows explorer](https://hannahaline.github.io/hatteras-shoreline-windows/) shows how the measured rate at any stretch of beach depends on which years you include.

{% include hatteras/todo.liquid text="The explorer is still private, so this link 404s until it launches. Launch both together." %}

{% include hatteras/pager.liquid %}
