"""Local product-photo loading for the customer catalogue."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps, ImageTk

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "products"
ITEMS_DIR = ASSETS_DIR / "items"
CATALOG_DIR = ASSETS_DIR / "catalog"
for directory in (ASSETS_DIR, ITEMS_DIR, CATALOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)

_TK_IMAGE_CACHE: dict[tuple[int, tuple[int, int]], ImageTk.PhotoImage] = {}
_IMAGE_EXTENSIONS = (".webp", ".png", ".jpg", ".jpeg")


def product_image_key(item_name: str) -> str:
    """Make a stable filename key without conflating different products."""
    normalized = re.sub(r"[^a-z0-9]+", "-", item_name.lower()).strip("-")
    digest = hashlib.sha1(item_name.encode("utf-8")).hexdigest()[:10]
    return f"{normalized[:90]}-{digest}"


def _find_image(item_id: int, item_name: str, category: str = "") -> Path | None:
    """Return an item photo, then an exact-name catalogue photo, then category photo if available."""
    for directory, stem in ((ITEMS_DIR, str(item_id)), (CATALOG_DIR, product_image_key(item_name))):
        for extension in _IMAGE_EXTENSIONS:
            candidate = directory / f"{stem}{extension}"
            if candidate.is_file():
                return candidate

    if category:
        cat_slug = category.lower().replace("&", "and").replace(",", "").replace(" ", "_").strip()
        cat_file = ASSETS_DIR / f"{cat_slug}.png"
        if cat_file.is_file():
            return cat_file

    return None


def _unavailable_photo(size: tuple[int, int]) -> ImageTk.PhotoImage | None:
    """Use an honest unavailable state if no photo exists."""
    try:
        image = Image.new("RGBA", size, "#f8fafc")
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, size[0] - 1, size[1] - 1), outline="#cbd5e1", width=1)
        draw.text((16, max(12, size[1] // 2 - 8)), "Product photo unavailable", fill="#64748b")
        return ImageTk.PhotoImage(image)
    except Exception:
        return None


def get_product_image(item_id: int | str, item_name: str, category: str, size: tuple[int, int] = (210, 110)) -> ImageTk.PhotoImage | None:
    """Return the photo for a product, sized for a Tk card.

    Checks item-specific photo first, then exact catalog photo, then
    category department photo, and falls back to a clean placeholder.
    """
    try:
        numeric_id = int(item_id)
    except (ValueError, TypeError):
        numeric_id = 0

    cache_key = (numeric_id, size)
    if cache_key in _TK_IMAGE_CACHE:
        return _TK_IMAGE_CACHE[cache_key]

    target_file = _find_image(numeric_id, item_name, category)
    if target_file:
        try:
            with Image.open(target_file) as source:
                image = ImageOps.contain(source.convert("RGBA"), size, Image.Resampling.LANCZOS)
            canvas = Image.new("RGBA", size, "#ffffff")
            canvas.alpha_composite(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
            ImageDraw.Draw(canvas).rectangle((0, 0, size[0] - 1, size[1] - 1), outline="#e2e8f0", width=1)
            photo = ImageTk.PhotoImage(canvas)
            _TK_IMAGE_CACHE[cache_key] = photo
            return photo
        except Exception as error:
            print(f"Could not render product image {target_file}: {error}")

    photo = _unavailable_photo(size)
    if photo is not None:
        _TK_IMAGE_CACHE[cache_key] = photo
    return photo
