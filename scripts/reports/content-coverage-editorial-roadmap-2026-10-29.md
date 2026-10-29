# Content quality, topical coverage, and evidence-based editorial roadmap

**Date:** 2026-10-29  
**Website:** https://coding.infoconex.com/  
**Repository:** infoconex/coding-blog, \`main\`  
**Baseline reviewed:** 103 articles in the successful GitHub Pages Run [#506](https://github.com/infoconex/coding-blog/actions/runs/40914316680) generated artifact, \`search.json\`, rendered HTML, series pages, and selected original article Markdown. Previous [SEO/AEO audit](seo-aeo-content-audit-summary-2026-10-28.md) and [internal-linking study](internal-linking-topical-audit-2026-10-29.md) were consulted. Counts below refer to the artifact, **not** search-engine performance data.

## Executive finding

The best next investment is **original, reproducible engineering work that extends existing article sequences**, not generic SEO text expansion. The 2008–2024 archive includes many short news and troubleshooting posts whose historical context is the point. By contrast, 2025–2026 writing demonstrates repeatable investigations, code, commands, tradeoffs, and supporting repositories. Preserve that distinction.

**Recommended next article:** *Before You Upgrade .NET: Build a Dependency Inventory You Can Verify* (working title). This directly fulfills a stated next step in the existing "Staying Current with .NET" sequence. **Do not publish the article until a real repository, inventory command output, and validation experiment exist.**

A strong second article can be written from **already completed evidence**: *How I Made SEO Validation a Deployment Gate for GitHub Pages*. The published blog-rebuild article describes the migration, but does not cover the tested rendered-HTML enforcement, failure handling, and sitemap/canonical cross-checks now implemented in this repository.

## Catalog inventory and interpretation

| Measured signal | Result | Interpretation |
| --- | ---: | --- |
| Total published articles in \`search.json\` and generated HTML | 103 | Source catalog and generated-site count agree |
| Published during 2008–2016 | 61 | Early historical archive, many event/news items |
| Published during 2017–2024 | 13 | Occasional platform and personal observations |
| Published during 2025–2026 | 29 | Newer, more in-depth technical series |
| Published in 2026 | 23 | Recent focus is developer tooling, AI, .NET and GitHub |
| Median rendered article word count, all years | ~394 | Text-only estimate; not a quality score |
| Median, 2008–2016 | ~244 | Appropriate to many period-specific notes |
| Median, 2017–2024 | ~240 | Mix of short commentary and announcements |
| Median, 2025–2026 | ~1,186 | More structured, hands-on reporting |
| Articles with fewer than 250 rendered words | 41 | **All pre-2025**; do not automatically expand |
| Articles without an \`h2\` in their body | 47 | Mostly shorter pieces; not automatically a structural error |
| Articles with at least one rendered \`pre\` code block | 43 | Opinion, history and release posts need not have code |
| Articles with no code block | 60 | Not an SEO failure |

*Method:* Word counts are simple word-token estimates from the text of each generated \`.post-content\`; image captions, table text, and code can affect counts. This is not a full editorial line-by-line fact check, original-content detector, search-rank assessment, or engagement analysis. The previous SEO/AEO technical milestone reported zero critical errors or advisory warnings and is not re-opened here.

### Existing curated series

| Series | Rendered article count | Coverage |
| --- | ---: | --- |
| [Staying Current with .NET](https://coding.infoconex.com/series/staying-current-with-dotnet/) | 5 | RC1 upgrade preflight, SDK selection, clean build, isolated SDK testing, SDK management |
| [CopyGitHubRepo](https://coding.infoconex.com/series/copygithubrepo/) | 5 | Safe snapshot creation through v0.4.0 Pages migration |
| [AI Flywheel](https://coding.infoconex.com/series/ai-flywheel/) | 5 | Specification, framework, tests, CLI, project integration |
| [SOLID Principles](https://coding.infoconex.com/series/solid-principles/) | 6 | Introduction and one detailed article per principle |
| **Total curated-series pages** | **21** | Four meaningful topical paths |

**Existing strengths:** In the current .NET series, \`global.json\`, clean environments, isolation boundaries, actual CLI commands, and Microsoft references already receive substantial explanation. The NuGet publication-cooldown post already includes a controlled proof-of-concept, five scenarios, and source repository. The CopyGitHubRepo and AI Flywheel posts already explain planning, tests, authority boundaries and evidence. These are **not gaps** to fill with near-duplicate introductions.

**Historical content treatment:** Articles about events, early release announcements, BlueQuartz/BlueOnyx, obsolete ASP.NET technologies, and early networking code should remain accessible with original dates and examples. Where context is needed, prefer a clearly dated note or an original new retrospective **based on evidence**, rather than quietly revising old material to sound current. Do not unpublish, merge, redirect, bulk retag, or expand 41 short pieces merely to satisfy a word threshold.

## Ranked editorial opportunities

### P1 — .NET dependency inventory before an upgrade

**Working title:** *Before You Upgrade .NET: Build a Dependency Inventory You Can Verify*

**Reader problem:** Which SDKs, workloads, target frameworks, packages, configuration sources and external tooling must be understood *before* comparing .NET 10 and .NET 11 or starting a migration?

**Evidence in existing articles:** [Before You Upgrade .NET, Do You Know What Is Building It?](https://coding.infoconex.com/post/2026/09/16/before-you-upgrade-dotnet-do-you-know-what-is-building-it) covers SDK selection; [Can You Build Your .NET Application on a Clean Machine?](https://coding.infoconex.com/post/2026/09/17/can-you-build-your-dotnet-application-on-a-clean-machine) covers hidden environment state; [How to Test a New .NET SDK Without Installing It System-Wide](https://coding.infoconex.com/post/2026/09/20/how-to-test-a-new-dotnet-sdk-without-installing-it-system-wide) explicitly promises a later application inventory; [Managing .NET SDKs: Installation Was Just the Beginning](https://coding.infoconex.com/post/2026/10/21/managing-dotnet-sdks-installation-was-just-the-beginning) explicitly says the next topic is dependency inventory. This article would become **Part 6** of the existing series, not a new competing series.

**Minimum real-world exercise before publication:**
1. Choose or construct a permission-safe sample .NET repository, with pinned inputs and an explicitly documented SDK environment.
2. Capture source-controlled settings (\`global.json\`, project target frameworks, \`Directory.Build.props\`, \`Directory.Packages.props\`, \`NuGet.config\`, package lockfiles and tool manifests) **only where actually present**.
3. Compare static declared dependencies with what tools resolve, distinguishing direct from transitive package dependencies and host tool installation from repository declarations.
4. Demonstrate at least one real discrepancy (e.g., SDK selection, workload or package source) on a clean environment and its documented resolution.
5. Publish exact command versions, representative verified output, limitations (especially machine-specific state), and a reproducible companion repository or branch.

**Do not** manufacture output, suggest that a dependency inventory automatically proves upgrade compatibility, or conflate package/version selection with build reproducibility. **Status:** highest-priority *next investigation*, **not yet ready to publish**.

### P2 — Real-world rendered-HTML SEO and crawlability gates

**Working title:** *How I Made SEO Validation a Deployment Gate for GitHub Pages*

**Reader problem:** How can a Jekyll/GitHub Pages site prevent broken canonicals, structured data, social cards and sitemap omissions from being deployed?

**New material compared with existing content:** [Out With the Old, In With the New: Rebuilding Coding](https://coding.infoconex.com/post/2026/08/29/out-with-the-old-in-with-the-new-rebuilding-coding) explains the migration, **not** the later post-build enforcement implementation.

**Verified source evidence available now:** \`scripts/validate_seo.py\`, \`scripts/validate_indexability.py\`, fixture tests, \`.github/workflows/pages.yml\`, clean generated-site counts (113 HTML pages/103 articles, 112 sitemap destinations), and successful [Pages Run #505](https://github.com/infoconex/coding-blog/actions/runs/40907202932). Previous initial failed [Run #498](https://github.com/infoconex/coding-blog/actions/runs/40903406563) demonstrates why executable regression tests are needed; explain the corrected \`SplitResult.params\` bug without obscuring it.

**Suggested article sequence:** Why source Markdown checks are insufficient → inspect generated HTML → distinguish redirect/404/indexable pages → critical versus advisory checks → enforce after Jekyll and before Pages upload → demonstrate negative fixture tests → show a successful real build → explain why this does **not** prove live-origin behavior or Google/Bing indexing.

**Cautions:** Avoid implying GitHub Pages supports arbitrary server-side response headers or that zero SEO audit warnings guarantee ranking. Include focused code excerpts with repository links and actual logs. **Status:** evidence **available now**; strong candidate for a standalone practical article.

### P3 — Characterization testing a historical .NET traceroute implementation

**Working title:** *Before Modernizing a 2009 C# Traceroute, Characterize Its Behavior*

**Existing anchor:** [C# Traceroute using .NET Framework](https://coding.infoconex.com/post/2009/01/14/C-Traceroute-using-net-framework), supported by the earlier [C# Ping](https://coding.infoconex.com/post/2009/01/12/C-Ping-and-Traceroute). This offers a compelling historical-to-modern continuity story without replacing the original.

**Practical plan:** Preserve the legacy code as-is; create a separate characterization-test harness (potentially using Verify for approval/snapshot-style testing); isolate non-deterministic networking and timing dependencies; capture golden outputs and failure cases; then modernize in a distinct project. A future cross-platform implementation and alternate presentations should follow characterization, not precede it.

**Cautions:** Real ICMP/network results are unstable across OS, permissions, hosts and time; do not claim deterministic regression tests unless external effects are controlled. Do not promise identical output behavior before tests prove it. **Status:** depends on completing the separately planned project work; **do not publish a hypothetical result**.

### P4 — dotnetup versus Isolated .NET SDK: a reproducible comparison

**Working title:** *Microsoft's dotnetup vs. Isolated .NET SDK: What Does Each Actually Guarantee?*

**Existing anchor:** [Managing .NET SDKs: Installation Was Just the Beginning](https://coding.infoconex.com/post/2026/10/21/managing-dotnet-sdks-installation-was-just-the-beginning), and the public \`isolated-dotnet-sdk\` project referenced there.

**Required evidence:** Record exact compared versions/commit IDs, documented responsibilities and platform support, isolated install vs management operations, selection behavior with \`global.json\`, removal/uninstall boundaries, network failures and failure recovery. Publish a runnable matrix, raw commands, outcomes and environment constraints.

**Cautions:** This is an engineering comparison, not a marketing scorecard. Do not assert current dotnetup capabilities, release status or compatibility without checking the pinned upstream version. **Status:** worthwhile once the existing experimental data is updated and independently reproduced; potentially overlaps P1, so sequence carefully.

### P5 — Evidence-driven AI Flywheel case study

**Working title:** *From AI Specification to Verifiable Change: One Complete Flywheel Run*

**Existing anchor:** [Testing the AI Flywheel Framework with Durable Evidence](https://coding.infoconex.com/post/2026/07/27/testing-the-ai-flywheel-framework-with-durable-evidence) and [From Specification to System: How the AI Flywheel Became Four Projects](https://coding.infoconex.com/post/2026/09/03/from-specification-to-system-how-the-ai-flywheel-became-four-projects).

**Required evidence:** A completed, authorized run with traceable specification, inputs, decisions, test failures and fixes, before/after outputs and review/acceptance artifacts. Explain what the system could *not* establish, including any manual judgment. **Status:** hold until an actual end-to-end case is packaged and safe to publish.

## Do not prioritize without new evidence

* A generic "What is AI?", "What is SOLID?" or "How does GitHub Pages work?" article duplicates existing coverage without a new result.
* Another .NET 11 RC2 release-summary article would duplicate the already published [NuGet publication-cooldown experiment](https://coding.infoconex.com/post/2026/10/22/too-hot-to-handle-testing-nugets-new-package-cooldown) unless there is new experimental evidence.
* A bulk rewrite of short historical announcements would erase context and create unnecessary publication risk.
* SEO-only filler written to target keywords, fabricated first-hand results, guessed benchmark numbers, or fabricated update dates must not enter the archive.

## Reusable acceptance criteria for a new engineering article

The reader should be able to identify the **precise question** and answer early, reproduce critical steps using disclosed versions/prerequisites, inspect actual test output or relevant repository/commit evidence, understand negative cases and limitations, and distinguish observation from opinion. Use descriptive section headings and meaningful figures with accessible alt text when an image clarifies the engineering; do not add decorative figures as a requirement. Check existing posts before introducing another article on the same narrow question. Preserve canonical URLs, avoid rewriting original publication dates, and link to both earlier foundations and the actual proof.

**Publication policy:** This report proposes an evidence-backed editorial queue. No article has been silently drafted as published content, no new permalinks or categories were created, and no speculative source or deployment changes are justified by this review. Consider Search Console and Bing indexing later, once there is enough data to identify specific issues; their absence is not evidence that content needs artificial expansion.

## Milestone decision

**Stop here on content-quality auditing.** The highest value next independent project is **P1: building a reproducible .NET dependency inventory with actual experiments**. P2 can be written from completed GitHub Actions proof without more experiments if an editorial deliverable is preferred. Revisit the remaining candidates when the necessary implementation evidence exists, not simply on a publishing schedule.
