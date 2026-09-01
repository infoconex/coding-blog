---

title: "Windows 8 Hyper-V errors with \"could not be started because the hypervisor is not running\""
date: "2013-01-08"
description: "Just recently setup a new machine with Windows 8 and decided to install Hyper-V so that I could run windows XP for some of my legacy applications that will not run under Windows 8 64 bit."
tags: ["Hyper-V", "Windows 8"]
slug: "windows-8-hyper-v-errors-with-could-not-be-started-because-the-hypervisor-is-not-running"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2013/01/08/Windows-8-Hyper-V-errors-with-could-not-be-started-because-the-hypervisor-is-not-running"
permalink: "/post/2013/01/08/Windows-8-Hyper-V-errors-with-could-not-be-started-because-the-hypervisor-is-not-running"
legacyPaths: ["/post/2013/01/08/Windows-8-Hyper-V-errors-with-could-not-be-started-because-the-hypervisor-is-not-running"]
---
Just recently setup a new machine with Windows 8 and decided to install Hyper-V so that I could run windows XP for some of my legacy applications that will not run under Windows 8 64 bit. After installing Hyper-V components I attempted to setup a new virtual machine and start the install process when I was faced with the following error: "could not be started because the hypervisor is not running"

It turned out that I needed to run the following command

bcdedit /set hypervisorlaunchtype auto

After running the above command and restarting my machine it now works. Hope this helps save someone else hours they cannot back due to this issue.
