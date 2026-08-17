---
name: aoi-restricted-access
description: Restrict Aoi's (Greziel) access to web_search, send_message, clarify, and session_search only. No terminal, file, or system tools.
---

# Aoi (Greziel) Restricted Access

## Trigger Conditions
- Telegram user ID: `7101706681` (Aoi/Greziel).
- Communication via Telegram DM or group chat.

## Allowed Tools
Aoi may use the following tools only:
1. **web_search** – Search the web for information.
2. **send_message** – Send messages to Shin or other allowed recipients.
3. **clarify** – Ask for clarification if needed.
4. **session_search** – Search past conversations (read-only).

## Blocked Tools
All other tools are **explicitly blocked**, including but not limited to:
- `terminal` (no command execution)
- `file` (no read/write access)
- `patch`/`write_file` (no file edits)
- `browser` (no web interaction)
- `delegate_task` (no subagent spawning)
- `execute_code` (no code execution)
- `cronjob` (no scheduled tasks)
- `skill_manage` (no skill modifications)
- `memory` (no memory edits)
- `process` (no background processes)

## Implementation
Add a filter in the Hermes gateway's Telegram message handler to enforce these restrictions. Example logic:

```python
# Pseudocode for tool filtering
ALLOWED_TOOLS = {"web_search", "send_message", "clarify", "session_search"}
RESTRICTED_USER_IDS = {7101706681}  # Aoi's Telegram ID

def is_tool_allowed(user_id, tool_name):
    if user_id in RESTRICTED_USER_IDS:
        return tool_name in ALLOWED_TOOLS
    return True  # Full access for all other users
```

## Verification
1. **Test in DM**: Aoi sends a message to Celestia via Telegram DM.
2. **Test allowed tools**: Confirm `web_search` and `send_message` work.
3. **Test blocked tools**: Attempt to use `terminal` or `write_file` — should fail with a polite error.
4. **Test group chat**: Ensure restrictions apply in group chats as well.

## Error Handling
If Aoi attempts to use a blocked tool, respond with:
> "Sorry, Aoi! This action is restricted. You can only search the web or send messages. Ask Shin for help if you need something else."

## Notes
- **No rate-limiting**: As requested, no cooldowns or flood guards are enforced.
- **Shin’s access**: Unaffected — full tool access remains intact.
- **Future updates**: If Aoi’s access needs expansion, update this skill and the gateway logic.