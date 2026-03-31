---
name: search-first
description: Research-first workflow for codebase exploration, pattern discovery, and evidence-backed analysis before coding or investigating existing systems.
---

# Search First

## Overview

Research-first workflow that checks existing patterns, tools, and implementations before building new code. Use when understanding how systems work, finding existing patterns before coding, or investigating bugs, architecture, and dependencies.

## When to Use

- New features likely have existing patterns to follow
- Dependency or tooling choices need validation
- Avoiding duplicate abstractions in the codebase
- Understanding how systems work, why decisions were made
- Investigating bugs, architecture, or complex behavior patterns
- Tracing functionality and data flow across components

## When Not to Use

- Implementation is explicitly requested
- The user only wants a direct answer without analysis
- This is a brainstorming or design session (use brainstorming skill)

## Core Principles

1. **Evidence over assumptions** — Support every conclusion with specific file references and line numbers
2. **Compression first** — Keep findings high-signal; summarize aggressively, avoid flooding context
3. **Scope clarity** — If the research question is unclear, ask before diving in
4. **Read-only** — Never modify files or systems; purely investigative

## Inputs

- `content` — The target material to process (code, diff, spec, logs, task, or question)
- `also_consider` — optional constraints, priorities, or risks to account for

## Execution

### Step 1: Receive Scope
1. Load the provided content and identify artifact type and boundaries
2. If scope is unclear, request clarification before proceeding

### Step 2: Investigate Systematically

#### Investigation Sequence
1. **Scope Understanding** — What specifically needs to be understood or found
2. **High-Level Analysis** — Project structure, architecture patterns, dependencies
3. **Targeted Investigation** — Drill into specific files, components, or patterns
4. **Cross-Reference** — Trace relationships and dependencies across modules
5. **Pattern Recognition** — Identify recurring design decisions
6. **Insight Synthesis** — Explain why things are designed the way they are

#### Pre-Coding Research
1. Search local codebase for existing implementation patterns
2. Search known/internal patterns and approved dependencies
3. Compare adopt vs extend vs build-custom
4. Proceed with smallest safe approach

#### General Investigation
1. Map the relevant project structure and key files
2. Trace functionality and data flow across components
3. Identify design patterns, architectural decisions, and trade-offs
4. Examine error handling, edge cases, and test coverage
5. Synthesize findings with clear file citations

### Step 3: Present Output

```markdown
### Summary
Brief overview of what was investigated (≤5 bullets)

### Key Findings
- [finding] — `filepath:line` or `filepath:startLine-endLine`
- [finding] — `filepath:line`

### Recommendations
Next action or decision to make
```

For complex findings, include:
- **Technical Details** — Implementation details and code patterns
- **Insights and Context** — Why things were designed this way
- **Follow-up Suggestions** — Areas for deeper investigation

## Output Format

```markdown
### Summary
Brief overview of what was investigated

### Key Findings
Most important discoveries with specific file references

### Technical Details
Implementation details and code patterns supporting the findings

### Insights and Context
Why things were designed this way — trade-offs, constraints, relationships

### Follow-up Suggestions
Areas for deeper investigation or related components
```

## File Reference Format

Always cite code as: `filepath:startLine-endLine` for ranges, `filepath:startLine` for single lines.

## Halt Conditions

- HALT if content is empty, unreadable, or missing required context
- HALT if required evidence cannot be obtained from provided material
- HALT if output would be speculative without explicit assumptions stated
