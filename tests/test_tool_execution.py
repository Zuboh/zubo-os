from hooks import HookRegistry, HookEvent
from permissions import PermissionMode
import tool_execution
from tool_execution import execute_tool, ToolResult


def test_successful_dispatch_returns_result():
    hooks = HookRegistry()
    result = execute_tool("list_files", {}, hooks, PermissionMode.AUTO)
    assert isinstance(result, ToolResult)
    assert result.tool_name == "list_files"
    assert result.is_error is False
    assert "files" in result.output


def test_unknown_tool_is_error():
    hooks = HookRegistry()
    result = execute_tool("does_not_exist", {}, hooks, PermissionMode.AUTO)
    assert result.is_error is True
    assert "Unknown tool" in result.output["error"]


def test_blocked_by_permission_mode():
    hooks = HookRegistry()
    result = execute_tool("bash", {"command": "echo hi"}, hooks, PermissionMode.PLAN)
    assert result.is_error is True
    assert "blocked by permission mode" in result.output["error"]


def test_exception_in_tool_is_caught(monkeypatch):
    def boom(**kwargs):
        raise RuntimeError("kaboom")

    monkeypatch.setitem(tool_execution.TOOL_DISPATCH, "boom_tool", boom)
    hooks = HookRegistry()
    result = execute_tool("boom_tool", {}, hooks, PermissionMode.AUTO)
    assert result.is_error is True
    assert "kaboom" in result.output["error"]


def test_hooks_fire_pre_and_post_in_order():
    hooks = HookRegistry()
    events = []
    hooks.register(HookEvent.PRE_TOOL_USE, lambda ctx: events.append("pre"))
    hooks.register(HookEvent.POST_TOOL_USE, lambda ctx: events.append("post"))

    execute_tool("list_files", {}, hooks, PermissionMode.AUTO)

    assert events == ["pre", "post"]


def test_hooks_fire_even_when_blocked():
    hooks = HookRegistry()
    events = []
    hooks.register(HookEvent.PRE_TOOL_USE, lambda ctx: events.append("pre"))
    hooks.register(HookEvent.POST_TOOL_USE, lambda ctx: events.append("post"))

    execute_tool("bash", {"command": "x"}, hooks, PermissionMode.PLAN)

    assert events == ["pre", "post"]
