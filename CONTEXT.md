# Zubo OS

A personal CLI agent that mirrors Claude Code's internals — hook system, permission model, tool dispatch, context assembly — in ~300 lines of Python.

## Language

**Tool execution**:
One PRE_TOOL_USE hook → permission gate → dispatch → error classification → POST_TOOL_USE hook cycle for a single tool call, from the moment the model requests a tool to the moment its result is appended to the conversation. Lives in `tool_execution.py`.
_Avoid_: tool turn, tool call handling.

**Tool-result collapsing**:
Replacing a `tool_result` block's `content` with a fixed placeholder once it has survived 3 user turns in `messages`, so large tool output (file reads, command output) isn't rebilled at full price on every subsequent turn. Only `tool_result` blocks are collapsed — chat text is left untouched. Lives in `history.py`.
_Avoid_: history trimming, context pruning (too broad — this only targets tool output, not the whole message list).
