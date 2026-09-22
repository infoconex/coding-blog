---
title: "ASP.NET MVC3 Preview 1 - Released Today"
date: "2010-07-27"
description: "You can download the new ASP.NET MVC3 Preview 1 here"
tags: []
slug: "asp-net-mvc3-preview-1-released-today"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2010/07/27/ASPNET-MVC3-Preview-1-Released-Today"
permalink: "/post/2010/07/27/ASPNET-MVC3-Preview-1-Released-Today"
legacyPaths: ["/post/2010/07/27/ASPNET-MVC3-Preview-1-Released-Today"]
---
ASP.NET MVC 3 Preview 1 was released in July 2010. Scott Guthrie's archived [Introducing ASP.NET MVC 3 (Preview 1)](https://prod-static-asp-blogs.azurewebsites.net/scottgu/introducing-asp-net-mvc-3-preview-1/) post preserves the release details.

This is the next major release of the ASP.NET MVC framework and is fully backwards compatible with projects using ASP.NET MVC2.

ASP.NET MVC3 has all the great features of the previous releases and builds on top of that foundational work. So everything you previously used and learned still apply.

So what is new?

**Multiple View Engines** - Views now allow you to select the desired view engines you have installed on your machine. Example (ASPX, Razor, NHaml, Spark

**Global Filters** allow developers to apply filter logic across all controllers in an application.

**Dynamic ViewModel Property** enables you to use the new dynamic language support to pass ViewData in a cleaner syntax.

**New ActionResult types** - HttpNotFound, HttpRedirectResult and HttpStatusCodeResult

**Built-in JSON binding** support to enable action methods to receive JSON-encoded data and bind it to action method parameters.

**Model Validation** improvements added support for the new .NET 4 DataAnnotations metadata attributes, IValidateObject interface to do custom validation at the class level.

**Dependency injection** - Better support for using Dependency Injection and IOC containers. You can now use dependency injection in Controllers, Views and Action Filters with future support for Model Binders, Value Providers, Validation Providers and Model metadata Providers.

Brad Wilson wrote a four-part series about MVC3 dependency injection support. The original Typepad posts are no longer online, but Microsoft still preserves the [ASP.NET MVC 3 dependency resolver API documentation](https://learn.microsoft.com/en-us/previous-versions/aspnet/gg401972%28v%3Dvs.118%29), and Scott Guthrie's archived overview above provides the release context.

I am excited to see the improvements and look forward to upgrading my current projects to use some of the new features.
