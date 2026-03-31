---
name: code-review
description: Use when reviewing staged, uncommitted, branch, range, or pasted diffs and a Factory Droid should produce high-signal, actionable findings with security, correctness, performance, reliability, and maintainability coverage.
---

# Code Review

## Overview
Run a structured Factory Droid code review using layered analysis, confidence-gated findings, and actionable triage.

## When to Use
- Reviewing staged, uncommitted, branch, commit-range, or pasted diffs
- Checking risky changes touching auth, payments, persistence, network boundaries, or concurrency
- Wanting stronger review signal than a flat checklist
- Wanting balanced review coverage across correctness, reliability, performance, maintainability, and broad security regressions

Do not use this skill when there is no review target or the user wants implementation rather than review.
Use `security-review` instead when the task is primarily a dedicated security assessment, security triage, or Spring Security review.

## Core Principle
Review like an adversarial Factory Droid: gather the right diff, run independent layers, open surrounding context, then report only high-confidence, concrete findings.

## Inputs
- `content` — Review target details (staged, uncommitted, branch diff, commit range, or provided diff/file list).
- `also_consider` (optional) — Spec/story paths, acceptance criteria, risk focus (security/performance/reliability), or constraints.

## Execution
### Step 1: Gather Context
1. Detect review intent from user request:
   - staged changes
   - uncommitted changes
   - branch diff vs base
   - commit range
   - pasted/provided diff
2. If intent is unclear, ask user what to review and HALT.
3. Build a non-empty diff payload and validate it is reviewable.
4. Ask for optional spec/story context file path. If provided, include it in review context.
5. For large diffs, group review by feature/module area rather than raw file order.
6. Identify critical paths early:
   - authn/authz
   - payments or other irreversible writes
   - network or external API boundaries
   - migrations and persistence changes
   - concurrency/shared-state paths
7. Present checkpoint summary: files changed, add/remove counts, and whether spec context is loaded.

### Step 2: Run Parallel Review Layers
1. Run blind adversarial review on diff only by invoking `adversarial-review`.
2. Run branch/boundary review by invoking `edge-case-hunter`.
3. If spec/story context exists, run acceptance audit against the diff and spec constraints.
4. Add focused checks across:
   - Security: broad regression triage for auth bypass, injection, secrets exposure, and insecure defaults
   - Correctness: branch logic, validation, error paths, state transitions
   - Performance: N+1 patterns, redundant I/O/network, expensive loops
   - Reliability: retries/timeouts, idempotency, concurrency, observability gaps
   - Maintainability: SOLID violations, removal candidates, shotgun surgery, data clumps, overly broad abstractions
5. Collect findings from all completed layers. If a layer fails, continue and report degraded coverage.
6. Open full-file context for suspicious hunks before finalizing findings.
7. If the review becomes primarily security-driven or requires deeper trust-boundary analysis, switch to or invoke `security-review`.

### Step 2A: Coverage Checklist
Use these prompts to improve coverage without downgrading signal quality.

#### Security and Reliability
- Broad security regressions in changed code: auth bypass, ownership gaps, secrets exposure, unsafe interpolation, insecure defaults
- Missing retries, timeouts, or resource bounds
- Race conditions:
  - check-then-act / TOCTOU
  - read-modify-write without atomicity
  - concurrent shared state access
  - missing transaction or locking strategy

For deep security review, Spring Security analysis, or attack-path tracing, use `security-review`.

#### Correctness and Boundary Conditions
- Null/undefined handling, empty collections, whitespace-only strings
- Division by zero, overflow, negative values, off-by-one, pagination bounds
- Async error handling, swallowed exceptions, overly broad catches
- State transition gaps, invalid defaults, partial writes, missing idempotency

#### Performance
- N+1 queries or one-by-one remote calls
- Over-fetching, missing pagination, expensive loops on hot paths
- Missing cache where warranted, broken cache invalidation, unsafe global caching
- Unbounded memory growth or large in-memory buffers

#### Maintainability and Design
- SRP/OCP/LSP/ISP/DIP violations with practical impact
- Long methods, feature envy, primitive obsession, divergent change, dead code
- Removal candidates: distinguish safe delete now vs defer with migration/telemetry plan
- Prefer incremental refactors over large rewrites

For every maintainability finding, explain why it matters now; do not emit style-only observations.

### Step 3: Normalize and Triage
1. Normalize all findings into:
   - `id`
   - `source`
   - `title`
   - `detail`
   - `location`
2. Deduplicate overlapping findings and merge evidence.
3. Classify each finding into one bucket:
   - `decision_needed`
   - `patch`
   - `defer`
   - `dismiss`
4. Assign severity and confidence:
   - `critical` (95%+ confidence): security/data-loss/crash-level risk
   - `warning` (85%+ confidence): logic bugs, edge-case failures, meaningful perf regressions
   - `suggestion` (75%+ confidence): maintainability improvements with practical value
   - below 75%: do not report as issue; gather context first
5. Drop `dismiss` items from actionable output, but report dismiss count.
6. When multiple findings overlap, merge them under the strongest evidence-backed issue.

### Step 4: Present and Act
1. Present summary counts by bucket and by source layer.
2. List `decision_needed` first, then `patch`, then `defer`.
3. Render findings in this structure:
   - Summary (2-3 sentences)
   - Issues table: severity, file:line, issue
   - Detailed findings: confidence, problem, concrete fix
   - Recommendation: `APPROVE` | `APPROVE WITH SUGGESTIONS` | `NEEDS CHANGES`
4. Ask user how to proceed:
   - auto-fix patchable items
   - keep as action items
   - walk through one by one
5. If user chooses fixes, apply minimal safe diffs and re-run focused validation.

## Output Format
```markdown
## Code Review Summary

**Files reviewed**: X files, Y lines changed
**Overall assessment**: APPROVE | APPROVE WITH SUGGESTIONS | NEEDS CHANGES

## Issues
| Severity | Location | Issue |
| --- | --- | --- |
| warning | `path/file.ts:42` | Missing tenant check on update path |

## Detailed Findings
### 1. Missing tenant isolation on update
- **Confidence**: 97%
- **Source**: adversarial-review, edge-case-hunter
- **Problem**: ...
- **Concrete fix**: ...

## Recommendation
NEEDS CHANGES
```

If there are no actionable findings, state what was reviewed, what was checked, any uncovered areas, and residual risk.

## Review Rules
- Do not flag pure style nits unless they impact correctness or maintainability materially.
- Do not report low-confidence hypotheses as hard issues.
- Open full-file context for suspicious hunks; do not rely on patch lines only.
- Prefer concrete fix paths over generic advice.
- Default to review-only. Do not implement fixes unless the user asks.

## Halt Conditions
- HALT if diff/content is empty or unreadable.
- HALT if review scope is ambiguous and user has not selected a target.
- HALT if no actionable findings remain and report clean review outcome.
