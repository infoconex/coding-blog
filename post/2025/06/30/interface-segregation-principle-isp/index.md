---
title: "Interface Segregation Principle (ISP) – Keep Interfaces Focused"
date: "2025-06-30"
description: "The Interface Segregation Principle keeps abstractions focused so clients depend only on the behavior they actually need."
tags: ["c#", "solid principles", "interface segregation principle"]
slug: "interface-segregation-principle-isp"
author: "Jim Scott"
permalink: "/post/2025/06/30/interface-segregation-principle-isp"
series: "SOLID Principles"
seriesOrder: 5
published: false
---
The fourth principle in the **SOLID** family is the **Interface Segregation Principle (ISP)**.

The usual definition is:

> **Clients should not be forced to depend on methods they do not use.**

That sounds simple, but it addresses a problem that appears constantly in long-lived systems: an abstraction starts small, more responsibilities are added over time, and eventually every implementation is forced to support behavior that only some clients actually need.

The result is usually one of three things:

- implementations with empty methods,
- implementations that throw `NotSupportedException`, or
- callers that depend on large interfaces even though they use only a small part of them.

ISP asks us to design abstractions around **cohesive capabilities** instead of accumulating unrelated behavior into one convenient contract.

## Large interfaces create accidental coupling

Imagine an application has this service interface:

```csharp
public interface ICustomerService
{
    Customer Get(int id);
    void Save(Customer customer);
    void Delete(int id);
    void SendWelcomeEmail(int id);
    byte[] ExportCsv();
    void RebuildSearchIndex();
}
```

At first, this may seem convenient. There is one service for everything related to customers.

But consider a controller that only needs to read a customer:

```csharp
public class CustomerController
{
    private readonly ICustomerService _service;

    public CustomerController(ICustomerService service)
    {
        _service = service;
    }

    public Customer Get(int id)
    {
        return _service.Get(id);
    }
}
```

The controller technically depends on all six operations even though it needs only one.

That matters because the dependency communicates more than what the code actually requires. It also makes testing and substitution harder because every fake or mock must satisfy a contract much larger than the client's real needs.

## The problem becomes obvious in implementations

Suppose we create a read-only customer provider:

```csharp
public class ReportingCustomerService : ICustomerService
{
    public Customer Get(int id)
    {
        // Read from reporting database
        return new Customer();
    }

    public void Save(Customer customer)
    {
        throw new NotSupportedException();
    }

    public void Delete(int id)
    {
        throw new NotSupportedException();
    }

    public void SendWelcomeEmail(int id)
    {
        throw new NotSupportedException();
    }

    public byte[] ExportCsv()
    {
        return Array.Empty<byte>();
    }

    public void RebuildSearchIndex()
    {
        throw new NotSupportedException();
    }
}
```

The class compiles, but the abstraction is telling a lie.

`ReportingCustomerService` is being forced to claim capabilities it does not have.

That is exactly the kind of design ISP is intended to prevent.

## Split interfaces by responsibility

A better design is to model the capabilities separately:

```csharp
public interface ICustomerReader
{
    Customer Get(int id);
}

public interface ICustomerWriter
{
    void Save(Customer customer);
    void Delete(int id);
}

public interface ICustomerNotificationService
{
    void SendWelcomeEmail(int id);
}

public interface ICustomerExporter
{
    byte[] ExportCsv();
}

public interface ISearchIndexRebuilder
{
    void RebuildSearchIndex();
}
```

Now the controller can state exactly what it needs:

```csharp
public class CustomerController
{
    private readonly ICustomerReader _customers;

    public CustomerController(ICustomerReader customers)
    {
        _customers = customers;
    }

    public Customer Get(int id)
    {
        return _customers.Get(id);
    }
}
```

And the reporting implementation only implements the behavior it supports:

```csharp
public class ReportingCustomerReader : ICustomerReader
{
    public Customer Get(int id)
    {
        // Read from reporting database
        return new Customer();
    }
}
```

There are no fake capabilities and no unsupported operations.

The abstraction is smaller, but more importantly, it is more accurate.

## Interface segregation is about clients

One subtle point is that ISP is not simply "make every interface tiny."

The principle is about the needs of **clients**.

If a group of operations is consistently used together by the same callers and represents one cohesive capability, keeping them together may be perfectly reasonable.

For example:

```csharp
public interface IFileStore
{
    Stream OpenRead(string path);
    Stream OpenWrite(string path);
    bool Exists(string path);
    void Delete(string path);
}
```

That interface may be cohesive for the clients that use it.

Splitting every method into its own interface would add ceremony without improving the design.

The question is not "How small can this interface become?"

The better question is:

