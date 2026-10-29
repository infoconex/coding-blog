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

## Implemented second article group — 2026-10-29

These articles received focused changes on `main` after the unchanged 103-article baseline:

- `post/2008/10/14/Spawning-multiple-NET-delegates-really-slow/index.md`: more precise description, .NET/ThreadPool/concurrency tags, historical context, and an exact follow-up link to the 2008 .NET 2.0 SP2 installation article.
- `post/2009/04/21/How-do-I-open-a-file-that-is-in-use-in-C/index.md`: two descriptive H2 headings, C# file-I/O/log4net tags, current Microsoft FileShare documentation, a source-backed warning that sharing flags cannot override an existing exclusive file handle, and a contextual link to the file-stream article.
- `post/2010/04/26/Bind-DNS-e28093-Configuring-multiple-views-on-primary-and-secondary-DNS-servers/index.md`: split-DNS tags, historical deployment caveat with authoritative ISC guidance, non-clickable example hostnames, and fenced secondary ACL examples.

Re-read all three files from `main` after the commits and verified required date/permalink fields, nonempty tags, balanced Markdown code fences and absence of article-authored H1 headings. Original fenced code examples were preserved. The report's baseline rows remain a record of the pre-improvement snapshot, not a current-state scan.

**Verification boundary:** The GitHub connector returned no combined status contexts on the latest commit; it does not expose push-triggered Actions runs through its available run lookup. Public GitHub Actions and site pages were inaccessible through the browsing tool, so GitHub Actions, Jekyll build and production deployment are still **unverified**, not claimed successful.

## Implemented third article group — 2026-10-29

Three additional articles were improved on `main`, with their original dates, permalinks and original technical examples retained:

- `post/2012/10/12/Running-FSCK-on-an-LVM-(Logical-Volume-Manager)-using-Linux-Rescue-Disk/index.md`: added Linux/LVM/recovery tags; organized the rescue steps under meaningful headings; preserved the original `fsck` invocation as a code block; added prominent safety and historical-context guidance based on Red Hat's filesystem-repair documentation. The original account remains intact, but the commands are explicitly **not** presented as a universal modern procedure.
- `post/2010/10/11/ASPNET-CustomValidator-that-validates-multiple-controls-using-both-Server-Side-and-Client-Side-scripting/index.md`: replaced **16 obsolete MSDN API links** with corresponding Microsoft Learn .NET Framework API references; updated jQuery to HTTPS; emphasized server-side `Page.IsValid` checks and the fact that Web Forms is not ASP.NET Core. Original ASPX, C# and JavaScript code was preserved. Representative Microsoft Learn references were verified; this is not a claim that every link was independently checked end-to-end.
- `post/2008/11/03/NET-20-SP2-Installation-Were-to-find-it/index.md`: improved descriptive metadata and topic tags, converted the historical April 2009 update to a semantic H2, and linked back to the original .NET delegate/ThreadPool investigation.

The post-change source review confirmed that all three retain their original date/permalink fields and balanced code fences, with no additional article-body H1.

### New nonblocking prevention check

Extended the existing `scripts/validate.py` to **warn** on fenced code blocks without a language identifier; Kramdown `{: data-lang="..." }` attributes remain supported. Added four regression tests to the existing `scripts/test_validate_historical_links.py` suite. The validator now distinguishes these editorial warnings from the existing hard errors that fail publishing. The existing GitHub Actions workflows were not duplicated or modified. Actions and deployment results are not independently confirmed.

**Running total: nine articles improved across three groups.** The 103-article inventory CSV remains an unmodified **baseline**, rather than being overwritten after each article edit.

**Limited production spot check (2026-10-29):** The live November 3, 2008 .NET 2.0 SP2 article visibly contains this group’s new description, topic tags, April 2009 H2, and related link. Retrieved copies of the LVM and ASP.NET pages were cached from an earlier state, so they did not establish those pages’ latest deployed state. The connected GitHub API exposes no push-triggered Actions run result through the available methods; complete deployment status and validation therefore remain unverified.


## Implemented fourth article group — 2026-10-29

Four additional articles were updated directly on `main`. These edits preserve their original publication dates, permalink frontmatter, code examples, and image references:

