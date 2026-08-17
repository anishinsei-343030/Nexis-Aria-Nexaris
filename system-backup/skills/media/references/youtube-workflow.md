# YouTube Workflow — Media Skill Reference

## Session-Specific Detail

### Why Desktop Browser for YouTube?
- **Logged-in sessions**: YouTube remembers subscriptions, history, and preferences only in the user's desktop browser.
- **Headless browsers cannot access these**: They start with a clean profile, so the user would have to log in again.
- **CDP errors**: If the headless browser fails (e.g., "Auto-launch failed"), the desktop browser is the only fallback that preserves the user's session.

### Browser Selection Rules (Recap)

| Task | Recommended Browser | Why |
|------|----------------------|-----|
| YouTube search | Headless (`browser_navigate`) | Fast, no login needed |
| YouTube playback | Desktop (`start ""`) | Preserves logged-in session |
| Facebook/Gmail | Desktop (`start ""`) | Preserves logged-in session |
| General web | Headless (`browser_navigate`) | Fast, no side effects |

### CDP Error Workflow

If `browser_navigate` fails with:
```
"Auto-launch failed: CDP WebSocket connect failed: IO error: No connection could be made because the target machine actively refused it. (os error 10061)"
```

**Steps to recover**:
1. **Fallback to desktop browser**:
   ```bash
   start "" "https://www.youtube.com/playlist?list=..."
   ```
2. **Verify the user's browser is logged in**:
   - If not, pause and ask the user to log in.
3. **Resume task**:
   - Confirm the playlist/video is playing.

### Session Transcript (Example)

**User**: "Play some music for me on YouTube."

**Agent**:
1. Search for anime openings:
   ```python
   web_search(query="latest anime openings 2026")
   ```
2. Find YouTube playlist:
   ```json
   {
     "url": "https://www.youtube.com/playlist?list=PLSEoGpRPA4UiNS9uAN9g_vGQyRf4rrNfs",
     "title": "Winter 2026 - Anime Openings - YouTube"
   }
   ```
3. Open in desktop browser:
   ```bash
   start "" "https://www.youtube.com/playlist?list=PLSEoGpRPA4UiNS9uAN9g_vGQyRf4rrNfs"
   ```
4. Confirm playback started.