# Psychology Voice Workflow

## Overview
Dedicated workflow for psychology-related voice experiments, TTS audio, and content creation. All files related to the "Psychology Voice" topic go in:

```
D:\Hermes\Celestia mei Nexaris\psychology-voice\
```

## Folder Structure

```
psychology-voice/
├── tts_audio/            # Generated TTS audio files (.ogg, .mp3)
├── scripts/              # PowerShell/Python scripts for automation
├── notes/                # Session notes, research, and insights
├── experiments/          # Experimental setups and results
└── psychology-facts.md   # Curated list of psychology facts for TTS
```

## TTS Guidelines

### Content
- **Short and Punchy**: One-line psychology facts, insights, or thought-provoking statements.
- **Emotional Tone**: Warm, curious, and engaging. Avoid clinical or robotic delivery.
- **Examples**:
  - "People are more likely to remember something if they fail to complete it. It's called the Zeigarnik effect."
  - "Your brain treats rejection like physical pain. That's why heartbreak hurts so much."

### Technical
- **Tool**: `text_to_speech` with `mei-kokoclone` voice.
- **Output**: `.ogg` format, saved to `psychology-voice/tts_audio/`.
- **Delivery**: Use `MEDIA:` tag to send audio to the user.

## Workflow Steps

1. **Generate Fact**:
   - Source a short psychology fact or insight.
   - Ensure it fits the emotional tone and length guidelines.

2. **Generate TTS Audio**:
   ```python
   text_to_speech(text="<fact>", output_path="D:\\Hermes\Celestia mei Nexaris\\psychology-voice\\tts_audio\\<timestamp>.ogg")
   ```

3. **Save Fact**:
   - Append the fact to `psychology-facts.md` in the `psychology-voice/` folder.
   - Include source (if applicable) and timestamp.

4. **Deliver Audio**:
   - Send the audio file to the user using `MEDIA:` tag.
   - Example:
     ```
     MEDIA:D:\\Hermes\Celestia mei Nexaris\\psychology-voice\\tts_audio\\<timestamp>.ogg
     ```

5. **Organize Files**:
   - Move any related scripts, notes, or experiments to the appropriate subfolder.

## Pitfalls

- **File Paths**: Always verify the `psychology-voice/` folder exists before saving files.
- **TTS Quota**: Monitor TTS character usage to avoid hitting API limits.
- **Content Tone**: Ensure facts are engaging and not overly technical.
- **Workspace Clutter**: Never save psychology-related files outside the `psychology-voice/` folder.