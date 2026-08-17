---
title: "Liskov Substitution Principle (LSP) – Subtypes Should Keep Their Promises"
date: "2025-06-29"
description: "The Liskov Substitution Principle is about making abstractions trustworthy: subtypes should preserve the behavioral expectations of their base types."
tags: ["c#", "solid principles", "liskov substitution principle"]
slug: "liskov-substitution-principle-lsp"
author: "Jim Scott"
permalink: "/post/2025/06/29/liskov-substitution-principle-lsp"
published: false
series: "SOLID Principles"
seriesOrder: 4
---
The third principle in the **SOLID** family is the **Liskov Substitution Principle (LSP)**.

At first glance, LSP can sound more academic than the other SOLID principles. The usual definition is:

> **Objects of a subtype should be replaceable with objects of their base type without changing the correctness of the program.**

The principle comes from Barbara Liskov’s work on behavioral subtyping, and the important word is **behavioral**.

Inheritance is not just about sharing methods and properties. A derived type also inherits the expectations that callers have about the base type.

If a subtype technically satisfies the compiler but violates those expectations at runtime, the inheritance relationship is probably wrong.

## Inheritance creates a contract

Consider a simple payment processor:

```csharp
public abstract class PaymentProcessor
{
    public abstract void Process(decimal amount);
}
```

A caller using this abstraction has a reasonable expectation:

```csharp
public void ChargeCustomer(
    PaymentProcessor processor,
    decimal amount)
{
    processor.Process(amount);
}
```

Any `PaymentProcessor` should be usable here.

A credit-card implementation fits that expectation:

```csharp
public class CreditCardProcessor : PaymentProcessor
{
    public override void Process(decimal amount)
    {
        Console.WriteLine(
            $"Charging credit card: {amount:C}");
    }
}
```

So does a bank-transfer implementation:

```csharp
public class BankTransferProcessor : PaymentProcessor
{
    public override void Process(decimal amount)
    {
        Console.WriteLine(
            $"Initiating bank transfer: {amount:C}");
    }
}
```

Both implementations honor the behavior promised by `PaymentProcessor`.

Now imagine we add another subtype:

```csharp
public class ManualInvoiceProcessor : PaymentProcessor
{
    public override void Process(decimal amount)
    {
        throw new NotSupportedException(
            "Manual invoices cannot be processed automatically.");
    }
}
```

The compiler is perfectly happy.

The design should make us uncomfortable.

`ManualInvoiceProcessor` is claiming to be a `PaymentProcessor`, but callers cannot safely use it wherever a `PaymentProcessor` is expected.

The subtype has broken the contract.

## `NotSupportedException` is often a warning sign

There are legitimate uses for `NotSupportedException`, but seeing it inside an overridden method should make you look closely at the abstraction.

It often means a subtype inherited behavior that does not actually apply to it.

Consider this example:

```csharp
public abstract class Document
{
    public abstract void Save();
    public abstract void Print();
}
```

A regular document supports both:

```csharp
public class Report : Document
{
    public override void Save()
    {
        Console.WriteLine("Saving report.");
    }

    public override void Print()
    {
        Console.WriteLine("Printing report.");
    }
}
```

Then someone adds a read-only document:

```csharp
public class ReadOnlyDocument : Document
{
    public override void Save()
    {
        throw new NotSupportedException();
    }

    public override void Print()
    {
        Console.WriteLine("Printing document.");
    }
}
```

The problem is not really in `ReadOnlyDocument`.

The problem is that the base abstraction says every document can be saved.

That simply is not true.

One solution is to model the capabilities separately:

```csharp
public interface IPrintable
{
    void Print();
}

public interface ISaveable
{
    void Save();
}
```

Now a report can implement both:

```csharp
public class Report : IPrintable, ISaveable
{
    public void Save()
    {
        Console.WriteLine("Saving report.");
    }

    public void Print()
    {
        Console.WriteLine("Printing report.");
    }
}
```

While a read-only document only implements what it actually supports:

