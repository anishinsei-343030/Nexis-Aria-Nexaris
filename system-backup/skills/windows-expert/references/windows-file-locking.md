# Windows File Locking

## Symptoms
- `rm -rf` fails with "Device or resource busy" on Windows (Git Bash/MSYS).
- Files/folders remain locked even after closing applications.

## Diagnosis
1. **Check for locks** (requires `handle.exe` from Sysinternals):
   ```powershell
   handle.exe "C:\path\to\folder"
   ```
2. **Task Manager**: Look for processes using the folder (e.g., Obsidian, Git Bash, Explorer).

## Workaround
1. **Delete contents first**:
   ```bash
   rm -rf /c/path/to/folder/*
   ```
2. **Delete the folder**:
   ```bash
   rmdir /c/path/to/folder
   ```
3. **Force-delete on reboot** (if still locked):
   ```cmd
   rmdir /s /q "C:\path\to\folder"
   ```

## Prevention
- Close all applications using the folder before deletion.
- Use `handle.exe -p <PID>` to release locks.