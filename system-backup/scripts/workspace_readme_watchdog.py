#!/usr/bin/env python3
"""Wrapper so the cron scheduler (script paths must live under
~/.hermes/scripts/ or profile scripts/ dir) can call the real workspace
script at D:\\Hermes\\Nexis Aria Nexaris\\scripts\\update_workspace_readme.py.

Exits 0 with no output when nothing changed (silent skip).
Exits 0 with 'README updated' when it rewrote the file.
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