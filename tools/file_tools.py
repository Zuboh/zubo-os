import os
import re
from pathlib import Path

VAULT_PATH = Path(os.getenv("VAULT_PATH", "./example-vault"))

TOOL_SCHEMAS = [
    {
        "name": "read_file",
        "description": "Read a file from the vault by relative path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path from vault root"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "search_vault",
        "description": "Search all vault files for a keyword (case-insensitive). Returns matching files and up to 3 matching lines per file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search term"}
            },
            "required": ["query"],
        },
    },
    {
        "name": "list_files",
        "description": "List all markdown files in the vault.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "write_file",
        "description": "Write or overwrite a file in the vault. Creates parent directories if needed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path":    {"type": "string", "description": "Relative path from vault root"},
                "content": {"type": "string", "description": "File content"},
            },
            "required": ["path", "content"],
        },
    },
]


def read_file(path: str) -> dict:
    full = VAULT_PATH / path
    if not full.exists():
        return {"error": f"File not found: {path}"}
    return {"content": full.read_text()}


def search_vault(query: str) -> dict:
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    results = []
    for f in VAULT_PATH.rglob("*.md"):
        text = f.read_text()
        if pattern.search(text):
            lines = [l.strip() for l in text.splitlines() if pattern.search(l)][:3]
            results.append({"file": str(f.relative_to(VAULT_PATH)), "matches": lines})
    return {"matches": results}


def list_files() -> dict:
    files = sorted(str(f.relative_to(VAULT_PATH)) for f in VAULT_PATH.rglob("*.md"))
    return {"files": files}


def write_file(path: str, content: str) -> dict:
    full = VAULT_PATH / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content)
    return {"written": path}
