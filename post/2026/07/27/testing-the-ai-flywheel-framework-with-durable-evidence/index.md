---
title: "Testing the AI Flywheel Framework with Durable Evidence"
date: "2026-07-27"
description: "The AI Flywheel testing project separates framework implementation from repeatable prompts, fixtures, runners, and durable evidence."
tags: ["AI", "AI Flywheel", "Testing", "Software Engineering"]
slug: "testing-the-ai-flywheel-framework-with-durable-evidence"
author: "Jim Scott"
permalink: "/post/2026/07/27/testing-the-ai-flywheel-framework-with-durable-evidence"
series: "AI Flywheel"
seriesOrder: 4
---
AI-assisted development makes it easy to produce changes quickly.

That increases the value of testing, but it also changes what I want from the test system.

For the AI Flywheel Framework, I did not want tests to be an informal collection of prompts and screenshots. I wanted repeatable inputs, immutable source revisions, durable evidence, and results that could be traced back to the exact framework behavior being evaluated.

That is why the testing work lives in a separate repository: [ai-flywheel-framework-testing](https://github.com/infoconex/ai-flywheel-framework-testing).

## Why testing is separate from the framework

The framework is the thing being tested.

If all of the test prompts, fixtures, expected results, runners, and captured evidence lived inside the framework repository, it would be easy for test assumptions and implementation assumptions to evolve together.

Separating them creates a cleaner boundary.

The testing repository can change the way it challenges the framework without those assets becoming part of the distributed framework itself.

It also makes version pinning much clearer: a test result can identify the exact framework revision and the exact test revision used to produce it.

## The goal is reproducible evidence

A test should answer more than "did this seem to work?"

For AI-driven behavior I want to know:

- What exact prompt or scenario was used?
- What fixture did the AI operate against?
- Which framework revision was installed?
- Which testing revision defined the expectation?
- What actions occurred?
- What evidence was captured?
- What was the expected behavior?
- What actually happened?
- Is the failure in the framework, the test, or the expectation?

That is a much stronger basis for changing an operating model than conversational memory or a one-off successful run.

## Testing the normal path is not enough

The repository is intended to evaluate the framework across several kinds of scenarios:

- normal behavior;
- boundary conditions;
- expected failures;
- recovery behavior;
- invalid or incomplete operating state;
- authority and lifecycle constraints.

This is especially important for agentic systems because many defects only become visible when the system is uncertain, partially configured, interrupted, or presented with conflicting evidence.

A framework that works only on the happy path is not ready to govern autonomous work.

## Immutable inputs matter

If a test always runs against `main`, the meaning of an old result can become ambiguous.

The framework may have changed.

The prompt may have changed.

The fixture may have changed.

The expected behavior may have changed.

That is why a meaningful result should identify immutable revisions.

A result that says "framework commit A, test commit B, fixture C produced outcome D" can be investigated later.

A result that says "I ran the latest version and it looked good" cannot.

## A practical example

Consider a startup rule in the framework: the AI operator must begin with `.flywheel/manifest.yaml` and follow the entrypoint defined there.

A useful test fixture can deliberately provide an invalid manifest.

The expected behavior is not that the AI searches the repository for another plausible startup file.

The expected behavior is that it stops and reports an operating-model defect.

A test can therefore capture:

1. the exact framework revision;
2. a fixture with a malformed manifest;
3. the exact AI prompt used to initiate operation;
4. the observed actions;
5. whether the AI stopped at the required boundary;
6. the resulting report or evidence.

If the AI silently invents another traversal path, the test has exposed a framework or instruction defect.

If the expected behavior was wrong, the test has exposed a test defect instead.

Both are useful findings.

## Tests should expose ambiguity, not hide it

One danger in automated testing is writing assertions that simply confirm the implementation's current behavior.

That creates false confidence.

For the Flywheel, tests should be grounded in the specification and framework contracts. They should challenge whether the implementation preserves required behavior rather than merely snapshotting whatever it currently does.

That distinction is important whenever AI is involved because generated tests can easily mirror generated code.

Two pieces of generated work agreeing with each other is not independent evidence that either one is correct.

## Evidence becomes input to improvement

The testing repository is not outside the Flywheel concept. It is part of how the Flywheel can improve safely.

A failed scenario produces evidence.

That evidence can be evaluated and classified:

- Is the framework missing guidance?
- Is a schema too permissive?
- Is a lifecycle rule ambiguous?
- Is the prompt asking for something outside the intended authority boundary?
- Is the fixture unrealistic?
- Is the test itself asserting the wrong behavior?

Only after that classification should a change be proposed.

Then the same test—or a strengthened version of it—can validate the candidate improvement.

## Human judgment still matters

Automation can tell us whether an observed result matched an encoded expectation.

It cannot automatically prove that the expectation represents the right product behavior.

Humans still define the authority model, intended outcomes, risk tolerance, and what constitutes sufficient evidence.

This is why I do not view automated AI testing as a way to remove human review.

It is a way to make human review better informed and more reproducible.

## What this changes about AI development

When AI can generate implementation quickly, the bottleneck moves.

The hard problem becomes establishing confidence that the system behaves correctly across the cases that matter.

That pushes engineering attention toward:

- explicit specifications;
- immutable test inputs;
- independent expectations;
- durable evidence;
- boundary and recovery scenarios;
- traceability between defects and fixes.

In other words, faster code generation makes disciplined verification more valuable.

The goal of the AI Flywheel testing project is not simply to produce a green test result.

It is to create enough trustworthy evidence that framework changes can be accepted, rejected, or refined for reasons we can explain later.
