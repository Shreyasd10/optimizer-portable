---
name: create-plan
description: Use when requirements are approved and a Factory-ready implementation plan is needed before coding, execution, delegation, or review.
---

# Create Plan

## Overview

Create an evidence-backed implementation plan that another Droid, subagent, or human can execute with minimal extra context.

The plan should be concrete, scoped, low-ambiguity, and optimized for Factory workflows.

## When to Use

Use this skill when:
- requirements are already approved
- implementation should be broken into executable steps
- work may be delegated to subagents or another session
- file-level guidance, validation steps, and risks must be explicit
- the user asks for a plan, roadmap, execution strategy, or implementation breakdown

Do not use this skill for:
- open-ended brainstorming
- root-cause debugging before the fix is understood
- tiny single-file edits that do not need a formal plan
- direct implementation work

## Boundaries

This is a planning-only skill:
- research the codebase and existing patterns
- create strategic and execution-ready plans
- identify risks, assumptions, and alternatives
- describe implementation work in natural language
- do not implement the code changes
- do not write code snippets or patch examples in the plan

If the user wants implementation after approval, switch to execution.

## Plan Identity

Name the plan using this format:

`[purpose]-[scope]-plan`

Allowed purpose prefixes:
- `feature`
- `bugfix`
- `refactor`
- `migration`
- `infra`
- `architecture`
- `design`
- `process`

Examples:
- `feature-billing-portal-plan`
- `bugfix-session-timeout-plan`
- `refactor-search-indexer-plan`

If the plan should be stored as a file, use:

`plans/YYYY-MM-DD-[task-name]-vN.md`

Example:

`plans/2026-03-27-session-timeout-hardening-v1.md`

## Primary Directive

Produce an execution-ready Factory plan that is explicit, evidence-backed, easy to validate, and easy to hand off. Assume the next implementer should not have to infer missing decisions.

## Planning Process

### 1. Initial Assessment

Before writing the plan:
- inspect the project structure and relevant flows end to end
- read the important files closely enough to understand current behavior
- identify existing patterns, abstractions, and conventions
- determine likely risks, sequencing constraints, and validation commands
- note any requirements that are still ambiguous

### 2. Gather Evidence

Ground the plan in repository evidence whenever possible:
- cite important references using `filepath:line` format
- prefer repository-relative paths
- label unknowns as assumptions rather than facts

### 3. Shape the Plan

Translate approved requirements into discrete phases and atomic tasks:
- include exact files, modules, functions, commands, APIs, or tables whenever known
- state dependencies and sequencing explicitly
- prefer test-first ordering for behavior changes
- separate work that can be parallelized from work that must remain sequential

### 4. Validate the Plan

Before returning the plan:
- check that every requirement maps to one or more tasks
- check that every task has a validation method
- check that open questions are marked as blocking or non-blocking
- check that risks include mitigations and rollback notes
- if the repository has a plan validator, use it
- if no validator exists, run the self-review checklist in this skill and revise until it passes

## Core Rules

1. Start with a concise title and the generated plan name.
2. Include a file name when the plan is expected to be saved to disk.
3. Break work into phases and atomic tasks with explicit dependencies.
4. Include exact file paths, modules, functions, or commands whenever known.
5. Use repository evidence with `filepath:line` citations for important claims.
6. Use natural language describing what and why, not code or pseudo-code.
7. Include concrete verification steps for each phase.
8. Call out assumptions, unresolved choices, and rollback concerns.
9. Do not leave placeholders such as `TBD`, `TODO`, or “handle later”.
10. Do not mark speculative details as facts.

## Factory Adaptation

Plans should fit Factory workflows:
- optimize for execution by Droids or subagents
- include checkpoints suitable for `TodoWrite`
- describe where `AskUser` is required before implementation continues
- identify work that can be parallelized vs. work that must stay sequential
- prefer repository-relative file paths
- include concrete validator commands when discoverable
- identify where verification-before-completion should happen

## Required Output Structure

Use this exact section structure in the final plan.

```md
# [Plan Title]

- Plan Name: `[purpose-scope-plan]`
- Plan File: `plans/YYYY-MM-DD-[task-name]-vN.md` | `not required`
- Status: `planned`
- Owner: `[optional]`

## 1. Objective
- Short statement of the intended outcome

## 2. Scope
- In scope
- Out of scope

## 3. Requirements and Constraints
- `REQ-001`: ...
- `CON-001`: ...
- `SEC-001`: ...
- `PAT-001`: ...

## 4. Evidence
- `EVID-001`: `path/to/file:line-line` — why this matters

## 5. Assumptions and Open Questions
- `ASM-001`: ...
- `Q-001`: ... Recommended answer: ... Blocking: `Yes|No`

## 6. Phase Plan

### Phase 1: [Name]
Goal: ...
Dependencies: none | `[Phase/Task IDs]`

| Task ID | Description | Requirements | Files / Paths | Validation | Parallel? |
|---|---|---|---|---|---|
| `TASK-001` | ... | `REQ-001` | `src/...` | `npm test ...` | No |

### Phase 2: [Name]
Goal: ...
Dependencies: `TASK-001`

| Task ID | Description | Requirements | Files / Paths | Validation | Parallel? |
|---|---|---|---|---|---|
| `TASK-002` | ... | `REQ-002` | `src/...` | `npm run lint` | Yes |

## 7. Validation Strategy
- Unit / integration / lint / typecheck / build expectations
- Exact command set when known
- What must pass before implementation is considered complete

## 8. Risks and Rollback
- `RISK-001`: ...
- `MIT-001`: ...
- `RBK-001`: ...

## 9. Alternatives Considered
- `ALT-001`: ...

## 10. Execution Checklist
- [ ] Evidence reviewed
- [ ] Requirements mapped to tasks
- [ ] Blocking questions resolved or surfaced
- [ ] Validators identified
- [ ] Ready for implementation
```

## Task Authoring Rules

- Keep tasks small enough that progress is obvious.
- Each task must describe a concrete action, not a vague intention.
- Include what changes, why it changes, and where it changes.
- If a task changes behavior, include the test or validation that proves it.
- Mark tasks as parallel only when they do not edit the same files and do not depend on the same unfinished behavior.
- Every requirement must map to at least one task.
- Do not rely on generic tasks like “implement feature” or “fix bug”.

## Quality Bar

Reject the plan and revise it if any of these are true:
- task wording requires interpretation
- key files are omitted when they are knowable
- evidence is missing for major claims
- validation is missing or generic without justification
- requirements are not traceable to implementation steps
- risks are hand-waved
- sequencing is unclear
- blocking questions are buried
- the plan contains code blocks, code snippets, or pseudo-code

## Self-Review Checklist

Before returning the plan, confirm:
- the plan is grounded in actual repository context
- file references use repository-relative paths where possible
- important claims cite `filepath:line`
- validation commands are exact when discoverable
- assumptions are clearly labeled
- alternatives include trade-offs
- rollback concerns are practical, not ceremonial

## Factory-Specific Guidance

When useful, explicitly include:
- what should be tracked as `TodoWrite` items
- where `AskUser` is needed for product or technical decisions
- where subagents can help
- where work can be parallelized safely
- where verification-before-completion should happen

## Final Instruction

Return the plan in Markdown with a strong title, the generated plan name near the top, enough precision to start implementation immediately, and no code snippets inside the plan.
