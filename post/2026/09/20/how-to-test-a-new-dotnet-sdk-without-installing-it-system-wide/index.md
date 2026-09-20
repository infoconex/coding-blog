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

The Windows example uses PowerShell and Microsoft's [`dotnet-install.ps1`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script). The Linux and macOS example uses Bash and Microsoft's [`dotnet-install.sh`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script).

I tested this flow in both a Linux devcontainer and PowerShell 7 on a Windows 11 host.

In both cases, the wrapper script will:

- show the SDKs already available through the normal .NET installation;
- check whether the requested isolated SDK already exists;
- warn if the exact SDK is already installed normally and ask whether an isolated copy is still wanted;
- download Microsoft's current installation script;
- install the exact SDK into its own version-specific directory without modifying `PATH`;
- verify the isolated installation without depending on SDK selection from the current working directory.

The wrapper scripts use the prefix below for their own output so it is easy to distinguish from Microsoft's installer output:

```text
isolated-dotnet-sdk:
```

Microsoft's installer continues to use its own prefix:

```text
dotnet-install:
```

## Windows: Install with PowerShell

Microsoft provides [`dotnet-install.ps1`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script) for Windows.

Save the following as:

```text
install-isolated-dotnet-sdk.ps1
```

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

function Write-Info {
    param([string]$Message)

    Write-Host 'isolated-dotnet-sdk:' -ForegroundColor Cyan -NoNewline
    Write-Host " $Message"
}

function Write-WarningMessage {
    param([string]$Message)

    Write-Host 'isolated-dotnet-sdk:' -ForegroundColor Yellow -NoNewline
    Write-Host " $Message"
}

function Write-Success {
    param([string]$Message)

    Write-Host 'isolated-dotnet-sdk:' -ForegroundColor Green -NoNewline
    Write-Host " $Message"
}

Write-Info "Target SDK: $SdkVersion"
Write-Info "Isolated install directory: $InstallDir"
Write-Host

Write-Info 'Checking SDKs installed through the normal dotnet host...'

$DotNetCommand = Get-Command dotnet -ErrorAction SilentlyContinue
$InstalledVersions = @()

if ($DotNetCommand) {
    $InstalledSdks = dotnet --list-sdks
    $InstalledSdks
    Write-Host

    $InstalledVersions = $InstalledSdks |
        ForEach-Object { ($_ -split '\s+')[0] }
}
else {
    Write-WarningMessage 'No system dotnet installation was found.'
    Write-Host
}

Write-Info 'Checking for an existing isolated SDK...'

if (Test-Path $IsolatedDotNet) {
    $IsolatedVersions = & $IsolatedDotNet --list-sdks |
        ForEach-Object { ($_ -split '\s+')[0] }

    if ($IsolatedVersions -contains $SdkVersion) {
        Write-Success "Isolated SDK $SdkVersion is already installed."
        Write-Info "Location: $InstallDir"
        return
    }
}

Write-Info 'No existing isolated copy was found.'
Write-Host

# If the exact SDK is already installed normally, confirm that an
# additional isolated copy is really wanted.
if ($InstalledVersions -contains $SdkVersion) {
    Write-WarningMessage ".NET SDK $SdkVersion is already installed normally."

    $Response = Read-Host `
        'isolated-dotnet-sdk: Install an isolated copy too? [y/N]'

    if ($Response -notmatch '^[Yy]$') {
        Write-Info 'Installation cancelled.'
        return
    }

    Write-Host
}

Write-Info 'Creating isolated SDK root directory...'

New-Item `
    -ItemType Directory `
    -Path $SdkRoot `
    -Force | Out-Null

Write-Info "Downloading Microsoft's dotnet-install.ps1 script..."

Invoke-WebRequest `
    'https://dot.net/v1/dotnet-install.ps1' `
    -OutFile $InstallScript

Write-Info "Installing .NET SDK $SdkVersion..."

& $InstallScript `
    -Version $SdkVersion `
    -InstallDir $InstallDir `
    -NoPath

Write-Host
Write-Info 'Verifying the isolated SDK...'

& $IsolatedDotNet --list-sdks

Write-Host
Write-Success 'Isolated SDK installation completed successfully.'
Write-Info "Location: $InstallDir"
```

Before installing .NET 11 RC1, the wrapper might display the SDKs already installed normally:

```text
8.0.425 [C:\Program Files\dotnet\sdk]
9.0.318 [C:\Program Files\dotnet\sdk]
10.0.401 [C:\Program Files\dotnet\sdk]
```

After installation, verification should show the isolated SDK under its own directory:

```text
11.0.100-rc.1.26425.128 [C:\Users\<user>\dotnet-sdks\11.0.100-rc.1.26425.128\sdk]
```

If the exact SDK is already installed normally, the wrapper asks before creating another copy:

```text
isolated-dotnet-sdk: .NET SDK 10.0.401 is already installed normally.
isolated-dotnet-sdk: Install an isolated copy too? [y/N]
```

Pressing Enter leaves things as they are. An isolated duplicate is created only when explicitly requested.

## Linux and macOS: Install with Bash

Microsoft provides [`dotnet-install.sh`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script) for Linux and macOS.

Save the following as:

```text
install-isolated-dotnet-sdk.sh
```

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

# Use color only when writing to an interactive terminal.
if [[ -t 1 ]]; then
    CYAN='\033[0;36m'
    YELLOW='\033[0;33m'
    GREEN='\033[0;32m'
    RESET='\033[0m'
else
    CYAN=''
    YELLOW=''
    GREEN=''
    RESET=''
fi

info() {
    printf "%b%s%b %s\n" \
        "$CYAN" \
        "isolated-dotnet-sdk:" \
        "$RESET" \
        "$1"
}

warn() {
    printf "%b%s%b %s\n" \
        "$YELLOW" \
        "isolated-dotnet-sdk:" \
        "$RESET" \
        "$1"
}

success() {
    printf "%b%s%b %s\n" \
        "$GREEN" \
        "isolated-dotnet-sdk:" \
        "$RESET" \
        "$1"
}

info "Target SDK: $SDK_VERSION"
info "Isolated install directory: $INSTALL_DIR"
echo

info "Checking SDKs installed through the normal dotnet host..."
INSTALLED_VERSIONS=""

if command -v dotnet >/dev/null 2>&1; then
    INSTALLED_SDKS="$(dotnet --list-sdks)"
    echo "$INSTALLED_SDKS"
    echo

    INSTALLED_VERSIONS="$(
        echo "$INSTALLED_SDKS" |
        awk '{print $1}'
    )"
