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

For Hatteras, the island from Cape Point to just north of Rodanthe (about 45 km) is divided into 90 stretches, each 500 m long. Each stretch is a grid of 10 m cells running from the ocean across the island.
Sand moves across each stretch in storms, and between neighbouring stretches with the waves.

**References**

- Anarde, K., Moore, L. J., Murray, A. B., and Reeves, I. R. B. (2024). The future of developed barrier systems, Part I: Pathways toward uninhabitability, drowning, and rebound. [Preprint, EarthArXiv](https://doi.org/10.31223/X5P947).
- Reeves, I. R. B., Moore, L. J., Murray, A. B., Anarde, K. A., and Goldstein, E. B. (2021). Dune dynamics drive discontinuous barrier retreat. *Geophysical Research Letters*.
- Nienhuis, J. H., and Lorenzo-Trueba, J. (2019). Simulating barrier island response to sea level rise with the barrier island and inlet environment (BRIE) model v1.0. *Geoscientific Model Development*.

{% include hatteras/todo.liquid text="Check the author lists and add DOIs for Reeves et al. (2021) and Nienhuis and Lorenzo-Trueba (2019); confirm Anarde et al. is still the preprint." %}

</details>

## Does it recreate the past?

{% include hatteras/panel.liquid id="model-vs-observed" wide=true title="Model versus observations, with and without management" plan="The island as a line: observed shoreline change (CoastSat) against CASCADE, with a toggle for 'with management' versus 'no management'. Windows 1996–2015 and 2010–2026 to match the canonical periods. Plain summary of the skill below. UNPUBLISHED: keep it behind the draft flag until the paper is accepted." %}

{% include hatteras/todo.liquid text="One paragraph on what the model gets right, and where it misses (and why that is useful to know)." %}

## What this lets us do next

A model that reproduces the past gives us a way to ask "what if" questions:
what if the dunes were not rebuilt after a storm, what if a stretch of road were moved, or what if the seas rise faster?
Those forecasts are the next stage of this research, and they will be shared on this site as they are completed.

{% include hatteras/pager.liquid %}
