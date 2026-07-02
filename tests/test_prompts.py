from datetime import date
import prompts
from pathlib import Path


def assembled_text(active_skills=None):
    blocks = prompts.assemble_blocks(active_skills)
    return "\n".join(b["text"] for b in blocks)


def test_base_prompt_contains_today():
    result = assembled_text()
    assert date.today().isoformat() in result


def test_no_active_skills_has_no_skill_section():
    result = assembled_text()
    assert "Active Skill" not in result


def test_active_skill_injected(tmp_path, monkeypatch):
    monkeypatch.setattr("prompts.SKILLS_DIR", tmp_path)
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# My Skill\nDo the thing.")
    result = assembled_text(active_skills=["my-skill"])
    assert "Do the thing." in result
    assert "my-skill" in result


def test_missing_skill_ignored(tmp_path, monkeypatch):
    monkeypatch.setattr("prompts.SKILLS_DIR", tmp_path)
    result = assembled_text(active_skills=["nonexistent"])
    assert "nonexistent" not in result


def test_memory_injected_when_exists(tmp_path, monkeypatch):
    memory_file = tmp_path / "MEMORY.md"
    memory_file.write_text("- [test](test.md) — a test memory")
    monkeypatch.setattr("prompts.MEMORY_INDEX", memory_file)
    result = assembled_text()
    assert "a test memory" in result


def test_memory_absent_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr("prompts.MEMORY_INDEX", tmp_path / "MEMORY.md")
    result = assembled_text()
    assert "Persistent Memory" not in result


def test_persona_present():
    result = assembled_text()
    assert "direct and opinionated" in result


def test_persona_present_even_without_memory(tmp_path, monkeypatch):
    monkeypatch.setattr("prompts.MEMORY_INDEX", tmp_path / "MEMORY.md")
    result = assembled_text()
    assert "direct and opinionated" in result


def test_persona_before_memory_section(tmp_path, monkeypatch):
    memory_file = tmp_path / "MEMORY.md"
    memory_file.write_text("- [test](test.md) — a test memory")
    monkeypatch.setattr("prompts.MEMORY_INDEX", memory_file)
    result = assembled_text()
    assert result.index("direct and opinionated") < result.index("Persistent Memory")


def test_persona_has_no_em_or_en_dash():
    assert "—" not in prompts._PERSONA
    assert "–" not in prompts._PERSONA


def test_persona_language_instruction_present():
    result = assembled_text()
    assert "Default to Italian" in result


def test_persona_humor_guardrail_present():
    result = assembled_text()
    assert "A missed joke beats a forced one" in result


def test_single_block_when_no_active_skills():
    blocks = prompts.assemble_blocks()
    assert len(blocks) == 1
    assert blocks[0]["cache_control"] == {"type": "ephemeral"}


def test_two_blocks_when_skill_active(tmp_path, monkeypatch):
    monkeypatch.setattr("prompts.SKILLS_DIR", tmp_path)
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# My Skill\nDo the thing.")
    blocks = prompts.assemble_blocks(active_skills=["my-skill"])
    assert len(blocks) == 2
    assert all(b["cache_control"] == {"type": "ephemeral"} for b in blocks)
    assert "Do the thing." in blocks[1]["text"]


def test_single_block_when_active_skill_missing(tmp_path, monkeypatch):
    monkeypatch.setattr("prompts.SKILLS_DIR", tmp_path)
    blocks = prompts.assemble_blocks(active_skills=["nonexistent"])
    assert len(blocks) == 1
