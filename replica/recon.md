# Recon map: PdfCraft → PDFKraft

Written with the replica-recon method (Jakeschincariol/replica-skill). Date: 2026-10-26.

## Scope

| | |
|---|---|
| App | PdfCraft, https://github.com/storytold/pdfcraft, desktop (macOS, Windows, Linux, FreeBSD) and web (WASM) |
| Slice | The whole app, plus one feature it lacks: typing Khmer Unicode into a page with a Khmer font |
| For | A Khmer-speaking user who needs to put Khmer text on PDFs; published as PDFKraft |

## Sources

| source | what it gave | URL |
|---|---|---|
| README | the feature list, platforms, the "Add text" tool and its script support | https://github.com/storytold/pdfcraft/blob/main/README.md |
| source tree (MIT OR Apache-2.0) | the exact code path that refuses Khmer, and how Arabic, Hebrew and Thai were added | https://github.com/storytold/pdfcraft (commit 01b696df) |
| parity ledger | which features exist and are tested | `parity/acrobat-features.toml` |
| AGENTS.md / CLAUDE.md | the asset, font and never-crash rules the code is held to | repo root |
| craft-fonts | the optional font input and its manifest format | https://github.com/storytold/craft-fonts |
| prior analysis | the KhmerPDFcraft evidence ledger, which first located the Khmer refusal | kompheak7711/KhmerPDFcraft, `docs/analysis/` |

Public sources only; no account, no paywall, no binary.

## The licence changes the method

replica-recon sizes a clean-room rebuild of a 35-crate Rust PDF engine (renderer, COS parser,
encryption, forms, redaction, OCR, printing) as **XL: rescope it**. PdfCraft is released under
MIT OR Apache-2.0, which grants exactly what a clean room exists to avoid taking. So PDFKraft is
a **fork**: the code is used under its licence with notices kept, and the replica method is
applied to what the licence does not grant (the name, the ArtCraft trademarks, the screenshots)
and to the feature that is new (Khmer). `features.csv` records parity against the original
honestly: every PdfCraft feature is `yes` because it is the same code, and the Khmer rows are
what this project built.

## Screens (the ones the new feature and the rebrand touch)

| ID | screen | route | purpose | key components | states |
|---|---|---|---|---|---|
| S01 | Home | app start, no document | open or create, recent files, community card | mark, card, link pills | first run, card closed |
| S02 | Viewer | a document open | read, navigate, select | tabs, title bar buttons, page canvas, panels | continuous, two-up, read mode, dark |
| S03 | Add text box | Edit ▸ Add text, click on page | type page content | multiline text field, Done, Discard, format panel | empty, typing, mixed script, overflow, error (undrawable) |
| S04 | Format panel | with a text item | family, size, colour, bold, italic, alignment, spacing | combo boxes, toggles | default, item selected |
| S05 | About dialog | Help ▸ About | version, licence, links | mark, tabs About/Contributors/Models, link pills | each tab |
| S06 | Help menu | menu bar | shortcuts, links, updates, about | menu items from the command registry | — |
| S07 | Title bar | always | tabs, Open, theme, shortcuts, community button | ghost buttons | narrow window (tabs shrink) |

## Flows

```
F01 Add Khmer text to a page
    S02 viewer -> Edit ▸ Add text -> click on page -> S03 type (Khmer keyboard) -> Done -> page redraws shaped
    edge: a character no face has (refused with the character named), a 1-point-wide box (refused),
          no space in the text (wraps after whole clusters), Khmer and Arabic in one box (each its own run)
    clicks on the happy path: 3 (tool, place, Done)
F02 Add Khmer text headlessly
    pdfkraft-cli run --script -> page_add_text -> doc_save -> reopen -> page_text returns the typed order
F03 Find the project
    S07 GitHub button, S05 About links, S01 card, S06 Help menu -> the PDFKraft repository, issues, downloads, upstream
```

## Components changed

| component | where | change |
|---|---|---|
| shaped script | `crates/fonts/src/shaping.rs` | `ShapedScript::Khmer { serif, bold }`, `shape_khmer`, `khmer_has` |
| bundled faces | `crates/fonts/src/craft.rs`, `assets/fonts/` | `document_khmer_font`, `ui_khmer_fonts` |
| Add text layout | `crates/edit/src/added.rs` | `is_khmer`, `cluster_lines` (shared with Thai), error wording, Type 3 naming |
| interface fonts | `crates/ui-egui/src/theme.rs` | Noto Sans Khmer in every family |
| links | `crates/engine/src/links.rs`, `commands.rs` | GitHub, issues, downloads, upstream |
| mark | `crates/ui-egui/src/widgets.rs` | `app_mark` from the app icon |

## Data model (unchanged)

```
AddedText  text, family (Helvetica | Times | Courier), bold, italic, size, color, align,
           char_spacing, rect; stored in the item's stream dictionary under /PCAdded
           evidence: crates/edit/src/added.rs; confidence: certain (source)
```

## What cannot be cloned, on purpose

| item | why |
|---|---|
| ArtCraft name, wordmark, logos | trademarks; upstream's licence requires forks to remove them |
| getartcraft.com pages, the ArtCraft Discord | the upstream community, not a feature |
| craft-fonts as a shared asset repo | a storytold team resource; PDFKraft keeps it as the same optional input and bundles Khmer itself |
| signed, notarized installers | need the Apple and Windows signing accounts the workflow expects |

## Size

Fork + one shaped script + rebrand: **M** (days). A clean-room rewrite: XL. The hard parts were
the build (a pinned git dependency of the newest upstream commit does not build with current
Cargo, so the fork starts one commit earlier), keeping the asset policy green (every font and
icon hashed and attributed), and leaving nothing of the original brand behind without breaking
the UI tests that look for it.
