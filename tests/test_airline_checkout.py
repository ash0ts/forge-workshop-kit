import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest


def test_pinned_airline_assets_survive_autocrlf_checkout(tmp_path):
    git = shutil.which("git")
    if git is None:
        pytest.skip("Git is required to verify checkout conversion")
    root = Path(__file__).resolve().parents[1]
    relative_assets = Path("src/forge_workshop_kit/assets/airline")
    repository = tmp_path / "repository"
    destination = tmp_path / "checkout"
    assets = repository / relative_assets
    assets.mkdir(parents=True)
    destination.mkdir()
    (repository / ".gitattributes").write_bytes((root / ".gitattributes").read_bytes())
    expected = {}
    for source in (root / relative_assets).iterdir():
        if source.is_file():
            expected[source.name] = source.read_bytes()
            (assets / source.name).write_bytes(expected[source.name])
    (repository / "ordinary.txt").write_bytes(b"first\nsecond\n")
    env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}

    def run(*arguments):
        return subprocess.run(
            [git, "-c", "core.autocrlf=true", "-c", "core.safecrlf=false", *arguments],
            cwd=repository, env=env, check=True, capture_output=True,
        )

    run("init", "--quiet")
    run("add", ".")
    run("checkout-index", "--all", f"--prefix={destination.as_posix()}/")
    # The control proves Git performed Windows-style conversion in this checkout.
    assert (destination / "ordinary.txt").read_bytes() == b"first\r\nsecond\r\n"
    for name, contents in expected.items():
        assert (destination / relative_assets / name).read_bytes() == contents
    data = destination / relative_assets
    provenance = json.loads((data / "provenance.json").read_bytes())
    assert hashlib.sha256((data / "cases.json").read_bytes()).hexdigest() == provenance["cases_sha256"]
