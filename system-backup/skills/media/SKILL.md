---
name: media
description: Skills for working with media content — YouTube, music, playlists, audio, and video. Covers search, playback, browser selection, and logged-in session preservation.
version: 1.1.0
platforms: [windows]
triggers:
  - youtube
  - music
  - playlist
  - video
  - play
  - listen
  - watch
  - anime openings
  - spotify
  - soundcloud
---

# Media Skill — YouTube, Music, Playlists

## Core Principle
Always use the **minimum viable browser** for the task:
- **Headless browser** (`browser_navigate`) for simple info retrieval (e.g., search results).
- **Desktop browser** (`terminal("start ...")`) for logged-in sessions (YouTube, Facebook, Gmail).

## Trigger Conditions
Use this skill when the user asks to:
- Play music or videos on YouTube
- Open a playlist or channel
- Listen to anime openings, soundtracks, or albums
- Watch videos or streams
- Use Spotify, SoundCloud, or other music platforms

## YouTube Workflow

### 1. Search for Content
Use `web_search` to find playlists, videos, or channels:
```python
web_search(query="latest anime openings 2026")
```

### 2. Select the Best Result
- Prefer **YouTube playlists** (e.g., `youtube.com/playlist?list=...`).
- Fall back to **individual videos** if no playlist is found.

### 3. Open in Desktop Browser
If the headless browser fails (CDP error, logged-in session required), **fall back to the desktop browser** to preserve the user's logged-in state:
```bash
start "" "https://www.youtube.com/playlist?list=PLSEoGpRPA4UiNS9uAN9g_vGQyRf4rrNfs"
```

**Why?** Headless browsers cannot access logged-in YouTube sessions. The desktop browser keeps the user's account and preferences intact.

### 4. Verification
- Confirm the playlist/video opened in the user's default browser.
- If the user reports issues, check if the browser is already logged in.

## Browser Selection Rules

| Task | Recommended Browser | Why |
|------|----------------------|-----|
| YouTube search | Headless (`browser_navigate`) | Fast, no login needed |
| YouTube playback | Desktop (`start ""`) | Preserves logged-in session |
| Facebook/Gmail | Desktop (`start ""`) | Preserves logged-in session |
| General web | Headless (`browser_navigate`) | Fast, no side effects |

## Pitfalls
- **Headless browser fails on logged-in sites**: YouTube, Facebook, and Gmail require persistent sessions. Use the desktop browser for these.
- **CDP errors**: If `browser_navigate` fails with "Auto-launch failed", the CDP endpoint is unreachable. Fall back to `terminal("start ...")`.
- **Multiple Chrome instances**: Never use `taskkill /f /im chrome.exe`. It kills all Chrome processes, including the user's personal tabs.

## Supporting Files
- `references/youtube-workflow.md` — Detailed YouTube workflow and browser selection rules.

## Example Workflow
1. User asks: "Play anime openings on YouTube."
2. Search:
   ```python
   web_search(query="latest anime openings 2026")
   ```
3. Open playlist in desktop browser:
   ```bash
   start "" "https://www.youtube.com/playlist?list=PLSEoGpRPA4UiNS9uAN9g_vGQyRf4rrNfs"
   ```
4. Confirm playback started.