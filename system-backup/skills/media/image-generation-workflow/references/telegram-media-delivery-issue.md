# Telegram Media Delivery Issue

## Root Cause

The Telegram gateway blocks images containing **proprietary PNG chunks** (e.g., `caBX`, `fdEC`). These chunks are added by certain image generation tools (e.g., Stability AI) as metadata markers. When the image is sent via `MEDIA:` path, the gateway returns success but the image never appears in the chat.

**Not a relative-path issue** — absolute paths also fail for chunk-laden PNGs.

## Fix

### ImageMagick Conversion (Definitive)

1. **Install ImageMagick** (one-time, Windows via Chocolatey):
   ```bash
   "/c/ProgramData/chocolatey/bin/choco.exe" install imagemagick.app -y --force
   ```

2. **Find the installed version**:
   ```bash
   ls -d "/c/Program Files/ImageMagick-*"
   ```

3. **Convert to JPG** (strips all proprietary chunks — JPG format has no chunk mechanism):
   ```bash
   "C:/Program Files/ImageMagick-<VERSION>/magick.exe" input.png -strip -quality 95 output.jpg
   ```

4. **Deliver the JPG** via MEDIA:
   ```
   MEDIA:D:/path/to/output.jpg
   ```

### Stripping PNG Metadata (Less Reliable)
Stripping `-strip` while keeping PNG format may still fail if the gateway's chunk detection is aggressive. Prefer JPG conversion.

## Failed Alternatives (Do Not Recommend)

These cloud upload services were tested and failed from this environment:
- **0x0.st** — rejected the file
- **file.io** — required HTTPS redirect (curl doesn't follow by default)
- **transfer.sh** — blocked (exit 7: connection refused)
- **wetransfer** — ChromeDriver version mismatch (Chrome 149 vs ChromeDriver 125)

Do not suggest cloud upload fallbacks — they add latency and fail unpredictably. Stick with ImageMagick JPG conversion.

## Verification

Check the generated file exists and is a valid JPG:
```bash
ls -la "D:/Hermes\Celestia mei Nexaris/assets/images/output.jpg"
"C:/Program Files/ImageMagick-<VERSION>/magick.exe" identify "D:/Hermes\Celestia mei Nexaris/assets/images/output.jpg"
```
