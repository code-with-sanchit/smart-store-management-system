"""
SnapKart Logo Utilities.
Manages the application's official brand logos (with text and without text)
for Tkinter windows, headers, PDF receipts, and PDF reports.
"""

from __future__ import annotations

import sys
from pathlib import Path
from PIL import Image, ImageTk

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

LOGO_DIR = PROJECT_ROOT / "logo"
LOGO_APP_ICON = LOGO_DIR / "snapkart_app_icon.png"
LOGO_EMBLEM_TRANSPARENT = LOGO_DIR / "snapkart_emblem_transparent.png"
LOGO_BRAND_HORIZONTAL = LOGO_DIR / "snapkart_brand_horizontal.png"
LOGO_ICO = LOGO_DIR / "snapkart.ico"

# Backwards-compatible legacy constants
LOGO_NO_TEXT = LOGO_APP_ICON if LOGO_APP_ICON.is_file() else (LOGO_DIR / "Neon Blue Futuristic Shopping Cart.png")
LOGO_WITH_TEXT = LOGO_BRAND_HORIZONTAL if LOGO_BRAND_HORIZONTAL.is_file() else (LOGO_DIR / "SnapKart Smart Store Logo.png")

_LOGO_CACHE: dict[tuple[bool, tuple[int, int], bool], ImageTk.PhotoImage] = {}
_WINDOW_ICON_REF: dict[int, ImageTk.PhotoImage] = {}


def get_logo_path(with_text: bool = False, as_badge: bool = True) -> Path:
    """Returns the Path to the requested logo asset."""
    if with_text:
        if LOGO_BRAND_HORIZONTAL.is_file():
            return LOGO_BRAND_HORIZONTAL
        legacy = LOGO_DIR / "SnapKart Smart Store Logo.png"
        if legacy.is_file():
            return legacy
    else:
        if as_badge and LOGO_APP_ICON.is_file():
            return LOGO_APP_ICON
        if LOGO_EMBLEM_TRANSPARENT.is_file():
            return LOGO_EMBLEM_TRANSPARENT
        legacy = LOGO_DIR / "Neon Blue Futuristic Shopping Cart.png"
        if legacy.is_file():
            return legacy

    return LOGO_DIR


def get_logo_image(
    with_text: bool = False,
    size: tuple[int, int] = (40, 40),
    as_badge: bool = True
) -> ImageTk.PhotoImage | None:
    """
    Returns a cached, high-quality Tkinter PhotoImage for the requested logo.
    - with_text=False: Clean SnapKart emblem badge (for window icons, navbar, headers)
    - with_text=True: Full SnapKart Brand lockup with typography (for wide banners)
    """
    cache_key = (with_text, size, as_badge)
    if cache_key in _LOGO_CACHE:
        return _LOGO_CACHE[cache_key]

    path = get_logo_path(with_text=with_text, as_badge=as_badge)
    if not path.is_file():
        return None

    try:
        with Image.open(path) as img:
            resized = img.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized)
            _LOGO_CACHE[cache_key] = photo
            return photo
    except Exception as e:
        print(f"Error loading logo ({path}): {e}")
        return None


def set_window_icon(window, size: tuple[int, int] = (64, 64)) -> bool:
    """
    Sets the window icon using the clean emblem app badge.
    On Windows, sets native iconbitmap where possible and applies iconphoto.
    Keeps a persistent reference on the window to prevent Python garbage collection.
    """
    success = False
    try:
        # Try native Windows .ico first if present for crisp taskbar rendering
        if LOGO_ICO.is_file():
            try:
                window.iconbitmap(str(LOGO_ICO))
                success = True
            except Exception:
                pass

        icon_img = get_logo_image(with_text=False, size=size, as_badge=True)
        if icon_img is not None:
            window.iconphoto(False, icon_img)
            _WINDOW_ICON_REF[id(window)] = icon_img
            success = True
    except Exception as e:
        print(f"Notice: Could not set window icon: {e}")

    return success
