# PDFKraft design brief

Date: 2026-10-26. Status: implemented on branch `claude/laughing-hypatia-vjqral`.

## The request, as understood

Clone PdfCraft (storytold/pdfcraft) with the replica-skill method, make it able to type Khmer
Unicode with the REA method (understand the feature from evidence, then build it), bundle a
Khmer Unicode font in the application or use one from the operating system, and call the
result **PDFKraft**. Deliver it in the kompheak7711/PDFKraft repository.

## Assumptions made, because nobody could be asked mid-task

1. **A fork is the right "clone."** PdfCraft is MIT OR Apache-2.0. A clean-room rebuild of a
   35-crate PDF engine is a quarter-plus project and would not be PdfCraft; the user asked for
   PdfCraft with Khmer. The replica method is applied where the licence stops (name, trademarks,
   screenshots) and to the new feature. Upstream notices stay, as the licence requires.
2. **"Add Khmer font into the application" is satisfied by bundling** Noto Sans Khmer and Noto
   Serif Khmer (OFL) and using them for writing into PDFs. Using an installed OS Khmer font for
   writing is not built: upstream's architecture never embeds a system font in a PDF (its asset
   policy forbids it), and a bundled face gives the same output on every machine. The interface
   keeps upstream's installed-font fallback for scripts without a bundled face.
3. **Khmer applies to Add text (page content)**, the tool the earlier analysis found wanting.
   Comments, form fields and typed signatures keep the standard fonts, as upstream.
4. **Rebrand fully**: product name, crate names, app id, icon, links; not the history. Mentions of
   PdfCraft remain only as attribution (README, NOTICE, About, the "Based on PdfCraft" link).
5. **Start at upstream commit 01b696df**, one behind main, because main's newest commit pins a
   craft-libs revision that Cargo 1.97 cannot build.

## Architecture

See `replica/architecture.md`. In one paragraph: Khmer becomes the fourth shaped script of Add
text. The bundled faces are static `CraftFont`s in `crates/fonts`; `shape_khmer` runs harfrust's
Khmer shaper per grapheme cluster; `crates/edit` classifies Khmer characters, wraps by cluster
with zero-width-space and space breaks, and draws through the existing Type 3 writer with
ToUnicode and ActualText. The interface font stack gains Noto Sans Khmer.

## Components

- `crates/fonts`: faces, shaper, `khmer_has`.
- `crates/edit`: `is_khmer`, `cluster_lines`, `is_ignorable`, `khmer_error`, branches.
- `crates/ui-egui`: font stack; links, mark, home card, About, title bar (brand).
- `crates/engine`: `links.rs`, `commands.rs` (brand).
- `apps/pdfkraft-cli`: version banner (brand).
- `packaging/`, `assets/app-icon/`, `ATTRIBUTION.toml`, `NOTICE`, `AGENTS.md`, `README.md`.

## Error handling

Every failure is an `EditError::Invalid` with the character or cause named, returned before the
document is touched (`validate`). The faces are bundled, so `GlyphError::NoFont` for Khmer can
only mean an unreadable embedded file and says so. No new `unwrap`, index or `unsafe`.

## Testing

Four zooms, as upstream asks: unit (shaping clusters and outlines, face selection), crate
(Add text round trip, wrapping, refusal, odd-input sweep), integration (automation tools: save,
reopen, extract, render, retype), end to end (typing in the egui box). Plus the gates: `cargo fmt
--check`, clippy on the touched crates, `cargo xtask assets`, `cargo xtask layers`, `cargo xtask
parity`.

## Out of scope, stated

Dictionary-based Khmer line breaking; italic synthesis; Khmer in annotations and forms; writing
with installed fonts; signed installers; merging upstream commits after 01b696df.
