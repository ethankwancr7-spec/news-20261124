"""Contest entry point (Python 3.13, standard library only)."""
from pathlib import Path
import os
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

ARTWORK = Path(__file__).resolve().parent / "assets" / "entry.png"


def main():
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "entry.png"
    try:
        if target.samefile(ARTWORK):
            return  # The master, even through a path alias, is already published.
    except FileNotFoundError:
        pass

    # Only the final rename touches the public path. Each writer owns a
    # separate staging file on the same filesystem as the target.
    staged = None
    try:
        with NamedTemporaryFile(dir=destination, prefix=".entry-", suffix=".tmp",
                                delete=False) as stream:
            staged = Path(stream.name)
            with ARTWORK.open("rb") as source:
                copyfileobj(source, stream)
            stream.flush()
            os.fsync(stream.fileno())
        staged.chmod(0o644)
        os.replace(staged, target)
        staged = None
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
