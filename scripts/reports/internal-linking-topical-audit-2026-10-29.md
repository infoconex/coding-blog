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
