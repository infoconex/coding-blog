---
title: "Open/Closed Principle (OCP) – Building for Extension, Not Modification"
date: "2025-06-28"
description: "The second principle in the SOLID family is the Open/Closed Principle (OCP) . It’s a simple but powerful idea:"
tags: ["c#", "solid principles", "open closed principle"]
slug: "open-closed-principle-ocp-building-for-extension-not-modification"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2025/06/28/open-closed-principle-ocp-building-for-extension-not-modification"
permalink: "/post/2025/06/28/open-closed-principle-ocp-building-for-extension-not-modification"
legacyPaths: ["/post/2025/06/28/open-closed-principle-ocp-building-for-extension-not-modification"]
---
The second principle in the **SOLID** family is the **Open/Closed Principle (OCP)**. It’s a simple but powerful idea:

> **“Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification.”**
>  — Bertrand Meyer

This principle was first introduced in 1988 by **Bertrand Meyer**, who emphasized using inheritance to extend software behavior without changing existing code. Later, **Robert C. Martin (Uncle Bob)** adopted and expanded the principle as part of the SOLID design principles, promoting the use of interfaces, abstractions, and composition to make it more practical in modern object-oriented design. Uncle Bob summarized it as:

> **“You should be able to extend a software module’s behavior without modifying its source code.”**
>  — Robert C. Martin

The core idea remains the same: build systems that are **easy to extend** without risking the stability of what's already working.

---

### Common Signs You May Be Violating OCP

- Large **switch** or **if-else** chains based on types or enum values.
- Classes that require frequent modifications to add new behavior.
- Classes handling multiple responsibilities (which often indicates an **SRP** violation, increasing OCP risk).
- Hard-coded dependencies rather than abstractions.
- Duplicated logic spread across multiple places instead of centralized extension points.

---

### The Problem: Violating the Open/Closed Principle

Suppose you’re building a reporting system that generates different types of reports:

This implementation works, but every time you need to add a new report type, you must modify the `GenerateReport` method. That violates the **Open/Closed Principle**.

```csharp
public class ReportGenerator
{
    public string GenerateReport(string reportType)
    {
        if (reportType == "PDF")
            return "Generating PDF report...";

        if (reportType == "Excel")
            return "Generating Excel report...";

        if (reportType == "Html")
            return "Generating HTML report...";

        return "Unknown report type.";
    }
}
```

 This implementation works, but every time you need to add a new report type, you must modify the `GenerateReport` method. That violates the **Open/Closed Principle**.

### The Solution: Apply the Open/Closed Principle

Let’s refactor the design to allow new behavior without modifying existing logic.

**Example usage:**

```csharp
var generator = new ReportGenerator();

Console.WriteLine(generator.GenerateReport(new PdfReport()));
Console.WriteLine(generator.GenerateReport(new HtmlReport()));
```

**Step 1: Define an abstract base class**

```csharp
public abstract class Report
{
    public abstract string Generate();
}
```

**Step 2: Implement each report format as a separate class**

```csharp
public class PdfReport : Report
{
    public override string Generate() => "Generating PDF report...";
}

public class ExcelReport : Report
{
    public override string Generate() => "Generating Excel report...";
}

public class HtmlReport : Report
{
    public override string Generate() => "Generating HTML report...";
}
```

**Step 3: Use the base class in the generator**

```csharp
public class ReportGenerator
{
    public string GenerateReport(Report report)
    {
        if (report == null) return "No report provided.";
        return report.Generate();
    }
}
```

Now if you want to add a new report format—say **WordReport**—you just create a new class without touching any existing code.

### Summary

| Without OCP | With OCP |
| --- | --- |
| Uses **switch** or **if** logic | Uses polymorphism |
| Must change logic to add behavior | Extend by adding new classes |
| High chance of breaking existing code | Existing code stays untouched |

---

### When to Apply the Open/Closed Principle

- When new behavior is expected to be added in the future
- When you notice repeated modification of the same class
- When changes in one place frequently cause bugs elsewhere

Avoid overengineering. If there’s only one type of behavior and no likelihood of change, a simple implementation might be more appropriate. The goal is to prepare for change when change is likely.

---

### Final Thoughts

The **Open/Closed Principle** helps you build code that is easier to maintain, extend, and test. You reduce risk by protecting existing code from frequent edits while still making room for growth.

This is the second article in the **SOLID** series. Up next, we’ll explore the **Liskov Substitution Principle**, which teaches us when and how subclassing can go wrong.

Want to read the full series? Browse all SOLID principle articles: [Create better software by applying SOLID principles](/post/2025/06/13/creat-better-software-by-applying-solid-principles)
