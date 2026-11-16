"""Build pinned notebooks, a wheel, and saved previews. Never publish or run exercises."""

import argparse
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
from release_support import sha256 as checksum


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


def build_aria_bundle(output, version, *, root=ROOT):
    """Package the twelve completed investigations for use without Forge access."""
    assets = root / "src/forge_workshop_kit/assets/aria"
    workshop_rows = json.loads((root / "src/forge_workshop_kit/workshops.json").read_text(encoding="utf-8"))["templates"]
    recordings = []

    def required_file(folder, name):
        candidate = (folder / name).resolve()
        if not candidate.is_relative_to(assets.resolve()) or not candidate.is_file() or candidate.stat().st_size == 0:
            raise ValueError(f"Missing or invalid ARIA recording file: {name}")
        return candidate

    for workshop in workshop_rows:
        for stop in workshop.get("aria_investigations", []):
            source = required_file(assets.parent, stop["recorded_example"])
            record = json.loads(source.read_text(encoding="utf-8"))
            if (record.get("status") != "recorded" or record.get("stop_id") != stop["id"]
                    or record.get("workshop") not in (workshop["slug"], workshop["id"])
                    or not all(record.get(key) for key in ("prompt", "response", "records", "citation_check"))):
                raise ValueError(f"ARIA recording is not complete: {source}")
            captures = record.get("captures", [])
            if not {"response", "verification"}.issubset({capture.get("role") for capture in captures}):
                raise ValueError(f"ARIA recording needs response and verification captures: {source}")
            for capture in captures:
                required_file(source.parent, capture["path"])
            for name in (record.get("excerpt_path"), *record.get("transcript_paths", {}).values()):
                if name:
                    required_file(source.parent, name)
            if not record.get("excerpt_path") or not record.get("transcript_paths", {}).get("html"):
                raise ValueError(f"ARIA recording needs offline source and transcript: {source}")
            recordings.append({"workshop": workshop["slug"], "stop": stop["id"], "id": record["id"],
                               "transcript": f"aria/{workshop['slug']}/{record['transcript_paths']['html']}"})

    if not recordings:
        raise ValueError("No completed ARIA investigations are configured.")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    destination = output / f"aria-investigations-v{version}.zip"
    readme = ("# Recorded ARIA investigations\n\n"
        "Unzip this package and open a transcript HTML file in your browser. No login is needed to read the bundled prompts, actual responses, source excerpts, and captures. Native Forge links still require their usual project access.\n\n"
        "These are instructor investigations, not results from your edits. Each transcript states what ARIA could inspect and which claims were checked. Original dataset/image licenses are retained beside their recordings; the kit source uses the included MIT license.\n\n"
        "The included Python files show how the notebook cards and transcripts are built. For the runnable notebooks and locked dependencies, use https://github.com/ash0ts/forge-workshop-kit.\n\n"
        + "\n".join(f"- [{row['workshop']} / {row['stop']}]({row['transcript']})" for row in recordings) + "\n")
    with tempfile.NamedTemporaryFile(dir=output, suffix=".zip", delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            def add(name, contents):
                entry = zipfile.ZipInfo(str(name), date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o644 << 16
                bundle.writestr(entry, contents)
            add("README.md", readme)
            for source in sorted(assets.rglob("*")):
                if source.is_file() and not source.name.startswith("."):
                    if source.is_symlink() or not source.resolve().is_relative_to(assets.resolve()):
                        raise ValueError(f"Unexpected link in ARIA assets: {source}")
                    add(Path("aria") / source.relative_to(assets), source.read_bytes())
            for name in ("LICENSE", "src/forge_workshop_kit/aria.py", "src/forge_workshop_kit/aria_client.py", "src/forge_workshop_kit/aria_visual.py", "scripts/build_aria_recordings.py", "docs/aria-investigations.md"):
                add(name, (root / name).read_bytes())
            file_count = len(bundle.namelist())
        temporary_path.replace(destination)
    finally:
        temporary_path.unlink(missing_ok=True)
    return {"file": destination.name, "sha256": checksum(destination), "bytes": destination.stat().st_size,
            "files": file_count, "recordings": len(recordings), "records": recordings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", action="append", choices=[row["slug"] for row in templates()])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    version = project_metadata()["version"]
    output = (args.output or ROOT / "dist" / f"v{version}").resolve()
    output.mkdir(parents=True, exist_ok=True)
    selected = [row for row in templates() if not args.only or row["slug"] in args.only]
    from build_visual_guides import build as build_guides
    build_guides(exports=True)
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
    manifest["aria_investigations"] = build_aria_bundle(output, version)
    visual_downloads = ROOT / "dist/visual-guides/downloads"
    manifest["visual_materials"] = []
    for source in sorted(visual_downloads.glob("*.zip")):
        destination = output / source.name
        shutil.copyfile(source, destination)
        manifest["visual_materials"].append({"file": destination.name, "sha256": checksum(destination), "bytes": destination.stat().st_size})
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
