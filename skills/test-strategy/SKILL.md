---
name: test-strategy
version: 1.0.0
description: |
  Decide what tests should exist for a feature, bugfix, or coverage effort.
  Use when choosing between unit, integration, API, end-to-end, and script-based manual verification.
---

# Test strategy

Use this skill to decide the right test mix before writing or expanding tests.

## Goal

Turn a change request, feature plan, or coverage gap into a practical testing plan.

## Questions this skill answers

- What should be tested?
- What can stay untested without creating real risk?
- Which checks belong in unit, integration, API, E2E, or script-based manual verification?
- Which flows are business-critical or regression-prone?
- What should be added now versus later?

## When to use it

Use this skill when:
- a planner finished a feature plan and implementation is about to start
- an existing area needs better coverage
- a bugfix needs the right regression protection
- a system crosses API, DB, or service boundaries and the right test layer is not obvious

## Output shape

Produce a short testing plan with these sections in order:
- similar existing tests or helpers
- critical paths
- edge cases
- recommended automated tests
- recommended script-based manual checks
- out-of-scope checks for now

For each recommended item, use this structure:
- priority: `P0` | `P1` | `P2`
- behavior:
- recommended layer:
- why this layer:
- automate now: `yes` | `no`
- validator:

## Decision rules

### Start with risk

Test the areas where failure would matter most:
- business rules
- data mutation
- auth or permission rules
- external integrations
- persistence changes
- cross-service interactions
- known flaky or historically fragile areas

### Use the narrowest test that gives confidence

- Unit tests for pure logic and branching
- Integration tests for repositories, DB interactions, and wiring
- API tests for contract behavior and endpoint rules
- E2E tests for a few critical user journeys
- Script-based manual bundles when verification spans APIs, databases, services, or environment state in a way that is awkward to encode as regular automated tests right now

### Separate automated from script-based manual work

Automate when the check is stable, repeatable, and worth rerunning often.

Prefer script-based manual bundles when:
- setup is operationally heavy
- multiple services must be inspected together
- DB state must be checked directly
- the workflow is currently exploratory but should still be reproducible

## Coverage planning for existing code

When improving coverage for old code:
- find the most important untested branches
- prioritize regression-prone logic before chasing raw coverage numbers
- prefer a few strong tests over many shallow ones
- identify whether missing tests come from hard-to-test design that should be simplified first
- search for similar tests and helpers before proposing new patterns

## What to include in a plan

For each recommended test item, state:
- behavior being proved
- suggested test layer
- why that layer is appropriate
- whether it should be automated now
- how it should be validated
- the likely existing test file, helper, or pattern to reuse when known

## What not to do

- Do not recommend E2E for everything.
- Do not optimize for coverage percentage alone.
- Do not blur together unit, integration, and manual verification.
- Do not create a plan so broad that no one knows what to implement first.

## Verify it worked

Before finishing, confirm:
- each high-risk behavior has a proposed proving strategy
- automated and manual/scripted checks are clearly separated
- the recommended work is small enough to execute incrementally
