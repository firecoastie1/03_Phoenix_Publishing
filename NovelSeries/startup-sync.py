#!/usr/bin/env python3
"""
On-startup sync for Moonbound NovelSeries.
Runs when Hermes starts. Compares local repo with remote,
pulls if remote is newer, pushes if local is newer.
"""
import os
import subprocess
import sys

WATCH_DIR = os.path.expanduser("F:/01_Ventures/NovelSeries")
LOG_FILE = os.path.expanduser("F:/01_Ventures/NovelSeries/watcher.log")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def log(msg):
    ts = __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} {msg}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(line)
        f.flush()

def run_git(*args):
    """Run a git command and return (stdout, stderr, returncode)."""
    try:
        result = subprocess.run(
            ["git", "-C", WATCH_DIR] + list(args),
            capture_output=True, text=True, timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def ensure_token_url():
    """Ensure remote URL has token for auth."""
    if not GITHUB_TOKEN:
        log("WARNING: GITHUB_TOKEN not set — push will fail")
        return False
    remote_url, _, _ = run_git("remote", "get-url", "origin")
    remote_url = remote_url.strip()
    if "github.com" in remote_url and GITHUB_TOKEN not in remote_url:
        authenticated_url = remote_url.replace(
            "https://github.com",
            f"https://{GITHUB_TOKEN}@github.com"
        )
        run_git("remote", "set-url", "origin", authenticated_url)
    return True

def sync():
    """Pull if remote is newer, push if local is newer."""
    log("=== Startup sync ===")

    # First, pull any changes from remote
    log("Checking for remote changes...")
    stdout, stderr, rc = run_git("fetch", "origin")
    if rc != 0:
        log(f"FETCH failed: {stderr[:200]}")
        return
    log("Fetch OK")

    # Compare HEAD with origin/HEAD
    local_head, _, _ = run_git("rev-parse", "HEAD")
    remote_head, _, _ = run_git("rev-parse", "origin/HEAD")

    if local_head.strip() == remote_head.strip():
        log("Local and remote are in sync. Nothing to do.")
        return

    # Check if remote is ahead of local (we need to pull)
    stdout, stderr, rc = run_git("merge-base", "--is-ancestor", "HEAD", "origin/HEAD")
    remote_ahead = (rc == 0)

    if remote_ahead:
        log("Remote is newer. Pulling...")
        stdout, stderr, rc = run_git("pull", "origin", "HEAD")
        if rc == 0:
            log(f"Pull OK: {stdout.strip()[:100]}")
        else:
            log(f"PULL failed: {stderr[:200]}")
            # Try rebase if merge conflicts
            log("Trying rebase instead...")
            stdout, stderr, rc = run_git("pull", "--rebase", "origin", "HEAD")
            if rc == 0:
                log(f"Rebase pull OK: {stdout.strip()[:100]}")
            else:
                log(f"Rebase pull also failed: {stderr[:200]}")
                log("Manual resolution needed.")
        return

    # Local is ahead of remote (we need to push)
    log("Local is newer. Pushing...")
    stdout, stderr, rc = run_git("push", "origin", "HEAD")
    if rc == 0:
        log("Push OK")
    else:
        log(f"PUSH failed: {stderr[:200]}")
        # Maybe need to pull first then rebase
        log("Trying pull --rebase then push...")
        stdout, stderr, rc = run_git("pull", "--rebase", "origin", "HEAD")
        if rc == 0:
            stdout, stderr, rc = run_git("push", "origin", "HEAD")
            if rc == 0:
                log("Rebase + push OK")
            else:
                log(f"Push after rebase failed: {stderr[:200]}")
        else:
            log(f"Pull-rebase also failed: {stderr[:200]}")

    log("=== Startup sync complete ===")

if __name__ == "__main__":
    log("=== Startup sync starting ===")
    ensure_token_url()
    sync()
