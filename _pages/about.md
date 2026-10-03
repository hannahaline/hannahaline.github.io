---
layout: about
title: about
permalink: /
subtitle: >-
  <span class="hero-role">Ph.D. candidate, <a href="https://cecl.online/">Coastal Environmental Change Lab</a>, UNC Chapel Hill</span>
  <span class="hero-tagline">How barrier islands change, and what that means for the people and wildlife that depend on them</span>
  <span class="hero-buttons">
  <a class="hero-btn" href="https://scholar.google.com/citations?user=rFOSoSYAAAAJ">Google Scholar</a>
  <a class="hero-btn" href="https://orcid.org/0000-0003-0767-8669">ORCID</a>
  <a class="hero-btn" href="/cv/">CV</a>
  </span>

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # news is drawn below as a picture feed instead
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 10 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
---

I am a Ph.D. candidate in Earth, Marine, and Environmental Sciences at UNC Chapel Hill, where I study how barrier islands change—and what that means for the people and wildlife that depend on them. My research integrates coastal geomorphology, wildlife ecology, and human dimensions to examine shoreline change on developed and undeveloped coastlines under climate change.

On Hatteras Island, I use numerical modeling and remote sensing to evaluate management strategies, such as beach nourishment and groin installation, alongside stakeholder input from communities, agencies, and conservation organizations navigating real decisions about infrastructure and managed retreat. In parallel, I model shorebird habitat dynamics on the Virginia Coast Reserve to understand how geomorphic change shapes species persistence over time.


<div class="about-banner mt-4">
{% include figure.liquid loading="lazy" path="assets/img/photos/banner-barrier-aerial.jpg" alt="Aerial view of barrier islands, an inlet, and the sound behind them" class="img-fluid rounded z-depth-1 banner-img" %}
</div>

<div class="row mt-4 about-columns">
  <div class="col-md-6">
    <h3>Interests</h3>
    <ul class="about-list">
      <li>Barrier island evolution and coastal geomorphology</li>
      <li>Numerical modeling and remote sensing</li>
      <li>Coastal management, infrastructure, and managed retreat</li>
      <li>Shorebird habitat and coastal wildlife conservation</li>
      <li>Human dimensions of coastal change</li>
    </ul>
    <div class="about-field-photo mt-2">
      {% include figure.liquid loading="lazy" path="assets/img/photos/hatteras-dunes.jpg" alt="Hannah standing among dune grasses on a barrier island" class="img-fluid rounded z-depth-1" %}
    </div>
  </div>
  <div class="col-md-6">
    <h3>Education</h3>
    <ul class="about-list education">
      <li><i class="fa-solid fa-graduation-cap"></i><span><b>Ph.D. in Earth, Marine, and Environmental Sciences</b>, 2024–present<br><small>University of North Carolina at Chapel Hill · advisor <a href="https://cecl.online/about/">Dr. Laura Moore</a><br><i>Dissertation: Modeling Coupled Dynamics of Mid-Atlantic Barrier Islands for Improved Coastal Management</i><br>Committee: Dr. Sarah Karpanty, Dr. Katherine Anarde, Dr. Tamlin Pavelsky, Dr. Antonio B. Rodriguez</small></span></li>
      <li><i class="fa-solid fa-graduation-cap"></i><span><b>M.S. in Natural Resources</b>, 2024<br><small>Auburn University · advisor <a href="https://www.uwyo.edu/haub/about-us/people/dunning-kelly.html">Dr. Kelly Dunning</a><br><i>Thesis: <a href="https://etd.auburn.edu/handle/10415/9305">Conservation Compliance and Public Awareness: Assessing Dolphin and Sea Turtle Interactions in Coastal Alabama</a></i></small></span></li>
      <li><i class="fa-solid fa-graduation-cap"></i><span><b>B.S. in Wildlife Ecology &amp; Conservation</b>, 2022, Summa Cum Laude<br><small>University of Florida · advisors <a href="https://wec.ifas.ufl.edu/people/wec-faculty/kathryn-sieving/">Dr. Kathryn Sieving</a> and <a href="https://case.fiu.edu/about/directory/profiles/gomes-cristina.html">Dr. Cristina Gomes</a><br><i>Honors thesis: Utilizing Bioacoustics for Conservation of the St. Vincent Amazon Parrot</i><br>Minors: Economics; International Studies in Agricultural and Life Sciences</small></span></li>
    </ul>
  </div>
</div>

<h2 class="news-heading">News</h2>

<div class="news-feed">
{%- assign news_items = site.news | sort: "date" | reverse -%}
{%- assign pictured = 0 -%}
{%- for item in news_items -%}
{%- if item.img -%}
{%- assign side = pictured | modulo: 2 -%}
{%- assign pictured = pictured | plus: 1 -%}
<div class="row news-card align-items-center">
<div class="col-md-4{% if side == 1 %} news-img-right{% endif %}">
{%- include figure.liquid loading="lazy" path=item.img alt=item.title class="img-fluid rounded z-depth-1 news-img" -%}
</div>
<div class="col-md-8">
<h3 class="news-title">{{ item.title }}</h3>
<p class="news-date">{{ item.date | date: "%B %Y" }}</p>
<div class="news-text">{{ item.content }}</div>
</div>
</div>
{%- else -%}
<div class="row news-line">
<div class="col-sm-2 news-date">{{ item.date | date: "%b %Y" }}</div>
<div class="col-sm-10 news-text">{{ item.content }}</div>
</div>
{%- endif -%}
{%- endfor -%}
</div>
