import pytest


@pytest.fixture
def fake_vault(tmp_path):
    daily = tmp_path / "daily"
    daily.mkdir()
    (daily / "2026-07-01.md").write_text(
        "---\ntype: daily\n---\n\n# July 1\n\nWorked on Python agents today."
    )
    resources = tmp_path / "resources"
    resources.mkdir()
    (resources / "python-agents.md").write_text(
        "---\ntype: resource\n---\n\n# Python Agents\n\nPatterns for anthropic SDK agents."
    )
    return tmp_path
