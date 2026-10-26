# Build log: PDFKraft

One line per step, what was harder than it looked, and what was left out on purpose.

| step | date | status | notes |
|---|---|---|---|
| Recon (`recon.md`, `features.csv`) | 2026-10-26 | done | Both targets publish source; the Khmer refusal was located in `crates/edit/src/added.rs` by reading, as the REA skill directs for full source trees. Sized a clean-room rebuild as XL and chose a fork under MIT OR Apache-2.0. |
| Base commit | 2026-10-26 | done, one commit behind upstream main | Upstream `64e0868b` pins craft-libs `edc41f68`, whose `crates/menu/Cargo.toml` overrides `default-features` on a workspace dependency; Cargo 1.97 refuses the manifest, so nothing in that workspace resolves. The fork starts at `01b696df`. Merge forward once upstream re-pins. |
| Shell: rename | 2026-10-26 | done | 653 files: identifiers, crate names, paths, app id `io.github.kompheak7711.pdfkraft`, repository URL. `vendor/` untouched. Two SVG assets held the old name as text and needed new hashes. |
| Fonts | 2026-10-26 | done | Noto Sans Khmer and Noto Serif Khmer v2.004 (notofonts/khmer releases, unhinted TTF), Regular and Bold, OFL, attributed and hashed. Committed in the repo on purpose; upstream keeps fonts in craft-fonts. |
| Vertical slice: Khmer Add text | 2026-10-26 | done | `ShapedScript::Khmer { serif, bold }`, `shape_khmer`, `is_khmer`, `cluster_lines`, `is_ignorable`, errors, Type 3 naming. harfrust 0.12 ships the Khmer shaper (`script::KHMER`). Harder than it looked: zero-width spaces, which Khmer uses as word marks, were refused as "not WinAnsi"; they are now break opportunities that are not drawn. |
| Tests | 2026-10-26 | done | fonts (shaping clusters and outlines on all four faces; face selection), edit (round trip, ToUnicode, ActualText, serif selection, width-independent wrapping check, refusal, odd-input sweep), automation (tools end to end), ui-egui (typing). The first wrapping assertion guessed a box width and was wrong: the whole phrase fit in 90 pt. It now narrows the box and checks where the first break lands. |
| Interface font | 2026-10-26 | done | Noto Sans Khmer in every egui family. The text box still draws glyph by glyph (no OpenType shaping in egui); the page shows the shaped result. |
| Brand | 2026-10-26 | done | Links to the PDFKraft repository, issues, releases and the upstream credit; new geometric mark and icon set from `packaging/icons.py` (stdlib only; the upstream `icons.sh` needed resvg); `docs/brand/` (trademarks) and `docs/images/` (upstream screenshots) removed with their 21 attribution entries; stale translation rows for the old community strings dropped (306 rows across 34 catalogs); packaging metadata, NOTICE, AGENTS.md, README rewritten. |
| Gates | 2026-10-26 | green, with one environmental exception | `cargo fmt --check`; clippy `-D warnings` on fonts, edit, engine, ui-egui, automation, cli, the app and xtask; `cargo xtask layers`, `assets`, `parity`; `cargo build -p pdfkraft -p pdfkraft-cli`. Tests: fonts 92, edit 284, engine 386, automation 313, cli 93, ui-egui 571 unit + 1153 integration passed. 30 ui-egui tests (1 unit, 29 integration) fail in this container only because egui_kittest finds no wgpu adapter ("No adapter found"); they render pages and signatures on the GPU and touch nothing this fork changed. Run them on a machine with a GPU. |
| Khmer font list | 2026-10-26 | done | Seven faces the project owner supplied (Khmer OS Battambang, Muol, Siemreap; Khmer M1, M2, S1, S2; all LGPL 2.1 or later per their name tables) join the Noto faces in `KHMER_FACES`. The shaper caches one slot per face; an item names its family (`khmer_font`, saved as `/KhmerFont`), the automation tools take `khmer_font`, and the format panel has a Khmer font combo. LGPL-2.1-or-later added to the asset allowlist for fonts, with the licence text in `assets/fonts/LGPL-2.1.txt`. |
| Build apps workflow | 2026-10-26 | done | `.github/workflows/build.yml`: unsigned macOS universal `.dmg` (ad-hoc signed), Windows x64 `.msi` and portable `.zip`, Linux AppImage/deb/rpm/tar, attached to a `build-<run>` pre-release. The upstream release workflow needs a paid macOS runner size and the signing accounts, so it stays for later. |

## Left out, and why

- Khmer in comments, form fields and typed signatures: a different code path (annotation
  appearance streams with standard fonts); not asked for, not promised.
- Writing into a PDF with a font installed on the computer: upstream's asset policy never embeds
  a system font into a document, and bundling gives the same output everywhere.
- Dictionary-based Khmer line breaking: no segmentation data in the tree; zero-width spaces and
  spaces do the job the way Khmer text already marks it.
- Signed installers: the release workflow expects the upstream signing accounts.
