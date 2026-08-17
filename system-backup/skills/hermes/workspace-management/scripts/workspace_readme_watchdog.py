#!/usr/bin/env python3
"""Thin cron wrapper. Place in ~/.hermes/profiles/<name>/scripts/ and
point the cron job at just this filename (relative path required).

Calls the real workspace script. Contract:
  exit 0 + empty stdout = silent skip (tree unchanged)
  exit 0 + printed line  = README was rewritten
  exit 1                 = real script failed (cron will alert)
"""
import subprocess
import sys

REAL = r"D:\Hermes\Nexis Aria Nexaris\scripts\update_workspace_readme.py"

if __name__ == "__main__":
    res = subprocess.run([sys.executable, REAL], capture_output=True, text=True)
    out = (res.stdout or "").strip()
    err = (res.stderr or "").strip()
    if res.returncode != 0:
        print(f"update_workspace_readme failed: {err or out}")
        sys.exit(1)
    if out:
        print(out)
    sys.exit(0)
