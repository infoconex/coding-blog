---
layout: default
title: About
description: About Jim Scott, this engineering archive, and why the historical record stays intact.
permalink: /about/
stylesheet: /assets/css/about.css
---

<section class="shell about-hero">
  <div>
    <div class="eyebrow">About</div>
    <h1>Building software, preserving the lessons.</h1>
  </div>
  <p class="about-hero__lede">I’m Jim Scott. I write about software engineering, architecture, systems, code, and the lessons that survive contact with production.</p>
</section>

<section class="shell about-grid">
  <article class="about-main">
    <div class="eyebrow">The work</div>
    <h2>Engineering is more than the code that ships.</h2>
    <p>I’m a software engineer focused on building systems that are understandable, maintainable, and useful in the real world.</p>
    <p>Over the years I’ve worked across application development, architecture, infrastructure, databases, and production operations. A lot of what I write here comes from that overlap: the point where clean design meets legacy code, operational constraints, evolving requirements, and the occasional hard-earned lesson.</p>
    <p>I tend to be most interested in software design, system architecture, C#, data-intensive applications, Linux, automation, and the engineering tradeoffs that appear once a system has to live in production for a long time.</p>
    <p>This site is partly a technical notebook and partly an archive. Some articles go back many years, so they also reflect how tools, practices, and my own thinking have changed over time. I’ve kept that history intact rather than rewriting everything to look current.</p>
    <p>I value simple designs, explicit tradeoffs, strong fundamentals, and code that the next person can understand without archaeology. I’m less interested in chasing patterns for their own sake than in understanding when an idea actually makes software better.</p>
    <p>Most of the writing here is practical: examples, architecture notes, debugging discoveries, design principles, and observations collected while building and maintaining software.</p>

    <div class="about-principles">
      <div><strong>Design</strong><span>Make intent visible and change affordable.</span></div>
      <div><strong>Systems</strong><span>Understand behavior beyond a single function or service.</span></div>
      <div><strong>Operations</strong><span>Production is where assumptions meet evidence.</span></div>
      <div><strong>History</strong><span>Keep the record, including the parts that have aged.</span></div>
    </div>
  </article>

  <aside class="about-side">
    <div class="about-fact"><span>Writing since</span><strong>2008</strong></div>
    <div class="about-fact"><span>Focus</span><strong>Software engineering</strong></div>
    <div class="about-fact"><span>Archive</span><strong>Historical URLs preserved</strong></div>
    {% if site.profile_links %}
    <div class="about-links">
      <span>Elsewhere</span>
      {% for link in site.profile_links %}
        <a href="{{ link.url }}" rel="me">{{ link.title }} ↗</a>
      {% endfor %}
    </div>
    {% endif %}
  </aside>
</section>

<section class="shell about-archive-policy">
  <div class="eyebrow">Archive policy</div>
  <div>
    <h2>Old technical writing stays old.</h2>
    <p>I preserve historical posts at their original public paths instead of silently rewriting them to look current. Technology changes. APIs disappear. Practices improve. An older article can still be useful as a record of how a problem was approached at the time without pretending it is current guidance.</p>
    <p>Older articles receive an archive notice when appropriate. If an article is substantially revisited, the update should be explicit rather than erasing the original context.</p>
    <a class="text-link" href="{{ '/archive/' | relative_url }}">Browse the full archive →</a>
  </div>
</section>

<section class="shell about-closing">
  <div>
    <div class="eyebrow">Keep exploring</div>
    <h2>Start with the writing, then follow the threads.</h2>
  </div>
  <div class="about-actions">
    <a href="{{ '/writing/' | relative_url }}">Browse writing <span>→</span></a>
    <a href="{{ '/archive/' | relative_url }}">Explore history <span>→</span></a>
  </div>
</section>
