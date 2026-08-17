---
layout: default
title: Talks
description: Talks, presentations, and engineering sessions.
permalink: /talks/
published: false
---
<section class="shell" style="padding:clamp(64px,9vw,112px) 0 100px;max-width:980px">
  <div class="eyebrow">Talks</div>
  <h1 style="font-family:var(--font-heading,var(--font-sans));font-size:clamp(54px,8vw,96px);font-weight:var(--heading-weight,800);line-height:.92;letter-spacing:-.055em;margin:18px 0 42px;text-transform:var(--heading-transform,none)">Ideas presented out loud.</h1>
  {% for talk in site.data.talks %}
    <article style="padding:24px 0;border-top:1px solid var(--line)">
      <div class="eyebrow">{% if talk.date %}{{ talk.date }}{% endif %}{% if talk.event %} · {{ talk.event }}{% endif %}</div>
      <h2>{% if talk.url %}<a href="{{ talk.url }}">{{ talk.title }}</a>{% else %}{{ talk.title }}{% endif %}</h2>
      {% if talk.description %}<p>{{ talk.description }}</p>{% endif %}
    </article>
  {% endfor %}
</section>
