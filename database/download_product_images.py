import os
import sys
from database.generate_real_photos import download_and_generate_photos

if __name__ == "__main__":
    print("Creating local product artwork...")
    created = download_and_generate_photos()
    print(f"Created {created} locally generated catalogue images.")
