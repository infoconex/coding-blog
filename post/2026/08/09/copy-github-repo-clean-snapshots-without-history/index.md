---
title: "Copy GitHub Repo – Clean Snapshots Without Carrying History"
date: "2026-08-09"
description: "Copy GitHub Repo is a PowerShell utility for creating clean repository snapshots or preserving full history with explicit planning, verification, and recovery safeguards."
tags: ["GitHub", "PowerShell", "Automation", "Developer Tools"]
slug: "copy-github-repo-clean-snapshots-without-history"
author: "Jim Scott"
permalink: "/post/2026/08/09/copy-github-repo-clean-snapshots-without-history"
---
Sometimes you want a copy of a GitHub repository, but you do **not** want its history.

A normal clone preserves Git history. A fork keeps a relationship to the original repository. A mirror is designed to reproduce refs. A template repository is useful for starting new projects, but it is not always the workflow you want when publishing the current state of an existing repository.

That is the problem behind [copy-github-repo](https://github.com/infoconex/copy-github-repo).

The project is a PowerShell utility for safely publishing or copying GitHub repositories with two explicit content modes: **Snapshot** and **FullHistory**.

## Snapshot is the default

Snapshot mode is designed for clean publication.

It takes the current state of the source repository's default branch and publishes that content into a new repository as one unrelated root commit.

That intentionally leaves behind:

- previous commit history;
- old branches and tags;
- pull requests;
- issues and milestones;
- other historical GitHub records that are not part of the current source tree.

The result is a new repository that starts from the current content rather than inheriting the historical identity of the source repository.

That is different from simply cloning and pushing to another remote.

## FullHistory is explicit

Sometimes history is the thing you need to preserve.

For those cases, FullHistory mode keeps ordinary Git history, branches, tags, and reachable Git LFS objects.

This distinction is important because there is no universally correct meaning of "copy a repository."

If the goal is clean publication, preserving every historical ref is wrong.

If the goal is migration, removing ancestry and tags may be unacceptable.

The tool makes that choice explicit rather than guessing.

## Why not just use a few Git commands?

You can create a clean snapshot manually.

The process is not conceptually difficult: obtain the current content, remove the source Git identity, initialize a new repository, create a root commit, create the destination repository, push the content, restore selected settings, and verify the result.

The difficulty is in doing all of that safely and repeatedly.

Questions appear quickly:

- Does the destination already exist?
- Are you about to overwrite something important?
- Should repository visibility be preserved?
- Which settings should be restored?
- What happens if mutation succeeds halfway and verification fails?
- What if Git LFS is involved?
- What if the source and destination names are the same?
- How do you prove that the final repository contains what you intended?

The project exists to turn those edge cases into an explicit product contract instead of a collection of shell assumptions.

## Plan before mutation

The deterministic API supports a non-mutating planning path:

```powershell
Copy-GitHubRepository `
    -SourceRepository infoconex/source `
    -DestinationRepository infoconex/destination `
    -PlanOnly
```

That lets you inspect the intended operation before GitHub is changed.

Only after reviewing the plan do you run the execution path:

```powershell
Copy-GitHubRepository `
    -SourceRepository infoconex/source `
    -DestinationRepository infoconex/destination
```

`-WhatIf` is also non-mutating.

This plan-first approach is one of the most important safety choices in the tool.

## Existing destinations are not silently overwritten

The utility rejects an existing destination repository unless the user has selected an explicit archive-and-replace flow.

Replacement is treated as a distinct operation with its own confirmation and recovery requirements.

For same-name replacement, the original repository is archived and verified before the original name is reused.

Destructive replacement requires exact typed confirmation. `-Force` does not bypass that authority boundary.

That is intentional.

A command-line switch should not turn a high-impact repository replacement into an accidental default.

## Verification is part of success

Creating the destination is not enough to report success.

The tool verifies content after publication.

That distinction matters because remote mutation can succeed while the final repository is still incomplete or incorrect.

For example, a push could succeed while expected refs or LFS content are missing, or repository settings might not match the intended state.

A safe migration tool needs to distinguish "the API call succeeded" from "the operation achieved the requested outcome."

## Failures should preserve recovery information

Another important design choice is that the tool does not automatically delete or aggressively roll back repositories after every post-mutation failure.

Once a remote repository has been changed, automatic cleanup can destroy the very evidence needed to recover safely.

Instead, the project favors durable recovery information and explicit follow-up.

That makes failures less magical, but much easier to reason about.

## The guided wizard

For interactive use, the recommended entry point is:

```powershell
Start-CopyGitHubRepositoryWizard
```

The wizard discovers repositories, defaults to Snapshot behavior, lets the user review choices, produces a real plan, and requires an explicit Execute decision before mutation.

A repository checkout can start the same experience with:

```powershell
./copy-github-repo.ps1
```

The wizard is useful for humans, while `Copy-GitHubRepository` remains the deterministic API for scripts and automation.

Keeping those layers separate avoids mixing interactive UI behavior with the underlying repository-copy contract.

## Authentication and prerequisites

The tool uses standard local tooling:

- PowerShell 7.4 or newer;
- Git;
- GitHub CLI (`gh`);
- Git LFS when the selected mode requires it.

Authentication is handled through GitHub CLI:

```powershell
gh auth login --hostname github.com
```

Version 1 intentionally supports GitHub.com and fails closed for other hosts rather than pretending enterprise or alternate hosts behave identically.

## Snapshot versus fork, mirror, and template

These workflows solve different problems.

A **fork** preserves a GitHub relationship to the upstream project.

A **mirror** is intended to preserve repository refs and history as faithfully as possible.

A **template repository** provides a reusable starting structure for future repositories.

A **Snapshot copy** publishes the current source state as a new historical root with no inherited Git ancestry.

A **FullHistory copy** is the option when ancestry, branches, tags, blame information, signed historical commits, or other Git history must survive.

The tool does not try to collapse those meanings into one command that makes hidden decisions.

## A practical use case

Imagine a repository that has years of internal development history, experimental branches, old credentials that were removed long ago, obsolete issue discussions, and a current source tree that is now ready to be published independently.

A Snapshot copy can create a clean public repository containing the reviewed current state without publishing the entire historical record.

That does **not** erase the original repository. It creates a new repository with a different history.

The source remains the source, and the published snapshot becomes a new project starting point.

## Safety is the main feature

The core Git operations are not the most interesting part of this project.

The interesting part is the set of boundaries around them:

- planning before mutation;
- explicit mode selection;
- no silent overwrite;
- confirmation for destructive replacement;
- verification before success;
- preservation of recovery information;
- clear support boundaries.

That is a pattern I increasingly value in developer tooling.

Automation is most useful when it removes repetitive work **without removing the user's authority over consequential decisions**.

Copy GitHub Repo is built around that idea.
