---
layout: page
title: Storms
permalink: /hatteras/storms/
description: Every high-water event on Hatteras Island since 1984, and what the biggest storms did to the beach.
nav: false
---

{% include hatteras/subnav.liquid %}

<p class="hat-lead">
A big storm can reshape the beach in a few days.
This page shows every {% include hatteras/term.liquid id="high-water-event" text="high-water event" %} since 1984, then looks closely at three hurricanes.
</p>

## Every high-water event since 1984

Each dot is one high-water event: a time when tide, {% include hatteras/term.liquid id="storm-surge" text="storm surge" %} and waves together pushed water high up the beach. The taller the stem, the higher the water reached.
The beach projects and road moves of the same years are on the [management page]({{ '/hatteras/management/' | relative_url }}).

{% include hatteras/timeline.liquid mode="storms" %}

## Hurricane Isabel, 2003

Isabel brought the highest water of the whole record: an estimated 5.2 m above {% include hatteras/term.liquid id="mean-high-water" text="mean high water" %} at the shore in September 2003, almost a metre higher than any storm since.
There are no map-ready aerial photos from just after Isabel, so the [Then and now]({{ '/hatteras/then-and-now/' | relative_url }}) comparison jumps from 2002 to 2007. {% include hatteras/term.liquid id="oblique-photo" text="Oblique photos" %} taken from a plane fill that gap.

The worst damage was just south-west of Cape Point, beyond the stretch this research models. There, Isabel cut a new {% include hatteras/term.liquid id="breach" text="breach" %} about 500 m wide that completely severed the island, and it {% include hatteras/term.liquid id="overwash" text="overwashed" %} the villages of Frisco and Hatteras Village.
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

## Hurricane Irene, 2011

In August 2011, Irene cut through Pea Island, opening a breach now called New Inlet. NC-12 was carried across it by a temporary bridge from October 2011, replaced by the permanent Etheridge Bridge in 2017.
You can see the breach in the [New Inlet comparison]({{ '/hatteras/then-and-now/#spot=newinlet' | relative_url }}), and the bridges on the [management page]({{ '/hatteras/management/' | relative_url }}).

Irene cut five breaches through the island between Cape Hatteras and Oregon Inlet, severing NC-12 in several places. The U.S. Geological Survey photographed two of the breach sites before and after the storm.

{% assign irene = '/assets/hatteras/img/irene/' | relative_url %}
<figure class="hat-storm-place">
{% include hatteras/photo_slider.liquid before="/assets/hatteras/img/irene/rodanthe_before_aligned.jpg" after="/assets/hatteras/img/irene/rodanthe_after_aligned.jpg" before_label="6 May 2008" after_label="31 Aug 2011" before_alt="Rodanthe in May 2008: houses behind NC-12, with a wide beach in front" after_alt="The same houses in August 2011: water has cut a channel across the island and the road" ratio="857 / 464" %}
<figure class="hat-photo-narrow"><img src="{{ irene }}rodanthe_overview_2011.jpg" alt="Oblique aerial photo looking along Rodanthe after Hurricane Irene, with NC-12 broken where water cut across the island beside a line of sandbags" loading="lazy"></figure>
<figcaption class="hat-caption"><b>Rodanthe.</b> A breach was carved through the island here, severing NC-12. Drag the slider to compare the same spot on 6 May 2008 and 31 August 2011; the yellow arrow points to the same cottage. The 2008 photo has been warped to line up with the 2011 one, so houses on pilings may sit slightly off. Below: looking along the coast on 30 August 2011.</figcaption>
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

## Hurricane Dorian, 2019

Dorian made landfall at Cape Hatteras as a Category 2 hurricane on the morning of 6 September 2019.
At the shore, water reached an estimated 3.0 m above mean high water and stayed above the top of the beach for about 31 hours. Isabel's water stayed that high for about 100 hours.

Even so, the ocean side of the island came through largely intact.
NOAA photographed the island from the air the next day. Comparing those photos with ones from 2016, we found no fresh sheets of washed-over sand across NC-12 anywhere between Buxton and Oregon Inlet.
You can look for yourself: the 7 September 2019 photo is one of the years in [Then and now]({{ '/hatteras/then-and-now/' | relative_url }}).

High water on its own does not decide what a storm does to the island. The height of the dunes, the width of the beach and how long the water stays high all matter too, and these are what the model weighs storm by storm.

{% comment %} Sources: landfall time and place from HURDAT2 (AL052019, 6 Sep 12:30 UTC, 35.2N 75.6W). Water level and hours above the berm from storm_record_1996_2024_labelled_events.csv (Dorian 3.022 m MHW, 31 h; Isabel 100 h). "No fresh overwash" from the 2016 vs 2019 photo check on 2026-10-03 (NC-12 sampled every 2 km plus eight close-ups) and the overwash record (OBS-024: no overwash on the modelled island). Category from HURDAT2 (85 kt at landfall = Category 2 on the Saffir-Simpson scale); the CASCADE match table still says Category 1. {% endcomment %}

{% include hatteras/pager.liquid %}
