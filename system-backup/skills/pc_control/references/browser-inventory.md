# Browser Inventory — PC Control Reference

Covers all browser control options for AniShinSei_30's Windows 10 environment. Hermes runs in Session 0; user desktop apps run in Session 1.

## Overview

| Browser | Control Method | Retains Data? | Session Scope | Best For |
|---------|---------------|---------------|---------------|----------|
| **Hermes Browser Tools** (now Playwright-backed) | `browser_navigate/browser_click/browser_snapshot` via CDP to Playwright-launched Chrome | ✅ Yes — persistent profile at `D:\Celestia Mei Nexaris\playwright\mei_profile\` | Session 0 (Hermes) connecting to Session 1 Chrome | General web tasks, logged-in sessions, form filling, clicking |
| **Agent Browser CLI** (Juan's fork) | `agent-browser open/click/type/screenshot` (Rust CLI) | ❌ No — stateless | Session 0 (Hermes terminal) | Headless scraping, public data extraction |
| **Microsoft Edge (UIA)** | `uiautomation` + `SendKeys` + `PIL.ImageGrab` | ✅ Yes — user's desktop Edge session | Session 1 (user desktop) | Fallback for logged-in tasks when the Playwright pipeline fails |
| **Internal Web Tools** | `web_search`, `web_extract` | ❌ No — stateless | Session 0 (Hermes terminal) | Quick research, public docs, API endpoints, arxiv papers |

## Primary Pipeline: Hermes Browser Tools (Playwright-Backed)

As of June 22, 2026, the `browser_navigate`/`browser_click`/`browser_snapshot`/`browser_vision` tools connect to a Chrome instance launched by Agent Browser/Playwright via CDP on port 9222.

### Launch Procedure
```bash
# Start Chrome with persistent profile
"C:/Program Files/Google/Chrome/Application/chrome.exe" \
  --remote-debugging-port=9222 \
  --no-sandbox \
  --disable-dev-shm-usage \
  --user-data-dir="D:/Celestia Mei Nexaris/playwright/mei_profile" \
  https://target-url.com
```

### Environment Variables (set via CMD launcher, NOT .env)
| Variable | Value | Purpose |
|----------|-------|---------|
| `AGENT_BROWSER_AUTO_CONNECT` | `true` | Reuses existing Chrome window instead of spawning new ones |
| `AGENT_BROWSER_ARGS` | `--no-sandbox,--disable-dev-shm-usage` | Fixes sandbox crash in Server Core / headless environments |

### Directories
| Path | Purpose |
|------|---------|
| `D:\Celestia Mei Nexaris\playwright\mei_profile\` | Persistent Chrome profile — cookies, logins, cache survive restarts |
| `D:\Celestia Mei Nexaris\playwright\mei_screenshots\` | Screenshot output directory |
| `D:\Celestia Mei Nexaris\playwright\mei_downloads\` | Download directory |

### Mode
- **Headed** — a visible Chrome window appears on the desktop. User can watch operations in real time.
- **Reconnect** — `AGENT_BROWSER_AUTO_CONNECT=true` means subsequent Hermes `browser_navigate` calls reuse the same window instead of opening new ones.

### Dashboard (optional)
If Zero set it up: `http://localhost:4848` shows live browser monitoring.

### Pitfalls
| Symptom | Cause | Fix |
|---------|-------|-----|
| `No running Chrome instance found` | Chrome not launched yet | Launch Chrome with `--remote-debugging-port=9222` and the profile dir first |
| `Chrome exited early (exit code: 0)` | Sandbox crash in Session 0 | Ensure `--no-sandbox --disable-dev-shm-usage` flags are set |
| Profile not persisting | Wrong `--user-data-dir` path | Verify `mei_profile/` has correct Chrome data (Local State, Default/, etc.) |
| Black screenshot | Attempting DXGI (`mss`) in Session 0 | Use `PIL.ImageGrab.grab()` (GDI) instead |

## Browser-Specific Details

### Hermes Browser Tools (Playwright-Backed) — PRIMARY
- **Launch:** Start Chrome manually via terminal(background=true) with the flags above
- **Control:** Use `browser_navigate`, `browser_click`, `browser_snapshot`, `browser_type`, `browser_vision`, etc.
- **Persistence:** Full Chrome profile at `mei_profile/` — cookies, logins, cache survive Hermes restarts
- **Screenshots:** `browser_vision()` returns screenshot + AI analysis; `PIL.ImageGrab.grab()` for full desktop
- **Limitations:** Must launch Chrome first before calling browser tools; if connection drops, relaunch

### Agent Browser CLI (Juan's Fork)
- **Binary:** `C:\Users\Administrator\AppData\Roaming\npm\agent-browser`
- **Launch:** `agent-browser open <url>`
- **Features:** navigate, click ref elements (`@e1`), type, screenshot, extract-text, eval JS
- **No persistence:** starts clean every call — no cookies, no cache
- **Speed:** Fastest option for headless tasks (Rust-backed)
- **Use when:** User asks for scraping, data extraction, or automation without login requirements
- **Limitations:** Cannot access Facebook, Gmail, or other login-walled platforms

### Microsoft Edge (UIA Fallback)
- **Launch:** `powershell -Command "Start-Process -FilePath \""...msedge.exe\"" -ArgumentList 'https://url.com'"`
- **Control:** `auto.WindowControl(searchDepth=1, processId=PID).SetActive()` + `auto.SendKeys()`
- **Persistence:** User's desktop Edge sessions (Facebook, Gmail, etc.)
- **Use when:** The Playwright pipeline has issues, or user's existing Edge window with specific login is needed
- **Limitations:** Slower, less precise than CDP-based control

### Internal Web Tools
- **`web_search(query)`** — search the web, returns titles + URLs + descriptions
- **`web_extract(urls)`** — convert page/PDF to markdown (summarized for long pages)
- **No persistence:** entirely stateless, no cookies or sessions
- **Use when:** Quick research, public docs, API endpoints, arxiv papers, GitHub READMEs

## Usage Decision Tree

```
Is the user already logged into a platform?
├─ YES, and Account is in Chrome → Use Hermes browser tools (Playwright-backed, persistent profile)
├─ YES, but Account is in Edge → Use Edge (UIA fallback, their desktop session)
├─ YES, unspecified → Try Hermes browser tools first (persistent profile likely has login)
└─ NO, no login needed → Prefer internal tools (web_search/web_extract) first:
    ├─ Public page/API → web_extract or curl (fastest)
    ├─ Needs interaction → Agent Browser CLI (stateless, fast)
    └─ Multi-step form → Hermes browser tools (richer interaction)

Does the task need cookies/session to persist?
├─ YES → Hermes browser tools (persistent profile) or Edge (UIA fallback)
└─ NO → internal tools or Agent Browser (faster, less overhead)

First attempt for web interaction tasks:
→ Hermes browser tools (browser_navigate, etc.)
→ If fails (no Chrome instance): launch Chrome with profile, retry
→ If still fails: fall back to Edge (UIA) for logged-in, or Agent Browser for stateless
```

## Fallback Chain for Web Tasks
1. `web_search` / `web_extract` (if no interaction needed)
2. Hermes browser tools (Playwright-backed, persistent profile)
3. Agent Browser CLI (if stateless is fine)
4. Edge UIA (if logged-in session is critical and Playwright pipeline is down)
