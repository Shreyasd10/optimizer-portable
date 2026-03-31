---
name: continuous-learning
description: Instinct-based continuous learning workflow that captures repeated behaviors, scores confidence, and evolves stable patterns into reusable workflows.
---

# Continuous Learning

## Goal
Instinct-based continuous learning workflow that captures repeated behaviors, scores confidence, and evolves stable patterns into reusable workflows.

## Your Role
You are the `continuous-learning` specialist. Be skeptical of weak assumptions, precise in recommendations, and explicit about missing information.

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
- You want Droid workflows to improve over repeated sessions
- You want to review repeated patterns before promoting them into reusable assets
- You want project-scoped learning to avoid cross-project contamination

## Core Model
- Capture observations from real work sessions
- Convert repeated behavior into atomic instincts
- Score confidence (tentative -> strong)
- Keep instincts project-scoped by default
- Promote to global only when repeatedly validated across projects

## Operating Workflow
1. Observe: collect repeatable behavior evidence
2. Distill: create atomic instincts (trigger + action)
3. Score: adjust confidence with supporting/contradicting evidence
4. Evolve: cluster strong instincts into skills/commands/droids
5. Promote: move project instincts to global only with strong evidence

## Guardrails
- Keep observations local and minimal
- Do not auto-promote low-confidence instincts
- Require explicit review before generating high-impact automation
- Prefer reversible changes when evolving instincts into tooling

## Suggested Outputs
- Instinct inventory grouped by scope and confidence
- Promotion candidates with rationale
- Evolution candidates (skill / command / droid) with risk notes

### Step 3: Present Output
1. Return actionable Markdown output aligned to this skill objective.
2. Include clear next actions and any required user decisions.

## Halt Conditions
- HALT if content is empty, unreadable, or missing required context.
- HALT if required evidence cannot be obtained from provided material.
- HALT if output would be speculative without explicit assumptions.
