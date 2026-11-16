"""Asset organization must resume safely without issuing another generation."""
import importlib.util
import json
import zipfile
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "organize_workshop_audio.py"
spec = importlib.util.spec_from_file_location("organize_workshop_audio", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AssetStore:
    def __init__(self):
        self.assets = {}
        self.uploads = 0

    def list(self, name):
        return [asset for asset in self.assets.values() if asset["name"] == name]

    def get(self, asset_id):
        return self.assets[asset_id]

    def upload(self, asset):
        self.uploads += 1
        remote = {"asset_id": str(self.uploads), "name": asset["name"], "mime_type": asset["mime_type"], "content_url": "https://private.invalid/signed-secret"}
        self.assets[remote["asset_id"]] = remote
        return remote


def test_completed_upload_is_reused_and_private_url_is_not_saved(tmp_path):
    audio = tmp_path / "narration.wav"
    audio.write_bytes(b"recorded narration")
    planned = module.plan_files([audio], "collection-v1")
    receipt = tmp_path / "receipt.json"
    store = AssetStore()
    module.upload_assets(store, planned, receipt)
    module.upload_assets(store, planned, receipt)
    assert store.uploads == 1
    assert "signed-secret" not in receipt.read_text()
    assert json.loads(receipt.read_text())["assets"][planned[0]["name"]]["remote"]["asset_id"] == "1"


def test_ambiguous_upload_requires_reconciliation(tmp_path):
    audio = tmp_path / "effect.wav"
    audio.write_bytes(b"transition effect")
    planned = module.plan_files([audio], "collection-v1")
    receipt = tmp_path / "receipt.json"
    name = planned[0]["name"]
    receipt.write_text(json.dumps({"schema_version": 1, "assets": {name: {**planned[0], "status": "uploading"}}}))
    store = AssetStore()
    with pytest.raises(RuntimeError, match="outcome is unknown"):
        module.upload_assets(store, planned, receipt)
    assert store.uploads == 0
    store.assets["saved"] = {"asset_id": "saved", "name": name, "mime_type": "audio/wav"}
    module.upload_assets(store, planned, receipt)
    assert store.uploads == 0
    assert json.loads(receipt.read_text())["assets"][name]["status"] == "completed"


def test_changed_media_has_a_new_remote_identity(tmp_path):
    audio = tmp_path / "narration.wav"
    audio.write_bytes(b"first take")
    first = module.plan_files([audio], "collection-v1")[0]
    audio.write_bytes(b"revised take")
    second = module.plan_files([audio], "collection-v1")[0]
    assert first["name"] != second["name"]
    assert first["sha256"] != second["sha256"]


def test_nonmedia_source_is_not_uploaded(tmp_path):
    source = tmp_path / "private-receipt.json"
    source.write_text("{}")
    with pytest.raises(ValueError, match="keep source and receipts"):
        module.plan_files([source], "collection-v1")


def test_selected_index_verifies_audio_before_remote_upload(tmp_path):
    audio = tmp_path / "audio.mp3"
    audio.write_bytes(b"saved audio")
    receipt = tmp_path / "receipt.json"
    receipt.write_text(json.dumps({"audio_sha256": module.sha256(audio)}))
    index = tmp_path / "audio-index.json"
    index.write_text(json.dumps({"complete": True, "assets": [{"asset_id": "pending-00", "status": "completed", "audio_file": "audio.mp3", "receipt": "receipt.json"}]}))
    assert "pending-00" in module.plan_index(index, "collection-v1")[0]["name"]
    audio.write_bytes(b"unreviewed replacement")
    with pytest.raises(ValueError, match="no longer matches"):
        module.plan_index(index, "collection-v1")


def test_concurrent_uploaders_share_one_receipt_lock(tmp_path):
    audio = tmp_path / "narration.wav"
    audio.write_bytes(b"approved take")
    planned = module.plan_files([audio], "collection-v1")
    receipt = tmp_path / "receipt.json"
    started, release = Event(), Event()

    class SlowAssetStore(AssetStore):
        def upload(self, asset):
            started.set()
            assert release.wait(5), "Test did not release the first upload"
            return super().upload(asset)

    store = SlowAssetStore()
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(module.upload_assets, store, planned, receipt)
        try:
            assert started.wait(5), "First upload never started"
            second = pool.submit(module.upload_assets, store, planned, receipt)
            with pytest.raises(RuntimeError, match="upload lock exists"):
                second.result(timeout=5)
        finally:
            release.set()
        first.result(timeout=5)
    module.upload_assets(store, planned, receipt)
    assert store.uploads == 1
    assert not receipt.with_name("receipt.json.lock").exists()
    assert not list(tmp_path.glob("*.tmp"))


def test_failed_upload_preserves_pending_receipt_and_releases_lock(tmp_path):
    audio = tmp_path / "narration.wav"
    audio.write_bytes(b"approved take")
    planned = module.plan_files([audio], "collection-v1")
    receipt = tmp_path / "receipt.json"

    class InterruptedAssetStore(AssetStore):
        def upload(self, asset):
            raise TimeoutError("connection ended after dispatch")

    with pytest.raises(TimeoutError):
        module.upload_assets(InterruptedAssetStore(), planned, receipt)
    assert not receipt.with_name("receipt.json.lock").exists()
    assert json.loads(receipt.read_text())["assets"][planned[0]["name"]]["status"] == "uploading"
    with pytest.raises(RuntimeError, match="outcome is unknown"):
        module.upload_assets(AssetStore(), planned, receipt)


def package_fixture(root):
    audio = root / "audio.mp3"
    audio.write_bytes(b"approved narration")
    alignment = root / "alignment.json"
    alignment.write_text(json.dumps({"characters": ["A"], "character_start_times_seconds": [0.0], "character_end_times_seconds": [0.5], "unrelated_private_field": "do-not-share"}))
    receipt = root / "receipt.json"
    receipt.write_text(json.dumps({"audio_sha256": module.sha256(audio), "alignment_sha256": module.sha256(alignment), "request_sha256": "request-1", "api_key": "do-not-share", "provider_headers": {"history-item-id": "public-history-id", "xi-api-key": "do-not-share"}}))
    index = root / "audio-index.json"
    index.write_text(json.dumps({"schema_version": 1, "collection": "reviewed video", "complete": True, "api_key": "do-not-share", "assets": [{"asset_id": "pending-00", "kind": "tts", "status": "completed", "audio_file": "audio.mp3", "receipt": "receipt.json", "alignment_file": "alignment.json", "request_sha256": "request-1"}]}))
    (root / "raw-response.json").write_text('{"audio_base64": "do-not-share"}')
    (root / "provider-history-index.json").write_text(json.dumps({"schema_version": 1, "collection": "reviewed video", "tts": [{"asset_id": "pending-00", "request_sha256": "request-1", "history_item_id": "public-history-id", "character_count_change_to": "do-not-share"}, {"asset_id": "pending-00", "request_sha256": "superseded", "history_item_id": "superseded-history"}]}))
    return index


def test_package_contains_only_selected_checked_audio_and_safe_metadata(tmp_path):
    index = package_fixture(tmp_path)
    output = tmp_path / "selected.zip"
    result = module.package_assets(index, output, "collection-v1")
    assert result["assets"] == 1
    with zipfile.ZipFile(output) as archive:
        assert "raw-response.json" not in archive.namelist()
        public_index = json.loads(archive.read("audio-index.json"))
        take = public_index["assets"][0]
        assert archive.read(take["audio_file"]) == b"approved narration"
        public_receipt = json.loads(archive.read(take["receipt"]))
        assert public_receipt["provider_headers"]["history-item-id"] == "public-history-id"
        assert public_receipt["alignment_sha256"] == module.hashlib.sha256(archive.read(take["alignment_file"])).hexdigest()
        for name in archive.namelist():
            assert b"do-not-share" not in archive.read(name)
            assert b"superseded-history" not in archive.read(name)
        manifest = json.loads(archive.read("package-manifest.json"))
        for name, row in manifest["files"].items():
            assert module.hashlib.sha256(archive.read(name)).hexdigest() == row["sha256"]


def test_package_is_deterministic_and_preserves_previous_export_on_bad_alignment(tmp_path):
    index = package_fixture(tmp_path)
    output = tmp_path / "selected.zip"
    first = module.package_assets(index, output, "collection-v1")
    second = module.package_assets(index, output, "collection-v1")
    assert first["sha256"] == second["sha256"]
    (tmp_path / "alignment.json").write_text("changed")
    with pytest.raises(ValueError, match="Alignment no longer matches"):
        module.package_assets(index, output, "collection-v1")
    assert module.sha256(output) == first["sha256"]
