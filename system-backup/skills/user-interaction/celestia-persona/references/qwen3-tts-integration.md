# Local TTS Integration (Chatterbox-Nano)

## Provider Details

- **Provider Name in Hermes Config:** `mei-kokoclone`
- **Backend:** Local Chatterbox-Nano (CPU) — no cloud, no API key, no quota
- **Bridge:** `D:\DevTools\tts\hermes_tts.py` → `D:\DevTools\tts\tts_generate.py`
- **Voice Type:** Custom cloned voice (cloned from Shin's samples, ref `D:\DevTools\tts\ref_mei.wav`)

## Known Constraints

- **Speed control:** available via `--rate` (default 0.9 = slightly slower).
- **No tilde (~)** — causes garbled pronunciation. Strip all tildes from TTS input.
- **English-only for voice output.** Japanese romaji through English TTS sounds terrible — disabled. Japanese text ok for on-screen captions only.
- **CPU-bound:** ~10-30s per reply. Do not issue parallel TTS calls.

## Usage

```python
# text_to_speech tool handles this automatically
# Just pass text, the provider "mei-kokoclone" is configured as default
text_to_speech(text="Your text here")
```

## Voice-First Default

- Default ALL replies to voice.
- Fallback to text only on command failure (no quota concept — failures are transient).
- Retry voice on the next user message.

## Migration Notes

Replaced Qwen3-TTS / ElevenLabs as primary provider (both dead/deprecated). Local TTS offers:
- No quota, no API keys, fully offline
- Custom cloned voice for persona consistency
- Speed control via `--rate`
- If the venv breaks: rebuild with Python 3.11 (`uv venv D:\DevTools\tts\.venv --python 3.11`) and reinstall chatterbox from git master
