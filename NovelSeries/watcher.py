#!/usr/bin/env python3
"""Auto-git watcher for Moonbound NovelSeries directory.
Polls for file changes, auto-commits, pushes after 60s of no changes.
Run via schtasks /sc onlogon to persist across reboots.
"""
import os
import subprocess
import time
import sys
from datetime import datetime

WATCH_DIR = os.path.expanduser("F:/01_Ventures/NovelSeries")
LOG_FILE = os.path.expanduser("F:/01_Ventures/NovelSeries/watcher.log")
PUSH_INTERVAL = 60  # seconds of no changes before pushing
POLL_INTERVAL = 5   # seconds between checks
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} {msg}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(line)
        f.flush()

def has_changes():
    """Check if git status shows uncommitted changes."""
    try:
        result = subprocess.run(
            ["git", "-C", WATCH_DIR, "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        return bool(result.stdout.strip())
    except Exception as e:
        log(f"ERROR checking status: {e}")
        return False

def auto_commit():
    """Stage all changes and commit."""
    try:
        subprocess.run(
            ["git", "-C", WATCH_DIR, "add", "-A"],
            capture_output=True, text=True, timeout=10
        )
        result = subprocess.run(
            ["git", "-C", WATCH_DIR, "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        if not result.stdout.strip():
            return  # Nothing to commit
        # Count changed files
        files = [l for l in result.stdout.strip().split('\n') if l]
        count = len(files)
        message = f"Auto-commit: {count} file(s) changed"
        subprocess.run(
            ["git", "-C", WATCH_DIR, "commit", "-m", message],
            capture_output=True, text=True, timeout=10
        )
        log(f"Committed {count} file(s): {message}")
    except Exception as e:
        log(f"ERROR committing: {e}")

def push():
    """Push to remote origin."""
    if not GITHUB_TOKEN:
        log("WARNING: GITHUB_TOKEN not set, skipping push")
        return
    try:
        # Use token-based URL for push
        remote_url = subprocess.run(
            ["git", "-C", WATCH_DIR, "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=10
        ).stdout.strip()
        
        # Replace URL with token-authenticated version
        if "github.com" in remote_url:
            authenticated_url = remote_url.replace(
                "https://github.com",
                f"https://{GITHUB_TOKEN}@github.com"
            )
            subprocess.run(
                ["git", "-C", WATCH_DIR, "remote", "set-url", "origin", authenticated_url],
                capture_output=True, text=True, timeout=10
            )
        
        result = subprocess.run(
            ["git", "-C", WATCH_DIR, "push", "origin", "main"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            log("Pushed successfully")
        else:
            log(f"Push failed: {result.stderr[:200]}")
    except Exception as e:
        log(f"ERROR pushing: {e}")

def main():
    log("Watcher started")
    push_countdown = PUSH_INTERVAL  # Start counting immediately
    
    while True:
        try:
            changed = has_changes()
            if changed:
                push_countdown = PUSH_INTERVAL  # Reset countdown
                auto_commit()
            else:
                push_countdown -= POLL_INTERVAL
                if push_countdown <= 0:
                    push()
                    push_countdown = PUSH_INTERVAL
        except Exception as e:
            log(f"ERROR in main loop: {e}")
        
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
