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
You can download the new ASP.NET MVC3 Preview 1 [here](http://go.microsoft.com/fwlink/?LinkID=157073)

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

Visit Brad Wilson's article on MVC3 dependency injection support.

- [ASP.NET MVC 3 Service Location: Introduction (Part 1)](http://bradwilson.typepad.com/blog/2010/07/service-location-pt1-introduction.html)
- [ASP.NET MVC 3 Service Location: Controllers (Part 2)](http://bradwilson.typepad.com/blog/2010/07/service-location-pt2-controllers.html)
- [ASP.NET MVC 3 Service Location: Views (Part 3)](http://bradwilson.typepad.com/blog/2010/07/service-location-pt3-views.html)
- [ASP.NET MVC 3 Service Location: Filters (Part 4)](http://bradwilson.typepad.com/blog/2010/07/service-location-pt4-filters.html)

I am excited to see the improvements and look forward to upgrading my current projects to use some of the new features.
