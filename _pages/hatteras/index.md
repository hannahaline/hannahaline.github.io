---
layout: page
title: Hatteras Island, past and present
permalink: /hatteras/
description: How Hatteras Island has changed since the 1990s, why, and how a computer model can help plan for what comes next.
nav: false
---

{% include hatteras/subnav.liquid %}

<section class="hat-hero hat-bleed" style="--hat-hero-img: url('{{ '/assets/img/photos/hatteras-aerial.jpg' | relative_url }}')">
  <div class="hat-hero-text">
    <h2>Living with a changing coast</h2>
    <p>Hatteras Island is always changing. Storms, waves, and rising seas reshape it, and so do the roads, dunes, and beach projects that keep it livable.</p>
  </div>
</section>

<p class="hat-lead">
This site shares what my research has learned about how Hatteras Island has changed over the last three decades.
It covers what satellites and aerial photos show, the natural processes behind those changes, and the ways that people manage the island.
It also introduces a computer model that recreates this history, so that we can test management choices before making them.
</p>

<div class="hat-keypoint">
<b>Why a model?</b> If a model can reproduce how the island actually changed, including the effects of {% include hatteras/term.liquid id="beach-nourishment" text="beach nourishment" %}, dune building, and moving the road, then we can use it to ask "what if" questions about the future with more confidence.
</div>

<figure class="hat-photo-wide">
<img src="{{ '/assets/hatteras/img/buxton_houses_2025.jpg' | relative_url }}" alt="Oceanfront houses on pilings standing in the surf at Buxton, one collapsed into the water, with debris on the wet sand" loading="lazy">
<figcaption class="hat-caption">Houses in the surf at Buxton on 30 September 2025, the day five unoccupied houses there collapsed. Photo: <a href="https://www.nps.gov/caha/learn/news/five-unoccupied-houses-collapse-in-buxton-september-30-2025.htm">National Park Service</a>.</figcaption>
</figure>

{% include hatteras/todo.liquid text="Swap the hero photo for a Hatteras-specific aerial (Rodanthe S-curves or Buxton) once imagery sources are settled." %}

## Explore

<div class="hat-cards">
  <a class="hat-card" href="{{ '/hatteras/island/' | relative_url }}">
    <h3>How the island works</h3>
    <p>How barrier islands work: waves, storms, overwash, and sea-level rise.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/shoreline-change/' | relative_url }}">
    <h3>Shoreline change</h3>
    <p>Where the beach has retreated or grown since 1996, measured from satellite images.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/storms/' | relative_url }}">
    <h3>Storms</h3>
    <p>Every high-water event since 1984, and what Isabel, Irene and Dorian did to the island.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/then-and-now/' | relative_url }}">
    <h3>Then and now</h3>
    <p>Aerial photos from 1993 to 2024, side by side at four places on the island.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/management/' | relative_url }}">
    <h3>Management</h3>
    <p>Beach nourishment, NC-12, dune building, and groins: how each one shapes the island.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/model/' | relative_url }}">
    <h3>The model</h3>
    <p>How CASCADE works in plain language, and how well it recreates the past.</p>
  </a>
</div>

## The study area

The research covers Hatteras Island from Cape Point north to Oregon Inlet, including the villages of Buxton, Avon, Salvo, Waves, and Rodanthe.
Most of the island lies within Cape Hatteras National Seashore. NC-12, the only road on and off the island, runs its full length.

<figure class="hat-studymap">
<img src="{{ '/assets/hatteras/img/study_area_map.jpg' | relative_url }}" alt="Map of Hatteras Island from Cape Point to Oregon Inlet, showing the villages of Buxton, Avon, Salvo, Waves and Rodanthe, NC-12, the beach nourishment reaches at Buxton, Avon and the Rodanthe S-curves, and the Buxton groins" loading="lazy">
<figcaption class="hat-caption">Hatteras Island from Cape Point to Oregon Inlet. Sand-coloured bands just off the beach mark the stretches nourished at Buxton (2017 and 2022), Avon (2022) and the Rodanthe S-curves (2014), and the red line marks the Buxton groins. Since 2022, NC-12 crosses Pamlico Sound on the Jug Handle Bridge; the dashed line is the beach road it replaced.</figcaption>
</figure>


{% include hatteras/pager.liquid %}
