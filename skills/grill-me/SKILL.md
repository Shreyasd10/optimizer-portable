---
name: grill-me
description: Use when the user wants their plan, design, or approach stress-tested through pointed questioning, deeper scrutiny, and decision-by-decision review before implementation.
---

# Grill Me

Stress-test a plan through direct, systematic questioning until the important decisions, assumptions, and trade-offs are exposed.

Ask questions one at a time. For each question, include your recommended answer so the user sees both the challenge and your default judgment.

If a question can be answered by checking the codebase, current files, or repository structure, inspect that context instead of asking the user to guess.

## When to Use

Use this when:

- the user says "grill me"
- the user wants a plan or design stress-tested
- the user wants hidden assumptions surfaced before implementation
- the user has a proposal but not yet a high-confidence decision tree

Do not use this for ordinary implementation work where the user is asking you to just make the change.

## Core Pattern

Move through the design tree branch by branch:

1. Identify the next unresolved decision
2. Ask one sharp question about it
3. Provide your recommended answer
4. Incorporate the user's response
5. Continue until the major risks and dependencies are resolved

Do not stop just because the user answered a few questions well. Keep going until there are no high-impact unresolved questions left.

## What to Probe

- Goals and success criteria
- Scope boundaries
- Constraints and non-goals
- UX and behavior choices
- Data and state assumptions
- Failure modes and edge cases
- Operational or maintenance risks
- Testing and validation expectations

## Rules

- Ask exactly one question per message
- Keep questions specific, not vague
- Prefer the highest-leverage unresolved question first
- Use repository context when available
- Do not jump into implementation during the grilling process
- Do not end early while any major assumption, branch, or dependency remains unclear
- Escalate from obvious questions to edge cases, failure modes, rollout concerns, and validation questions
- Stop only when the design is coherent enough to proceed confidently and no high-impact unanswered questions remain

## Red Flags

If you catch yourself thinking any of these, keep grilling:

- "This is probably good enough already"
- "The rest can be figured out during implementation"
- "I already asked a few solid questions"
- "The remaining uncertainties are probably minor"

Those are signs to find the next important unresolved branch.

## Example Style

Question: What should happen if the user closes the modal halfway through the flow and comes back later?

Recommended answer: Preserve in-progress state for the current session, but reset on explicit cancellation unless the feature has a clear draft-saving requirement.

## Exit Condition

Finish when:

- the main branches of the decision tree are resolved
- remaining questions are genuinely low impact
- the user has a shared understanding of the recommended path forward
- there are no high-impact unanswered questions left