else
    warn "No system dotnet installation was found."
    echo
fi

info "Checking for an existing isolated SDK..."

if [[ -x "$ISOLATED_DOTNET" ]]; then
    if "$ISOLATED_DOTNET" --list-sdks |
        awk '{print $1}' |
        grep -Fxq "$SDK_VERSION"; then

        success "Isolated SDK $SDK_VERSION is already installed."
        info "Location: $INSTALL_DIR"
        exit 0
    fi
fi

info "No existing isolated copy was found."
echo

# If the exact SDK is already installed normally, confirm that an
# additional isolated copy is really wanted.
if echo "$INSTALLED_VERSIONS" | grep -Fxq "$SDK_VERSION"; then
    warn ".NET SDK $SDK_VERSION is already installed normally."

    read -r -p \
        "isolated-dotnet-sdk: Install an isolated copy too? [y/N] " \
        RESPONSE

    if [[ ! "$RESPONSE" =~ ^[Yy]$ ]]; then
        info "Installation cancelled."
        exit 0
    fi

    echo
fi

info "Creating isolated SDK root directory..."
mkdir -p "$SDK_ROOT"

info "Downloading Microsoft's dotnet-install.sh script..."
curl -sSL \
    https://dot.net/v1/dotnet-install.sh \
    -o "$INSTALL_SCRIPT"

info "Installing .NET SDK $SDK_VERSION..."
bash "$INSTALL_SCRIPT" \
    --version "$SDK_VERSION" \
    --install-dir "$INSTALL_DIR" \
    --no-path

echo
info "Verifying the isolated SDK..."
"$ISOLATED_DOTNET" --list-sdks

