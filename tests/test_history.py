from history import collapse_stale_tool_results, COLLAPSE_PLACEHOLDER, COLLAPSE_THRESHOLD


def _tool_result_message(content="original file text"):
    return {
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": "toolu_1",
            "content": content,
            "is_error": False,
        }],
    }


def test_tool_result_at_threshold_is_collapsed():
    messages = [_tool_result_message()]
    message_turns = [1]
    collapse_stale_tool_results(messages, message_turns, current_turn=1 + COLLAPSE_THRESHOLD)
    assert messages[0]["content"][0]["content"] == COLLAPSE_PLACEHOLDER


def test_tool_result_below_threshold_untouched():
    messages = [_tool_result_message()]
    message_turns = [1]
    collapse_stale_tool_results(messages, message_turns, current_turn=1 + COLLAPSE_THRESHOLD - 1)
    assert messages[0]["content"][0]["content"] == "original file text"


def test_already_collapsed_block_not_reprocessed():
    messages = [_tool_result_message(content=COLLAPSE_PLACEHOLDER)]
    message_turns = [1]
    # Should not raise, and content stays the placeholder.
    collapse_stale_tool_results(messages, message_turns, current_turn=1000)
    assert messages[0]["content"][0]["content"] == COLLAPSE_PLACEHOLDER


def test_plain_user_text_message_untouched():
    messages = [{"role": "user", "content": "hello there"}]
    message_turns = [1]
    collapse_stale_tool_results(messages, message_turns, current_turn=1000)
    assert messages[0]["content"] == "hello there"


def test_assistant_message_untouched():
    messages = [{
        "role": "assistant",
        "content": [{"type": "tool_use", "id": "toolu_1", "name": "read_file", "input": {}}],
    }]
    message_turns = [1]
    collapse_stale_tool_results(messages, message_turns, current_turn=1000)
    assert messages[0]["content"][0]["name"] == "read_file"


def test_mixed_history_only_stale_tool_result_collapsed():
    messages = [
        {"role": "user", "content": "first question"},
        {"role": "assistant", "content": [{"type": "text", "text": "answer"}]},
        _tool_result_message(),
    ]
    message_turns = [1, 1, 1]
    collapse_stale_tool_results(messages, message_turns, current_turn=1 + COLLAPSE_THRESHOLD)
    assert messages[0]["content"] == "first question"
    assert messages[1]["content"][0]["text"] == "answer"
    assert messages[2]["content"][0]["content"] == COLLAPSE_PLACEHOLDER