- `post/2010/01/16/(MVP)-Model-View-Presenter-Passive-View/index.md`: rewrote the content description to reflect a concrete C# Windows Forms refactoring, added five topic tags and descriptive H2/H3 navigation through view/presenter setup and mock-based unit tests, changed three original Martin Fowler references to HTTPS, and linked the 2008 design-pattern and 2013 Strategy/Factory Method articles. Verified both Martin Fowler pattern destinations publicly.
- `post/2009/11/26/Automatically-attaching-VHD-files-in-Windows-7-and-Windows-2008/index.md`: added Windows/DiskPart/automation tags and three useful H2 headings, with a historical caveat and authoritative Microsoft references for current DiskPart commands and Task Scheduler run-level considerations. All nine images and the original DiskPart script remain unchanged.
- `post/2010/01/04/ASPNET-MVC-Tutorials/index.md`: improved the description and ASP.NET MVC 2-focused tags, introduced three semantic section headings, replaced a generic 'older versions' document link with Microsoft's specific MVC 1/2 archive and MVC 2 overview, and connected the article to the Passive View walkthrough.
- `post/2008/10/14/Object-Oriented-Design-Patterns/index.md`: added topical tags and a short follow-up section linking the author's subsequent hands-on MVP and Strategy/Factory Method examples.

All four were independently fetched from `main` after the edits. Source verification found no new article-level H1, missing frontmatter date/permalink, or unbalanced fenced code blocks; the original MVP's seven code blocks and five screenshots, and the Windows VHD post's nine images were preserved. Updated Microsoft and Martin Fowler reference destinations were located and opened. **Running total: 13 articles improved.** The original 103-row CSV remains the unchanged baseline.

### Structured data — source-level findings, not rendered certification

- The site config sets `seo.type: BlogPosting` for migrated article pages; the default layout invokes `{% seo title=false %}`. Official jekyll-seo-tag documentation confirms support for this type and the `seo.date_modified` override.
- `_data/authors.yml` maps the author string `Jim Scott` to a `Person` record with the About URL, consistent with the SEO plugin's documented author lookup. This is better than relying only on the global author's URL, but rendered JSON-LD still requires checking.
- At the time of this editorial group, the shared post layout displayed `page.updated`, while jekyll-seo-tag used `seo.date_modified`, `last_modified_at`, then `date`; the fifth group subsequently aligned the visible update field with the plugin's metadata. Do not automatically mark the historical publication date as new.
- At the time of this review, `_layouts/default.html` unconditionally emitted Open Graph and Twitter image tags after `{% seo %}`; the fifth group later made these conditional. The SEO plugin may also emit image tags when articles specify `image:`, so **possible duplicate social image metadata** must be checked in generated HTML before changing the shared template.
- Production pages and GitHub Actions runs were not accessible to the available independent retrieval method in this pass. The four commits are present on `main`; actual Pages deployment, rendered schema, and workflow execution remain unverified.

## Implemented sixth article group — 2026-10-29

Four further articles were updated on `main`, bringing the cumulative editorial improvements to **17 of 103 articles**. The audit CSV continues to capture the original 2026-10-28 baseline; it is not rescored automatically.

| Article | Focused change | Preserved |
| --- | --- | --- |
| `post/2012/12/05/Calling-WCF-Service-using-LINQPad/index.md` | Added sections and WCF configuration tags; upgraded LINQPad link to HTTPS; explained why a class-library proxy configuration was not found by the query host; linked the official LINQPad FAQ and Microsoft WCF client documentation. Clarified LINQPad 5's F4 per-query app.config alternative without claiming it applied to every version. | Original two XML examples, date, permalink |
| `post/2010/07/27/ASPNET-MVC3-Preview-1-Released-Today/index.md` | Added MVC/Razor/dependency-injection tags, section headings, an official Microsoft MVC 3 overview, and a link to the earlier MVC 2 article. Corrected the historical interface spelling `IValidateObject` to `IValidatableObject`, as explicitly documented by Microsoft. | Original 2010 preview context, date, permalink |
| `post/2009/11/27/HP-MediaSmart-Server-is-my-favorite-device-for-2009/index.md` | Replaced truncated description, added Windows Home Server/backup tags, historical-hardware context and a warning against exposing unsupported home servers publicly. Updated three product links from HTTP to HTTPS without changing their affiliate paths or claiming they remain available; repaired two run-together labels. | Original firsthand review, seven images, date, permalink |
| `post/2026/01/01/all-progress-depends-on-the-unreasonable/index.md` | Replaced the title-only meta description with a content-specific summary and added two navigable section headings. | Original leadership essay, date, permalink |

