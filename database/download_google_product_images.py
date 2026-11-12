"""Deprecated compatibility command for locally generated product artwork."""

from database.generate_local_artwork import build_artwork


if __name__ == "__main__":
    print(f"Created {build_artwork()} local product images.")
