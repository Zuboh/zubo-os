import subprocess


TOOL_SCHEMAS = [
    {
        "name": "bash",
        "description": "Execute a shell command. Requires permission confirmation in default mode.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to execute"}
            },
            "required": ["command"],
        },
    }
]


def bash(command: str, timeout: int = 30) -> dict:
    """Execute a shell command with timeout and capture output.

    Args:
        command: Shell command to execute
        timeout: Timeout in seconds (default 30)

    Returns:
        dict with 'stdout', 'stderr', 'returncode' on success,
        or 'error' key on timeout/exception
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {timeout}s"}
    except Exception as e:
        return {"error": str(e)}
