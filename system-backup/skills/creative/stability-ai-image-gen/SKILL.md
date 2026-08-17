---

name: stability-ai-image-gen
description: Generate images using the Stability AI API via curl. This skill provides a reliable method for creating high-quality images and saving them to the correct directory.
---

## Trigger Conditions
Use this skill when:
- You need to generate an image using the Stability AI API for Celestia's visual identity, Hermes social media branding, or any other image generation task.
- The `image_gen` Hermes tool is unavailable or misconfigured.
- You want to ensure the image is saved to `D:\\Hermes\Celestia mei Nexaris\\assets\\images\\` or `D:\\Hermes\Celestia mei Nexaris\\Hermes-Social\\branding\\` for Hermes brand assets.

---

## Round-Robin Key Selection

Stability AI supports multiple API keys for load distribution and credit management. Load keys from `STABILITY_AI_API_KEYS` (a JSON array or comma-separated string) and pick one round-robin:

```bash
# Parse keys from config (comma-separated)
KEYS_JSON=$(hermes config get STABILITY_AI_API_KEYS)
# The config returns a JSON array; extract keys via Python or jq
# Use python to pick a random key:
python3 -c "import os,json,random; keys=json.loads(os.environ.get('STABILITY_AI_API_KEYS','[]')); print('Bearer '+random.choice(keys))"
```

Set all keys at once via:
```bash
hermes config set STABILITY_AI_API_KEYS '["sk-key1...", "sk-key2...", "sk-key3..."]'
```

**Pitfall**: Always verify the selected key has credits before attempting generation. If a key returns HTTP 402, remove it from the rotation and try another.

---

## Steps

### 0. User Context: Shin's Preferences
This user (Shin) prefers **anime-style, high-detail, 'masterpiece'-quality** portraits. Check `references/anime-prompts.md` for curated prompt templates. For Celestia portraits use the Celestia-specific template.

### 1. Pre-Flight Checks: API Key + Credits
Before generating, perform two checks:

**Check A — API Key validity**:
```bash
curl -X GET "https://api.stability.ai/v1/user/account" \
     -H "Authorization: Bearer $STABILITY_AI_API_KEY" \
     -H "Accept: application/json"
```
If response contains `"message": "Incorrect API key provided"`, the key is invalid. Report to user immediately — do not attempt generation.

**Check B — Credit availability**:
```bash
curl -s -X GET "https://api.stability.ai/v1/user/balance" \
     -H "Authorization: Bearer $STABILITY_AI_API_KEY" \
     -H "Accept: application/json"
```
If credits are 0 or the request returns an error (e.g., HTTP 402), **do not attempt generation**. Report the state to the user transparently and propose alternatives:
- Configure a different API key with credits
- Switch to a different provider (FAL, OpenAI DALL-E)
- Use browser automation (ChatGPT image generation) as a workaround
- Save the prompt for later use when credits are available

To retrieve the current key:
```bash
hermes config get STABILITY_AI_API_KEY
```

### 2. Prepare the Output Directory
Ensure the output directory exists:
```bash
mkdir -p "D:\Hermes\Celestia mei Nexaris\assets\images"
```

### 3. Generate the Image
Use the following `curl` command to generate the image. Ensure the `Content-Type` is `multipart/form-data` by using `-F` flags for parameters. Replace `<PROMPT>` with your desired prompt and `<FILENAME>` with the output filename (e.g., `cosmic_spire.png`).

```bash
curl -s -X POST "https://api.stability.ai/v2beta/stable-image/generate/ultra" \
     -H "Authorization: Bearer *** \
     -H "Accept: image/*" \
     -F "prompt=<PROMPT>" \
     -F "output_format=png" \
     --fail \
     --output "D:/Hermes\Celestia mei Nexaris/assets/images/<FILENAME>"
```

