---
title: ".NET Core 3.0 Might Finally Be Ready for My Existing Applications"
date: "2019-09-23"
description: ".NET Core 3.0 adds Windows Forms and WPF support, making me take a more serious look at whether some existing .NET Framework applications could eventually move over."
tags: [".NET Core", ".NET", "C#"]
slug: "net-core-3-0-might-finally-be-ready-for-my-existing-applications"
author: "Jim Scott"
permalink: "/post/2019/09/23/net-core-3-0-might-finally-be-ready-for-my-existing-applications"
---
Microsoft released .NET Core 3.0 today, and this is the first release that really has me thinking about some of my existing .NET Framework applications instead of only new projects.

The biggest reason is Windows desktop support. .NET Core 3.0 now supports Windows Forms and WPF, which removes one of the obvious reasons many existing applications had to stay on the full .NET Framework.

That does not mean I am ready to start migrating everything.

There are still compatibility issues to think about, and older applications often depend on libraries or framework features that may not move cleanly. For a stable application that is working fine today, there needs to be a good reason to take on that work.

But the decision is getting more interesting.

C# 8 is also part of this release, and .NET Core continues to feel more complete each time Microsoft updates it. A few years ago I viewed .NET Core mostly as something interesting for new web applications and cross-platform development. With 3.0, the gap between it and the applications many of us already have is getting smaller.

I am still not planning any large migrations tomorrow, but I am going to start looking more seriously at which applications might make sense to move.
