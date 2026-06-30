---
type: resource
created: 2026-06-28
tags: [python, ai, agents]
---

# Python Agents — Reference

## Message accumulation pattern

Maintain `messages: list[dict]`. Append user messages AND full assistant
responses (including `tool_use` blocks). Tool results go back as user turn.

## Tool dispatch pattern

```python
DISPATCH = {"tool_name": fn}
result = DISPATCH[name](**tool_input)
```

## Stop reason loop

- `end_turn` → print text response, break inner loop
- `tool_use` → execute tools, append results as user turn, continue inner loop
- Anything else → log error, break
