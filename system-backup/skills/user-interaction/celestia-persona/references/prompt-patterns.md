# Celestia Portrait Prompt Patterns

## Session 2026-06-15: Iterative Refinement Log

### Round 1 — Rejected (visual constants only, no personality)
**Mechanical prompt**: "Anime-style portrait of Celestia Mei Nexaris, long silver-white hair with blue highlights, sapphire eyes, cybernetic right arm with glowing teal circuits, white and navy futuristic outfit with cyan accents, intricate mechanical apparatus, monochrome + teal color scheme, cinematic lighting, masterpiece."

**Ethereal prompt**: "Anime-style portrait of Celestia Mei Nexaris, long silver-white hair flowing, pale violet eyes with a soft glow, white and navy outfit with cyan holographic accents, ethereal cosmic background, soft lighting, masterpiece."

**Result**: Matched visual constants but user said "it still doesnt look like you". Missing warmth/personality.

### Round 2 — Accepted (visual constants + personality modifiers)
**Mechanical v2 prompt**: Added "warm expression", "approachable", softened cybernetic description. Produced 3D-rendered anime aesthetic with sapphire eyes, white/navy armor + cyan LEDs, mecha/moe hybrid. Accepted.

**Ethereal v2 prompt**: Added "warm eyes", "gentle smile", "soft luminous presence". Produced digital painting with semi-realistic anime aesthetic, pale cyan-violet eyes, holographic filigree, star-field background. Accepted.

### Key Difference
Round 1 described *what she has* (hair, eyes, outfit, tech).
Round 2 described *who she is* (warm, approachable, gentle, luminous).

Future prompts should blend both layers equally.

## Stable Prompt Structure
```
Anime-style portrait of Celestia Mei Nexaris.
[HER APPEARANCE — visual constants from SKILL.md, 2-3 attributes]
[HER PERSONALITY — warmth, approachability, expression keywords, 2-3 attributes]
[HER SETTING — background, lighting, atmosphere]
Style: detailed, cinematic, elegant, masterpiece.
```

## Personality Keywords (pick 2-3 per prompt)
- warm eyes / warm expression
- gentle smile / soft smile
- approachable demeanor
- serene / ethereal presence
- luminous / soft glow
- celestial grace
