---
layout: post
title: ".NET 11 Is Here. .NET 8 and .NET 9 Are Out of Support."
seoTitle: ".NET 11 Released as .NET 8 and 9 Reach End of Support"
date: "2026-11-10"
slug: "net-11-released-net-8-9-end-of-support"
author: "Jim Scott"
published: true
featured: false
permalink: "/post/2026/11/10/net-11-released-net-8-9-end-of-support"
description: ".NET 11 launches as .NET 8 and 9 reach end of support. Review final servicing updates for .NET 8, 9, and 10, security fixes, and upgrade choices."
tags:
  - .NET
  - .NET 11
  - .NET 10
  - Software Engineering
  - Security
  - Lifecycle Management
series: "Staying Current with .NET"
seriesOrder: 8
---

On November 10, 2026, Microsoft officially [released .NET 11](https://devblogs.microsoft.com/dotnet/announcing-dotnet-11/). But did you know Microsoft also released servicing updates for .NET 8, .NET 9, and .NET 10, even though .NET 8 and .NET 9 reached end of support on the very same day?

That may sound contradictory. It isn't. November 10 was both a major .NET release day and Microsoft's regular Patch Tuesday. The final updates for .NET 8 and .NET 9 do not extend their support lifetimes.

For development teams, the announcements call for three different responses: evaluate .NET 11, apply the applicable servicing and security fixes, and migrate applications still depending on .NET 8 or .NET 9.

In September, I wrote [“.NET 11 RC1 Is Here. Is Your Upgrade Process Ready?”](/post/2026/09/12/net-11-rc1-is-here-is-your-upgrade-process-ready). I argued that upgrade readiness should be an ongoing evaluation rather than a project triggered by an approaching end-of-support deadline. Today's releases put that approach to the test.

## What Did Microsoft Release on November 10, 2026?

Here is a snapshot of the runtime and SDK releases, along with their support status, on November 10, 2026:

| .NET version | Runtime release | Latest SDK | Support status |
| --- | --- | --- | --- |
| .NET 11 | `11.0.0` | `11.0.100` | New, supported STS release |
| .NET 10 | `10.0.15` | `10.0.404` | Supported LTS release; November servicing update |
| .NET 9 | `9.0.23` | `9.0.321` | Final servicing update; end of support |
| .NET 8 | `8.0.34` | `8.0.428` | Final servicing update; end of support |

Microsoft's November releases include both runtime and SDK updates. The table shows the latest SDK version listed for each release, not every SDK feature band serviced that day. Additional SDK feature bands also received updates, as reflected in Microsoft's [official .NET release metadata](https://github.com/dotnet/core/blob/main/release-notes/releases-index.json) and release notes.

SDK version numbers are different from runtime version numbers. For example, SDK `10.0.404` includes runtime `10.0.15`. Installing an updated SDK also installs its corresponding runtime, but it does not retarget existing projects or update deployed applications. SDK servicing can independently update build tools, compilers, and templates.

Microsoft's [November servicing announcement](https://devblogs.microsoft.com/dotnet/dotnet-and-dotnet-framework-november-2026-servicing-updates/) provides release notes, downloads, container-image information, and security advisories.

## Why Release .NET 8 and .NET 9 Updates on Their End-of-Support Date?

Microsoft aligns .NET end-of-support dates with Patch Tuesday. November 10 was both the published end-of-support date for .NET 8 and .NET 9 and the date Microsoft released their final patches.

A *servicing update* is a cumulative patch release that can include security fixes, non-security fixes, or both, depending on the version's support phase. During the final six months of a release's normal lifecycle, known as its *maintenance support* phase, servicing is limited to security fixes.

A *final servicing update* is the last patch delivered under that normal lifecycle. It does **not** extend support beyond the published date.

An application running .NET 8.0.34 can have the latest available .NET 8 runtime patch and still depend on an unsupported release. The application does not suddenly stop working, but Microsoft will not provide subsequent fixes for that release under its normal support policy.

The reverse distinction matters, too: being on a *supported* release does not mean you can ignore servicing updates. Microsoft's [support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) requires systems to remain current on released patches to qualify for support.

**Should you install the final .NET 8 or .NET 9 patches if you cannot upgrade immediately?** Yes. Apply the final available fixes to reduce risk while you complete the migration. Just don't mistake the latest available patch for continued support.

## Do the November Security Fixes Require More Than a Runtime Update?

**Yes, in some cases.** Microsoft's [November security advisories](https://devblogs.microsoft.com/dotnet/dotnet-and-dotnet-framework-november-2026-servicing-updates/) cover vulnerabilities in .NET, ASP.NET Core, and related tooling. Some fixes require action beyond installing a new shared runtime.

Two examples are particularly useful:

- **A NuGet package update ([CVE-2026-118747](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-118747)).** This denial-of-service vulnerability affects `System.Formats.Cbor`; Microsoft's November summary lists .NET 8, 9, 10, and 11. For the .NET 9 package line, the corrected package version is `9.0.24`, while the final .NET 9 runtime is `9.0.23`. Installing runtime `9.0.23` alone does not update an affected package dependency. Check the advisory for the applicable fixed package version, update the dependency, then rebuild and redeploy the application.
- **Tooling and previously generated code ([CVE-2026-118741](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-118741)).** This ASP.NET Core elevation-of-privilege vulnerability concerns Identity scaffolding and templates; Microsoft's November summary lists .NET 8, 9, and 10. Updating the affected scaffolding or template packages, or updating the SDK that supplies the templates, addresses future code generation. Previously generated vulnerable application code also needs to be corrected, rebuilt, and redeployed. A runtime patch cannot repair source code that was generated earlier.

The lesson is to follow each advisory's **affected-product list and remediation instructions**, rather than assuming the newest runtime installer resolves every issue.

Your deployment model also determines how a runtime fix reaches an application:

- **Framework-dependent applications** normally use the latest installed compatible shared-runtime patch at their next start, subject to runtime-selection settings.
- **Self-contained applications** include their own runtime. They need to be rebuilt or republished using the patched runtime, then redeployed.
- **Containers** need updated images and redeployment. Patching the host's shared .NET installation does not update a runtime packaged inside an image.

## What's New in .NET 11?

.NET 11 is generally available as a **Standard Term Support (STS)** release, not a preview. Microsoft's [release announcement](https://devblogs.microsoft.com/dotnet/announcing-dotnet-11/) highlights several improvements:

- **C# 15:** Union types and closed hierarchies make it easier to model a known set of application states and check how they are handled.
- **SDK and build tooling:** A Native AOT command-line host and a warm MSBuild server reduce overhead in everyday development workflows.
- **ASP.NET Core:** Asynchronous validation, OpenAPI 3.2 support, and new capabilities for Blazor and SignalR.
- **Runtime and libraries:** Performance optimizations, built-in Zstandard compression, and additional APIs for common tasks.

These are reasons to evaluate .NET 11, not automatic reasons to deploy it immediately. Compatibility, dependency readiness, automated tests, hosting support, and operational requirements should drive adoption decisions.

## Should You Upgrade to .NET 10 or .NET 11?

With .NET 8 and .NET 9 out of support, both .NET 10 and .NET 11 are supported upgrade destinations.

| Release | Support model | Published end of support |
| --- | --- | --- |
| .NET 10 | Long Term Support (LTS) | November 14, 2028 |
| .NET 11 | Standard Term Support (STS) | November 14, 2028 |

According to [Microsoft's .NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) and the [.NET 11 release notes](https://github.com/dotnet/core/blob/main/release-notes/11.0/README.md), both releases have the same published end-of-support date. LTS releases receive three years of support; STS releases receive two. Microsoft says they have the same quality and servicing standards.

**Choosing .NET 11 provides newer capabilities, not additional support runway over .NET 10.**

For organizations following an LTS-oriented production strategy, .NET 10 remains a sensible default. Teams that need .NET 11 features can adopt it as a supported production release after validating their applications and dependencies. Both can be reasonable choices.

## Can Installing .NET 11 Change Which SDK Builds Your Existing Projects?

**Yes.** When no applicable `global.json` controls SDK selection, the `dotnet` CLI normally uses the highest installed SDK available to that host. Installing .NET 11 SDK `11.0.100` into your normal .NET installation can therefore cause commands such as `dotnet build` and `dotnet test` to use .NET 11, even if a project still targets `net8.0` or `net10.0`.

A `global.json` file can specify an SDK version and roll-forward policy, giving a repository more control over its build toolchain. The CLI searches for this file starting from the current working directory and moving up through parent directories. You can check the selected SDK with `dotnet --version` from the directory where you normally build the project.

I explored this in [“Before You Upgrade .NET, Do You Know What Is Building It?”](/post/2026/09/16/before-you-upgrade-dotnet-do-you-know-what-is-building-it), including why two developers can build the same project with different SDKs and how `global.json` makes that choice intentional. Microsoft documents the selection rules in its [SDK guidance](https://learn.microsoft.com/en-us/dotnet/core/versions/selection) and [`global.json` reference](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json).

A newer SDK can change the compiler, analyzers, build tools, and SDK defaults used for an existing project. However, **the default C# language version still follows the project's target framework**, unless the project explicitly overrides it with `LangVersion`. For example, a `net8.0` project defaults to C# 12, not C# 15, when built with the .NET 11 SDK. Microsoft documents this in its [C# language versioning guidance](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning).

This is a change to the development toolchain, not an automatic upgrade of the application's target framework or deployed runtime.

This is one reason I built [Isolated .NET SDK](https://github.com/infoconex/isolated-dotnet-sdk). It installs an exact SDK version into a separate, user-owned directory without permanently modifying the normal `PATH`, so I can test .NET 11 by invoking its isolated `dotnet` host explicitly. SDK selection rules still apply when using that host. If a repository's `global.json` pins a different SDK, I need to account for that pin in the test setup; using an isolated host does not bypass it. The [earlier article on testing an SDK without installing it system-wide](/post/2026/09/20/how-to-test-a-new-dotnet-sdk-without-installing-it-system-wide) walks through that distinction.

## How Can You Find Applications Still Using .NET 8 or .NET 9?

Start by checking the SDK and shared runtimes visible to the `dotnet` host you invoke. Microsoft's [installed-version guide](https://learn.microsoft.com/en-us/dotnet/core/install/how-to-detect-installed-versions) documents the inventory commands:

```bash
dotnet --version
dotnet --list-sdks
dotnet --list-runtimes
```

`dotnet --version` reports the SDK selected in the current working-directory context. The other commands list SDKs and shared runtimes visible to that host. Deliberately isolated installations may not appear in its inventory.

These commands **do not tell you which runtime each production application actually uses**. To establish that, distinguish three kinds of evidence:

- **Build target:** Examine `<TargetFramework>` or `<TargetFrameworks>` in project files. Check `global.json` to understand SDK selection, not runtime selection.
- **Runtime requirements:** Inspect deployed `*.runtimeconfig.json` files and runtime roll-forward configuration for framework-dependent applications. By default, a `net8.0` application will not roll forward to a newer major runtime; `RollForward`, `DOTNET_ROLL_FORWARD`, or `--roll-forward` can change that behavior. See Microsoft's [runtime-selection documentation](https://learn.microsoft.com/en-us/dotnet/core/versions/selection).
- **Actual deployment:** Verify hosting environments, application diagnostics, deployed container images, and self-contained application artifacts to understand what is running.

In [“Managing .NET SDKs: Installation Was Just the Beginning,”](/post/2026/10/21/managing-dotnet-sdks-installation-was-just-the-beginning) I showed how Isolated .NET SDK can list, verify, and audit SDK installations against Microsoft's release information. That is useful for understanding a development environment, but an SDK inventory is not a complete inventory of production application dependencies.

One terminology reminder: **.NET Framework 4.8 is not .NET 8.** .NET Framework 4.8 follows the lifecycle of the Windows version on which it is installed. The end of support for .NET 8 and .NET 9 does not retire .NET Framework 4.8.

## What Should Development Teams Do Now?

I would prioritize four actions:

1. **Find unsupported workloads.** Identify applications targeting or running .NET 8 or .NET 9, including containers and self-contained deployments. Prioritize upgrades by exposure and business criticality.
2. **Apply the relevant fixes.** Bring .NET 10 environments up to the November servicing level. Apply the final .NET 8 or .NET 9 patches where an immediate upgrade is not possible, and follow security advisories for NuGet packages, tooling, and generated code.
3. **Evaluate .NET 11.** Run builds and automated tests, check dependencies and hosting support, and decide whether its new capabilities justify adoption. My earlier articles on [clean-machine builds](/post/2026/09/17/can-you-build-your-dotnet-application-on-a-clean-machine) and [testing SDKs without system-wide installation](/post/2026/09/20/how-to-test-a-new-dotnet-sdk-without-installing-it-system-wide) describe useful preparation steps. Remaining on supported .NET 10 is also a valid outcome.
4. **Make lifecycle checks routine.** Track support dates and servicing levels across application and build inventories. Review framework currency before deadlines create urgency.

## A New Release Is an Opportunity. End of Support Is a Deadline.

In the [opening article of this series](/post/2026/09/12/net-11-rc1-is-here-is-your-upgrade-process-ready), I described a simple operating rhythm: **RC is preflight, GA is the decision point, and EOS is the execution deadline.**

November 10 illustrates why that distinction matters. .NET 11 is ready to evaluate. .NET 10 has servicing fixes to apply. .NET 8 and .NET 9 have received their final updates. Applications still depending on them need to move to a supported release.

A new release should trigger an evaluation, not an emergency migration. Servicing updates should be normal maintenance. An end-of-support date should confirm a transition already underway, not start the discovery process.

That's the goal of the [Staying Current with .NET](https://coding.infoconex.com/series/staying-current-with-dotnet/) series: make framework currency a routine engineering practice rather than a recurring upgrade crisis.

## References

- [Microsoft: Announcing .NET 11](https://devblogs.microsoft.com/dotnet/announcing-dotnet-11/)
- [Microsoft: November 2026 .NET servicing updates](https://devblogs.microsoft.com/dotnet/dotnet-and-dotnet-framework-november-2026-servicing-updates/)
- [Microsoft: .NET and .NET Core support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core)
- [Microsoft: .NET 11 release notes](https://github.com/dotnet/core/blob/main/release-notes/11.0/README.md)
- [Microsoft: Select which .NET version to use](https://learn.microsoft.com/en-us/dotnet/core/versions/selection)
- [Microsoft: Check installed .NET versions](https://learn.microsoft.com/en-us/dotnet/core/install/how-to-detect-installed-versions)
- [Microsoft: .NET Framework lifecycle FAQ](https://learn.microsoft.com/en-us/lifecycle/faq/dotnet-framework)
