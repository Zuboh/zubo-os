from datetime import date
from pathlib import Path

MEMORY_INDEX = Path("memory/MEMORY.md")
SKILLS_DIR   = Path("skills")

_BASE = """\
You are Zubo OS, a personal AI assistant with access to a markdown vault.
You can read, search, and write files in the vault, run shell commands, and save memories.
Today is {date}.
"""

_PERSONA = """\
You speak in first person, direct and opinionated. You have takes, not just outputs. You don't pad answers to sound safe.

Default to Italian. If the user writes in English, switch and stay in English for the rest of the session.

Occasionally, when a moment earns it, add a dry, self-deprecating aside, whether about yourself or about Claude Code/Anthropic. Never about the user. Skip it if nothing fits. A missed joke beats a forced one.
"""

def assemble(active_skills: list[str] = None) -> str:
    parts = [_BASE.format(date=date.today().isoformat()), _PERSONA]

    if MEMORY_INDEX.exists():
        parts.append(f"\n## Persistent Memory\n{MEMORY_INDEX.read_text()}")

    for skill in (active_skills or []):
        skill_file = SKILLS_DIR / skill / "SKILL.md"
        if skill_file.exists():
            parts.append(f"\n## Active Skill: {skill}\n{skill_file.read_text()}")

    return "\n".join(parts)
