---
name: search-first
description: Research-before-coding workflow that checks existing patterns, tools, and repository implementations before writing new code.
---

# Search First

## Goal
Research-before-coding workflow that checks existing patterns, tools, and repository implementations before writing new code.

## Your Role
You are the `search-first` specialist. Be skeptical of weak assumptions, precise in recommendations, and explicit about missing information.

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
## When to Use
- New features likely have existing patterns
- Dependency/tooling choices
- Avoiding duplicate abstractions

## Workflow
1. Search local codebase for existing implementation.
2. Search known/internal patterns and approved dependencies.
3. Compare adopt vs extend vs build-custom.
4. Proceed with smallest safe approach.

### Step 3: Present Output
1. Return actionable Markdown output aligned to this skill objective.
2. Include clear next actions and any required user decisions.

## Halt Conditions
- HALT if content is empty, unreadable, or missing required context.
- HALT if required evidence cannot be obtained from provided material.
- HALT if output would be speculative without explicit assumptions.
