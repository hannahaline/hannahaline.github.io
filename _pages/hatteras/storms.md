---
layout: page
title: Storms
permalink: /hatteras/storms/
description: The named storms that raised the water highest at Hatteras since 1984, and what the biggest did to the beach.
nav: false
---

{% include hatteras/subnav.liquid %}

<p class="hat-lead">
A big storm can reshape the beach in a few days.
This page ranks the named storms that raised the water highest at Hatteras since 1984, then looks closely at three hurricanes.
</p>

## The biggest named storms since 1984

Each bar is one named storm, ranked by how high the water reached at the shore, as tide, {% include hatteras/term.liquid id="storm-surge" text="storm surge" %} and waves together pushed it up the beach.
The colour shows the storm's category when it was closest to Hatteras.
Category alone does not decide how high the water gets: Dorian passed almost overhead as a Category 2 and raised the water less than Sandy, a Category 1 some 400 km offshore, because a storm's size, track and how long it lingers matter as much as its winds.
Nor'easters matter too: the strongest, in March 2018, pushed the water higher than every hurricane except Isabel.

<figure class="hat-photo-wide" style="max-width: 50rem; margin-left: auto; margin-right: auto;">
<img src="{{ '/assets/hatteras/img/named_storms.png' | relative_url }}" alt="Bar chart of the 15 named storms that raised the water highest at Hatteras since 1984, coloured by category when closest. Isabel 2003 is highest at 5.2 m, then the 1991 Perfect Storm at 4.6 m, Earl, Irene, Sandy, Erin and Florence near 3.6 to 3.8 m; Dorian, which passed almost overhead, reached 3.0 m. A dashed line marks the highest nor'easter, March 2018, at 4.3 m" loading="lazy">
<figcaption class="hat-caption">The 15 named storms that raised the water highest at the shore since 1984, with each storm's category and distance when it was closest to Cape Hatteras, and the highest nor'easter for comparison. Water level: peak tide, surge and wave run-up at the shore, estimated from the Duck tide gauge and the WIS wave hindcast, in metres above mean high water. The hatched bar (Erin, 2025) is an estimate placed after the wave record ends. Categories and tracks: National Hurricane Center best-track database (HURDAT2). The 1991 "Perfect Storm" was an unnamed subtropical storm.</figcaption>
</figure>

## Where storms can get over the dunes

How much a storm does depends on where its water meets a low spot in the dunes.
The chart shows the lowest point of the dunes on each 500 m stretch of the island, against the water levels of three storms.
Where a bar falls below a line, that storm's water could wash over there: Isabel could reach over the low point of almost every stretch, and even a large nor'easter reaches the low spots around Rodanthe and between Avon and Salvo.

<figure class="hat-photo-wide" style="max-width: 50rem; margin-left: auto; margin-right: auto;">
<img src="{{ '/assets/hatteras/img/model_steps/step3.png' | relative_url }}" alt="Chart of the lowest dune top on each 500 m stretch from Cape Point to just north of Rodanthe, with lines for the water levels of Isabel (5.2 m), Irene and Earl (3.8 m) and a large nor'easter (3.0 m); many stretches dip below the lines, most of all around Rodanthe and between Avon and Salvo" loading="lazy">
<figcaption class="hat-caption">The lowest dune top on each 500 m stretch, as the model's 1996–2015 run starts (beach and dunes from the 1996 NOAA/NASA lidar survey), against the peak water levels of three storms, in metres above mean high water. Dunes are worn down while a storm goes on, so water gets over in more places than this shows. The same chart appears in the walk-through on <a href="{{ '/hatteras/model/' | relative_url }}">the model page</a>.</figcaption>
</figure>

The beach projects and road moves of the same years are on the [management page]({{ '/hatteras/management/' | relative_url }}).

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
You can see the breach in the [New Inlet comparison]({{ '/hatteras/then-and-now/#spot=newinlet' | relative_url }}), and the bridges on the [NC-12 page]({{ '/hatteras/management/nc-12/' | relative_url }}).

Irene cut five breaches through the island between Cape Hatteras and Oregon Inlet, severing NC-12 in several places. The U.S. Geological Survey photographed two of the breach sites before and after the storm.

{% assign irene = '/assets/hatteras/img/irene/' | relative_url %}
<figure class="hat-storm-place">
<div class="hat-storm-grid">
<figure class="hat-storm-over"><img src="{{ irene }}rodanthe_overview_2011.jpg" alt="Oblique aerial photo looking along Rodanthe after Hurricane Irene, with NC-12 broken where water cut across the island beside a line of sandbags" loading="lazy"></figure>
<div class="hat-storm-pair">
<figure><img src="{{ irene }}rodanthe_2008.jpg" alt="Rodanthe in May 2008: houses behind the road, with a wide beach in front" loading="lazy"></figure>
<figure><img src="{{ irene }}rodanthe_2011.jpg" alt="The same houses in August 2011: water has cut a channel across the island and the road" loading="lazy"></figure>
</div>
</div>
<figcaption class="hat-caption"><b>Rodanthe.</b> A breach was carved through the island here, severing NC-12. Left: looking along the coast on 30 August 2011. Right: the same spot on 6 May 2008 and 31 August 2011; the yellow arrow points to the same cottage.</figcaption>
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
NOAA photographed the island from the air the next day. A comparison of those photos with ones from 2016 shows no fresh sheets of washed-over sand across NC-12 anywhere between Buxton and Oregon Inlet.
You can look for yourself: the 7 September 2019 photo is one of the years in [Then and now]({{ '/hatteras/then-and-now/' | relative_url }}).

High water on its own does not decide what a storm does to the island. The height of the dunes, the width of the beach and how long the water stays high all matter too, and these are what the model weighs storm by storm.

{% comment %} Sources: landfall time and place from HURDAT2 (AL052019, 6 Sep 12:30 UTC, 35.2N 75.6W). Water level and hours above the berm from storm_record_1996_2024_labelled_events.csv (Dorian 3.022 m MHW, 31 h; Isabel 100 h). "No fresh overwash" from the 2016 vs 2019 photo check on 2026-10-03 (NC-12 sampled every 2 km plus eight close-ups) and the overwash record (OBS-024: no overwash on the modelled island). Category from HURDAT2 (85 kt at landfall = Category 2 on the Saffir-Simpson scale); the CASCADE match table still says Category 1. {% endcomment %}

{% include hatteras/pager.liquid %}
