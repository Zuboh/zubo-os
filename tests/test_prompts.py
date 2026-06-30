from datetime import date
import prompts
from pathlib import Path


def test_base_prompt_contains_today():
    result = prompts.assemble()
    assert date.today().isoformat() in result


def test_no_active_skills_has_no_skill_section():
    result = prompts.assemble()
    assert "Active Skill" not in result


def test_active_skill_injected(tmp_path, monkeypatch):
    monkeypatch.setattr("prompts.SKILLS_DIR", tmp_path)
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# My Skill\nDo the thing.")
    result = prompts.assemble(active_skills=["my-skill"])
    assert "Do the thing." in result
    assert "my-skill" in result


def test_missing_skill_ignored(tmp_path, monkeypatch):
    monkeypatch.setattr("prompts.SKILLS_DIR", tmp_path)
    result = prompts.assemble(active_skills=["nonexistent"])
    assert "nonexistent" not in result


def test_memory_injected_when_exists(tmp_path, monkeypatch):
    memory_file = tmp_path / "MEMORY.md"
    memory_file.write_text("- [test](test.md) — a test memory")
    monkeypatch.setattr("prompts.MEMORY_INDEX", memory_file)
    result = prompts.assemble()
    assert "a test memory" in result


def test_memory_absent_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr("prompts.MEMORY_INDEX", tmp_path / "MEMORY.md")
    result = prompts.assemble()
    assert "Persistent Memory" not in result
