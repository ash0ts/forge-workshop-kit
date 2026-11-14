"""Build pinned notebooks, a wheel, and saved previews. Never publish or run exercises."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

from release_support import ROOT, project_metadata, templates


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(args, *, env=None, timeout=300):
    subprocess.run(args, cwd=ROOT, env=env, check=True, timeout=timeout)


def check_distribution(path):
    """Reject runtime state or downloaded outputs before publishing Python packages."""
    path = Path(path)
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as bundle:
            names = bundle.namelist()
    else:
        with tarfile.open(path) as bundle:
            names = ["/".join(Path(name).parts[1:]) for name in bundle.getnames()]
    forbidden = {
        ".workshop",
        ".workshop-deployments",
        ".env",
        ".context",
        "artifacts",
        "wandb",
        "evidence",
        "decks",
        ".venv",
        "__pycache__",
        "__marimo__",
    }
    for name in names:
        parts = Path(name).parts
        if forbidden.intersection(parts) or (
            parts and parts[0] == "data" and name != "data/README.md"
        ):
            raise ValueError(
                f"Runtime or presentation material found in Python distribution: {name}"
            )
    return {
        "file": path.name,
        "sha256": checksum(path),
        "bytes": path.stat().st_size,
        "files": len(names),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", action="append", choices=[row["slug"] for row in templates()])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    version = project_metadata()["version"]
    output = (args.output or ROOT / "dist" / f"v{version}").resolve()
    output.mkdir(parents=True, exist_ok=True)
    selected = [row for row in templates() if not args.only or row["slug"] in args.only]
    # Generation uses the same lockfile for copied and local notebooks.
    for row in selected:
        run([sys.executable, "scripts/build_notebooks.py", "--only", row["slug"]])
    run(["uv", "build", "--out-dir", str(output)])
    wheel = output / f"forge_workshop_kit-{version}-py3-none-any.whl"
    if not wheel.is_file():
        raise RuntimeError("The built wheel does not match the package version.")
    sdist = output / f"forge_workshop_kit-{version}.tar.gz"
    manifest = {
        "schema_version": 1,
        "release": version,
        "wheel": check_distribution(wheel),
        "source_distribution": check_distribution(sdist),
        "templates": {},
    }
    for row in selected:
        source = ROOT / "notebooks" / (row["slug"] + ".py")
        destination = output / source.name
        shutil.copyfile(source, destination)
        html = output / (row["slug"] + ".html")
        run([sys.executable, "-m", "marimo", "check", str(source)])
        with tempfile.TemporaryDirectory(prefix="workshop-preview-") as directory:
            environment = {
                key: value
                for key, value in os.environ.items()
                if not any(
                    token in key.upper() for token in ("API_KEY", "TOKEN", "SECRET", "PASSWORD")
                )
            }
            environment.update(
                WANDB_MODE="disabled",
                WANDB_API_KEY="",
                WORKSHOP_STATE_DIR=directory,
                SUNPY_CONFIGDIR=directory,
                MPLCONFIGDIR=directory,
            )
            environment.pop("WORKSHOP_PROJECT", None)
            environment.pop("WANDB_ENTITY", None)
            environment.pop("WANDB_PROJECT", None)
            environment.pop("WANDB_NOTEBOOK_COLLECTION", None)
            environment.pop("WANDB_NOTEBOOK_ANCHOR_RUN", None)
            run(
                [
                    sys.executable,
                    "-m",
                    "marimo",
                    "export",
                    "html",
                    str(source),
                    "--no-include-code",
                    "--no-sandbox",
                    "--force",
                    "-o",
                    str(html),
                ],
                env=environment,
            )
        manifest["templates"][row["slug"]] = {
            "title": row["title"],
            "workshop_id": row["id"],
            "workflow_version": row["workflow_version"],
            "source": {"file": destination.name, "sha256": checksum(destination)},
            "html": {"file": html.name, "sha256": checksum(html)},
        }
    manifest["lock_sha256"] = checksum(ROOT / "uv.lock")
    (output / "release-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"Built {len(selected)} templates in {output}. Nothing was published.")


if __name__ == "__main__":
    main()
