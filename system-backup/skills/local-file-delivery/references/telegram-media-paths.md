# Telegram `MEDIA:` Path Handling

## Path Format Requirements
Telegram's `MEDIA:` tag requires **forward slashes** or **POSIX-style paths** for Windows files:
- ✅ **Valid**: `D:/Hermes\Celestia mei Nexaris/assets/images/file.png`
- ✅ **Valid**: `/d/Hermes\Celestia mei Nexaris/assets/images/file.png`
- ❌ **Invalid**: `D:\Hermes\Celestia mei Nexaris\assets\images\file.png` (backslashes cause silent failures)

## Gateway Routing Quirks
- **DMs**: `MEDIA:` paths may fail silently if the gateway is misconfigured. Test with a small file first.
- **Group Chats**: More reliable, but confirm receipt with the user.

## Pre-Delivery Verification
Always run these checks before sending:
```bash
ls -la "/path/to/file"  # Verify existence and permissions
file "/path/to/file"    # Confirm file type
```

## Fallback Options
If `MEDIA:` fails:
1. Upload to a temporary host (e.g., Imgur) and send the URL.
2. Use `execute_code` to encode the file as a data URL (for small files).

## Debugging Silent Failures
- Check gateway logs for errors (e.g., `~/.hermes/logs/gateway.log`).
- Verify the Telegram client has permissions to access the file path.