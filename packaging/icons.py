#!/usr/bin/env python3
"""Regenerate the PDFKraft app icon set from the geometry in assets/app-icon/pdfkraft.svg.

The mark is geometric (a rounded tile, a K drawn as three butt-capped strokes, and a dot), so this
script re-states the same numbers and rasterises them itself: no font, no SVG renderer, nothing
but the Python standard library. The outputs are committed, so building and packaging never need
it. After running it, refresh the sha256 values in ATTRIBUTION.toml (`packaging/icons.py` prints
them), then `cargo xtask assets --write`.

    python3 packaging/icons.py

Writes, under assets/app-icon/:
  pdfkraft-1024.png                      1024 px on Apple's grid (824 px body on a transparent canvas)
  pdfkraft.icns                          macOS icon, 16-1024 px, each on Apple's grid
  pdfkraft.ico                           Windows icon, 16-256 px, full bleed
  hicolor/<n>x<n>/apps/<app id>.png      Linux hicolor theme, 16-512 px, full bleed
"""

import hashlib
import math
import pathlib
import struct
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "assets" / "app-icon"
APP_ID = "io.github.kompheak7711.pdfkraft"

# The geometry, in the master's 512-unit space (see assets/app-icon/pdfkraft.svg).
TILE_RADIUS = 112.0
STROKE = 68.0
STEM = ((176.0, 116.0), (176.0, 396.0))
ARM = ((176.0, 256.0), (340.0, 120.0))
LEG = ((176.0, 256.0), (368.0, 396.0))
DOT = (412.0, 136.0, 26.0)
BLUE = (0x1B, 0x3A, 0x6B)
PAPER = (0xF4, 0xF1, 0xEA)
RED = (0xC8, 0x10, 0x2E)


def in_tile(x, y):
    """Inside the rounded 512 tile."""
    if not (0.0 <= x < 512.0 and 0.0 <= y < 512.0):
        return False
    r = TILE_RADIUS
    cx = r if x < r else 512.0 - r if x > 512.0 - r else x
    cy = r if y < r else 512.0 - r if y > 512.0 - r else y
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def near_segment(x, y, seg):
    """Within half a stroke of a butt-capped segment."""
    (ax, ay), (bx, by) = seg
    dx, dy = bx - ax, by - ay
    t = ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)
    if t < 0.0 or t > 1.0:
        return False
    px, py = ax + t * dx, ay + t * dy
    return (x - px) ** 2 + (y - py) ** 2 <= (STROKE / 2.0) ** 2


def colour_at(x, y):
    """The colour under one sample point, or None outside the tile."""
    if not in_tile(x, y):
        return None
    cx, cy, r = DOT
    if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
        return RED
    if near_segment(x, y, STEM) or near_segment(x, y, ARM) or near_segment(x, y, LEG):
        return PAPER
    return BLUE


def render(size, pad=0):
    """RGBA rows for a `size` px canvas with the tile filling `size - 2 * pad` px of it."""
    body = size - 2 * pad
    scale = 512.0 / body
    ss = max(2, min(8, 2048 // size))  # supersampling per axis
    inv = 1.0 / (ss * ss)
    rows = []
    for py in range(size):
        row = bytearray()
        for px in range(size):
            r = g = b = a = 0.0
            for sy in range(ss):
                y = (py - pad + (sy + 0.5) / ss) * scale
                if y < 0.0 or y >= 512.0:
                    continue
                for sx in range(ss):
                    x = (px - pad + (sx + 0.5) / ss) * scale
                    c = colour_at(x, y)
                    if c is None:
                        continue
                    r += c[0]
                    g += c[1]
                    b += c[2]
                    a += 1.0
            if a == 0.0:
                row += b"\0\0\0\0"
            else:
                # Straight (non-premultiplied) colour of the covered part, coverage as alpha.
                row += bytes((round(r / a), round(g / a), round(b / a), round(255.0 * a * inv)))
        rows.append(bytes(row))
    return rows


def png(size, rows):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    raw = b"".join(b"\0" + row for row in rows)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def ico(blobs):
    head = struct.pack("<HHH", 0, 1, len(blobs))
    entries, data, offset = b"", b"", 6 + 16 * len(blobs)
    for size, blob in blobs:
        entries += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(blob), offset)
        data += blob
        offset += len(blob)
    return head + entries + data


def icns(blobs):
    body = b"".join(kind + struct.pack(">I", 8 + len(blob)) + blob for kind, blob in blobs)
    return b"icns" + struct.pack(">I", 8 + len(body)) + body


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print(f"{hashlib.sha256(data).hexdigest()}  {path.relative_to(ROOT)}")


def main():
    full = {}
    for s in (16, 20, 24, 32, 40, 48, 64, 128, 256, 512):
        full[s] = png(s, render(s))
    for s in (16, 24, 32, 48, 64, 128, 256, 512):
        write(DIR / "hicolor" / f"{s}x{s}" / "apps" / f"{APP_ID}.png", full[s])
    write(DIR / "pdfkraft.ico", ico([(s, full[s]) for s in (16, 20, 24, 32, 40, 48, 64, 128, 256)]))
    # Apple's grid: the body is 824/1024 of the canvas at every size.
    mac = {s: png(s, render(s, pad=round(s * 100 / 1024))) for s in (16, 32, 64, 128, 256, 512, 1024)}
    write(DIR / "pdfkraft-1024.png", mac[1024])
    kinds = [(b"icp4", 16), (b"icp5", 32), (b"icp6", 64), (b"ic07", 128), (b"ic08", 256), (b"ic09", 512), (b"ic10", 1024)]
    write(DIR / "pdfkraft.icns", icns([(k, mac[s]) for k, s in kinds]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