**Are clients being forced to depend on behavior they do not need?**

## Role-based interfaces are often clearer

One useful way to think about ISP is to model roles instead of objects.

Suppose we have this interface:

```csharp
public interface IEmployee
{
    void Work();
    void ApproveExpense(decimal amount);
    void Hire(Employee employee);
}
```

Not every employee approves expenses or hires people.

Instead, model the roles explicitly:

```csharp
public interface IWorker
{
    void Work();
}

public interface IExpenseApprover
{
    void ApproveExpense(decimal amount);
}

public interface IHiringManager
{
    void Hire(Employee employee);
}
```

A manager can implement all three:

```csharp
public class EngineeringManager :
    IWorker,
    IExpenseApprover,
    IHiringManager
{
    public void Work()
    {
        Console.WriteLine("Planning and reviewing work.");
    }

    public void ApproveExpense(decimal amount)
    {
        Console.WriteLine($"Approved {amount:C}.");
    }

    public void Hire(Employee employee)
    {
        Console.WriteLine($"Hiring {employee.Name}.");
    }
}
```

An individual contributor only implements the role that applies:

```csharp
public class SoftwareEngineer : IWorker
{
    public void Work()
    {
        Console.WriteLine("Building software.");
    }
}
```

This is a more faithful representation of the system.

## Fat interfaces spread change farther than necessary

Large interfaces also increase the cost of change.

If we add a method to a broad interface:

```csharp
public interface IOrderService
{
    Order Get(int id);
    void Save(Order order);
    void Cancel(int id);
    void Export();
    void Archive();
    void RecalculateTax();
}
```

then every implementation must change, even if only one implementation actually needs the new behavior.

That is unnecessary coupling.

A focused interface limits the blast radius of changes because fewer consumers and implementations depend on it.

This is one of the practical reasons ISP matters in production systems. Smaller dependency surfaces make systems easier to evolve.

## ISP and the Single Responsibility Principle

ISP and the **Single Responsibility Principle** are closely related.

SRP asks whether a module has too many reasons to change.

ISP asks whether clients are being forced to depend on too many responsibilities.

A large interface often reveals that multiple responsibilities have been grouped together simply because they operate on the same domain object.

For example, reading customers, sending email, exporting reports, and rebuilding indexes may all involve customer data, but they do not necessarily represent the same responsibility.

Separating those concerns makes both the implementation and its contracts clearer.

## ISP and Liskov Substitution

ISP also helps support the **Liskov Substitution Principle**.

When an interface contains operations that do not apply to every implementation, developers often respond by throwing exceptions:

```csharp
public void Delete(int id)
{
    throw new NotSupportedException();
}
```

Now callers cannot safely substitute one implementation for another.

The ISP violation creates an LSP violation.

By splitting the interface into capabilities, every implementation can honestly support the contract it implements.

## Watch for capability checks

Another sign that an interface may be too broad is code like this:

```csharp
if (service.CanExport)
{
    service.Export();
}
```

Capability checks are not always wrong, but they can indicate that the abstraction contains optional behavior that might be better represented by a separate interface.

Instead, a caller that needs exporting can depend directly on:

```csharp
public interface IExporter
{
    void Export();
}
```

Then the type system expresses the requirement instead of runtime conditionals.

## Avoid interface explosion

There is a bad version of interface segregation too.

A codebase can become cluttered with interfaces such as:

```csharp
IOrderGetter
IOrderSaver
IOrderDeleter
IOrderUpdater
IOrderValidator
```

when the operations are naturally cohesive and always used together.

That does not make the design automatically better.

Every abstraction has a cost: another name to understand, another dependency to wire, another place to navigate, and another contract to maintain.

The goal is not maximum fragmentation.

The goal is **cohesion**.

A good interface represents a meaningful capability that its clients actually need.

## A practical test for ISP

When reviewing an interface, ask:

- Do most clients use most of these methods?
- Are implementations throwing `NotSupportedException` for parts of the contract?
- Are empty methods being added just to satisfy the interface?
- Are unrelated responsibilities grouped together because they concern the same entity?
- Does changing one capability force unrelated implementations to change?
- Would a client be clearer if it depended on a smaller role-based abstraction?

If several answers point in the same direction, the interface is probably doing too much.

## The principle in practice

The Interface Segregation Principle is about keeping dependencies honest.

Clients should depend on the behavior they actually require, and implementations should only promise behavior they can actually provide.

Good interfaces make responsibilities visible.

Bad interfaces hide unrelated capabilities behind one convenient name and push the complexity into implementations and callers.

When an interface becomes difficult to implement without exceptions, optional behavior, or empty methods, the answer is usually not another workaround.

It is often a better boundary.
