---
name: inbox
description: Check for pending workflow improvements, suggested skills, and optimization recommendations. Run this to see what could be improved based on your recent sessions and patterns.
---

# Inbox - Pending Improvements & Suggestions

Get actionable recommendations based on your recent session history and stored patterns.

## When to Use

- At the start of a session to get context
- When stuck or not making progress
- After completing a task to see what could be better
- To review recent learnings and suggestions

## What It Shows

1. **Pending recommendations** - workflow improvements suggested by past analysis
2. **Recent patterns** - learnings from recent sessions
3. **Suggested skills** - which skills might help for current task types
4. **Outstanding todos** - optimization items waiting to be addressed

## How to Run

```
/inbox
```

The skill will:
- Check recent session history
- Load stored patterns and recommendations
- Present actionable suggestions
- Show what skills may help

## Output Format

```
## Inbox

### Recommendations (3)
1. **Consider /brainstorming for complex features** - suggested from session abc123
2. **Use /tdd-driver for refactors** - pattern stored from recent work
3. **Review /code-review for PRs** - skill suggested based on workflow

### Recent Patterns
- Authentication flow pattern (stored 2 days ago)
- React state management approach (stored 1 week ago)

### Suggested for Current Task
Based on recent context, consider: /brainstorming, /code-review

## Empty Inbox

If nothing is pending, you'll see:
```
Inbox is empty. Run /optimize after successful sessions to build patterns.
```
