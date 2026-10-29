---
layout: default
title: About
seoTitle: "About Jim Scott | VP of Software Engineering & Technical Author"
description: "Meet Jim Scott, a Vice President of Software Engineering, technical author since 2008, and open-source developer focused on .NET, architecture, and automation."
permalink: /about/
redirect_from:
  - /author/jscott/
  - /author/jscott.aspx
stylesheet: /assets/css/about.css
profilePage: true
---

{% assign portrait_asset = site.static_files | where: "path", "/assets/images/about/jim-scott.webp" | first %}
<section class="shell about-hero">
  <div class="about-hero__identity">
    <div class="eyebrow">About Jim Scott</div>
    {% if portrait_asset %}
    <figure class="about-hero__portrait">
      <img src="{{ '/assets/images/about/jim-scott.webp' | relative_url }}" alt="Portrait of Jim Scott" width="480" height="480" loading="eager" decoding="async">
    </figure>
    {% endif %}
    <h1>Building software, preserving the lessons.</h1>
    <div class="about-hero__intro">
      <p class="about-hero__lede">I’m Jim Scott, a Vice President of Software Engineering who still enjoys working directly with code. I write about software engineering, architecture, open-source tools, and the lessons that survive contact with production.</p>
    </div>
  </div>
  <dl class="about-highlights" aria-label="Professional background at a glance">
    <div><dt>Writing since</dt><dd>2008</dd></div>
    <div><dt>Role</dt><dd>Vice President of Software Engineering</dd></div>
    <div><dt>Focus</dt><dd>Software engineering</dd></div>
    <div class="about-highlights__connect"><dt>Connect</dt><dd>
    {% if site.profile_links %}
    <nav class="about-highlights__links" aria-label="Professional profiles">
      {% for link in site.profile_links %}
        <a href="{{ link.url }}" rel="me">
          {% if link.title == 'GitHub' %}
          <svg class="about-hero__icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">
            <path d="M12 .3C5.37.3 0 5.67 0 12.3c0 5.3 3.44 9.8 8.2 11.38.6.11.82-.26.82-.58v-2.04c-3.34.73-4.04-1.42-4.04-1.42-.55-1.38-1.34-1.75-1.34-1.75-1.09-.75.09-.73.09-.73 1.2.09 1.84 1.24 1.84 1.24 1.07 1.83 2.81 1.3 3.49.99.11-.77.42-1.3.76-1.6-2.67-.3-5.47-1.34-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.53-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6.01 0c2.29-1.55 3.3-1.23 3.3-1.23.65 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.6-2.8 5.63-5.48 5.92.43.37.82 1.1.82 2.22v3.29c0 .32.22.7.83.58A12 12 0 0 0 24 12.3C24 5.67 18.63.3 12 .3Z"/>
          </svg>
          {% elsif link.title == 'LinkedIn' %}
          <svg class="about-hero__icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">
            <path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.37V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12ZM6.99 20.45H3.68V9h3.31v11.45ZM22.23 0H1.77C.79 0 0 .77 0 1.73v20.54c0 .96.79 1.73 1.77 1.73h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0h.01Z"/>
          </svg>
          {% endif %}
          {{ link.title }} <span aria-hidden="true">↗</span>
        </a>
      {% endfor %}
    </nav>
    {% endif %}
    </dd></div>
  </dl>
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

  </article>

</section>


<section class="shell about-feature-section" aria-labelledby="about-projects-heading">
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

<section class="shell about-feature-section" aria-labelledby="about-writing-heading">
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
