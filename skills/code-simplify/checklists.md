# code-simplify checklists

## Pre-refactor

- [ ] Identify all public interfaces in scope
- [ ] Confirm behavior invariants (outputs, errors, side effects, ordering)
- [ ] Confirm API-change policy (default: not allowed)
- [ ] Confirm performance constraints

## During refactor

- [ ] Make small, focused edits
- [ ] Prefer simplification over redesign
- [ ] Remove duplication where safe
- [ ] Keep naming intent-revealing and consistent
- [ ] Re-check invariants after each change

## Post-refactor

- [ ] Verify public APIs unchanged (unless explicitly approved)
- [ ] Run tests for touched areas
- [ ] Run lint/typecheck as applicable
- [ ] Document assumptions, risks, and caveats
- [ ] Summarize maintainability improvements
