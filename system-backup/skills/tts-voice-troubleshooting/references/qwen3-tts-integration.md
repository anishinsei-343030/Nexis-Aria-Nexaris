# Local TTS (Chatterbox-Nano) Reference

## Overview
The local Chatterbox-Nano TTS is the **primary** TTS provider for this profile (`mei-kokoclone` in `~/.hermes/config.yaml`). It runs fully on-device:
- **No quota, no API keys, no cloud dependency**
- **English only**
- CPU-bound: ~10-30s per generation

---

## Stack

```
config.yaml mei-kokoclone (type: command)
  → "D:\DevTools\tts\.venv\Scripts\python.exe" "D:\DevTools\tts\hermes_tts.py"
      --input-file {input_path} --output {output_path} --ref <voice>
  → D:\DevTools\tts\tts_generate.py (Chatterbox-Nano, CPU)
  → refs: D:\DevTools\tts\ref_yui.wav | ref_mei.wav | ref_nexis.wav
```

## Requirements

- The venv **must** be Python 3.11 (torch 2.6.0 has no Python 3.14 wheels).
- Rebuild if broken:
  ```
  uv venv D:\DevTools\tts\.venv --python 3.11
  uv pip install --python "D:\DevTools\tts\.venv\Scripts\python.exe" "chatterbox-tts @ git+https://github.com/resemble-ai/chatterbox.git"
  ```
- The bridge (`tts_generate.py`) refuses to run under the wrong Python with a clear error.

## Manual Test

```
"D:\DevTools\tts\.venv\Scripts\python.exe" "D:\DevTools\tts\hermes_tts.py" --text "Hello" --output C:\Users\Administrator\.hermes\audio_cache\test.wav --ref mei
```

## Pitfalls

- **Do NOT switch to qwen3tts / cloud TTS providers** — they are dead/deprecated. Local TTS is the intended setup.
- **Voice refs are wav clones of Shin's samples** — keep them in `D:\DevTools\tts\`.
- **Parallel TTS calls** overwhelm the CPU — avoid.
- **Tilde (~)** breaks pronunciation — strip from TTS text.
