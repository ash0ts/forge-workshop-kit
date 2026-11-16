#!/usr/bin/env python3
"""Index or upload approved workshop audio to ElevenLabs Assets without generating it."""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile

API = "https://api.elevenlabs.io/v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        temporary.write_text(json.dumps(value, indent=2) + "\n")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-")


def describe_file(path: Path, collection: str, label: str | None = None) -> dict[str, Any]:
    path = path.resolve(strict=True)
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    if not mime.startswith(("audio/", "video/", "image/")):
        raise ValueError(f"Assets accepts media; keep source and receipts in the repository: {path.name}")
    digest = sha256(path)
    name = f"forge-workshop-kit__{safe_name(collection)}__{safe_name(label or path.stem)}__{digest[:12]}{path.suffix.lower()}"
    return {"path": str(path), "name": name, "sha256": digest, "bytes": path.stat().st_size, "mime_type": mime}


def plan_files(paths: list[Path], collection: str) -> list[dict[str, Any]]:
    result = []
    seen = set()
    for path in paths:
        record = describe_file(path, collection)
        if record["name"] not in seen:
            result.append(record)
            seen.add(record["name"])
    if not result:
        raise ValueError("Select at least one finished audio, video, or poster file with --file.")
    return result


def plan_index(index_path: Path, collection: str) -> list[dict[str, Any]]:
    index_path = index_path.resolve(strict=True)
    index = json.loads(index_path.read_text())
    if not index.get("complete"):
        raise ValueError("Finish the audio check before uploading its selected takes.")
    assets = []
    for item in index["assets"]:
        if item.get("status") != "completed":
            raise ValueError("The audio index contains an unfinished take.")
        media = (index_path.parent / item["audio_file"]).resolve(strict=True)
        if not media.is_relative_to(index_path.parent):
            raise ValueError("Selected audio must stay within its production directory.")
        receipt = (index_path.parent / item["receipt"]).resolve(strict=True)
        if not receipt.is_relative_to(index_path.parent):
            raise ValueError("Selected receipt must stay within its production directory.")
        saved = json.loads(receipt.read_text())
        record = describe_file(media, collection, item["asset_id"])
        if saved.get("audio_sha256") != record["sha256"]:
            raise ValueError(f"Audio no longer matches its saved generation: {item['asset_id']}")
        assets.append(record)
    return assets


