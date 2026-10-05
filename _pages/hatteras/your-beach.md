---
layout: page
title: Your stretch of beach
permalink: /hatteras/your-beach/
description: Pick a village or a stretch of NC-12 for a plain summary of how its shoreline has changed, what was done there, and the storms that washed over it.
nav: false
---

{% include hatteras/subnav.liquid %}

<p class="hat-lead">
Pick a village or a stretch of NC-12 below for a short summary of that part of the island: how fast its shoreline is moving,
the beach fills, road moves and bridges there, the storms that washed over it, and how it looked from the air in 1993 and today.
</p>

{% include hatteras/stretch_picker.liquid %}

<details class="hat-deeper" markdown="1">
<summary>Go deeper: where these numbers come from</summary>

- **The stretches** follow the model's half-kilometre sections of beach, numbered from Cape Point (GIS 1) to Oregon Inlet (GIS 120). Villages are roughly their built-up shore; the boundaries between them are approximate.
- **Shoreline rates** are the average, over every survey line on the stretch, of the rate fitted to all satellite shorelines in each period (CoastSat). They include the sand that beach fills added. The [shoreline change pages]({{ '/hatteras/shoreline-change/' | relative_url }}) show every survey line.
- **Fills, road moves and bridges** are the projects in the model's management record; fill dates come from Dare County, Corps of Engineers and news reports.
- **Overwash** comes from {% include hatteras/term.liquid id="overwash" text="overwash" %} mapped by eye on aerial and satellite images from 1984 to 2024. An image shows what the island looked like on that day, so a storm's overwash can be missed if the next clear image came months later. Storm names are the named storms between the image and the one before it. The record stops just north of Rodanthe, so Pea Island is not covered.

</details>

{% include hatteras/pager.liquid %}
