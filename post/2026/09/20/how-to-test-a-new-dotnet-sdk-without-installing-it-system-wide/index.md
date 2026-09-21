---
layout: post
title: "How to Test a New .NET SDK Without Installing It System-Wide"
date: "2026-09-20"
slug: "how-to-test-a-new-dotnet-sdk-without-installing-it-system-wide"
author: "Jim Scott"
published: false
featured: false
permalink: "/post/2026/09/20/how-to-test-a-new-dotnet-sdk-without-installing-it-system-wide"
description: "Install and test an exact .NET SDK in isolation without changing the SDKs available through your normal system-wide dotnet installation."
tags:
  - .NET
  - Software Engineering
  - Development Environment
  - SDK
series: "Staying Current with .NET"
seriesOrder: 4
---

# How to Test a New .NET SDK Without Installing It System-Wide

In the previous articles in this series, we looked at knowing which .NET SDK is building an application and making sure the application can be built on a clean machine.

There is another scenario that comes up when evaluating a .NET upgrade.

I want to try a newer SDK without changing the SDK installation I use for normal development.

For this experiment I used .NET 11 RC1:

```text
11.0.100-rc.1.26425.128
```

I could install it normally alongside my existing SDKs, but I do not have to.

Microsoft provides [`dotnet-install`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script) scripts that can install an SDK into a directory we choose instead of using the normal system-wide installer. Microsoft also documents this approach for [testing prerelease .NET SDKs locally](https://learn.microsoft.com/en-us/dotnet/core/tools/test-prerelease-sdk-locally).

I wanted to make that workflow repeatable, so I created a small tool around those scripts:

[infoconex/isolated-dotnet-sdk](https://github.com/infoconex/isolated-dotnet-sdk)

## What I Want from an Isolated SDK

There are three things I care about.

First, the SDK should live outside the normal .NET installation.

Instead of installing under a location such as:

```text
C:\Program Files\dotnet\
```

I keep isolated SDKs under my home directory:

```text
Windows
C:\Users\<user>\dotnet-sdks\

Linux
/home/<user>/dotnet-sdks/

macOS
/Users/<user>/dotnet-sdks/
```

Second, I want an exact SDK version. If another release appears tomorrow, I do not want my test environment silently changing underneath me.

Third, I do not want the isolated SDK added to `PATH`.

The result is simple:

```text
Normal .NET installation
    Used normally through: dotnet

Isolated SDK
    Used explicitly through its path
```

## Install the Tool

On Windows with PowerShell:

```powershell
irm https://raw.githubusercontent.com/infoconex/isolated-dotnet-sdk/main/isolated-dotnet-sdk.ps1 | iex
```

On Linux or macOS with Bash:

```bash
curl -fsSL https://raw.githubusercontent.com/infoconex/isolated-dotnet-sdk/main/isolated-dotnet-sdk.sh | bash
```

The first run saves the tool under `~/dotnet-sdks` and opens an interactive menu:

```text
isolated-dotnet-sdk: What would you like to do?

  1. Install an SDK
  2. Remove an isolated SDK
  3. List isolated SDKs
  4. Exit

Selection:
```

Choosing **Install an SDK** loads Microsoft's published .NET release metadata and lets me choose a supported or development channel.

For example:

```text
isolated-dotnet-sdk: Select a supported or development .NET channel:

  1. .NET 11.0  STS  Go Live  latest SDK 11.0.100-rc.1.26425.128
  2. .NET 10.0  LTS  Active   latest SDK 10.0.401
  3. .NET 9.0   STS  Maintenance  latest SDK 9.0.318
  4. .NET 8.0   LTS  Maintenance  latest SDK 8.0.425

  A. Show end-of-life channels
  M. Enter an exact SDK version manually
  Q. Cancel
```

After choosing a channel, the tool lists its SDK versions and marks versions already present on the machine.

```text
1. 11.0.100-rc.1.26425.128 (latest, isolated)
```

A version can be marked as:

- `latest` when it is the latest SDK identified by Microsoft's release metadata;
- `system` when it is already available through the normal `dotnet` host;
- `isolated` when it is already installed under `~/dotnet-sdks`.

If an SDK is already installed normally, the tool does not silently create another copy:

```text
isolated-dotnet-sdk: .NET SDK 10.0.401 is already installed normally.
isolated-dotnet-sdk: Install an isolated copy too? [y/N]
```

Pressing Enter leaves the system as it is.

## You Can Still Be Explicit

The menu is useful when I am working interactively, but scripts and automation should be able to specify exactly what they want.

PowerShell:

```powershell
& "$HOME\dotnet-sdks\isolated-dotnet-sdk.ps1" `
    -Action Install `
    -Version '11.0.100-rc.1.26425.128'
```

Bash:

```bash
"$HOME/dotnet-sdks/isolated-dotnet-sdk.sh" \
    install \
    11.0.100-rc.1.26425.128
```

Supplying the version bypasses the picker.

If I intentionally want an isolated copy of an SDK that is already installed normally, PowerShell supports `-Yes` and Bash supports `--yes`.

## What Gets Installed?

This is a complete SDK installation, not just a runtime.

It contains the development tooling behind commands such as:

```text
dotnet restore
dotnet build
dotnet test
dotnet msbuild
dotnet pack
```

along with the compiler, NuGet tooling, templates, targeting packs, and runtime components included with that SDK.

The Microsoft install script itself is cached under `~/dotnet-sdks`, and each SDK gets its own version-specific directory.

For example:

```text
dotnet-sdks/
    10.0.401/
    11.0.100-rc.1.26425.128/
```

That makes it easy to keep multiple isolated SDKs side by side.

## `global.json` Still Matters

This was the most interesting detail I found while testing the workflow.

An isolated `dotnet` executable still performs normal SDK resolution based on the current working directory.

The repository I used for testing contains this `global.json`:

```json
{
  "sdk": {
    "rollForward": "disable",
    "version": "10.0.401"
  }
}
```

The isolated installation contained only:

```text
11.0.100-rc.1.26425.128
```

If I invoked the isolated executable from inside that repository with a command that requires SDK selection, the repository still asked for `10.0.401`.

That is correct behavior, but it means simply using a different `dotnet` executable is not enough to ignore `global.json`.

The tool handles its own SDK-management operations from the neutral `~/dotnet-sdks` directory so the repository I happened to launch it from does not interfere.

It also verifies installations with:

```text
dotnet --list-sdks
```

rather than relying on:

```text
dotnet --version
```

`--version` requires SDK selection. `--list-sdks` tells us what is physically available under that isolated host.

This distinction matters later when we intentionally connect an isolated SDK to an existing repository.

## Give the SDK a Quick Test

Before involving an existing application, I want to prove the isolated SDK can create, build, and run a simple project.

I do this from a neutral temporary directory so an existing repository's `global.json` cannot influence the test.

On Windows:

```powershell
$DotNet = "$HOME\dotnet-sdks\11.0.100-rc.1.26425.128\dotnet.exe"
$TestProject = Join-Path $env:TEMP 'SdkExperiment'

Set-Location $env:TEMP

& $DotNet new console -n SdkExperiment -f net11.0
& $DotNet build $TestProject
& $DotNet run --project $TestProject
```

On Linux or macOS:

```bash
DOTNET="$HOME/dotnet-sdks/11.0.100-rc.1.26425.128/dotnet"
TEST_PROJECT="/tmp/SdkExperiment"

cd /tmp

"$DOTNET" new console -n SdkExperiment -f net11.0
"$DOTNET" build "$TEST_PROJECT"
"$DOTNET" run --project "$TEST_PROJECT"
```

The expected application output is:

```text
Hello, World!
```

At that point I know the isolated SDK itself can create, restore, build, and run a .NET 11 application.

One caveat is worth calling out. Isolating the SDK files does not create a hermetic sandbox. The .NET CLI can still create normal per-user state during first-time use, such as telemetry configuration or a development HTTPS certificate.

The isolation here is about keeping the SDK out of the normal system-wide installation and off `PATH`.

## The Normal SDK Installation Does Not Change

On the Windows machine I used for testing, the normal command:

```powershell
dotnet --list-sdks
```

continued to report:

```text
8.0.425 [C:\Program Files\dotnet\sdk]
9.0.318 [C:\Program Files\dotnet\sdk]
10.0.401 [C:\Program Files\dotnet\sdk]
```

The isolated .NET 11 SDK did not appear there.

On the Linux devcontainer, the normal host likewise continued to report only its system-installed `10.0.401` SDK.

That is exactly what I wanted. The new SDK exists, but the normal development environment has not been changed to use it.

Starting with .NET 10, `global.json` supports `sdk.paths`, which can tell the .NET host to search additional SDK locations. Microsoft documents that behavior in both the [`global.json` overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) and [Test prerelease .NET SDKs locally](https://learn.microsoft.com/en-us/dotnet/core/tools/test-prerelease-sdk-locally).

I am leaving that configuration for the next article.

## Cleanup Is Part of the Tool Too

An isolated SDK should be easy to remove when the experiment is over.

Run the tool without a version and it will show only the SDKs installed under `~/dotnet-sdks`.

PowerShell:

```powershell
& "$HOME\dotnet-sdks\isolated-dotnet-sdk.ps1" -Action Remove
```

Bash:

```bash
"$HOME/dotnet-sdks/isolated-dotnet-sdk.sh" remove
```

Before deleting the selected version, the tool runs [`dotnet build-server shutdown`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build-server) using that isolated host.

That matters on Windows. During testing, MSBuild and the compiler server kept files inside the isolated SDK locked until those build servers were shut down.

The tool then removes only the selected version directory. Other isolated SDKs and the normal system installation are left alone.

## What I Actually Tested

I tested the tool with PowerShell 7 on Windows 11 and with Bash inside a Linux devcontainer.

The tests covered:

- bootstrapping the tool from GitHub;
- selecting SDKs interactively;
- installing an exact SDK version;
- recognizing system-installed and isolated SDKs;
- creating an isolated duplicate only when explicitly requested;
- keeping the repository's existing `global.json` from affecting tool-management operations;
- listing isolated SDKs;
- shutting down build servers before removal;
- removing only isolated SDK directories;
- rejecting invalid SDK version input;
- returning a nonzero exit status for operational failures;
- leaving the normal system SDK installation unchanged.

That is enough for me to treat this as a tool I can reuse rather than a one-off script embedded in an article.

The implementation and usage documentation are available here:

[infoconex/isolated-dotnet-sdk](https://github.com/infoconex/isolated-dotnet-sdk)

## Now We Have a Tool We Can Use

Installing a newer SDK was not the goal.

The goal was having newer tooling available without changing the SDK installation the normal development environment depends on.

Now I have that.

In the next article, I am going to intentionally connect an existing repository to the isolated SDK and use it to understand what actually needs to change before an upgrade.

## Microsoft References

- [.NET install scripts](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script)
- [Test prerelease .NET SDKs locally](https://learn.microsoft.com/en-us/dotnet/core/tools/test-prerelease-sdk-locally)
- [`dotnet build-server`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build-server)
- [`global.json` overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json)
- [.NET 11 RC1 release notes](https://github.com/dotnet/core/blob/main/release-notes/11.0/preview/rc1/11.0.0-rc.1.md)
- [.NET 11 downloads](https://dotnet.microsoft.com/en-us/download/dotnet/11.0)