**Example**:
```bash
curl -s -X POST "https://api.stability.ai/v2beta/stable-image/generate/ultra" \
     -H "Authorization: Bearer *** \
     -H "Accept: image/*" \
     -F "prompt=A majestic cosmic spire reaching towards a nebula" \
     -F "output_format=png" \
     --fail \
     --output "D:/Hermes\Celestia mei Nexaris/assets/images/celestia_ultra_test.png"
```

**Important**: If the `curl` command returns an HTTP error (e.g., `400 Bad Request`), the output file will likely contain a JSON error message instead of an image. Inspect the file content if you suspect an error.

### 4. Verify the Image
Check that the image was saved to the correct directory:
```bash
ls "D:\Hermes\Celestia mei Nexaris\assets\images\"
```

### 5. Send the Image
Ensure the image is sent as a photo, not a file. Use forward slashes (`/`) in the path:
```
MEDIA:D:/Hermes\Celestia mei Nexaris/assets/images/<FILENAME>
```

**Verification Step**:
Before sending, confirm the file exists and is a valid image:
```bash
file "D:/Hermes\Celestia mei Nexaris/assets/images/<FILENAME>" | grep -i "PNG image"
```
If the command returns `PNG image data`, the file is valid and can be sent.

---

### 6. Reference Anime Prompts  
For Shin's portrait requests, use the curated prompts in `references/anime-prompts.md`. They include Celestia-specific templates optimized for high-detail anime-style output.

---

## Pitfalls

### 1. 401 Unauthorized Error
- **Cause**: The `STABILITY_AI_API_KEY` is missing or incorrect.
- **Solution**: Verify the key is set in your environment and correctly referenced in the `curl` command.

### 2. Invalid or Missing Header Value
- **Cause**: The `Accept` header is not set to `image/*`.
- **Solution**: Ensure the header is included as `-H "Accept: image/*"`.

### 3. Output File Not Saved
- **Cause**: The output directory does not exist or the filename is invalid.
- **Solution**: Create the directory beforehand and ensure the filename is valid.

### 4. Curl Syntax Errors
- **Cause**: Improper escaping of quotes or special characters in the `curl` command.
- **Solution**: Use the exact syntax provided in the **Steps** section. Pay close attention to escaping backslashes and quotes.

### 5. Shell Variable Masking (CRITICAL)
- **Cause**: The terminal tool displays environment variable values (like `$STABILITY_AI_API_KEY`) as `***` for security. If you copy the curl command from a previous response that shows `***`, subsequent runs will try literal `***` as the key and fail with 401/403.
- **Solution**: Always store the key in a bash variable first, then reference that variable:
  ```bash
  KEY="$STABILITY_AI_API_KEY" && curl -s -X POST "https://api.stability.ai/v2beta/stable-image/generate/ultra" \
    -H "Authorization: Bearer $KEY" \
    -H "Accept: image/*" \
    -F "prompt=..." \
    -F "output_format=png" \
    --fail \
    --output "path/to/output.png"
  ```
- **Pitfall**: Do NOT use `$STABILITY_AI_API_KEY` directly in the `-H` header value in a multi-line curl command — if the line gets re-displayed, the key becomes `***` in your output and will fail on re-run. Always capture into a variable first on the same line as the assignment.

### 6. v1 Endpoints vs v2beta/ultra Auth
- **Cause**: The legacy `v1/generation/stable-diffusion-*` endpoints use a different auth scheme than `v2beta/stable-image/generate/ultra`. A key that works on v2beta may return `401 Unauthorized` on v1 endpoints.
- **Solution**: Use `v2beta/stable-image/generate/ultra` exclusively. Do not fall back to `v1/generation/` endpoints unless the key was explicitly provisioned for v1.
- **Diagnostic**: If `v2beta/ultra` returns `403 (Cloudflare)`, the issue is likely IP-based or rate-limiting, not the key. Wait and retry, or switch to a different provider.

### 7. Telegram Blocks PNGs with Proprietary Chunks
- **Cause**: Some Stability AI-generated PNGs contain proprietary chunks (e.g., `caBX`, `fdEC`) that the Telegram gateway silently blocks — `MEDIA:` returns success but the image never appears in chat.
- **Diagnostic — check for problematic chunks**:
  ```bash
  "C:/Program Files/ImageMagick-<VERSION>/magick.exe" identify -verbose path/to/image.png | grep -i "chunk\|caBX\|fdEC"
  ```
