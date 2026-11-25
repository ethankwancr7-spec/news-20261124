"""Contest entry point (Python 3.13, standard library only)."""
from pathlib import Path
import os
from shutil import copyfile

ARTWORK = Path(__file__).resolve().parent / "assets" / "entry.png"


def main():
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    copyfile(ARTWORK, destination / "entry.png")


if __name__ == "__main__":
    main()
