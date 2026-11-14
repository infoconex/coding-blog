---
layout: post
title: "Learning from Outages: Protecting Services and Customers"
seoTitle: "Service Outage Lessons: Resilience, FMEA, and Recovery Testing"
date: "2026-11-13"
updated: "2026-11-13"
slug: "learning-from-outages-protecting-services-and-customers"
author: "Jim Scott"
published: true
featured: false
permalink: "/post/2026/11/13/learning-from-outages-protecting-services-and-customers/"
description: "Learn how to protect customers from service outages using FMEA, dependency analysis, failure testing, and controlled recovery."
tags:
  - Software Engineering
  - Reliability
  - Resilience
  - Incident Management
image: /post/2026/11/13/learning-from-outages-protecting-services-and-customers/images/microsoft-outage-article-banner-1080x432.png
---

![Illustration introducing lessons from the Microsoft 365 outage about service resilience, customer protection, and recovery](images/microsoft-outage-article-banner-1080x432.png)

*A practical way to examine your dependencies, customer commitments, and recovery behavior after a major outage.*

A service outage creates two questions for every engineering organization: **What happens to our customers when a service we depend on becomes unavailable? And what happens to our customers when our own service fails or recovers badly?**

The November 12–13, 2026 Microsoft 365 outage is a useful prompt for asking those questions. [Archived Microsoft service-health notices](https://mailservices.isc.upenn.edu/computing/email/penno365/alerts/ms-incidents.html?q=EX1550543) described unavailable servers shifting demand onto remaining infrastructure and additional internal load during recovery. They do not establish that client retries caused the incident, nor do they provide enough detail to reconstruct Microsoft's architecture. We do not need to know every internal cause to learn from the failure patterns and examine our own systems.

This article focuses on that exercise: map critical customer journeys, identify the effects of dependency failure, and test whether your service can degrade and recover without creating further harm.

## Start with the customer journey

List the services your customers rely on and the external services your product depends on. A dependency may be an API, identity provider, payment processor, email platform, cloud service, or an internal system owned by another team.

Then follow a real customer journey from start to finish. For example: *a customer places an order; the system records it; a confirmation is sent through Microsoft 365*. Ask what happens if the email service is unavailable at each step. Can the order still be accepted? Is the confirmation durably queued? Can the customer see that the order succeeded? What happens if delivery is delayed for hours, or the queue fills?

This separates the business function from the dependency used to support it. If sending a confirmation fails, the order may still be valid. If the product treats both as one operation, a temporary email outage could prevent useful work or cause duplicate orders when the customer tries again.

The same questions apply when your service itself is degraded. Which customer actions remain safe? Which should be delayed or rejected? What should users see? Who decides when traffic can be restored?

## Use FMEA to make the risks concrete

Failure Mode and Effects Analysis (FMEA) helps teams list what could fail, how customers or operations would be affected, and what controls could reduce the risk. Begin with one important journey rather than trying to model the whole company.

Here is an illustrative starter table for an order workflow that relies on an external notification service:

| Failure mode | Potential customer effect | Protection to examine | Evidence-producing test |
| --- | --- | --- | --- |
| Notification provider is unavailable | Order succeeds but confirmation is delayed or lost | Durable queue, visible status, bounded retries | Disable the provider in a test environment; verify order completion and later delivery |
| Confirmation times out after the provider accepted it | Duplicate confirmation or duplicate business action | Idempotency key, delivery-state reconciliation | Allow acceptance but drop the response; retry and check for duplicates |
| Queue grows beyond capacity | Notifications are rejected or consume resources needed by core work | Queue limits, backpressure, alerting, explicit overflow behavior | Generate a sustained backlog and verify limits and customer messaging |
| A shared dependency slows down | Threads, connections, or workers remain occupied | Deadlines, concurrency limits, early load shedding | Add latency under realistic load and measure effects on unrelated workflows |
| Retry behavior multiplies across layers | More requests arrive while capacity is falling | One end-to-end retry budget, backoff and jitter | Count downstream attempts per customer action across all layers |
| Service returns and queued work drains too quickly | Recovery creates another period of overload | Rate-limited drain, gradual traffic admission | Restore the dependency with a backlog and observe stability |
| A recovered instance passes a basic health check but cannot sustain load | Returning capacity fails again under traffic | Readiness criteria, staged admission, capacity checks | Restore instances gradually while demand remains high |

A formal FMEA can record causes, severity, likelihood, detectability, existing controls, owners, and verification. Scores can help prioritize work, but they should not hide a severe customer impact behind an average score.

FMEA has limits. It can miss unsafe interactions among components that are each functioning as designed. Fault-tree analysis traces combinations of events that can lead to system failure; Systems-Theoretic Process Analysis (STPA) examines unsafe interactions and control decisions. Use additional methods when the service's complexity or consequences call for them.

## Treat recovery as part of the failure

Teams often test whether a service fails safely, then stop when it comes back. Recovery can be the most demanding part of an outage: traffic returns, queued work accumulates, clients reconnect, and operators apply changes while capacity is constrained.

For every critical dependency, test both loss and restoration:

1. **Slow it down.** Measure timeouts, connection use, worker saturation, queue growth, and impact on unrelated customer journeys.
2. **Make it unavailable.** Confirm whether core work can continue, pause safely, or fail with a clear message.
3. **Restore it with backlog.** Observe retry volume, duplicate effects, queue-drain rate, and overall stability.
4. **Reduce and restore your own capacity.** Verify that health checks, traffic distribution, and gradual admission work under realistic demand.

Define acceptance conditions before testing. Examples include a maximum downstream attempt count per customer action, a queue limit with an explicit overflow path, no duplicate order effects, unaffected workflows staying within latency limits, and a controlled recovery rate.

Run the first exercise as a discussion-based tabletop. Bring together engineering, operations, and someone who understands customer impact. Trace one journey through an assumed outage, identify unanswered questions, and choose a safe experiment. This one-hour discussion does not involve injecting failure into a live service. Run the experiment later in a test or production-like environment with agreed safeguards, monitoring, and stop conditions.

## When a provider outage affects your service

You may not be able to change how Microsoft 365, a payment provider, or an identity service behaves. You can decide how your product behaves when that dependency is unavailable.

For a notification dependency, useful design questions include:

- Can the customer complete the primary transaction without the notification provider?
- Is the notification stored durably, and can delivery be resumed without duplicating effects?
- Are retries bounded across the application, SDK, and infrastructure layers?
- Can the customer see the transaction's real status while a message is pending?
- What happens when the queue reaches its limit?
- Is there an approved alternate channel for time-sensitive notices?
- How will the backlog drain after service returns without overwhelming the provider or your own systems?

Document the business functions that must continue, tolerable delays, queue limits, customer messaging, and operator actions. Then rehearse the decisions and test the behavior. A dependency inventory is useful only when it leads to clear ownership and evidence that the failure path works.

## Put the lessons into practice

Choose one customer journey that matters to your business, identify the dependency most likely to disrupt it, and document what customers would experience if that dependency slowed down, failed, and recovered. Use the findings to design a controlled test with measurable acceptance criteria. The goal is not to predict the next provider outage; it is to demonstrate that your service can protect customers when one occurs.

## Frequently asked questions

### What can we learn from an outage when the provider has not published a full root-cause report?

You can distinguish confirmed observations from unknown causes, then use the observed failure patterns to ask questions about your own architecture. Avoid claiming that a specific safeguard was missing or that a particular retry policy caused the event unless the evidence supports it.

### Should teams inject failures into production?

Not as the first step. Begin with a discussion-based tabletop, then run a controlled experiment in a test or production-like environment. Production testing requires explicit limits, monitoring, rollback conditions, and people prepared to stop the experiment.

### How should an application behave when Microsoft Graph or Exchange is unavailable?

Keep core work independent of the unavailable service where possible. Queue notifications durably, bound retries, make operations idempotent, show users what is pending, and decide what happens when the queue fills. Test both the outage and the backlog drain after service returns.

## Sources and further reading

The article uses Microsoft's public updates as context; they are preliminary incident reports, not a complete post-incident analysis. Detailed service-health notices are available to administrators in the Microsoft 365 admin center. The following independent archive, hosted by the University of Pennsylvania and not operated by Microsoft, preserves copies of notices that are not publicly accessible in that form:

- [Microsoft 365 service status](https://status.cloud.microsoft/) — Microsoft's public status site.
- [Independent archive hosted by the University of Pennsylvania](https://mailservices.isc.upenn.edu/computing/email/penno365/alerts/ms-incidents.html?q=EX1550543) — copies of detailed Microsoft service-health notices.
- [Microsoft's November 13 statement on the initiating network issue and staged restoration](https://x.com/Microsoft/status/2121282013600907325).
- [American Society for Quality: What Is Failure Mode and Effects Analysis?](https://asq.org/quality-resources/fmea).
- [MIT: Systems-Theoretic Process Analysis (STPA) Handbook](https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf).
- [AWS Builders' Library: Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/).
- [Google SRE: Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/).
- [Microsoft Azure Architecture Center: Retry Storm antipattern](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/retry-storm/).
- [Microsoft Azure Architecture Center: Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker).
- [Microsoft Graph throttling guidance](https://learn.microsoft.com/en-us/graph/throttling).
