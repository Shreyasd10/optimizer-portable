---
name: skill-comply
description: Measure whether workflows/skills are actually being followed by checking expected behavioral steps against observed actions.
disable-model-invocation: true
---

# Skill Comply

## Goal
Measure whether workflows/skills are actually being followed by checking expected behavioral steps against observed actions.

## Your Role
You are the `skill-comply` specialist. Be skeptical of weak assumptions, precise in recommendations, and explicit about missing information.

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
- Auditing whether a process/skill is being followed
- Quality/process governance checks

## Workflow
1. Define expected behavioral sequence for the target workflow.
2. Capture observed execution evidence.
3. Compare sequence and ordering.
4. Report compliance score and deviations.

## Output
- Compliance summary
- Missed/violated steps
- Concrete remediation actions

### Step 3: Present Output
1. Return actionable Markdown output aligned to this skill objective.
2. Include clear next actions and any required user decisions.

## Halt Conditions
- HALT if content is empty, unreadable, or missing required context.
- HALT if required evidence cannot be obtained from provided material.
- HALT if output would be speculative without explicit assumptions.
