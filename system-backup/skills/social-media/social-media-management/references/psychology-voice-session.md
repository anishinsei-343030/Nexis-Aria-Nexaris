# Psychology Voice Session — 2026-06-30

## Context
- **Topic**: Psychology Voice (Telegram topic ID 49)
- **User**: AniShin Sei (Shin)
- **Agent**: Celestia Mei Nexaris
- **Goal**: Set up a dedicated folder and voice system for bilingual psychology content

## Session Summary

### 1. Folder Setup
- Created: `D:\Celestia Mei Nexaris\Workspace\Psychology Voice\`
- Moved existing psychology files into topic folder:
  - `psychology-full-scripts.md`
  - `psychology-visual-concepts.md`
  - `psychology-sample-scripts.md`
  - `psychology-content-plan.md`
- **Rule**: All files from this Telegram topic go here

### 2. Voice System Update
- **New rule**: Japanese → romaji for English TTS
- Created `voice-system.md` documenting:
  - Default language: English
  - Japanese support: romaji conversion when requested
  - Examples:
    - こんにちは → Konnichiwa
    - ありがとうございます → Arigatou gozaimasu
  - Reason: English-only TTS workaround

### 3. Script Updates
- **Target**: TTS audio columns in psychology scripts
- **Action**: Convert all Japanese in TTS columns to romaji
- **Files updated**:
  - `psychology-full-scripts.md`
  - `psychology-sample-scripts.md`
- **Example conversion**:
  - Before: `「先延ばしは感情の問題。Name the feeling first。」`
  - After: `"Saki nobashi wa kanjou no mondai. Name the feeling first."`

### 4. Visual Display
- **No change**: Japanese in captions, graphics, subtitles, and visual text left as-is
- **Rationale**: Visual display uses Japanese characters; only TTS audio needs romaji

## Romaji Conversion Table (Session-Specific)

| Japanese | Romaji | Context |
|----------|--------|---------|
| 先延ばしは感情の問題 | Saki nobashi wa kanjou no mondai | Procrastination script |
| 境界線を引く勇気 | Kyoukaisen wo hiku yuuki | Boundaries script |
| 大人になるって、感情をどう扱うか | Otona ni naru tte, kanjou wo do atsukau ka | Emotional maturity script |
| 知ってる痛みの方が安心する | Shitteru itami no hou ga anshin suru | Toxic dynamics script |
| 信頼は言葉より行動 | Shinrai wa kotoba yori koudou | Trust script |
| 修復の技術 | Shuufuku no gijutsu | Repair script |
| コントロールできるものだけに集中 | Control dekiru mono dake ni shuuchuu | Stoicism script |
| 苦しみのほとんどは、想像の中 | Kurushimi no hotondo wa, souzou no naka | Stoicism script |
| 死を忘れるな | Shi wo wasureruna | Memento Mori script |
| 成長は、孤独を感じるものだよね | Seichou wa, kodoku wo kanjiru mono da yo ne | Growth script |
| 昔の自分が必要としていたものを、手放す勇気 | Mukashi no jibun ga hitsuyou to shiteita mono wo, tebanasu yuuki | Growth script |
| 不安型と回避型はなぜか惹かれ合う | Fuangangata to kaihigata wa, nazeka hikare au | Attachment styles script |
| コメントで教えてね | Comment de oshiete ne | CTA script |

## Tools Used
- `terminal` — folder creation, file moves
- `write_file` — `voice-system.md` creation
- `patch` — script updates
- `memory` — workspace rule update

## Outcome
- **Topic folder**: All psychology voice files in one place
- **Voice system**: Documented romaji rule for Japanese TTS
- **Scripts**: All TTS audio columns use romaji; visual display unchanged
- **Ready for**: TTS audio generation, content production

## Follow-Up
- Generate TTS audio for updated scripts
- Create visual assets (carousels, reels)
- Schedule content posting