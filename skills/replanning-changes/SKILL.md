---
name: replanning-changes
description: Use when an existing approved plan, task list, or in-flight implementation must be revised because requirements, constraints, dependencies, or execution reality changed.
---

# Replanning Changes

## Overview

Use this skill to revise work that already has a plan or has already started.

The core principle is preservation before replacement: keep valid completed work, isolate what changed, and update only the affected plan sections with a clear decision trail.

## When to Use

Use this skill when:
- there is already an approved implementation plan
- execution has already started and new information invalidates part of the plan
- requirements, scope, sequencing, dependencies, or constraints changed mid-stream
- you need to salvage completed work instead of planning from scratch
- blocked or failed tasks require a revised path forward

Do not use this skill when:
- requirements are approved but no plan exists yet
- the user wants a first-pass implementation plan from scratch
- the work is only brainstorming and not ready for execution planning
- the change is trivial enough to update directly without a formal replanning pass

Use `create-plan` instead when the task is initial planning from approved requirements.

## Trigger Boundary vs `create-plan`

Choose `replanning-changes` if the user mentions:
- existing plan
- already started
- update the remaining plan
- revise the plan
- re-sequence work
- new constraint
- changed requirement
- failed assumption
- blocked task
- preserve completed work

Choose `create-plan` if the user mentions:
- approved requirements
- create a plan
- implementation plan for new work
- handoff plan
- phased plan before coding starts

## Primary Directive

Produce a change-aware plan update that:
- preserves valid prior work
- identifies exactly what changed
- records why the change was made
- updates only the affected tasks, phases, assumptions, risks, and validation

Never silently replace the original plan with a clean rewrite that hides the delta.

## Replanning Workflow

### 1. Establish the Baseline

Capture:
- the original objective
- the current plan or task list
- what is already completed, in progress, blocked, or not started

If this baseline is missing, ask for it before replanning.

### 2. Identify the Change

Classify the change precisely:
- requirement change
- scope expansion or reduction
- technical discovery
- dependency shift
- validator failure
- scheduling or resource constraint

State which assumptions are no longer valid.

### 3. Compute Impact

For each changed input, determine:
- which phases or tasks are unaffected
- which tasks are superseded
- which tasks need edits
- which new tasks must be added
- which validations must change
- whether rollback or migration steps need revision

### 4. Produce the Revision

Return:
- a decision log
- an impact summary
- the updated phase plan
- explicit superseded, unchanged, and new work

## Required Output Structure

```md
# [Replan Title]

- Plan Name: `[purpose-scope-plan]`
- Replan Name: `[purpose-scope-replan]`
- Status: `replanned`

## 1. Change Summary
- What changed
- Why it changed
- What remains valid

## 2. Current Execution State
- Completed work
- In-progress work
- Blocked work
- Not-started work

## 3. Decision Log
- `DEC-001`: Decision made
  - Reason:
  - Consequence:

## 4. Impact Analysis
- `IMP-001`: Unaffected phases/tasks
- `IMP-002`: Superseded tasks
- `IMP-003`: Modified tasks
- `IMP-004`: New tasks
- `IMP-005`: Validation changes

## 5. Updated Assumptions and Open Questions
- `ASM-001`: ...
- `Q-001`: ... Recommended answer: ...

## 6. Revised Phase Plan

### Phase 1: [Name]
Goal: ...
Dependencies: ...

| Task ID | Status | Change Type | Description | Files / Paths | Validation |
|---|---|---|---|---|---|
| `TASK-001` | Keep | Unchanged | ... | `src/...` | `npm test ...` |
| `TASK-002` | Replace | Superseded | ... | `src/...` | `npm run lint` |
| `TASK-003` | Add | New | ... | `src/...` | `npm test ...` |

## 7. Risks, Mitigations, and Rollback
- `RISK-001`: ...
- `MIT-001`: ...
- `RBK-001`: ...

## 8. Execution Checklist
- [ ] Original plan deltas captured
- [ ] Superseded work marked clearly
- [ ] Revised tasks validated
- [ ] Ready to resume execution
```

## Quality Bar

The replan is incomplete if it:
- hides which tasks changed
- discards completed work without justification
- fails to mark superseded tasks
- omits the reason for the change
- updates tasks but not validation
- rewrites the whole plan when a targeted delta would be clearer

## Common Mistakes

| Mistake | Why it fails |
|---|---|
| Rewriting the plan from scratch | It loses decision history and obscures what changed |
| Treating replanning as initial planning | It ignores completed, blocked, and in-flight work |
| Merging old and new scope silently | It removes traceability |
| Keeping invalid assumptions | It causes repeated failure in later phases |

## Final Instruction

Return a Markdown replan that clearly separates unchanged work, superseded work, and new work, with a visible decision log and enough precision to resume execution immediately.
