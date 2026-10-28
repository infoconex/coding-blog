---
layout: default
title: About
seoTitle: "About Jim Scott | VP of Software Engineering & Technical Author"
description: "Meet Jim Scott, a Vice President of Software Engineering, technical author since 2008, and open-source developer focused on .NET, architecture, and automation."
permalink: /about/
stylesheet: /assets/css/about.css
profilePage: true
---

<section class="shell about-hero">
  <div>
    <div class="eyebrow">About</div>
    <h1>Building software, preserving the lessons.</h1>
  </div>
  <p class="about-hero__lede">I’m Jim Scott, a Vice President of Software Engineering who still enjoys working directly with code. I write about software engineering, architecture, open-source tools, and the lessons that survive contact with production.</p>
</section>

<section class="shell about-grid">
  <article class="about-main">
    <div class="eyebrow">The work</div>
    <h2>Engineering is more than the code that ships.</h2>
    <p>My work spans engineering leadership and hands-on software development. As a Vice President of Software Engineering, I care about helping teams build systems that are understandable, maintainable, and useful in the real world.</p>
    <p>Over the years I’ve worked across application development, architecture, infrastructure, databases, and production operations. A lot of what I write here comes from that overlap: the point where clean design meets legacy code, operational constraints, evolving requirements, and the occasional hard-earned lesson.</p>
    <p>I tend to be most interested in software design, system architecture, C#, data-intensive applications, Linux, automation, and the engineering tradeoffs that appear once a system has to live in production for a long time.</p>
    <p>This site is partly a technical notebook and partly an archive. Some articles go back many years, so they also reflect how tools, practices, and my own thinking have changed over time. I’ve kept that history intact rather than rewriting everything to look current.</p>
    <p>I value simple designs, explicit tradeoffs, strong fundamentals, and code that the next person can understand without archaeology. I’m less interested in chasing patterns for their own sake than in understanding when an idea actually makes software better.</p>
    <p>Most of the writing here is practical: examples, architecture notes, debugging discoveries, design principles, and observations collected while building and maintaining software. I also share open-source projects and experiments so readers can inspect the implementation and evaluate the results themselves.</p>

    <div class="about-principles">
      <div><strong>Design</strong><span>Make intent visible and change affordable.</span></div>
      <div><strong>Systems</strong><span>Understand behavior beyond a single function or service.</span></div>
      <div><strong>Operations</strong><span>Production is where assumptions meet evidence.</span></div>
      <div><strong>History</strong><span>Keep the record, including the parts that have aged.</span></div>
    </div>
  </article>

  <aside class="about-side">
    <div class="about-fact"><span>Writing since</span><strong>2008</strong></div>
    <div class="about-fact"><span>Role</span><strong>Vice President of Software Engineering</strong></div>
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


<section class="shell about-archive-policy" aria-labelledby="about-projects-heading">
  <div class="eyebrow">Selected open-source projects</div>
  <div>
    <h2 id="about-projects-heading">Build it. Test it. Share what works.</h2>
    <p>Some of the questions behind my writing turn into tools. These projects are public, so the code and engineering decisions are available to explore.</p>
    <div class="about-feature-list">
      <div>
        <h3><a href="https://github.com/infoconex/isolated-dotnet-sdk">Isolated .NET SDK <span aria-hidden="true">↗</span></a></h3>
        <p>A tool for managing and verifying .NET SDK installations without changing the normal development environment.</p>
      </div>
      <div>
        <h3><a href="https://github.com/infoconex/copy-github-repo">Copy GitHub Repo <span aria-hidden="true">↗</span></a></h3>
        <p>A PowerShell project exploring how to copy GitHub repositories and preserve the parts that matter.</p>
      </div>
      <div>
        <h3><a href="https://github.com/infoconex/ai-flywheel-spec">AI Flywheel Spec <span aria-hidden="true">↗</span></a></h3>
        <p>An open specification exploring how repeatable AI-assisted engineering workflows can improve through evidence and feedback.</p>
      </div>
    </div>
    <a class="text-link" href="https://projects.infoconex.com/">Explore the complete project collection →</a>
  </div>
</section>

<section class="shell about-archive-policy" aria-labelledby="about-writing-heading">
  <div class="eyebrow">Selected writing</div>
  <div>
    <h2 id="about-writing-heading">Technical answers backed by experiments.</h2>
    <p>I prefer showing what I tried, what happened, and where the limitations are. These articles are representative of that approach.</p>
    <div class="about-feature-list">
      <div>
        <h3><a href="{{ '/post/2026/10/22/too-hot-to-handle-testing-nugets-new-package-cooldown' | relative_url }}">Testing NuGet's New Package Cooldown <span aria-hidden="true">↗</span></a></h3>
        <p>An experiment examining what a NuGet publication cooldown does—and does not—protect against.</p>
      </div>
      <div>
        <h3><a href="{{ '/post/2026/10/21/managing-dotnet-sdks-installation-was-just-the-beginning' | relative_url }}">Managing .NET SDKs <span aria-hidden="true">↗</span></a></h3>
        <p>How a small SDK installation helper developed into a tool for managing, verifying, and auditing isolated SDKs.</p>
      </div>
      <div>
        <h3><a href="{{ '/post/2026/09/03/from-specification-to-system-how-the-ai-flywheel-became-four-projects' | relative_url }}">From Specification to System <span aria-hidden="true">↗</span></a></h3>
        <p>What it takes to turn an AI engineering idea into a collection of usable, independently evolving projects.</p>
      </div>
    </div>
    <a class="text-link" href="{{ '/writing/' | relative_url }}">Explore the writing archive →</a>
  </div>
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
