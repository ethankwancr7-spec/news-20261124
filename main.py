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
    os.chmod(OUTPUT_DIR, 0o755)
    shutil.copyfile(SOURCE, OUTPUT)
    os.chmod(OUTPUT, 0o644)


if __name__ == "__main__":
    main()
