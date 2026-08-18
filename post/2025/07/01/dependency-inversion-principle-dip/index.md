---
title: "Dependency Inversion Principle (DIP) – Depend on Abstractions, Not Details"
date: "2025-07-01"
description: "The Dependency Inversion Principle keeps high-level policy from being tightly coupled to low-level implementation details."
tags: ["C#", "SOLID Principles", "Dependency Inversion Principle"]
slug: "dependency-inversion-principle-dip"
author: "Jim Scott"
permalink: "/post/2025/07/01/dependency-inversion-principle-dip"
series: "SOLID Principles"
seriesOrder: 6
published: true
---
The fifth and final principle in the **SOLID** family is the **Dependency Inversion Principle (DIP)**.

The usual definition is:

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**
>
> **Abstractions should not depend on details. Details should depend on abstractions.**

At first, this can sound like another way of saying "use interfaces."

It is more important than that.

DIP is about deciding **which direction dependencies should point**.

High-level business rules should not be forced to know the details of databases, email providers, file systems, HTTP clients, message brokers, or other infrastructure concerns.

Those details should be replaceable without rewriting the policy that uses them.

## The problem with depending directly on details

Consider an order service that sends a confirmation email after an order is placed:

```csharp
public class OrderService
{
    public void PlaceOrder(Order order)
    {
        SaveOrder(order);

        var smtp = new SmtpClient("smtp.example.com");
        smtp.Send(
            "orders@example.com",
            order.CustomerEmail,
            "Order received",
            "Thanks for your order.");
    }

    private void SaveOrder(Order order)
    {
        using var connection = new SqlConnection(
            "Server=.;Database=Orders;Trusted_Connection=True;");

        connection.Open();

        // Save order
    }
}
```

This class contains both high-level policy and low-level infrastructure details.

The policy is simple:

1. save the order,
2. send a confirmation.

But that policy is now directly coupled to SQL Server and SMTP.

Testing the class becomes harder. Changing the database becomes harder. Changing email providers becomes harder. Running the logic without infrastructure becomes harder.

The business rule has become dependent on implementation details.

## Introduce abstractions around the behavior the policy needs

A better design starts by identifying what the high-level code actually needs.

It needs somewhere to persist an order:

```csharp
public interface IOrderRepository
{
    void Save(Order order);
}
```

And it needs a way to send a confirmation:

```csharp
public interface IOrderNotifier
{
    void SendConfirmation(Order order);
}
```

Now the high-level service can depend on those abstractions:

```csharp
public class OrderService
{
    private readonly IOrderRepository _orders;
    private readonly IOrderNotifier _notifier;

    public OrderService(
        IOrderRepository orders,
        IOrderNotifier notifier)
    {
        _orders = orders;
        _notifier = notifier;
    }

    public void PlaceOrder(Order order)
    {
        _orders.Save(order);
        _notifier.SendConfirmation(order);
    }
}
```

The policy is now easy to understand.

It also no longer knows whether orders are stored in SQL Server, PostgreSQL, a document database, or memory.

It does not know whether notifications are sent through SMTP, an API, a queue, or not at all during a test.

Those are details.

## The details depend on the abstraction

A SQL implementation can provide the repository:

```csharp
public class SqlOrderRepository : IOrderRepository
{
    private readonly string _connectionString;

    public SqlOrderRepository(string connectionString)
    {
        _connectionString = connectionString;
    }

    public void Save(Order order)
    {
        using var connection = new SqlConnection(_connectionString);
        connection.Open();

        // Save order
    }
}
```

An SMTP implementation can provide the notifier:

```csharp
public class SmtpOrderNotifier : IOrderNotifier
{
    private readonly SmtpClient _client;

    public SmtpOrderNotifier(SmtpClient client)
    {
        _client = client;
    }

    public void SendConfirmation(Order order)
    {
        _client.Send(
            "orders@example.com",
            order.CustomerEmail,
            "Order received",
            "Thanks for your order.");
    }
}
```

Notice the dependency direction.

