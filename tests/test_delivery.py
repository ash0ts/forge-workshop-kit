"""The public distribution must explain access and include its rendering assets."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_offline_bundle_has_file_open_help_local_icon_and_pdf(tmp_path):
    builder = module("build_decks")
    directory = tmp_path / "deck"
    directory.mkdir()
    (directory / "index.html").write_text('<link rel="icon" href="https://cdn.example/icon.png"><div id="app"></div>')
    pdf = tmp_path / "slides.pdf"
    pdf.write_bytes(b"%PDF-test")
    builder.prepare_browser_files(directory, "Solar", offline=True, pdf=pdf)
    builder.prepare_browser_files(directory, "Solar", offline=True, pdf=pdf)
    index = (directory / "index.html").read_text()
    assert index.count('id="offline-help"') == 1
    assert 'location.protocol==="file:"' in index
    assert 'href="deck.pdf"' in index
    assert "cdn.example" not in index
    assert (directory / "deck.pdf").read_bytes() == pdf.read_bytes()
    assert (directory / "serve.py").is_file()
    assert "--open" in (directory / "start.cmd").read_text()


def test_asset_check_detects_missing_reveal_and_remote_font(tmp_path):
    checker = module("check_deck_assets")
    deck, built = tmp_path / "source", tmp_path / "built"
    deck.mkdir()
    built.mkdir()
    (deck / "slides.md").write_text('<img src="/images/first.svg"> :frames=\'{"src": "/guides/missing.svg"}\'')
    (built / "index.html").write_text('<link rel="stylesheet" href="/assets/style.css">')
    (built / "images").mkdir()
    (built / "images/first.svg").write_text('<svg/>')
    (built / "assets").mkdir()
    (built / "assets/style.css").write_text('@font-face { src: url(https://example.com/font.woff2) }')
    result = checker.check(deck, built)
    assert result["missing"] == ["/guides/missing.svg"]
    assert result["remote_render_dependencies"] == ["https://example.com/font.woff2"]
