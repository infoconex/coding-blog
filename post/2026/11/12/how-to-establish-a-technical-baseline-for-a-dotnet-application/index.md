---
layout: post
title: "How to Establish a Technical Baseline for a .NET Application"
seoTitle: "How to Establish a .NET Technical Baseline"
description: "How to document .NET projects, builds, dependencies, tooling, and tests while separating declared settings from verified results."
date: "2026-11-12"
slug: "how-to-establish-a-technical-baseline-for-a-dotnet-application"
author: "Jim Scott"
published: false
featured: false
permalink: "/post/2026/11/12/how-to-establish-a-technical-baseline-for-a-dotnet-application"
tags:
  - .NET
  - Software Engineering
  - Modernization
  - MSBuild
  - Technical Discovery
series: "Staying Current with .NET"
seriesOrder: 10
image: /post/2026/11/12/how-to-establish-a-technical-baseline-for-a-dotnet-application/images/how-to-establish-a-technical-baseline-for-a-dotnet-application-banner.png
---
![Illustration of .NET project structure, MSBuild configuration, dependencies, test results, and a technical evidence checklist](images/how-to-establish-a-technical-baseline-for-a-dotnet-application-banner.png)

Before modernizing a .NET application, establish **what exists and what has actually been verified**.

A technical baseline records the projects, configuration, dependencies, build and test evidence, and unanswered questions at a specific source revision.

This article explains the methodology. The companion [RecordSift walkthrough](https://github.com/infoconex/RecordSift) will demonstrate the investigation using actual commands, evidence, and documentation. The method applies to both traditional and modern .NET projects.

This article follows our [introduction to evidence-driven modernization](/post/2026/11/11/modernizing-dotnet-evidence-driven-journey-with-recordsift) in the [Staying Current with .NET](/series/staying-current-with-dotnet/) series.

## What Is a Technical Baseline?

A technical baseline records how an application is configured, built, tested, and delivered **at a specific point in time**. It answers four questions:

- **What exists?** The source revision, projects, dependencies, and configuration.
- **How does it work technically?** The tools, environments, and build processes.
- **What is verified?** Operations actually performed and their results.
- **What remains unknown?** Missing inputs, conflicting evidence, or unexecuted checks.

Identify the repository, full commit SHA, discovery date, and scope. Capture uncommitted changes and external inputs when relevant; a branch name alone is not a fixed reference.

**Reproducible discovery** means another engineer can repeat the investigation using the documented inputs. It does not guarantee identical build artifacts.

## What Makes Technical Evidence Reliable?

Classify each finding by **what its evidence establishes**:

| Evidence method | What it proves | Example |
|---|---|---|
| **Source-inspected** | A declaration exists at a recorded revision | A project declares its target framework |
| **Tool-evaluated** | A tool resolved a value under known inputs | MSBuild evaluates a property |
| **Executed** | An operation ran with a recorded outcome | A build or test run succeeded or failed |

These aren't interchangeable. MSBuild imports, conditions, and command-line settings can change evaluated properties; evaluation alone does not establish build success or the final state after target execution. See [MSBuild evaluation](https://learn.microsoft.com/en-us/visualstudio/msbuild/evaluate-items-and-properties).

Similarly, a package declaration is not a verified restore. For `PackageReference`, a restore can produce the resolved graph in `project.assets.json`; a lock file does not, by itself, prove that locked-mode restore ran. `packages.config` has different dependency-recording semantics.

**Provenance is separate from method.** An earlier test run remains executed evidence, but only for its recorded commit, environment, command, and scope.

For each significant finding, retain the source revision, evidence location, method, relevant tool and invocation, outcome, and verification status. Record failures and gaps rather than implying they passed.

## What Should a .NET Technical Baseline Document?

Use a consistent inventory of the application's technical foundations:

| Area | What to document |
|---|---|
| **Solutions and projects** | Solution entry points, project roles, formats, target frameworks, and references |
| **Build configuration** | MSBuild imports and evaluated settings, compiler options, `global.json`, `Directory.Build.props` and `Directory.Build.targets`, and other shared configuration |
| **Dependencies** | NuGet format, `Directory.Packages.props` where applicable, package sources, declared and resolved packages, and external prerequisites |
| **Toolchain and environment** | OS, architecture, SDKs, runtimes, .NET Framework targeting packs, MSBuild or Visual Studio, and required inputs |
| **Builds and tests** | Commands, configurations, test runners, coverage of projects or tests, execution results, and artifacts |
| **CI/CD and delivery** | Workflow definitions versus completed runs, packaging, releases, and deployment requirements |
| **Runtime and compatibility** | Hosting, native dependencies, runtime configuration, and existing API or compatibility checks |

Keep project format separate from target framework: an SDK-style project can target .NET Framework. Likewise, configuration can be inherited, and NuGet settings can extend beyond the repository. Record **which settings actually apply**, not just which files exist.

Not every area applies to every application. **An absent file is an observation, not a recommendation to create it.** Reference existing functional and test documentation instead of duplicating it.

## What Should the Finished Baseline Look Like?

Keep the output simple and navigable:

- **Discovery overview:** application, commit SHA, date, scope, and links to supporting records.
- **Technical inventory:** the relevant areas above, organized for easy reference.
- **Evidence and gaps:** source files, evaluated outputs, run logs, results, and anything unverified or conflicting.

For example, a project file can establish a **declared target framework** without proving the project builds. Record the source path and method, then track build verification separately.

A useful baseline lets another engineer locate the same source, understand the configuration, repeat the investigation, and distinguish verified results from outstanding questions.

## Where Does Discovery End and Modernization Assessment Begin?

**Discovery establishes facts; assessment decides what to change.**

Finding an older project format, repeated setting, particular dependency version, or missing configuration file does not automatically make it a defect.

Modernization assessment evaluates options, compatibility, benefits, risks, and priorities **after** the existing state is documented. This separation makes the baseline equally useful for traditional and modern .NET projects.

## Applying the Methodology to RecordSift

The companion article will apply this method to [RecordSift](https://github.com/infoconex/RecordSift), our .NET Framework 4.8 case study.

We'll inspect the real repository, run appropriate discovery and verification commands, and publish the technical baseline with its evidence and open questions. Modernization assessment will follow separately.

**First document what exists. Then decide what should change.**
