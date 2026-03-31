# Visual Companion Guide

Browser-based visual brainstorming companion for mockups, diagrams, and visual comparisons in Factory workflows.

## When to Use

Decide per question, not per session. Use it when the user would understand the next step better by seeing it than by reading it.

**Use the browser for:**

- UI mockups and layout options
- Architecture or flow diagrams
- Side-by-side visual comparisons
- Look-and-feel discussions
- Spatial relationships and navigation flows

**Use the terminal for:**

- Requirements and scope questions
- Conceptual approach choices
- Trade-off discussions
- Technical design decisions
- Clarifying questions that are primarily verbal

A question about UI is not automatically visual. If words are enough, stay in the terminal.

## How It Works

The visual companion serves HTML content from a watched directory and records browser interactions for later turns.

- Write a new HTML screen for each visual step
- Share the URL with the user
- Read recorded events on the next turn
- Iterate until the visual question is resolved

## Factory Adaptation Notes

- Prefer the browser-navigation or agent-browser skill when browser interaction is needed in Factory
- Use a project-local temporary area only if the task truly needs persistent visual artifacts
- Do not assume a fixed `.superpowers/brainstorm/` path in Factory projects
- Do not require this companion for ordinary brainstorming; it is optional support

## Interaction Loop

1. Confirm the current visual question actually benefits from a browser view
2. Generate a new visual artifact for that question
3. Tell the user what they are looking at and what feedback you want
4. Combine terminal feedback with any browser interaction signals
5. Either revise the current visual or move back to terminal-first discussion

## Minimal Guidance for Screens

- Use one fresh screen per step
- Keep the choices obvious and labeled
- Prefer simple HTML fragments or lightweight pages
- Clear stale visuals when moving back to text-only discussion
