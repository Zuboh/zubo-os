from dataclasses import dataclass, field
from typing import Callable, Any
from enum import Enum

class HookEvent(Enum):
    PRE_TOOL_USE  = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    USER_INPUT    = "UserInput"
    STOP          = "Stop"

@dataclass
class HookContext:
    event: HookEvent
    data: dict[str, Any] = field(default_factory=dict)

HookFn = Callable[[HookContext], "HookContext | None"]

class HookRegistry:
    def __init__(self):
        self._hooks: dict[HookEvent, list[HookFn]] = {e: [] for e in HookEvent}

    def register(self, event: HookEvent, fn: HookFn) -> None:
        self._hooks[event].append(fn)

    def run(self, event: HookEvent, data: dict[str, Any] = None) -> HookContext:
        ctx = HookContext(event=event, data=data or {})
        for fn in self._hooks[event]:
            result = fn(ctx)
            if result is not None:
                ctx = result
        return ctx
