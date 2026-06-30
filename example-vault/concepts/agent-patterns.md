---
type: resource
created: 2026-06-29
tags: [ai, concepts, architecture]
---

# Agent Patterns

## The 98.4% rule

VILA-Lab analysis: only 1.6% of Claude Code is AI decision logic.
The 98.4% is deterministic infrastructure: tool execution, hook dispatch,
permission gates, context assembly, message accumulation.

## Hook pattern

Inject behavior at lifecycle events without modifying the core loop:
- PreToolUse: validate, log, block dangerous commands
- PostToolUse: cache results, audit trail, transform output
- UserInput: slash command detection, preprocessing
- Stop: cleanup, persist state to disk

## Context assembly

System prompt built at runtime = static base + active skills + memory index.
Skills loaded on demand via slash command, not at startup.
This is exactly how Claude Code assembles its context.
