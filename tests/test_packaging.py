"""Deployment and dependency checks use local fixtures; no remote writes or inference."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from types import SimpleNamespace

import pytest

from forge_workshop_kit.manifest import get_workshop, list_templates, list_workshops

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import publish_templates
import release_support


def test_notebook_generation_writes_utf8_with_lf_without_utf8_locale(tmp_path):
    for name in (
        "scripts/build_notebooks.py", "scripts/notebook_builder.py",
        "scripts/pending_cells.py", "scripts/solar_cells.py", "scripts/release_support.py",
        "examples/solar/candidate.py", "src/forge_workshop_kit/workshops.json",
        "pyproject.toml", "uv.lock",
    ):
        destination = tmp_path / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)
    (tmp_path / "notebooks").mkdir()
    environment = {
        **os.environ, "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0", "LC_ALL": "C",
    }
    subprocess.run(
        [sys.executable, "scripts/build_notebooks.py", "--only", "facilitator"],
        cwd=tmp_path, env=environment, check=True, capture_output=True, timeout=120,
    )
    output = (tmp_path / "notebooks/facilitator.py").read_bytes()
    assert "participants’ public project links" in output.decode("utf-8")
    assert b"\r\n" not in output


def test_notebook_build_rejects_uv_exporter_drift(monkeypatch):
    expected = release_support.notebook_build_uv_version()
    monkeypatch.setattr(
        release_support.subprocess, "run",
        lambda *args, **kwargs: SimpleNamespace(stdout=f"uv {expected} (test build)"),
    )
    release_support.check_notebook_build_uv()
    monkeypatch.setattr(
        release_support.subprocess, "run",
        lambda *args, **kwargs: SimpleNamespace(stdout="uv 0.0.0 (different exporter)"),
    )
    with pytest.raises(RuntimeError, match="Notebook generation requires uv"):
        release_support.check_notebook_build_uv()


def test_manifest_is_independent_and_preserves_workflow_identity():
    assert {row['slug'] for row in list_templates()} == {'starter', 'facilitator', 'pending_inc', 'solar_autoresearch', 'request_routing', 'visual_inspection', 'transit_factory'}
    assert len(list_workshops()) == 5
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
            row["slug"] in ("solar_autoresearch", "visual_inspection")
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
            row["slug"] in ("solar_autoresearch", "visual_inspection")
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
        "notebooks/__marimo__/session/transit_factory.py.json",
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
    with tarfile.open(sdist, "w:gz") as archive:
        archive.add(secret, arcname="forge_workshop_kit-0.6.0/notebooks/__marimo__/session/transit_factory.py.json")
    with pytest.raises(ValueError, match="Runtime or presentation"):
        check_distribution(sdist)


def test_renamed_notebook_uploads_to_current_collection(tmp_path, monkeypatch):
    built_release(tmp_path)
    receipt = tmp_path / 'deployment.json'
    publish_templates.write_receipt(receipt, {
        'schema_version': 1, 'project': 'alice/lab',
        'templates': {'starter': {'id': 'same', 'status': 'publishing'}},
    })
    old_source = tmp_path / 'old.py'
    old_source.write_text('old template')
    calls = {'rename': 0, 'upload': 0, 'reads': 0}

    class Entry:
        def __init__(self, path):
            self.path = path
        def download(self, root):
            return self.path

    class API:
        def __init__(self):
            self._service_api = self
            self.name = 'Untitled'
            self.collection = 'Untitled'
            self.version = 0
            self.uploaded = {}
        def execute_graphql(self, query, variables):
            assert 'createNotebook' not in query, 'Resume the saved notebook identity.'
            if 'renameNotebook' in query:
                calls['rename'] += 1
                self.name = variables['n']
                self.collection = 'Starter-renamed-collection'
                return {'renameNotebook': {'notebook': {'id': 'same'}}}
            calls['reads'] += 1
            return {'notebook': {'id': 'same', 'name': self.name,
                'project': {'name': 'lab', 'entity': {'name': 'alice'}},
                'currentVersion': {'artifactCollectionName': self.collection, 'versionIndex': self.version}}}
        def artifact(self, path, type):
            assert path == f'alice/lab/{self.collection}:v{self.version}'
            assert type == 'notebook'
            return SimpleNamespace(get_entry=lambda name: Entry(self.uploaded.get(name, old_source)))
    api = API()

    class Artifact:
        def __init__(self, name, **kwargs):
            # This is the regression: the old implementation used Untitled here.
            assert name == api.collection == 'Starter-renamed-collection'
            self.files = {}
        def add_file(self, path, name):
            self.files[name] = Path(path)

    class Run:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def log_artifact(self, artifact):
            calls['upload'] += 1
            api.uploaded = artifact.files
            api.version += 1
            return SimpleNamespace(wait=lambda timeout: None)

    import wandb
    monkeypatch.setattr(wandb, 'init', lambda **kwargs: Run())
    monkeypatch.setattr(wandb, 'Artifact', Artifact)
    publish_templates.publish_one('alice/lab', tmp_path, receipt, 'starter', api=api)
    record = json.loads(receipt.read_text())['templates']['starter']
    assert record['status'] == 'verified'
    assert record['currentVersion']['artifactCollectionName'] == 'Starter-renamed-collection'
    assert calls == {'rename': 1, 'upload': 1, 'reads': 3}
    publish_templates.publish_one('alice/lab', tmp_path, receipt, 'starter', api=api)
    assert calls == {'rename': 1, 'upload': 1, 'reads': 4}
