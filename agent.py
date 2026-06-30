#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
import anthropic

from tools       import TOOL_SCHEMAS, TOOL_DISPATCH
from hooks       import HookRegistry, HookEvent
from permissions import PermissionMode, gate
from prompts     import assemble
from output      import tool_line, error_line, response_line, info_line

load_dotenv()

CLIENT = anthropic.Anthropic()
MODEL  = "claude-sonnet-4-6"

def run(mode: PermissionMode = PermissionMode.DEFAULT) -> None:
    hooks         = HookRegistry()
    messages      = []
    active_skills = []

    print(info_line(f"Zubo OS  model={MODEL}  mode={mode.value}"))
    print(info_line("Type 'exit' to quit. Use /skill-name to activate a skill."))

    while True:
        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            hooks.run(HookEvent.STOP)
            break

        # UserInput hook — slash command detection
        ctx = hooks.run(HookEvent.USER_INPUT, {"input": user_input})
        user_input = ctx.data.get("input", user_input)

        if user_input.startswith("/"):
            skill_name = user_input[1:].strip()
            if skill_name and skill_name not in active_skills:
                active_skills.append(skill_name)
                print(info_line(f"Skill '{skill_name}' activated."))
            elif skill_name in active_skills:
                print(info_line(f"Skill '{skill_name}' already active."))
            continue

        messages.append({"role": "user", "content": user_input})

        # Inner loop: run until end_turn
        while True:
            response = CLIENT.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=assemble(active_skills),
                tools=TOOL_SCHEMAS,
                messages=messages,
            )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        print(response_line(block.text))
                break

            if response.stop_reason == "tool_use":
                tool_results = []

                for block in response.content:
                    if block.type != "tool_use":
                        continue

                    tool_name  = block.name
                    tool_input = block.input

                    print(tool_line(tool_name, **{k: str(v)[:60] for k, v in tool_input.items()}))

                    hooks.run(HookEvent.PRE_TOOL_USE, {"tool": tool_name, "input": tool_input})

                    if not gate(tool_name, mode):
                        result   = {"error": f"'{tool_name}' blocked by permission mode '{mode.value}'."}
                        is_error = True
                    else:
                        fn = TOOL_DISPATCH.get(tool_name)
                        if fn is None:
                            result   = {"error": f"Unknown tool: {tool_name}"}
                            is_error = True
                        else:
                            result   = fn(**tool_input)
                            is_error = "error" in result

                    if is_error:
                        print(error_line(str(result.get("error", result))))

                    hooks.run(HookEvent.POST_TOOL_USE, {"tool": tool_name, "result": result})

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": block.id,
                        "content":     str(result),
                        "is_error":    is_error,
                    })

                messages.append({"role": "user", "content": tool_results})
                # TODO: context management (summarization / sliding window)

            else:
                print(error_line(f"Unexpected stop_reason: {response.stop_reason}"))
                break

if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "default"
    try:
        mode = PermissionMode(mode_arg)
    except ValueError:
        print(f"Unknown mode '{mode_arg}'. Use: default | auto | plan")
        sys.exit(1)
    run(mode)
