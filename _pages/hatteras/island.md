---
layout: page
title: How a barrier island works
permalink: /hatteras/island/
description: The natural processes that move sand on, off, and along Hatteras Island.
nav: false
---

{% include hatteras/subnav.liquid %}

<p class="hat-lead">
Barrier islands are long, narrow strips of sand between the ocean and a {% include hatteras/term.liquid id="sound" text="sound" %}.
They are not fixed in place. Over decades to centuries, waves, storms, and rising seas move their sand, and the island slowly shifts.
</p>

<figure class="hat-xsection-wrap">
{% include hatteras/cross_section.svg %}
<figcaption class="hat-caption">A slice across Hatteras Island, from Pamlico Sound to the Atlantic. NC-12 runs just behind the dune along much of the island, and the villages sit on the island interior.</figcaption>
</figure>

## Waves move sand along the coast

Waves rarely hit the beach head-on. When they arrive at an angle, they push sand along the shore in a slow, steady current called *longshore transport*.
Where more sand arrives than leaves, the beach grows. Where more leaves than arrives, it erodes.

{% assign ls = '/assets/hatteras/img/longshore/' | relative_url %}
<div class="hat-pairs">
<figure class="hat-pair">
<div class="hat-pair-photos">
<figure><img src="{{ ls }}dye_release_2010.jpg" alt="Aerial photo of the surf off Cape Hatteras with bright green dye in the water, stretched out along the beach inside the breaking waves; a truck is parked on the beach" loading="lazy"><figcaption>(a) Dye in the surf</figcaption></figure>
<figure><img src="{{ ls }}cape_point.jpg" alt="Aerial photo of Cape Point: a long hook of sand curving out into the ocean, with waves bending around its tip" loading="lazy"><figcaption>(b) Cape Point</figcaption></figure>
</div>
<figcaption class="hat-caption">(a) Green dye poured into the surf off Cape Hatteras during a 2010 USGS study shows how the water moves: the current inside the breaking waves stretches it out along the beach, and that same current carries sand. (b) Cape Point, where the sand carried south along the island's east-facing shore meets waves wrapping around the point from the south and piles up into a growing hook of beach. Photos: Dann Blackwood and Don Bowers (a) and Dann Blackwood (b), U.S. Geological Survey, from <a href="https://www.usgs.gov/geology-and-ecology-of-national-parks/geology-cape-hatteras-national-seashore">Geology of Cape Hatteras National Seashore</a>. Public domain.</figcaption>
</figure>
</div>

<details class="hat-deeper" markdown="1">
<summary>Go deeper: wave angle and shoreline shape</summary>