```csharp
public class ReadOnlyDocument : IPrintable
{
    public void Print()
    {
        Console.WriteLine("Printing document.");
    }
}
```

The design is more explicit, and callers no longer need to discover unsupported behavior through exceptions.

## A subtype should not strengthen preconditions

Another way to violate LSP is to make a derived type more restrictive than the base type.

Suppose we have:

```csharp
public class MessageSender
{
    public virtual void Send(string message)
    {
        if (string.IsNullOrWhiteSpace(message))
            throw new ArgumentException(
                "Message is required.");

        Console.WriteLine(message);
    }
}
```

Now we create an SMS sender:

```csharp
public class SmsSender : MessageSender
{
    public override void Send(string message)
    {
        if (message.Length > 160)
            throw new ArgumentException(
                "SMS messages cannot exceed 160 characters.");

        base.Send(message);
    }
}
```

This looks reasonable from the SMS implementation’s point of view.

But it changes the behavioral contract.

The base type accepts any non-empty string. The subtype only accepts strings up to 160 characters.

Code written against `MessageSender` can therefore succeed with one implementation and unexpectedly fail with another.

That is an LSP violation.

The underlying problem is that `SmsSender` is not really substitutable for the broader abstraction.

A better design might make the restriction part of the abstraction itself:

```csharp
public interface IMessageSender
{
    SendResult Send(Message message);
}
```

Then each transport can explicitly participate in validation or expose its capabilities rather than pretending every transport behaves identically.

## A subtype should not weaken guarantees

The reverse problem happens when a subtype promises less than the base type.

Imagine a repository:

```csharp
public abstract class UserRepository
{
    public abstract User GetById(int id);
}
```

Callers may reasonably assume that if the method returns, they receive a valid `User`.

Then a derived repository does this:

```csharp
public class CachedUserRepository : UserRepository
{
    public override User GetById(int id)
    {
        return null;
    }
}
```

Technically, that may compile if nullable reference types are disabled.

Behaviorally, the subtype has weakened the guarantee.

If "not found" is legitimate behavior, that should be represented consistently in the abstraction:

```csharp
public interface IUserRepository
{
    User? GetById(int id);
}
```

Or perhaps:

```csharp
public interface IUserRepository
{
    bool TryGetById(
        int id,
        out User? user);
}
```

The important point is that callers should not need subtype-specific knowledge to use the abstraction safely.

## The classic Rectangle and Square problem

One of the best-known LSP examples involves rectangles and squares.

Mathematically, a square is a rectangle.

That does not automatically mean a mutable `Square` should inherit from a mutable `Rectangle`.

Consider:

```csharp
public class Rectangle
{
    public virtual int Width { get; set; }
    public virtual int Height { get; set; }

    public int Area => Width * Height;
}
```

A caller might reasonably write:

```csharp
public static void Resize(Rectangle rectangle)
{
    rectangle.Width = 5;
    rectangle.Height = 10;

    Console.WriteLine(rectangle.Area);
}
```

The expected area is `50`.

Now implement `Square` like this:

```csharp
public class Square : Rectangle
{
    public override int Width
    {
        get => base.Width;
        set
        {
            base.Width = value;
            base.Height = value;
        }
    }

    public override int Height
    {
        get => base.Height;
        set
        {
            base.Width = value;
            base.Height = value;
        }
    }
}
```

Pass a `Square` into `Resize` and the result is no longer what the caller expects.

The inheritance relationship is mathematically correct but behaviorally incorrect.

That is exactly the kind of distinction LSP asks us to notice.

## Prefer abstractions based on behavior, not classification

A common source of LSP problems is inheritance based on statements like:

- a square **is a** rectangle
- an ostrich **is a** bird
- a read-only file **is a** file
- a manual invoice **is a** payment
- an administrator **is a** user

Those statements may be true in ordinary language.

They are not enough to justify inheritance.

The better question is:

**Can the subtype honor every meaningful expectation of the base type?**

If the answer is no, composition or a different abstraction is usually safer.

For example, instead of:

```csharp
public abstract class Bird
{
    public abstract void Fly();
}
```

