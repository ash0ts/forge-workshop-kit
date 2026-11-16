"""Install the portable visual skill and its optional global default instruction."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "teenage-engineering-visualizations"
SOURCE = ROOT / "skills" / NAME
START = "<!-- teenage-engineering-visualizations:begin -->"
END = "<!-- teenage-engineering-visualizations:end -->"
RULE = f"""{START}
## Technical visuals

Use the global `teenage-engineering-visualizations` skill by default for technical
diagrams, process and project explanations, system overviews, incremental teaching
visuals, and technical posters. It owns the visual direction, templates, rendering,
and checks; do not route these tasks through other visual or design skills. Read its
`SKILL.md` in the global skills directory. Explicit requests for another style take
precedence. This default does not apply to unrelated UI design, photos, or artwork.
{END}"""
EXCLUDED = {"node_modules", "__pycache__", ".DS_Store", ".git", ".venv", "dist"}


def source_files(source=SOURCE):
    return [p for p in sorted(source.rglob("*")) if p.is_file()
            and not EXCLUDED.intersection(p.relative_to(source).parts)
            and p.suffix != ".pyc"]


def instruction(text):
    if (START in text) != (END in text):
        raise ValueError("Incomplete existing visual-skill instruction; inspect AGENTS.md first.")
    if START in text:
        before, tail = text.split(START, 1)
        _, after = tail.split(END, 1)
        return before + RULE + after
    return text.rstrip() + ("\n\n" if text.strip() else "") + RULE + "\n"


def install(codex_home, *, default=False):
    codex_home = Path(codex_home).expanduser().resolve()
    destination = codex_home / "skills" / NAME
    destination.parent.mkdir(parents=True, exist_ok=True)
    inputs = source_files()
    if not inputs or not (SOURCE / "SKILL.md").is_file():
        raise ValueError("Skill source is incomplete.")
    existing = (codex_home / "AGENTS.md").read_text(encoding="utf-8") if (codex_home / "AGENTS.md").exists() else ""
    updated = instruction(existing) if default else existing
    manifest = {str(p.relative_to(SOURCE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    with tempfile.TemporaryDirectory(dir=destination.parent, prefix=".te-install-") as temporary:
        staged = Path(temporary) / NAME
        for path in inputs:
            target = staged / path.relative_to(SOURCE)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        (staged / "installation.json").write_text(json.dumps({"schema_version": 1, "files": manifest}, indent=2) + "\n", encoding="utf-8")
        if destination.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = codex_home / "skill-backups" / f"{NAME}-{stamp}"
            backup.parent.mkdir(parents=True, exist_ok=True)
            destination.rename(backup)
        staged.rename(destination)
    if default and updated != existing:
        agents = codex_home / "AGENTS.md"
        with tempfile.NamedTemporaryFile(mode="w", dir=codex_home, prefix=".agents-", delete=False, encoding="utf-8", newline="\n") as output:
            output.write(updated)
            temporary_path = Path(output.name)
        temporary_path.replace(agents)
    for relative, expected in manifest.items():
        if hashlib.sha256((destination / relative).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Installed file differs: {relative}")
    return {"destination": str(destination), "files": len(manifest), "default": default}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser())
    parser.add_argument("--default", action="store_true", help="Make this the default for technical visuals in global AGENTS.md")
    args = parser.parse_args()
    print(json.dumps(install(args.codex_home, default=args.default), indent=2))


if __name__ == "__main__":
    main()
