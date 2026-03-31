---
name: manual-test-design
version: 1.0.0
description: |
  Design repeatable script-based manual verification flows for APIs, databases, and service interactions.
  Use when a manual test should become a reusable bundle of scripts and checks.
---

# Manual test design

Use this skill when a manual verification flow should be turned into a repeatable script bundle.

## Goal

Transform ad hoc testing into a structured bundle that can be rerun with minimal guesswork.

## Typical use cases

- call create APIs to seed data
- inspect DB state before a change
- call update or processing APIs
- inspect DB state after a change
- verify state across more than one service
- capture cleanup and rerun steps

## Output shape

Design a bundle that should default to:
- `run-test.sh`
- `.env.example`
- `expected-results.md`
- optional `setup.sql`
- optional `before.sql`
- optional `after.sql`
- optional `cleanup.sql`
- optional request payload files
- optional `artifacts/` output folder

## Workflow

### 1. Define the scenario

State:
- what system behavior is being verified
- what input state is required
- what exact change should happen
- what observable evidence proves success

### 2. Break the flow into stages

Common stages:
1. environment and auth setup
2. seed or setup actions
3. before-state inspection
4. main action call
5. after-state inspection
6. cross-service verification if needed
7. cleanup

### 3. Choose the right artifact for each stage

- shell script for orchestration
- curl commands for API calls
- SQL files for DB checks
- env files for hosts, creds, tokens, IDs
- markdown report for expected outcomes and operator notes

### 4. Make the checks explicit

For each check, define:
- command to run
- expected output or state
- failure signal
- whether execution should stop on failure or continue gathering evidence

## Design rules

- Keep secrets out of generated files.
- Put environment-specific values behind variables.
- Prefer idempotent setup and cleanup when possible.
- Make before and after checks easy to compare.
- If multiple services are involved, label each service boundary clearly.

## When to prefer this over normal automated tests

Use script-based manual bundles when:
- the verification depends on live infrastructure or environment wiring
- DB state inspection is part of the acceptance criteria
- multiple services must be checked together
- the workflow is too operational for a narrow unit or integration test right now

## What not to do

- Do not call it manual if the flow is opaque and unreproducible.
- Do not mix credentials directly into scripts.
- Do not generate one giant unreadable script if separate SQL or payload files would make the flow clearer.

## Verify it worked

Before finishing, confirm:
- the scenario has a clear start state and end state
- each verification step has an explicit command or artifact
- rerunning the bundle would be understandable to another engineer
- the bundle has a clear expected-results artifact that explains what pass and fail look like
