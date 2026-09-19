import sys
from pathlib import Path

from PIL import Image

if len(sys.argv) != 2:
    print("Usage: python convert_jpg_to_webp.py <jpg_file>")
    sys.exit(1)

jpg_file = Path(sys.argv[1])

with Image.open(jpg_file) as img:
    img.save(jpg_file.with_suffix(".webp"), "webp", quality=100)
