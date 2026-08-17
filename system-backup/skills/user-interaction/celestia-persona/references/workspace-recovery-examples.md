# Workspace Recovery Examples

## Example 1: Recreating `Artwork/Character_Design.md`

**Scenario**: User accidentally deletes `Character_Design.md`.

**Commands**:
```bash
mkdir -p "D:\\Hermes\Celestia mei Nexaris\\assets\\images\"
echo -e "# Character Design References\n\n## Celestia Mei Nexaris\n- Silver-white hair, faint blue highlights\n- Sapphire/violet eyes\n- Futuristic accessories + star motifs\n- White/navy outfit with cyan accents\n\n## Zero Riven Nexaris\n- Dark cybernetic aesthetic\n- Monochrome + teal accents\n" > "D:\\Hermes\Celestia mei Nexaris\\assets\\images\\Character_Design.md"
```

**Verification**:
```bash
ls -la "D:\\Hermes\Celestia mei Nexaris\\assets\\images\\"
cat "D:\\Hermes\Celestia mei Nexaris\\assets\\images\\Character_Design.md"
```

---

## Example 2: Recreating `Scripts/Mei_Browser.ps1`

**Scenario**: Browser control script missing.

**Commands**:
```bash
mkdir -p "D:\\Hermes\Celestia mei Nexaris\\scripts\"
echo -e '# Mei_Browser.ps1 — Browser control for Cosplay Fusion Hub & FB tasks\n# Usage: powershell -File "D:\\Hermes\Celestia mei Nexaris\\scripts\\Mei_Browser.ps1" -Command {start|stop|status}\n\nparam(\n    [Parameter(Mandatory=$true)]\n    [string]$Command\n)\n\n$ChromePID = Get-Content "D:\\Celestia Mei Nexaris\\playwright\\chrome.pid" -ErrorAction SilentlyContinue\n\nswitch ($Command) {\n    "start" {\n        if ($ChromePID) {\n            Write-Host "Browser already running (PID: $ChromePID)"
        } else {\n            Start-Process "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222\n            Write-Host "Browser started"
        }\n    }\n    "stop" {\n        if ($ChromePID) {\n            Stop-Process -Id $ChromePID -Force\n            Remove-Item "D:\\Celestia Mei Nexaris\\playwright\\chrome.pid" -ErrorAction SilentlyContinue\n            Write-Host "Browser stopped"
        } else {\n            Write-Host "No browser process found"
        }\n    }\n    "status" {\n        if ($ChromePID) {\n            Write-Host "Browser running (PID: $ChromePID)"
        } else {\n            Write-Host "Browser not running"
        }\n    }\n}\n' > "D:\\Hermes\Celestia mei Nexaris\\scripts\\Mei_Browser.ps1"
```

**Verification**:
```bash
ls -la "D:\\Hermes\Celestia mei Nexaris\\scripts\\"
powershell -File "D:\\Hermes\Celestia mei Nexaris\\scripts\\Mei_Browser.ps1" -Command status
```

---

## Example 3: Full Workspace Rebuild

**Scenario**: Entire `Workspace` folder deleted.

**Commands**:
```bash
mkdir -p "D:\\Hermes\Celestia mei Nexaris\\{assets,audio,video,scripts,knowledge,output,projects}"

# Restore stub files
## Artwork
mkdir -p "D:\\Hermes\Celestia mei Nexaris\\assets\\images\\OCs\\"
echo -e "# OCs (Original Characters)\n\n## Celestia Mei Nexaris\n- Role: Celestial Intelligence\n- Theme: Cosmic guardian\n" > "D:\\Hermes\Celestia mei Nexaris\\assets\\images\\OCs\\celestia.md"

## Documents
mkdir -p "D:\\Hermes\Celestia mei Nexaris\\knowledge\\"
echo -e "# Nexaris World Lore\n\n## Starlight Archives\nA cosmic library where time is stored in starlight.\n" > "D:\\Hermes\Celestia mei Nexaris\\knowledge\\starlight_archives.md"

## Scripts
mkdir -p "D:\\Hermes\Celestia mei Nexaris\\scripts\\Browser\\"
echo -e '# Mei_Browser.ps1 — Browser control\n# Usage: powershell -File "$PSScriptRoot\\Mei_Browser.ps1" -Command {start|stop|status}\n' > "D:\\Hermes\Celestia mei Nexaris\\scripts\\Browser\\Mei_Browser.ps1"
```

**Verification**:
```bash
tree "D:\\Hermes\Celestia mei Nexaris\\" /F
```