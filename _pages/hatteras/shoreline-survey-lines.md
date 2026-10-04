---
layout: page
title: "Shoreline change: survey lines"
permalink: /hatteras/shoreline-change/survey-lines/
section: /hatteras/shoreline-change/
description: A map of shoreline change rates on every survey line across the beach of Hatteras Island, with each spot's satellite record.
nav: false
map: true
chart:
  chartjs: true
---

{% include hatteras/subnav.liquid %}
{% include hatteras/shoreline_tabs.liquid %}

<p class="hat-lead">
Each coloured line on the map is a survey line across the beach ({% include hatteras/term.liquid id="transect" text="transect" %}), every 50 m from Cape Point to Oregon Inlet.
Red lines show where the shoreline has moved landward, and blue lines show where it has moved seaward.
</p>

Use the buttons to compare the whole satellite record with the two periods the model recreates.
Click any line to see every satellite shoreline at that spot since the 1980s.
Or switch to **Change year by year** and press play to watch where the shoreline sat each year.

{% include hatteras/shoreline_map.liquid part="map" %}

{% include hatteras/pager.liquid %}
