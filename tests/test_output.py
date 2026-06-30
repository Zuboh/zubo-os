from output import tool_line, error_line, response_line, info_line

def test_tool_line_contains_name_and_params():
    line = tool_line("read_file", path="foo.md")
    assert "read_file" in line
    assert "path=foo.md" in line

def test_error_line_contains_message():
    line = error_line("File not found")
    assert "File not found" in line

def test_response_line_contains_text():
    line = response_line("Hello world")
    assert "Hello world" in line

def test_info_line_contains_message():
    line = info_line("Starting up")
    assert "Starting up" in line
