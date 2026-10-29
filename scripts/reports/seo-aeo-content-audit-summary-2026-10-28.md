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

## Milestone: SEO validation guardrails ready for production triage — 2026-10-29

**Implementation is complete enough to pause this chat.** The next independent work item is **production-generated HTML verification and triage of SEO diagnostic warnings**. This is a handoff milestone, not a claim that production is certified.

### Completed and checked in source

- `scripts/validate_seo.py` now detects missing article canonical metadata, duplicate Open Graph/Twitter tags, missing local social images, absent or incomplete `BlogPosting` JSON-LD, and incorrect historical article canonical routes. Checking article identity by built-source path ensures a wrong canonical cannot suppress the schema inspection.
- `scripts/test_validate_seo.py` now contains **11 regression tests**, covering valid pages, duplicate tags, missing author URLs, absent schema, extensionless and `.html` article builds, lost canonical metadata, wrong canonical URL, missing social-card files, and redirects.
- `scripts/validate_images.py` invokes the built-site SEO scanner in **nonblocking** mode after the existing image audit; it prints totals and `SEO WARNING:` lines. Even unexpected scanner exceptions are reported as warnings without failing an otherwise successful image audit.
- `scripts/test_validate_images.py` now has **8 tests**, including verification of visible SEO warnings and exception containment.
- Existing `.github/workflows/validate.yml` already runs both regression test modules, while the unchanged `.github/workflows/pages.yml` already runs `scripts/validate_images.py --site-dir _site` after the Jekyll build. The scanner is therefore connected to the deployment pipeline **indirectly** via that existing step.
- No workflow permissions, IndexNow behavior, publishing dates, historical paths, or article content were changed in this milestone. The original 103-row baseline remains untouched; **17 of 103 articles** were individually improved in preceding groups.

### Limits and stop condition

GitHub app source reads confirm the new methods, test cases, and workflow references exist on `main`. **The test suite has not been executed in this environment** because the complete repository is not mounted in the runtime and no GitHub Actions logs were available through the connected GitHub actions. Public browsing of article HTML or GitHub's workflow pages could not establish the latest deployed rendered metadata. **Do not equate the commits or a zero-context combined commit status with passing CI or a healthy production deployment.**

**Next independent item:** Retrieve the most recent `Deploy Jekyll site to Pages` run, expand the build job's `Verify generated images, clickable image links, and alt text` step, and collect all `SEO diagnostic`/`SEO WARNING` lines. Validate them against the generated `_site` artifact (or representative production pages with raw HTML). Resolve verified issues without changing article dates or permalinks. Only if all diagnostics are accurate and pass, consider a separate change to make critical SEO failures build-blocking. Keep the external-link inventory, remaining article rewrites and AEO editorial work as separate later milestones.

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


## Production-generated HTML verification and diagnostic remediation — 2026-10-29

**Status: Completed for this milestone, with explicit live-origin limitations.**
The previous milestone's unverified workflow state has now been superseded by **actual GitHub Actions logs, two downloaded Pages build artifacts, and a reproducible examination of their generated HTML**.

### GitHub Actions evidence

