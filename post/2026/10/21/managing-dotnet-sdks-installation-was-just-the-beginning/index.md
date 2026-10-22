---
layout: post
title: "Managing .NET SDKs: Installation Was Just the Beginning"
date: "2026-10-21"
slug: "managing-dotnet-sdks-installation-was-just-the-beginning"
author: "Jim Scott"
published: true
featured: false
permalink: "/post/2026/10/21/managing-dotnet-sdks-installation-was-just-the-beginning"
description: "How Isolated .NET SDK evolved from a simple installer wrapper into a tool for managing, verifying, and auditing SDK installations."
tags:
  - .NET
  - Software Engineering
  - Development Environment
  - SDK
series: "Staying Current with .NET"
seriesOrder: 5
image: /post/2026/10/21/managing-dotnet-sdks-installation-was-just-the-beginning/images/managing-dotnet-sdks-installation-was-just-the-beginning-banner.png
---

![Managing .NET SDKs: Installation Was Just the Beginning](images/managing-dotnet-sdks-installation-was-just-the-beginning-banner.png)

In September, I wrote about [testing a new .NET SDK without installing it system-wide](/post/2026/09/20/how-to-test-a-new-dotnet-sdk-without-installing-it-system-wide).

In that article, I introduced a small project I'd been working on called [Isolated .NET SDK](https://github.com/infoconex/isolated-dotnet-sdk).

I described it this way:

> It still uses Microsoft's official `dotnet-install` scripts underneath. The project just handles the workflow around them.

That was accurate when I wrote it.

