---
title: "Single Responsibility Principle (SRP) - Only one reason to change"
date: "2025-06-28"
description: "The Single Responsibility Principle is the first of the five SOLID principles of object-oriented design, introduced by Robert C. Martin (Uncle Bob). It helps make software easier to understand, maintain, and extend."
tags: ["c#", "solid principles", "single responsibility principle"]
slug: "single-responsibility-principle-srp-only-one-reason-to-change"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2025/06/28/single-responsibility-principle-srp"
permalink: "/post/2025/06/28/single-responsibility-principle-srp"
legacyPaths: ["/post/2025/06/28/single-responsibility-principle-srp"]
---
The **Single Responsibility Principle** is the first of the five SOLID principles of object-oriented design, introduced by Robert C. Martin (Uncle Bob). It helps make software easier to understand, maintain, and extend.

> **Definition:** A class should have only one reason to change.

This means a class should encapsulate only one responsibility or role. When a class has multiple responsibilities, those become tightly coupled, making changes risky and costly.

---

## What Uncle Bob Says About SRP Smells

Robert C. Martin (Uncle Bob) describes several code smells that help identify when the Single Responsibility Principle may be violated. These smells fall into two groups:

---

### Direct Indicators of SRP Violations

- Divergent Change
   A class changes for multiple unrelated reasons (e.g., business logic, logging, persistence). This tightly couples different concerns and clearly violates SRP.
- Vague Class Names
   Names like `Manager`, `Processor`, or `Service` often signal that a class handles multiple responsibilities.
- Chunky Methods
   Large methods containing multiple unrelated operations indicate the class may be doing too much.

---

### Related Design Smells Often Associated with SRP Violations

- Shotgun Surgery (Inverse)
   Responsibilities scattered across many classes require multiple changes spread out for a single change. This reflects poor responsibility distribution in the system.
- Feature Envy
   A class frequently accesses data or methods of another class, indicating misplaced behavior but not necessarily multiple responsibilities.
- Inappropriate Intimacy
   Excessive coupling through access to internal details of other classes; often correlates with SRP issues but can appear independently.
- Data Clumps
   Groups of related variables passed together instead of encapsulated. This points to missing abstractions and can contribute to SRP violations.
- Multiple Stakeholders Affected
   When different teams or roles must change the same class for different reasons; a design smell important at an organizational level.

---

## Bad Example: A Class Doing Too Much (Smells Annotated)

```csharp
using System;
using System.IO;
using System.Runtime.Caching;
using log4net;

public class ReportManager
{
    // Smell: Divergent change - Logging responsibility mixed in using a 3rd party library
    // Violation: Tight coupling to log4net means if we want to change logging
    // frameworks, we must modify this class and others using log4net directly.
    private static readonly ILog _logger = LogManager.GetLogger(typeof(ReportManager));

    // Smell: Divergent change - Caching responsibility mixed in
    // Violation: Direct dependency on MemoryCache couples business logic
    // to caching implementation; changing caching tech requires class modification.
    private readonly MemoryCache _cache = MemoryCache.Default;

    public string CreateReport(string reportId)
    {
        if (_cache.Contains(reportId))
        {
            _logger.Info($"Report {reportId} retrieved from cache.");
            return _cache.Get(reportId) as string;
        }

        // Core business logic — report data generation
        var reportData = new
        {
            ReportId = reportId,
            GeneratedAt = DateTime.Now,
            Content = $"This is the content of report {reportId}."
        };

        // Smell: Divergent change - Serialization logic mixed with business logic
        // Violation: Tight coupling to System.Text.Json means changes to format or serializer
        // affect this class, violating SRP.
        string reportJson = System.Text.Json.JsonSerializer.Serialize(reportData, new System.Text.Json.JsonSerializerOptions { WriteIndented = true });

        // Smell: Divergent change - File persistence mixed in
        // Violation: Using File.WriteAllText directly couples file I/O to business logic;
        // changing persistence strategy requires editing this method.
        string filePath = $"report_{reportId}.json";
        File.WriteAllText(filePath, reportJson);

        _logger.Info($"Report {reportId} saved to {filePath}");

        _cache.Set(reportId, reportJson, DateTimeOffset.Now.AddMinutes(10));

        return reportJson;
    }
}
```

### Summary: Why the example Violates SRP

The `ReportManager` class in the example violates the Single Responsibility Principle by taking on **multiple distinct responsibilities**, each of which could change for a different reason:

- **Business Logic** – Generating the contents of the report.
- **Logging** – Logging using a specific framework (`log4net`), tightly coupling the class to a particular logging mechanism.
- **Caching** – Storing and retrieving data using `MemoryCache`, which could change independently from business logic.
- **Serialization** – Converting the report to JSON using `System.Text.Json`, which may need to be swapped or modified in isolation.
- **Persistence** – Writing the report to disk with `File.WriteAllText`, introducing concerns related to file systems, security, or output formats.

