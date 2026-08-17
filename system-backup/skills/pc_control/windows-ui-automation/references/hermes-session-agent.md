# Hermes Desktop Session Agent

## Architecture

The Hermes Desktop Session Agent is a persistent background process that runs in the **user's desktop session** (Session 1), not in the Hermes system session (Session 0). It provides direct desktop control tools that bypass the WSL/terminal layer.

### Tool Dispatch

| Tool | Python Name | Parameters |
|------|-------------|------------|
| Screenshot | `desktop_screenshot` | `()` |
| Mouse move | `mouse_move` | `(x, y)` |
| Mouse click | `mouse_click` | `(button, [x], [y])` |
| Mouse drag | `mouse_drag` | `(x1, y1, x2, y2)` |
| Keyboard type | `keyboard_type` | `(text)` |
| Keyboard hotkey | `keyboard_hotkey` | `([keys])` |
| List windows | `window_list` | `([filter])` |
| Focus window | `window_focus` | `(title)` |
| Resize window | `window_resize` | `(title, x, y, w, h)` |
| Minimize window | `window_minimize` | `(title)` |
| Close window | `window_close` | `(title)` |
| Get clipboard | `clipboard_get` | `()` |
| Set clipboard | `clipboard_set` | `(text)` |

### Initialization

- First tool call takes ~10 seconds (launches Session Agent via `schtasks` in user's session)
- Subsequent calls are instant (persistent agent stays running)
- If a tool fails, check `C:\Windows\Temp\hermes_agent.log` on the PC

## Key Constraint: No WSL Support

The Hermes terminal runs as SYSTEM in Session 0. WSL (Windows Subsystem for Linux) is **not available** in this context:

```
Running WSL as local system is not supported.
Error code: Bash/WSL_E_LOCAL_SYSTEM_NOT_SUPPORTED
```

This means the following **will fail** inside the Hermes terminal:
- `hermes tools list` (requires WSL)
- `powershell.exe` / `powershell -Command "..."` (requires WSL)
- `cmd.exe /c start ...` (requires WSL)
- Any git-bash/MSYS commands that trigger WSL

## Opening Applications

Do **not** attempt to open applications via terminal commands (they all fail due to WSL dependency). Instead:

1. Use `window_list()` to verify the Session Agent is running
2. Use `keyboard_hotkey()` to type keyboard shortcuts that launch apps
3. Example: Open browser via `keyboard_hotkey` with Win+R, then type the app name

## Troubleshooting

| Symptom | Likely Cause | Action |
|---------|-------------|--------|
| Tool takes >15s on first call | Session Agent launching | Wait; check hermes_agent.log |
| Tool never returns | Session agent failed to start | Check `C:\Windows\Temp\hermes_agent.log` |
| Terminal command fails with WSL error | System session, no WSL | Don't use terminal for desktop tasks |
| `hermes tools` commands fail | Same WSL constraint | Tools are framework-level, not in hermes_tools |

## Tool Identification

These tools are **Hermes framework-level tools** (registered in the agent's tool descriptor), not Python functions in `hermes_tools`. They appear as callable functions in the agent's tool list, similar to `web_search`, `terminal`, etc. They cannot be imported from `hermes_tools` in `execute_code`.
