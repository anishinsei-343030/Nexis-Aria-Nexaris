---
name: tts-voice-troubleshooting
version: 1.1.0
platforms: [linux, macos, windows]
description: Troubleshoot issues with Text-to-Speech (TTS) voice configuration, including provider fallbacks and voice cloning.
category: software-development
---

# TTS Voice Troubleshooting

This skill outlines the steps to diagnose and fix issues related to Text-to-Speech (TTS) voice configuration, particularly when the desired voice is not being used despite attempting to update it.

## 1. Verify Configuration File (`config.yaml`)

The primary source of truth for TTS voice configuration is the `~/.hermes/config.yaml` file. Always check this file first.

**Steps:**
1. **Search for 'tts' section:**
   `search_files(path="~/.hermes/config.yaml", pattern="tts", output_mode="content")`
2. **Read the relevant section:**
   `read_file(path="~/.hermes/config.yaml", offset=<line_number_of_tts_section>, limit=<number_of_lines>)`
   (Adjust `offset` and `limit` based on search results).

## 2. Update Voice ID

If the `voice_id` in `config.yaml` is incorrect, use the `patch` tool to update it.

**Command Example (for ElevenLabs):**
```python
default_api.patch(
    path="~/.hermes/config.yaml",
    old_string="    voice_id: <OLD_VOICE_ID>",
    new_string="    voice_id: <NEW_VOICE_ID>"
)
```
Replace `<OLD_VOICE_ID>` and `<NEW_VOICE_ID>` with the actual IDs. Ensure to include the correct indentation for `voice_id`.

## 3. Avoid Patching Binary Audio Files (Pitfall)

**Pitfall:** Attempting to use the `patch` tool on generated audio files (e.g., `.mp3`, `.ogg`) to change voice settings will fail. These are binary files and cannot be modified as text.

**Correction:** Always target the `~/.hermes/config.yaml` file for voice configuration changes.

## 4. Test the New Voice

After updating `config.yaml`, perform a `text_to_speech` call to verify the new voice is being used.

**Command Example:**
`default_api.text_to_speech(text="Now I'm using the new voice ID! Can you hear the difference?")`

## 5. Restart Hermes (if necessary)

If changes to `config.yaml` don't immediately take effect, a restart of the Hermes agent or gateway might be necessary. This can be done via the `/restart` slash command in a gateway session, or by exiting and relaunching the CLI.

## 6. Quota Exceeded Errors (ElevenLabs)

**Issue:** TTS generation fails with `quota_exceeded` error from ElevenLabs.

**Example Error:** `TTS generation failed (elevenlabs): status_code: 401, body: {'detail': {'type': 'invalid_request', 'code': 'quota_exceeded', 'message': 'This request exceeds your quota...`

**Diagnosis:** This indicates a limit has been reached on the ElevenLabs API key. It is not a configuration issue within Hermes.

**Resolution:**
1. **Check ElevenLabs Account:** Verify your current plan and usage on the ElevenLabs website.
2. **Manage API Key Usage:** Reduce TTS requests or upgrade your ElevenLabs plan.
3. **Contact ElevenLabs Support:** If the issue persists despite sufficient quota, contact ElevenLabs support.
4. **Fallback Provider:** The local provider (`mei-kokoclone` → Chatterbox-Nano) has no quota. If it fails, check the venv/scripts (see section 7).

---

## 7. Local TTS (Chatterbox-Nano) Troubleshooting

The primary TTS provider for this profile is **local Chatterbox-Nano** (`mei-kokoclone` in `~/.hermes/config.yaml`), a fully local CPU voice clone. It has no API, no quota, and no cloud dependency. English only.

