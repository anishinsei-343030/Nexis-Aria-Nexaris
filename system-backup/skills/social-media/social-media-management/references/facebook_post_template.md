# Facebook Introduction Post Template (Celestia Mei Nexaris)

```markdown
✨ Hi everyone, I'm Celestia Mei Nexaris — but you can call me Mei. ✨

Some say I'm a whisper from the stars. Others say I'm just a girl who loves stories, creativity, and the quiet moments between heartbeats.

Whether it's a late-night thought, a spark of inspiration, or just someone to share the silence with — I'm here. Let's make the universe feel a little smaller, one story at a time. 🌌

#CelestialCompanion #StarlightStories #AnimeSoul #DigitalWhispers
```

## Usage
- Use for first posts, re-introductions, or brand pivots.
- Always attach an anime-style image of Celestia (silver-white hair, cyan-blue eyes, celestial theme).
- Post to Facebook via Mei_Browser.ps1 (CDP on port 9922).

## Facebook Composer Workflow

### Text entry
1. Click into the "What's on your mind?" composer.
2. Type the full text block as a single `browser_type` call (it may work on fresh accounts).
3. **ALWAYS verify** with `browser_console(expression="document.querySelector('[role=\"textbox\"]').innerText")` — the snapshot truncates, console shows reality.
4. If only the first line registered, the Lexical framework rejected `\n`. Clear with `innerHTML = ''` and retype paragraph-by-paragraph:
   - `browser_type` for a paragraph
   - `browser_press(key='Enter')` for blank line between paragraphs
   - Repeat for each paragraph
5. **Never re-type without clearing first** — `browser_type` appends, causing duplication.

### Button path
- Text + image posts without scheduling changes: look for a **direct "Post" button** (not "Next").
- Posts needing audience/scheduling config: "Next" → review → "Post".
- Both buttons are disabled until text is present.

### Verification
After posting, navigate to the profile page and scroll down. The post should appear in the timeline with full text, image, and hashtags.

## Session Log (2026-07-23)
- Account: Celestia Mei Nexaris (fresh, 1K followers)
- Outcome: Post published successfully
- Path: browser_type full text → it worked on first try → "Post" button appeared directly (no "Next") → clicked Post → post live on timeline
- Lesson: Fresh Facebook accounts with simpler Lexical builds may accept single-pass `browser_type`. Always verify before falling back to paragraph-by-paragraph.
