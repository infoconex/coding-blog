---
layout: default
title: Projects
description: Selected software and engineering projects.
permalink: /projects/
published: false
---
<section class="shell" style="padding:clamp(64px,9vw,112px) 0 100px;max-width:980px">
  <div class="eyebrow">Projects</div>
  <h1 style="font-family:var(--font-heading,var(--font-sans));font-size:clamp(54px,8vw,96px);font-weight:var(--heading-weight,800);line-height:.92;letter-spacing:-.055em;margin:18px 0 42px;text-transform:var(--heading-transform,none)">Things built beyond the archive.</h1>
  {% for project in site.data.projects %}
    <article style="padding:24px 0;border-top:1px solid var(--line)">
      <h2><a href="{{ project.url }}">{{ project.title }}</a></h2>
      {% if project.description %}<p>{{ project.description }}</p>{% endif %}
      {% if project.tags %}<div class="eyebrow">{{ project.tags | join: ' · ' }}</div>{% endif %}
    </article>
  {% endfor %}
</section>
