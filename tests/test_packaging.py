"""Deployment and dependency checks use local fixtures; no remote writes or inference."""

import hashlib
import json
import sys
import tomllib
from pathlib import Path

import pytest

from forge_workshop_kit.manifest import get_workshop, list_templates, list_workshops

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import publish_templates
import release_support


def test_manifest_is_independent_and_preserves_workflow_identity():
    assert len(list_templates()) == 4
    assert len(list_workshops()) == 2
    solar = get_workshop("solar-autoresearch")
    assert solar["workflow_version"] == "1"
    solar["steps"].clear()
    assert get_workshop("solar-autoresearch")["steps"]


def metadata(header):
    return tomllib.loads(
        "\n".join(
            line.removeprefix("# ")
            for line in header.splitlines()[1 : header.splitlines().index("# ///", 1)]
        )
    )


def test_notebook_pins_only_its_selected_workshop():
    for row in list_templates():
        content = metadata(release_support.notebook_header(row["slug"], row["title"]))
        dependencies = content["dependencies"]
        version = release_support.project_metadata()["version"]
        assert f"v{version}/forge_workshop_kit-{version}" in dependencies[0]
        assert any(item.startswith("torch==") for item in dependencies) == (
            row["slug"] == "solar_autoresearch"
        )
        assert any(item.startswith("sunpy==") for item in dependencies) == (
            row["slug"] == "solar_autoresearch"
        )
        assert any(item.startswith("mcp==") for item in dependencies) == (
            row["slug"] == "pending_inc"
        )
        assert all("==" in item for item in dependencies[1:])
        assert set(dependencies[1:]) == set(
            release_support.locked_requirements(tuple(row["extras"]))
        )
        assert bool(content.get("tool", {}).get("uv", {}).get("sources")) == (
            row["slug"] == "solar_autoresearch"
        )


def test_dependency_groups_do_not_pull_science_into_base():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert not any(
        name in dep
        for dep in project["project"]["dependencies"]
        for name in ["torch", "sunpy", "scikit-learn", "mcp"]
    )
    assert "data-prep" in project["dependency-groups"]
    assert project["project"]["optional-dependencies"]["pending"] == ["mcp>=1.20,<2"]


def built_release(tmp_path):
    row = {"title": "Starter", "workflow_version": "1"}
    for key, name, content in [
        ("source", "starter.py", "print('saved')"),
        ("html", "starter.html", "<html>Saved preview</html>"),
    ]:
        (tmp_path / name).write_text(content)
        row[key] = {"file": name, "sha256": hashlib.sha256(content.encode()).hexdigest()}
    wheel = tmp_path / "package.whl"
    wheel.write_bytes(b"local fixture")
    manifest = {
        "release": release_support.project_metadata()["version"],
        "wheel": {"file": wheel.name, "sha256": publish_templates.sha256(wheel)},
        "templates": {"starter": row},
    }
    (tmp_path / "release-manifest.json").write_text(json.dumps(manifest))
    return row


def test_publish_rejects_modified_preview(tmp_path):
    built_release(tmp_path)
    (tmp_path / "starter.html").write_text("stale preview")
    with pytest.raises(ValueError, match="changed after validation"):
        publish_templates.load_build(tmp_path)


def test_destination_receipts_and_remote_ids_are_project_bound(tmp_path):
    path = tmp_path / "receipt.json"
    publish_templates.write_receipt(
        path, {"schema_version": 1, "project": "alice/lab", "templates": {}}
    )
    with pytest.raises(ValueError, match="another project"):
        publish_templates.load_receipt(path, "bob/lab")
    with pytest.raises(ValueError, match="Nothing was changed"):
        publish_templates.verify_destination(
            {"id": "old", "project": {"name": "lab", "entity": {"name": "alice"}}}, "bob/lab"
        )


def test_uncertain_creation_is_retained_without_duplicate(tmp_path):
    built_release(tmp_path)
    receipt = tmp_path / "deployment.json"

    class API:
        _service_api = None

        def __init__(self):
            self._service_api = self
            self.calls = 0

        def execute_graphql(self, query, variables):
            self.calls += 1
            raise TimeoutError("Create response was interrupted")

    api = API()
    with pytest.raises(TimeoutError):
        publish_templates.publish_one("alice/lab", tmp_path, receipt, "starter", api=api)
    assert json.loads(receipt.read_text())["templates"]["starter"]["status"] == "create_pending"
    with pytest.raises(RuntimeError, match="do not create a duplicate"):
        publish_templates.publish_one("alice/lab", tmp_path, receipt, "starter", api=api)
    assert api.calls == 1


