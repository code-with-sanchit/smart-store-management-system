"""Deprecated name retained for old project instructions."""

from database.generate_local_artwork import build_artwork


def download_and_generate_photos() -> int:
    """Create local catalogue artwork without using the internet."""
    return build_artwork()


if __name__ == "__main__":
    print(f"Created {download_and_generate_photos()} local product images.")
