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

Before deciding how to modernize a .NET application, we need to understand what actually exists.

That can be harder than it sounds. A project's target framework may be obvious, but its effective build settings can depend on imported MSBuild files, installed tools, environment variables, package configuration, and continuous integration workflows. A successful build tells us something useful; it doesn't necessarily explain all the conditions that made the build possible.

**A technical baseline is an evidence-backed snapshot of an application's technical state at a known source revision.** It documents what the repository declares, what tools resolve, what has actually been executed, and what remains unverified.

This approach is useful whether the application targets .NET Framework 4.8 or a current .NET release, and whether its projects use traditional or SDK-style formats.

This article establishes the methodology. The companion [RecordSift](https://github.com/infoconex/RecordSift) walkthrough will apply it to a real application, showing the commands, outputs, and resulting documentation rather than repeating the checklist in the abstract.

This is part of the [Staying Current with .NET](/series/staying-current-with-dotnet/) series and follows the [introduction to our evidence-driven modernization journey](/post/2026/11/11/modernizing-dotnet-evidence-driven-journey-with-recordsift).

## What Is a Technical Baseline?

A technical baseline describes how an application is organized, configured, built, tested, and delivered **as it exists today**. It is an inventory and a record of supporting evidence, not an improvement plan.

At minimum, it answers four questions:

- **What are we examining?** The repository, exact source revision, relevant solutions and projects, and the scope of discovery.
- **How is it assembled?** Project relationships, target frameworks, build configuration, dependencies, and the tools and environment involved.
- **What has been verified?** Which operations actually ran, under what conditions, and with what outcomes.
- **What do we still not know?** Missing inputs, conflicting observations, failed commands, and verification that has not been performed.

The source revision matters. Branch names can move, and two engineers examining the same branch a week apart may be looking at different code. Record the repository, a full commit SHA, the discovery date, and any uncommitted changes or external inputs that affect the investigation. Where applicable, preserve submodule revisions and references to separately maintained build inputs.

A reproducible baseline means another engineer can retrieve the identified sources and **repeat the investigation**. It does not promise identical binaries or a successful build on every machine.

## What Makes Technical Evidence Reliable?

The central distinction is between **what source declares, what a tool evaluates, and what execution demonstrates**.

| Evidence method | What it establishes | Example |
|---|---|---|
| **Source-inspected** | A declaration, file, reference, or workflow definition exists at a particular revision | A project file declares a target framework |
| **Tool-evaluated** | A tool resolves configuration or dependencies using specified inputs | MSBuild reports the evaluated target framework or properties |
| **Executed** | An operation ran and produced a recorded result | A particular solution build or test run succeeded or failed |

These methods answer different questions. A source declaration is not proof that the build succeeds. An evaluated MSBuild property reflects a particular invocation and its inputs, not necessarily the state after targets execute. And a successful Debug build does not verify Release packaging or every target framework.

MSBuild can combine settings from projects, imported `.props` and `.targets` files, SDK defaults, conditions, environment variables, and command-line properties. Its [build process](https://learn.microsoft.com/en-us/visualstudio/msbuild/build-process-overview) and [property evaluation behavior](https://learn.microsoft.com/en-us/visualstudio/msbuild/evaluate-items-and-properties) help explain why inspecting a project file and inspecting an evaluated value are different activities.

The same principle applies to dependencies. A `PackageReference` declaration identifies a requested dependency. Restore produces an execution result and can generate a resolved dependency graph in `project.assets.json`. A `packages.lock.json` file records resolved dependency information, but its presence alone does not prove that a current restore succeeded or enforced locked mode. For `packages.config`, the recorded package list has different semantics from `PackageReference`; neither format should be mistaken for an observed restore outcome.

**Evidence provenance is separate from evidence method.** A test run from an earlier investigation is still executed evidence, but it belongs to the source revision, environment, command, and scope that produced it. It cannot automatically verify today's baseline.

For material findings, retain enough context to interpret the result: source revision, relevant file or artifact, method, tool and version, invocation or conditions, observed result, and verification status. Use precise statuses such as *verified for the stated scope*, *not verified*, *incomplete*, or *conflicting*.

A failed build or an unexecuted test suite is not something to hide. It is part of an accurate baseline.

## What Should a .NET Technical Baseline Document?

The goal is a complete technical inventory **without turning the methodology article into a command reference**. The categories below provide a consistent structure; the RecordSift walkthrough will show how to collect each one.

| Area | What to capture |
|---|---|
| **Source identity** | Repository, immutable commit, discovery scope, local modifications, and relevant external inputs |
| **Solutions and projects** | `.sln`, `.slnx`, or `.slnf` entry points; project paths, roles, formats, target frameworks, and project-reference relationships |
| **MSBuild and compilation** | Applicable properties and imports, conditions, SDK selection, compiler options, configurations, custom targets, and evaluated values when available |
| **Repository-wide configuration** | Relevant `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, `.editorconfig`, NuGet configuration, and other shared settings |
| **Dependencies** | Project and assembly references, NuGet management format, package sources, direct and resolved dependencies, lock files, and non-NuGet prerequisites |
| **Development and build environment** | OS and architecture, .NET SDKs and runtimes, .NET Framework targeting packs, MSBuild or Visual Studio versions, package tools, and required environment inputs |
| **Build and test execution** | Documented commands, selected configurations, test frameworks and runners, actual outcomes, result artifacts, and coverage of projects or test assemblies |
| **CI/CD and delivery** | Workflow definitions and completed runs, runner environments, validation steps, packaging, published artifacts, and deployment processes |
| **Runtime requirements** | Hosting platform, runtime version, architecture, native prerequisites, configuration files, and deployment assumptions |
| **Existing compatibility evidence** | Public API checks, assembly identities, serialization contracts, package validation, or consumer checks where relevant |

The table is intentionally broad. Not every application has every file, framework, workflow, or delivery mechanism. **An absent configuration file is an observation, not an instruction to add it.**

A few distinctions are particularly important:

- An SDK-style project is not the same thing as a modern target framework. SDK-style projects can target .NET Framework, and one solution may combine different project formats and frameworks.
- Effective MSBuild behavior may depend on imports and invocation context; the settings visible in one file do not necessarily describe the entire build.
- NuGet settings can come from repository, user, and machine scope. Central Package Management applies to relevant `PackageReference` projects; it is not a third dependency-management format.
- CI workflow definitions tell us what *should* run; completed runs and retained logs tell us what *did* run. Local and CI commands may differ.
- Existing testing and compatibility documentation should be referenced, not duplicated. This baseline inventories the technical mechanisms and their execution evidence rather than restating functional test scenarios.

For technical details on these mechanisms, see Microsoft's documentation for [MSBuild directory imports](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory), [SDK selection with `global.json`](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json), [NuGet configuration](https://learn.microsoft.com/en-us/nuget/consume-packages/configuring-nuget-behavior), and [dependency resolution](https://learn.microsoft.com/en-us/nuget/concepts/dependency-resolution).

## What Should the Finished Baseline Look Like?

I prefer a short discovery overview supported by a navigable technical baseline and links to the actual evidence.

The **overview** identifies the application, source revision, discovery date, scope, and the location of the detailed inventory. Someone new to the repository should be able to understand what was examined without reading every tool output.

The **technical inventory** organizes the areas above into consistent sections or files. Larger repositories may need separate project, dependency, build, and test records. A small repository might reasonably keep them together.

The **evidence references** connect important claims to source paths, evaluated output, workflow runs, test reports, or build artifacts. A concise finding might look like this:

| Field | Illustrative record |
|---|---|
| Observation | Project declares a particular target framework |
| Source and scope | Specific project at a recorded commit |
| Evidence | Project-file path |
| Method | Source-inspected |
| Verification | Declaration identified; successful build not established by this observation |

This is an illustration of how to record a finding, **not a claim about RecordSift**. The companion article will use actual evidence.

Finally, preserve an **outstanding-gaps record**. If a restore fails, a tool is unavailable, a CI result belongs to a different commit, or some projects have not been tested, say so explicitly. Avoid collapsing different revisions, platforms, configurations, or test scopes into a single claim that something is “verified.”

The baseline is useful when another engineer can identify the same source, find the applicable tools and configuration, locate the verification evidence, and see which questions remain open.

It is a dated snapshot that future discoveries can be compared against, not a document claiming the application will never change.

## Where Does Discovery End and Modernization Assessment Begin?

Discovery and assessment are related, but they serve different purposes.

During discovery, we might find traditional project formats, duplicated properties, specific package versions, missing configuration files, or differences between local and CI execution. We should record those facts and how we established them.

**We should not automatically treat every observation as a problem to fix.**

Modernization assessment asks different questions: Which changes are applicable? What benefits or risks do they introduce? What might affect compatibility? How should changes be prioritized and verified?

Separating those activities keeps the baseline factual and makes it useful even for a repository already using current .NET versions, SDK-style projects, and modern build tooling.

It also gives us a stable point of comparison: when we later change the project system, dependencies, or build process, we can compare the new state with the documented baseline rather than relying on memory.

## Applying the Methodology to RecordSift

The next article puts this method to work using [RecordSift](https://github.com/infoconex/RecordSift), a .NET Framework 4.8 application.

We'll identify the source revision, inspect the solutions and projects, examine build configuration and dependencies, document the environment, and capture the results of the build and test infrastructure. We'll distinguish declarations from evaluated configuration and executed verification throughout.

Most importantly, we'll publish the resulting technical documentation and its evidence, including anything we cannot establish. Readers will be able to follow a real investigation instead of a hypothetical set of commands.

Only after that baseline exists will we move into assessing modernization opportunities.

The guiding principle is simple: **document what exists, show what the evidence proves, and keep recommendations separate from the facts.**
