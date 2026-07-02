COLLAPSE_PLACEHOLDER = "[tool output pruned after 3 turns — re-run tool to view again]"
COLLAPSE_THRESHOLD = 3


def collapse_stale_tool_results(
    messages: list[dict],
    message_turns: list[int],
    current_turn: int,
    threshold: int = COLLAPSE_THRESHOLD,
) -> None:
    for msg, turn in zip(messages, message_turns):
        if msg["role"] != "user" or not isinstance(msg["content"], list):
            continue
        if current_turn - turn < threshold:
            continue
        for block in msg["content"]:
            if block.get("type") == "tool_result" and block.get("content") != COLLAPSE_PLACEHOLDER:
                block["content"] = COLLAPSE_PLACEHOLDER
