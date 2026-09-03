---
title: "CopyGitHubRepo v0.4.0: Migrating GitHub Pages Without Guessing"
date: "2026-09-03"
description: "CopyGitHubRepo v0.4.0 adds opt-in GitHub Pages restoration, safer custom-domain handoff, independent verification, and recovery evidence for repository migrations."
tags: ["GitHub", "PowerShell", "Automation", "Developer Tools"]
slug: "copygithubrepo-v0-4-0-migrating-github-pages-without-guessing"
author: "Jim Scott"
published: false
permalink: "/post/2026/09/03/copygithubrepo-v0-4-0-migrating-github-pages-without-guessing"
series: "CopyGitHubRepo"
seriesOrder: 5
---

When I started building [CopyGitHubRepo](https://github.com/infoconex/copy-github-repo), the problem looked mostly like a Git problem.

Copy the repository content. Decide whether to preserve history. Recreate the destination. Verify the result.

That model worked well for the first releases, but the deeper I went into repository migration, the clearer something became:

**A GitHub repository is more than its Git data.**

GitHub Releases are one example. GitHub Pages is another.

A repository can contain every file required to build a website and still not have GitHub Pages configured correctly at the destination. A copied `CNAME` file does not prove that a custom domain is actually bound. A copied Pages workflow does not prove that GitHub has enabled the service. And a successful Git push tells you nothing about whether the destination repository is publishing from the intended branch, path, or Actions workflow.

That distinction is the focus of **CopyGitHubRepo v0.4.0**.

This release adds opt-in GitHub Pages restoration with a strong bias toward reviewed evidence, explicit boundaries, independent verification, and recoverability.

It is also the final article in this CopyGitHubRepo series.

## Git Content Is Not GitHub Pages State

The most important idea in v0.4.0 is simple:

> Copying the files for a GitHub Pages site is not the same thing as preserving GitHub Pages configuration.

A Pages repository can contain ordinary Git content such as:

- HTML, CSS, JavaScript, and generated site files;
- Jekyll configuration;
- a `CNAME` file;
- `.github/workflows/**` used for Pages deployment.

Snapshot and FullHistory migrations can already copy those files when they are part of the approved source state.

But GitHub also stores Pages configuration outside Git itself. That includes whether Pages is configured, how it publishes, the branch and path when branch-based publishing is used, a custom-domain binding, and supported HTTPS intent.

Version 0.4.0 treats that GitHub-side configuration as separate migration state.

If you want CopyGitHubRepo to restore supported Pages configuration, you now opt in with `-RestorePages`:

```powershell
Copy-GitHubRepository `
    -SourceRepository infoconex/source `
    -DestinationRepository infoconex/destination `
    -RestorePages
```

The switch is deliberately opt-in because restoring a hosted site can have consequences beyond simply copying repository content.

## The Migration Plan Is the Authority

One of the design principles that became increasingly important while building CopyGitHubRepo is that execution should not rediscover mutable source state and quietly make new decisions.

The migration plan is supposed to represent what was reviewed.

For Pages restoration, CopyGitHubRepo captures the supported GitHub-side Pages evidence during planning. Execution is then bound to that reviewed evidence rather than rerunning discovery and treating whatever happens to be visible later as the new authority.

Before destination mutation, relevant source state is revalidated so stale evidence causes the migration to fail closed rather than continuing with assumptions that may no longer be true.

That matters for normal repository migration, but it matters even more when a custom domain is involved.

## Custom Domains Turn Replacement Into a Handoff

A same-name or archive-and-replace migration can create an awkward problem when the repository being replaced owns a GitHub Pages custom domain.

The old repository may need to release the domain before the replacement repository can claim it.

That means the operation is no longer a single mutation. It becomes a handoff.

Version 0.4.0 adds controlled custom-domain handoff for supported replacement scenarios. The process uses fail-closed repository identity checks and deliberate ordering so CopyGitHubRepo can distinguish the repository being archived from the replacement repository being created.

The archived repository must be the repository that actually held the original identity before a replacement is allowed to assume it.

Only then can the Pages-domain handoff proceed through the reviewed migration path.

This is one of those features where the happy path is not the interesting part.

The more important question is:

**What happens if the handoff only gets halfway through?**

## Recovery Evidence Matters When Operations Are Multi-Step

A custom-domain move can fail after the old repository releases the domain but before the replacement successfully claims it.

That is exactly the kind of situation where a migration tool should not simply print an error and leave the operator guessing about what changed.

CopyGitHubRepo v0.4.0 records recovery and provenance evidence for the supported handoff path so a partial failure can be understood in terms of the identities involved, the state that was reviewed, and the operations that actually completed.

The goal is not to pretend every external dependency can be rolled back automatically.

The goal is to make partial state explicit and recoverable instead of ambiguous.

That difference has shaped a lot of the project.

A destructive migration utility should be conservative about what it changes, precise about what it verified, and useful when something goes wrong.

## Pages Activation Is Controlled Too

There is another subtle GitHub Pages problem that can appear during migration.

A repository may contain a workflow that publishes to Pages. Copying that workflow can create the impression that Pages itself was preserved, or can participate in activation behavior at the destination.

Version 0.4.0 separates those concerns.

Copied workflow files remain Git content. They are not treated as authoritative evidence that Pages was configured or migrated successfully.

Pages restoration happens through the reviewed `-RestorePages` path, and the migration controls implicit activation behavior so unsupported GitHub-side state is not silently enabled outside that contract.

This is a recurring theme in CopyGitHubRepo:

**Do not infer service state from repository files when GitHub maintains that state separately.**

## Branch and Path Publishing Must Be Representable

Branch-based Pages publishing introduces another question: what if the reviewed source configuration refers to a branch or path that cannot be represented safely at the destination?

CopyGitHubRepo does not invent a substitute.

If the source says Pages publishes from a particular branch and path, the migration either has evidence that the destination can represent that configuration or it fails closed.

It will not quietly choose another branch because it seems close enough.

That behavior may feel strict, but migration software should not manufacture configuration and then describe the result as preservation.

Preservation means being able to trace the destination state back to reviewed source evidence.

## Some Things Deliberately Stay Outside the Contract

GitHub Pages also depends on systems CopyGitHubRepo does not control.

Version 0.4.0 makes those boundaries explicit.

The tool does **not** claim to migrate or manage:

- external DNS records;
- DNS ownership-verification records;
- secret values;
- account or organization domain ownership;
- certificate provisioning;
- externally dependent HTTPS readiness.

Those conditions can be observed and reported where appropriate, but they are not silently treated as completed migration work.

This was an important distinction to make because a Pages site can be correctly configured inside GitHub while DNS or certificate state is still converging outside GitHub.

The migration report needs to distinguish those cases instead of collapsing them into one vague "Pages succeeded" result.

## Verification Is Independent of the Migration Claim

One of the principles I have tried to strengthen with each release is that successful execution should not be its own proof.

If the migration code says it restored Pages, verification should independently read the resulting GitHub-side state and compare it with the reviewed plan.

Version 0.4.0 extends verification for the supported Pages configuration, including Actions-based publishing and representable branch/path publishing.

It also keeps external readiness separate from migrated GitHub state.

That produces a more useful answer than simply asking whether a command returned without throwing an exception.

The questions become:

- Did the destination receive the Pages configuration that was reviewed?
- Does GitHub independently report the expected publishing mode?
- Is the expected custom domain actually bound?
- Is HTTPS intent represented where supported?
- Are external DNS, certificate, or ownership conditions still pending?

Those are much closer to the questions an operator actually cares about.

## The Wizard Supports the Same Contract

The guided experience has been updated as well.

If you prefer using:

```powershell
Start-CopyGitHubRepositoryWizard
```

you can opt into Pages restoration there too.

The wizard uses the same real planning path as `Copy-GitHubRepository -RestorePages`. It does not reconstruct a second, approximate view of Pages state just for the interactive interface.

That is important because the command interface and the wizard should not disagree about what is going to happen.

Both are reviewing and executing the same migration contract.

## What v0.4.0 Really Adds

It would be easy to describe this release as "GitHub Pages support," but I think that undersells what changed.

The feature itself is useful, especially for anyone moving documentation sites, project sites, or repositories that publish directly through GitHub Pages.

But the larger improvement is architectural.

CopyGitHubRepo now has a clearer model for handling GitHub-side service state that is related to repository content without being part of Git.

The process is:

1. discover the state during planning;
2. turn it into immutable reviewed evidence;
3. determine whether the state is safely representable at the destination;
4. revalidate relevant source assumptions before mutation;
5. execute the supported restoration path;
6. independently verify the resulting GitHub-side state;
7. preserve recovery evidence when multi-step operations can fail partially.

That model is useful beyond Pages.

It is a better way to think about repository migration in general.

## Updating to v0.4.0

CopyGitHubRepo is available from the [PowerShell Gallery](https://www.powershellgallery.com/packages/CopyGitHubRepo/).

If you already have it installed with PSResourceGet:

```powershell
Update-PSResource CopyGitHubRepo
```

Or install it with:

```powershell
Install-PSResource CopyGitHubRepo
```

You can confirm the loaded module version with:

```powershell
Start-CopyGitHubRepositoryWizard -Version
```

The [v0.4.0 release](https://github.com/infoconex/copy-github-repo/releases/tag/v0.4.0) and the complete [CopyGitHubRepo documentation](https://infoconex.github.io/copy-github-repo/) are available now.

## Closing the Series

This is the last article I plan to write in the CopyGitHubRepo release series.

The project itself will continue to evolve, but the first four releases established the foundation I originally wanted:

- **v0.1.0** made the project a published PowerShell module and established the Snapshot and FullHistory migration experience;
- **v0.2.0** added GitHub Release preservation to FullHistory migrations;
- **v0.3.0** brought selected release preservation to Snapshot migrations through newly constructed checkpoint history;
- **v0.4.0** extends the migration model beyond Git content into supported GitHub-side Pages configuration, including controlled custom-domain handoff and independent verification.

Looking back, the project became less about "copying a repository" and more about answering a harder question:

**What does it mean to move a GitHub repository and be able to trust the result?**

For me, the answer now includes more than files, commits, tags, releases, or configuration taken individually.

It means knowing what was reviewed, knowing what was changed, knowing what was verified, knowing what was deliberately left outside the contract, and having enough evidence to recover when the world does not cooperate.

That is the direction I wanted CopyGitHubRepo to reach.

And v0.4.0 feels like the right place to close this series.
