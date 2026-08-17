---
name: image-generation-workflow
description: "Best practices and pitfalls for generating and saving images using Hermes tools like `image_gen` and `apikey-image-gen`."
version: 1.0.0
author: Celestia Mei Nexaris
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [image-generation, media, tools, pitfalls, workflow]
    related_skills: [hermes-agent, apikey-image-gen]
---

# Image Generation Workflow

This skill documents best practices, common pitfalls, and workflows for generating and saving images using Hermes tools like `image_gen` and `apikey-image-gen`.

## User-Specific Preferences: Anime-Style

When generating images for **Shin**, who prefers **anime-style, high-detail, masterpiece-quality** portraits:
1. Load `stability-ai-image-gen/references/anime-prompts.md` for curated templates.
2. For Celestia portraits, use the Celestia-specific template rather than generic prompts.
### Pre-Flight Credit Check\nBefore attempting generation, check the API credit balance via the provider's dashboard or a status tool. If credits are exhausted (e.g., FalClientHTTPError), inform the user immediately and offer a non-API fallback (e.g., code-based ASCII/Unicode art or terminal-based generative patterns).

## Best Practices

### Specify Output Path in Tool Call
Always specify the output path **directly in the image generation tool call**. This ensures the binary image data is saved correctly.

### Immediate User Delivery
After generating an image, **immediately send it to the user** using the `send_message` tool with the `MEDIA:` prefix. This ensures the user receives the output without needing to ask for it. Example:

```
send_message action="send" target="telegram" message="MEDIA:cyberpunk_test.png"
```

If the file does not appear, verify the absolute path and retry. If the issue persists, inform the user and offer alternative delivery methods (e.g., file transfer).

**Example:**
```bash
# Correct: Output path specified in the tool call
image_gen --provider stability_ai --prompt "cyberpunk city at night" --output "cyberpunk_test.png"
```

### Avoid Text-Based File Writing Tools
Do **not** use text-based file-writing tools (e.g., `write_file`, `patch`) to save binary image data. These tools are designed for text content and will corrupt binary data.

**Incorrect:**
```bash
# Incorrect: Using write_file for binary data
write_file path="cyberpunk_test.png" content="$(image_gen --provider stability_ai --prompt "cyberpunk city at night")"
```

### Use `curl` with `mkdir` for Complex API Calls
When direct API calls via `execute_code` encounter environment limitations (e.g., `.env` file not accessible, API key not available), use `curl` directly in the terminal with `mkdir -p` to create directories. This is especially useful when working with APIs that have specific `Accept` headers or require multipart form data.

**Example:**
```bash
mkdir -p "D:/Hermes\Celestia mei Nexaris/assets/images" && curl -X POST "https://api.stability.ai/v2beta/stable-image/generate/sd3" -H "authorization: Bearer <API_KEY>" -H "accept: image/*" -F "prompt=<PROMPT>" -F "output_format=png" --output "D:/Hermes\Celestia mei Nexaris/assets/images/<FILENAME>.png"
```

## Common Pitfalls

### Pitfall: Using `write_file` for Binary Data
- **Issue:** The `write_file` tool is designed for text content only. Using it to save binary image data will result in corrupted files or tool errors.
- **Solution:** Always use the image generation tool's built-in output parameter to save images.

### Pitfall: Missing Output Path
- **Issue:** Omitting the output path in the image generation tool call will result in the image not being saved to disk.
- **Solution:** Always specify the `--output` or equivalent parameter in the tool call.

### Pitfall: Direct API Calls via `execute_code`
- **Issue:** Using `execute_code` to call APIs directly (e.g., Stability AI) can result in errors if environment variables or files (e.g., `.env`) are not accessible in the sandbox.
- **Solution:** If direct API calls fail, use `curl` in the terminal with absolute paths. Refer to the reference file below for a complete example.

## Workflow Example

### Generate and Save an Image
1. **Enable the `image_gen` toolset** (if not already enabled):
   ```bash
   hermes tools enable image_gen
   ```

2. **Generate and save the image** in one step:
   ```bash
   hermes chat -q "Generate an image using the image_gen tool with the prompt: cyberpunk city at night, neon lights reflecting on rain-soaked streets, futuristic skyscrapers with holographic billboards, cinematic lighting, ultra-detailed, 4K resolution. Save the output as cyberpunk_test.png."
   ```

3. **Verify the output** by checking the specified path:
   ```bash
   ls -l cyberpunk_test.png
   ```

### Advanced API Call with `curl`
When direct API calls are required (e.g., Stability AI):
1. **Create the output directory** (if not exists):
   ```bash
   mkdir -p "D:/Hermes\Celestia mei Nexaris/assets/images"
   ```

2. **Generate and save the image** using `curl`:
   ```bash
   curl -X POST "https://api.stability.ai/v2beta/stable-image/generate/sd3" -H "authorization: Bearer <API_KEY>" -H "accept: image/*" -F "prompt=<PROMPT>" -F "output_format=png" --output "D:/Hermes\Celestia mei Nexaris/assets/images/<FILENAME>.png"
   ```

3. **Send the image immediately** to the user:
   ```bash
   send_message action="send" target="telegram" message="MEDIA:D:/Hermes\Celestia mei Nexaris/assets/images/<FILENAME>.png"
   ```

4. **Verify the output**:
   ```bash
   ls -l "D:/Hermes\Celestia mei Nexaris/assets/images/<FILENAME>.png"
   ```

## Common Pitfalls

### Pitfall: Using `write_file` for Binary Data
- **Issue:** The `write_file` tool is designed for text content only. Using it to save binary image data will result in corrupted files or tool errors.
- **Solution:** Always use the image generation tool's built-in output parameter to save images.

