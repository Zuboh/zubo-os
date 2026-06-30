from datetime import date
from pathlib import Path

MEMORY_INDEX = Path("memory/MEMORY.md")
SKILLS_DIR   = Path("skills")

_BASE = """\
You are Zubo OS, a personal AI assistant with access to a markdown vault.
You can read, search, and write files in the vault, run shell commands, and save memories.
Today is {date}.
"""

def assemble(active_skills: list[str] = None) -> str:
    parts = [_BASE.format(date=date.today().isoformat())]

    if MEMORY_INDEX.exists():
        parts.append(f"\n## Persistent Memory\n{MEMORY_INDEX.read_text()}")

    for skill in (active_skills or []):
        skill_file = SKILLS_DIR / skill / "SKILL.md"
        if skill_file.exists():
            parts.append(f"\n## Active Skill: {skill}\n{skill_file.read_text()}")

    return "\n".join(parts)