class AssetAPI:
    def __init__(self, key: str) -> None:
        self.key = key

    def request(self, method: str, path: str, body: bytes | None = None, content_type: str | None = None) -> dict[str, Any]:
        headers = {"xi-api-key": self.key}
        if content_type:
            headers["Content-Type"] = content_type
        request = urllib.request.Request(API + path, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            try:
                detail = json.load(error).get("detail", {})
            except (ValueError, AttributeError):
                detail = {}
            status = detail.get("status", "request_failed") if isinstance(detail, dict) else "request_failed"
            raise RuntimeError(f"ElevenLabs Assets HTTP {error.code}: {status}. Check asset permissions and plan access; no automatic retry was made.") from None

    def list(self, name: str) -> list[dict[str, Any]]:
        result = []
        cursor = None
        seen = set()
        while True:
            query = {"search": name, "page_size": 100}
            if cursor:
                query["cursor"] = cursor
            page = self.request("GET", "/assets?" + urllib.parse.urlencode(query))
            result.extend(item for item in page["assets"] if item.get("name") == name)
            if not page.get("has_more"):
                return result
            cursor = page.get("next_cursor")
            if not cursor or cursor in seen:
                raise RuntimeError("ElevenLabs asset pagination did not advance.")
            seen.add(cursor)

    def get(self, asset_id: str) -> dict[str, Any]:
        return self.request("GET", "/assets/" + urllib.parse.quote(asset_id, safe=""))

    def upload(self, asset: dict[str, Any]) -> dict[str, Any]:
        path = Path(asset["path"])
        if sha256(path) != asset["sha256"]:
            raise ValueError(f"Selected file changed after planning: {path.name}")
        boundary = "workshop-" + uuid.uuid4().hex
        body = (
            f'--{boundary}\r\nContent-Disposition: form-data; name="name"\r\n\r\n{asset["name"]}\r\n'
            f'--{boundary}\r\nContent-Disposition: form-data; name="asset"; filename="{asset["name"]}"\r\n'
            f'Content-Type: {asset["mime_type"]}\r\n\r\n'
        ).encode() + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
        return self.request("POST", "/assets", body, f"multipart/form-data; boundary={boundary}")


def public_asset(asset: dict[str, Any]) -> dict[str, Any]:
    # Signed download URLs expire and must not enter durable or public receipts.
    return {key: asset[key] for key in ("asset_id", "name", "mime_type", "created_at_unix") if key in asset}


def upload_assets(api: AssetAPI, assets: list[dict[str, Any]], receipt_path: Path) -> dict[str, Any]:
    # Lock the entire read/reconcile/upload/write transaction for this receipt.
    # A killed process leaves a lock so a second runner cannot repeat an unknown upload.
    receipt_path = receipt_path.resolve()
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    lock = receipt_path.with_name(receipt_path.name + ".lock")
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise RuntimeError(
            f"An asset upload lock exists at {lock}. Check its process and receipt before retrying; "
            "do not remove the lock while another upload is running."
        ) from None
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump({"pid": os.getpid(), "started_at": time.time()}, handle)
        return _upload_assets_locked(api, assets, receipt_path)
    finally:
        lock.unlink()


def _upload_assets_locked(api: AssetAPI, assets: list[dict[str, Any]], receipt_path: Path) -> dict[str, Any]:
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {"schema_version": 1, "assets": {}}
    for asset in assets:
        name = asset["name"]
        saved = receipt["assets"].get(name, {})
        if saved.get("sha256") and saved["sha256"] != asset["sha256"]:
            raise ValueError(f"Receipt hash disagrees with selected asset: {name}")
        if saved.get("status") == "completed":
            remote = api.get(saved["remote"]["asset_id"])
            if remote.get("name") != name:
                raise ValueError(f"Remote asset name changed: {name}")
            continue
        matching = api.list(name)
        if len(matching) > 1:
            raise RuntimeError(f"More than one remote asset has this exact name: {name}. Review it in Assets before continuing.")
        if matching:
            remote = matching[0]
        elif saved.get("status") == "uploading":
            raise RuntimeError(f"Previous upload outcome is unknown for {name}. Check Assets before clearing this pending receipt; this command will not upload it twice.")
        else:
            receipt["assets"][name] = {**asset, "status": "uploading", "started_at": time.time()}
            save_json(receipt_path, receipt)
            remote = api.upload(asset)
            if remote.get("name") != name or not remote.get("asset_id"):
                raise RuntimeError("ElevenLabs returned an unexpected asset identity. The pending receipt was preserved.")
        receipt["assets"][name] = {**asset, "status": "completed", "remote": public_asset(remote), "completed_at": time.time()}
        save_json(receipt_path, receipt)
    return receipt



# Public handoffs contain only these production fields, never raw provider responses.
INDEX_FIELDS = ("schema_version", "collection", "seconds", "manifest_sha256", "visual_sha256", "config_sha256", "chapters", "characters", "paid_tts_requests", "paid_sfx_requests", "complete")
TAKE_FIELDS = ("asset_id", "kind", "name", "chapter", "shot", "capture", "start", "duration", "text", "characters", "voice_id", "model_id", "request_sha256", "status", "audio_sha256", "audio_duration", "tempo")
RECEIPT_FIELDS = (*TAKE_FIELDS, "provider", "started_at", "completed_at", "audio_bytes", "response_sha256", "alignment_sha256")
HEADER_FIELDS = ("request-id", "history-item-id", "x-request-id", "character-cost", "content-type")
HISTORY_FIELDS = ("asset_id", "name", "request_sha256", "status", "matches", "history_item_id", "request_id", "date_unix")


def only(record, fields):
    return {key: record[key] for key in fields if key in record}


def source_file(root, relative):
    path = (root / relative).resolve(strict=True)
    if not path.is_relative_to(root):
        raise ValueError("Packaged source must stay within its production directory")
    return path


def package_assets(index_path: Path, output: Path, collection: str) -> dict[str, Any]:
    """Package selected takes and safe receipts locally; no key or network is used."""
    index_path = index_path.resolve(strict=True)
    root = index_path.parent
    plan_index(index_path, collection)
    index = json.loads(index_path.read_text())
    public_index = only(index, INDEX_FIELDS)
    public_index["assets"] = []
    files = {}
    selected = {}
    for row in index["assets"]:
        asset_id = row["asset_id"]
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", asset_id) or asset_id in selected:
            raise ValueError("Selected takes must have distinct plain asset IDs")
        selected[asset_id] = row.get("request_sha256")
        audio = source_file(root, row["audio_file"])
        receipt = json.loads(source_file(root, row["receipt"]).read_text())
        group = "narration" if row["kind"] == "tts" else "sound-effects"
        base = f"{group}/{asset_id}-{receipt['audio_sha256'][:12]}"
        audio_name = base + audio.suffix
        receipt_name = base + ".receipt.json"
        public_row = only(row, TAKE_FIELDS)
        public_row.update(audio_file=audio_name, receipt=receipt_name)
        public_receipt = only(receipt, RECEIPT_FIELDS)
        public_receipt["audio_file"] = audio_name
        public_receipt["provider_headers"] = only(receipt.get("provider_headers", {}), HEADER_FIELDS)
        files[audio_name] = audio.read_bytes()
        if row.get("alignment_file"):
            alignment_path = source_file(root, row["alignment_file"])
            if sha256(alignment_path) != receipt.get("alignment_sha256"):
                raise ValueError(f"Alignment no longer matches its generation: {asset_id}")
            alignment = json.loads(alignment_path.read_text())
            alignment = only(alignment, ("characters", "character_start_times_seconds", "character_end_times_seconds"))
            alignment_name = base + ".alignment.json"
            public_row["alignment_file"] = alignment_name
            public_receipt["alignment_file"] = alignment_name
            files[alignment_name] = (json.dumps(alignment, indent=2) + "\n").encode()
            public_receipt["source_alignment_sha256"] = receipt["alignment_sha256"]
            public_receipt["alignment_sha256"] = hashlib.sha256(files[alignment_name]).hexdigest()
        files[receipt_name] = (json.dumps(public_receipt, indent=2) + "\n").encode()
        public_index["assets"].append(public_row)
    history_path = root / "provider-history-index.json"
    if history_path.exists():
        history = json.loads(history_path.read_text())
        public_history = only(history, ("schema_version", "collection", "sfx"))
        public_history["tts"] = [only(row, HISTORY_FIELDS) for row in history.get("tts", []) if row.get("asset_id") in selected and row.get("request_sha256") == selected[row["asset_id"]]]
        files["provider-history-index.json"] = (json.dumps(public_history, indent=2) + "\n").encode()
    files["audio-index.json"] = (json.dumps(public_index, indent=2) + "\n").encode()
    files["README.txt"] = (
        "Selected Workshop Kit narration and sound effects\n\n"
        "audio-index.json maps each selected take to its screen time, audio, character alignment, and receipt. "
        "The audio files retain their original generated timing; tempo and placement are recorded in the index.\n"
        "Receipts include provider history identities when available. They do not prove Assets folder placement.\n"
        "This package excludes raw provider responses, credentials, superseded takes, and large mixed WAV stems.\n"
        "Production instructions: https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/video-production.md\n"
    ).encode()
    package_manifest = {"schema_version": 1, "collection": index["collection"], "selected_assets": len(selected),
                        "files": {name: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)} for name, data in files.items()}}
    files["package-manifest.json"] = (json.dumps(package_manifest, indent=2) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in sorted(files):
                info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, files[name])
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return {"path": str(output), "assets": len(selected), "files": len(files), "bytes": output.stat().st_size, "sha256": sha256(output)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "check", "upload", "package"))
    parser.add_argument("--collection", default="collection-v0.12.0", help="Versioned production name used to group search results")
    parser.add_argument("--file", type=Path, action="append", default=[], help="Approved finished media; repeat to upload several files")
    parser.add_argument("--audio-index", type=Path, help="Upload the selected checked takes from this generation index")
    parser.add_argument("--receipt", type=Path, default=Path("dist/walkthrough-production/audio/asset-library-receipt.json"))
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--output", type=Path, default=Path("dist/walkthrough-production/forge-workshops-audio-assets.zip"), help="Local selected-assets ZIP output")
    args = parser.parse_args()
    def selected_assets():
        assets = plan_index(args.audio_index, args.collection) if args.audio_index else []
        if args.file:
            assets.extend(plan_files(args.file, args.collection))
        if not assets:
            raise ValueError("Select --file or --audio-index.")
        return assets
    if args.command == "package":
        if not args.audio_index:
            raise ValueError("Packaging requires --audio-index")
        print(json.dumps(package_assets(args.audio_index, args.output, args.collection)))
        return
    if args.command == "plan":
        print(json.dumps({"assets": selected_assets(), "network_requests": 0}, indent=2))
        return
    from build_workshop_audio import load_api_key
    api = AssetAPI(load_api_key(args.env_file))
    if args.command == "check":
        api.list(f"forge-workshop-kit__{safe_name(args.collection)}")
        print("ElevenLabs Assets access works. This check did not upload or generate media.")
        return
    receipt = upload_assets(api, selected_assets(), args.receipt)
    print(json.dumps({"receipt": str(args.receipt), "completed_assets": sum(item.get("status") == "completed" for item in receipt["assets"].values())}))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError) as error:
        raise SystemExit(str(error)) from None
