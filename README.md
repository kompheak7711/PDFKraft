<p align="center">
  <img src="assets/app-icon/pdfkraft-small.svg" width="128" height="128" alt="PDFKraft icon: a white K and a red dot on a deep blue tile">
</p>

<h1 align="center">PDFKraft</h1>

<p align="center">
  <b>The PDF workbench that types Khmer.</b><br>
  Read, organize, combine, split, secure and edit PDFs in a fast, native app written in Rust,
  and add Khmer Unicode text to any page with the bundled Khmer fonts.<br>
  macOS · Windows · Linux · FreeBSD · the web
</p>

<p align="center">
  <img alt="License: MIT OR Apache-2.0" src="https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-1b3a6b?style=flat-square">
  <img alt="Written in Rust" src="https://img.shields.io/badge/written%20in-Rust-1b3a6b?style=flat-square">
  <img alt="Khmer Unicode" src="https://img.shields.io/badge/types-%E1%9E%81%E1%9F%92%E1%9E%98%E1%9F%82%E1%9E%9A-c8102e?style=flat-square">
  <img alt="No account, no telemetry" src="https://img.shields.io/badge/no%20account-no%20telemetry-1b3a6b?style=flat-square">
</p>

PDFKraft is a fork of [PdfCraft](https://github.com/storytold/pdfcraft), the open-source
PDF workbench by the ArtCraft team (MIT OR Apache-2.0). It keeps everything PdfCraft does and
adds the one thing it could not: **typing Khmer Unicode onto a page**. PdfCraft's Add text tool
writes with the PDF standard fonts and bolts on three complex scripts (Arabic, Hebrew, Thai)
through optional fonts; a Khmer character was refused before anything was written. The
source-level evidence is in
[docs/analysis/khmer-add-text-evidence.md](docs/analysis/khmer-add-text-evidence.md).

## What is different from PdfCraft

- **Khmer in Add text.** Khmer letters, vowel signs, coeng subscripts, diacritics, digits and
  punctuation (U+1780–U+17FF and the Khmer Symbols block) are shaped with the HarfBuzz port
  [harfrust](https://github.com/harfbuzz/harfrust) and its Khmer shaper, so ជើង subscripts stack
  under their consonant, pre-base vowels such as ែ and ើ come out before it, and marks sit where
  the font puts them. Each grapheme becomes one glyph of a Type 3 font with a ToUnicode map, and
  every line carries ActualText, so the Khmer stays searchable and copyable in other readers.
- **Khmer fonts in the app.** Nine Khmer families are committed under `assets/fonts/` and
  embedded in every build, the web build included: Noto Sans Khmer and Noto Serif Khmer (Regular
  and Bold, SIL Open Font License), Khmer OS Battambang, Khmer OS Muol and Khmer OS Siemreap
  (Danh Hong, LGPL 2.1 or later), and Khmer M1, Khmer M2, Khmer S1 and Khmer S2 (LIM
  Sovanvichet, LGPL 2.1 or later). The format panel's **Khmer font** list picks one per text
  box; left on "follow the font", Helvetica and Courier items use Noto Sans Khmer, Times items
  Noto Serif Khmer, and bold text the Bold face. No download, no optional build input, no
  system font.
- **Khmer on screen.** Noto Sans Khmer is in the interface font stack, so file names, document
  titles and the text you are typing into an Add text box show in Khmer.
- **Khmer word wrapping.** Khmer has no spaces between words. Lines break at a zero-width space
  (U+200B, how Khmer text marks word boundaries) or an ordinary space when the line has one, and
  after a whole grapheme cluster otherwise. A subscript or vowel sign is never separated from its
  consonant.
- **Its own name and mark.** The app, its packages and its app id
  (`io.github.kompheak7711.pdfkraft`) are PDFKraft's. The ArtCraft wordmark and logos, which are
  trademarks that PdfCraft's licence requires forks to remove, are not part of this repository.

Everything else, from the renderer to the organizer, forms, redaction, printing, the headless CLI
and the MCP server, is PdfCraft's work, unchanged.

## Type Khmer onto a page

1. Open a PDF.
2. Choose **Edit ▸ Add text** (the `edit.text` command; **T** in the tools panel).
3. Click where the text should start. Switch your keyboard to Khmer (NiDA, Khmer Unicode or the
   layout your system ships) and type. Type a space or a zero-width space between words if you
   want lines to break there.
4. Pick the family, size, colour and bold in the format panel, and the **Khmer font** (Noto
   Sans or Serif Khmer, Khmer OS Battambang, Muol or Siemreap, Khmer M1, M2, S1 or S2). Left
   on "follow the font", Helvetica and Courier items are written in Noto Sans Khmer and Times
   items in Noto Serif Khmer. The choice is saved with the text box and comes back when you
   reopen the file.
5. Click **Done** (or click elsewhere on the page). The page redraws with the shaped text.

Mixed text works: Khmer, Latin, Thai, Arabic and Hebrew can share one text box, each in its own
face, in the right direction.

What is not covered yet, so you know before you rely on it:

- The text box you type into is an egui text field, which draws glyph by glyph without OpenType
  shaping. While you type, subscripts and pre-base vowels show in their typed order; the shaped
  result appears on the page once the box is committed.
- Italic is not synthesised for Khmer (nor for Arabic, Hebrew or Thai).
- Wrapping is glyph-safe, not dictionary-based: without a space or zero-width space, a line may
  break between any two clusters, that is, in the middle of a word.
- Comments, form fields and typed signatures still use PdfCraft's standard fonts and refuse Khmer,
  as they do in PdfCraft. Khmer that is already in a PDF has always rendered; this fork is about
  writing it.
- The bundled Noto faces are the only Khmer faces for writing into a PDF. Fonts installed on your
  computer are read only as a last-resort interface fallback, for scripts without a bundled face.

## Build it

Building needs Rust 1.95 or later.

```sh
git clone https://github.com/kompheak7711/PDFKraft
cd PDFKraft
cargo run --release -p pdfkraft -- some.pdf          # the desktop app
cargo xtask models                                     # optional: the OCR models Scan & OCR needs
```

The headless tools and the opt-in MCP server:

```sh
cargo run --release -p pdfkraft-cli -- tools                         # list the tools
cargo run --release -p pdfkraft-cli -- run --script steps.json --root DIR
cargo run --release -p pdfkraft-cli -- mcp                           # MCP server on stdio
```

For example, this script adds Khmer text to the first page and saves a copy:

```json
[
  {"tool": "doc_open", "args": {"path": "in.pdf"}},
  {"tool": "page_add_text", "args": {"doc": 1, "page": 1, "text": "ភាសាខ្មែរ", "at": [72, 72], "size": 14, "khmer_font": "Khmer OS Muol"}},
  {"tool": "doc_save", "args": {"doc": 1, "path": "out.pdf"}}
]
```

Japanese, Chinese, Arabic, Thai, Hebrew and Devanagari faces come from
[craft-fonts](https://github.com/storytold/craft-fonts), an optional build input exactly as in
PdfCraft. Khmer does not need it:

```sh
git clone https://github.com/storytold/craft-fonts ../craft-fonts
CRAFT_FONTS_DIR=$PWD/../craft-fonts cargo run --release -p pdfkraft -- some.pdf
```

The web build is `trunk build --release` in `apps/pdfkraft-web` (see
[packaging/web/README.md](packaging/web/README.md)).

**Ready-made apps for macOS, Windows and Linux** come from the **Build apps** workflow
(`.github/workflows/build.yml`): open the repository's Actions tab, choose "Build apps", click
"Run workflow" on the branch you want, and wait. It builds a universal macOS `.dmg`, a Windows
`.msi` and portable `.zip`, and a Linux AppImage, `.deb`, `.rpm` and tarball, then attaches
them to a pre-release named `build-<run number>` under Releases. These builds are not signed or
notarized, so the first launch needs one extra step:

- macOS: Gatekeeper says the app cannot be opened; click Done, then System Settings ▸ Privacy &
  Security ▸ Open Anyway, or run `xattr -dr com.apple.quarantine /Applications/PDFKraft.app`.
- Windows: SmartScreen says "Windows protected your PC"; click More info ▸ Run anyway.

`.github/workflows/release.yml` is PdfCraft's signed release pipeline, kept for the day the
Apple and Windows signing accounts exist.

## Development

```sh
cargo test -p pdfkraft-fonts                          # shaping: clusters, outlines, the four Khmer faces
cargo test -p pdfkraft-edit khmer                     # Add text round trip, wrapping, serif selection
cargo test -p pdfkraft-automation khmer               # the tools end to end: save, reopen, extract, render
cargo test -p pdfkraft-ui-egui typing_khmer           # typing into the box
cargo xtask assets                                     # every font and icon is attributed and hashed
```

The Khmer path lives in `crates/fonts/src/craft.rs` (the bundled faces), `crates/fonts/src/shaping.rs`
(`shape_khmer`) and `crates/edit/src/added.rs` (classification, wrapping, the Type 3 writer it
shares with the other shaped scripts). `AGENTS.md` and `CLAUDE.md` are PdfCraft's contributor
rules, renamed; they still apply, with one change: Khmer fonts are committed here on purpose.

The design brief, the feature matrix and the build log of this fork are in
[docs/superpowers/specs/2026-10-26-pdfkraft-design.md](docs/superpowers/specs/2026-10-26-pdfkraft-design.md)
and [replica/](replica/).

## License and credits

PDFKraft is licensed under either the MIT License or the Apache License 2.0, at your option
(`LICENSE-MIT`, `LICENSE-APACHE`), like PdfCraft, whose copyright notices it keeps (`NOTICE`).
Third-party material is listed per file in `ATTRIBUTION.md`. The Khmer typefaces are Noto Sans
Khmer and Noto Serif Khmer, Copyright 2022 The Noto Project Authors, under the SIL Open Font
License 1.1 (`assets/fonts/OFL-NotoKhmer.txt`); the Khmer OS faces (Copyright 2007 Danh Hong) and the
Khmer M and S faces (Copyright 2007 LIM Sovanvichet) are under the GNU Lesser General Public
License 2.1 or later (`assets/fonts/LGPL-2.1.txt`), the one copyleft exception in the asset
policy (`AGENTS.md` §1.2), made for fonts the project owner supplies.
