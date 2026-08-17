---
title: "Decorating the tree for Christmas"
date: "2022-12-26"
description: "As a software developer, I've always been fascinated by design patterns and how they can help solve common problems in software design. This holiday season, I've been thinking a lot about how some of these patterns can…"
tags: ["design patterns", "c#"]
slug: "decorating-the-tree-for-christmas"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2022/12/26/decorating-the-tree-for-christmas"
permalink: "/post/2022/12/26/decorating-the-tree-for-christmas"
legacyPaths: ["/post/2022/12/26/decorating-the-tree-for-christmas"]
---
As a software developer, I've always been fascinated by design patterns and how they can help solve common problems in software design. This holiday season, I've been thinking a lot about how some of these patterns can be incorporated into our daily lives, just like the themes and traditions of Christmas.

One pattern that I've found particularly useful is the "Decorator" pattern. This pattern allows us to add new functionality to an existing object without altering its structure. In the spirit of Christmas, we can think of this pattern as a way to add extra decorations or ornaments to a Christmas tree without changing the tree itself. Just like how we can add various ornaments to a tree to make it more festive and personalized, the Decorator pattern allows us to add new features to an object without changing its core functionality.

Here is an example using C#

```csharp
// The base component interface
public interface ITree
{
    void Display();
}

// The concrete component classes
public class PineTree : ITree
{
    public void Display()
    {
        Console.WriteLine("I am a pine tree.");
    }
}

public class FirTree : ITree
{
    public void Display()
    {
        Console.WriteLine("I am a fir tree.");
    }
}

// The base decorator class
public abstract class TreeDecorator : ITree
{
    protected ITree tree;

    public TreeDecorator(ITree tree)
    {
        this.tree = tree;
    }

    public virtual void Display()
    {
        tree.Display();
    }
}

// Concrete decorator classes
public class ChristmasLightsDecorator : TreeDecorator
{
    public ChristmasLightsDecorator(ITree tree) : base(tree) {}

    public override void Display()
    {
        base.Display();
        Console.WriteLine("I am decorated with Christmas lights.");
    }
}

public class OrnamentsDecorator : TreeDecorator
{
    public OrnamentsDecorator(ITree tree) : base(tree) {}

    public override void Display()
    {
        base.Display();
        Console.WriteLine("I am decorated with ornaments.");
    }
}

public class GarlandDecorator : TreeDecorator
{
    public GarlandDecorator(ITree tree) : base(tree) {}

    public override void Display()
    {
        base.Display();
        Console.WriteLine("I am decorated with garland.");
    }
}

// Client code
ITree tree = new PineTree();
tree = new ChristmasLightsDecorator(tree);
tree = new OrnamentsDecorator(tree);
tree = new GarlandDecorator(tree);
tree.Display();
```

`I am a pine tree.
I am decorated with Christmas lights.
I am decorated with ornaments.
I am decorated with garland.`

This demonstrates how the decorator pattern allows you to dynamically add new behavior to an existing object by wrapping it in decorator objects that implement the same interface. Using an interface to define the base component class allows you to decorate objects of different types, as long as they implement the same interface.

Merry Christmas

A book that inspired my journey [Design Patterns Explained](https://www.amazon.com/Design-Patterns-Explained-Perspective-Oriented/dp/0321247140?crid=2Z5DYLKAXQ7BO&keywords=design+patterns+explained&qid=1674950429&sprefix=design+patterns+explained%2Caps%2C147&sr=8-1&ufe=app_do%3Aamzn1.fos.006c50ae-5d4c-4777-9bc0-4513d670b6bc&linkCode=ll1&tag=codblo-20&linkId=4e24b64e3cbeb0f3574b6183c1bf288c&language=en_US&ref_=as_li_ss_tl "Design Patterns Explained")

[![](http://ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=0321247140&Format=_SL160_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag=codblo-20&language=en_US)](https://www.amazon.com/Design-Patterns-Explained-Perspective-Oriented/dp/0321247140?crid=2Z5DYLKAXQ7BO&keywords=design+patterns+explained&qid=1674950429&sprefix=design+patterns+explained%2Caps%2C147&sr=8-1&ufe=app_do%3Aamzn1.fos.006c50ae-5d4c-4777-9bc0-4513d670b6bc&linkCode=li2&tag=codblo-20&linkId=1727183172276dc1779c74d6ed914fa5&language=en_US&ref_=as_li_ss_il)![](https://ir-na.amazon-adsystem.com/e/ir?t=codblo-20&language=en_US&l=li2&o=1&a=0321247140)
