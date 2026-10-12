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
LOGO_NO_TEXT = LOGO_DIR / "Neon Blue Futuristic Shopping Cart.png"
LOGO_WITH_TEXT = LOGO_DIR / "SnapKart Smart Store Logo.png"

_LOGO_CACHE: dict[tuple[bool, tuple[int, int]], ImageTk.PhotoImage] = {}
_WINDOW_ICON_REF: dict[int, ImageTk.PhotoImage] = {}


def get_logo_path(with_text: bool = False) -> Path:
    """Returns the Path to the requested logo asset."""
    target = LOGO_WITH_TEXT if with_text else LOGO_NO_TEXT
    if target.is_file():
        return target
    # Fallback if specific file missing
    alt = LOGO_NO_TEXT if with_text else LOGO_WITH_TEXT
    if alt.is_file():
        return alt
    return LOGO_DIR


def get_logo_image(with_text: bool = False, size: tuple[int, int] = (40, 40)) -> ImageTk.PhotoImage | None:
    """
    Returns a cached, high-quality Tkinter PhotoImage for the requested logo.
    - with_text=False: Neon Blue Futuristic Shopping Cart emblem (for window icons, navbar icons)
    - with_text=True: Full SnapKart Smart Store Logo with branding typography (for banners, dialog headers)
    """
    cache_key = (with_text, size)
    if cache_key in _LOGO_CACHE:
        return _LOGO_CACHE[cache_key]

    path = get_logo_path(with_text=with_text)
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
    Sets the window icon using the clean emblem logo (without text).
    Keeps a persistent reference on the window to prevent Python garbage collection.
    """
    try:
        icon_img = get_logo_image(with_text=False, size=size)
        if icon_img is not None:
            window.iconphoto(False, icon_img)
            # Store reference to prevent garbage collection
            _WINDOW_ICON_REF[id(window)] = icon_img
            return True
    except Exception as e:
        print(f"Notice: Could not set window icon: {e}")
    return False