Any change in **any one** of these areas — e.g., switching logging libraries, changing report format, updating caching rules — would require modifying this class, increasing the chance of bugs and creating ripple effects.

This coupling of responsibilities creates **fragile code** that is harder to test, extend, and maintain.

Refactoring by **separating each responsibility into its own class** restores SRP and makes each concern independently testable and changeable.

## Refactored Example: Applying SRP by Separating Responsibilities

---

### ReportService

**Purpose:**
 Coordinates the report creation workflow by delegating to specialized classes.

**How it helps SRP:**
 Acts as an orchestrator without taking on multiple responsibilities, preventing coupling and divergent change.

```csharp
public class ReportService
{
    private readonly ReportGenerator _generator = new();
    private readonly JsonSerializer _serializer = new();
    private readonly FileSaver _saver = new();
    private readonly Logger _logger = new();
    private readonly Cache _cache = new();

    public string GetReport(string reportId)
    {
        if (_cache.TryGet(reportId, out var cached))
        {
            _logger.Info($"Report {reportId} retrieved from cache.");
            return cached;
        }

        var reportData = _generator.Generate(reportId);
        var reportJson = _serializer.Serialize(reportData);

        string path = $"report_{reportId}.json";
        _saver.Save(reportJson, path);
        _logger.Info($"Report {reportId} saved to {path}");

        _cache.Set(reportId, reportJson, TimeSpan.FromMinutes(10));
        return reportJson;
    }
}
```

### Summary: How `ReportService` Fixes the SRP Violation

The `ReportService` class acts as an **orchestrator**, coordinating multiple well-defined components that each have a **single responsibility**:

- **`ReportGenerator`** handles the creation of report content (business logic).
- **`JsonSerializer`** takes care of converting data to JSON (serialization).
- **`FileSaver`** encapsulates writing to disk (persistence).
- **`Logger`** abstracts away logging logic and dependency on a specific framework.
- **`Cache`** manages temporary storage and retrieval of report data (caching).

By delegating each responsibility to a specialized class, `ReportService` eliminates the **divergent change smell** found in the original `ReportManager`. Each class can now be modified or tested independently — for example:

- Swapping out the caching mechanism won't affect how the report is serialized.
- Updating the report structure won't impact file writing logic.
- Changing the logging library affects only the `Logger` class.

This design keeps the **business workflow centralized** while preserving the **single responsibility** of each collaborator, making the system easier to **extend, test, and maintain**.

### ReportGenerator

**Purpose:**
 This class focuses solely on generating the core report data.

**How it helps SRP:**
 Changes related to report creation logic will affect only this class, preventing unrelated reasons for modification.

```csharp
using System;

public class ReportGenerator
{
    public ReportData Generate(string reportId)
    {
        return new ReportData
        {
            ReportId = reportId,
            GeneratedAt = DateTime.Now,
            Content = $"This is the content of report {reportId}."
        };
    }
}

public class ReportData
{
    public string ReportId { get; set; } = string.Empty;
    public DateTime GeneratedAt { get; set; }
    public string Content { get; set; } = string.Empty;
}
```

### JsonSerializer

**Purpose:**
 Handles serialization of objects into JSON format.

**How it helps SRP:**
 Isolates serialization so that changes to serialization logic affect only this class.

```csharp
using System.Text.Json;

public class JsonSerializer
{
    public string Serialize<T>(T data)
    {
        return JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true });
    }
}
```

### FileSaver

**Purpose:**
 Manages saving content to the file system.

**How it helps SRP:**
 Encapsulates file persistence, so changes to storage affect only this class.

```csharp
using System.IO;

public class FileSaver
{
    public void Save(string content, string filePath)
    {
        File.WriteAllText(filePath, content);
    }
}
```

### Logger

**Purpose:**
 Encapsulates logging behavior using log4net.

**How it helps SRP:**
 Abstracts logging implementation to isolate logging-related changes.

```csharp
using log4net;

public class Logger
{
    private static readonly ILog _log = LogManager.GetLogger(typeof(Logger));

    public void Info(string message)
    {
        _log.Info(message);
    }
}
```

### Cache

**Purpose:**
 Manages caching of data using MemoryCache.

**How it helps SRP:**
 Separates caching concerns to localize cache-related changes.

```csharp
using System;
using System.Runtime.Caching;

public class Cache
{
    private readonly MemoryCache _cache = MemoryCache.Default;

    public bool TryGet(string key, out string value)
    {
        value = _cache.Get(key) as string;
        return value != null;
    }

    public void Set(string key, string value, TimeSpan duration)
    {
        _cache.Set(key, value, DateTimeOffset.Now.Add(duration));
    }
}
```

###
