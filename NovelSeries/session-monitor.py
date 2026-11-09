#!/usr/bin/env python3
"""
Hermes session monitor for Moonbound NovelSeries.
Monitors whether the Hermes desktop app (or any hermes process) is running.
When Hermes is running, it polls for git changes and auto-pushes.
When Hermes closes, it does a final push of any pending changes.
Runs as a background process via Windows Scheduled Task or the watcher.
"""
import os
import subprocess
import time
import sys
import signal

WATCH_DIR = os.path.expanduser("F:/01_Ventures/03_Phoenix Publishing/NovelSeries")
LOG_FILE = os.path.expanduser("F:/01_Ventures/03_Phoenix Publishing/NovelSeries/watcher.log")
POLL_INTERVAL = 5
PUSH_INTERVAL = 60
HERMES_CHECK_INTERVAL = 15  # how often to check if Hermes is still running
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def log(msg):
    ts = __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} {msg}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(line)
        f.flush()

def run_git(*args):
    try:
        result = subprocess.run(
            ["git", "-C", WATCH_DIR] + list(args),
            capture_output=True, text=True, timeout=10
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def has_changes():
    stdout, _, _ = run_git("status", "--porcelain")
    return bool(stdout.strip())

def auto_commit():
    stdout, stderr, rc = run_git("add", "-A")
    if rc != 0:
        log(f"Add failed: {stderr[:200]}")
        return
    stdout, _, _ = run_git("status", "--porcelain")
    if not stdout.strip():
        return
    files = [l for l in stdout.strip().split('\n') if l]
    count = len(files)
    msg = f"Auto-commit: {count} file(s) changed"
    run_git("commit", "-m", msg)
    log(f"Committed {count} file(s)")

def get_hermes_pids():
    """Return list of PIDs for hermes-related processes."""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq hermes.exe", "/NH", "/FO", "CSV"],
            capture_output=True, text=True, timeout=10
        )
        pids = []
        for line in result.stdout.strip().split('\n'):
            line = line.strip().strip('"')
            if line and line.isdigit():
                pids.append(int(line))
        # Also check for hermes in the desktop process
        result2 = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Electron.exe", "/NH", "/FO", "CSV"],
            capture_output=True, text=True, timeout=10
        )
        # The desktop app uses Electron — hard to distinguish without more work
        # Return what we found
        return pids
    except Exception as e:
        log(f"PID check error: {e}")
        return []

def is_hermes_running():
    """Check if any hermes process is alive."""
    pids = get_hermes_pids()
    if not pids:
        # Also check via process list name
        try:
            result = subprocess.run(
                ["wmic", "process", "where", "name like '%hermes%'", "get", "ProcessId", "/NH"],
                capture_output=True, text=True, timeout=10
            )
            lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip().isdigit()]
            return len(lines) > 0
        except:
            return False
    return True

def ensure_token_url():
    if not GITHUB_TOKEN:
        return False
    remote_url, _, _ = run_git("remote", "get-url", "origin")
    remote_url = remote_url.strip()
    if "github.com" in remote_url and GITHUB_TOKEN not in remote_url:
        auth_url = remote_url.replace(
            "https://github.com",
            f"https://{GITHUB_TOKEN}@github.com"
        )
        run_git("remote", "set-url", "origin", auth_url)
    return True

def push():
    stdout, stderr, rc = run_git("push", "origin", "HEAD")
    if rc == 0:
        log("Push OK")
        return True
    else:
        log(f"Push failed: {stderr[:200]}")
        # Try rebase + push
        stdout, stderr, rc = run_git("pull", "--rebase", "origin", "HEAD")
        if rc == 0:
            stdout, stderr, rc = run_git("push", "origin", "HEAD")
            if rc == 0:
                log("Rebase + push OK")
                return True
        log("Final push failed, manual resolution needed")
        return False

def shutdown_push():
    """Final push when Hermes closes."""
    log("=== SHUTDOWN: Hermes detected as closed, pushing pending changes ===")
    if has_changes():
        log("Pending changes detected. Committing...")
        auto_commit()
    if has_changes():
        log("Changes remain after commit — something went wrong.")
        return
    ensure_token_url()
    push()
    log("=== SHUTDOWN sync complete ===")

def main():
    log("=== Session monitor starting ===")
    ensure_token_url()
    push_countdown = PUSH_INTERVAL
    hermes_was_running = is_hermes_running()

    while True:
        try:
            # Check if Hermes is still running
            hermes_alive = is_hermes_running()

            if hermes_alive and not hermes_was_running:
                log("Hermes session detected — resuming monitoring")

            if not hermes_alive and hermes_was_running:
                log("Hermes session closed — triggering shutdown sync")
                shutdown_push()
                break  # Exit after shutdown push

            # Normal operation: watch for git changes
            if hermes_alive:
                changed = has_changes()
                if changed:
                    push_countdown = PUSH_INTERVAL
                    auto_commit()
                else:
                    push_countdown -= POLL_INTERVAL
                    if push_countdown <= 0:
                        push()
                        push_countdown = PUSH_INTERVAL

            hermes_was_running = hermes_alive

        except Exception as e:
            log(f"ERROR in main loop: {e}")

        time.sleep(POLL_INTERVAL)

    log("Session monitor exiting")

if __name__ == "__main__":
    main()