The shape of the coast is itself set by the waves. Along the Outer Banks, large waves arrive from both the northeast and the southeast.
When waves come in at a steep angle to the shore, small bumps in the coastline tend to grow rather than smooth out. Over centuries, this is thought to build the great capes of the Carolinas, including Cape Hatteras (Ashton, Murray and Arnoult, 2001, [*Nature*](https://doi.org/10.1038/35104541)).
Near a cape, small shifts in wave direction can turn one stretch of beach from eroding to growing. That is part of why Cape Point behaves so differently from the rest of the island.

The model represents this with two settings: how often waves arrive at a steep angle, and whether more of them come from the north or the south.

</details>

## Storms move sand across the island

During big storms, water levels rise and waves can run over the dunes. This is called *overwash*. It carries sand from the beach onto the island and into the sound.
Overwash can bury roads and houses, but it is also how a barrier island builds itself higher and moves landward as the sea rises.

<figure class="hat-model-figure" data-scroll-start="0.6">
{% include hatteras/overwash.svg %}
<figcaption class="hat-caption">Not to scale. A storm surge raises the water, and waves run up the beach and over a low dune, laying down a new layer of sand across the island.</figcaption>
</figure>

<figure class="hat-photo-wide">
<img src="{{ '/assets/hatteras/img/isabel/overwash_nc12_2003.jpg' | relative_url }}" alt="Aerial photo after Hurricane Isabel: the dunes are gone and a sheet of sand reaches from the beach across the island and over NC-12, where trucks are clearing the road" loading="lazy">
<figcaption class="hat-caption">Overwash after Hurricane Isabel. Between Frisco and Hatteras Village on 21 September 2003, three days after the storm, the dunes are gone and a sheet of sand washed in from the beach covers the island and NC-12; the road shows only at the left, and trucks are clearing it. Photo: U.S. Geological Survey, <a href="https://pubs.usgs.gov/ds/761/">Archive of post-Hurricane Isabel coastal oblique aerial photographs</a> (Data Series 761), frame 2003_0921_r045s18. Public domain.</figcaption>
</figure>

## Dunes are the island's first defence

Dunes block small and medium storms from overwashing the island. Grasses trap blowing sand, so dunes regrow between storms.

<figure class="hat-model-figure" data-scroll-start="0.5">
{% include hatteras/dunes.svg %}
<figcaption class="hat-caption">Not to scale; heights exaggerated. The same storm against two dunes. (a) <i>Collision</i>: the highest reach of the waves stays below the crest of a tall dune. The waves cut into its face (hatched) and carry that sand offshore, and the island and road behind stay dry. (b) <i>Overwash</i>: the waves reach higher than the crest of a low dune, run over it, and leave a layer of sand across the island and the road. The two regimes follow the storm impact scale of Sallenger (2000, <a href="https://doi.org/10.2112/1551-5036(2000)016[0890:SISFBI]2.0.CO;2"><i>Journal of Coastal Research</i></a>).</figcaption>
</figure>
On Hatteras, many of today's dunes were built or rebuilt by people, which is covered on the [management page]({{ '/hatteras/management/' | relative_url }}).

## Rising seas

Sea level on the Outer Banks is rising.
At the NOAA {% include hatteras/term.liquid id="tide-gauge" text="tide gauge" %} at Duck, the nearest long record, the sea has risen by about 4.9 mm a year since 1978: about 23 cm (9 inches) in all.
Higher water lets storms reach farther, and over time it pushes the whole island landward.

The rise has not been steady.
Over the first period the model recreates, 1996–2015, the {% include hatteras/term.liquid id="trend" text="trend" %} was about 3.8 mm a year. Over the second, 2010–2026, it was about 5.5 mm a year.

{% include hatteras/sea_level.liquid %}

Sea level also swings up and down from month to month and year to year, so a trend fitted to 15 or 20 years shifts depending on which years it covers.
Ending the second period in 2024 instead of early 2026, for example, gives about 6.5 mm a year instead of 5.5.
The long-term rise is clearer than any single number.

<details class="hat-deeper" markdown="1">
<summary>Go deeper: the sea-level numbers</summary>

The record is the monthly mean water level at Duck (NOAA station 8651370), with the average seasonal cycle removed.
Each trend is a straight line fitted to the monthly values in its years, both end years included: 3.8 ± 1.4 mm per year for 1996–2015 and 5.5 ± 2.0 mm per year for 2010–2026 (95% ranges).
The dashed line is NOAA's own trend over the whole record, 4.9 mm per year.
This is *relative* sea-level rise: it includes any sinking of the land, which is what matters for the island.
The model raises sea level at each period's rate, rounded to the nearest millimetre: 4 mm a year for 1996–2015 and 5 mm a year for 2010–2026.

</details>

<details class="hat-deeper" markdown="1">
<summary>Key terms</summary>

{% include hatteras/glossary_list.liquid ids="shoreline,dune-line,erosion,accretion,overwash,longshore-transport,beach-nourishment" %}

Every term used on these pages is in the [glossary]({{ '/hatteras/glossary/' | relative_url }}).

</details>

{% include hatteras/pager.liquid %}
