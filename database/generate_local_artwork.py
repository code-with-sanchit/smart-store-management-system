"""Create lightweight local catalogue art without downloading anything from the web."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common.image_loader import ASSETS_DIR, CATALOG_DIR, product_image_key
from database.curated_catalog import CURATED_CATALOG


CATEGORY_COLORS = {
    "Grocery & Staples": (184, 116, 46), "Dairy, Milk & Paneer": (58, 125, 184),
    "Fresh Vegetables & Greens": (44, 132, 83), "Fresh Fruits & Berries": (208, 80, 77),
    "Bakery & Breakfast": (189, 120, 62), "Snacks, Chips & Namkeen": (222, 142, 35),
    "Chocolates, Sweets & Biscuits": (126, 74, 58), "Tea, Coffee & Beverages": (64, 116, 151),
    "Personal Care & Grooming": (184, 86, 150), "Health, Wellness & Supplements": (72, 133, 115),
    "All Medicines & First Aid": (204, 66, 66), "Household & Cleaning": (72, 135, 171),
    "Home & Kitchenware": (104, 101, 165), "Stationery & Office Supplies": (57, 133, 166),
    "Clothing & Fashion": (157, 89, 128), "Girls Accessories & Makeup": (198, 97, 139),
    "Tech & Mobile Accessories": (67, 99, 157), "Seasonal, Pooja & Festival": (180, 87, 51),
    "Ready to Eat": (173, 107, 52), "Sports & Fitness": (58, 130, 100),
}


def _font(size: int, bold: bool = False):
    try:
        return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def _slug(category: str) -> str:
    return category.lower().replace("&", "and").replace(",", "").replace(" ", "_")


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and draw.textbbox((0, 0), candidate, font=font)[2] > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    return lines + ([current] if current else [])


def create_product_art(category: str, name: str, destination: Path) -> None:
    """Render a clean shelf-card image with category colour and product label."""
    base = CATEGORY_COLORS.get(category, (71, 85, 105))
    image = Image.new("RGB", (640, 400), base)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((22, 22, 618, 378), radius=28, fill=(255, 255, 255))
    draw.rounded_rectangle((42, 42, 598, 178), radius=20, fill=base)
    draw.ellipse((268, 66, 372, 170), fill=(255, 255, 255))
    draw.rectangle((298, 90, 342, 150), fill=base)
    draw.text((62, 202), category.upper(), fill=base, font=_font(18, True))
    y = 236
    for line in _wrap(draw, name, _font(30, True), 510)[:3]:
        draw.text((62, y), line, fill=(15, 23, 42), font=_font(30, True))
        y += 42
    draw.text((62, 344), "SnapKart curated catalogue", fill=(100, 116, 139), font=_font(17))
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "PNG", optimize=True)


def build_artwork() -> int:
    """Regenerate category and exact-product artwork for the curated starter list."""
    generated = 0
    for category in {category for category, _, _, _ in CURATED_CATALOG}:
        create_product_art(category, category, ASSETS_DIR / f"{_slug(category)}.png")
        generated += 1
    for category, name, _, _ in CURATED_CATALOG:
        create_product_art(category, name, CATALOG_DIR / f"{product_image_key(name)}.png")
        generated += 1
    return generated


if __name__ == "__main__":
    print(f"Created {build_artwork()} local catalogue images.")
