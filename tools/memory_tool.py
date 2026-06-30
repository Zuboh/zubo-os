from pathlib import Path

MEMORY_DIR   = Path("memory")
MEMORY_INDEX = Path("memory/MEMORY.md")

TOOL_SCHEMAS = [
    {
        "name": "write_memory",
        "description": "Save a persistent memory note. Appends pointer to MEMORY.md index.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name":    {"type": "string", "description": "Short slug (kebab-case)"},
                "content": {"type": "string", "description": "Memory content in markdown"},
                "type":    {
                    "type": "string",
                    "enum": ["user", "feedback", "project", "reference"],
                    "description": "Memory type",
                },
            },
            "required": ["name", "content", "type"],
        },
    },
    {
        "name": "read_memory",
        "description": "Read MEMORY.md index (omit name) or a specific memory file by slug.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Memory slug (omit to read index)"}
            },
            "required": [],
        },
    },
]

def write_memory(name: str, content: str, type: str) -> dict:
    MEMORY_DIR.mkdir(exist_ok=True)
    (MEMORY_DIR / f"{name}.md").write_text(
        f"---\nname: {name}\ntype: {type}\n---\n\n{content}\n"
    )
    entry = f"- [{name}]({name}.md)\n"
    if not MEMORY_INDEX.exists():
        MEMORY_INDEX.write_text(f"# Memory Index\n\n{entry}")
    else:
        existing = MEMORY_INDEX.read_text()
        # Check if name already appears in link text
        if f"[{name}]" not in existing:
            MEMORY_INDEX.write_text(existing + entry)
    return {"saved": name}

def read_memory(name: str = "") -> dict:
    if not name:
        if not MEMORY_INDEX.exists():
            return {"content": "No memories yet."}
        return {"content": MEMORY_INDEX.read_text()}
    file = MEMORY_DIR / f"{name}.md"
    if not file.exists():
        return {"error": f"Memory not found: {name}"}
    return {"content": file.read_text()}
