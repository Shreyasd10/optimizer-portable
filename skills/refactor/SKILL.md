---
name: refactor
description: Use when code is tangled, duplicated, oversized, or hard to change safely, especially in Java or Spring Boot codebases where behavior must be preserved while improving structure, testability, and consistency with existing repository patterns.
---

# Refactor

## Overview

Refactor code in small, behavior-preserving slices. Start by adapting to the current repository's architecture and conventions, then choose the smallest safe change that improves clarity, cohesion, and testability.

## When to Use

- Refactoring tangled or hard-to-maintain code
- Reducing duplication, oversized classes/methods, or unclear responsibilities
- Improving testability, naming, and design consistency
- Preparing existing modules for feature work without changing public behavior

## When Not to Use

- The user only wants a tiny direct fix
- The task is primarily a new feature, migration, or docs-only change
- Refactoring is frozen or prohibited
- The requested improvement would intentionally change public behavior, contracts, or persistence semantics without approval

## Inputs

- The user request
- The relevant files or modules
- Existing tests and validators
- Repository conventions already in use

If the user provides additional requirements: `$ARGUMENTS`

## Required Behavior

1. Inspect the local codebase first and infer the active stack, architecture, and naming conventions before proposing changes.
2. Prefer existing repository patterns over generic clean-code ideals when they conflict.
3. Choose the narrowest safe refactor that materially improves maintainability.
4. Preserve externally visible behavior unless the user explicitly approves behavior changes.
5. Keep diffs reviewable and incremental.
6. Add or update tests where needed to lock behavior before or during refactoring.
7. Run the repository's relevant validators before completion.

## Codebase Adaptation Rules

- Detect the language, framework, module layout, test stack, and validation commands from the current repository.
- Reuse existing libraries, annotations, helpers, and patterns already present in the codebase.
- Do not introduce new abstractions, patterns, or dependencies unless the codebase already uses them or the user asks for them.
- Prefer local consistency over textbook purity.
- If several valid refactors exist, choose the one with the smallest diff and clearest readability gain.

## Java and Spring Boot Focus

When the active codebase is Java or Spring Boot, prioritize:

- Breaking up oversized services, methods, and utility classes
- Preserving controller-service-repository boundaries already used by the repo
- Replacing field injection with constructor injection when consistent with the project
- Removing duplicated mapping, validation, orchestration, or query logic
- Keeping controllers thin and business logic in services
- Preventing entity/DTO leakage when the repo already distinguishes them
- Preserving `@Transactional` boundaries and exception-handling behavior
- Using repo-native tests such as JUnit 5, Mockito, MockMvc, `@WebMvcTest`, `@DataJpaTest`, or existing integration-test patterns

## Safety and Escalation

- Do not silently change API contracts, serialized payloads, database schemas, transaction scope, auth behavior, or feature-flag semantics.
- Stop and call out risk if the refactor touches billing, auth, security boundaries, shared contracts, or compliance-sensitive code.
- If detailed implementation heuristics are needed, open `resources/implementation-playbook.md`.

## Output

- Main refactoring risks and target areas
- Ordered refactor plan
- Behavior-preserving code changes
- Test and verification results

## Resource

- `resources/implementation-playbook.md`
