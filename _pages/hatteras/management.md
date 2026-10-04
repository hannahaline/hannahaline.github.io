---
layout: page
title: How management shapes the island
permalink: /hatteras/management/
description: Beach nourishment, NC-12, dune building, and groins, and what each one does to the island.
nav: false
---

{% include hatteras/subnav.liquid %}

<p class="hat-lead">
Hatteras Island today is partly a product of nature and partly a product of people.
For decades, people have built dunes, paved and moved a highway, pumped sand onto beaches, and built structures to hold the shore in place.
Each of these changes how sand moves, and therefore how the island changes.
</p>

{% include hatteras/timeline.liquid mode="management" %}

Open marks on the timeline are projects shown for context that the model does not include.
The model also leaves out the sand dredged from Oregon Inlet's navigation channel and placed on Pea Island beaches in several years (1990, 1999, 2000, 2003 and 2004), and the emergency fills on Pea Island after Hurricane Isabel (2003) and in 2013.

## Dune building

Along most of Hatteras Island, a line of dunes stands between the ocean and {% include hatteras/term.liquid id="nc-12" %}. After storms, sand washed onto the road is pushed back onto the dunes, and low or broken dunes are rebuilt.
A tall, continuous dune keeps small and medium storms off the road and out of the villages.
It also stops {% include hatteras/term.liquid id="overwash" text="overwash" %}, the natural process that carries sand onto the island and lets it build upward as the sea rises.
An island held behind a fixed {% include hatteras/term.liquid id="dune-line" text="dune line" %} can grow lower and narrower over time, compared with one that is free to roll landward.

The dune line itself is largely built by people.
Between 1936 and 1940, Civilian Conservation Corps and Works Progress Administration crews, directed by the National Park Service, put up almost 3 million feet of sand fencing to build a continuous barrier dune along the Outer Banks.
The Park Service added to it in the late 1950s and rebuilt dunes after the 1962 Ash Wednesday storm, then stopped maintaining the dune line in the early 1970s.

<p class="hat-caption">Sources: Dolan and Godfrey (1972), <a href="https://npshistory.com/publications/water/nrr-5.pdf"><i>Dune Stabilization and Beach Erosion, Cape Hatteras National Seashore</i></a>, NPS Natural Resource Report 5; National Park Service, <a href="https://www.nps.gov/subjects/geology/management-response-to-storms.htm">Management Response to Storms</a>.</p>

<details class="hat-deeper" markdown="1">
<summary>Go deeper: how the model represents dune management</summary>

The model follows the same rules every year:

- **Along the road**, whenever a storm lowers the dune in front of NC-12 below a minimum height, the dune is rebuilt to a set design height. Overwash sand that lands on the road is pushed back onto the dune.
- **In the villages** (Buxton, Avon, and Salvo–Waves–Rodanthe), part of the overwash that lands among houses is removed, as people clear streets and yards. The model removes 40%, the residential end of the range measured by Rogers and others (2015).
- **Where no road or village needs protecting**, such as Cape Point and the stretch where the Jug Handle Bridge now carries the road over the {% include hatteras/term.liquid id="sound" text="sound" %}, dunes are left to change naturally.

</details>

## NC-12: the road that sets the line

NC-12 is the only road on and off Hatteras Island. Where it runs close to the ocean, every big storm threatens to wash sand over it or cut through it. Keeping it open shapes how the rest of the beach is managed.
Where the ocean has come too close, the road has been moved:

- **1989, the S-curves north of Rodanthe.** The road was rebuilt farther inland, by up to about 110 m.
- **1999, north of Buxton.** After Hurricane Dennis, a stretch of road was moved inland by up to about 75 m.
- **2011 and 2017, New Inlet on Pea Island.** Hurricane Irene cut through the island, and the road now crosses the {% include hatteras/term.liquid id="breach" text="breach" %} on a bridge.
- **2022, the Jug Handle Bridge.** The road at the S-curves now leaves the island and crosses Pamlico Sound, so that stretch of beach no longer has a road behind it.

