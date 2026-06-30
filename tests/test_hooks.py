from hooks import HookRegistry, HookEvent, HookContext

def test_register_and_run_fires_hook():
    registry = HookRegistry()
    calls = []

    def my_hook(ctx: HookContext):
        calls.append(ctx.event)
        return ctx

    registry.register(HookEvent.PRE_TOOL_USE, my_hook)
    registry.run(HookEvent.PRE_TOOL_USE, {"tool": "bash"})
    assert len(calls) == 1
    assert calls[0] == HookEvent.PRE_TOOL_USE

def test_hook_can_modify_context():
    registry = HookRegistry()

    def modify(ctx: HookContext):
        ctx.data["modified"] = True
        return ctx

    registry.register(HookEvent.USER_INPUT, modify)
    result = registry.run(HookEvent.USER_INPUT, {"input": "hello"})
    assert result.data["modified"] is True

def test_no_hooks_runs_cleanly():
    registry = HookRegistry()
    ctx = registry.run(HookEvent.STOP)
    assert ctx.event == HookEvent.STOP

def test_multiple_hooks_chain_in_order():
    registry = HookRegistry()
    order = []

    registry.register(HookEvent.POST_TOOL_USE, lambda ctx: (order.append(1), ctx)[1])
    registry.register(HookEvent.POST_TOOL_USE, lambda ctx: (order.append(2), ctx)[1])
    registry.run(HookEvent.POST_TOOL_USE)
    assert order == [1, 2]

def test_hook_returning_none_does_not_replace_context():
    registry = HookRegistry()

    registry.register(HookEvent.PRE_TOOL_USE, lambda ctx: None)
    result = registry.run(HookEvent.PRE_TOOL_USE, {"tool": "bash"})
    assert result.data["tool"] == "bash"
