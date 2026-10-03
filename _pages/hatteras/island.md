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

<figure class="hat-model-figure">
{% include hatteras/longshore.svg %}
<figcaption class="hat-caption">Simplified. Along Hatteras Island's east-facing shore, waves from the northeast drive sand south toward Cape Hatteras. Arrow widths are schematic, read from the shoreline record: the drift grows where the beach is eroding (more sand leaving than arriving), holds steady where the beach is stable, and ends at Cape Point, where sand builds up. Island outline © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors.</figcaption>
</figure>

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

<figure class="hat-model-figure">
{% include hatteras/overwash.svg %}
<figcaption class="hat-caption">Not to scale. A storm surge raises the water, and waves run up the beach and over a low dune, laying down a new layer of sand across the island.</figcaption>
</figure>

{% assign sandy = '/assets/hatteras/img/sandy/' | relative_url %}
<div class="hat-pairs">
<figure class="hat-pair">
<div class="hat-pair-photos">
<figure><img src="{{ sandy }}buxton_2011.jpg" alt="Buxton from the air in August 2011: oceanfront houses behind a wide, dry beach" loading="lazy"></figure>
<figure><img src="{{ sandy }}buxton_2012.jpg" alt="The same houses at Buxton in November 2012: the beach is gone in front of them, the houses stand at the water's edge, and sand covers the ground and roads behind" loading="lazy"></figure>
</div>
<figcaption class="hat-caption"><b>Buxton, after Hurricane Sandy.</b> Looking west along the shore on 30 August 2011, just after Hurricane Irene (left), and on 4 November 2012, after Sandy (right). Erosion moved the shoreline landward until it reached the houses built on the beach, and sand on the roads shows overwash; some of that sand was already there after Irene. The yellow arrow points to the same building. Photos: U.S. Geological Survey, St. Petersburg Coastal and Marine Science Center, <a href="https://www.usgs.gov/media/images/oblique-aerial-photographs-buxton-north-carolina">Oblique aerial photographs of Buxton, North Carolina</a>. Public domain.</figcaption>
</figure>
</div>

## Dunes are the island's first defence

Dunes block small and medium storms from overwashing the island. Grasses trap blowing sand, so dunes regrow between storms.
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
