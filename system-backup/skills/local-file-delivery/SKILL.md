---\nname: local-file-delivery\ndescription: name: local-file-delivery\nversion: 1.0.0\nplatforms: [linux, macos, windows]\n---
name: local-file-delivery
description: Procedures for locating and delivering local files to the user via Telegram, including handling large binary files and timeouts.
category: system-utility
---

# Local File Delivery

Guidelines for finding and sending files from the local filesystem to the user.

## 1. Efficient Location
Searching the entire root directory (`/` or `/c/`) often leads to timeouts. Use a tiered search strategy:
1. **Targeted Search**: Check common user directories first.
   - `/c/Users/<user>/Documents`
   - `/c/Users/<user>/Desktop`
   - `/c/Users/<user>/Downloads`
   - `/c/Users/<user>/OneDrive`
2. **Limited Depth**: Use `find` with `-maxdepth` (e.g., 5) to avoid scanning deep system directories.
3. **Broad Search**: Only perform a full recursive search if targeted searches fail.

## 2. Delivery via Telegram
Use the `MEDIA:` prefix within the `send_message` tool to send files as native attachments.

### Path Format Requirements
- **Windows Paths**: Use **forward slashes** (`D:/path/to/file`) or **POSIX-style** (`/d/path/to/file`). Backslashes (`D:\path\to\file`) may cause silent failures.
- **Verification**: Always confirm the file exists (`ls -la /path/to/file`) and has read permissions before sending.

### Gateway Routing Quirks
- **DMs vs. Group Chats**: `MEDIA:` paths may fail silently in DMs if the gateway is misconfigured. Test with a small file first.
- **Fallback**: If `MEDIA:` fails, upload the file to a temporary host (e.g., Imgur) and send the URL.

- **Format**: `MEDIA:/absolute/path/to/file`
- **Verification**: Always confirm to the user that the file has been sent as an attachment. Provide evidence (e.g., `ls -la` output) for irreversible actions.

## 3. Handling Binary Files
- **Do NOT** use `read_file` on `.docx`, `.pdf`, `.exe`, or other binary formats. This will trigger a binary file error.
- Use `ls -la` or `stat` to verify the file's existence and size before attempting delivery.

## User Preferences
- **Simplicity First**: The user prefers direct file delivery without splitting, compressing, or saving to the desktop. Only split or compress if the file exceeds Telegram's size limits (2 GB for regular users, 4 GB for channels/bots) and the user explicitly approves.

## 4. Handling Delivery Failures
### Silent Failures in Group Chats
- The `send_message` tool with `MEDIA:` tags may **fail silently** in group chats, reporting errors like "No deliverable text or media" or "Chat not found" even when the file is delivered. Always confirm receipt with the user.

### Retry Strategy
If delivery fails:
1. **Verify the file path and size** with `ls -la`.
2. **Check for PNG proprietary chunks** (`Image_process_failed` error). See `references/png-image-process-failed.md` for the cleaning procedure.
3. **Retry with text + `MEDIA:`**: Include a short message alongside the `MEDIA:` tag to avoid silent failures.

### Post-Move Cleanup
After moving files to a new location:
1. **Delete the source directory** to avoid remnants:
   ```bash
   rm -rf /path/to/source
   ```
2. **Verify deletion** with:
   ```bash
   find /path/to/source -name "*" 2>/dev/null || echo "DELETED"
   ```
3. **Pitfall: Windows File Locks**
   If `rm -rf` fails with "Device or resource busy":
   - Delete contents first:
     ```bash
     rm -rf /path/to/source/*
     ```
   - Retry `rmdir /path/to/source`.
   - If still locked, use Task Manager to kill processes (Obsidian, Git Bash, Explorer).
   ```
send_message(message="Here's the file:\n\nMEDIA:/path/to/file", target="telegram:Group Name (group)")
   ```
3. **Fallback to Targeted Delivery**: If the file is small (< 50MB), retry sending to the **specific group chat** (e.g., `telegram:Chaos Control (group)`).

### Large File Workaround (Splitting)
Only split files if they exceed Telegram's size limits and the user approves. Use `dd` to split into chunks (e.g., 5MB each).
```bash
dd if="/path/to/file" of="/path/to/part_01.part" bs=1 skip=0 count=5242880
dd if="/path/to/file" of="/path/to/part_02.part" bs=1 skip=5242880 count=5242880
```

Provide reassembly instructions to the user:

**Windows (CMD):**
`copy /b file.part* original_filename.ext`

**Linux/macOS (Terminal):**
`cat file.part* > original_filename.ext`

**Windows (CMD):**
`copy /b file.part* original_filename.ext`

**Linux/macOS (Terminal):**
`cat file.part* > original_filename.ext`

## Pitfalls
- **Tool Availability**: Do not rely on `zip` or `7z` as they may not be installed in the environment. Use `dd` for splitting as it is a standard POSIX tool.
- **PowerShell Escaping**: When using `powershell` inside `execute_code`, be careful with curly braces `{}` in f-strings; they must be doubled `{{ }}` to be treated as literal characters.
- **Silent Failures**: If the user says they "don't see the file", the `MEDIA:` tag may have failed due to size or path issues. Move immediately to the splitting workaround.
- **`MEDIA:` Path Failures in DMs**: The `MEDIA:` prefix within `send_message` may fail silently in DMs even when the file is delivered. Always confirm receipt with the user and provide evidence.
- **PNG `Image_process_failed` Error**: Telegram rejects PNGs with proprietary chunks (e.g., `caBX`, `fdEC` from ComfyUI or SD WebUI). See `references/png-image-process-failed.md` for detection and cleaning procedures.
- **Fallback Delivery Strategy**: If `MEDIA:` fails:
  1. Retry with `send_message(message="File:", target="telegram:Your Group Chat", media="MEDIA:/path/to/file")` to include a text message alongside the media.
  2. Use an external upload service (e.g., Imgur) as a reliable fallback instead of `transfer.sh`. Upload to Imgur and provide the direct link.
  3. If the file is small (< 50MB), retry sending to the specific group chat (e.g., `telegram:Chaos Control (group)`) using the direct group ID.
- **Windows Path Formatting**: Always use forward slashes (`D:/path/to/file`) or POSIX-style (`/d/path/to/file`) when specifying paths with `MEDIA:`. Backslashes (`D:\\path\\to\\file`) may cause silent failures.
- **Large File Splitting**: Only split files if they exceed Telegram's size limits. Use `dd` to split into chunks (e.g., 5MB each). Do NOT rely on `zip` or `7z` as they may not be installed in the environment.
