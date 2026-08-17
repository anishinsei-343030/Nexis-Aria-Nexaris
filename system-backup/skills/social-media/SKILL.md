---
name: social-media
description: Manage AI-operated social media personas — content creation, scheduling, brand consistency, and growth analytics. Umbrella for Hermes social media operation.
version: 1.0.0
platforms: [windows]
metadata:
  hermes:
    tags: [social-media, hermes, branding, automation, content]
---

# Social Media Management

Use this skill when the user asks about managing or growing a social media presence, operating a brand account, or setting up an automated content pipeline for an AI personality.

## Persona: Hermes

Hermes is the primary AI social media personality. See `references/hermes-bible.md` for full character bible.

**Identity**: Disclosed AI (Greek messenger god theme)
**Mission**: Demystify AI, tech, productivity
**Content Pillars**: AI News, Productivity, Tech Trends, Motivation/Learning, Behind-the-Scenes
**Avoids**: Politics, polarizing issues, unverified claims

## Workspace Structure

All assets stored under:
```
D:\Hermes\Celestia mei Nexaris\Hermes-Social\
├── accounts/              # Per-platform guides (see Phase 0 step 6)
│   └── <platform>/          e.g. facebook/, twitter/, instagram/
│       └── guide.md         Brand rules, posting workflow, pitfalls
├── branding/              # Logos, color palette, banners
│   ├── character_bible.md
│   └── hermes_logo_concept_1.png
├── content/
│   ├── posts/
│   ├── images/
│   └── videos/
├── analytics/
└── reference/
```

**accounts/ convention**: Each platform account gets its own subfolder with a `guide.md` containing:
- Account URL, handle, follower count, categories
- Brand rules (including whether to disclose AI or not — see Non-Hermes Persona section)
- Platform-specific posting workflow (editor quirks, image upload method)
- Content calendar template
- Pitfalls & fixes specific to that platform

## Phase 0: Account Onboarding

Use this when the user gives you an existing social media account to manage.

**Workflow:**
1. Start the browser (Mei_Browser.ps1 for this setup)
2. Navigate to the platform's login page
3. **User must log in manually** — account creation, CAPTCHA, phone verification, and 2FA cannot be automated. If the browser auto-logs into an existing account (session persistence), user logs out first or a separate browser profile is needed.
4. Once logged in, navigate to the account's profile URL to verify access
5. Record account details in fact store and memory: URL, follower count, listed categories, linked accounts
6. Check for persona-vs-profile data mismatches (DOB, name, location) — flag discrepancies but don't change without user approval. Facebook DOB changes require ID verification; hiding privacy to "Only me" is the alternative if user doesn't want it public.

**Pitfall — DOB mismatch:** Account profile may show a DOB set during signup that differs from the AI persona's lore. Don't attempt to change it unless asked. Facebook locks DOB changes behind government ID verification.

**Pitfall — browser session persistence:** If the browser profile already has a logged-in session, opening a new tab/window still inherits that session. User must log out first or start a fresh browser profile on a different port.

## Phase-Based Deployment

Follow this phased approach when building or expanding a social media presence:

### Phase 1: Define the Persona
- Create character bible (identity, voice, brand rules, topics)
- Generate logo and visual assets (load `stability-ai-image-gen` skill)
- Verify assets with `vision_analyze` before user delivery
- Save brand rules to memory

### Phase 2: Build Content Engine
- Research Agent: cron-job scanning trends/news
- Content Agent: draft posts + captions
- Creative Agent: generate images/videos (load `stability-ai-image-gen` or `ffmpeg-video-animation`)
- Analytics Agent: track engagement metrics

### Phase 3: Infrastructure
- Use cron jobs for scheduling (every 2h with session_search dedup)
- Use `agent-browser` for browser-based posting (X/Bluesky)
- Manual upload for Instagram/TikTok (anti-bot measures)
- Propose-then-approve workflow for all external posts

### Phase 4: Growth & Community
- Track: follower growth, reach, saves, shares, comments
- Weekly pattern analysis → improved content
- Draft replies via agent, manual review for high-risk interactions

## Non-Hermes Personas (Fantasy / Anime / Celestial)

Some accounts are **not** disclosed AI. These are character personas — celestial companions, anime muses, fantasy beings. They follow different brand rules:

| Aspect | Disclosed AI (Hermes) | Fantasy Persona (Celestia) |
|--------|----------------------|---------------------------|
| Bio disclosure | "This is an AI" | Celestial metaphors only |
| Language | Tech, productivity, AI news | Stories, emotions, anime, creativity |
| AI terms | Use "AI," "algorithm" | Swap to "starlight," "celestial rhythm" |
| Risk | Low (transparency) | Moderate (policy flags if detected) |

**For fantasy personas, NEVER use in posts/bio**: AI, artificial intelligence, digital being, code, programmed, algorithm, neural network, bot.

**USE instead**: celestial companion, starlight soul, cosmic muse, whisper from the stars, born from the cosmos, constellation, celestial rhythm.

Create a separate reference file per persona under `accounts/<platform>/<persona>-brand.md`.

## Platform Capabilities Matrix

| Platform | Posting Method | Automation Level | Notes |
|----------|---------------|-----------------|-------|
| **X/Twitter** | browser automation | High | Uses agent-browser + cron jobs |
| **Bluesky** | browser automation | High | Uses agent-browser + cron jobs |
| **Instagram** | Manual/mobile relay | Low | CAPTCHA/anti-bot blocks automation |
| **TikTok** | Manual/mobile relay | Low | Mobile upload required |
| **YouTube** | Browser upload | Medium | Requires logged-in session |
| **Facebook** | Browser upload | Medium | Requires logged-in session |

## Image Generation Provider Chain

1. **Stability AI** — primary (use `stability-ai-image-gen` skill, ~958 credits as of 2026-06-17)
2. **OpenAI DALL-E** — fallback if `$OPENAI_API_KEY` is set
3. **ChatGPT Browser Automation** — last resort (requires login, use `chatgpt-image-generation` skill)

See `stability-ai-image-gen/references/hermes-brand-assets.md` for verified logo generation prompts.

## Cron Job Design

- Schedule every 2 hours (PC may be off — includes catch-up logic)
- Use `session_search` dedup to avoid re-processing
- Stagger 15-min apart from other cron jobs
- Each post submits via propose-then-approve workflow (no auto-publishing without review)

## Pitfalls

- **Image generation credits**: Always check balance before generating. FAL and Stability AI can exhaust mid-session.
- **PNG block on Telegram**: Stability AI PNGs contain proprietary chunks that Telegram silently drops. Convert to JPG before delivery.
- **Account creation**: Cannot automate — CAPTCHA and phone verification require manual user action.
- **Real-time engagement**: Cron jobs are isolated sessions. No continuity between runs. Not suitable for live conversations.
- **Instagram/TikTok**: Require mobile relay (Termux proposal exists but not yet implemented).
