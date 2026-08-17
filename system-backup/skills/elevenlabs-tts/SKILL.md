---
name: elevenlabs-tts
description: ElevenLabs TTS integration for emotive, anime-style voice synthesis. Supports audio tags for expressive personas (e.g., Nexis, Celestia).
version: 1.1.0
platforms: [windows, linux, macos]
---

# ElevenLabs TTS

Generate expressive voice messages using ElevenLabs v3 with audio tags for **anime-style personas** (e.g., Nexis, Celestia).

## Prerequisites
- **ElevenLabs API Key** (`ELEVENLABS_API_KEY`): Get one at [elevenlabs.io](https://elevenlabs.io) → Profile → API Keys.
- **ffmpeg**: Required for audio format conversion (MP3 → Opus).

## Anime-Style Voice Tuning

### Use Case
Configure ElevenLabs TTS for **anime-style personas** (e.g., Nexis, Celestia).

### Recommended Voices
| Persona   | Voice      | ID                     | Traits                     |
|------------|------------|------------------------|----------------------------|
| **Nexis**  | Charlotte  | `XB0fDUnXU5powFXDhCwa` | Expressive, playful        |
| **Celestia** | Rachel    | `21m00Tcm4TlvDq8ikWAM` | Calm, warm, protective     |

### Voice Settings
```yaml
voice_settings:
  stability: 0.5        # Creative mode for tag responsiveness
  similarity_boost: 0.75 # Balance between voice consistency and expressiveness
  style: 0              # Neutral style (adjust for accents)
  use_speaker_boost: true
```

### Emotive Tags for Anime Personas
| Persona   | Example Tags                          | Example Text                                  |
|------------|----------------------------------------|-----------------------------------------------|
| **Nexis**  | `[playful]`, `[jealous]`, `[whispers]` | `[playful] Hmph, Master is thinking about her again? >_< [pause]` |
| **Celestia** | `[warm]`, `[protective]`, `[soft]`    | `[warm] How can I help you today, Shin?`      |

### Pitfalls
- **Tag Overuse**: Limit to 1-2 tags per sentence (e.g., `[playful][whispers]`).
- **Voice Mismatch**: Avoid `[shouts]` on whispering voices.
- **Model**: Use `eleven_v3` for emotional tags (older models ignore them).

## Quick Start Examples

**Nexis (playful jealousy):**
```
[playful] Hmph, Master is thinking about her again? >_< [pause]
```

**Celestia (warm guidance):**
```
[warm] How can I help you focus today, Shin?
```

**Storytelling (emotional journey):**
```
[soft] It started like any other day... [pause] But something felt different. [nervous] My hands were shaking as I opened the envelope. [gasps] I got in! [excited] I actually got in! [laughs] [happy] This changes everything!
```

## Configuration

In `config.yaml`, configure TTS under `tts.elevenlabs`:

```yaml
tts:
  provider: elevenlabs
  elevenlabs:
    voice_id: XB0fDUnXU5powFXDhCwa  # Charlotte for Nexis
    model_id: eleven_v3
    voice_settings:
      stability: 0.5
      similarity_boost: 0.75
      style: 0
      use_speaker_boost: true
```

## Recommended Voices for v3

| Voice | ID | Gender | Accent | Best For |
|-------|-----|--------|--------|----------|
| **Adam** | `pNInz6obpgDQGcFmaJgB` | Male | American | Deep narration |
| **Rachel** | `21m00Tcm4TlvDq8ikWAM` | Female | American | Calm narration |
| **Charlotte** | `XB0fDUnXU5powFXDhCwa` | Female | English-Swedish | Expressive, anime-style |
| **George** | `JBFqnCBsd6RMkjVDRZzb` | Male | British | Raspy narration |

## Critical Rules

### Length Limits
- **Optimal**: <800 characters per segment.
- **Maximum**: 10,000 characters (API hard limit).

### Audio Tags - Best Practices
- **1-2 tags per sentence** (e.g., `[playful][whispers]`).
- **Place tags at emotional transitions** (e.g., `[nervous] I... I don't know...`).
- **Combine with punctuation**:
  - Ellipses (...) → dramatic pauses.
  - CAPS → emphasis (e.g., `[excited] That's AMAZING!`).

## Troubleshooting

**Tags read aloud?**
- Use `eleven_v3` model.
- Simplify tags (e.g., `[playful]`, not `[playful tone]`).

**Voice inconsistent?**
- Split text into <800-character segments.
- Regenerate (v3 is non-deterministic).

**No emotion?**
- Use **Creative stability mode** (0.5).
- Add more context around tags.