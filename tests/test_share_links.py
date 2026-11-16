"""Sharing metadata must survive partial source bundles without crossing workshops."""

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_share_links", ROOT / "scripts/build_share_links.py")
sharing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sharing)


@pytest.mark.parametrize("field,value", [
    ("url", "https://ash0ts.github.io/forge-workshop-kit/packet/?utm_source=forged#solar"),
    ("short_url", "https://example.com/looks-like-a-short-link"),
    ("short_url", "https://utm.io/uuH97?utm_source=extra"),
    ("short_url", "https://utm.io/uuH97#wrong"),
])
def test_rejects_unregistered_link_shapes_and_tracking_changes(tmp_path, field, value):
    manifest = json.loads((ROOT / "docs/share-links.json").read_text())
    manifest["links"]["solar"][field] = value
    path = tmp_path / "links.json"
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        sharing.load_links(path)


def test_rejects_correct_tracking_with_wrong_workshop_destination(tmp_path):
    manifest = json.loads((ROOT / "docs/share-links.json").read_text())
    manifest["links"]["solar"]["url"] = manifest["links"]["solar"]["url"].replace("solar.html", "pending.html")
    path = tmp_path / "links.json"
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="notebook start page"):
        sharing.load_links(path)


@pytest.mark.parametrize("slug,source", [("packet", "loom"), ("loom", "slack")])
def test_rejects_collection_links_with_wrong_source(tmp_path, slug, source):
    manifest = json.loads((ROOT / "docs/share-links.json").read_text())
    expected_source = sharing.COLLECTION_LINKS[slug]["source"]
    manifest["links"][slug]["url"] = manifest["links"][slug]["url"].replace(
        f"utm_source={expected_source}", f"utm_source={source}"
    )
    path = tmp_path / "links.json"
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="UTM values differ"):
        sharing.load_links(path)


def test_rejects_reusing_slack_short_url_for_loom(tmp_path):
    manifest = json.loads((ROOT / "docs/share-links.json").read_text())
    manifest["links"]["loom"]["short_url"] = manifest["links"]["packet"]["short_url"]
    path = tmp_path / "links.json"
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="own registered short URL"):
        sharing.load_links(path)


def test_partial_bundle_keeps_qr_and_poster_associated_with_included_workshop(tmp_path, monkeypatch):
    # Source ZIPs contain one workshop, but retain the shared link registry.
    (tmp_path / "docs").mkdir()
    manifest = json.loads((ROOT / "docs/share-links.json").read_text())
    (tmp_path / "docs/share-links.json").write_text(json.dumps(manifest))
    (tmp_path / "src/forge_workshop_kit").mkdir(parents=True)
    templates = {"templates": [{"authoring": {"deck": {"directory": "solar", "title": "Solar"}}}]}
    (tmp_path / "src/forge_workshop_kit/workshops.json").write_text(json.dumps(templates))
    (tmp_path / "visual-guides/solar").mkdir(parents=True)
    poster = tmp_path / "visual-guides/solar/poster.json"
    poster.write_text(json.dumps({"poster": {"cta": {"label": "Open workshop", "url": "old"}}}))
    (tmp_path / "decks").mkdir()
    (tmp_path / "decks/share-packet.css").write_text("body { color: black; }")
    (tmp_path / "skills/teenage-engineering-visualizations/assets/fonts").mkdir(parents=True)
    requests = []

    def render(command, **kwargs):
        assert command[0] == "node"
        requests.extend(json.loads(kwargs["input"]))
        for row in requests:
            Path(row["svg"]).parent.mkdir(parents=True, exist_ok=True)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(sharing, "ROOT", tmp_path)
    monkeypatch.setattr(sharing.subprocess, "run", render)
    sharing.build(tmp_path / "site")
    assert {Path(row["svg"]).name for row in requests} == {"workshop-qr.svg", "solar.svg", "packet.svg", "loom.svg"}
    for row in requests:
        slug = Path(row["svg"]).stem
        if slug == "workshop-qr":
            slug = "solar"
        assert row["url"] == manifest["links"][slug]["short_url"]
    assert json.loads(poster.read_text())["poster"]["cta"]["url"] == manifest["links"]["solar"]["short_url"]
    page = (tmp_path / "site/share/index.html").read_text()
    assert 'id="solar"' in page and 'id="packet"' in page
    assert 'id="loom"' in page
    assert "All six workshops · Community Slack" in page
    assert "All six workshops · Loom" in page
    assert 'id="pending"' not in page
    assert manifest["links"]["solar"]["short_url"] in page
    assert manifest["links"]["loom"]["short_url"] in page
    assert manifest["legacy_links"]["internal_packet"]["short_url"] not in page
