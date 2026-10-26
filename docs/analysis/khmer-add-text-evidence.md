# Why PdfCraft could not type Khmer, and what PDFKraft changed

An evidence ledger in the form the REA "reverse-engineer-anything" skill
(https://github.com/morluto/rea) asks for: each conclusion tied to the evidence behind it,
observations kept apart from inferences and unknowns. The target publishes its complete source,
so, as that skill itself instructs for a full source repository, the analysis reads the source
rather than instrumenting a binary; no REA engine was run.

Target: https://github.com/storytold/pdfcraft at commit `01b696df` (2026-10-26), the commit
PDFKraft starts from. File references are to that tree (the same paths in this repository, with
`pdfcraft_` crate names renamed to `pdfkraft_`).

## Question: why does Add text refuse a Khmer character?

### Observations (static, source)

- `crates/edit/src/added.rs` defines the Add text item (`AddedText`) and its drawing. The
  `Family` enum has three members, Helvetica, Times and Courier, each mapped by `base_font` to a
  PDF standard-14 font name. Standard-14 text is written with `win_ansi`, a Unicode to
  Windows-1252 table (`crates/fonts/src/lib.rs`, `win_ansi_byte`).
- `first_undrawable` (added.rs) returns the first character that would be drawn as `?`. Its
  branches handle Thai (`is_thai`), Arabic (`shaped_arabic`) and Hebrew (`is_hebrew`); for any
  item not "shaped by a face" it returns `first_non_win_ansi(line)`. U+1780–U+17FF is not in
  Windows-1252, so a Khmer character is returned here.
- `validate` (added.rs) calls `first_undrawable` and returns `EditError` through `undrawable`
  before `write` touches the document. The automation tool `page_add_text` and the UI both go
  through `write`, so both refuse.
- `shaped_layout` (added.rs) classifies characters into `ShapedScript::Thai`, `Hebrew` or
  `Arabic`; `crates/fonts/src/shaping.rs` has exactly those three variants, one `harfrust`
  shaper face per variant, loaded from the optional craft-fonts input
  (`crates/fonts/src/craft.rs`: `document_thai_font`, `document_hebrew_font`,
  `document_arabic_font`).
- `crates/fonts/build.rs` embeds faces from a craft-fonts checkout only when `CRAFT_FONTS_DIR`
  is set; the pinned craft-fonts manifest (`fonts/manifest.txt`) lists Arab, Thai, Hebr, Deva,
  Geor, Hang, Jpan, Hans and Zsym faces and no `Khmr` face.
- `crates/render/src/text.rs` mentions Khmer once, in the text-extraction heuristics (clusters
  of Indic, Thai, Lao, Myanmar and Khmer never get an inferred space). Rendering of Khmer that is
  already in a PDF is therefore handled; writing it is not.

### Conclusion (high confidence)

Add text in PdfCraft writes Windows-1252 text in the standard fonts and adds exactly three
complex scripts through optional faces. Khmer has no face, no shaper variant and no
classification branch, so `first_undrawable` reports the first Khmer character and `validate`
refuses the item before anything is written. There is no user font choice in that path.

### Unknowns

- Whether upstream plans a Khmer face in craft-fonts; the roadmap does not say.
- How the Thai wrapping behaves on long Thai words was not measured; only the mechanism
  (breaking after any cluster) is established and reused.

## What PDFKraft built from this

| requirement | implementation | evidence that it works |
|---|---|---|
| A Khmer face in every build | Noto Sans Khmer and Noto Serif Khmer, Regular and Bold, committed in `assets/fonts/` and embedded by `crates/fonts/src/craft.rs` | `cargo xtask assets` (attributed, hashed); `craft::khmer_tests::khmer_faces_are_bundled_and_picked_by_style` |
| Proper shaping | `ShapedScript::Khmer { serif, bold }` and `shape_khmer` in `shaping.rs`, using harfrust's Khmer shaper (`script::KHMER`) with grapheme clusters | `shaping::khmer_tests::khmer_clusters_keep_subscripts_and_vowel_signs_with_their_consonant`: ខ្មែរ shapes to clusters ["ខ្មែ", "រ"], the first with ≥3 glyphs, one of them below the baseline (the subscript), and a wider advance than ខ alone (the pre-base vowel) |
| Classification and drawing | `is_khmer`, the `shaped_layout` branch, `khmer_error`, Type 3 family name "Khmer", the `draw` and `validate` branches in `added.rs` | `edit::tests::added_khmer_text_is_shaped_wraps_at_word_marks_and_survives_reopen`: the ToUnicode map contains `<178117D2179817C2>` (the four-character cluster as one glyph), the FontDescriptor is `NotoSansKhmer` (or `NotoSerifKhmer` for a bold Times item), ActualText carries the typed order |
| Word wrapping | `cluster_lines` (the former `thai_lines`, now shared) breaks at U+200B or a space when present, else after a cluster; `is_ignorable` drops U+200B from drawn lines | the same test: as the box narrows the first break lands on the zero-width space, and no line ever starts with a coeng or a vowel sign |
| Never crash | the odd-input sweep (lone coeng, lone vowel signs, controls, mixed scripts, 300 clusters, blank lines) | `edit::tests::odd_khmer_text_never_panics` |
| Headless parity | no change needed: `page_add_text` carries any text | `automation::khmer_text_through_tools_saves_reopens_extracts_and_renders`: save, reopen, `page_text` returns the typed string, `page_render` produces an image, `content_update` retypes |
| Khmer on screen | `ui_khmer_fonts` appended in `theme.rs` | `ui-egui::content::typing_khmer_text_keeps_clusters_and_commits_to_page` |

## Limits stated (so no one is surprised)

- The egui text field shows unshaped glyphs while typing; the page shows the shaped result.
- No italic synthesis; no dictionary-based line breaking.
- Comments, form fields and typed signatures still refuse Khmer (standard fonts), as upstream.
- Installed system Khmer fonts are not used to write into a PDF; the bundled faces are.
