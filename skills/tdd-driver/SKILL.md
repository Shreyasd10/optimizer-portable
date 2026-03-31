---
name: tdd-driver
version: 1.0.0
description: |
  Drive implementation through a strict test-driven loop.
  Use when a feature, bugfix, or refactor should be built with red-green-refactor instead of code-first changes.
---

# TDD driver

Use this skill when the implementation should move in small, test-first slices.

## Goal

Keep the work inside a tight loop:

1. pick the smallest next behavior slice
2. write one failing test
3. implement only enough to make it pass
4. refactor without changing behavior
5. rerun the relevant checks

## When to use it

Use this skill when:
- a planned feature is ready for implementation
- a bugfix should be locked down with a regression test first
- the user explicitly asks for TDD
- the code is risky enough that small validated steps are safer than large edits

Do not use it when:
- the task is pure research or planning
- there is no realistic way to validate behavior yet
- the user explicitly does not want TDD

## Core rules

- Never start with implementation code when a failing test can be written first.
- Keep slices small enough that one test or one tiny cluster of tests drives the next change.
- Prefer behavior-focused tests over implementation-detail tests.
- After green, clean up the code before moving to the next slice.
- Do not claim progress without fresh test evidence.

## Workflow

### 1. Pick the next slice

Define the smallest user-visible or system-visible behavior that can be tested next.

Good slices:
- one method behavior
- one endpoint rule
- one validation case
- one regression condition

Bad slices:
- half a subsystem
- an entire feature with multiple branches
- broad horizontal scaffolding with no proving test

### 2. Write the failing test

Before any implementation change:
- identify the right test layer
- add or update a test that proves the missing behavior
- run the smallest relevant test command
- confirm it fails for the expected reason

If the test cannot fail clearly, the slice is probably too large or the test is poorly chosen.

### 3. Make it pass

Change the production code as little as possible.

Rules:
- solve only the failure in front of you
- do not opportunistically implement future slices
- prefer existing patterns and abstractions
- avoid unrelated refactors during the red-to-green step

### 4. Refactor

Once tests pass:
- clean duplication
- improve naming
- simplify logic
- remove temporary scaffolding if it is no longer needed

Keep behavior fixed while refactoring. Rerun tests after the cleanup.

### 5. Repeat

Move to the next smallest failing test and continue until the requested behavior is complete.

## How to choose the test level

- Unit test: isolated business logic and branching behavior
- Integration test: repository, DB, wiring, serialization, service boundaries
- API or endpoint test: request-response rules and contract behavior
- E2E test: only when lower layers are not enough for confidence

Default to the narrowest layer that proves the behavior.

## What not to do

- Do not write a large batch of tests before any code changes.
- Do not implement a large chunk and add tests afterward while calling it TDD.
- Do not keep going after a failing test without first understanding why it failed.
- Do not use mocks so aggressively that the test stops proving real behavior.

## Handoff guidance

If another droid is implementing:
- tell it the exact slice being worked on
- tell it which test should fail first
- tell it which validator proves green
- require it to report red, green, and refactor outcomes separately

## Verify it worked

Before finishing, confirm:
- the final slice has automated test coverage
- relevant tests pass on current code
- any broader validators required by the repo also pass
- the diff does not include speculative code that no test forced
