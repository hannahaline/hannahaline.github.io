---
layout: page
title: The model
permalink: /hatteras/model/
description: How the CASCADE model works, and how well it recreates Hatteras Island's recent past.
nav: false
---

{% include hatteras/subnav.liquid %}

<p class="hat-lead">
CASCADE is a computer model of a {% include hatteras/term.liquid id="barrier-island" text="barrier island" %} and the people who manage it.
It starts from a detailed map of the island's elevation, applies the storms, waves, and sea-level rise that actually happened, and lets the island change, year by year.
</p>

## How it works, in four parts

<figure class="hat-model-figure">
{% include hatteras/model_diagram.svg %}
</figure>

<ol class="hat-model-parts">
  <li><b>The starting island.</b> Laser elevation surveys (lidar) give the height of the beach, dunes, and island interior at the start of each run, on a grid of 10 m cells.</li>
  <li><b>Storms and overwash.</b> Each year, the real storms from the record are sent over the island. Where they overtop the dunes, sand moves inland.</li>
  <li><b>Sand along the shore.</b> Waves move sand along the beach between neighbouring stretches of island, so what happens in one place affects the next.</li>
  <li><b>People.</b> Management rules rebuild dunes, add nourishment sand, and protect or move the road, as happened in real life.</li>
</ol>

<details class="hat-deeper" markdown="1">
<summary>Go deeper: what is inside CASCADE</summary>

CASCADE couples two existing models. **Barrier3D** simulates the cross-shore processes on each stretch of island: dune growth, storm overwash, and shoreface change. **BRIE** simulates sand moving alongshore between stretches.
Human-management modules sit on top: beach and dune management, roadway management, and, in this project, a groin module.
The model is open source ([CASCADE on GitHub](https://github.com/UNC-CECL/CASCADE)).

For Hatteras, the island from Cape Point to just north of Rodanthe (about 45 km) is divided into 90 stretches, each 500 m long. Each stretch is a grid of 10 m cells running from the ocean across the island.
Sand moves across each stretch in storms, and between neighbouring stretches with the waves.

**References**

- Anarde, K. A., Moore, L. J., Murray, A. B., and Reeves, I. R. B. (2024). The future of developed barrier systems: 1. Pathways toward uninhabitability, drowning, and rebound. *Earth's Future*, 12(4), e2023EF003672. [doi:10.1029/2023EF003672](https://doi.org/10.1029/2023EF003672)
- Anarde, K. A., Moore, L. J., Murray, A. B., and Reeves, I. R. B. (2024). The future of developed barrier systems: 2. Alongshore complexities and emergent climate change dynamics. *Earth's Future*, 12(4), e2023EF004200. [doi:10.1029/2023EF004200](https://doi.org/10.1029/2023EF004200)
- Reeves, I. R. B., Moore, L. J., Murray, A. B., Anarde, K. A., and Goldstein, E. B. (2021). Dune dynamics drive discontinuous barrier retreat. *Geophysical Research Letters*, 48(13), e2021GL092958. [doi:10.1029/2021GL092958](https://doi.org/10.1029/2021GL092958)
- Nienhuis, J. H., and Lorenzo-Trueba, J. (2019). Simulating barrier island response to sea level rise with the barrier island and inlet environment (BRIE) model v1.0. *Geoscientific Model Development*, 12(9), 4013–4030. [doi:10.5194/gmd-12-4013-2019](https://doi.org/10.5194/gmd-12-4013-2019)

</details>

## Does it recreate the past?

{% include hatteras/panel.liquid id="model-vs-observed" wide=true title="Model versus observations, with and without management" plan="The island as a line: observed shoreline change (CoastSat) against CASCADE, with a toggle for 'with management' versus 'no management'. Windows 1996–2015 and 2010–2026 to match the canonical periods. Plain summary of the skill below. UNPUBLISHED: keep it behind the draft flag until the paper is accepted." %}

{% comment %} DRAFT, unpublished results: shown only while hatteras_draft is on. Written 2026-10-03 from the CASCADE
diagnoses (2010-2024 failure diagnosis, dune recovery diagnosis, groin option A study, the 2021 step); Hannah to check
every claim against the 1996-2015 / 2010-2026 matrix before it goes public. {% endcomment %}
{% if site.hatteras_draft %}
{% include hatteras/todo.liquid text="Draft for Hannah to check against the 2026-window matrix. Hidden from the public build until the paper is accepted." %}

The model does best in the earlier period. It captures the broad pattern of where the island lost ground and where it held, and it overwashes the island in roughly the storms that did so in reality.
Including management matters: rebuilding dunes and adding sand closes the low spots in the dune line that otherwise let storms through, and brings the model's erosion much closer to what happened.

It misses in three places, and each one teaches us something.
It cannot make the island-wide seaward jump of 2021, which no process in the model explains.
Its dunes regrow too slowly after a storm flattens them, so in the stormier later years it lets too much water over the island.
And it has no process that keeps Cape Point built out, so the cape smooths away unless something, like the groins, holds it.
Knowing where the model falls short tells us which forecasts to trust most, and which parts of the model to improve next.
{% endif %}

## What this lets us do next

A model that reproduces the past gives us a way to ask "what if" questions:
what if the dunes were not rebuilt after a storm, what if a stretch of road were moved, or what if the seas rise faster?
Those forecasts are the next stage of this research, and they will be shared on this site as they are completed.

{% include hatteras/pager.liquid %}
