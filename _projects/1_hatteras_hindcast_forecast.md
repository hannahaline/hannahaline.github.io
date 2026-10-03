---
layout: page
title: Hindcasting and forecasting Hatteras Island
description: Chapter 1 — can CASCADE reproduce three decades of change on Hatteras, and where is the island headed?
img: assets/img/research/hatteras_card.jpg
importance: 1
category: current research
---

<div class="glance">
  <h4>At a glance</h4>
  <dl>
    <dt>Question</dt>
    <dd>How well can a model that couples natural processes with human management reproduce how Hatteras Island has changed since the 1990s, and how will the island evolve under different future climate and management choices?</dd>
    <dt>Where</dt>
    <dd>Hatteras Island, North Carolina: a 45 km reach from Cape Point to Pea Island, including the villages of Buxton, Avon, Salvo, Waves, and Rodanthe</dd>
    <dt>Approach</dt>
    <dd>The CASCADE model (Barrier3D, BRIE, and human-management modules), hindcast over 1996–2010 and 2010–2024 against satellite-derived shorelines, then run forward under climate and management scenarios</dd>
    <dt>Data</dt>
    <dd>LiDAR elevation surveys, CoastSat shorelines, digitized dune lines, storm records, and the history of beach nourishment, dune building, and NC-12 relocation</dd>
    <dt>Collaborators</dt>
    <dd>L. Moore, K. Anarde, A. B. Murray, S. Dalyander, B. Franklin, R. Sahraei</dd>
    <dt>Status</dt>
    <dd>Hindcasts under way; forecasts next</dd>
  </dl>
</div>

Barrier islands are dynamic coastal landscapes shaped by the interplay of storms, sea-level rise, sediment transport, and human intervention. On Hatteras Island, decades of beach nourishment, dune construction, and road relocation have been layered on top of those natural processes, and decisions about NC-12 and the island's villages are being made right now.

In this chapter, I use the CoAStal Community-lAnDscape Evolution (CASCADE) model to ask whether we can reproduce the island's recent past before forecasting its future. CASCADE couples Barrier3D, which simulates dune dynamics, overwash, and shoreface change across the island, with the BarrieR Inlet Environment (BRIE) model, which moves the shoreline alongshore, and adds modules for human responses such as beach nourishment, dune construction, and road relocation. I first **hindcast** the island from 1996 to 2024, comparing the model's shoreline change with satellite-derived shorelines, and then **forecast** how the island might evolve under different rates of sea-level rise and management strategies.

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/research/hatteras_study_area.jpg" alt="Study area map of Hatteras Island: the 90 model domains along the island from Cape Point to Pea Island on aerial imagery, with NC-12, the villages, and the Buxton groin field" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="caption">
  The modelled reach of Hatteras Island, rotated so it runs south to north from left to right (north arrow, top): 90 model domains, each 500 m alongshore, from Cape Point to the southern end of Pea Island, with NC-12, the villages, and the Buxton groins. Inset: Hatteras Island on the North Carolina coast. Basemap: Esri World Imagery.
</div>

A key part of this work is building realistic, site-specific inputs: I process LiDAR-derived elevation data, digitize historical dune lines, derive shoreline change from satellite imagery, and develop the island's planform, storm, sea-level, and management time series in Python and GIS.

### Approach

1. **Build Hatteras in the model.** Island topography from LiDAR, digitized dune lines, the island's planform, storms, sea level, and the history of beach nourishment, dune building, and NC-12 relocation.
2. **Hindcast the recent past.** Run the model over 1996–2010 and 2010–2024 and compare its shoreline change with satellite-derived shorelines from CoastSat.
3. **Forecast the future.** Run the calibrated model forward under different rates of sea-level rise and management strategies to explore what lies ahead for NC-12 and the island's villages.

### Presentations

- Ocean Sciences Meeting 2026, Glasgow, United Kingdom (poster)
- XV Simpósio Nacional de Geomorfologia (SINAGEO) 2025, Natal, Brazil (talk)
- Community Surface Dynamics Modeling System Meeting 2025, Boulder, Colorado (poster)
- Earth, Marine, and Environmental Sciences Research Symposium 2026, UNC Chapel Hill (poster)

See all [talks and posters](/talks/).

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/photos/barrier-island-aerial.jpg" alt="Aerial view of a developed barrier island" class="img-fluid rounded z-depth-1 strip-img" %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/photos/dune-scarp.jpg" alt="Hannah beside an eroded dune scarp" class="img-fluid rounded z-depth-1 strip-img" %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/photos/cape-lookout-shoal.jpg" alt="Hannah on a wide, open sand flat" class="img-fluid rounded z-depth-1 strip-img" %}
  </div>
</div>

This research is conducted under the mentorship of Dr. Laura Moore at UNC–Chapel Hill and is supported by NOAA, the NSF through the LTER program, and a Mountains to Sea Graduate Research Fellowship from the NC Water Resources Research Institute and North Carolina Sea Grant.
