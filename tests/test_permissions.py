from permissions import PermissionMode, gate

def test_auto_allows_all():
    assert gate("bash", PermissionMode.AUTO) is True
    assert gate("write_file", PermissionMode.AUTO) is True
    assert gate("read_file", PermissionMode.AUTO) is True

def test_plan_blocks_all():
    assert gate("bash", PermissionMode.PLAN) is False
    assert gate("read_file", PermissionMode.PLAN) is False

def test_default_allows_safe_tools():
    assert gate("read_file", PermissionMode.DEFAULT) is True
    assert gate("search_vault", PermissionMode.DEFAULT) is True
    assert gate("list_files", PermissionMode.DEFAULT) is True
    assert gate("read_memory", PermissionMode.DEFAULT) is True

def test_default_prompts_bash_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert gate("bash", PermissionMode.DEFAULT) is True

def test_default_prompts_bash_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert gate("bash", PermissionMode.DEFAULT) is False

def test_default_prompts_write_file_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert gate("write_file", PermissionMode.DEFAULT) is True