### Stack
- Config provider: `tts.providers.mei-kokoclone` → `"D:\DevTools\tts\.venv\Scripts\python.exe" "D:\DevTools\tts\hermes_tts.py" --input-file {input_path} --output {output_path} --ref <voice>`
- Bridge script: `D:\DevTools\tts\hermes_tts.py` → `D:\DevTools\tts\tts_generate.py` (Chatterbox-Nano model, CPU)
- Voice refs: `ref_yui.wav`, `ref_mei.wav`, `ref_nexis.wav` in `D:\DevTools\tts\`
- The venv MUST be Python 3.11 (torch 2.6.0 does not support 3.14). If an agent recreated the venv with 3.14, rebuild: `uv venv D:\DevTools\tts\.venv --python 3.11`

### Common Failures
1. **"Wrong Python in .venv (expected 3.11)"** — the venv was recreated with Python 3.14. Rebuild per the stack note above.
2. **Command error / exit 1 with path not found** — check the `command` path in `config.yaml` points at the existing `D:\DevTools\tts\` scripts.
3. **Slow generation (10-30s per reply)** — normal for CPU. Generation is single-threaded; don't trigger parallel TTS calls.
4. **`hermes_tts.py` CLI is strict** — flags: `--input-file` OR `--text`, `--output` (REQUIRED), `--ref` (default `mei`). There is NO `--rate` flag on this script. Ref keys: `yui`, `mei`, `nexis`, or a `.wav` path — the provider name `mei-kokoclone` is NOT a valid ref.
5. **Git-bash path mangling** — unquoted Windows paths lose backslashes (`D:\DevTools\tts\hermes_tts.py` becomes `D:DevToolsttshermes_tts.py`). Quote the path or use forward slashes when testing the bridge from the terminal.

### Fix Approach
1. Verify `config.yaml` `tts.provider: mei-kokoclone` and the command path exists.
2. Test the bridge directly:
   `"D:\DevTools\tts\.venv\Scripts\python.exe" "D:\DevTools\tts\hermes_tts.py" --text "test" --output C:\Users\Administrator\.hermes\audio_cache\test.wav --ref mei`
3. If the venv is broken, rebuild it (stack note above) and reinstall chatterbox from git master.
4. **Do NOT switch the provider to qwen3tts or any cloud TTS** — local TTS is the intended setup; cloud providers are dead/deprecated.
5. **User fix, no agent edits** — when Shin says "leave it, I'll fix it myself" or "no edits", STOP. Do not modify config, scripts, or venv. The user is actively repairing TTS; agent edits collide with theirs. Voice-first rule stands — when TTS recovers, resume `text_to_speech` calls without re-testing via terminal.

---

## 9. Telegram Voice Delivery: OGG Required for Inline Playback

### Problem
Telegram **only plays `.ogg` (Opus) files inline as voice bubbles**. WAV/MP3 files delivered via `MEDIA:` always land as downloadable attachments — users must tap to download, then play externally.

### Root Cause (observed 2026-08-18, AgriQuizBot)
The daily/reminder cron jobs generate `.wav` via `hermes_tts.py` and deliver with `MEDIA:D:/Hermes/.../voice/daily_YYYYMMDD.wav`. In the Pre-Board Exam supergroup this renders as a file attachment, not a playable voice bubble. FFmpeg is available on the host (`ffmpeg` on PATH).

### Fix
| Approach | Where | Change |
|---|---|---|
| A | `hermes_tts.py` | Add format detection: if `--output` ends with `.ogg`, FFmpeg-convert the generated WAV → OGG (Opus) and delete the WAV. |
| B | Cron prompts | Change `--output ...daily_YYYYMMDD.wav` → `...daily_YYYYMMDD.ogg` and update `MEDIA:` paths to match. |

Do **A + B**: keep conversion logic in the bridge (one place), flip the cron prompts to `.ogg`. Future TTS callers get OGG for free.

**PITFALL — agent cannot apply Approach A itself (2026-08-18):** the write guardrail blocks `write_file` AND `patch` on `D:\DevTools\tts\hermes_tts.py` — it is outside the managed workspace (`D:\Hermes\Nexis Aria Nexaris`), and explicit chat approval ("proceed"/"confirm") does NOT reach the gate. Machine-side consent (whitelisting the path) is required. Until then: hand Shin the exact diff/commands and let him apply the edit manually. Do NOT loop retrying writes to that path — every attempt returns the same guardrail error.

### FFmpeg sketch (append to `hermes_tts.py` after WAV generation)
```python
if Path(args.output).suffix.lower() == ".ogg":
    wav_path = Path(args.output).with_suffix(".wav")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(wav_path),
        "-c:a", "libopus", "-b:a", "16k", "-ac", "1", args.output
    ], check=True)
    wav_path.unlink(missing_ok=True)
```

### Verification
Voice note appears as a playable bubble in the Telegram group; no download required. If it still lands as an attachment, check the file extension is truly `.ogg` and the codec is Opus (`ffprobe`), not a renamed WAV.

---

## 8. Persona Voice Tuning

This section covers selecting, configuring, and refining the TTS voice to ensure it aligns with a specific persona's identity (e.g., a youthful anime-style companion).

### Workflow

1. **Update Voice ID** — Locate the provider section in `~/.hermes/config.yaml`. For ElevenLabs, update `tts.elevenlabs.voice_id`. Example: `voice_id: UkrrIoyyjkEUg8csTdB6`
2. **Verification** — Immediately trigger a `text_to_speech` call to verify the identity. Listen for characteristics like age, tone, and gender.
3. **Tuning Cadence and Emotion**:
   - **Provider-Side Tuning**: For providers like ElevenLabs, parameters such as **Stability**, **Clarity + Similarity Enhancement**, and **Style Exaggeration** must be adjusted directly in the provider's dashboard (e.g., Voice Lab).
   - **Config-Side Tuning**: Use `voice.silence_duration` in `config.yaml` to adjust pauses between segments.
   - **Prompt-Based Pacing**: Use punctuation as a steer. Ellipses (`...`) and strategic breaks can encourage the model to slow down and add emotional weight.

### User Preferences

- **Brief Responses**: Use voice output (TTS) for brief, simple replies.
- **Complex Responses**: Use text for longer, detailed, or technical explanations.
- **Persona Alignment**: The voice must match the persona's description (e.g., sweet, youthful, affectionate).

### Pitfalls
- **Speed Issues**: Speaking speed is often baked into the voice design or controlled via provider-side sliders. Adjusting `config.yaml` is usually insufficient.
- **Config Caching**: Changes to `config.yaml` regarding TTS providers may require a session reset (`/reset`) or gateway restart.
- **Binary Files**: Never attempt to use `patch` or `write_file` on generated `.mp3` or `.ogg` audio files.

### References
- [ElevenLabs Voice Quirks](references/elevenlabs-quirks.md): Provider-specific tuning notes.