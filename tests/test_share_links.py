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


def test_rejects_correct_tracking_with_wrong_workshop_fragment(tmp_path):
    manifest = json.loads((ROOT / "docs/share-links.json").read_text())
    manifest["links"]["solar"]["url"] = manifest["links"]["solar"]["url"].replace("#solar", "#pending")
    path = tmp_path / "links.json"
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="own workshop card"):
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
    assert {Path(row["svg"]).name for row in requests} == {"workshop-qr.svg", "solar.svg", "packet.svg"}
    for row in requests:
        slug = "packet" if Path(row["svg"]).name == "packet.svg" else "solar"
        assert row["url"] == manifest["links"][slug]["short_url"]
    assert json.loads(poster.read_text())["poster"]["cta"]["url"] == manifest["links"]["solar"]["short_url"]
    page = (tmp_path / "site/share/index.html").read_text()
    assert 'id="solar"' in page and 'id="packet"' in page
    assert 'id="pending"' not in page
    assert manifest["links"]["solar"]["short_url"] in page
