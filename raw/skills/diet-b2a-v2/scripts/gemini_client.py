"""Thin wrapper around gemini-imagegen/gemini_auto.GeminiImageGen.
Always applies corner-logo inpainting on downloaded images.
"""
from __future__ import annotations
import os
import sys
import time
from pathlib import Path

# Import existing Gemini automation
GEMINI_ROOT = r"C:\Users\gguy\Desktop\MD\gemini-imagegen"
sys.path.insert(0, GEMINI_ROOT)
from gemini_auto import GeminiImageGen  # noqa: E402

# Import logo remover from sibling
sys.path.insert(0, str(Path(__file__).parent))
from logo_remover import process_image as _strip_logo  # noqa: E402


SESSION_DIR = str(Path(GEMINI_ROOT) / ".session")


def new_client(output_dir: str, headless: bool = False) -> GeminiImageGen:
    # Remove stale SingletonLock before start
    lock = Path(SESSION_DIR) / "SingletonLock"
    if lock.exists():
        try:
            lock.unlink()
        except Exception:
            pass
    cfg = {
        "session_dir": SESSION_DIR,
        "output_dir": output_dir,
        "headless": headless,
        "timeout_generation": 240,
        "timeout_page": 60,
        "check_interval": 5,
        "download_min_size": 10000,
        "aspect_ratio": "9:16",
    }
    gen = GeminiImageGen(cfg)
    return gen


def select_thinking_model(page, logger=None):
    """Click the top model-picker and choose '2.5 Pro' / Thinking mode.
    Gemini web UI default is Fast; we force Thinking per wiki rule.
    Returns True if a switch click happened (best-effort, silent skip otherwise).
    """
    def _log(m):
        if logger:
            logger(m)
        else:
            print(m)

    import time as _t
    # 1) open model picker
    openers = [
        'button[data-test-id="bard-mode-menu-button"]',
        'bard-mode-menu-button button',
        'button[aria-label*="모델" i]',
        'button[aria-label*="model" i]',
        '[class*="mode-menu"] button',
    ]
    opened = False
    for sel in openers:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=1500):
                btn.click()
                opened = True
                _log(f"model picker opened: {sel}")
                break
        except Exception:
            pass
    if not opened:
        _log("model picker not found (maybe already Pro/Thinking)")
        return False
    _t.sleep(1)
    # 2) pick Thinking / 2.5 Pro
    picks = [
        '[role="menuitemradio"]:has-text("Thinking")',
        '[role="menuitem"]:has-text("Thinking")',
        '[role="menuitemradio"]:has-text("사고")',
        '[role="menuitem"]:has-text("사고")',
        '[role="menuitemradio"]:has-text("2.5 Pro")',
        '[role="menuitem"]:has-text("2.5 Pro")',
        'button:has-text("2.5 Pro")',
    ]
    for sel in picks:
        try:
            it = page.locator(sel).first
            if it.is_visible(timeout=1500):
                it.click()
                _log(f"selected thinking model: {sel}")
                _t.sleep(1.5)
                return True
        except Exception:
            pass
    # close menu if open
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    _log("thinking model not clickable")
    return False


def clean_logo(path: str | Path):
    """In-place replace the image with logo-stripped version."""
    p = Path(path)
    tmp = p.with_name(p.stem + "_clean" + p.suffix)
    _strip_logo(str(p), str(tmp))
    tmp.replace(p)
    return p


def generate(
    gen: GeminiImageGen,
    prompt: str,
    upload_images: list[str],
    output_name: str,
    *,
    new_chat: bool = True,
    strip_logo: bool = True,
) -> str | None:
    if new_chat:
        gen.new_chat()
    time.sleep(2)
    # Ensure Thinking model on every new chat (Gemini sometimes resets to Fast)
    try:
        select_thinking_model(gen.page, logger=gen.log)
    except Exception as e:
        gen.log(f"thinking model toggle failed: {e}")
    if upload_images:
        if not gen.upload_files(upload_images):
            gen.log("upload failed")
            return None
    gen.send_prompt(prompt)
    if not gen.wait_for_generation():
        gen.log("generation timeout")
    path = gen.download_image(output_name)
    if path and strip_logo:
        try:
            clean_logo(path)
            gen.log(f"logo stripped: {path}")
        except Exception as e:
            gen.log(f"logo strip failed: {e}")
    return path
