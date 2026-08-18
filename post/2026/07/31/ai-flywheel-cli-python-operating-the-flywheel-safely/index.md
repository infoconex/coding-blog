---
title: "AI Flywheel CLI for Python – Operating the Flywheel Safely"
date: "2026-07-31"
description: "The Python AI Flywheel CLI provides local commands for inspection, validation, lifecycle operations, installation, and upgrade with explicit safety boundaries."
tags: ["Python", "AI", "AI Flywheel", "CLI"]
slug: "ai-flywheel-cli-python-operating-the-flywheel-safely"
author: "Jim Scott"
permalink: "/post/2026/07/31/ai-flywheel-cli-python-operating-the-flywheel-safely"
---
Once the AI Flywheel specification and framework existed, the next practical question was obvious:

**How should a person or AI operator inspect and operate the framework from the command line without turning every action into an ad hoc script?**

That led to [ai-flywheel-cli-python](https://github.com/infoconex/ai-flywheel-cli-python), a cross-platform command-line application for inspecting, installing, validating, upgrading, and operating AI Flywheel artifacts in a repository.

The CLI is not the specification and it is not the framework. It is one implementation for operating them.

## Why Python

The first CLI implementation uses Python because it provides a practical cross-platform runtime, strong packaging support, mature testing tools, and a good fit for structured file validation and command-line workflows.

The important architectural point is that the framework itself does not depend on Python. The framework remains implementation-neutral.

That means another implementation could exist later without changing the underlying operating model.

## Start with read-only commands

A good operations CLI should make inspection easier than mutation.

The CLI therefore includes commands such as:

```text
flywheel doctor .
flywheel status .
flywheel validate .
```

`doctor` checks repository prerequisites.

`status` reports whether Flywheel artifacts are installed and whether the current installation validates.

`validate` checks required files, state invariants, active references, execution parentage, filename-to-ID consistency, and lifecycle completeness.

These commands make the operating state visible before anyone starts changing it.

## Structured output matters

Automation should not have to parse prose to determine whether something failed.

The CLI can return JSON and uses an explicit exit-code contract.

For example, a validation failure returns a Flywheel-specific exit code with structured category and reason fields.

That allows a script or AI operator to distinguish between things such as validation failure, repository conflict, lock contention, a governed AI fallback, and another expected operation failure.

This is a small design detail with a large operational benefit: failure becomes machine-readable without becoming mysterious to humans.

## Operating the execution lifecycle

The CLI also exposes commands for lifecycle transitions.

An execution can be started for a ready goal:

```text
flywheel start-execution <mission-id> <goal-id> <execution-id> \
  --intended-outcome "<outcome>" \
  --repository .
```

It can then advance through the lifecycle:

```text
flywheel advance-lifecycle \
  --summary "<summary>" \
  --ref <record-id> \
  --expected-stage <stage> \
  --repository .
```

After validation, the execution can be persisted and eventually completed through Reuse.

The CLI enforces stage boundaries, references, schemas, and state transitions rather than leaving those rules to the caller.

That is exactly the kind of work that should move out of AI reasoning and into deterministic capability.

## Installation is plan-first

Repository mutation is where command-line convenience can become dangerous.

For that reason, installation and upgrade are plan-first operations.

A command such as:

```text
flywheel install . \
  --archive ai-flywheel-framework.zip \
  --checksum <sha256> \
  --framework-version 0.1.0
```

produces a plan without applying it.

Mutation requires an explicit `--apply`.

That makes review part of the normal workflow rather than an optional debugging technique.

## Safety is part of the product contract

The CLI verifies SHA-256 checksums before extraction, rejects unsafe archive paths, acquires a repository mutation lock, stages changes, and records installation metadata only after success.

It also refuses to silently overwrite an existing `.flywheel` installation.

Upgrade follows the same philosophy. It refuses to overwrite locally modified framework-owned files and protects mutable operating content such as missions, goals, executions, evidence, approvals, and knowledge from being treated like replaceable framework files.

Those distinctions are important because "upgrade the framework" should not mean "replace the repository's accumulated operating history."

## Atomic state changes

An AI-assisted workflow can fail halfway through an operation just like any other software.

The CLI therefore treats state mutation as an operation that needs locking, staging, validation, and rollback behavior.

Temporary runtime files live under:

```text
.flywheel/.runtime/
```

That directory holds local locks, staging data, and build output and is not intended to be committed.

This keeps ephemeral execution mechanics separate from durable Flywheel state.

## The CLI is deliberately incomplete

One design goal is to avoid turning the CLI into a giant command surface simply because something could be automated.

The first implementation focuses on inspection, validation, framework installation and upgrade, and execution lifecycle transitions.

Some administrative operations remain deferred.

Release discovery is not implicit. The initial implementation expects a verified archive and checksum rather than silently locating and downloading whatever appears to be current.

Hosted execution is also not automatically enabled.

These are useful examples of an important rule: automation should expand only when its authority, verification, and failure behavior are understood.

## A practical repository workflow

A typical local flow can look like this:

```text
python -m venv .venv
python -m pip install -e ".[dev]"
flywheel doctor . --json
flywheel status .
flywheel validate . --json
```

If a framework installation is needed, generate the install plan first, review it, then explicitly apply it.

Once a mission and goal are ready, use the lifecycle commands to start and advance an execution while the CLI enforces the structural rules.

The AI can still provide reasoning and orchestration, but it does not need to manually edit state files for operations the CLI already knows how to perform safely.

## Determinism is the point

The Python CLI is a good example of the Moving Determinism Boundary from the AI Flywheel specification.

At first, an AI could manipulate YAML files directly and reason about lifecycle transitions each time.

Once those rules are understood, repeating that reasoning is unnecessary risk.

The stable parts belong in deterministic tooling.

The CLI turns known operating rules into executable constraints while leaving contextual decisions and judgment where they belong.

That is the larger purpose of the project: not to replace AI reasoning, but to make the parts that no longer require reasoning predictable, testable, and safe.
