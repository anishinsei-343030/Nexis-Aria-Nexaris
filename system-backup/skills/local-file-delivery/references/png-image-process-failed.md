# PNG "Image_process_failed" — Proprietary Chunk Stripping

Telegram's image processing rejects PNGs with unrecognized proprietary chunks. The typical error is `Image_process_failed` with no further detail.

## Root Cause

Certain tools (e.g., ComfyUI, SD WebUI, niche editors) embed custom ancillary chunks in PNG files:
- `caBX` (ComfyUI metadata)
- `fdEC` (additional metadata/workflow data)
- Other tool-specific chunks

Telegram's image decoder does not recognize these chunks and rejects the entire file.

## Detection

Check for non-standard chunks using Python:

```python
from PIL import Image
import struct

with Image.open("file.png") as img:
    info = img.info
    # Look for unusual keys like 'caBX', 'fdEC', etc.
    print(info.keys())
```

Or with `pngcheck` if available:
```bash
pngcheck -v file.png | grep -E 'caBX|fdEC'
```

## Cleaning (Stripping Chunks)

### Method 1: Clean re-encode (PIL/Pillow)

```python
from PIL import Image

img = Image.open("original.png")
# Save strips proprietary chunks — PIL only keeps standard PNG chunks
img.save("cleaned.png", "PNG")
```

**Pitfall:** PIL may re-encode losslessly but strips all ancillary chunks including valid ones (EXIF, ICC profiles). Acceptable for Telegram delivery.

### Method 2: JPEG fallback

```python
from PIL import Image

img = Image.open("original.png")
img = img.convert("RGB")
img.save("fallback.jpg", "JPEG", quality=92)
```

Smaller file size, more reliable delivery. Always works.

## Verification

After cleaning, verify the file can be opened cleanly:

```python
from PIL import Image
img = Image.open("cleaned.png")
img.verify()  # raises on corrupt data
```

## Delivery

Send with `MEDIA:absolute/path/to/cleaned_image.png` via `send_message`.

## Pitfalls

- Do **not** rely on `convert` (ImageMagick) — may not be installed.
- Do **not** use `transfer.sh` or similar — network may be blocked.
- The `MEDIA:` path is the primary delivery mechanism; only fall back to external hosts if gateway logging shows a different error.
- After cleaning, use forward-slash paths (`C:/Users/...` not `C:\Users\...`) — backslashes cause silent failures.
