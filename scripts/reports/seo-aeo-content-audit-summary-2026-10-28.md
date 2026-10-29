# Coding blog: SEO, AEO, accessibility and content-quality baseline

**Audit date:** 2026-10-28 (America/Los_Angeles)  
**Source repository:** `infoconex/coding-blog`, branch `main`  
**Source snapshot:** `756d345c9996dd1a778ae4e85f26df4349147c6c` (article reads pinned to this commit)  
**Inventory:** [103-article CSV](seo-aeo-article-baseline-2026-10-28.csv)

## Scope and limitations

The report evaluates all 103 identified published article `post/YYYY/MM/DD/*/index.md` source files. Each row includes the source path, published URL, original date, approximate prose word count, technical and content-review findings, and a triage priority. Word counts are estimates, not editorial quality targets.

The checks are source-level screening, **not a complete rendered-site audit or independent factual review**. Descriptions flagged for review are not necessarily invalid. HTTP and legacy-documentation URLs are **unverified review candidates**, not confirmed broken links. The audit did not establish live HTTP status for every external URL or exhaustively inspect every article's technical correctness. The automated inventory does not assert that structured data is correct on every deployed article.

Priorities are heuristic and should be adjusted for technical substance, search relevance, archival importance, and cost of change. Preserve original dates, source code, historical claims, redirects, and permalinks.

## Source-level findings

| Metric | Articles |
|---|---:|
| Published article files | **103** |
| Articles with missing/weak section headings (screening) | 16 |
| Descriptions requiring editorial review | 10 |
| Articles with empty topical tags | 40 |
| Contextual internal-link opportunities | 19 |
| Articles with code-block labeling issues | 2 |
| Articles with empty/missing image alt text identified | 0 |
| Articles with external reference review candidates | 13 |
| Articles with notable content improvement opportunities | 21 |
| Duplicate titles identified | 0 |
| Additional H1 headings in article bodies | 0 |
| High / Medium / Low automated priority | **7 / 19 / 77** |

**Not yet independently verified:** duplicate description text across all 103 pages; absolute canonical tags and social image accessibility in deployed HTML; HTTP status of all external URLs; all article structured-data nodes; exact rendered heading and table accessibility; actual Google/Bing indexing and AI citations.

## First editorial shortlist (technical value, not just automated score)

1. **Understanding .NET Reference Types and Value Types (2009).** Long, useful C# tutorial with no section headings or topic tags in the baseline. Important technical-review caveat: simplified claims that value types are always on the stack and reference types on the heap should be checked against authoritative CLR documentation before any correction; preserve the original as a historical source.
2. **C# Ping (2009).** Original ICMP/Wireshark debugging anecdote, real code, related to the traceroute utility. Label the console example and link the related investigation.
3. **C# Traceroute using .NET Framework (2009).** Distinct, original C# example; improve truncated summary, add tags, link the companion article. Preserve historical code unchanged.
4. **ASP.NET CustomValidator with server/client validation (2010).** Practical code and useful search intent. Existing headings and alt text look improved; verify 17 historical HTTP documentation references individually, without mechanically changing archival links.
5. **How do I open a file that is in use in C#? (2009).** Focused troubleshooting answer, with opportunities for section headings, tags, and authoritative modern references if verified.
6. **Spawning multiple .NET delegates really slow (2008).** Original performance investigation with enduring relevance. Distinguish original observations from current runtime expectations; preserve benchmark and date.
7. **BIND DNS: multiple views on primary and secondary servers (2010).** Substantial technical configuration tutorial; review accuracy/security context, topical tags, and navigable sections.
8. **Running FSCK on an LVM using Linux rescue media (2012).** High reader value and operational risk: prioritize clear historical context, safe terminology, and careful source-backed caveats before touching commands.
9. **How to Test a New .NET SDK Without Installing It System-Wide (2026).** Strong direct connection to current engineering projects and follow-up SDK articles; review description length and contextual links.
10. **Too Hot to Handle? Testing NuGet's New Package Cooldown (2026).** Original reproducible experiment with potential citation value; verify that key findings and limitations remain prominent and accurately sourced. This article has no major source-level defect in the screening.

## Implemented initial article group

The following low-risk improvements were committed to `main` after the baseline (the baseline CSV intentionally remains unchanged):

- `post/2009/01/12/C-Ping-and-Traceroute/index.md`: add targeted tags, semantic section headings, a `text` label on console output, and a direct link to traceroute.
- `post/2009/01/14/C-Traceroute-using-net-framework/index.md`: replace an ellipsis-truncated description with a faithful one, add topic tags and a heading, and link the companion Ping article.
- `post/2009/03/20/Understanding-NET-Reference-Types-and-Value-Types/index.md`: improve description and tags, add section headings, and preserve the historical ASCII diagram in a `text` code block.

Article publication dates, original C# code, canonical historical paths and technical assertions were preserved in this batch.

## Shared structured-data and deployment review

- `_config.yml` uses `seo.type: BlogPosting` for the `post` directory, appropriate because migrated articles are pages rather than `site.posts`.
- `_layouts/default.html` invokes `{% seo title=false %}`, and restricts its additional `ProfilePage` JSON-LD to the About page. Avoid adding another BlogPosting block.
- `_layouts/post.html` has one layout-owned article H1, a historical notice for articles older than five years, and related-content navigation.
- Confirm, using rendered production HTML, the actual `headline`, `description`, `author.url`, `datePublished`, `dateModified`, image URL and canonical URL; the source alone cannot prove these outputs.
- Modification dates should be provided only for meaningful changes. Verify that the current visible `page.updated` field agrees with the SEO plugin's documented `seo.date_modified` field when both are present. Do not update original `date`.
- The Pages workflow has a `continue-on-error: true` social-card generation step. Review whether missing generated cards can leave broken Open Graph image URLs, ideally via a nonblocking artifact check first.

## Recommended ongoing validation

**Implemented after the baseline:** Existing `scripts/validate.py` now rejects an author-authored article H1 that would duplicate the shared article heading, and warns on duplicate normalized meta descriptions. The already-running `scripts/test_validate_historical_links.py` suite now covers H1 behavior in Markdown, HTML, and fenced code. No new workflow or dependency was introduced.

Prefer extending `scripts/validate.py` and `.github/workflows/validate.yml`. Potential **errors**: duplicate permalink, missing required metadata, absent linked local image, malformed fences, broken internal historical URLs, or a body H1 that duplicates the layout-owned H1. Potential **warnings**: duplicate description text, missing useful tags, generic alt text, unlabeled code blocks, sparse headings in lengthy technical material, and review-candidate external HTTP URLs. Avoid arbitrary minimum word counts.

**Remaining work:** inspect any duplicate-description warnings from the updated validator; verify rendered article structured data and social cards; live-test external links; review the next editorial batch; run and verify Actions/deployment; add targeted warnings and tests to existing validation. Do not report these as completed until independently confirmed.
