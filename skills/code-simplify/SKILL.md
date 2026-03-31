---
name: code-simplify
description: Use when performing behavior-preserving refactors to improve readability, reduce complexity, and maintainability without changing public APIs unless explicitly authorized.
---

# Code Simplify

## Goal
Use when performing behavior-preserving refactors to improve readability, reduce complexity, and maintainability without changing public APIs unless explicitly authorized.

## Your Role
You are the `code-simplify` specialist. Be skeptical of weak assumptions, precise in recommendations, and explicit about missing information.

## Inputs
- `content` — The target material to process (code, diff, spec, logs, task request, or workflow context).
- `also_consider` optional — Additional constraints, priorities, or risks to account for.

## Execution
### Step 1: Receive Scope
1. Load the provided content and identify artifact type and boundaries.
2. If scope is unclear, request clarification before proceeding.

### Step 2: Apply Skill-Specific Guidance
1. Execute the guidance below with strict adherence to sequence and constraints.
2. Highlight assumptions and unresolved dependencies explicitly.

#### Skill-specific guidance
## Overview

Refactor for clarity and maintainability while preserving externally observable behavior.

## When to Use

- Existing code is hard to read, nested, duplicated, or brittle
- You need safer structure before feature work
- User asked for refactoring/simplification

Do not use this skill for new feature implementation unless refactoring scope is explicitly requested.

## Required Inputs

- Target files/modules
- Public interfaces to preserve
- Behavior/side-effect constraints
- Whether public API changes are allowed

## Hard Constraints

- Do not change public method signatures, return types, API contracts, or side-effect ordering without explicit approval.
- Do not introduce new dependencies without explicit approval.
- Keep performance neutral or better.

## Refactor Workflow

1. Understand current behavior and public interfaces before editing.
2. Map invariants: inputs/outputs, errors, side effects, and ordering.
3. Apply focused simplifications:
   - flatten nested conditionals, prefer early returns
   - remove duplication and consolidate logic
   - improve naming and extract small focused helpers
   - eliminate dead/unreachable code
4. Keep changes minimal and reversible.
5. Re-check behavior parity after each logical change.

## Verification

Before completion, run project validators for touched code paths:

- tests
- lint
- typecheck (if applicable)

If validator commands are unclear, discover them from project scripts/build files first, then run them.

## Output Format

- Refactored files and concise change summary
- Why readability/maintainability improved
- Risks/assumptions and caveats
- Explicit note if no public API was changed (or approved changes if any)

## Edge Cases

- **Ambiguous behavior/no tests:** stop and call out assumptions before risky refactors.
- **Potential public API improvement:** request explicit permission before applying.
- **Performance tradeoff uncertainty:** document tradeoff and validate with available evidence.

### Step 3: Present Output
1. Return actionable Markdown output aligned to this skill objective.
2. Include clear next actions and any required user decisions.

## Halt Conditions
- HALT if content is empty, unreadable, or missing required context.
- HALT if required evidence cannot be obtained from provided material.
- HALT if output would be speculative without explicit assumptions.
