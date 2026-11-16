"""The public distribution must explain access and include its rendering assets."""

import importlib.util
import json
import pytest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


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


class Elements(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.elements = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def attributes(self, tag):
        return [attrs for name, attrs in self.elements if name == tag]


def test_library_tour_is_visible_without_opening_another_page(tmp_path):
    builder = module("build_decks")
    builder.write_library_index(tmp_path, [{"slug": "pending", "title": "Pending, Inc."}])
    page = Elements((tmp_path / "index.html").read_text(encoding="utf-8"))
    videos = page.attributes("video")
    assert len(videos) == 1
    assert "controls" in videos[0]
    assert videos[0].get("preload") == "metadata"
    assert "autoplay" not in videos[0]
    assert videos[0].get("poster")
    sources = page.attributes("source")
    assert any(row.get("src", "").endswith("/forge-workshops-captioned.mp4") for row in sources)
    assert any(row.get("href") == "walkthrough/" for row in page.attributes("a"))
    assert (tmp_path / "walkthrough/index.html").is_file()
    # Reserve poster height before lazy loading so QR anchor targets do not move.
    assert all(row.get("width") == "1200" and row.get("height") == "1500"
               for row in page.attributes("img"))


def test_guide_index_opens_every_workshop_sequence_and_preserves_old_links(tmp_path):
    builder = module("build_visual_guides")
    index = json.loads((ROOT / "visual-guides/index.json").read_text(encoding="utf-8"))
    legacy = tmp_path / "visual-language/comparison/index.html"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("Existing skill reference", encoding="utf-8")
    builder.write_guide_index(tmp_path, index)
    page = Elements((tmp_path / "visual-language/index.html").read_text(encoding="utf-8"))
    hrefs = {urlsplit(row.get("href", "")).path for row in page.attributes("a")}
    images = page.attributes("img")
    for workshop in index["workshops"]:
        slug = workshop["slug"]
        for sequence in workshop["sequences"]:
            assert any(path.endswith(f"/guides/{slug}/{sequence['id']}/index.html")
                       or path.endswith(f"/guides/{slug}/{sequence['id']}/") for path in hrefs)
        # Each workshop preview must show one of its own actual drawings.
        previews = [row for row in images if f"/guides/{slug}/" in row.get("src", "")]
        assert previews and all(row.get("alt") for row in previews)
        assert all(row.get("width") == "1200" and row.get("height") == "675" for row in previews)
    assert not any(path in {"comparison/index.html", "overview/index.html", "branches/index.html",
                           "transformation/index.html", "sequence/index.html", "poster/index.html"}
                   for path in hrefs)
    assert legacy.read_text(encoding="utf-8") == "Existing skill reference"


def test_current_notebook_start_pages_use_saved_files_and_version_the_hosted_option():
    builder = module("build_share_packet")
    templates = json.loads((ROOT / "src/forge_workshop_kit/workshops.json").read_text(encoding="utf-8"))["templates"]
    reports = json.loads((ROOT / "reports/published.json").read_text(encoding="utf-8"))["reports"]
    for row in templates:
        deck = row.get("authoring", {}).get("deck")
        if not deck:
            continue
        slug = deck["directory"]
        report = reports["airline" if slug == "airline_monitoring" else slug]
        source = builder.notebook_start_body(row, report)
        notebook = Path(row["authoring"]["notebook"])
        assert f'marimo edit --sandbox {notebook.name}' in source
        assert 'marimo edit --sandbox https://' not in source
        assert 'wandb login --host https://api.wandb.ai --verify' in source
        primary = source.split('<details>', 1)[0]
        assert f'href="../notebooks/{notebook.name}" download' in primary
        assert report["hosted_notebook_url"] not in primary
        assert 'v0.12.0' in primary
        assert 'v0.11.1' in source.split('<details>', 1)[1]
        assert report["hosted_notebook_url"] in source
        assert report["hosted_notebook_url"].startswith('https://forge.coreweave.com/notebooks/')
        assert report["notebook_url"] not in source
        assert '.workshop/' in source
        assert '<strong>Run all</strong>' in primary


def test_partial_guide_index_does_not_advertise_unavailable_workshops(tmp_path):
    builder = module("build_visual_guides")
    index = json.loads((ROOT / "visual-guides/index.json").read_text(encoding="utf-8"))
    index["workshops"] = [row for row in index["workshops"] if row["slug"] == "solar"]
    builder.write_guide_index(tmp_path, index)
    source = (tmp_path / "visual-language/index.html").read_text(encoding="utf-8")
    assert '/guides/solar/window/' in source
    assert '/guides/pending/' not in source
    assert '/guides/transit/' not in source
    links = {row.get('href') for row in Elements(source).attributes('a')}
    public = 'https://ash0ts.github.io/forge-workshop-kit/'
    assert {public, public + 'walkthrough/', public + 'solar/',
            public + 'packet/start/solar.html'} <= links
    for name in ['index.html', 'walkthrough/index.html', 'solar/index.html', 'packet/start/solar.html']:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('Local page', encoding='utf-8')
    builder.write_guide_index(tmp_path, index)
    links = {row.get('href') for row in Elements((tmp_path / 'visual-language/index.html').read_text(encoding='utf-8')).attributes('a')}
    assert {'../', '../walkthrough/', '../solar/', '../packet/start/solar.html'} <= links


def test_current_notebook_start_does_not_require_an_older_hosted_template():
    builder = module('build_share_packet')
    templates = json.loads((ROOT / 'src/forge_workshop_kit/workshops.json').read_text(encoding='utf-8'))['templates']
    row = next(row for row in templates if row.get('authoring', {}).get('deck'))
    report = {'url':'https://example.com/report'}
    source = builder.notebook_start_body(row, report)
    assert 'Download the current notebook (.py)' in source
    assert 'v0.11.1' not in source
    assert 'supports notebook import' in source
    with pytest.raises(ValueError, match='actual Forge notebook'):
        builder.notebook_start_body(row, {**report, 'hosted_notebook_url':'https://example.com/start'})


def test_deck_setup_qr_uses_the_same_saved_file_path_as_the_start_page():
    builder = module("share_storyboard")
    for slug in builder.TARGETS:
        body = builder._body("https://utm.io/example", closing=False, workshop=slug)
        assert "Download the current notebook" in body
        assert "saved file in marimo" in body
        assert "Copy to project" not in body
        assert 'href="https://utm.io/example"' in body
