"""Build metadata shared by notebook generation and release verification."""

import json
import subprocess
import tomllib
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/ash0ts/forge-workshop-kit"


def project_metadata():
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def notebook_build_uv_version():
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["tool"]["workshop-build"]["uv-version"]


def check_notebook_build_uv():
    expected = notebook_build_uv_version()
    result = subprocess.run(["uv", "--version"], check=True, capture_output=True, text=True, timeout=10)
    found = result.stdout.strip().split()
    if len(found) < 2 or found[1] != expected:
        raise RuntimeError(
            f"Notebook generation requires uv {expected}; found {result.stdout.strip()!r}. "
            "Install the build version from pyproject.toml before generating notebooks. "
            "This restriction does not apply to running participant notebooks."
        )


def templates():
    return json.loads((ROOT / "src/forge_workshop_kit/workshops.json").read_text(encoding="utf-8"))["templates"]


@cache
def locked_requirements(extras=()):
    check_notebook_build_uv()
    args = [
        "uv",
        "export",
        "--offline",
        "--no-cache",
        "--frozen",
        "--no-dev",
        "--no-group",
        "data-prep",
        "--no-emit-project",
        "--no-hashes",
        "--no-annotate",
        "--format",
        "requirements-txt",
    ]
    for extra in extras:
        args.extend(["--extra", extra])
    result = subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True, timeout=120)
    requirements = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-"):
            raise ValueError(f"Unexpected uv export option in dependency pins: {line}")
        requirements.append(line)
    return requirements


def notebook_header(slug, title):
    project = project_metadata()
    metadata = next(row for row in templates() if row["slug"] == slug)
    version = project["version"]
    extras = tuple(metadata["extras"])
    extra_suffix = "[" + ",".join(extras) + "]" if extras else ""
    wheel = (
        f"{REPOSITORY}/releases/download/v{version}/forge_workshop_kit-{version}-py3-none-any.whl"
    )
    dependencies = [f"forge-workshop-kit{extra_suffix} @ {wheel}", *locked_requirements(extras)]
    lines = [
        "# /// script",
        f"# requires-python = {json.dumps(project['requires-python'])}",
        "# dependencies = [",
    ]
    lines.extend("#   " + json.dumps(requirement) + "," for requirement in dependencies)
    lines.append("# ]")
    if "solar" in extras or "inspection" in extras:
        lines.extend(
            [
                "# [tool.uv.sources]",
                '# torch = [{ index = "pytorch-cpu", marker = "sys_platform != \'darwin\'" }]',
                "# [[tool.uv.index]]",
                '# name = "pytorch-cpu"',
                '# url = "https://download.pytorch.org/whl/cpu"',
                "# explicit = true",
            ]
        )
    lines.extend(
        [
            "# ///",
            "import marimo",
            '__generated_with = "0.25.2"',
            f'app = marimo.App(width="medium", app_title={title!r})',
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uv-version", action="store_true")
    args = parser.parse_args()
    if args.uv_version:
        print(notebook_build_uv_version())
