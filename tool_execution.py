from dataclasses import dataclass

from hooks import HookRegistry, HookEvent
from permissions import PermissionMode, gate
from tools import TOOL_DISPATCH


@dataclass
class ToolResult:
    tool_name: str
    output: dict
    is_error: bool


def execute_tool(
    tool_name: str,
    tool_input: dict,
    hooks: HookRegistry,
    mode: PermissionMode,
) -> ToolResult:
    hooks.run(HookEvent.PRE_TOOL_USE, {"tool": tool_name, "input": tool_input})

    if not gate(tool_name, mode):
        result = {"error": f"'{tool_name}' blocked by permission mode '{mode.value}'."}
        is_error = True
    else:
        fn = TOOL_DISPATCH.get(tool_name)
        if fn is None:
            result = {"error": f"Unknown tool: {tool_name}"}
            is_error = True
        else:
            try:
                result = fn(**tool_input)
                is_error = "error" in result
            except Exception as exc:
                result = {"error": str(exc)}
                is_error = True

    hooks.run(HookEvent.POST_TOOL_USE, {"tool": tool_name, "result": result})
    return ToolResult(tool_name, result, is_error)