By the time I released [Isolated .NET SDK v0.4.0](https://github.com/infoconex/isolated-dotnet-sdk/releases/tag/v0.4.0) on October 17, less than a month later, it wasn't anymore.

I hadn't planned on building an SDK management tool. I wanted a convenient way to test different .NET SDK versions without changing my normal development environment.

But as the project evolved, I found there was more to managing an isolated SDK than getting it installed.

## Moving Beyond Microsoft's Installer Scripts

Microsoft's `dotnet-install` scripts already provide a way to install SDKs outside the normal system locations. That's where I started, and they're still useful for many situations.

My original tool simplified the process of selecting, installing, and removing SDK versions.

But installation raised some questions.

How do I know the downloaded SDK is actually the version I requested? What happens if installation fails halfway through? How do I avoid leaving behind something that looks installed but isn't usable?

Starting with v0.2.0, the project moved away from relying on Microsoft's installer scripts.

It now uses Microsoft's published release metadata to locate the exact SDK archive, verify its checksum, and validate the installation before moving it into its final location.

The tool still relies on Microsoft's official SDK distributions. What changed is that it takes responsibility for the installation process rather than delegating that work to another script.

## Installing an SDK Wasn't the End of the Problem

Once I could install SDKs into separate directories, I needed a better way to manage them.

What started as a simple installer has grown into a tool for managing the lifecycle of isolated .NET SDKs.

Here's the main menu from v0.4.0:

```text
Isolated .NET SDK v0.4.0

What would you like to do?

  I. Install an SDK
  R. Remove an isolated SDK
  L. List installed SDKs
  V. Verify an isolated SDK
  A. Audit installed SDKs

  E. Exit

Selection:
```

The menu provides an overview of what the tool can do. Three operations in particular help answer questions that come up when working with different SDK versions.

The following examples are from my Windows development machine running the official v0.4.0 release. I've anonymized my Windows account name and omitted the temporary loading messages.

### List: What Do I Have Installed?

The normal `dotnet --list-sdks` command doesn't necessarily show SDKs deliberately installed in separate locations.

**List** shows both isolated and system SDKs, keeping them separate so I can see what's installed and where.

```text
Installed .NET SDKs

Isolated SDKs:
  10.0.303  C:\Users\<user>\dotnet-sdks\10.0.303
  9.0.205   C:\Users\<user>\dotnet-sdks\9.0.205

System SDKs:
  10.0.402  C:\Program Files\dotnet\sdk\10.0.402
  10.0.401  C:\Program Files\dotnet\sdk\10.0.401
  9.0.319   C:\Program Files\dotnet\sdk\9.0.319
  8.0.426   C:\Program Files\dotnet\sdk\8.0.426
```

I have two isolated SDKs and four system SDKs.

The distinction matters because the tool can inspect system SDKs, but it doesn't own them or attempt to remove them.

### Verify: Does This SDK Actually Work?

Finding an SDK directory doesn't mean the installation is healthy.

**Verify** checks whether a specific isolated SDK works, resolves to the expected version, and actually comes from its isolated directory.

Here's the result of verifying my isolated SDK `10.0.303`:

```text
Verify isolated .NET SDK

SDK information:
  SDK version         10.0.303
  .NET channel        10.0
  Support type        LTS
  Status              Active
  SDK release date    2026-08-11
  Channel EOS date    2028-11-14
  Update available    10.0.402

Installed components:
  Host version        10.0.11
  Architecture        x64
  Runtime identifier  win-x64

  .NET runtimes:
    Microsoft.AspNetCore.App      10.0.11
    Microsoft.NETCore.App         10.0.11
    Microsoft.WindowsDesktop.App  10.0.11

Verification:
  Installation directory  OK  C:\Users\<user>\dotnet-sdks\10.0.303
  .NET host               OK  Host executable found and launched
  SDK inventory           OK  Exact SDK found in isolated installation
  SDK resolution          OK  Correct SDK selected

Isolated SDK 10.0.303 verified successfully.
```

The isolated SDK is working correctly, even though a newer version is available.

Verify tells me whether the SDK installation is usable, not whether it's the latest version or whether my application will build successfully with it.

### Audit: Is This SDK Still Current and Supported?

An SDK can work perfectly and still be outdated or out of support.

**Audit** uses Microsoft's release metadata to evaluate installed SDKs, identifying their lifecycle status and whether updates are available.

Here's the Audit result from the same machine:

```text
.NET SDK audit

Isolated SDKs:
  10.0.303  LTS  Active       Release: 2026-08-11  EOS: 2028-11-14  Update -> 10.0.402
  9.0.205   STS  Maintenance  Release: 2025-06-10  EOS: 2026-11-10  Update -> 9.0.319

System SDKs:
  10.0.402  LTS  Current      Release: 2026-10-13  EOS: 2028-11-14
  10.0.401  LTS  Active       Release: 2026-09-08  EOS: 2028-11-14  Update -> 10.0.402
  9.0.319   STS  Maintenance  Release: 2026-10-13  EOS: 2026-11-10
  8.0.426   LTS  Maintenance  Release: 2026-10-13  EOS: 2026-11-10
```

Notice that both isolated SDKs have updates available, and those newer versions are already installed system-wide.

That doesn't make the isolated installations invalid. They might be there intentionally for testing.

Audit gives me the information I need to decide whether to keep them, update them, or remove them.

It also connects directly to my [Staying Current with .NET](https://coding.infoconex.com/series/staying-current-with-dotnet/) series. I don't want to discover an unsupported SDK only when an upgrade becomes urgent.

While the interactive menu makes the tool convenient to use from a terminal, the same operations are available directly from the command line for scripts and automation.

I've also moved away from downloading the tool from a changing `main` branch. The recommended installation now uses verified scripts from published GitHub releases, with the option to select a specific version. The [GitHub repository](https://github.com/infoconex/isolated-dotnet-sdk) contains the installation instructions and command documentation.

## The Edge Cases Made Things Interesting

One of the more challenging areas of v0.4.0 was improving support for older .NET SDKs.

I initially approached installation and verification with the expectations you'd have from modern SDKs.

But older releases don't always follow the same conventions. Archive names, version mappings, and even available command-line capabilities can differ.

Supporting those versions meant accounting for the differences without weakening verification.

Removal presented its own challenges. A build process might still have files open, or an earlier installation might have left behind an incomplete directory.

Version 0.4.0 improves handling of these situations, including safer removal and recovery when something doesn't finish cleanly.

There are still limits. Some historical SDKs won't run on modern operating systems, and locked files can't always be removed immediately.

I'd rather have the tool report those limitations clearly than make an operation appear successful when it wasn't.

## Where This Leaves Me

One thing I was reminded of while building this tool is that getting something to work is often the easy part. Making it reliable, maintainable, and useful across different environments takes considerably more thought.

I'm pleased with where [Isolated .NET SDK v0.4.0](https://github.com/infoconex/isolated-dotnet-sdk/releases/tag/v0.4.0) has landed. There's always more that could be added, but I think it now addresses the problems I originally set out to solve, along with several I hadn't anticipated.

I can now return to what I originally planned for this series: using newer .NET tooling to understand an application's dependencies before attempting an upgrade.
