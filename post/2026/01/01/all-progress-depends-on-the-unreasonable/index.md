---
title: "All Progress Depends on the Unreasonable"
date: "2026-01-01"
description: "Progress often starts when someone questions a constraint everyone else has learned to accept. In software and organizations, constructive unreasonableness is often what turns inherited limitations into better systems."
tags: ["software engineering", "architecture", "leadership", "change management"]
slug: "all-progress-depends-on-the-unreasonable"
author: "Jim Scott"
permalink: "/post/2026/01/01/all-progress-depends-on-the-unreasonable"
---
A new year naturally invites improvement. We make lists, set goals, tighten processes, and promise ourselves that this time we will execute more consistently.

There is value in all of that. But improvement inside an existing system is not the same thing as changing the system itself.

Some of the most important progress I have seen in software has started with a person asking a question that sounded unreasonable at first:

- Why does this deployment have to take two hours?
- Why are we maintaining the same rule in four different applications?
- Why does this service need to know how the database stores the data?
- Why are we afraid to change this code?
- Why is this process still manual?
- Why is "we have always done it this way" being treated as a requirement?

Those questions can be uncomfortable because mature systems accumulate assumptions. Some are legitimate constraints. Others are simply decisions that survived long enough to become invisible.

That distinction matters.

## Reasonable systems preserve themselves

Software teams need stability. Production systems need controls. Organizations need conventions. A team that challenges every decision every day will spend more time debating than delivering.

So we learn to adapt.

We learn the build process. We work around the awkward API. We add another conditional to the legacy service. We memorize which job must be restarted after deployment. We accept that a report takes fifteen minutes because it has always taken fifteen minutes.

This kind of adaptation is often rational. It keeps work moving.

The danger is that adaptation can slowly become acceptance.

A temporary workaround becomes architecture. A limitation becomes policy. A historical accident becomes "best practice." Eventually the system is no longer shaped primarily by what we would design today. It is shaped by what everyone has learned not to question.

## Constructive unreasonableness

Being unreasonable does not mean ignoring constraints or dismissing experience. It means refusing to assume that today's constraints are permanent simply because they are familiar.

In engineering, constructive unreasonableness usually has three characteristics.

First, it is **grounded in evidence**. The goal is not to challenge something for the sake of being disruptive. There should be a real problem: excessive lead time, operational risk, duplicated logic, poor reliability, difficult testing, unnecessary coupling, or some other measurable cost.

Second, it is **specific about the alternative**. "This is bad" is not a design. A useful challenge comes with a direction: automate the deployment, isolate the dependency, move the rule behind an abstraction, simplify the data flow, remove an unnecessary layer, or make ownership explicit.

Third, it is **willing to confront tradeoffs**. Better systems are rarely free. A proposed change may require migration work, temporary duplication, retraining, new monitoring, or accepting a different kind of complexity. Constructive resistance acknowledges those costs instead of pretending they do not exist.

That is what separates useful unreasonableness from recklessness.

## Legacy code needs unreasonable questions

Legacy systems are an especially good place to see this dynamic.

A codebase can contain choices that made perfect sense ten years ago but no longer match the environment around it. Dependencies change. Hosting changes. traffic changes. Teams change. What was once the simplest design may eventually become the thing preventing the next change.

The easy response is to keep adapting ourselves to the old design.

The harder response is to ask whether the design should still have that authority.

Consider a service that directly creates a SQL connection, sends email, writes files, formats reports, and applies business rules. The reasonable response to a new requirement may be to add another branch to the existing class because that is the lowest-risk local change.

The unreasonable question is different:

**Why should one class own all of those reasons to change?**

That question may lead to separating responsibilities, introducing clearer boundaries, or moving infrastructure details behind abstractions. It may create more files while producing a system that is much easier to change safely.

This is one reason principles such as SOLID remain useful. They give us language for challenging designs that technically work but have accumulated too many responsibilities, dependencies, or assumptions.

## Architecture is a record of accepted assumptions

Every architecture contains assumptions about the future.

We assume a database will remain the system of record. We assume a service boundary will remain useful. We assume a vendor API will remain stable. We assume a workload will stay within a certain scale. We assume a particular team will continue owning a particular capability.

There is nothing wrong with making assumptions. Engineering would be impossible without them.

Problems appear when we forget that they were assumptions in the first place.

Good architectural work therefore involves occasionally reopening questions that appear settled:

- Is this boundary still helping us?
- Is this abstraction still hiding something useful?
- Is this dependency still justified?
- Are we paying complexity for a future that never arrived?
- Are we preserving a design because it is good, or because changing it feels expensive?

Sometimes the answer is that the existing design is still correct. That is a valuable result too. Challenging an assumption does not obligate us to replace it.

But assumptions that can never be questioned are no longer engineering decisions. They are doctrine.

## "Best practice" is context, not proof

One of the easiest ways to stop a useful engineering discussion is to label something a best practice.

Best practices can encode decades of experience, and ignoring that experience casually is foolish. But the phrase can also become a substitute for understanding.

A practice is useful because it addresses particular risks under particular conditions. If we cannot explain those conditions, we are not applying a principle; we are copying a rule.

That is where a little unreasonableness helps.

Why do we need this pattern here?

What failure does this extra service prevent?

What does this abstraction buy us?

What happens if we choose the simpler implementation?

Those questions do not reject established practice. They force us to understand why we are using it.

## Progress needs people who are willing to create friction

The person asking these questions is not always the easiest person in the meeting.

They may slow down a decision that appeared settled. They may force a team to explain a process everyone else has simply inherited. They may point out that an efficient workflow is efficiently producing the wrong outcome.

That friction can be healthy.

Teams need people who can distinguish productive disagreement from obstruction. The goal is not to win arguments. The goal is to make sure important assumptions receive enough pressure before they become permanent constraints.

The best challengers I have worked with are not contrarians. They listen carefully, understand the history, respect genuine constraints, and then ask the question anyway.

They are willing to say: I understand why we got here. I am not convinced we still need to stay here.

## A useful question for 2026

As 2026 begins, I am less interested in asking how efficiently we can adapt to every system already around us.

A more useful question is:

**Which constraints are real, and which ones have we simply become good at living with?**

In software, architecture, and organizations, progress often begins when someone is willing to examine that difference.

Not every unreasonable idea deserves to survive contact with reality. But neither should every existing reality be allowed to survive without being questioned.

That tension is where a great deal of worthwhile engineering happens.

---

*This article was adapted from my LinkedIn article, [All Progress Depends on the Unreasonable](https://www.linkedin.com/pulse/all-progress-depends-unreasonable-jim-scott-b0vtc), originally published January 1, 2026.*
