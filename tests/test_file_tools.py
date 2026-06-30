import pytest
import tools.file_tools as file_tools


def test_read_file_success(monkeypatch, fake_vault):
    monkeypatch.setattr("tools.file_tools.VAULT_PATH", fake_vault)
    result = file_tools.read_file("daily/2026-07-01.md")
    assert "content" in result
    assert "Python agents" in result["content"]


def test_read_file_not_found(monkeypatch, fake_vault):
    monkeypatch.setattr("tools.file_tools.VAULT_PATH", fake_vault)
    result = file_tools.read_file("nonexistent.md")
    assert "error" in result
    assert "nonexistent.md" in result["error"]


def test_search_vault_hit(monkeypatch, fake_vault):
    monkeypatch.setattr("tools.file_tools.VAULT_PATH", fake_vault)
    result = file_tools.search_vault("Python agents")
    assert len(result["matches"]) > 0
    assert any("python-agents.md" in m["file"] for m in result["matches"])


def test_search_vault_miss(monkeypatch, fake_vault):
    monkeypatch.setattr("tools.file_tools.VAULT_PATH", fake_vault)
    result = file_tools.search_vault("unicorn_xyz_nothere")
    assert result["matches"] == []


def test_list_files(monkeypatch, fake_vault):
    monkeypatch.setattr("tools.file_tools.VAULT_PATH", fake_vault)
    result = file_tools.list_files()
    assert "files" in result
    assert len(result["files"]) == 2
    assert all(f.endswith(".md") for f in result["files"])


def test_write_file_creates_file(monkeypatch, fake_vault):
    monkeypatch.setattr("tools.file_tools.VAULT_PATH", fake_vault)
    result = file_tools.write_file("new/note.md", "# New Note\n\nContent here.")
    assert result == {"written": "new/note.md"}
    assert (fake_vault / "new" / "note.md").read_text() == "# New Note\n\nContent here."


def test_write_file_overwrites(monkeypatch, fake_vault):
    monkeypatch.setattr("tools.file_tools.VAULT_PATH", fake_vault)
    file_tools.write_file("daily/2026-07-01.md", "new content")
    result = file_tools.read_file("daily/2026-07-01.md")
    assert result["content"] == "new content"