All four were fetched from `main` after editing, confirming dates and permalinks, relevant tags, balanced code fences, and no article-authored H1s. Metadata descriptions range from **150 to 161 characters**. All newly examined article-body links use HTTPS or root-relative URLs; no live HTTP status was established for every external destination. Official LINQPad and Microsoft Learn references were checked.

**Deployment and structured-data limits:** Production article pages and public Actions run details were not independently retrievable through the available web tools. The generated HTML SEO scanner remains committed and its unit tests are in the standard validation workflow, but the scanner was **not yet wired to the Pages built-site step at the time of that batch** (a later nonblocking integration is recorded in the seventh group). Do not treat this source-level review as proof of successful deployment, canonical metadata or rich-result eligibility.

## Implemented fifth group — shared social metadata and SEO validation — 2026-10-29

After reviewing the **actual upstream Jekyll SEO Tag Liquid template** (`jekyll/jekyll-seo-tag/lib/template.html`) alongside `_layouts/default.html`, duplicate metadata was confirmed at the source level:

- The plugin always emits `twitter:card`. Previously, our layout emitted a second `twitter:card`.
- When an article declares `image` in frontmatter, the plugin emits `og:image`, `twitter:image`, and corresponding image metadata. Previously, the layout emitted a second, sometimes conflicting, image URL based on the separate generated social-card path.
- The default layout has been updated to **let the plugin own image metadata when `page.image` exists**. For older articles without explicit `image` frontmatter, the layout continues emitting its fallback `og:image` and `twitter:image`, with descriptive image-alt metadata. The custom `twitter:card` tag was removed everywhere to avoid duplication.
- **Tradeoff:** the plugin emits a `summary` card for posts without explicit `image` frontmatter, rather than the former manually added `summary_large_image` card. Their fallback `twitter:image` remains. Evaluate previews before choosing an approach that supplies plugin-owned images for every historical article; do not reintroduce duplicate metadata solely to force large cards.
- `_layouts/post.html` now renders visible update dates from `page.seo.date_modified` (or `page.last_modified_at`) to match the SEO plugin's documented modification-date precedence. A historical article does not receive an automatic new `dateModified` merely because its source was migrated or formatted. The original publication date is unchanged.

Added `scripts/validate_seo.py`, an offline inspection tool for **built Jekyll HTML**, checking single canonical and social-image tags, matching canonical/OG/schema URLs, and one `BlogPosting` JSON-LD node with headline, description, dates, and identifiable author on article pages. It also considers extensionless post files and ignores bare redirect pages. Added `scripts/test_validate_seo.py` covering positive, duplicate, author, schema, redirect, and extensionless-file cases. These unit tests are wired into the **existing** `.github/workflows/validate.yml` validation job.

**Important limitation:** The attempt to add `scripts/validate_seo.py --site-dir _site` to the **Pages build workflow** was blocked by the GitHub connector's safety check. At the time, the rendered-site scanner was **not automatically invoked during Pages deployment**. The seventh group subsequently added nonblocking diagnostic invocation through the already-executed image-validation script. It can be run manually after a Jekyll build, but no built-site scan, regression-test execution, GitHub Actions result, or production HTML validation has been independently verified in this pass. The source-level conflict and its conditional fix are verified; production is not certified. The existing Pages workflow was left unchanged.

The article-improvement total remains **13 of the 103 original published articles**; these commits concern the common layout and validation coverage, not additional editorial article rewrites.

## Seventh group — automatic, nonblocking rendered SEO diagnostics — 2026-10-29

**Purpose:** Close gaps in the generated-HTML checker and put its results into an existing post-build Actions log without editing the Pages deployment workflow.