`OrderService` does not depend on `SqlOrderRepository` or `SmtpOrderNotifier`.

Those infrastructure classes depend on contracts that describe what the application needs.

That is the inversion.

## Dependency inversion is not dependency injection

DIP and **dependency injection** are related, but they are not the same thing.

Dependency inversion is a **design principle**.

Dependency injection is one technique for supplying dependencies to an object.

This constructor uses dependency injection:

```csharp
public OrderService(
    IOrderRepository orders,
    IOrderNotifier notifier)
{
    _orders = orders;
    _notifier = notifier;
}
```

But simply injecting something does not mean the design follows DIP.

For example:

```csharp
public class OrderService
{
    private readonly SqlOrderRepository _repository;

    public OrderService(SqlOrderRepository repository)
    {
        _repository = repository;
    }
}
```

The dependency is injected, but the high-level class still depends directly on a low-level implementation detail.

Dependency injection can help implement DIP, but it is not a substitute for thinking about dependency direction.

## The abstraction should belong to the policy

A useful question is: **Who should define the interface?**

It is tempting to put an interface next to every infrastructure class:

```text
SqlOrderRepository
ISqlOrderRepository
```

But the important contract is not "what SQL can do."

The important contract is "what the application needs from order persistence."

That distinction changes how we design the interface.

This is better:

```csharp
public interface IOrderRepository
{
    void Save(Order order);
    Order? GetById(int id);
}
```

than exposing database-specific details such as:

```csharp
public interface ISqlOrderRepository
{
    DataTable ExecuteStoredProcedure(string name);
    SqlConnection OpenConnection();
}
```

The second abstraction still leaks the low-level technology into the high-level code.

An interface alone does not create inversion if the interface itself is shaped around the detail.

## DIP protects business rules from infrastructure churn

Infrastructure changes more often than many business rules.

Databases are replaced.

Email vendors change.

APIs are versioned.

Queues move.

Storage systems change.

Cloud services are introduced or removed.

If business logic directly depends on those details, infrastructure changes spread through the application.

A good abstraction creates a boundary around that volatility.

For example:

```csharp
public interface IPaymentGateway
{
    PaymentResult Charge(
        decimal amount,
        PaymentMethod paymentMethod);
}
```

The checkout workflow can depend on `IPaymentGateway` without caring which vendor implements it.

```csharp
public class CheckoutService
{
    private readonly IPaymentGateway _payments;

    public CheckoutService(IPaymentGateway payments)
    {
        _payments = payments;
    }

    public PaymentResult Checkout(Order order)
    {
        return _payments.Charge(
            order.Total,
            order.PaymentMethod);
    }
}
```

A Stripe adapter, legacy gateway, sandbox implementation, or fake test gateway can all satisfy that contract.

The core workflow remains stable.

## DIP improves testing, but testing is not the main goal

One obvious benefit of abstractions is easier testing.

A test implementation can be simple:

```csharp
public class FakeOrderRepository : IOrderRepository
{
    public List<Order> SavedOrders { get; } = new();

    public void Save(Order order)
    {
        SavedOrders.Add(order);
    }
}
```

That is useful, but testability is not the deepest reason to apply DIP.

The bigger benefit is architectural.

The high-level policy becomes independent of volatile details.

Good testability is often evidence that the dependency boundary is in the right place.

## Do not create interfaces for every class

DIP does not mean every concrete class needs an interface.

This is a common overcorrection:

```text
CustomerService
ICustomerService
CustomerMapper
ICustomerMapper
DateFormatter
IDateFormatter
StringHelper
IStringHelper
```

An abstraction has value when it creates a meaningful boundary.

It may protect high-level policy from infrastructure, isolate volatility, support genuinely different implementations, or make ownership clearer.

An interface that merely mirrors one concrete class without serving any architectural purpose adds ceremony rather than flexibility.

The question should be:

**What dependency do we need to protect ourselves from?**

Not:

**How many interfaces can we create?**

## Stable dependencies do not always need inversion

Suppose a class uses a simple immutable value object:

```csharp
public record Money(decimal Amount, string Currency);
```

