"""Verify Gemini session is still valid. Non-headless to allow user to see state."""
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

SESSION = Path(r"C:\Users\gguy\Desktop\MD\gemini-imagegen\.session")
FLAG = Path(__file__).parent / "session_ok.flag"


def main():
    if not SESSION.exists():
        print(f"ERROR: no session dir at {SESSION}")
        print("Run login_once.py first.")
        sys.exit(2)

    # Remove stale SingletonLock if present
    lock = SESSION / "SingletonLock"
    if lock.exists():
        try:
            lock.unlink()
            print("removed stale SingletonLock")
        except Exception as e:
            print("warn: could not remove SingletonLock:", e)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(SESSION), headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
            viewport=None,
            ignore_default_args=["--enable-automation"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
        time.sleep(12)
        try:
            page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            pass
        time.sleep(3)

        # Look for an input textbox (indicates logged-in chat UI)
        try:
            html = page.content()
        except Exception:
            time.sleep(4)
            html = page.content()
        logged = (
            'role="textbox"' in html
            or "zero-state" in html
            or "대화" in html or "prompt" in html.lower()
        )
        # Also check url didn't bounce to accounts.google.com
        url = page.url
        if "accounts.google" in url or "signin" in url:
            logged = False

        page.screenshot(path=str(Path(__file__).parent / "session_screenshot.png"))
        print("url=", url)
        print("logged_in=", logged)
        ctx.close()

    if logged:
        FLAG.write_text("ok", encoding="utf-8")
        print("SESSION OK ->", FLAG)
        sys.exit(0)
    else:
        print("SESSION INVALID. Run login_once.py and sign in manually with cjm@ccfm.co.kr.")
        sys.exit(3)


if __name__ == "__main__":
    main()
