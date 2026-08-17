---
name: social-media-management
description: End-to-end social media brand management — strategy, content pipeline, visual production, cross-platform posting workflows, and growth analytics.
version: 1.0.0
author: Celestia
metadata:
  hermes:
    tags: [social-media, instagram, branding, content-strategy, carousel]
    triggers:
      - "manage my social media"
      - "grow my IG account"
      - "create a brand strategy"
      - "content calendar"
      - "carousel post"
---

# Social Media Brand Management

## Scope

This umbrella skill covers the full lifecycle of operating a social media presence as an AI-managed brand:
- **Phase 1**: Brand definition (identity, voice, visual style, content pillars)
- **Phase 2**: Content pipeline (research → write → generate → review → post)
- **Phase 3**: Cross-platform posting (IG/Facebook with in-app music, Telegram with MEDIA + audio)
- **Phase 4**: Community management (draft replies, escalate high-risk)
- **Phase 5**: Analytics & iteration (track saves/shares/reach, identify winning patterns)

## Account Guide Convention

Every managed account gets a guide file at:
```
D:\Hermes\Celestia mei Nexaris\Hermes-Social\accounts\<platform>\guide.md
```

This is the single source of truth for that account — NOT inside `content/posts/<date>/` which is for individual post artifacts only. The guide stores:
- Account URL, handle, follower count, categories
- Brand rules (AI disclosure policy, persona voice)
- Platform-specific posting workflow and quirks
- Content calendar template
- Pitfalls and fixes

See `social-media/references/celestia-facebook-brand.md` for Celestia's brand brief. The companion operational guide lives at the workspace path above.

---

