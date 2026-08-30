---
title: "Out With the Old, In With the New: Rebuilding Coding"
date: "2026-08-29"
description: "After years on BlogEngine.NET, Coding has a new design and a new foundation built on Jekyll, GitHub Pages, Git, and Markdown."
tags: ["Blogging", "GitHub Pages", "Jekyll", "Markdown", "Software Development"]
slug: "out-with-the-old-in-with-the-new-rebuilding-coding"
author: "Jim Scott"
published: true
permalink: "/post/2026/08/29/out-with-the-old-in-with-the-new-rebuilding-coding"
---

There is something slightly dangerous about being a software developer and owning a website.

Eventually you look at it and think:

*I should probably rebuild this.*

That thought can sit around for years.

In my case, it finally won.

The Coding blog has a new design, a new home underneath it, and a very different way of being maintained and published.

Considering this site has been around since 2008, I think it was probably time.

## The Old Coding Blog

For years, the site ran on [BlogEngine.NET](https://github.com/BlogEngine/BlogEngine.NET).

It did what I needed it to do.

I could write articles, organize them into categories and tags, maintain an archive, and publish whatever problem or idea I happened to be working through at the time.

Over the years, that turned into a fairly large collection of writing about .NET, C#, SQL Server, Windows, architecture, development practices, virtualization, GitHub, AI, and quite a few other things.

BlogEngine.NET provided a home for all of it.

But eventually the age of the site started to show.

![The previous version of Jim Scott's Coding Blog.](images/coding-blog-before.png)

*The previous version of the blog, captured from the Internet Archive.*

The old design had the characteristics you would expect from a blog that had evolved over a long period of time.

A large author sidebar.

Traditional blog navigation.

Categories and archives organized around the conventions of an earlier generation of blogging platforms.

A layout that worked, but increasingly felt like something I was maintaining because it was already there rather than because it was how I would build the site today.

There is nothing particularly wrong with that.

Software that keeps doing its job for years deserves some respect.

But there is also a point where continuing to maintain the old thing costs more than replacing it with something simpler.

I had reached that point.

## The New Coding

The new site takes a very different approach.

![The redesigned Coding homepage at coding.infoconex.com.](images/coding-blog-after.png)

*The redesigned Coding homepage at coding.infoconex.com.*

The first and most obvious change is the design.

The new homepage is much more focused on the writing itself.

There is less surrounding chrome, clearer navigation, better support for browsing the archive, improved handling of tags, built-in search, and a theme system that lets the site change its appearance without changing its structure.

The new design also reflects what the blog has become.

When I started writing here, a lot of the content was about solving individual development problems: a .NET API, a SQL Server technique, something strange in Windows, or a piece of C# that took longer to figure out than it should have.

I still write those kinds of articles.

But over time the subjects have expanded into software architecture, engineering practices, development tooling, AI, automation, and lessons learned from building and operating software over a long period of time.

The new site needed to accommodate both.

It needed to preserve the old articles while giving the newer writing a better home.

## More Than a Redesign

The visual change is only half of this project.

The bigger change is underneath it.

I moved the blog from **BlogEngine.NET to GitHub Pages**, using **Jekyll** to build the site and **Markdown files as the source for the articles**.

That fundamentally changes how I maintain the blog.

The old model was a blogging application.

The new model is a repository.

An article is now just a text file.

For example, the article you are reading lives in a structure similar to this:

```text
post/
└── 2026/
    └── 08/
        └── 29/
            └── out-with-the-old-in-with-the-new-rebuilding-coding/
                ├── index.md
                └── images/
```

At the top of that Markdown file is a small amount of metadata:

```yaml
---
title: "Out With the Old, In With the New: Rebuilding Coding"
date: "2026-08-29"
tags:
  - Blogging
  - GitHub Pages
  - Jekyll
  - Markdown
published: true
---
```

Everything after that is the article.

Plain text.

Markdown.

No special editor is required, and the content is not dependent on the internals of a particular blogging platform.

Jekyll takes those files and turns them into the finished website. GitHub Pages publishes the result.

For a software engineering blog, this workflow feels considerably more natural.

## The Blog Is Now Source Code

One of the things I like most about the new approach is that the website is maintained much more like any other software project.

The articles are version controlled.

The layouts are version controlled.

The CSS is version controlled.

The configuration is version controlled.

If I change an article, Git shows me exactly what changed.

If I change the layout, I have a history of that change.

If I break something, I can see when it happened and what caused it.

There is no separate mental model for "working on the blog."

I clone the repository, make a change, commit it, and push it.

That is already a workflow I use every day.

It also means the repository is the source of truth for the site.

The published website can be rebuilt from what is stored in Git.

That simplicity was one of the main reasons I wanted to make the move.

## Markdown as the Long-Term Format

Moving the articles to Markdown was just as important as moving the site to GitHub Pages.

A blog design will eventually become old.

This new one will too.

That is just how websites work.

But the writing should not have to be reinvented every time the presentation changes.

Markdown gives me a fairly durable separation between the content and the system displaying it.

An article written today is fundamentally just a text document.

If I eventually decide that Jekyll is no longer the right way to build the site, the articles are still Markdown files sitting in Git.

I can move them somewhere else.

I can process them with scripts.

I can search them with normal development tools.

I can update hundreds of them programmatically if I need to.

That last point became particularly useful during the migration.

## Moving Years of History

Starting a new static blog is easy.

Migrating one that has been accumulating content since 2008 is a different problem.

I did not want the redesign to mean throwing away the history of the site.

Quite the opposite.

One of the goals was to make that history easier to navigate.

That meant bringing the existing articles forward, preserving their publication dates and URLs wherever practical, cleaning up inconsistent metadata, normalizing tags, reconnecting article series, and making sure older writing still had a place in the new structure.

Some of those articles describe technologies that are no longer current.

That's fine.

They are still part of the history of the site, and in some cases they are part of the history of how we built software at the time.

Looking through the archive now creates an interesting timeline.

There are articles about technologies and problems from earlier versions of .NET sitting beside articles about modern architecture, GitHub automation, AI-assisted development, and the problems we are solving today.

I like that.

Software changes quickly enough that a long-running technical blog eventually becomes a record of that change.

I did not want a redesign to erase it.

## Fewer Moving Parts

There is another benefit to the new architecture that I appreciate more as time goes on: there simply isn't much application infrastructure involved anymore.

The site doesn't need to behave like a traditional blogging application just because it contains a blog.

Most of the content is static.

An article doesn't need application logic to display it.

It needs HTML.

Jekyll generates that HTML ahead of time, and GitHub Pages serves it.

That's a very different architecture from running a full application to dynamically produce pages whose contents rarely change.

For this site, static generation is a much better match for the problem.

There are fewer moving parts and fewer things I need to think about simply to keep old articles available.

That leaves more time for the part I actually care about.

Writing them.

## Some Things Haven't Changed

The technology behind Coding has changed considerably.

The reason for the site hasn't.

A lot of the articles here started because I encountered a problem, spent too much time figuring it out, and decided I should write down what I learned.

The theory has always been that if something cost me an afternoon, there is a reasonable chance somebody else will eventually run into the same thing.

Writing it down helps me remember it.

Sometimes it helps somebody else avoid spending the same afternoon.

That is still what I want this site to be.

Sometimes the subject will be .NET.

Sometimes architecture.

Sometimes AI.

Sometimes GitHub, automation, engineering management, or development practices.

And sometimes it will be one very specific problem that probably has no business taking as long to solve as it did.

The technology changes.

The motivation doesn't.

## Out With the Old, In With the New

BlogEngine.NET served this site for a long time.

This isn't a criticism of it.

It did the job I needed it to do, and it did that job for years.

But the way I build and maintain software has changed, and eventually it made sense for the blog to change with it.

The new Coding is simpler on the surface and simpler underneath it.

**Markdown for the content.**

**Git for the history.**

**Jekyll for the build.**

**GitHub Pages for publishing.**

And a new design wrapped around all of the writing that was already here.

The old site is retired.

The articles remain.

The archive remains.

The history remains.

They just have a new home.

Welcome to the new **Coding**.
