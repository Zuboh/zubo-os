# Zubo OS

A personal CLI agent that mirrors Claude Code's internals — hook system, permission model, tool dispatch, context assembly — in ~300 lines of Python.

## Language

**Tool execution**:
One dispatch → hook sequencing → error classification cycle for a single tool call, from the moment the model requests a tool to the moment its result is appended to the conversation. Lives in `tool_execution.py`.
_Avoid_: tool turn, tool call handling.
