# Game Boy Garden — Proven Example (2026-08-15 session)

Context: Nexis + Celestia group-chat pixel art session. FAL credits exhausted,
`execute_code` blocked at the consent gate. Delivered 100% in-chat ASCII. This
is the known-good reference design.

## Single Flower (daisy) — 14 wide × 10 tall, Game Boy palette

```text
      ▒▒▒
     ▒▒▓▓▒▒
    ▒▓▓██▓▓▒
    ▓█████▓▒
    ▓█████▓▒
    ▒▓▓██▓▓▒
     ▒▒▓▓▒▒
       ▓▓
       ▓▓
```

- `█` = #0F380F (darkest) — petal centers
- `▓` = #306230 — inner petal ring
- `▒` = #8BAC0F — outer petal ring
- space = #9BBC0F (lightest, background)

## Three-Flower Garden — side-by-side row (32 chars wide)

```text
      ▒▒▒        ▒▒        ▒▒▒▒
     ▒▒▓▓▒▒     ▒▓▓▒      ▒▓▓▓▒
    ▒▓▓██▓▓▒   ▒▓██▓▒    ▒▓██▓▓▒
    ▓█████▓▒   ▒▓██▓▒    ▒▓██▓▓▒
    ▒▓▓██▓▓▒    ▒▓▓▒     ▒▓▓▓▓▒
     ▒▒▓▓▒▒      ▓▓        ▒▒▒▒
       ▓▓        ▓▓         ▓▓
       ▓▓        ▓▓         ▓▓
```

Left = daisy (full bloom), center = tulip (cup shape), right = smaller bloom
(bud). All three share the same 4-shade palette; row alignment kept by padding
each column to equal height.

## Design Notes

- Stems are 2px (`▓▓`) columns; keep them 2-wide so they don't vanish at chat
  font sizes.
- Tulip: `▒▓██▓▒` top row reads as the classic tulip cup. Bloom center sits at
  column 2 (`▒▓██▓▓▒`) for a closed-petal look.
- 32-char row is the hard ceiling for mobile Telegram rendering; the 3-flower
  garden exactly fills it.
