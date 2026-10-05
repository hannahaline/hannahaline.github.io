---
layout: page
title: Hatteras Island, past and present
permalink: /hatteras/
description: How Hatteras Island has changed since the 1990s, why, and how a computer model can help plan for what comes next.
nav: false
---

{% include hatteras/subnav.liquid %}

<section class="hat-hero hat-bleed" style="--hat-hero-img: url('{{ '/assets/hatteras/img/hero_banner.jpg' | relative_url }}'); --hat-hero-pos: 50% 55%">
  <div class="hat-hero-text">
    <h2>Living with a changing coast</h2>
    <p>Hatteras Island is always changing. Storms, waves, and rising seas reshape it, and so do the roads, dunes, and beach projects that keep it livable.</p>
  </div>
  <span class="hat-hero-credit">The beach below the Cape Hatteras Lighthouse, 2004. Photo: <a href="https://commons.wikimedia.org/wiki/File:Lighthouse_at_Cape_Hatteras_National_Seashore._NPS-Michael_B._Edwards_(18497979278).jpg">NPS / Michael B. Edwards</a></span>
</section>

<p class="hat-lead">
This site summarizes research on how Hatteras Island has changed over the last three decades.
It covers what satellites and aerial photos show, the natural processes behind those changes, and the ways that people manage the island.
It also introduces a computer model that recreates this history, so that management choices can be tested before they are made.
</p>

## The study area

The study area runs from Cape Point north to Oregon Inlet and includes the villages of Buxton, Avon, Salvo, Waves, and Rodanthe.
Most of the island lies within Cape Hatteras National Seashore. NC-12, the only road on and off the island, runs its full length.

<figure class="hat-studymap">
<img src="{{ '/assets/hatteras/img/study_area_map.jpg' | relative_url }}" alt="Map of Hatteras Island from Cape Point to Oregon Inlet, showing the villages of Buxton, Avon, Salvo, Waves and Rodanthe, NC-12, the beach nourishment reaches at Buxton, Avon and the Rodanthe S-curves, and the Buxton groins" loading="lazy">
<figcaption class="hat-caption">Hatteras Island from Cape Point to Oregon Inlet. Sand-coloured bands just off the beach mark the stretches nourished at Buxton (2017 and 2022), Avon (2022) and the Rodanthe S-curves (2014), and the red line marks the Buxton groins. Since 2022, NC-12 crosses Pamlico Sound on the Jug Handle Bridge; the dashed line is the beach road it replaced.</figcaption>
</figure>

## Start here: three steps

<ol class="hat-steps-path">
  <li>
    <img src="{{ '/assets/hatteras/img/isabel/overwash_nc12_2003.jpg' | relative_url }}" alt="Sand washed across NC-12 after Hurricane Isabel" loading="lazy">
    <div>
      <h3><span>1</span> The island changes</h3>
      <p>Hatteras is a barrier island. Waves carry sand along the beach and storms carry it across the island, so the shoreline keeps moving. Since 1996 it has moved landward by almost 2 m a year at Rodanthe and seaward by more than 2 m a year at Cape Point, with smaller changes in between.</p>
      <a href="{{ '/hatteras/island/' | relative_url }}">How the island works</a> · <a href="{{ '/hatteras/shoreline-change/' | relative_url }}">Shoreline change</a>
    </div>
  </li>
  <li>
    <img src="{{ '/assets/hatteras/img/dunes/scurves_dune_2011.jpg' | relative_url }}" alt="A tall dune newly built in front of NC-12 at the S-curves in 2011" loading="lazy">
    <div>
      <h3><span>2</span> People manage it</h3>
      <p>Since the 1930s, people have built and rebuilt dunes, added sand to beaches, moved NC-12 and built bridges, mostly to keep the road open and protect homes. These choices also change how sand moves on the island, which affects how it responds to later storms.</p>
      <a href="{{ '/hatteras/management/' | relative_url }}">How management shapes the island</a>
    </div>
  </li>
  <li>
    <img src="{{ '/assets/hatteras/img/model_steps/step1.png' | relative_url }}" alt="One stretch of the island as an aerial photo and as the model's grid of heights" loading="lazy">
    <div>
      <h3><span>3</span> A model compares options</h3>
      <p>CASCADE is a computer model of the island and its management. It is checked against what actually happened since 1996, and the site shows where it matches and where it does not. A model that passes that check can be used to compare options for the future; it does not choose between them.</p>
      <a href="{{ '/hatteras/model/' | relative_url }}">The model</a>
    </div>
  </li>
</ol>

<p class="hat-start-own">Live on the island or look after part of it? <a href="{{ '/hatteras/your-beach/' | relative_url }}">See the summary for your stretch of beach</a>.</p>

<div class="hat-keypoint">
<b>Why a model?</b> If a model can reproduce how the island actually changed, including the effects of {% include hatteras/term.liquid id="beach-nourishment" text="beach nourishment" %}, dune building, and moving the road, then it can be used to ask "what if" questions about the future with more confidence.
</div>

## Explore

<div class="hat-cards">
  <a class="hat-card" href="{{ '/hatteras/your-beach/' | relative_url }}">
    <h3>Your stretch of beach</h3>
    <p>Pick a village or a stretch of NC-12 for a short summary: shoreline change, fills, road moves and storms there.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/island/' | relative_url }}">
    <h3>How the island works</h3>
    <p>How barrier islands work: waves, storms, overwash, and sea-level rise.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/shoreline-change/' | relative_url }}">
    <h3>Shoreline change</h3>
    <p>Where the beach has retreated or grown since 1996, measured from satellite images: on a map, as one chart along the island, and as the shoreline every ten years since the 1980s.</p>
  </a>
  <a class="hat-card" href="{{ '/hatteras/storms/' | relative_url }}">
    <h3>Storms</h3>
    <p>The named storms that raised the water highest since 1984, and what Isabel, Irene and Dorian did to the island.</p>
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

{% include hatteras/pager.liquid %}
