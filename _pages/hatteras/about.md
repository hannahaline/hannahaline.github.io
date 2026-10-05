---
layout: page
title: About this project
permalink: /hatteras/about/
description: Who is behind this research, how it was funded, and how to get in touch.
nav: false
---

{% include hatteras/subnav.liquid %}

This site shares results from doctoral research by Hannah Henry at the University of North Carolina at Chapel Hill on how Hatteras Island has changed and how management shapes it.
It is written for the people who live on, manage, and plan for the island.

## The researcher

<div class="hat-person">
<img src="{{ '/assets/img/prof_pic.jpg' | relative_url }}" alt="Portrait of Hannah Henry" loading="lazy">
<div markdown="1">
**Hannah Henry** is a PhD Candidate in the Department of Earth, Marine, and Environmental Sciences at the University of North Carolina at Chapel Hill, working in the Coastal Environmental Change Lab with Dr. Laura Moore.
Her research combines satellite shorelines, aerial photos and the CASCADE model to study how Hatteras Island has changed and how management shapes it.

[More about Hannah]({{ '/' | relative_url }}) · [hahenry@unc.edu](mailto:hahenry@unc.edu)
</div>
</div>

Collaborators on this work are L. Moore, K. Anarde, A. B. Murray, S. Dalyander, B. Franklin and R. Sahraei.

Thanks to the National Park Service at Cape Hatteras National Seashore, the North Carolina Department of Transportation and Dare County for data and local knowledge, and to the US Army Corps of Engineers, the US Geological Survey and NOAA, whose surveys and records this work relies on.

{% include hatteras/todo.liquid text="Collaborators' full names and affiliations, from Hannah." %}

## Funding

This work is supported by a Mountains to Sea Graduate Research Fellowship from the North Carolina Water Resources Research Institute and North Carolina Sea Grant, and by NOAA and the National Science Foundation through the Long Term Ecological Research (LTER) program.

## Data sources

- **Shorelines:** CoastSat Live ([coastsat.space](https://coastsat.space)), the public dataset of shorelines traced from Landsat and Sentinel-2 satellite images with [CoastSat](https://github.com/kvos/CoastSat) (Vos and others, 2019), 1984 to January 2026.
- **Water levels:** NOAA tide gauge 8651370 at Duck, North Carolina.
- **Waves:** the US Army Corps of Engineers Wave Information Study (WIS) hindcast, station 63228.
- **Storm tracks and names:** the National Hurricane Center's best-track database (HURDAT2).
- **Aerial photos:** NC OneMap orthoimagery (NC Center for Geographic Information and Analysis, NC 911 Board), and NOAA National Geodetic Survey emergency response imagery.
- **Road, bridge and nourishment history:** compiled from NCDOT project documents, agency records and local news coverage.
- **Island elevation (the model's starting island):** airborne lidar. The US Army Corps of Engineers' 2009 survey, with gaps filled from NOAA's 2014 survey after Hurricane Sandy; for the 1996–2015 period, the beach and dunes come from the 1996 NOAA/NASA ALACE survey.
- **The model:** [CASCADE](https://github.com/UNC-CECL/CASCADE), open source.

## Publications

{% include hatteras/todo.liquid text="Link the chapters as they are published." %}

## Contact

Questions, corrections, or local knowledge about how the island has changed are welcome. Please email [hahenry@unc.edu](mailto:hahenry@unc.edu).

{% include hatteras/pager.liquid %}