- **Fix — convert to JPG with ImageMagick** (strips all proprietary chunks):
  ```bash
  # Install ImageMagick (one-time)
  "/c/ProgramData/chocolatey/bin/choco.exe" install imagemagick.app -y --force

  # Find installed version
  ls -d "/c/Program Files/ImageMagick-*"

  # Convert to JPG
  "C:/Program Files/ImageMagick-<VERSION>/magick.exe" input.png -strip -quality 95 output.jpg
  ```
- **Then deliver the JPG** via `MEDIA:D:/path/to/output.jpg`
- **Pitfall**: Do NOT suggest cloud upload services (0x0.st, file.io, transfer.sh, wetransfer) — they are unreliable from this environment. ImageMagick conversion is the definitive fix.

### 9. Nonexistent Image-to-Video Endpoint (v2beta)
- **Cause**: The endpoint `POST /v2beta/image-to-video` does not exist on Stability AI's v2beta API. Attempting to use it returns `HTTP 404 Not Found`.
- **Session 2026-06-15**: This endpoint was attempted for Celestia animation but failed with 404.
- **Solution**: Stability AI does not currently offer a public image-to-video API. For video generation:
  - Use **HeyGen Video Agent** (requires `HEYGEN_API_KEY`)
  - Use **ComfyUI + AnimateDiff** (requires local GPU)
  - Use **FFmpeg** for Ken Burns-style animations from static images (no API required)
  - Use **browser automation** (ChatGPT image-to-video)
- **Pitfall**: Do not attempt to use `/v2beta/image-to-video` or `/v1/video/generate`. Neither endpoint exists.
- **Cause**: The `write_file` tool is designed for text content only. Using it to save binary image data corrupts the file.
- **Solution**: Always use the image generation tool's built-in output parameter (`--output` for curl, `output_path` for API calls) to save images.

---

## Fallback Provider Logic

If Stability AI fails consistently (all keys exhausted), fall back to these providers in order:

1. **FAL AI** — Use `image_generate` tool if `$FAL_KEY` is set.
   - Endpoint via curl: `POST https://fal.run/fal-ai/flux-pro/v1.1-ultra`
   - Auth: `Authorization: Key $FAL_KEY`

2. **OpenAI DALL-E** — Use via curl if `$OPENAI_API_KEY` is set.
   - Endpoint: `POST https://api.openai.com/v1/images/generations`
   - Model: `dall-e-3`, Size: `1024x1024`

3. **ChatGPT Browser Automation** — Use Playwright-based automation as last resort (requires login).

**Pitfall**: Do not attempt more than one key per provider per fallback cycle. If FAL returns 403 (locked) and Stability returns 402 (no credits), inform the user rather than looping.
After generating the image:
1. Confirm the file exists in `D:\Hermes\Celestia mei Nexaris\assets\images\`.
2. Open the image to verify it matches the prompt.
3. Send the image to the user using `MEDIA:` syntax.

---

## Example Workflow
1. **Prompt**: "futuristic cityscape at dusk, neon lights, ultra-detailed, 4K resolution"
2. **Command**:
   ```bash
   curl -X POST "https://api.stability.ai/v2beta/stable-image/generate/sd3" \
        -H "Authorization: Bearer $STABILITY_AI_API_KEY" \
        -H "Accept: image/*" \
        -H "Content-Type: application/json" \
        --data-raw "{\"prompt\": \"futuristic cityscape at dusk, neon lights, ultra-detailed, 4K resolution\", \"output_format\": \"png\"}" \
        --output "D:\\Hermes\Celestia mei Nexaris\\assets\\images\\cityscape.png"
   ```
3. **Output**:
   ```
   MEDIA:D:\Hermes\Celestia mei Nexaris\assets\images\cityscape.png
   ```