| Evidence | Before correction (commit `e82722bd`) | After correction (commit `a53e8671`) |
| --- | --- | --- |
| Deploy Jekyll site to Pages | [Run #495](https://github.com/infoconex/coding-blog/actions/runs/40899349304): **success** | [Run #496](https://github.com/infoconex/coding-blog/actions/runs/40901319305): **success** |
| Validate content and security | [Run #526](https://github.com/infoconex/coding-blog/actions/runs/40899349200): **success** | [Validation run](https://github.com/infoconex/coding-blog/actions/runs/40901318649): **success** |
| Generated HTML / article audit | **114 pages / 103 articles** | **113 pages / 103 articles** (one canonical redirect now excluded) |
| SEO diagnostic warnings | **5** | **0** |
| Rendered image audit | **46**, no broken local images or alt-text failures | **46**, no broken local images or alt-text failures |
| SEO regression suite | **11/11 passed** | **15/15 passed** |
| Image validator regression suite | **8/8 passed** | **8/8 passed** |
| Built-page browser security checks | **114 HTML files**, passed | **114 HTML files**, passed |
| Pages deployment | **success** | **success** |

Logs were retrieved from the actual `build` and `validate` jobs, including the step **Verify generated images, clickable image links, and alt text**. No unexpected SEO scanner exceptions or image-validation errors appeared. The pre-fix Jekyll artifact was GitHub Actions artifact **12906944815**; the corrected build artifact was **12909182798**. Both artifacts were downloaded and inspected rather than inferred from commits or green status indicators.

### Full rendered HTML inspection

The pre-fix built artifact contained **114 HTML files**: 113 canonical-bearing content files and one legacy redirect. An independent parser inspection of the generated HTML found:

- Exactly one canonical URL on each of the 113 content files, all with the expected `https://coding.infoconex.com` host, and no repeated canonical destinations.
- Exactly one each of `og:url`, `og:image`, `twitter:image`, `twitter:card`, and `description` on those files; no empty HTML `<title>` elements.
- **103 BlogPosting JSON-LD nodes**, matching their article canonical URLs; all publication and modification dates were parseable. **102** already had `Jim Scott` and the correct `/about/` profile URL. One historical article had `johnscott` and lacked a public author profile.
- Exactly one About-page `ProfilePage` JSON-LD node. Its `mainEntity` identifies Jim Scott, his About URL, portrait, Vice President of Software Engineering role, and external profiles.
- No unexpected `robots`, `googlebot`, or `bingbot` index directives on the 113 content files. The redirect deliberately has `noindex, follow` and a canonical to `/about/`.
- Local social image references were present in the generated artifact, as independently checked by the build-time SEO and image scanners. This is not a claim that third-party crawlers always fetch or display those images.

Representative generated URLs specifically inspected (title, description, canonical, social metadata, JSON-LD when relevant, dates, indexing metadata, and relevant image references):

| Type | URL |
| --- | --- |
| Homepage | https://coding.infoconex.com/ |
| Author About / ProfilePage | https://coding.infoconex.com/about/ |
| Writing collection | https://coding.infoconex.com/writing/ |
| Writing archive | https://coding.infoconex.com/archive/ |
| Historical article without explicit banner | https://coding.infoconex.com/post/2009/01/14/C-Traceroute-using-net-framework |
| Recently improved historical article | https://coding.infoconex.com/post/2009/04/21/How-do-I-open-a-file-that-is-in-use-in-C |
| Historical screenshot-rich article | https://coding.infoconex.com/post/2009/11/26/Automatically-attaching-VHD-files-in-Windows-7-and-Windows-2008 |
| Historical guest-authored article with image | https://coding.infoconex.com/post/2010/01/16/Visual-Studio-CloudService-app-Build-fails-Unable-to-remove-directory |
| Modern article with banner | https://coding.infoconex.com/post/2026/10/24/my-github-projects-needed-a-home-so-i-built-one |
| Modern NuGet research with banner | https://coding.infoconex.com/post/2026/10/22/too-hot-to-handle-testing-nugets-new-package-cooldown |

Public web crawler retrieval additionally corroborated visible content on the homepage, About, writing, archive, the October 24 project article, and the improved April 2009 file-access article. Some web crawler results were stale or inaccessible. **Raw HTTP response headers, live-origin HTML bytes for all 113 pages, Google/Bing indexing outcomes, and social-preview rendering were not independently established.** The authoritative rendered-markup evidence in this milestone is the deployed GitHub Pages build artifact from successful run #496; do not confuse that with a complete independent live-site crawl.

### Five warnings resolved

1. **Four false positives on `author/jscott/index.html`** — The `jekyll-redirect-from` page has an intentional canonical to `/about/`, a meta-refresh, and `noindex, follow`; redirect pages need no Open Graph or Twitter cards. The scanner formerly skipped only redirects with no canonical. It now excludes explicitly identified redirect pages even when they include the destination canonical. Added a canonical-redirect regression fixture.
2. **One real author-identification issue on the January 16, 2010 Azure/Visual Studio article** — Frontmatter retains the original historical author key `johnscott`; the article is signed **John**. Since this byline did not match `_data/authors.yml`, the built BlogPosting contained the unhelpful display name `johnscott` and no `author.url`. Added a mapping from `johnscott` to **John Scott**, derived from the byline identifier and signature, and made the shared post layout show mapped author names. The corrected build artifact confirms both visible byline and schema now say **John Scott**. **No independent public author profile was verified, so none was invented and the article was not falsely attributed to Jim Scott.** Identity corroboration beyond the original byline is still a possible historical editorial follow-up.
3. **Refined author validation** — A populated author name is required. For the primary author `Jim Scott`, the validator still requires the correct `https://coding.infoconex.com/about/` profile URL. For a historical guest without an identified public profile, `author.url` is advisory rather than mandatory. Added tests for permitted guest name-only metadata, unnamed guests, and incorrect Jim Scott URLs.

The fixes were committed **directly to `main`** as [`a53e8671a485065a582af0933d227c8dab7a719f`](https://github.com/infoconex/coding-blog/commit/a53e8671a485065a582af0933d227c8dab7a719f). No article publication date, URL, original example, IndexNow configuration, security policy, or third-party dependencies were altered.

### Deployment-blocking decision

**Keep the integrated SEO diagnostic nonblocking for now.** The initial five findings are resolved, and the corrected full build shows **zero SEO warnings**. However, one clean generated build is not sufficient evidence to turn every SEO diagnostic into a deployment failure. In particular:

- Nonarticle files with **both** missing canonical and missing `og:url` are currently skipped; that could hide a future regression on the homepage or About page. Add explicit indexing-page coverage before relying on this scanner as a required deployment gate.
- The image validator deliberately catches unexpected exceptions from the SEO checker and only warns. A mandatory gate must surface scanner crashes as failures.
- Ensure genuine redirects are excluded without accidentally bypassing validation on normal content pages; enforce well-formed JSON-LD and local social assets as critical failures, while keeping editorial/social-preview recommendations advisory.
- Retain `scripts/validate_seo.py --site-dir _site` as a **strict standalone scan**, which already exits with error for detected findings. Promote only stable, well-tested critical checks to the existing post-build workflow after the missing-metadata blind spot and exception handling are covered by regression tests.

### Remaining monitoring and next project

Continue verifying the full Jekyll Pages deployment and its SEO summary in Actions; monitor search indexing and sitemap coverage independently in Google Search Console and Bing Webmaster Tools. The unchanged historical 103-article baseline CSV remains the pre-edit inventory. Consider **SEO guardrail enforcement and indexability coverage** as the next independent engineering project: detect missing metadata even on nonarticle pages, add ProfilePage and malformed-JSON-LD regression cases, distinguish true redirects, and introduce narrowly scoped deployment-blocking failures after a clean full-build test. Later editorial/AEO opportunities (internal topic clusters, citations and external-link maintenance) are separate work items.


## SEO validation hardening and deployment enforcement — 2026-10-29

**Scope:** Preserve the original 103-article baseline and previous audit findings. No article content, publication dates, permalinks, IndexNow behavior, social-card generation, or Jekyll ownership of SEO metadata were changed.

### Baseline and confirmed gaps

At the start of this milestone, commit `ad3fde4dea13480ad1b924b1382f0cae1c934224` was current on `main`. GitHub Actions Pages run [#497](https://github.com/infoconex/coding-blog/actions/runs/40901877345) showed successful content/security validation, build, deployment, and IndexNow jobs. Its build log reported 113 content HTML pages, 103 articles, 46 images, and zero SEO diagnostic findings. The SEO audit was still nonblocking inside `validate_images.py`.

The old SEO checker skipped nonarticle HTML pages missing both canonical and Open Graph URLs. It scanned JSON-LD only for article pages; it did not require the About page's ProfilePage identity node, validate date syntax, verify the built URL for nonarticle canonical links, or compare canonical destinations across rendered pages. Unexpected SEO checker exceptions were swallowed by the nonblocking image validator.

### Enforcement design

* The existing `scripts/validate_seo.py` now audits all generated indexable HTML documents, including homepage, About, and collections. Genuine Jekyll meta-refresh redirects remain excluded. Historical article paths retain their extensionless and trailing-slash compatibility.
* **ERROR:** SEO001–006 (missing/duplicate/unsafe/wrong/shared canonical and unexpected indexing exclusion); SEO010 and SEO012 (conflicting social metadata); SEO020–027 (malformed JSON-LD and invalid required BlogPosting identity, date, URL, image); SEO030–036 (About ProfilePage and Person identity); SEO040–042 (broken or non-HTTPS local social/structured-data images); SEO900 (missing site, no content, invalid encoding, or other fundamental scan failure).
* **WARNING:** SEO011 flags absent or empty optional Open Graph/Twitter fields. It is editorial/advisory; it does not fail the build. The validator does not attempt to judge social-card appearance or meta-description quality.
* Critical diagnostics identify both the generated file and its expected public URL. The scan raises unexpected runtime exceptions rather than swallowing them.
* The `pages.yml` build now runs `python3 scripts/validate_seo.py --site-dir _site` as an **independent mandatory post-Jekyll step** before uploading the Pages artifact. The image validator no longer invokes a second, nonblocking SEO scan. Image, browser-security, historical URL, content validation and IndexNow jobs remain unchanged.
* No new dependency or GitHub Actions workflow was added.

### Regression and failure simulation

Expanded `scripts/test_validate_seo.py` with focused missing canonical tests for homepage, About and collections; incorrect canonical paths and domains; shared canonical URLs; unintended robots noindex and malformed canonical syntax; malformed JSON-LD; valid @graph/array composition; invalid dates; missing or incorrect ProfilePage identity; optional social metadata warnings; missing structured-data image files; corrupt encoding; redirect spoof prevention; extensionless historical paths; and scanner exception propagation. Existing cases already cover missing BlogPosting, author attribution, duplicate social tags, missing social cards and legitimate redirects.

The image regression suite was updated to remove obsolete assertions that SEO problems must remain nonblocking inside `validate_images.py`; the standalone SEO quality gate now owns that responsibility. Two replacement image regression tests confirm the image validator remains independent and broken local images remain blocking; the image regression count stays at eight.

### Verified GitHub Actions and deployment results

The GitHub connector's general REST fetch can list **push-triggered workflow runs**, and the job-log actions retrieve the complete job logs. Those logs establish the milestone's results:

| Evidence | Initial enforcement run | Corrected final run |
| --- | --- | --- |
| Commit | `f4180c9171e3c5066c5011485da334b2d55a41f2` | `e66087bf23afe4d80c5b30d677907b030a387f29` |
| Pages run | [#498](https://github.com/infoconex/coding-blog/actions/runs/40903406563): failed | [#502](https://github.com/infoconex/coding-blog/actions/runs/40904313928): **success** |
| Standalone validation | [Run #529](https://github.com/infoconex/coding-blog/actions/runs/40903406288): failed | [Run #533](https://github.com/infoconex/coding-blog/actions/runs/40904313680): **success** |
| SEO tests | failed | **34/34 passed** |
| Image tests | not reached | **8/8 passed** |
| Generated SEO audit | build not reached | **113 pages, 103 articles** |
| Critical SEO errors / advisory warnings | not reached | **0 / 0** |
| Rendered images | build not reached | **46, no local-image or alt-text failures** |
| Browser security | not reached | **passed** |
| Build / deploy / IndexNow jobs | skipped | **all succeeded** |

The first enforcement run failed during the SEO unit tests with `AttributeError: 'SplitResult' object has no attribute 'params'`. The erroneous URL-parsing check was removed in commit `325f046525bf815a50509201563ef9e7e394a798`. The final deployment's SEO test job log explicitly reports `Ran 34 tests ... OK`; the image test job reports `Ran 8 tests ... OK`. The post-Jekyll build log explicitly reports:

```text
Image audit: examined 46 rendered images
Image audit: no missing/local broken image links or missing/generic alt text
SEO audit: 113 HTML pages, 103 articles
SEO audit: 0 critical error(s), 0 advisory warning(s)
```

The new mandatory **Verify critical SEO metadata in generated HTML** step succeeded before Pages artifact upload. The subsequent GitHub Pages **deploy** and **Notify IndexNow** jobs both succeeded. Two intermediate Pages runs (#500 and #501) were automatically cancelled in favor of newer pushes by the existing concurrency policy, not by new SEO violations.

**Outcome:** Deployment-blocking rendered SEO validation is active and passed on the complete generated Pages build. The tests simulate critical errors and an advisory-only warning; unit tests prove the expected classifications, while the full live Actions job proves clean generated-site acceptance. There was no separate intentional failing production build to test every type of critical violation end-to-end.

### Verification limits and maintenance

Generated-site Jekyll artifacts and Actions logs do not establish a live HTTP crawl, response-header correctness for every URL, actual Google/Bing indexing, external reference health, or social-preview appearance. Optional social metadata remains advisory by design. Non-HTML utility files are outside the indexable-page scan. Continue reviewing job output after changes to Jekyll, SEO Tag, generated social cards, or redirects; expand critical rules only when fixtures and complete generated builds support enforcement. The untouched 103-article baseline CSV remains the historical audit baseline. A separate next project should focus on search engine indexing, sitemap/robots coverage, Search Console and Bing Webmaster evidence.

## Sitemap, robots and crawlability verification — 2026-10-29

**Status: Generated-site audit and deploy-time enforcement completed. Official search-engine indexing coverage and raw live HTTP responses remain unverified.**

### Baseline evidence and findings

Examined the *actual* GitHub Pages artifact from successful [run #503](https://github.com/infoconex/coding-blog/actions/runs/40905240862), containing `artifact.tar` with Jekyll's full generated output (rather than assuming the source `robots.txt` or Jekyll sitemap plugin proves the output).

* `_site/sitemap.xml`: **112 unique canonical HTTPS URLs**, on `coding.infoconex.com`: all **103 historical and modern articles** and **nine** other pages (homepage, About, writing, archive, series landing, four series collections). No duplicate URLs, unexpected hosts, query strings or fragments.
* Generated indexable HTML canonical set: **112 matching sitemap entries**, with **zero omissions**, **zero unknown sitemap destinations**, and no duplicate canonical ownership. The prior SEO audit's 113 canonical-bearing pages **included `404.html`**, which is intentionally not advertised in the sitemap.
* Historical author redirect `author/jscott/index.html` is excluded from sitemap coverage; experimental pages and utilities are not included. Historical article permalinks retain their extensionless forms.
* Generated `robots.txt`: `User-agent: *`, `Allow: /`, and `Sitemap: https://coding.infoconex.com/sitemap.xml`. No wildcard site-wide disallow was found.
* These checks audit generated files, not raw HTTP response status, redirect chains, CDN caching, `X-Robots-Tag` headers, Google Search Console, or Bing Webmaster Tools. Public web-crawler views displayed the homepage/About and article pages but cannot establish indexing coverage.

### Automated preventive checks

Committed directly to `main` as [`1974bed47e1549c79267d274b950bc71e54975c0`](https://github.com/infoconex/coding-blog/commit/1974bed47e1549c79267d274b950bc71e54975c0).

* Added `scripts/validate_indexability.py`, using the existing `SeoParser` and `Finding` abstractions. Validates sitemap XML and duplicate entries, HTTPS/host/query/fragment correctness, the expected robots sitemap, wildcard `Disallow: /`, and exact two-way matching between generated canonical pages and sitemap locations. Excludes real generated redirects and `404.html`; does not hardcode the number of articles.
* **Critical failures** (CRAWL001–004, CRAWL011, CRAWL013–014, CRAWL020–025) block the build. **Warnings** (CRAWL010/012) report a missing robots file or missing sitemap advertisement without failing publication. The validator does not treat optional sitemap `lastmod` as required, to avoid fabricated content-modification dates.
* Added **15** focused regression tests in `scripts/test_validate_indexability.py`, including intentionally broken sitemap and robots fixtures, redirect exclusion, 404 handling, and extensionless article URLs. Extended existing `validate.yml` unit-test job and existing `pages.yml` post-Jekyll build; no new workflows or dependencies, and no content, URL, SEO template, IndexNow, or security changes.

### Verified enforcement and deployment

* [Deploy Jekyll site to Pages #504](https://github.com/infoconex/coding-blog/actions/runs/40906717516), on `1974bed47e1549c79267d274b950bc71e54975c0`: **success**. Reusable validation, security audit, Jekyll build, deployment, and IndexNow notification jobs **all succeeded**.
* [Validate content and security #535](https://github.com/infoconex/coding-blog/actions/runs/40906717450): **success**. Job log confirms **15/15 crawlability regression tests passed** (including failure simulations).
* Post-build logs: `Crawlability audit: 112 sitemap URLs, 112 indexable generated pages` and `0 critical error(s), 0 advisory warning(s)`. Existing SEO gate: **113 HTML pages / 103 articles, 0 errors, 0 warnings**. Image validation: **46 images, no broken local references or generic/missing alt text**. Browser security checks passed.
* The new crawlability command runs **before artifact upload** and fails on critical errors. Tests confirm known critical failures are classified as blocking; the successful generated-site Actions run proves the clean deployment passes it. No deliberate failing production deployment was performed.

### Remaining limitations and next independent work

Actual indexed/not-indexed URL counts, discovery and crawl diagnostics, submitted sitemap statuses, `noindex` directives in **live HTTP headers**, live status/redirect behavior, and crawler-specific access cannot be established from artifact inspection alone. To measure indexing coverage and identify real exclusions, connect and inspect verified **Google Search Console** and **Bing Webmaster Tools** property data (or export their coverage/sitemap reports). Do not infer indexing from a `site:` query or from 112 technically valid sitemap entries.

A future scoped live-origin smoke check could verify raw HTTP status, sitemap/robots availability, and response headers without making transient network errors deployment-blocking. Do not change IndexNow or original article dates as part of that work. Preserve the 103-article baseline CSV and this history of audit findings.
