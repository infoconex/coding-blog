---
layout: post
title: "How to Test a New .NET SDK Without Installing It System-Wide"
date: "2026-09-20"
slug: "how-to-test-a-new-dotnet-sdk-without-installing-it-system-wide"
author: "Jim Scott"
published: false
featured: false
permalink: "/post/2026/09/20/how-to-test-a-new-dotnet-sdk-without-installing-it-system-wide"
description: "Use Microsoft's dotnet-install scripts to test an exact .NET SDK version in isolation without adding it to your normal system-wide SDK installation."
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

I want to try a newer SDK, perhaps a preview or release candidate, without adding it to my normal development environment.

As I write this, .NET 11 RC1 is available with SDK version:

```text
11.0.100-rc.1.26425.128
```

I could install it normally alongside my existing SDKs.

But I do not have to.

Microsoft provides installation scripts that let us put an SDK into a directory we choose instead of using the normal system-wide installer. Microsoft also documents this approach for [testing prerelease .NET SDKs locally](https://learn.microsoft.com/en-us/dotnet/core/tools/test-prerelease-sdk-locally).

## Keep the SDK Isolated

Before installing anything, there are three choices I want to make.

First, I want the SDK outside the normal .NET installation.

Instead of placing it somewhere like:

```text
C:\Program Files\dotnet\
```

I will keep isolated SDKs under my home directory:

```text
Windows
C:\Users\<user>\dotnet-sdks\

Linux
/home/<user>/dotnet-sdks/

macOS
/Users/<user>/dotnet-sdks/
```

Second, I want an **exact SDK version**.

If another release appears tomorrow, rerunning the setup should not silently change which SDK I am testing.

Third, I do not want the isolated SDK added to `PATH`, even for the current session.

Microsoft's installers provide options for that:

```text
Windows
-NoPath

Linux/macOS
--no-path
```

Those options prevent the install directory from being added to `PATH` for the current process or shell session. The installers do not permanently add the directory to the user's `PATH`.

The result is a simple model:

```text
Normal .NET installation
    Used normally through: dotnet

Isolated SDK
    Used explicitly through its path
```

The next two scripts automate this setup.

The Windows example uses PowerShell and Microsoft's [`dotnet-install.ps1`](https://dot.net/v1/dotnet-install.ps1). The Linux and macOS example uses Bash and Microsoft's [`dotnet-install.sh`](https://dot.net/v1/dotnet-install.sh).

In both cases, the script will:

- show the SDKs already available through the normal .NET installation;
- check whether the requested isolated SDK already exists;
- warn if the exact SDK is already installed normally and ask whether an isolated copy is still wanted;
- download Microsoft's current installation script;
- install the exact SDK into its own version-specific directory without modifying `PATH`;
- verify the isolated SDK when finished.

## Windows: Install with PowerShell

Microsoft provides [`dotnet-install.ps1`](https://dot.net/v1/dotnet-install.ps1) for Windows.

Here is the complete script:

```powershell
# SDK version to install and evaluate.
$SdkVersion = '11.0.100-rc.1.26425.128'

# Keep isolated SDKs under the current user's home directory.

# Example: C:\Users\<user>\dotnet-sdks
$SdkRoot = Join-Path $HOME 'dotnet-sdks'

# Example: C:\Users\<user>\dotnet-sdks\11.0.100-rc.1.26425.128
$InstallDir = Join-Path $SdkRoot $SdkVersion

# Example: C:\Users\<user>\dotnet-sdks\dotnet-install.ps1
$InstallScript = Join-Path $SdkRoot 'dotnet-install.ps1'

# Example:
# C:\Users\<user>\dotnet-sdks\11.0.100-rc.1.26425.128\dotnet.exe
$IsolatedDotNet = Join-Path $InstallDir 'dotnet.exe'

# Show SDKs already installed through the normal dotnet host.
$DotNetCommand = Get-Command dotnet -ErrorAction SilentlyContinue
$InstalledVersions = @()

if ($DotNetCommand) {
    Write-Host 'SDKs currently installed:'
    $InstalledSdks = dotnet --list-sdks
    $InstalledSdks
    Write-Host

    $InstalledVersions = $InstalledSdks |
        ForEach-Object { ($_ -split '\s+')[0] }
}
else {
    Write-Host 'No system dotnet installation was found.'
    Write-Host
}

# If this isolated SDK already exists, there is nothing to install.
if (Test-Path $IsolatedDotNet) {
    $ExistingVersion = & $IsolatedDotNet --version

    if ($ExistingVersion -eq $SdkVersion) {
        Write-Host "Isolated SDK $SdkVersion is already installed at:"
        Write-Host $InstallDir
        return
    }
}

# If the exact SDK is already installed normally, confirm that an
# additional isolated copy is really wanted.
if ($InstalledVersions -contains $SdkVersion) {
    $Response = Read-Host `
        ".NET SDK $SdkVersion is already installed. Install an isolated copy too? [y/N]"

    if ($Response -notmatch '^[Yy]$') {
        Write-Host 'Installation cancelled.'
        return
    }
}

# Create the root directory used for isolated SDKs.
New-Item `
    -ItemType Directory `
    -Path $SdkRoot `
    -Force | Out-Null

# Download Microsoft's current Windows installer.
Invoke-WebRequest `
    'https://dot.net/v1/dotnet-install.ps1' `
    -OutFile $InstallScript

# Install the exact SDK without adding it to PATH for this process.
& $InstallScript `
    -Version $SdkVersion `
    -InstallDir $InstallDir `
    -NoPath

# Verify the isolated SDK.
& $IsolatedDotNet --version
```

Before installing .NET 11 RC1, the script might display:

```text
SDKs currently installed:
8.0.425 [C:\Program Files\dotnet\sdk]
9.0.318 [C:\Program Files\dotnet\sdk]
10.0.401 [C:\Program Files\dotnet\sdk]
```

After installation, the final verification should return:

```text
11.0.100-rc.1.26425.128
```

The isolated SDK will be located at:

```text
C:\Users\<user>\dotnet-sdks\11.0.100-rc.1.26425.128\
```

If the exact SDK is already installed normally, the script asks before creating another copy:

```text
.NET SDK 11.0.100-rc.1.26425.128 is already installed.
Install an isolated copy too? [y/N]
```

Pressing Enter leaves things as they are. An isolated duplicate is created only when explicitly requested.

## Linux and macOS: Install with Bash

Microsoft provides [`dotnet-install.sh`](https://dot.net/v1/dotnet-install.sh) for Linux and macOS.

The Bash script follows the same rules:

```bash
#!/usr/bin/env bash

# SDK version to install and evaluate.
SDK_VERSION="11.0.100-rc.1.26425.128"

# Keep isolated SDKs under the current user's home directory.

# Example Linux: /home/<user>/dotnet-sdks
# Example macOS: /Users/<user>/dotnet-sdks
SDK_ROOT="$HOME/dotnet-sdks"

# Example: ~/dotnet-sdks/11.0.100-rc.1.26425.128
INSTALL_DIR="$SDK_ROOT/$SDK_VERSION"

# Example: ~/dotnet-sdks/dotnet-install.sh
INSTALL_SCRIPT="$SDK_ROOT/dotnet-install.sh"

# Example: ~/dotnet-sdks/11.0.100-rc.1.26425.128/dotnet
ISOLATED_DOTNET="$INSTALL_DIR/dotnet"

# Show SDKs already installed through the normal dotnet host.
INSTALLED_VERSIONS=""

if command -v dotnet >/dev/null 2>&1; then
    echo "SDKs currently installed:"
    INSTALLED_SDKS="$(dotnet --list-sdks)"
    echo "$INSTALLED_SDKS"
    echo

    INSTALLED_VERSIONS="$(
        echo "$INSTALLED_SDKS" |
        awk '{print $1}'
    )"
else
    echo "No system dotnet installation was found."
    echo
fi

# If this isolated SDK already exists, there is nothing to install.
if [[ -x "$ISOLATED_DOTNET" ]]; then
    EXISTING_VERSION="$("$ISOLATED_DOTNET" --version)"

    if [[ "$EXISTING_VERSION" == "$SDK_VERSION" ]]; then
        echo "Isolated SDK $SDK_VERSION is already installed at:"
        echo "$INSTALL_DIR"
        exit 0
    fi
fi

# If the exact SDK is already installed normally, confirm that an
# additional isolated copy is really wanted.
if echo "$INSTALLED_VERSIONS" | grep -Fxq "$SDK_VERSION"; then
    read -r -p \
        ".NET SDK $SDK_VERSION is already installed. Install an isolated copy too? [y/N] " \
        RESPONSE

    if [[ ! "$RESPONSE" =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
fi

# Create the root directory used for isolated SDKs.
mkdir -p "$SDK_ROOT"

# Download Microsoft's current Linux/macOS installer.
curl -sSL \
    https://dot.net/v1/dotnet-install.sh \
    -o "$INSTALL_SCRIPT"

# Install the exact SDK without adding it to PATH for this shell session.
bash "$INSTALL_SCRIPT" \
    --version "$SDK_VERSION" \
    --install-dir "$INSTALL_DIR" \
    --no-path

# Verify the isolated SDK.
"$ISOLATED_DOTNET" --version
```

The final verification should return:

```text
11.0.100-rc.1.26425.128
```

The SDK will be stored under:

```text
Linux
/home/<user>/dotnet-sdks/11.0.100-rc.1.26425.128/

macOS
/Users/<user>/dotnet-sdks/11.0.100-rc.1.26425.128/
```

Microsoft documents both platform-specific installers in the [.NET install scripts reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script).

## What Did We Install?

This is a complete SDK installation, not just a runtime.

It gives us the development tooling behind commands such as:

```text
dotnet restore
dotnet build
dotnet test
dotnet msbuild
dotnet package
```

along with the compiler, NuGet tooling, templates, targeting packs, and runtime components included with the SDK.

That is exactly what we want when evaluating a newer development toolchain.

## Keep Multiple SDKs Side by Side

Because each SDK lives in a directory named after its exact version, multiple isolated versions can coexist:

```text
dotnet-sdks/
    10.0.401/
    11.0.100-rc.1.26425.128/
    11.0.100-rc.2.xxxxx.xxx/
```

Choosing one is explicit.

On Windows:

```powershell
& "$HOME\dotnet-sdks\11.0.100-rc.1.26425.128\dotnet.exe" --version
```

On Linux or macOS:

```bash
"$HOME/dotnet-sdks/11.0.100-rc.1.26425.128/dotnet" --version
```

There is no need to uninstall one SDK before testing another.

## Give the SDK a Quick Test

Before using a prerelease SDK with an existing repository, I want to prove that it can create, build, and run a simple application.

On Windows:

```powershell
$DotNet = "$HOME\dotnet-sdks\11.0.100-rc.1.26425.128\dotnet.exe"

& $DotNet new console -n SdkExperiment -f net11.0
& $DotNet build .\SdkExperiment
& $DotNet run --project .\SdkExperiment
```

On Linux or macOS:

```bash
DOTNET="$HOME/dotnet-sdks/11.0.100-rc.1.26425.128/dotnet"

"$DOTNET" new console -n SdkExperiment -f net11.0
"$DOTNET" build ./SdkExperiment
"$DOTNET" run --project ./SdkExperiment
```

At this point, I know the isolated SDK itself works before involving an existing application.

The disposable project can then be deleted.

On Windows:

```powershell
Remove-Item .\SdkExperiment -Recurse -Force
```

On Linux or macOS:

```bash
rm -rf ./SdkExperiment
```

## Why Doesn't the Normal SDK List Show It?

If I run the normal system command:

```powershell
dotnet --list-sdks
```

the isolated SDK will not appear in this setup.

For example:

```text
8.0.425 [C:\Program Files\dotnet\sdk]
9.0.318 [C:\Program Files\dotnet\sdk]
10.0.401 [C:\Program Files\dotnet\sdk]
```

That is expected.

We deliberately placed the .NET 11 SDK outside the locations being searched by the normal system .NET host.

For now, we invoke the isolated copy directly.

Starting with .NET 10, `global.json` supports `sdk.paths`, which can tell the .NET host to search additional SDK locations. Microsoft documents this in both the [`global.json` overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) and [Test prerelease .NET SDKs locally](https://learn.microsoft.com/en-us/dotnet/core/tools/test-prerelease-sdk-locally).

That is where this becomes useful for an existing repository.

I am leaving that configuration for the next article.

## Cleanup

Removing an isolated SDK is simply removing its version directory.

On Windows:

```powershell
Remove-Item `
    -Path (Join-Path $HOME 'dotnet-sdks\11.0.100-rc.1.26425.128') `
    -Recurse `
    -Force
```

On Linux or macOS:

```bash
rm -rf "$HOME/dotnet-sdks/11.0.100-rc.1.26425.128"
```

Other isolated SDK versions remain untouched:

```text
dotnet-sdks/
    10.0.401/
    11.0.100-rc.2.xxxxx.xxx/
```

## Now We Have a Tool We Can Use

We now have a .NET 11 RC1 SDK that is separate from the normal system-wide installation and is only used when we explicitly choose it.

Installing it was not the goal.

The goal is having newer tooling available without changing the development environment we already depend on.

In the next article, I am going to use this SDK to answer a more important question:

> Before upgrading a .NET application, do we actually know what we are upgrading?

We will temporarily configure an existing repository to use the isolated SDK, inventory its projects, frameworks, packages, build configuration, development tools, tests, and external dependencies, and then restore the repository to its original SDK configuration.

The isolated SDK gives us the tool.

The next step is using it to understand the application before we change it.

## Microsoft References

- [.NET install scripts](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script)
- [Test prerelease .NET SDKs locally](https://learn.microsoft.com/en-us/dotnet/core/tools/test-prerelease-sdk-locally)
- [`global.json` overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json)
- [.NET 11 RC1 release notes](https://github.com/dotnet/core/blob/main/release-notes/11.0/preview/rc1/11.0.0-rc.1.md)
- [.NET 11 downloads](https://dotnet.microsoft.com/en-us/download/dotnet/11.0)