<figure class="hat-photo-wide">
<img src="{{ '/assets/hatteras/img/road_moves_map.jpg' | relative_url }}" alt="Three aerial maps of NC-12: north of Buxton, where the road was moved inland in 1999; the Rodanthe S-curves, where it was moved inland in 1989 and then bypassed by the Jug Handle Bridge in 2022; and New Inlet on Pea Island in early 2012, with Hurricane Irene's breach and the temporary bridge across it" loading="lazy">
<figcaption class="hat-caption">Where NC-12 has been moved. Dashed: the road before a move; orange: after the 1989 or 1999 move; yellow: the road today. Distances are the largest measured moves. Imagery: Esri World Imagery (left, middle); NC OneMap / NC Center for Geographic Information and Analysis, early 2012 (right).</figcaption>
</figure>

We measured how far the road moved by comparing digitised road lines from 1978 and 2008, and the model moves the road by the same distances in the years the moves happened.

<figure class="hat-photo-wide" style="max-width: 34rem; margin-left: auto; margin-right: auto;">
<img src="{{ '/assets/hatteras/img/nc12_scurves_2016.jpg' | relative_url }}" alt="Aerial photo of NC-12 at the Rodanthe S-curves running a short distance behind a low dune line, with a narrow beach and the surf beyond" loading="lazy">
<figcaption class="hat-caption">NC-12 at the Rodanthe S-curves in early 2016, running just behind a low, narrow dune line with the ocean a few tens of metres away. Since 2022 the Jug Handle Bridge has carried the road around this stretch. Imagery: NC OneMap / NC Center for Geographic Information and Analysis.</figcaption>
</figure>

## Beach nourishment

Beach nourishment means dredging sand from offshore and pumping it onto the beach, to make the beach wider and higher.
A wider beach takes the brunt of storm waves before they reach the dunes, houses and road.
The added sand does not stay put: waves spread it along the shore and carry some of it offshore, so many projects are repeated; Buxton's beach was nourished in 2017 and again in 2022.

The model includes four projects:

| Year | Where | Sand placed |
|---|---|---|
| 2014 | Rodanthe, the S-curves | about 1.6 million cubic yards |
| 2017 | Buxton, 2.9 miles north from the lighthouse groin | about 2.6 million cubic yards |
| 2022 | Buxton, the same 2.9 miles | about 1.2 million cubic yards |
| 2022 | Avon, north of the pier to the village edge | about 1.0 million cubic yards |
{: .hat-table}

Each project shows up in the satellite record as a sudden seaward jump on that stretch of beach (see the [shoreline change page]({{ '/hatteras/shoreline-change/' | relative_url }})).

{% include hatteras/panel.liquid id="nourishment-explorer" title="Where the sand went" plan="Small multiples or a slider: the shoreline before, just after, and some years after each fill, observed versus modelled." %}

## Groins and hard structures

A groin is a wall built out across the beach into the surf.
It catches sand moving along the shore, so the beach on the side the sand comes from grows wider.
The beach on the other side is cut off from that sand and often erodes faster.

<figure class="hat-model-figure" data-scroll-start="0.3">
{% include hatteras/groin.svg %}
<figcaption class="hat-caption">Not to scale. Sand drifting along the shore piles up against the groin, widening the beach on the side it comes from; the beach beyond the groin is starved of sand and cut back.</figcaption>
</figure>

In 1969–70 the US Navy built three groins at Buxton, two north and one just south of where the Cape Hatteras Lighthouse then stood, to protect its Naval Facility; they also shielded the lighthouse.
The shore kept retreating, and in the summer of 1999 the lighthouse itself was moved 2,900 feet (880 m) to the southwest.
The 2017 and 2022 Buxton nourishment projects start at the lighthouse groin and run north.

<p class="hat-caption">Sources: National Park Service, <a href="https://parkplanning.nps.gov/showFile.cfm?projectID=132446&amp;sfid=813968">Buxton Southern Groin Repair</a> (2025); Dare County, <a href="https://www.deq.nc.gov/coastal-management/proposed-groin-repairs-buxton-20250624-ncdcm/open">proposed groin repairs at Buxton</a>, NC Division of Coastal Management (2025); National Park Service, <a href="https://www.nps.gov/caha/learn/historyculture/movingthelighthouse.htm">Moving the Cape Hatteras Lighthouse</a>.</p>

<details class="hat-deeper" markdown="1">
<summary>Go deeper: modelling a groin</summary>

CASCADE did not include hard structures, so part of my research adds a groin module.
In the model, the groin blocks a share of the sand moving along the shore at its location. The beach on one side gains what the other side loses.
We test it by asking whether the model, with the groin in place, reproduces the shoreline change measured on both sides of the Buxton groins.

</details>

{% include hatteras/pager.liquid %}