There is little reason to hide that behind `IMoney`.

Likewise, depending on a stable part of the language or framework does not automatically violate DIP.

The principle matters most at architectural boundaries where high-level behavior would otherwise become coupled to lower-level implementation choices.

Use the principle where dependency direction affects changeability.

## DIP and the Open/Closed Principle

DIP helps make the **Open/Closed Principle** practical.

If a service depends on an abstraction:

```csharp
public class ReportService
{
    private readonly IReportStore _store;

    public ReportService(IReportStore store)
    {
        _store = store;
    }
}
```

we can introduce a new storage implementation without modifying the service.

That is extension without modification.

If the service directly constructs a particular storage provider, adding a new implementation usually requires changing the service itself.

The dependency structure determines whether extension remains local or spreads through the system.

## DIP and Liskov Substitution

DIP also relies on the **Liskov Substitution Principle**.

Depending on an abstraction only helps when its implementations are actually substitutable.

If one `IReportStore` works normally while another throws `NotSupportedException` for ordinary operations, callers still need implementation-specific knowledge.

So DIP gives us the boundary, while LSP helps ensure the implementations can safely live behind it.

## DIP and Interface Segregation

The **Interface Segregation Principle** helps keep DIP abstractions focused.

A high-level service should depend on the smallest cohesive capability it needs.

Instead of:

```csharp
public interface IInfrastructureServices
{
    void SendEmail();
    void SaveFile();
    void WriteAuditLog();
    void PublishMessage();
    void ExecuteSql();
}
```

prefer meaningful contracts:

```csharp
public interface IEmailSender
{
    void Send(EmailMessage message);
}

public interface IAuditLog
{
    void Write(AuditEntry entry);
}

public interface IMessagePublisher
{
    void Publish<T>(T message);
}
```

The high-level module can then depend only on what it actually needs.

## Composition belongs near the edge

At some point, concrete implementations must be selected.

An application has to decide that `IOrderRepository` is implemented by `SqlOrderRepository` and that `IOrderNotifier` is implemented by `SmtpOrderNotifier`.

That wiring belongs near the application's composition root:

```csharp
services.AddScoped<IOrderRepository, SqlOrderRepository>();
services.AddScoped<IOrderNotifier, SmtpOrderNotifier>();
services.AddScoped<OrderService>();
```

The application startup code knows the details.

The business logic does not.

That is a healthy dependency structure: details are assembled at the edge and passed inward through abstractions.

## A practical test for DIP

When reviewing a design, ask:

- Does business logic directly create database, HTTP, email, file-system, or messaging clients?
- Would changing an infrastructure provider require modifying core business rules?
- Are high-level modules importing low-level implementation types?
- Are interfaces shaped around what the application needs, or around what a vendor technology exposes?
- Are abstractions creating useful boundaries, or merely duplicating concrete class names?
- Can infrastructure implementations change without forcing changes in the policy that uses them?

Those questions usually reveal whether dependency direction is helping or hurting the design.

## SOLID works as a system

DIP is the final letter in SOLID, but the principles reinforce one another.

**Single Responsibility Principle** keeps modules focused on one reason to change.

**Open/Closed Principle** encourages extension without repeatedly modifying stable code.

**Liskov Substitution Principle** makes sure implementations can safely stand behind abstractions.

**Interface Segregation Principle** keeps those abstractions focused on what clients actually need.

**Dependency Inversion Principle** points dependencies toward those abstractions instead of toward volatile details.

None of the principles is a rule that should be applied mechanically.

They are tools for identifying designs that become expensive to change.

## The principle in practice

The Dependency Inversion Principle is about protecting important policy from implementation detail.

High-level code should describe **what the system needs to accomplish**.

Low-level code should describe **how a particular technology accomplishes it**.

When those two concerns are tightly coupled, infrastructure decisions spread into business logic and every change becomes larger than it should be.

A good abstraction reverses that relationship.

The details become replaceable.

The policy remains stable.

That is the real value of dependency inversion—and a fitting conclusion to SOLID as a whole.
