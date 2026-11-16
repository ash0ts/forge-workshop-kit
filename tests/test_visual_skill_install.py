"""The global installer must preserve instructions and unrelated skills."""
import importlib.util
from pathlib import Path

import pytest


def installer():
    source = Path(__file__).parents[1] / "scripts/install_visual_skill.py"
    spec = importlib.util.spec_from_file_location("visual_skill_install", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_install_preserves_other_skills_and_replaces_only_its_rule(tmp_path):
    tool = installer()
    (tmp_path / "AGENTS.md").write_text("Keep my existing instruction. Café → ☀\n", encoding="utf-8")
    other = tmp_path / "skills" / "other" / "SKILL.md"
    other.parent.mkdir(parents=True)
    other.write_text("Unrelated skill")
    first = tool.install(tmp_path, default=True)
    second = tool.install(tmp_path, default=True)
    instructions = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert instructions.startswith("Keep my existing instruction. Café → ☀\n")
    assert instructions.count(tool.START) == 1
    assert other.read_text() == "Unrelated skill"
    assert first["files"] == second["files"]
    assert list((tmp_path / "skill-backups").iterdir())
    assert not list((tmp_path / "skills" / tool.NAME).rglob("node_modules"))


def test_install_without_default_leaves_instructions_unchanged(tmp_path):
    (tmp_path / "AGENTS.md").write_text("My instructions.\n")
    installer().install(tmp_path)
    assert (tmp_path / "AGENTS.md").read_text() == "My instructions.\n"


def test_incomplete_managed_rule_stops_before_installing(tmp_path):
    tool = installer()
    (tmp_path / "AGENTS.md").write_text(tool.START)
    with pytest.raises(ValueError, match="Incomplete"):
        tool.install(tmp_path, default=True)
    assert not (tmp_path / "skills" / tool.NAME).exists()
