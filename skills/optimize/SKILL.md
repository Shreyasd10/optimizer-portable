---
name: optimize
description: Harvest your best traces and patterns from recent sessions. Run this after successful sessions to extract reusable workflows, effective tool chains, and patterns for future sessions. Analyzes session logs and stores learnings.
---

# Optimize - Harvest Your Best Traces

Extract and store patterns from recent successful sessions.

## When to Use

- After completing a complex task successfully
- When you discovered an effective approach or workflow
- Before starting similar tasks to recall what worked before
- Periodically to build your personal pattern library

## What It Does

1. **Scans recent session logs** for successful tool chains and workflows
2. **Extracts patterns** - effective prompts, tool sequences, approaches
3. **Stores learnings** via the local optimizer or ruflo bridge
4. **Updates recommendations** for future similar tasks

## How to Run

```
/optimize
```

The skill will:
- Find recent successful sessions
- Identify reusable patterns
- Store them in your optimizer memory
- Report what was learned

## Pattern Categories

Stored patterns include:
- **Tool chains** - sequences of tools that worked well
- **Prompt patterns** - effective prompt structures
- **Workflow approaches** - how you tackled certain task types
- **Session strategies** - planning, validation, iteration approaches

## Integration

Uses your existing optimizer setup at `~/.factory/optimizer/`:
- Local JSON storage when ruflo is disabled
- Vector memory when ruflo is available

## Example

```
/optimize
```

Output might be:
```
Harvested 3 patterns:
- React component creation workflow
- API error handling pattern  
- Test-driven debugging approach
```

## Notes

- Only stores patterns from sessions you mark as successful
- Respects your `.ruflo_disabled` preference
- Backs up to local JSON even when ruflo is unavailable