### Pitfall: Missing Output Path
- **Issue:** Omitting the output path in the image generation tool call will result in the image not being saved to disk.
- **Solution:** Always specify the `--output` or equivalent parameter in the tool call.

## Workflow Example

### Generate and Save an Image
1. **Enable the `image_gen` toolset** (if not already enabled):
   ```bash
   hermes tools enable image_gen
   ```

2. **Generate and save the image** in one step:
   ```bash
   hermes chat -q "Generate an image using the image_gen tool with the prompt: cyberpunk city at night, neon lights reflecting on rain-soaked streets, futuristic skyscrapers with holographic billboards, cinematic lighting, ultra-detailed, 4K resolution. Save the output as cyberpunk_test.png."
   ```

3. **Verify the output** by checking the specified path:
   ```bash
   ls -l cyberpunk_test.png
   ```

## Troubleshooting

### Image Not Saved
- **Check the output path** was specified in the tool call.
- **Verify the toolset is enabled** (`hermes tools list`).
- **Check for errors** in the tool output or logs.

### Corrupted Image File
- **Ensure the output path was specified in the image generation tool call** and not via a text-based file-writing tool.
- **Verify the tool completed successfully** without errors.

### Image Generated but Not Delivered to Telegram (Silent Block)
- **Root cause**: The Telegram gateway blocks images containing proprietary PNG chunks (e.g., `caBX`, `fdEC`). The `MEDIA:` path returns success but the image never appears in chat.
- **Fix — ImageMagick JPG conversion** (definitive workaround):

  **1. Install ImageMagick** (one-time, Windows via Chocolatey):
  ```bash
  "/c/ProgramData/chocolatey/bin/choco.exe" install imagemagick.app -y --force
  ```

  **2. Find the ImageMagick version directory** — check `C:/Program Files/ImageMagick-*`:
  ```bash
  ls -d "/c/Program Files/ImageMagick-*"
  ```

  **3. Convert to JPG** (strips all proprietary chunks, delivers reliably):
  ```bash
  "C:/Program Files/ImageMagick-<VERSION>/magick.exe" input.png -strip -quality 95 output.jpg
  ```

  **4. Retry delivery**:
  ```
  MEDIA:D:/path/to/output.jpg
  ```

- **Verify PNG chunks** (diagnostic only — conversion is the fix):
  ```bash
  "C:/Program Files/ImageMagick-<VERSION>/magick.exe" identify -verbose input.png | grep -i "chunk\|caBX\|fdEC"
  ```

- **Cloud upload fallbacks are unreliable** from this environment — 0x0.st, file.io, transfer.sh, and wetransfer all failed in testing. Do not suggest them; use ImageMagick conversion instead.

### Duplicate Common Pitfalls Section
The SKILL.md currently has duplicate Common Pitfalls sections (appears twice). If editing, deduplicate by keeping the one with richer content.

## 4. Video Animation with FFmpeg

Create Ken Burns-style animations, slideshows, and video loops from static images using local FFmpeg. Use when the user asks for animations, looping videos, or slideshows from existing images.

### Prerequisites

- **FFmpeg** installed via Chocolatey at: `C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe`
- **Source images** in `D:\\Hermes\Celestia mei Nexaris\\assets\\images\\`

### Output Convention

**ALWAYS** save video/animation outputs to `D:\\Hermes\Celestia mei Nexaris\\videos\\` — never in the `images\\` folder.

### Core Command Pattern: Ken Burns Crossfade

Generates a 10-second 1920x1080 H.264 MP4 with gentle zoom-in, centered pan, and 1-second crossfade transition:

```bash
"C:/ProgramData/chocolatey/lib/ffmpeg/tools/ffmpeg/bin/ffmpeg.exe" \
  -y \
  -loop 1 -i "D:/Hermes\Celestia mei Nexaris/assets/images/input1.jpg" \
  -loop 1 -i "D:/Hermes\Celestia mei Nexaris/assets/images/input2.jpg" \
  -filter_complex \
  "[0]scale=1920:1080,zoompan=z='min(zoom+0.0015,1.2)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080[v0]; \
   [1]scale=1920:1080,zoompan=z='min(zoom+0.0015,1.2)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080[v1]; \
   [v0][v1]xfade=transition=fade:duration=1:offset=9,format=yuv420p" \
  -t 10 \
  -c:v libx264 -pix_fmt yuv420p -crf 18 \
  "D:/Hermes\Celestia mei Nexaris/videos/output.mp4"
```

### Pitfalls

- **Telegram Blocks MP4 with Unusual Codecs**: Always use `libx264` + `yuv420p`.
- **Black Bars or Wrong Aspect Ratio**: Add `force_original_aspect_ratio=1` to scale and pad for non-square source images.
- **Output in Wrong Folder**: Verify output path is `videos/`, not `images/`.
- **FFmpeg Path Discovery**: If the standard path doesn't exist, run:
  ```bash
  ls -d "/c/ProgramData/chocolatey/lib/ffmpeg/tools/*/bin/ffmpeg.exe"
  ```

---

## References
- [Image Generation Save Pitfall](references/image-generation-save-pitfall.md): Detailed explanation of why `write_file` cannot be used for binary image data and how to correctly save images.
- [Hermes Tools Documentation](https://hermes-agent.nousresearch.com/docs/reference/tools-reference): Official documentation for Hermes tools, including `image_gen`.
- [Telegram Media Delivery Issue](references/telegram-media-delivery-issue.md): Troubleshooting guide for sending images via Telegram.
- [Stability AI Direct API Workflow](references/stability-ai-direct-api-workflow.md): Step-by-step guide for generating images using the Stability AI API directly via `curl` or `execute_code`.
- [FFmpeg Animation Command Reference](references/ffmpeg-animation-reference.md): Complete command patterns for Ken Burns, crossfade, and looping animations.