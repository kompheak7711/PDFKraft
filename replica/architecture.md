# Architecture: PDFKraft

The stack is PdfCraft's, used under its licence: a Rust workspace of 35 crates in `crates/`
(layered L1 `cos` … L7 `ui-egui`), three apps in `apps/` (`pdfkraft` desktop with egui/wgpu,
`pdfkraft-cli` headless tools and MCP, `pdfkraft-web` WASM) and `xtask` for the gates. Nothing
below the UI depends on egui; the automation tools reach every feature headlessly.

## Where the new feature lives

```
assets/fonts/NotoSansKhmer-*.ttf, NotoSerifKhmer-*.ttf   bundled, attributed, hashed
crates/fonts  (L2)
  craft.rs     document_khmer_font(serif, bold), ui_khmer_fonts()
  shaping.rs   ShapedScript::Khmer { serif, bold }, shape_khmer(), khmer_has(), 4 face caches
crates/edit   (L5)
  added.rs     is_khmer(), cluster_lines() (Thai and Khmer), is_ignorable() (ZWSP), khmer_error(),
               classification in shaped_layout(), the draw and validate branches
crates/ui-egui (L7)
  theme.rs     Noto Sans Khmer appended to every interface font family
crates/automation, apps/pdfkraft-cli      unchanged: page_add_text already carries any text
```

Data flow for one Add text item with Khmer in it:

```
typed text ──wrapped()──▶ paragraphs ──cluster_lines()──▶ lines (ZWSP dropped)
   └ shaped_layout(line): bidi runs ─▶ segments by script ─▶ shape_khmer() ─▶ ShapedCluster[]
draw_laid_shaped(): one Type 3 glyph per distinct cluster (outline from the same face),
   ToUnicode <code> → cluster text, per-line /ActualText with the typed order
validate(): first_undrawable() refuses a character no face has, before anything is written
```

## Decisions

1. **Fork, not clean room.** See `recon.md`. Upstream notices are kept (`NOTICE`, the licence
   files, the git history).
2. **Bundle the Khmer faces in the repository** rather than through craft-fonts, so every build
   and the web build type Khmer without an optional input. Upstream's "fonts live in craft-fonts"
   rule is consciously set aside for these four files; everything else about the asset policy
   (attribution, hashes, OFL only) is kept and enforced by `cargo xtask assets`.
3. **One enum variant per face.** `ShapedScript::Khmer { serif, bold }` keeps glyph ids and
   outline caches per face, so a serif item never borrows a sans glyph.
4. **Zero-width space is a break, not content.** It is dropped from the drawn line and its
   ActualText; the item's stored text keeps it, so editing round-trips.
5. **Start at upstream 01b696df**, the parent of the newest commit, whose pinned craft-libs
   revision Cargo 1.97 rejects (a `default-features = false` override on a workspace
   dependency). Later upstream commits can be merged once that is fixed upstream.

## Build order followed

shell (rename and app id) → fonts (assets, attribution) → the vertical slice (shape → wrap →
draw → validate → tests at four zooms) → interface font → brand (links, mark, icon, packaging,
tests) → docs.
