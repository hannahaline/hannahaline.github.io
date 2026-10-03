---
layout: page
title: research
permalink: /research/
description: Barrier island change, coastal wildlife, and the people who manage both.
nav: true
nav_order: 1
display_categories: [current research, past research]
horizontal: false
map: true
---

<div class="research-intro">
<p>Barrier islands are shaped by storms, sea-level rise, sediment moving along the coast, and the people who live on them. My dissertation uses numerical modeling, satellite records, and field data to understand how these islands change, and what that means for the communities and wildlife that depend on them. Three questions guide it:</p>
<ol class="research-questions">
<li><a href="/projects/1_hatteras_hindcast_forecast/"><b>Can we reproduce, and then forecast, how a developed barrier island evolves?</b></a> Hindcasting and forecasting Hatteras Island with CASCADE.</li>
<li><a href="/projects/2_groin_module/"><b>How do hard structures like groins change that evolution?</b></a> Building a groin module and testing it at Buxton.</li>
<li><a href="/projects/3_vcr_oystercatchers/"><b>How does barrier island change reshape habitat for nesting shorebirds?</b></a> American Oystercatchers on the Virginia Coast Reserve.</li>
</ol>
</div>

<h2 class="map-heading">Where I work</h2>
<div id="research-map" role="region" aria-label="Map of research sites"></div>
<p class="map-note">Click a marker to open the project. Teal: current research · grey: past research · gold: training and fieldwork.</p>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.min.css" integrity="sha256-QZFpF9DkpabUBLoCc7fQJVCmtag/LaVAfAkUJSfuNyY=" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.min.js" integrity="sha256-MgH13bFTTNqsnuEoqNPBLDaqxjGH+lCpqrukmXc8Ppg=" crossorigin="anonymous"></script>
<script>
document.addEventListener("DOMContentLoaded", function () {
  var sites = [
    { ll: [35.27, -75.53], kind: "current", title: "Hatteras Island, North Carolina", links: [["Chapter 1: Hindcasting and forecasting Hatteras Island", "/projects/1_hatteras_hindcast_forecast/"], ["Chapter 2: Hard structures in CASCADE (Buxton groins)", "/projects/2_groin_module/"]] },
    { ll: [37.42, -75.70], kind: "current", title: "Virginia Coast Reserve, Virginia", links: [["Chapter 3: Shorebird nesting habitat", "/projects/3_vcr_oystercatchers/"]] },
    { ll: [30.45, -88.00], kind: "past", title: "Mobile Bay, Alabama", links: [["Marine wildlife and stakeholders on the Alabama coast", "/projects/4_alabama_marine_wildlife/"]] },
    { ll: [40.04, -105.25], kind: "past", title: "NCAR, Boulder, Colorado", links: [["Modeling coral bleaching in National Marine Sanctuaries (Bridge to GVP, 2024)", "/projects/7_ncar_coral_bleaching/"]] },
    { ll: [29.65, -82.34], kind: "past", title: "University of Florida, Gainesville", text: "Avian Behavioral Ecology and Conservation Lab, 2020–2022: 434 bioacoustic samples processed to train a machine learning model of avian communication across the U.S. and Europe" },
    { ll: [34.70, -76.55], kind: "training", title: "Cape Lookout and Shackleford Banks, North Carolina", text: "Duke University barrier island processes field course, 2025" },
    { ll: [29.55, -83.35], kind: "past", title: "Big Bend, Florida", text: "Sea turtle distribution and habitat use with the Sea Turtle Conservancy, 2019–2020: in-water captures, biological sampling, and satellite tagging along 250 km of coast" },
    { ll: [21.16, -90.03], kind: "past", title: "Gulf of Mexico (U.S., Mexico, Cuba)", links: [["Transboundary fisheries in the Gulf of Mexico", "/projects/5_swimm_gulf_fisheries/"]] },
    { ll: [13.25, -61.20], kind: "past", title: "St. Vincent and the Grenadines", links: [["The endangered St. Vincent Amazon Parrot", "/projects/6_st_vincent_parrot/"]] },
    { ll: [-7.00, 110.42], kind: "training", title: "Semarang and Yogyakarta, Indonesia", text: "NSF-ASI Graduate Training Program in Coastal Hazards, 2025" }
  ];
  var colors = { current: "#2f7f93", past: "#7f8a90", training: "#c8880f" };
  var start = function () {
    if (typeof L === "undefined") { return setTimeout(start, 100); }
    var map = L.map("research-map", { scrollWheelZoom: false, worldCopyJump: true });
    L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
      attribution: "Tiles &copy; Esri &mdash; Esri, HERE, Garmin, &copy; OpenStreetMap contributors",
      maxZoom: 16
    }).addTo(map);
    L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}", {
      maxZoom: 16
    }).addTo(map);
    var bounds = [];
    sites.forEach(function (s) {
      var html = "<b>" + s.title + "</b>";
      if (s.links) { s.links.forEach(function (l) { html += '<br><a href="' + l[1] + '">' + l[0] + "</a>"; }); }
      if (s.text) { html += "<br>" + s.text; }
      L.circleMarker(s.ll, { radius: 9, color: "#fff", weight: 2, fillColor: colors[s.kind], fillOpacity: 0.95 }).addTo(map).bindPopup(html);
      bounds.push(s.ll);
    });
    map.fitBounds(bounds, { padding: [30, 30] });
  };
  start();
});
</script>

<!-- pages/projects.md -->
<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  <!-- Generate cards for each project -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>
