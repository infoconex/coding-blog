---

title: "Countdown to New Year's with the Observer Pattern"
date: "2022-12-27"
description: "One design pattern that you might find fun to relate to New Year's Eve is the Observer design pattern."
tags: []
slug: "countdown-to-new-year-s-with-the-observer-pattern"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2022/12/27/countdown-to-new-year-s-with-the-observer-pattern"
permalink: "/post/2022/12/27/countdown-to-new-year-s-with-the-observer-pattern"
legacyPaths: ["/post/2022/12/27/countdown-to-new-year-s-with-the-observer-pattern"]
---
One design pattern that you might find fun to relate to New Year's Eve is the Observer design pattern. The Observer design pattern is a behavioral design pattern that defines a one-to-many dependency between objects, so that when one object changes state, all of its dependents are notified and updated automatically.

You can think of New Year's Eve as the "subject" in this analogy, and all of the people celebrating the new year as the "observers". When the clock strikes midnight and the new year begins, the subject (New Year's Eve) changes state, and all of the observers (people celebrating the new year) are notified and updated automatically.

Here is an example of the Observer pattern in C#:

```csharp
public interface ISubject
{
    void Attach(IObserver observer);
    void Detach(IObserver observer);
    void Notify();
}

public interface IObserver
{
    void Update();
}

public class NewYearsEve : ISubject
{
    private readonly List<IObserver> observers;

    public NewYearsEve()
    {
        observers = new List<IObserver>();
    }

    public void Attach(IObserver observer)
    {
        observers.Add(observer);
    }

    public void Detach(IObserver observer)
    {
        observers.Remove(observer);
    }

    public void Notify()
    {
        foreach (IObserver observer in observers)
        {
            observer.Update();
        }
    }
}

public class PartyGoer : IObserver
{
    public void Update()
    {
        Console.WriteLine("It's midnight! Happy New Year!");
    }
}
```

In this example, the `NewYearsEve` class is the subject, and the `PartyGoer` class is the observer. The `NewYearsEve` class has methods for attaching and detaching observers, and a method for notifying all of its observers when its state changes. The `PartyGoer` class has an `Update` method that is called when the `NewYearsEve` subject changes state.

Here is an example of how you could use the Observer design pattern in a New Year's Eve scenario:

```csharp
NewYearsEve newYearsEve = new NewYearsEve();

PartyGoer partyGoer1 = new PartyGoer();
PartyGoer partyGoer2 = new PartyGoer();
PartyGoer partyGoer3 = new PartyGoer();

newYearsEve.Attach(partyGoer1);
newYearsEve.Attach(partyGoer2);
newYearsEve.Attach(partyGoer3);

newYearsEve.Notify();
```

Example Output at Midnight:

```html
It's midnight! Happy New Year!
It's midnight! Happy New Year!
It's midnight! Happy New Year!
```


I hope this example gives you some ideas for how you can relate the Observer design pattern to New Year's Eve! Let me know if you have any questions or need further clarification.