we can represent capabilities directly:

```csharp
public abstract class Bird
{
    public abstract void Eat();
}

public interface IFlyingBird
{
    void Fly();
}
```

Now an eagle can fly:

```csharp
public class Eagle : Bird, IFlyingBird
{
    public override void Eat()
    {
        Console.WriteLine("Eagle eating.");
    }

    public void Fly()
    {
        Console.WriteLine("Eagle flying.");
    }
}
```

An ostrich does not need to pretend:

```csharp
public class Ostrich : Bird
{
    public override void Eat()
    {
        Console.WriteLine("Ostrich eating.");
    }
}
```

The model says what the objects can actually do.

## LSP is really about trust

When code depends on an abstraction, it is placing trust in that abstraction.

If I accept an `IEnumerable<T>`, I expect I can enumerate it.

If I accept a writable stream, I expect writing to work.

If I accept a repository, I expect its documented result semantics to remain consistent.

If I accept a payment processor, I should not need a growing collection of subtype checks:

```csharp
if (processor is ManualInvoiceProcessor)
{
    // special case
}
else if (processor is LegacyPaymentProcessor)
{
    // different special case
}
else
{
    processor.Process(amount);
}
```

Once callers need to know the concrete subtype to avoid broken behavior, the abstraction has stopped doing its job.

## LSP and the Open/Closed Principle

LSP has a close relationship with the **Open/Closed Principle**.

OCP tells us that we should be able to introduce new behavior through extension rather than repeatedly modifying stable code.

But that only works if new implementations can safely participate in the existing abstraction.

Suppose we have:

```csharp
public void ProcessPayment(
    PaymentProcessor processor,
    decimal amount)
{
    processor.Process(amount);
}
```

If every new processor honors the same behavioral contract, adding a new processor may require no change here.

That is OCP working properly.

But if each subtype has exceptions, special cases, or unsupported operations, this eventually happens:

```csharp
if (processor is ManualInvoiceProcessor)
{
    // ...
}
else if (processor is CryptoProcessor)
{
    // ...
}
else if (processor is LegacyProcessor)
{
    // ...
}
```

Now adding a subtype forces modification of existing logic.

The LSP violation has undermined OCP.

## LSP and the Single Responsibility Principle

There is also a connection to **Single Responsibility**.

Poor inheritance hierarchies often appear because one abstraction is trying to represent too many capabilities at once.

A large base type might assume that everything can:

```csharp
Save();
Print();
Email();
Export();
Archive();
Delete();
```

Then subclasses implement only some of those operations and throw exceptions for the rest.

That is usually a signal that the abstraction itself contains unrelated responsibilities.

Breaking those behaviors into smaller, cohesive contracts improves both SRP and LSP.

## Do not create abstractions just to satisfy SOLID

LSP does not mean every class needs an interface.

It does not mean inheritance is bad.

It does not mean all implementations must behave identically.

Different implementations can have very different internal behavior.

A SQL repository and an in-memory repository do not need to work the same way internally. They do need to honor the same externally visible contract if callers are expected to treat them interchangeably.

The goal is substitutability, not uniformity.

## A practical test for LSP

When reviewing an inheritance hierarchy or interface implementation, ask a few simple questions.

Can callers use the subtype without checking its concrete type?

Does the subtype throw exceptions for operations the abstraction says are supported?

Does the subtype require stricter input than the base type?

Does it return weaker results or violate guarantees made by the abstraction?

Would replacing the base type with this subtype surprise existing callers?

If the answer to any of those questions is yes, the abstraction deserves another look.

## The principle in practice

The Liskov Substitution Principle is ultimately about making abstractions trustworthy.

A subtype should not merely compile as a replacement for its base type.

It should **behave like a valid replacement**.

That means preserving the expectations that callers rely on.

When those expectations cannot be preserved, the answer is usually not another conditional or another `NotSupportedException`.

The answer is often a better abstraction.

Good inheritance makes extension easier.

Bad inheritance creates hidden conditions that spread throughout the system.

LSP helps us tell the difference.
