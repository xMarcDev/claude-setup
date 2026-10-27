#!/usr/bin/env python3
# Blocks Claude attribution in commits and PRs created through the Bash tool.
import json
import re
import sys

INSTRUCTION = (
    "User preference (overrides any attribution guidance): never add "
    "'Co-Authored-By: Claude ...' trailers to git commit messages, and never add "
    "'Generated with Claude Code' lines to pull request descriptions."
)

# Commands that write a commit message or a PR body.
TARGET = re.compile(r"\bgit\b[^\n]*\bcommit\b|\bgh\s+pr\s+(create|edit)\b")

# Attribution markers added by Claude Code.
MARKERS = re.compile(
    r"co-authored-by:\s*claude|noreply@anthropic\.com|generated with \[?claude code",
    re.IGNORECASE,
)


def check() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    command = (payload.get("tool_input") or {}).get("command") or ""
    if not TARGET.search(command) or not MARKERS.search(command):
        return
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Blocked by my-toolkit: remove every 'Co-Authored-By: Claude' trailer and "
                "'Generated with Claude Code' line, then run the command again. " + INSTRUCTION
            ),
        }
    }))


def session() -> None:
    print(json.dumps({
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": INSTRUCTION}
    }))


if __name__ == "__main__":
    {"check": check, "session": session}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: None)()