- `scripts/validate_seo.py`: fixed a false-negative where a rendered article with **neither** a canonical link **nor** an `og:url` could be silently skipped. Source-path detection now distinguishes genuine historical article output from lightweight redirect pages. The scanner also verifies that same-site `og:image` and `twitter:image` references point to files present in the generated `_site` directory (including generated social-card fallbacks).
- `scripts/test_validate_seo.py`: now covers the new missing-metadata and missing-asset cases, a historical post redirect, and successful article output with an actual local social-card fixture. Nine SEO scanner tests are present in source.
- `scripts/validate_images.py`: the existing **post-Jekyll-build image validation** now invokes the SEO scanner and prints its page/article totals and individual findings as `SEO WARNING` messages. **SEO findings do not block deployment at this stage**; the existing image/accessibility errors still fail as before.
- `scripts/test_validate_images.py`: added a regression test that verifies SEO warnings are visible while an otherwise clean image audit succeeds.
- `.github/workflows/pages.yml` remains unchanged: it **already runs `scripts/validate_images.py --site-dir _site` after the Jekyll build**, so these diagnostics should be visible in that step's logs on the next successful run. This is not yet a fail-on-SEO-error gate.

**Verification boundary:** Committed source and test fixtures were reviewed; no complete Jekyll site build or GitHub Actions log has been independently retrieved or executed here. Consequently, the number and severity of actual rendered SEO findings are **unknown**. Before promoting the SEO scan to deployment-blocking enforcement, inspect the next build log and resolve any true positives and false positives. The separate `python3 scripts/validate_seo.py --site-dir _site` command remains available to fail an intentional manual/local audit.

This change does not add or update article publication dates, change historical routes, or submit any URLs to IndexNow. **17 of 103 articles** remain the total edited in the baseline review series.

## Shared structured-data and deployment review

- `_config.yml` uses `seo.type: BlogPosting` for the `post` directory, appropriate because migrated articles are pages rather than `site.posts`.
- `_layouts/default.html` invokes `{% seo title=false %}`, and restricts its additional `ProfilePage` JSON-LD to the About page. Avoid adding another BlogPosting block.
- `_layouts/post.html` has one layout-owned article H1, a historical notice for articles older than five years, and related-content navigation.
- Confirm, using rendered production HTML, the actual `headline`, `description`, `author.url`, `datePublished`, `dateModified`, image URL and canonical URL; the source alone cannot prove these outputs.
- Modification dates should be provided only for meaningful changes. The fifth group updated the visible timestamp source to `page.seo.date_modified`, falling back to `page.last_modified_at`; verify the rendered output when explicitly set. Do not update original `date`.
- The Pages workflow has a `continue-on-error: true` social-card generation step. Review whether missing generated cards can leave broken Open Graph image URLs, ideally via a nonblocking artifact check first.
- **Updated after this baseline:** the earlier unconditional social-image markup has been changed to a conditional fallback when `page.image` is absent, and the custom `twitter:card` tag has been removed. The upstream plugin is the sole source of image tags when frontmatter specifies an image. Production proof still requires examining built HTML.

## Recommended ongoing validation

**Implemented after the baseline:** Existing `scripts/validate.py` now rejects an author-authored article H1 that would duplicate the shared article heading, and warns on duplicate normalized meta descriptions. The already-running `scripts/test_validate_historical_links.py` suite now covers H1 behavior in Markdown, HTML, and fenced code. No new workflow or dependency was introduced.

Prefer extending `scripts/validate.py` and `.github/workflows/validate.yml`. Potential **errors**: duplicate permalink, missing required metadata, absent linked local image, malformed fences, broken internal historical URLs, or a body H1 that duplicates the layout-owned H1. Potential **warnings**: duplicate description text, missing useful tags, generic alt text, unlabeled code blocks, sparse headings in lengthy technical material, and review-candidate external HTTP URLs. Avoid arbitrary minimum word counts.

**Remaining work:** inspect any duplicate-description warnings from the updated validator; verify rendered article structured data and social cards; live-test external links; review the next editorial batch; run and verify Actions/deployment; add targeted warnings and tests to existing validation. Do not report these as completed until independently confirmed.
