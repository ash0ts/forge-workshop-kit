"""Stage published video assets on the workshop site, checking every file hash.

Use --source for a local production directory. --fetch downloads only the named
public release assets. Neither path generates media or calls a paid service.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    checksum = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def plain_name(name):
    return isinstance(name, str) and name not in ("", ".", "..") and not any(
        char in name for char in ("/", "\\", "\0", "\r", "\n")
    ) and Path(name).name == name


def release_url(url, filename):
    parsed = urllib.parse.urlsplit(url)
    parts = parsed.path.split("/")
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or parsed.query
        or parsed.fragment
        or len(parts) != 7
        or parts[:5] != ["", "ash0ts", "forge-workshop-kit", "releases", "download"]
        or not plain_name(urllib.parse.unquote(parts[5]))
        or urllib.parse.unquote(parts[6]) != filename
    ):
        raise ValueError("Expected a named public Workshop Kit release asset")
    return url


def validated_assets(manifest):
    assets = manifest["assets"]
    if not isinstance(assets, list) or not assets:
        raise ValueError("The video manifest must contain media assets")
    names = set()
    for asset in assets:
        name = asset["filename"]
        if not plain_name(name) or name == "manifest.json":
            raise ValueError("Media filenames must be plain filenames")
        release_name = asset.get("release_filename", name)
        if not plain_name(release_name):
            raise ValueError("Release media filenames must be plain filenames")
        if name in names:
            raise ValueError(f"Duplicate media filename: {name}")
        names.add(name)
        if not re.fullmatch(r"[a-f0-9]{64}", asset["sha256"]):
            raise ValueError(f"Invalid media SHA-256: {name}")
        if type(asset["bytes"]) is not int or asset["bytes"] < 0:
            raise ValueError(f"Invalid media byte count: {name}")
    return assets


def matches(path, asset):
    return path.is_file() and path.stat().st_size == asset["bytes"] and digest(path) == asset["sha256"]


def stage(manifest, site, *, source=None, fetch=False):
    assets = validated_assets(manifest)
    destination = Path(site) / "walkthrough/media"
    destination.mkdir(parents=True, exist_ok=True)
    completed = []
    # Verify every incoming file before replacing any existing public media.
    with tempfile.TemporaryDirectory(prefix=".video-stage-", dir=destination) as staging:
        pending = []
        for asset in assets:
            name = asset["filename"]
            target = destination / name
            completed.append(name)
            if matches(target, asset):
                continue
            temporary = Path(staging) / name
            if source is not None and (Path(source) / name).is_file():
                shutil.copyfile(Path(source) / name, temporary)
            elif fetch:
                url = release_url(asset["url"], asset.get("release_filename", name))
                with urllib.request.urlopen(url, timeout=120) as response, temporary.open("wb") as output:
                    shutil.copyfileobj(response, output)
            else:
                raise FileNotFoundError(f"Missing {name}. Supply --source or explicitly --fetch published media.")
            if not matches(temporary, asset):
                raise ValueError(f"Published media does not match its manifest: {name}")
            pending.append((temporary, target))
        staged_manifest = Path(staging) / "manifest.json"
        staged_manifest.write_text(json.dumps(manifest, indent=2) + "\n")
        for temporary, target in pending:
            temporary.replace(target)
        staged_manifest.replace(destination / "manifest.json")
    return completed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "media/walkthrough/published.json")
    parser.add_argument("--site", type=Path, default=ROOT / "dist/decks/site")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    print(json.dumps({"staged": stage(manifest, args.site, source=args.source, fetch=args.fetch)}))


if __name__ == "__main__":
    main()
