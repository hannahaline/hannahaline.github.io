---
layout: page
title: The model
permalink: /hatteras/model/
description: How the CASCADE model works, and how well it recreates Hatteras Island's recent past.
nav: false
---

{% include hatteras/subnav.liquid %}

<p class="hat-lead">
CASCADE is a computer model of a barrier island and the people who manage it.
It starts from a detailed map of the island's elevation, applies the storms, waves, and sea-level rise that actually happened, and lets the island change, year by year.
</p>

## How it works, in four parts

<div class="hat-cards">
  <div class="hat-card-static">
    <h3>1. The starting island</h3>
    <p>Laser elevation surveys (lidar) give the height of the beach, dunes, and island interior at the start of each run.</p>
  </div>
  <div class="hat-card-static">
    <h3>2. Storms and overwash</h3>
    <p>Each year, the real storms from the record are sent over the island. Where they overtop the dunes, sand moves inland.</p>
  </div>
  <div class="hat-card-static">
    <h3>3. Sand along the shore</h3>
    <p>Waves move sand along the beach between neighbouring stretches of island, so what happens in one place affects the next.</p>
  </div>
  <div class="hat-card-static">
    <h3>4. People</h3>
    <p>Management rules rebuild dunes, add nourishment sand, and protect or move the road, as happened in real life.</p>
  </div>
</div>

{% include hatteras/todo.liquid text="Turn the four cards into one diagram (a stack of island strips with arrows for overwash, longshore transport, and management), in house style." %}

<details class="hat-deeper" markdown="1">
<summary>Go deeper: what is inside CASCADE</summary>

CASCADE couples two existing models. **Barrier3D** simulates the cross-shore processes on each stretch of island: dune growth, storm overwash, and shoreface change. **BRIE** simulates sand moving alongshore between stretches.
Human-management modules sit on top: beach and dune management, roadway management, and, in this project, a groin module.
The model is open source ([CASCADE on GitHub](https://github.com/UNC-CECL/CASCADE)).

{% include hatteras/todo.liquid text="Add citations: Anarde et al. for CASCADE, Reeves et al. for Barrier3D, Nienhuis and Lorenzo-Trueba for BRIE. Add the domain size and number of domains in plain words." %}

</details>

## Does it recreate the past?

{% include hatteras/panel.liquid id="model-vs-observed" wide=true title="Model versus observations, with and without management" plan="The island as a line: observed shoreline change (CoastSat) against CASCADE, with a toggle for 'with management' versus 'no management'. Windows 1996–2015 and 2010–2026 to match the canonical periods. Plain summary of the skill below. UNPUBLISHED: keep it behind the draft flag until the paper is accepted." %}

{% include hatteras/todo.liquid text="One paragraph on what the model gets right, and where it misses (and why that is useful to know)." %}

## What this lets us do next

A model that reproduces the past gives us a way to ask "what if" questions:
what if the dunes were not rebuilt after a storm, what if a stretch of road were moved, or what if the seas rise faster?
Those forecasts are the next stage of this research, and they will be shared on this site as they are completed.

{% include hatteras/pager.liquid %}
