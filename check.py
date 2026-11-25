"""Offline preflight of this entry's 8-bit, non-interlaced RGB PNG."""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import os
import struct
import subprocess
from uuid import uuid4
import sys
import zlib


def inspect(data):
    assert len(data) <= 1_048_576, "Image exceeds the file-size limit"
    stream = BytesIO(data)
    assert stream.read(8) == b"\x89PNG\r\n\x1a\n", "Not PNG"
    compressed = bytearray()
    kinds = []
    while True:
        length, kind = struct.unpack(">I4s", stream.read(8))
        payload = stream.read(length)
        assert len(payload) == length, "Truncated chunk"
        expected, = struct.unpack(">I", stream.read(4))
        assert zlib.crc32(kind + payload) == expected, "Invalid chunk checksum"
        kinds.append(kind)
        if kind == b"IHDR":
            assert len(kinds) == 1
            assert struct.unpack(">IIBBBBB", payload) == (1024, 1024, 8, 2, 0, 0, 0)
        if kind == b"IDAT":
            compressed.extend(payload)
        if kind == b"IEND":
            assert length == 0 and not stream.read()
            break
    assert kinds[0] == b"IHDR" and b"IDAT" in kinds
    inflater = zlib.decompressobj()
    pixels = inflater.decompress(compressed) + inflater.flush()
    assert inflater.eof and not inflater.unused_data and not inflater.unconsumed_tail
    stride = 1 + 3 * 1024
    assert len(pixels) == 1024 * stride and max(pixels[::stride]) <= 4


def main():
    if not __debug__:
        raise SystemExit("Run check.py without -O to enable validation.")
    root = Path(__file__).resolve().parent
    master = root / "assets" / "entry.png"
    original = master.read_bytes()
    inspect(original)
    print(f"PASS assets/entry.png: complete 1024 x 1024 RGB PNG, {len(original)} bytes")

    # With no arguments, exercise the grading program itself. Use fresh,
    # initially absent output paths, and leave no copies in the source tree.
    scratch = root / "_review" / uuid4().hex
    for run in (1, 2):
        destination = scratch / f"run-{run}"
        assert not destination.exists()
        subprocess.run(
            [sys.executable, "-B", str(root / "main.py")],
            env={**os.environ, "MAKEFUN_OUTPUT_DIR": str(destination)},
            check=True,
        )
        output = destination / "entry.png"
        data = output.read_bytes()
        inspect(data)
        assert data == original, f"Output from run {run} differs from master"
        print(f"PASS run {run}: created new output directory; identical PNG")
        output.unlink()
        destination.rmdir()
    scratch.rmdir()

    for filename in sys.argv[1:]:
        data = Path(filename).read_bytes()
        inspect(data)
        assert data == original, f"{filename} differs from master"
        print(f"PASS {filename}: identical PNG")
    print("SHA-256:", sha256(original).hexdigest())


if __name__ == "__main__":
    main()
