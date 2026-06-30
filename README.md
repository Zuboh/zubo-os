# Zubo OS

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Tests](https://github.com/Zuboh/zubo-os/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)

A minimal personal AI agent built on the Claude API.
Demonstrates the same architectural patterns as Claude Code:
hook system, permission model, skill injection, context assembly.

> "Only 1.6% of Claude Code is AI decision logic. The other 98.4% is deterministic infrastructure."
> — [VILA-Lab analysis](https://github.com/VILA-Lab/Dive-into-Claude-Code)

## Quick start

```bash
git clone https://github.com/Zuboh/zubo-os
cd zubo-os
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY
python agent.py
```

### Modes

```bash
python agent.py default   # ask before bash/write_file (default)
python agent.py auto      # allow all tools
python agent.py plan      # no tool execution (analysis only)
```

### Skills

```
> /zubo-fitness
[INFO] Skill 'zubo-fitness' activated.
> log weight 76.5kg today
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for deep technical breakdown,
loop diagram, and comparison with Claude Code internals.

## Inspired by

- [Andrej Karpathy — LLM OS](https://x.com/karpathy/status/1723140519554191579)
- [Simon Willison — Tool use patterns](https://simonwillison.net)
- [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)
- [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)
