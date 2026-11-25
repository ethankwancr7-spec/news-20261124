"""Copy the committed front page to /output/entry.png. Standard library only."""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets" / "entry.png"
OUTPUT_DIR = Path("/output")
OUTPUT = OUTPUT_DIR / "entry.png"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    try:
        os.chmod(OUTPUT, 0o644)
    except OSError:
        pass


if __name__ == "__main__":
    main()
