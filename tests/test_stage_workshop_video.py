"""A media update must not publish unverified bytes or fetch unrelated URLs."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "stage_workshop_video.py"
spec = importlib.util.spec_from_file_location("stage_workshop_video", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def asset(name="tour.mp4", content=b"approved video"):
    return {"filename": name, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content),
            "url": f"https://github.com/ash0ts/forge-workshop-kit/releases/download/media-v1/{name}"}


def test_local_stage_checks_bytes_and_reuses_verified_file(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "tour.mp4").write_bytes(b"approved video")
    manifest = {"assets": [asset()]}
    site = tmp_path / "site"
    assert module.stage(manifest, site, source=source) == ["tour.mp4"]
    (source / "tour.mp4").unlink()
    assert module.stage(manifest, site) == ["tour.mp4"]
    target = site / "walkthrough/media"
    assert (target / "tour.mp4").read_bytes() == b"approved video"
    assert json.loads((target / "manifest.json").read_text()) == manifest


@pytest.mark.parametrize("mismatch", ["hash", "bytes"])
def test_mismatch_preserves_previous_media_and_manifest(tmp_path, mismatch):
    target = tmp_path / "site/walkthrough/media"
    target.mkdir(parents=True)
    (target / "tour.mp4").write_bytes(b"old public video")
    (target / "manifest.json").write_text("old manifest")
    source = tmp_path / "source"
    source.mkdir()
    (source / "tour.mp4").write_bytes(b"approved video")
    row = asset()
    row["sha256" if mismatch == "hash" else "bytes"] = "0" * 64 if mismatch == "hash" else row["bytes"] + 1
    with pytest.raises(ValueError, match="does not match"):
        module.stage({"assets": [row]}, tmp_path / "site", source=source)
    assert (target / "tour.mp4").read_bytes() == b"old public video"
    assert (target / "manifest.json").read_text() == "old manifest"
    assert not list(target.glob(".video-stage-*"))


def test_second_invalid_asset_prevents_first_replacement(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "tour.mp4").write_bytes(b"approved video")
    (source / "poster.png").write_bytes(b"wrong poster")
    target = tmp_path / "site/walkthrough/media"
    target.mkdir(parents=True)
    (target / "tour.mp4").write_bytes(b"old public video")
    with pytest.raises(ValueError, match="poster.png"):
        module.stage({"assets": [asset(), asset("poster.png", b"approved poster")]}, tmp_path / "site", source=source)
    assert (target / "tour.mp4").read_bytes() == b"old public video"


@pytest.mark.parametrize("name", ["../private.mp4", "/tmp/tour.mp4", "..\\private.mp4", ".", "", "manifest.json"])
def test_filename_traversal_is_blocked_before_staging(tmp_path, name):
    with pytest.raises(ValueError, match="plain filenames"):
        module.stage({"assets": [asset(name)]}, tmp_path / "site")
    assert not (tmp_path / "site").exists()


@pytest.mark.parametrize("url", [
    "https://example.com/tour.mp4",
    "https://github.com/other/repo/releases/download/v1/tour.mp4",
    "https://github.com/ash0ts/forge-workshop-kit/releases/download/../tour.mp4",
    "https://github.com/ash0ts/forge-workshop-kit/releases/download/%2E%2E/tour.mp4",
    "https://github.com/ash0ts/forge-workshop-kit/releases/download/media-v1/other.mp4",
    "https://github.com/ash0ts/forge-workshop-kit/releases/download/media-v1/tour.mp4?token=x",
    "http://github.com/ash0ts/forge-workshop-kit/releases/download/media-v1/tour.mp4",
])
def test_fetch_rejects_unrelated_or_ambiguous_url_before_network(tmp_path, monkeypatch, url):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid URL reached the network")
    monkeypatch.setattr(module.urllib.request, "urlopen", forbidden)
    row = {**asset(), "url": url}
    with pytest.raises(ValueError, match="Workshop Kit release"):
        module.stage({"assets": [row]}, tmp_path / "site", fetch=True)


def test_fetch_requires_explicit_flag_and_checks_download(tmp_path, monkeypatch):
    calls = []
    def download(url, timeout):
        calls.append(url)
        return io.BytesIO(b"approved video")
    monkeypatch.setattr(module.urllib.request, "urlopen", download)
    manifest = {"assets": [asset()]}
    with pytest.raises(FileNotFoundError):
        module.stage(manifest, tmp_path / "site")
    assert not calls
    module.stage(manifest, tmp_path / "site", fetch=True)
    assert calls == [asset()["url"]]


def test_byte_mismatch_is_not_accepted_from_cached_hash(tmp_path):
    target = tmp_path / "site/walkthrough/media"
    target.mkdir(parents=True)
    (target / "tour.mp4").write_bytes(b"approved video")
    row = asset()
    row["bytes"] += 1
    with pytest.raises(FileNotFoundError):
        module.stage({"assets": [row]}, tmp_path / "site")


def test_dated_release_asset_stages_under_stable_local_name(tmp_path, monkeypatch):
    requested = []
    release_name = "forge-workshops-narrated-2026-11-16.mp4"
    row = {**asset("tour.mp4"), "release_filename": release_name,
           "url": f"https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/{release_name}"}

    def download(url, timeout):
        requested.append(url)
        return io.BytesIO(b"approved video")

    monkeypatch.setattr(module.urllib.request, "urlopen", download)
    module.stage({"assets": [row]}, tmp_path / "site", fetch=True)
    assert requested == [row["url"]]
    assert (tmp_path / "site/walkthrough/media/tour.mp4").read_bytes() == b"approved video"
    assert not (tmp_path / "site/walkthrough/media" / release_name).exists()


@pytest.mark.parametrize("release_name", ["../tour.mp4", "..\\tour.mp4", "", "."])
def test_release_filename_traversal_rejected_before_fetch(tmp_path, monkeypatch, release_name):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid release filename reached the network")
    monkeypatch.setattr(module.urllib.request, "urlopen", forbidden)
    with pytest.raises(ValueError, match="Release media filenames"):
        module.stage({"assets": [{**asset(), "release_filename": release_name}]}, tmp_path / "site", fetch=True)