echo
success "Isolated SDK installation completed successfully."
info "Location: $INSTALL_DIR"
```

On Linux, the isolated SDK will be under a path like:

```text
/home/<user>/dotnet-sdks/11.0.100-rc.1.26425.128/
```

On macOS:

```text
/Users/<user>/dotnet-sdks/11.0.100-rc.1.26425.128/
```

Microsoft documents both platform-specific installers in the [.NET install scripts reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script).

## Why Verify with `--list-sdks` Instead of `--version`?

This is one of the details I did not fully appreciate until testing the scripts against a real repository.

I first verified the isolated executable with:

```text
dotnet --version
```

That works from a neutral directory.

But the .NET CLI still performs normal SDK resolution based on the current working directory. If I invoke the isolated `dotnet` executable while standing inside a repository with a `global.json`, that repository can still request a different SDK.

For example, the repository I used for testing pins:

```text
10.0.401
```

The isolated installation contains only:

```text
11.0.100-rc.1.26425.128
```

Running the isolated executable's `--version` command from that repository therefore failed because the repository requested an SDK that did not exist inside that isolated installation.

That is why the wrapper scripts verify with:

```text
dotnet --list-sdks
```

instead. Listing the SDKs tells us what is physically available under that isolated host without requiring the CLI to select one for the current repository.

This distinction matters again later when we intentionally connect the isolated SDK to an existing repository.

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

We can inspect a specific isolated installation directly.

On Windows:

```powershell
& "$HOME\dotnet-sdks\11.0.100-rc.1.26425.128\dotnet.exe" --list-sdks
```

On Linux or macOS:

```bash
"$HOME/dotnet-sdks/11.0.100-rc.1.26425.128/dotnet" --list-sdks
```

There is no need to uninstall one isolated SDK before testing another.

## Give the SDK a Quick Test

Before using a prerelease SDK with an existing repository, I want to prove that it can create, build, and run a simple application.

The important detail is where I run that test.

I do not want an existing repository's `global.json` influencing this experiment, so I use a neutral temporary directory.

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

At that point, I know the isolated SDK itself can create, restore, build, and run a .NET 11 application before involving an existing repository.

There is one other detail worth calling out.

An isolated SDK installation does not mean the .NET CLI can never create per-user state. During my Windows test, the first CLI invocation ran the normal .NET first-time experience and installed an ASP.NET Core HTTPS development certificate.

The isolation here is about keeping the SDK files out of the normal system-wide installation and keeping the SDK off `PATH`. It is not a hermetic sandbox around every side effect the .NET CLI may produce.

## Why Doesn't the Normal SDK List Show It?

After installing the isolated SDK, the normal system command still reports only the SDKs installed in the normal locations.

For example, on the Windows machine I used for testing:

```powershell
dotnet --list-sdks
```

still returned:

```text
8.0.425 [C:\Program Files\dotnet\sdk]
9.0.318 [C:\Program Files\dotnet\sdk]
10.0.401 [C:\Program Files\dotnet\sdk]
```

The isolated .NET 11 SDK did not appear there.

That is expected.

We deliberately placed it outside the locations being searched by the normal system .NET host.

Starting with .NET 10, `global.json` supports `sdk.paths`, which can tell the .NET host to search additional SDK locations. Microsoft documents this in both the [`global.json` overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) and [Test prerelease .NET SDKs locally](https://learn.microsoft.com/en-us/dotnet/core/tools/test-prerelease-sdk-locally).

That is where this becomes useful for an existing repository.

I am leaving that configuration for the next article.

## Cleanup

Removing the isolated SDK is still directory-based, but there is one practical detail to handle first.

A build can leave MSBuild and the C# compiler build server running. On Windows, those processes kept files inside the isolated SDK locked when I first tried to delete the directory.

The supported CLI command for shutting down build servers is [`dotnet build-server shutdown`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build-server).

Run that command from a neutral directory as well so an existing repository's `global.json` does not affect SDK resolution.

On Windows:

```powershell
$DotNet = "$HOME\dotnet-sdks\11.0.100-rc.1.26425.128\dotnet.exe"

Set-Location $env:TEMP
& $DotNet build-server shutdown

Remove-Item `
    -Path (Join-Path $HOME 'dotnet-sdks\11.0.100-rc.1.26425.128') `
    -Recurse `
    -Force
```

On Linux or macOS:

```bash
DOTNET="$HOME/dotnet-sdks/11.0.100-rc.1.26425.128/dotnet"

cd /tmp
"$DOTNET" build-server shutdown

rm -rf "$HOME/dotnet-sdks/11.0.100-rc.1.26425.128"
```

In both of my tests, shutting down the build servers first allowed the isolated SDK directory to be removed cleanly.

The Microsoft installer script itself remains under the SDK root:

```text
Windows
C:\Users\<user>\dotnet-sdks\dotnet-install.ps1

Linux/macOS
~/dotnet-sdks/dotnet-install.sh
```

That file can remain for future isolated SDK installs, or it can be removed separately if it is no longer needed.

Other isolated SDK versions remain untouched:

```text
dotnet-sdks/
    10.0.401/
    11.0.100-rc.2.xxxxx.xxx/
```

## Now We Have a Tool We Can Use

We now have a .NET 11 RC1 SDK that is separate from the normal system-wide installation and is only used when we explicitly choose it.

More importantly, we have tested the behavior rather than just assuming it works.

The normal `dotnet` host continued to report the same SDKs before and after the isolated installation. The isolated host saw only its own SDK. We created, restored, built, and ran a .NET 11 application with it on both Linux and Windows. We also removed it again without affecting the normal SDK installation.

Installing it was not the goal.

The goal is having newer tooling available without changing the SDK installation our normal development environment depends on.

In the next article, I am going to use this SDK to answer a more important question:

> Before upgrading a .NET application, do we actually know what we are upgrading?

We will intentionally connect an existing repository to the isolated SDK, inventory its projects, frameworks, packages, build configuration, development tools, tests, and external dependencies, and then restore the repository to its original SDK configuration.

The isolated SDK gives us the tool.

The next step is using it to understand the application before we change it.

## Microsoft References

- [.NET install scripts](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script)
- [Test prerelease .NET SDKs locally](https://learn.microsoft.com/en-us/dotnet/core/tools/test-prerelease-sdk-locally)
- [`dotnet build-server`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build-server)
- [`global.json` overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json)
- [.NET 11 RC1 release notes](https://github.com/dotnet/core/blob/main/release-notes/11.0/preview/rc1/11.0.0-rc.1.md)
- [.NET 11 downloads](https://dotnet.microsoft.com/en-us/download/dotnet/11.0)
