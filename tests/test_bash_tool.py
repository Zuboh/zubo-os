from tools.bash_tool import bash


def test_bash_runs_command():
    result = bash("echo hello")
    assert result["stdout"].strip() == "hello"
    assert result["returncode"] == 0


def test_bash_captures_stderr():
    result = bash("ls /path_that_does_not_exist_xyz")
    assert result["returncode"] != 0


def test_bash_timeout():
    result = bash("sleep 10", timeout=1)
    assert "error" in result
    assert "timed out" in result["error"]


def test_bash_captures_both_streams():
    result = bash("echo out && echo err >&2")
    assert "out" in result["stdout"]
    assert "err" in result["stderr"]
