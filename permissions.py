from enum import Enum

class PermissionMode(Enum):
    DEFAULT = "default"
    AUTO    = "auto"
    PLAN    = "plan"

GUARDED_TOOLS = {"bash", "write_file"}

def gate(tool_name: str, mode: PermissionMode) -> bool:
    if mode == PermissionMode.PLAN:
        return False
    if mode == PermissionMode.AUTO:
        return True
    if tool_name in GUARDED_TOOLS:
        answer = input(f"[PERMISSION] {tool_name} — allow? [y/N] ").strip().lower()
        return answer == "y"
    return True
