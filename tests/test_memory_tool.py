import tools.memory_tool as memory_tool

def test_write_memory_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.memory_tool.MEMORY_DIR",   tmp_path)
    monkeypatch.setattr("tools.memory_tool.MEMORY_INDEX", tmp_path / "MEMORY.md")
    result = memory_tool.write_memory("my-fact", "Content here.", "user")
    assert result == {"saved": "my-fact"}
    assert (tmp_path / "my-fact.md").exists()

def test_write_memory_updates_index(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.memory_tool.MEMORY_DIR",   tmp_path)
    monkeypatch.setattr("tools.memory_tool.MEMORY_INDEX", tmp_path / "MEMORY.md")
    memory_tool.write_memory("my-fact", "Content.", "feedback")
    index = (tmp_path / "MEMORY.md").read_text()
    assert "my-fact" in index

def test_write_memory_no_duplicate_index_entry(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.memory_tool.MEMORY_DIR",   tmp_path)
    monkeypatch.setattr("tools.memory_tool.MEMORY_INDEX", tmp_path / "MEMORY.md")
    memory_tool.write_memory("dup", "Content.", "user")
    memory_tool.write_memory("dup", "Updated.", "user")
    index = (tmp_path / "MEMORY.md").read_text()
    assert index.count("- [dup]") == 1

def test_read_memory_index(tmp_path, monkeypatch):
    index_file = tmp_path / "MEMORY.md"
    index_file.write_text("# Memory Index\n\n- [test](test.md)")
    monkeypatch.setattr("tools.memory_tool.MEMORY_INDEX", index_file)
    result = memory_tool.read_memory()
    assert "Memory Index" in result["content"]

def test_read_memory_specific(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.memory_tool.MEMORY_DIR", tmp_path)
    (tmp_path / "myfile.md").write_text("# My Memory\n\nSome content.")
    result = memory_tool.read_memory("myfile")
    assert "My Memory" in result["content"]

def test_read_memory_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.memory_tool.MEMORY_DIR", tmp_path)
    result = memory_tool.read_memory("nonexistent")
    assert "error" in result
