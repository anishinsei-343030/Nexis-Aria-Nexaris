#!/usr/bin/env python3
"""workspace_auto_backup.py — auto-backup Nexis workspace + Hermes profile to GitHub.

Runs from cron (no_agent mode, daily 23:00). Behavior:
  1. Mirror profile critical files -> <workspace>/system-backup/ (every run, copy + prune)
  2. Full tarball (profile + DBs) -> <workspace>/Backup/ (dedup: skip if <72h since last)
  3. git add -A + commit + push workspace repo (every run; silent when nothing changed)
  4. Non-zero exit + BACKUP_FAIL line on failure (cron alerts)

Excludes: secrets (.env, pairing/, gateway_state.json), runtime dirs and DBs from git
(DBs only inside the tarball, via sqlite-safe copies). Skills included (mirror +
tarball) minus curation artifacts (.curator_backups, .hub, .usage.json* etc).

Requires git credentials already configured (origin is HTTPS, credential helper /
PAT handles auth — verified by manual pushes).
"""
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

PROFILE = Path(r"C:\Users\Administrator\.hermes\profiles\nexis")
WORKSPACE = Path(r"D:\Hermes\Nexis Aria Nexaris")
MIRROR = WORKSPACE / "system-backup"
BACKUP_DIR = WORKSPACE / "Backup"
BACKUP_LOG = WORKSPACE / "output" / "backup.log"
MAX_HOURS = 72

# Profile entries mirrored to system-backup/ and included in the tarball.
INCLUDE = [
    "memories",
    "cron/jobs.json",
    "config.yaml",
    "SOUL.md",
    "profile.yaml",
    "channel_directory.json",
    "shell-hooks-allowlist.json",
    "scripts",
    "skills",
]

# Databases: tarball only (sqlite-safe copy), never mirrored into git.
DBS = [
    "memory_store.db",
    "state.db",
    "verification_evidence.db",
    "cron/executions.db",
]

KEEP_IN_MIRROR = {".gitignore"}  # files in the mirror owned by the repo, not the profile


def run(cmd, cwd=WORKSPACE, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def ignore_artifacts(dirname, names):
    return [n for n in names if n == "__pycache__" or n.startswith(".")]


def sync_mirror():
    """Copy the include set into system-backup/, then prune stale mirrored entries."""
    MIRROR.mkdir(parents=True, exist_ok=True)
    for rel in INCLUDE:
        src = PROFILE / rel
        if not src.exists():
            continue
        dst = MIRROR / rel
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore_artifacts)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    for child in MIRROR.iterdir():
        if child.name in KEEP_IN_MIRROR:
            continue
        covered = child.name in INCLUDE or any(
            rel.startswith(child.name + "/") for rel in INCLUDE
        )
        if not covered:
            if child.is_dir():
                shutil.rmtree(child, ignore_errors=True)
            else:
                child.unlink(missing_ok=True)


def safe_copy_db(src, dst):
    """Copy a live SQLite DB via the backup API (WAL-safe)."""
    conn = sqlite3.connect(f"file:{src.as_posix()}?mode=ro", uri=True)
    try:
        dest = sqlite3.connect(dst)
        try:
            conn.backup(dest)
        finally:
            dest.close()
    finally:
        conn.close()


def hours_since_last_backup():
    if not BACKUP_LOG.exists():
        return None
    lines = BACKUP_LOG.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
    if not lines:
        return None
    parts = lines[-1].split()[:2]
    if len(parts) < 2:
        return None
    try:
        last_dt = datetime.strptime(" ".join(parts), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    return (datetime.now() - last_dt).total_seconds() / 3600


def log(msg):
    BACKUP_LOG.parent.mkdir(parents=True, exist_ok=True)
    with BACKUP_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {msg}\n")


def make_tarball():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp) / "nexis-profile"
        for rel in INCLUDE:
            src = PROFILE / rel
            if not src.exists():
                continue
            dst = staging / rel
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore_artifacts)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        for rel in DBS:
            src = PROFILE / rel
            if not src.exists():
                continue
            dst = staging / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            safe_copy_db(src, dst)
        out = BACKUP_DIR / f"nexis_full_backup_{ts}.tar.gz"
        with tarfile.open(out, "w:gz") as tar:
            tar.add(staging, arcname="nexis-profile")
    return out


def main():
    # 1. Mirror profile -> system-backup/ (every run)
    sync_mirror()

    # 2. Tarball with dedup (only created at most every MAX_HOURS)
    hours = hours_since_last_backup()
    if hours is not None and hours < MAX_HOURS:
        log(f"Backup skipped (last: {hours:.1f} hours ago, max {MAX_HOURS}h)")
    else:
        backup_file = make_tarball()
        log(f"Backup created: {backup_file.name} ({backup_file.stat().st_size} bytes)")

    # 3. Git add / commit / push (every run; push always so pending commits retry)
    res = run(["git", "add", "-A"])
    if res.returncode != 0:
        print(f"BACKUP_FAIL: git add error: {res.stderr.strip()}")
        return 1
    res = run(["git", "diff", "--cached", "--quiet"])
    committed = False
    if res.returncode != 0:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        res = run(["git", "commit", "-m", f"Auto-backup {ts} (profile + workspace)"])
        if res.returncode != 0:
            print(f"BACKUP_FAIL: git commit error: {res.stderr.strip()}")
            return 1
        committed = True
    res = run(["git", "push", "origin", "master"])
    if res.returncode != 0:
        print(f"BACKUP_FAIL: git push error: {res.stderr.strip()}")
        return 1
    print(f"BACKUP_OK: {'committed and pushed' if committed else 'in sync (pushed)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
