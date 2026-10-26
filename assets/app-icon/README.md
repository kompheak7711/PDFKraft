# PDFKraft app icon

<img src="pdfkraft-small.svg" alt="PDFKraft app icon: a white K and a red dot on a deep blue tile" width="128">

A geometric mark: a **K** drawn as three butt-capped strokes and a dot, on a full-bleed colour
field. No font, no traced artwork, nothing from the upstream project's icon.

**Palette:** exactly three colours.

| Colour | Hex | Used for |
|---|---|---|
| Paper | `#f4f1ea` | the K |
| Khmer red | `#c8102e` | the dot |
| PDFKraft blue | `#1b3a6b` | the full-bleed field |

**Tile:** `viewBox="0 0 512 512"`, a rounded square with `rx=112` that clips everything. Windows and
Linux icons use the full-bleed tile. macOS icons put it on Apple's grid (an 824 px body centred on a
transparent 1024 px canvas).

**Provenance:** contributor-original, defined by the numbers in `pdfkraft.svg` and re-stated in
`packaging/icons.py`, which rasterises every PNG, the `.ico` and the `.icns` with the Python
standard library alone. Licence: [LICENSE.txt](LICENSE.txt) (`MIT OR Apache-2.0`, like the repo).

## Files

| File | What it is |
|---|---|
| `pdfkraft.svg` | the master vector; every PNG, `.ico` and `.icns` follows its geometry |
| `pdfkraft-small.svg` | the same vector, kept under the name the README and the About dialog use |
| `pdfkraft-1024.png` | 1024 px on Apple's grid; also the runtime Dock icon on macOS |
| `pdfkraft.icns` | macOS icon (16–1024 px) |
| `pdfkraft.ico` | Windows icon (16–256 px), embedded in `pdfkraft.exe` by `apps/pdfkraft/build.rs` |
| `pdfkraft-document.svg` | Windows PDF file icon master: a Lucide document outline, badge and outlined PDF lettering; no font dependency |
| `pdfkraft-document.ico` | Windows PDF file icon (16–256 px), embedded as resource 2 in `pdfkraft.exe` |
| `hicolor/<n>x<n>/apps/io.github.kompheak7711.pdfkraft.png` | Linux hicolor theme, 16–512 px; the 256 px one is the runtime icon on Windows and Linux |
| `hicolor/scalable/apps/io.github.kompheak7711.pdfkraft.svg` | Linux scalable icon (copy of the master) |

Regenerate with `python3 packaging/icons.py`, then refresh the hashes in `ATTRIBUTION.toml` and run
`cargo xtask assets --write`.
