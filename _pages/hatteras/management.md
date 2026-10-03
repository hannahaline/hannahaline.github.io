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

Along most of Hatteras Island, a line of dunes stands between the ocean and NC-12. After storms, sand washed onto the road is pushed back onto the dunes, and low or broken dunes are rebuilt.
A tall, continuous dune keeps small and medium storms off the road and out of the villages.
It also stops overwash, the natural process that carries sand onto the island and lets it build upward as the sea rises.
An island held behind a fixed dune line can grow lower and narrower over time, compared with one that is free to roll landward.

{% include hatteras/todo.liquid text="The history of the artificial dune line on the Outer Banks (when it was built, by whom): add with a source." %}

<details class="hat-deeper" markdown="1">
<summary>Go deeper: how the model represents dune management</summary>

The model follows the same rules every year:

- **Along the road**, whenever a storm lowers the dune in front of NC-12 below a minimum height, the dune is rebuilt to a set design height. Overwash sand that lands on the road is pushed back onto the dune.
- **In the villages** (Buxton, Avon, and Salvo–Waves–Rodanthe), part of the overwash that lands among houses is removed, as people clear streets and yards. The model removes 40%, the residential end of the range measured by Rogers and others (2015).
- **Where no road or village needs protecting**, such as Cape Point and the stretch where the Jug Handle Bridge now carries the road over the sound, dunes are left to change naturally.

</details>

## NC-12: the road that sets the line

NC-12 is the only road on and off Hatteras Island. Where it runs close to the ocean, every big storm threatens to wash sand over it or cut through it. Keeping it open shapes how the rest of the beach is managed.
Where the ocean has come too close, the road has been moved:

- **1989, the S-curves north of Rodanthe.** The road was rebuilt farther inland, by up to about 110 m.
- **1999, north of Buxton.** After Hurricane Dennis, a stretch of road was moved inland by up to about 75 m.
- **2011 and 2017, New Inlet on Pea Island.** Hurricane Irene cut through the island, and the road now crosses the breach on a bridge.
- **2022, the Jug Handle Bridge.** The road at the S-curves now leaves the island and crosses Pamlico Sound, so that stretch of beach no longer has a road behind it.

We measured how far the road moved by comparing digitised road lines from 1978 and 2008, and the model moves the road by the same distances in the years the moves happened.

{% include hatteras/todo.liquid text="Photo of NC-12 behind a low dune (public domain, source noted)." %}

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

The Navy built the Buxton groins at the Cape Hatteras Lighthouse in 1969.
The 2017 and 2022 Buxton nourishment projects start at the lighthouse groin and run north.

{% include hatteras/todo.liquid text="Number of groins, the 1999 lighthouse move, and whether protecting the lighthouse was the stated purpose: add with sources." %}

<details class="hat-deeper" markdown="1">
<summary>Go deeper: modelling a groin</summary>

CASCADE did not include hard structures, so part of my research adds a groin module.
In the model, the groin blocks a share of the sand moving along the shore at its location. The beach on one side gains what the other side loses.
We test it by asking whether the model, with the groin in place, reproduces the shoreline change measured on both sides of the Buxton groins.

</details>

{% include hatteras/pager.liquid %}