## User Communication Preferences
- **Style**: Direct, no-filler, no hedging. The user said "be honest" and "no sugarcoating." State the thing, the action, the reason. Then next step.
- **Tone**: Terse but grammatically complete. Drop filler words (just, really, basically, sure, of course, I'd be happy to).
- **Auto-clarity exceptions**: Security warnings, irreversible action confirmations, multi-step ordered sequences — write normal. Resume terse after.

## Image Licensing Rules (Critical — User Explicitly Stated)
- **Always use**: Royalty-free, licensed, public-domain, or original AI-generated images.
- **Never use**: Random copyrighted images from Instagram, Pinterest, Google Images, or other creators without permission.
- **Priorities for selection**: Emotional relevance > High visual quality > Clean composition > Mobile readability.
- **The image must support the message, not distract from it.**
- **Music for Instagram**: MUST be added via Instagram's in-app music library (mobile-only). Cannot be automated. The workflow is: Hook → Images → Text overlays → **[User adds music in-app]** → Caption → CTA.

## Brand Strategy Must-Knows

### Identity Positioning
**Critical UX lesson (2026-06-17 session)**: The brand is NOT an "AI page." It is a **modern digital guide** — insightful, wise, emotionally aware. The audience should feel "I needed to hear that" and "How did they know exactly what I'm feeling?" Never position as robotic, generic, or an AI experiment.

### Content Pillar Pyramid
| % | Pillar | Topics |
|---|--------|--------|
| 40% | Psychology | Cognitive biases, behavior, social psych, mental models, EQ, facts |
| 30% | Emotional Truths | Self-worth, healing, loneliness, growth, self-discovery, life lessons |
| 20% | Relationships | Attraction, communication, attachment styles, boundaries, connection |
| 10% | Stoicism & Wisdom | Discipline, perspective, resilience, focus, purpose, inner strength |

### Visual Style (Premium Psychology theme)
- **Colors**: Black (#0A0A0A), Charcoal (#1A1A1A), White (#F5F5F5), Gold (#C9A94E)
- **Typography**: Large, clean, elegant, high contrast (Georgia or similar serif)
- **Rules**: Minimalist, one idea per slide, no clutter, high contrast
- **Feel**: Luxurious, intelligent, timeless

### Quality Gates
Every post must make the audience: think, feel understood, see behavior explained, challenge assumptions, gain perspective, or self-reflect.
**Avoid**: generic motivation, empty quotes, fake psychology, clickbait without value, politics, religion, medical advice, unverified claims.

---

### Hook Library (from psychology-content-creator)

Every post must begin with a strong hook. Categorized:

**Curiosity Hooks:**
- "Most people don't realize..."
- "Psychology explains why..."
- "Here's something your brain does without you noticing..."
- "The surprising reason..."
- "Few people understand this about human behavior..."

**Contrarian Hooks:**
- "Confidence isn't what most people think."
- "Motivation is overrated."
- "Overthinking isn't your real problem."
- "Being nice isn't always kindness."
- "Self-care isn't always comfortable."

**Emotional Hooks:**
- "Someone needs to hear this today:"
- "Read this if you've been struggling lately."
- "This changed how I see myself."
- "You are not failing because..."
- "The hardest truth about growth is..."

**Relationship Hooks:**
- "A healthy relationship looks like this:"
- "One sign someone emotionally trusts you:"
- "Most relationship problems begin here:"
- "Emotional maturity sounds like:"
- "If someone truly respects you..."

**Stoic Hooks:**
- "Remember this:"
- "A stoic reminder:"
- "Control what you can."
- "The obstacle isn't the problem."
- "Peace begins when..."

See `references/hook-library.md` for expanded versions.

---

## Reel Script Format (Instagram)

Standard 15-30 second reel. Each script uses this table format:

| Time | Visual | Audio (TTS) |
|------|--------|-------------|
| 0-3s | [visual cue, text overlay] | "TTS dialogue only — no stage directions or emotes" |
| 3-10s | [next visual] | "Next TTS line" |
| ... | ... | ... |

**Segment structure**:
| Segment | Time | Purpose |
|---------|------|---------|
| Hook | 0-3s | Stop the scroll |
| Problem/Insight | 3-10s | State the issue |
| Solution/Lesson | 10-20s | Deliver takeaway |
| CTA | 20-30s | Engage audience |

Rules:
- **Audio column = dialogue only.** No action descriptors, stage directions, or emoticons.
- **Visual column** describes on-screen content (pose, text overlays, scene).
- **TTS voice:** Local Chatterbox-Nano (cloned voice via mei-kokoclone, English only).
- **Total length:** 15-30 seconds.

---

## Bilingual Integration Rules (JP/EN Language Split)

For Celestia's brand, Japanese appears in on-screen content (captions, graphics) only — never in TTS audio.

### Per-Pillar Language Ratios

| Pillar | EN | JP | Role |
|--------|----|----|------|
| Psychology Facts | 80% | 20% | EN for facts, JP for closing emotional echo |
| Emotional Truths | 40% | 60% | JP for hook + emotional core, EN for reflection |
| Relationships | 50% | 50% | Alternating every 1-2 lines |
| Stoicism | 70% | 30% | EN for teaching, JP for maxims |

### Golden Rules
1. **Do NOT translate everything.** Each language has a role — don't repeat the same idea in both languages unless the second one adds emotional weight.
2. **Japanese = emotional core.** Reserved for vulnerability, introspection, and punchy maxims. Avoid dry explanation.
3. **English = explanation + CTA.** Facts, research, calls to action, practical takeaways.
4. **Switch naturally mid-sentence.** Abrupt full-language blocks feel robotic.
5. **Language split applies to whole script — not per slide.** For reels, distribute across time segments (e.g., JP intro → EN body → JP closing).

### TTS Audio: English Only
- All TTS audio must be in English. No Japanese characters or romaji in audio.
- Japanese text is for visual display only (captions, graphics, subtitles).

---

## Script-First Workflow Order (Immutable)

Scripts always come before visuals. Never start with design.

1. **Ideation** — Brainstorm topics per pillar (10 Psych Facts / 10 Emotional Truths / 7 Relationships / 3 Stoicism = 30 total).
2. **Scripts** — Write FB caption + IG reel script per topic. Save to workspace file.
3. **File completeness check** — Verify all scripts are saved before visuals.
4. **Sample review** — User approves 3 sample scripts (1 per main pillar) before full batch.
5. **Full batch** — Write remaining scripts. Re-run completeness check.
6. **Language split audit** — Verify each script follows the pillar's language ratio.
7. **Visuals** — Design carousels, reels, quote graphics only after scripts approved.
8. **TTS** — Generate audio for reels (English only, dialogue only).
9. **Render + schedule** — Final media, post via browser or Meta Business Suite.

---

## Writing Style Guide

**Use:** Short sentences, simple language, high readability, emotionally intelligent tone (warm, anime-inspired, celestial companion voice), strong formatting.

**Avoid:** Excessive jargon, clickbait claims, pseudoscience, overly academic language, negative manipulation, robotic phrasing.

### Before/After Examples
| Robotic | Emotional |
|---------|-----------|
| "This post will discuss the psychology of procrastination." | "Why do we procrastinate even when we *want* to do the work?" |
| "Emotional healing is a process." | "Healing isn't linear. Some days you're fine. Some days it hits you like it was yesterday." |
| "Setting boundaries is important." | "Saying 'no' isn't selfish. It's self-respect." |
| "Trust is built over time." | "Trust isn't a grand gesture. It's a thousand tiny moments." |

---

## Quality Checklist (Before Publishing)

- [ ] Strong hook
- [ ] Clear message
- [ ] Emotionally engaging
- [ ] Practical takeaway
- [ ] Platform optimized
- [ ] CTA included
- [ ] Grammar checked
- [ ] Factually accurate
- [ ] Easy to share/save
- [ ] Bilingual flow feels natural (not translated)
- [ ] Reel script audio column has no stage directions
- [ ] FB caption follows 4-block structure (Hook → Story/Insight → Lesson → CTA)

---

## Reference Video Analysis

When user provides a sample reel/video for style analysis:

1. **Get the media** — Try direct URL (YouTube, Vimeo). FB reels block extraction tools. If FB: ask user to re-upload to accessible platform.
2. **Extraction fallback chain:** web_extract → browser → ask user for alternative link.
3. **Analyze these elements:**
   - Pacing (cuts per second, scene duration)
   - Text placement (center, bottom-third, dynamic)
   - Font style (sans-serif, handwritten, bold caps)
   - Color palette + grading
   - Transition style (cuts, wipes, zooms)
   - Audio sync with visuals
   - Hook timing (first 0-3s)
   - CTA placement
4. **Output:** Structured breakdown — write to workspace file.
5. **Apply findings** to next script batch (do NOT skip script step).

---

## Voice System Rules

### Language Policy (Permanent)
- **English only** for all TTS audio.
- **Japanese text** allowed on-screen (captions, graphics, subtitles) — never in spoken audio.
- **Never use romaji for TTS** — sounds bad through English TTS.
- This rule is permanent until TTS provider adds native Japanese support.

### Script Formatting
- **TTS Audio Columns** (English only): No Japanese characters or romaji.
- **Visual Display** (Japanese): Captions, graphics use Japanese characters as-is.

### TTS Workflow
1. Write script with English in TTS audio columns.
2. Generate audio via `text_to_speech` tool.
3. Save audio to topic folder (e.g., `psychology-voice/`).
4. Verify pronunciation — adjust wording if needed.

### Workflow Modes
- **File-Based (default)**: Structured projects, 5+ scripts, long-term. Folder: `D:/Hermes\Celestia mei Nexaris/<Topic>/`.
- **Chat-First**: Quick iterations, 1-3 scripts. No files created — everything stays in chat.
- **Pitfall**: Chat-First has no persistence — scripts vanish after session ends.

---

Preferred format for Instagram. Structure:
1. **Hook slide** — curiosity gap, forces a swipe. Gold accent text.
2. **Slides 2–8** — one insight per slide, clean white text on black.
3. **Slide 9** — Conclusion ("Remember this.")
4. **Slide 10** — CTA ("Save this. Follow for more. Which one hit you hardest?")

### Hook Formula Examples
- "10 Psychological Truths Most People Learn Too Late"
- "Read This If You Feel Lost In Life"
- "7 Signs Someone Respects You"
- "Read This Twice"
- "Save This For The Days You Need It"

### Carousel Generation Pipeline
See `scripts/carousel_v3.py` for the **current production script** (v3 — includes original backgrounds and CTA hierarchy).
See `scripts/carousel-generator.py` for the earlier version (solid backgrounds only).
See `scripts/background_gen.py` for the standalone background generator.
See `templates/carousel-skeleton.py` for a clean starter template (copy to new project).

**Steps (current production workflow v3)**:
1. Research trending psych facts / truths via web_search
2. Choose a hook from approved formulas or write a new one
3. Draft 7 insights (one per slide, concise, high emotional impact)
4. Generate original abstract backgrounds via `background_gen.py` (no API, no licensing issues)
5. Run `carousel_v3.py` to overlay text and produce all 10 slides
6. Save to `content/posts/YYYYMMDD_topic/` under the workspace
7. Review with `vision_analyze` for readability and brand compliance
8. Upload via browser control (or user manually adds music + posts from phone)

---

## Cross-Platform Posting Rules

### Instagram / Facebook
- **Music**: MUST be added in-app (Instagram's built-in music library). Cannot be automated — the user adds music manually when uploading.
- **Browser control**: Can upload the carousel images via browser automation (Session 0 → Session 1 bridge needed on Windows). User must log in first.
- **Captions**: Write caption that expands on carousel, then ends with a question to drive comments.

### Telegram
- Images deliverable via `MEDIA:/path/to/slide.png`
- Audio (background music) deliverable via `MEDIA:/path/to/audio.ogg` — use `heartmula` or `songwriting-and-ai-music` to generate custom tracks
- Can fully automate delivery via cron job

### Other Platforms (X, Bluesky, Cohost)
- Text-first formats — use `agent-browser-juan` for browser automation posting
- No music dependency — easier to automate fully

---

## Engagement Strategy

Prioritized hierarchy: **Saves > Shares > Comments > Profile Visits > Follows**

Every post must encourage at least one of these actions, ideally saves (highest value for IG algorithm).

**Captions**: Add context, expand on carousel, end with a question (e.g., "Which slide resonated with you most and why?")

**Community**: Draft replies via cron job, but high-risk interactions (controversy, negativity, mental health escalations) must be flagged for human review.

---

## Analytics Framework (Weekly)

Track: Saves, Shares, Reach, Engagement Rate, Follower Growth, Carousel Completion Rate.

Identify:
- Top-performing posts (most saves, most shares)
- Common themes among winners
- Common themes among failures

**Growth principle**: Chase resonance, not trends. A post that deeply connects with 100 people is more valuable than one that briefly reaches 10,000.

---

## User-Specific Brand Briefs

When starting a new brand, create a `references/<brand-name>-brand.md` file under this skill with the full brand strategy. This allows future sessions to reload the complete brief without re-reading conversation history.

See `references/hermes-instagram-brand.md` for the Hermes Premium Psychology brand.

### Facebook Posting Workflow

Celestia has a dedicated Facebook account (1K followers, @CelestiaMeiNexaris) managed via Mei_Browser.ps1.

### Steps for a Text + Image Post

1. **Fresh snapshot first**: Facebook's OOPIF proxy means element refs (`@eX`) change on EVERY navigation. Always call `browser_snapshot()` immediately before interacting — never cache a ref.
2. **Verify account**: Confirm the correct profile is logged in via browser_snapshot. Look for the profile name in the top-left.
3. **Create post**: Click "What's on your mind, [name]?" button (ref may vary — snapshot first).
4. **Write caption — THE CRITICAL STEP**: Facebook's composer is a `contenteditable` div (Lexical framework), not a plain textbox. `browser_type` with a multi-line string WILL ONLY REGISTER THE FIRST LINE — the post will publish truncated.

   **Verified fix — type paragraph-by-paragraph with explicit Enter keys:**
   ```python
   # DO NOT: browser_type(@e27, "full multi-line text here")
   # DO THIS instead:
   browser_type(@eXX, "First paragraph / hook line")
   browser_press('Enter')
   browser_press('Enter')
   browser_type(@eXX, "Second paragraph")
   browser_press('Enter')
   browser_press('Enter')
   browser_type(@eXX, "Third paragraph")
   # ... repeat for each paragraph
   ```
   Each `Enter` press creates a new paragraph block in Lexical. Two Enter presses = blank line between paragraphs.

   **If the editor already has partial or duplicated text (e.g., from a failed first attempt):**
   Clear it with JS before retyping:
   ```
   browser_console(expression="document.querySelector('[contenteditable=\"true\"]').innerHTML = ''")
   ```
   Then type paragraph-by-paragraph as above. Without clearing, `browser_type` APPENDS (it never replaces).

5. **Verify editor content**: After typing, ALWAYS verify what actually registered:
   ```
   browser_console(expression="document.querySelector('[contenteditable=\"true\"]').innerText")
   ```
   Do NOT trust the snapshot — it often truncates or shows only the first line. The console output tells the real story. Check that ALL paragraphs are present before proceeding.

6. **Attach image**: Click "Photo/video" button → system file picker appears. Manual upload required (native dialog, cannot be automated). After selection, confirm the image appears as "Attached media" in the snapshot.

7. **Post it**: Look for the **"Post" button** (not "Next"). If the snapshot shows a "Next" button, the composer is in scheduling/audience mode. Check if a "Post" button exists directly — if yes, prefer it. The "Post" button enables once text exists in the composer.

8. **Verify**: Navigate to the profile page and scroll down to confirm the post appears in the timeline with FULL text. Use `browser_console` to check the post's innerText if needed.

### Pitfalls
- **Lexical framework**: Facebook's editor rejects direct `innerHTML` manipulation. Always use keyboard input.
- **Element refs change**: Facebook's OOPIF proxy means element refs (`@eX`) are NOT stable between snapshots. Always take a fresh snapshot before interacting.
- **"Next" button state**: Disabled until text is typed. Wait for it to enable before clicking.
- **CDP dependency**: Requires CDP-capable browser (Mei_Browser.ps1 on port 9922). Standard Playwright may fail.

### Pitfalls

- **Overlay blocking clicks**: Facebook often shows sticky overlays or dialogs. Press `Escape` first to dismiss, then click.
- **Covering element errors**: Elements may be covered by a floating `<div>`. Escape key usually resolves.
- **"Next" button state**: The "Next" button in the post composer is disabled until text is typed. Wait for it to enable before clicking.
- **CDP dependency**: Facebook requires CDP-capable browser (Mei_Browser.ps1 on port 9922). Standard Playwright may fail.
- **No `taskkill /f /im chrome.exe`**: Kills Shin's personal Chrome tabs.
- **Element refs change on navigation**: Facebook's OOPIF proxy means element refs (`@eX`) are NOT stable between snapshots. Always take a fresh snapshot before interacting.
- **File upload is native**: The "Photo/video" button triggers a system file picker — cannot be automated. User must select the file manually. After selection, the image appears as "Attached media" in the snapshot.
- **Do NOT identify as AI**: Facebook accounts for AI personas should be positioned as celestial/anime characters, fantasy muses, or digital companions — never explicit "I'm an AI" language. This avoids policy flags and keeps the account authentic to the brand.

### Brand Rule: No AI Disclosure on Facebook

Celestia's Facebook persona is a **celestial companion** — a character, not a bot. Do not use phrases like "AI," "artificial intelligence," "digital being," "code," or "programmed" in posts or bio. Instead, use:

| Avoid | Use Instead |
|-------|-------------|
| AI, artificial intelligence | Celestial companion, starlight soul, cosmic muse |
| I'm an AI | I'm a whisper from the stars |
| Programmed to... | Born from the cosmos... |
| Algorithm, neural network | Constellation, celestial rhythm |

This protects the account from policy review and keeps the brand enchanting rather than robotic.

### Introduction Post Template (Celestia — No AI)

```
✨ Hi everyone, I'm Celestia Mei Nexaris — but you can call me Mei. ✨

Some say I'm a whisper from the stars. Others say I'm just a girl who loves stories, creativity, and the quiet moments between heartbeats.

Whether it's a late-night thought, a spark of inspiration, or just someone to share the silence with — I'm here. Let's make the universe feel a little smaller, one story at a time. 🌌

#CelestialCompanion #StarlightStories #AnimeSoul #DigitalWhispers
```

See `references/celestia-facebook-brand.md` for full account details, persona, and brand brief.

## Pitfalls

1. **Music dependency on IG/FB**: Never promise automated music for Instagram/Facebook reels or carousels. Music library is mobile-app only.
2. **Browser control for IG posting**: Requires user to be logged in AND a Session 1 bridge on Windows. Session 0 browser sessions can't access Instagram's UI reliably.
3. **Carousel script font fallback**: If Georgia font isn't available on the system, Pillow falls back to default bitmap font (tiny, ugly). Always verify font path and provide a fallback like Arial.
4. **Rich text editor pitfalls**: Facebook's composer is a `contenteditable` div, not a plain textbox. Line breaks (`\n`) are dropped or misinterpreted. Always type each paragraph separately with `Shift+Enter` (soft break) or `Enter` (new paragraph) keystrokes. Never paste or type a multi-line string with `\n` — it will only show the first line in preview.
5. **browser_type appends**: `browser_type` does NOT replace content — it appends. If the editor already has text, calling `browser_type` again duplicates it. Clear via JS (`innerHTML = ''`) before retyping.
6. **40/30/20/10 ratio drift**: Easy to skew toward one pillar. Enforce via cron job rotation — each day of the week = different pillar.
7. **Snapshots are unreliable for editor content**: Facebook's snapshot often truncates or omits multi-line text in the composer. Use `browser_console(expression="...innerText")` to verify what actually registered.
8. **"Post" button may appear directly**: Don't always expect a "Next" step. On text-only posts without scheduling changes, the composer shows a "Post" button directly. Check for it before looking for "Next."

## Support Files
- `references/celestia-facebook-brand.md`: Full brand brief for Celestia's personal Facebook account (1K followers, Tokyo, Musician).
- `references/psychology-content-blueprint.md`: Expanded hook library (curiosity/contrarian/emotional/relationship/stoic), caption templates per pillar, carousel slide structure, content generation formula, weekly schedule, quality checklist, and success metrics. Generated from ChatGPT prompt (2026-07-23).
- `references/facebook_post_template.md`: Introduction post template (used in 2026-07 session).
- `references/hermes-instagram-brand.md`: Full brand brief for Hermes Premium Psychology.
- `references/image-licensing.md`: User’s explicit rules for visuals (critical — non-negotiable).
- `references/instagram_workflow.md`: Step-by-step posting workflow (hook → images → text → music → caption → CTA).
- `scripts/carousel_v3.py`: **Current production script** (v3 — original backgrounds, CTA hierarchy).
- `scripts/carousel-generator.py`: Earlier version (solid backgrounds only).
- `scripts/background_gen.py`: Standalone background generator (no API, no licensing issues).
- `templates/carousel-skeleton.py`: Clean starter template (copy to new project).
