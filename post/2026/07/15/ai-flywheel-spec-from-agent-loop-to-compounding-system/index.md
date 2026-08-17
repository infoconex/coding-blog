---
title: "AI Flywheel Spec – From Agent Loop to Compounding System"
date: "2026-07-15"
description: "The AI Flywheel specification defines an evidence-driven operating model where execution improves the system used by future execution."
tags: ["ai", "ai flywheel", "agentic ai", "software engineering"]
slug: "ai-flywheel-spec-from-agent-loop-to-compounding-system"
author: "Jim Scott"
permalink: "/post/2026/07/15/ai-flywheel-spec-from-agent-loop-to-compounding-system"
---
AI-assisted development usually starts with a simple loop: ask an AI to do something, review the result, correct it, and try again.

That can be useful, but a loop by itself does not compound.

The idea behind the [Infoconex AI Flywheel](https://github.com/infoconex/ai-flywheel-spec) is that execution should produce evidence that can improve the operating system used by later execution.

> **A loop repeats. A flywheel compounds.**

That distinction is the reason I started formalizing the AI Flywheel as a specification rather than leaving it as a collection of prompts and habits.

## The problem with ordinary agent loops

An AI agent may be able to plan, write code, run tools, retry failures, and even reflect on what happened. But none of those capabilities guarantees that the next execution begins from a better operating state.

A retry can repeat work without learning.

Memory can retain information without changing behavior.

Reflection can produce an observation that is never validated or reused.

Self-modifying code can change the wrong thing.

The missing piece is a governed mechanism for deciding what was learned, where that learning belongs, whether it is supported by evidence, and whether it should affect future work.

That is the job of the specification.

## The lifecycle

The AI Flywheel lifecycle is:

**Execute → Observe → Evaluate → Classify → Adapt → Validate → Persist → Reuse**

Each stage has a distinct responsibility.

### Execute

Perform the work using the current operating model. That may involve deterministic tools, procedural guidance, and AI reasoning working together.

### Observe

Capture what actually happened. The important word is **evidence**. The system should not improve itself based only on a plausible explanation of what might have happened.

### Evaluate

Compare the observed outcome with the intended result and success criteria.

### Classify

Determine what was learned, whether a change is justified, and where the learning belongs.

A lesson might belong in code, a procedure, validation logic, durable knowledge, a failure rule, or nowhere at all.

### Adapt

Create a candidate improvement when the evidence supports one. Adaptation is not mandatory. A successful cycle may simply reinforce an existing operating pattern.

### Validate

Test the proposed improvement or determine whether a no-change conclusion is sufficiently supported.

### Persist

Store validated and authorized learning in a durable operational asset.

### Reuse

Future execution begins from that updated operating state.

That final step is what turns repeated execution into a flywheel.

## Three mechanisms during execution

The operating model deliberately separates three different kinds of capability.

**Deterministic capability** handles work that can be made reliable and repeatable: scripts, programs, validators, API integrations, and other executable tools.

**Procedural guidance** describes how work should be performed, including ordering, constraints, escalation rules, and judgment that is too contextual to hard-code.

**AI reasoning** handles ambiguity, interpretation, orchestration, and decisions that cannot yet be reduced to deterministic behavior.

These are not lifecycle stages. They operate together during execution.

After execution, evidence may show that responsibility should move between them.

## The moving determinism boundary

One concept I find particularly useful is the **Moving Determinism Boundary**.

When a workflow is new, more responsibility may live in AI reasoning because the problem is still ambiguous. As execution produces evidence, repeated behavior can often move into a deterministic capability.

For example, imagine an AI repeatedly needs to inspect a repository and determine whether a set of files satisfies a known structural rule.

The first few times, the AI may reason through the structure manually. Once the rule is understood and stable, it may be better represented as a validator.

The next execution should use the validator rather than ask the model to rediscover the rule.

The Flywheel therefore does not assume that AI reasoning is always the most advanced solution. In many cases, successful AI operation should produce **less** reliance on probabilistic reasoning for known tasks.

## The authority boundary is different

The determinism boundary can move as evidence accumulates.

The **Authority Boundary** does not move simply because the AI has become confident.

Human authority defines what the system may execute, change, approve, or persist autonomously. Some operations can be delegated completely. Others require approval. Some should remain prohibited.

That separation matters because a self-improving system without an explicit authority model can confuse technical capability with permission.

Being able to make a change is not the same as being authorized to make it.

## A concrete example

Suppose an AI is responsible for maintaining a release process.

During execution it discovers that releases occasionally fail because a generated package includes a local development directory.

The Flywheel does not stop at "remember not to include that directory."

It can work through the lifecycle:

1. **Execute** the release and encounter the failure.
2. **Observe** the exact package contents and failed validation.
3. **Evaluate** the result against the release criteria.
4. **Classify** the lesson as a deterministic validation problem.
5. **Adapt** by adding a package-content check.
6. **Validate** the new check against both good and bad packages.
7. **Persist** the validator as part of the release tooling.
8. **Reuse** it automatically in every later release.

The lesson has moved from transient reasoning into a reusable deterministic capability.

That is much stronger than telling the agent to "be more careful next time."

## Why make this a specification?

Once a system can change the way it performs work, vague terminology becomes dangerous.

What counts as evidence?

When is adaptation justified?

What must be validated before learning becomes persistent?

What does conformance mean?

Where does human authority apply?

A specification gives those questions stable definitions and creates a target that implementations can be tested against.

It also keeps the methodology separate from any particular implementation. The Flywheel does not require Python, PowerShell, a specific agent platform, a particular model, or one CLI.

The specification defines the operating model. Implementations can change underneath it.

## What the Flywheel is not

The specification deliberately avoids treating common AI features as sufficient on their own.

A retry loop is not automatically a Flywheel.

An agent with memory is not automatically a Flywheel.

Reflection is not automatically a Flywheel.

An autonomous coding system is not automatically a Flywheel.

The defining property is that execution produces evidence, evidence is evaluated and governed, supported learning changes or reinforces durable operating assets, and future execution reuses that validated state.

## Why this matters for software engineering

AI can now generate code faster than teams can reliably review it.

That makes the surrounding engineering system more important, not less.

Specifications, tests, evidence, deterministic tooling, authority boundaries, and repeatable validation become the structure that makes increased execution speed useful rather than chaotic.

The AI Flywheel is an attempt to make that structure explicit.

The goal is not an AI that changes itself constantly.

The goal is an operating model that **learns only when the evidence justifies learning, changes the right thing, validates the change, and compounds the result over time**.
