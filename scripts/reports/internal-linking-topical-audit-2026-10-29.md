# Contextual internal links and topical discovery — 2026-10-29

## Scope and baseline

Analyzed the 103 rendered articles from the successful GitHub Pages Run #503 artifact (commit `15dfb4830a041246a070231508e084f88c39a5cf`). Links were measured inside each article's `.post-content` element; global navigation, chronologically adjacent articles, series controls, and automatically generated related-reading cards were counted separately. Only links resolving to another one of the 103 article canonical paths count as contextual article links.

| Baseline metric | Articles/links |
| --- | ---: |
| Published articles | 103 |
| Contextual article-to-article hyperlinks | 35 |
| Articles containing a contextual link to another article | 21 |
| Articles with zero contextual outgoing article links | 82 |
| Articles with zero incoming contextual article links | 75 |
| Articles with neither incoming contextual nor incoming related-card links | 51 |
| Articles with outgoing related-reading recommendations | 65 |
| Articles without related-reading recommendations | 38 |
| Links rendered in related-reading cards | 182 |
| Series sidebar/navigation links | 34 |
| Chronological article navigation links | 162 |

The existing template provides dynamic tag-based related reading (maximum three, newest first), chronological post navigation for non-series articles, and ordered navigation for four explicitly curated series. These are valuable but are not substitutes for human-written links clarifying the relationship between two article topics. Tag differences and many empty historical tags explain why a portion of the archive lacks generated related cards; automated tag mass-assignment was intentionally avoided.

## Changes made

Added one clearly identified **Further reading** or **Related history** section to **12 existing articles** with **22 validated internal article links** across four topical clusters:

* **.NET platform evolution:** .NET Core 1.0 (2016), 2.0 (2017), 3.0 (2019), .NET 6 (2021), and .NET 8 (2023); link the progression in both directions and connect .NET 8's platform maturity to a practical 2026 isolated-SDK evaluation guide.
* **BlueQuartz/BlueOnyx:** the 2008 BlueQuartz Mono tutorial, the 2009 Cobalt-to-BlueOnyx platform history, the 2011 OpenWebmail walkthrough, and the 2016 Roundcube walkthrough. Added historical-context cautions; these links do not endorse obsolete installation steps as current.
* **Design patterns:** the 2013 Strategy and Factory Method C# example connects backward to the 2008 introductory patterns article and forward to the 2025 SOLID introduction, while distinguishing design patterns from principles.
* **AI engineering:** the November 2022 ChatGPT first-impressions article and the August 2026 human-oversight article connect both ways, with a pointer to the AI Flywheel Spec for an implementation-oriented next step.

Each link target was checked against an existing `post/YYYY/MM/DD/<slug>/index.md` source path before committing. All links are root-relative and use the exact historical permalink casing and spelling. Sections are deliberately additive: original article body, commands, code examples, headings, dates, front matter, titles, and canonical URLs are unchanged. No new content templates, Jekyll dependencies, navigation rules, indexing submissions or GitHub Actions jobs were introduced.

## Quality controls and verification boundary

Existing `scripts/validate.py`, historical link checks, SEO quality gate, sitemap/crawlability gate, image validator, and browser-security checks must pass for deployment. The post-build artifact should be re-examined to confirm all new links rendered, resolve to canonical article pages, and the article graph improved as intended.

This is a relevance-based editorial pass, **not** a promise of ranking or indexing gains. Do not automatically add links across all historical posts or force broad tag merges merely to increase link counts. Search engines and AI answer engines can discover content through the sitemap and existing navigational links even when there is no contextual link; prioritize reader relevance over artificial quotas. A future small pass can assess other genuinely connected topic pairs based on user interest and search evidence.

## Post-deployment verification — completed

GitHub Pages [Run #506](https://github.com/infoconex/coding-blog/actions/runs/40914316680) on commit `1d84be34ae152f02a325c6732625e3a07f199337` **succeeded**: content validation, dependency/source-security checks, Jekyll build, mandatory SEO and crawlability checks, generated images, browser security, Pages deployment, and IndexNow notification all passed. The standalone [validation run #537](https://github.com/infoconex/coding-blog/actions/runs/40914316364) also succeeded.

Downloaded the **Run #506 generated Pages artifact** and compared every one of the **103** article `.post-content` sections with the pre-change Run #503 artifact. For every article, the original rendered content is an unchanged prefix of the new content. All newly added article URLs resolve to canonical pages in the generated artifact; no original contextual links were lost.

| Measured item | Pre-change Run #503 | Post-change Run #506 |
| --- | ---: | ---: |
| Contextual article-to-article links | 35 | **57** |
| Articles with outbound contextual article links | 21 | **33** |
| Articles with no outbound contextual article links | 82 | **70** |
| Articles with no inbound contextual article links | 75 | **65** |
| Articles with no inbound contextual or incoming related-reading links | 51 | **47** |
| Related-reading card links | 182 | **182** (unchanged) |
| Total published article pages | 103 | **103** |

The difference is **exactly 22 new source-to-destination links across exactly 12 edited articles**. Every new link and source was enumerated and validated against the 103 generated canonical article paths. This is a confirmed structural improvement to the site link graph, not a claim that search engines have indexed the pages or that rankings have improved. No broad additional linking pass is recommended until further topical priorities or search evidence emerge.
