"""Download product-image thumbnails selected from Google Images results.

The command is explicit: it does not run when the storefront opens and it
never overwrites a photo already curated by the store owner. Review images
before a public deployment.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from io import BytesIO
from pathlib import Path
from urllib.parse import quote_plus

import requests
from PIL import Image

# Support both ``python -m database.download_google_product_images`` and the
# documented direct script invocation from the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.image_loader import CATALOG_DIR, product_image_key
from database.db_connection import get_db_connection

GOOGLE_IMAGES = "https://www.google.com/search?tbm=isch&q="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
}


def fetch_google_thumbnail(session: requests.Session, product_name: str) -> Image.Image | None:
    """Get the first visible Google Images thumbnail for an exact product query."""
    response = session.get(GOOGLE_IMAGES + quote_plus(product_name), headers=HEADERS, timeout=20)
    response.raise_for_status()
    urls = re.findall(r'https://encrypted-tbn0\\.gstatic\\.com/images\\?[^"\\\\ ]+', response.text)
    for url in urls:
        try:
            image_response = session.get(url.replace("\\u003d", "="), headers=HEADERS, timeout=20)
            image_response.raise_for_status()
            with Image.open(BytesIO(image_response.content)) as image:
                return image.convert("RGB")
        except (requests.RequestException, OSError, ValueError):
            continue
    return None


def download_images(limit: int | None, query: str | None, pause: float) -> tuple[int, int]:
    conn = get_db_connection()
    if not conn:
        raise RuntimeError("Could not connect to MySQL. Start MySQL and check SNAPKART_DB_* settings.")
    cursor = conn.cursor(dictionary=True)
    try:
        sql, params = "SELECT item_id, name FROM inventory", []
        if query:
            sql += " WHERE name LIKE %s"
            params.append(f"%{query}%")
        sql += " ORDER BY item_id"
        if limit:
            sql += " LIMIT %s"
            params.append(limit)
        cursor.execute(sql, params)
        products = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    saved = skipped = 0
    with requests.Session() as session:
        for number, product in enumerate(products, start=1):
            target = CATALOG_DIR / f"{product_image_key(product['name'])}.jpg"
            if target.exists():
                skipped += 1
                continue
            try:
                image = fetch_google_thumbnail(session, product["name"])
                if image is None:
                    print(f"[{number}/{len(products)}] No result: {product['name']}")
                else:
                    image.thumbnail((600, 600), Image.Resampling.LANCZOS)
                    image.save(target, "JPEG", quality=90, optimize=True)
                    saved += 1
                    print(f"[{number}/{len(products)}] Saved: {product['name']}")
            except requests.RequestException as error:
                print(f"[{number}/{len(products)}] Request failed for {product['name']}: {error}")
            if pause:
                time.sleep(pause)
    return saved, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Download item-specific Google Images thumbnails for SnapKart.")
    parser.add_argument("--limit", type=int, help="Maximum number of items to process.")
    parser.add_argument("--query", help="Only process product names containing this text.")
    parser.add_argument("--pause", type=float, default=0.4, help="Seconds between Google queries (default: 0.4).")
    args = parser.parse_args()
    saved, skipped = download_images(args.limit, args.query, args.pause)
    print(f"Finished: {saved} downloaded, {skipped} already present. Files are in {CATALOG_DIR}.")


if __name__ == "__main__":
    main()
