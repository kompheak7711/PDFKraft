//! Project links: the GitHub button is one click away everywhere; Help menu, About dialog and
//! home screen open the PDFKraft pages.

use egui_kittest::Harness;
use egui_kittest::kittest::Queryable;
use pdfkraft_engine::links;
use pdfkraft_ui_egui::{Dialog, PDFKraftApp};

fn harness(setup: impl FnOnce(&mut PDFKraftApp) + 'static) -> Harness<'static, PDFKraftApp> {
    let mut h = Harness::builder().with_size(egui::vec2(1400.0, 900.0)).build_eframe(move |_cc| {
        let mut app = PDFKraftApp::new();
        app.set_option("language", "en").unwrap();
        setup(&mut app);
        app
    });
    h.run_steps(4);
    h
}

#[test]
fn github_button_in_the_top_bar_opens_the_repository() {
    let mut h = harness(|_| {});
    h.get_by_label("GitHub").click();
    h.run_steps(2);
    assert_eq!(h.state().last_opened_url.as_deref(), Some(links::GITHUB));
    assert_eq!(links::GITHUB, "https://github.com/kompheak7711/PDFKraft");
}

#[test]
fn home_screen_links() {
    for (label, url) in [
        ("PDFKraft on GitHub", links::GITHUB),
        ("Report a problem", "https://github.com/kompheak7711/PDFKraft/issues"),
        ("Downloads", "https://github.com/kompheak7711/PDFKraft/releases"),
        ("Based on PdfCraft", "https://github.com/storytold/pdfcraft"),
    ] {
        let mut h = harness(|_| {});
        h.get_by_label("Help and updates");
        h.get_by_label(label).click();
        h.run_steps(2);
        assert_eq!(h.state().last_opened_url.as_deref(), Some(url), "{label}");
    }
}

#[test]
fn home_community_card_closes_for_this_run() {
    let mut h = harness(|_| {});
    h.get_by_label("Help and updates");
    h.get_by_label("Close").click();
    h.run_steps(2);
    assert!(h.state().community_card_closed);
    assert!(h.query_by_label("Help and updates").is_none());
    assert!(h.query_by_label("Report a problem").is_none());
    // Not remembered: a fresh app shows the card again.
    assert!(!PDFKraftApp::new().community_card_closed);
}

#[test]
fn about_dialog_shows_the_mark_and_links() {
    let pdf = b"%PDF-1.7\n1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] >> endobj\ntrailer << /Root 1 0 R >>\n%%EOF";
    // With a document open, so the home screen's own links are not on screen.
    let mut h = harness(move |app| {
        app.open_bytes("one.pdf", None, pdf.to_vec()).unwrap();
        app.dialog = Some(Dialog::About);
    });
    assert!(h.query_all_by_label("PDFKraft").count() >= 1, "the mark (alt text)");
    assert!(h.query_all_by_label("ArtCraft").count() == 0, "no upstream trademark in the fork");
    h.get_by_label("Based on PdfCraft").click();
    h.run_steps(2);
    assert_eq!(h.state().last_opened_url.as_deref(), Some(links::UPSTREAM));
}
