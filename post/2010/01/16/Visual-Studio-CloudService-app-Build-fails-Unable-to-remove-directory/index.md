---
title: "Visual Studio - CloudService app \"Build fails\" Unable to remove directory."
date: "2010-01-16"
description: "While working on a CloudService application for Windows Azure, I encountered an error saying \"Unable to remove directory \"C:\\HelloAzure\\HelloAzure_WebRole\\bin\\_PublishedWebsites\". The directory is not empty."
tags: []
slug: "visual-studio-cloudservice-app-build-fails-unable-to-remove-directory"
author: "johnscott"
originalUrl: "http://coding.infoconex.com/post/2010/01/16/Visual-Studio-CloudService-app-Build-fails-Unable-to-remove-directory"
permalink: "/post/2010/01/16/Visual-Studio-CloudService-app-Build-fails-Unable-to-remove-directory"
legacyPaths: ["/post/2010/01/16/Visual-Studio-CloudService-app-Build-fails-Unable-to-remove-directory"]
---
While working on a CloudService application for Windows Azure, I encountered an error saying "Unable to remove directory "C:\HelloAzure\HelloAzure\_WebRole\bin\\_PublishedWebsites". The directory is not empty.

My version of Visual Studio is 2008 SP1, althopugh I assume the issue may be with other versions as well. The error occurs most every time I build, rebuild or publish.

I've attached a sample of the error below, note the WebRole\bin\\_PublishedWebsites directory was the only location affected and was consistent across all projects receiving the error.

This looks to be as the result of the Microsoft.CloudService.targets calls for the cleanup of the \_PublishedWebsites folder after the Webrole is compiled and it added to the .cspkg file.

![](images/build-failed-unable-to-remove-directory-publichedwebsites.png)

**In the end the issue was related to MS Forefront endpoint detection (antivirus), after adding **devenv.exe** to the excluded processes list the error was immediately resolved.**

Cheers,

John
