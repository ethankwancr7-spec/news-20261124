"""Local checks: size, PNG signature, and two identical runs of main.py."""

import hashlib
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENTRY = ROOT / "assets" / "entry.png"
OUTPUT = Path("/output/entry.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_png_size(data):
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit("FAIL: file does not start with a PNG signature")
    if data[12:16] != b"IHDR":
        raise SystemExit("FAIL: PNG is missing an IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def run_main(destination):
    subprocess.run([sys.executable, str(ROOT / "main.py")], check=True, cwd=ROOT)
    if not OUTPUT.is_file():
        raise SystemExit("FAIL: main.py did not write /output/entry.png")
    shutil.copyfile(OUTPUT, destination)


def main():
    data = ENTRY.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"FAIL: {len(data)} bytes is over 1 MiB")
    width, height = read_png_size(data)
    if (width, height) != (1024, 1024):
        raise SystemExit(f"FAIL: image is {width}x{height}, expected 1024x1024")

    with tempfile.TemporaryDirectory() as temp_name:
        folder = Path(temp_name)
        first = folder / "run-1.png"
        second = folder / "run-2.png"
        run_main(first)
        run_main(second)
        first_hash = sha256(first.read_bytes())
        second_hash = sha256(second.read_bytes())

    if first_hash != second_hash:
        raise SystemExit("FAIL: two runs of main.py wrote different bytes")
    if first_hash != sha256(data):
        raise SystemExit("FAIL: /output/entry.png does not match assets/entry.png")

    print("PASS")
    print(f"{width}x{height}, {len(data)} bytes, sha256 {first_hash}")


if __name__ == "__main__":
    main()