def test_matching_remote_files_resume_without_upload(tmp_path, monkeypatch):
    built_release(tmp_path)
    receipt = tmp_path / "deployment.json"
    publish_templates.write_receipt(
        receipt,
        {
            "schema_version": 1,
            "project": "alice/lab",
            "templates": {"starter": {"id": "same", "status": "publishing"}},
        },
    )

    class API:
        def __init__(self):
            self._service_api = self

        def execute_graphql(self, query, variables):
            assert query.startswith("query"), (
                "No mutation is needed when the previous upload completed"
            )
            return {
                "notebook": {
                    "id": "same",
                    "project": {"name": "lab", "entity": {"name": "alice"}},
                    "currentVersion": {"artifactCollectionName": "test", "versionIndex": 2},
                }
            }

    monkeypatch.setattr(publish_templates, "remote_matches", lambda *args: True)
    publish_templates.publish_one("alice/lab", tmp_path, receipt, "starter", api=API())
    assert json.loads(receipt.read_text())["templates"]["starter"]["status"] == "verified"


def test_remote_readback_checks_source_and_preview_bytes(tmp_path):
    row = built_release(tmp_path)
    notebook = {"currentVersion": {"artifactCollectionName": "notebook", "versionIndex": 3}}

    class Entry:
        def __init__(self, path):
            self.path = path

        def download(self, root):
            return self.path

    class Artifact:
        def get_entry(self, name):
            return Entry(tmp_path / ("starter.py" if name == "notebook.py" else "starter.html"))

    class API:
        def artifact(self, path, type):
            assert path == "alice/lab/notebook:v3"
            assert type == "notebook"
            return Artifact()

    assert publish_templates.remote_matches(API(), notebook, "alice/lab", row)
    (tmp_path / "starter.html").write_text("preview from another source")
    assert not publish_templates.remote_matches(API(), notebook, "alice/lab", row)


def test_publish_rejects_wrong_destination_before_any_mutation(tmp_path):
    built_release(tmp_path)
    receipt = tmp_path / "deployment.json"
    publish_templates.write_receipt(
        receipt,
        {
            "schema_version": 1,
            "project": "bob/lab",
            "templates": {"starter": {"id": "alice-notebook"}},
        },
    )

    class API:
        def __init__(self):
            self._service_api = self

        def execute_graphql(self, query, variables):
            assert query.startswith("query"), "Must not rename or upload to a mismatched target"
            return {
                "notebook": {
                    "id": "alice-notebook",
                    "project": {"name": "lab", "entity": {"name": "alice"}},
                }
            }

    with pytest.raises(ValueError, match="not bob/lab"):
        publish_templates.publish_one("bob/lab", tmp_path, receipt, "starter", api=API())


def test_python_distribution_rejects_runtime_state(tmp_path):
    import tarfile
    import zipfile

    from build_release import check_distribution

    safe = tmp_path / "safe.whl"
    with zipfile.ZipFile(safe, "w") as archive:
        archive.writestr("forge_workshop_kit/workshops.json", "{}")
    assert check_distribution(safe)["files"] == 1
    for forbidden in (
        "artifacts/model/weights.pt",
        ".workshop/journal.json",
        ".env",
        "evidence/run.json",
        "data/solar-v1/aia.npz",
    ):
        wheel = tmp_path / "bad.whl"
        with zipfile.ZipFile(wheel, "w") as archive:
            archive.writestr(forbidden, "must not publish")
        with pytest.raises(ValueError, match="Runtime or presentation"):
            check_distribution(wheel)
    secret = tmp_path / "secret"
    secret.write_text("must not publish")
    sdist = tmp_path / "bad.tar.gz"
    with tarfile.open(sdist, "w:gz") as archive:
        archive.add(secret, arcname="forge_workshop_kit-0.3.0/.env")
    with pytest.raises(ValueError, match="Runtime or presentation"):
        check_distribution(sdist)
