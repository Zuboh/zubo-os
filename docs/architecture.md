# Zubo OS — Architecture

## The loop

```
User input
    │
    ▼
UserInput hook  ← slash command detection, preprocessing
    │
    ▼
Claude API (sync)  ← system prompt = base + skills + memory
    │
    ├─ stop_reason: end_turn  →  print response
    │
    └─ stop_reason: tool_use
            │
            ▼
        PreToolUse hook  ← validate, log
            │
            ▼
        Permission gate  ← default / auto / plan
            │
            ▼
        Tool execution   ← dispatch dict → Python fn
            │
            ▼
        PostToolUse hook ← audit, cache
            │
            ▼
        Append tool_result to messages
            │
            └──────────────────────────────► loop
```

## Layer breakdown

### 1. Context assembly (`prompts.py`)

System prompt built at runtime from three sources:
- **Base prompt**: role, date, capabilities
- **Active skills**: SKILL.md files loaded on `/skill-name` slash command
- **Memory index**: MEMORY.md injected if present

This mirrors how Claude Code assembles its context window before each API call.

### 2. Hook system (`hooks.py`)

Four lifecycle events: `PreToolUse`, `PostToolUse`, `UserInput`, `Stop`.

Hooks registered as callables on a `HookRegistry`. Each hook receives a
`HookContext` (event + mutable data dict) and returns it (or None to pass through).

Hooks decouple cross-cutting concerns (logging, validation, slash commands)
from the core loop without modifying `agent.py`.

### 3. Permission model (`permissions.py`)

Three modes, selectable at startup:

| Mode    | Behavior |
|---------|----------|
| default | Ask for confirmation on guarded tools (bash, write_file) |
| auto    | Allow all tools without prompting |
| plan    | Block all tool execution (analysis only) |

`gate(tool_name, mode)` called in PreToolUse phase. Returns bool.

### 4. Tool dispatch (`tools/`)

Each tool module exports:
- `TOOL_SCHEMAS`: list of Anthropic-format tool dicts
- Python functions matching schema parameter names

`tools/__init__.py` merges all schemas and builds `TOOL_DISPATCH: dict[str, Callable]`.

`fn(**tool_input)` — Claude's `input` dict unpacked directly into the function.

### 5. Memory system (`tools/memory_tool.py`)

Markdown files in `memory/`. `MEMORY.md` is the index (injected into system prompt).
Each memory file has frontmatter (`name`, `type`) + content body.

Write path: `write_memory` → creates `.md` file, appends entry to index.
Read path: `read_memory` → returns index or specific file content.

## Zubo OS vs Claude Code

> "Only 1.6% of Claude Code is AI decision logic. The other 98.4% is
> deterministic infrastructure." — VILA-Lab analysis

Zubo OS implements the same 98.4%:

| Concern | Claude Code | Zubo OS |
|---------|-------------|---------|
| Tool dispatch | Internal registry | `TOOL_DISPATCH` dict |
| Hooks | 16+ hook types | 4 events, same pattern |
| Permission model | 3 modes (default/auto/plan) | Identical |
| Context assembly | CLAUDE.md + memory + skills | `prompts.assemble()` |
| Memory | File-based MEMORY.md | Identical format |
| Skill activation | `/skill-name` slash command | Identical |

The difference: Claude Code's infrastructure is production-hardened (streaming,
worktrees, MCP servers, concurrent tool calls). Zubo OS is the same conceptual
skeleton in ~300 lines of readable Python.
