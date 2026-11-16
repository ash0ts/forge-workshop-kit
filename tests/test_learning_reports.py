"""Publication safety and the self-service links; no live API calls."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("learning_reports", ROOT / "scripts/publish_learning_reports.py")
reports = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reports)


def test_articles_build_without_authentication():
    for slug in reports.SLUGS:
        report, plan = reports.build_report(slug, "example/teaching")
        assert report.entity == "example"
        assert report.project == "teaching"
        assert plan["blocks"] >= 10
        assert len(plan["images"]) >= 2
        assert any("notebooks/" in url for url in plan["links"])
        model = report._to_model()
        assert model.spec.blocks


def test_every_native_figure_keeps_its_caption_and_full_size_link():
    for slug in reports.SLUGS:
        report, plan = reports.build_report(slug, "example/teaching")
        blocks = report._to_model().spec.model_dump(mode="json", by_alias=True, exclude_none=True)["blocks"]
        figures = [block for block in blocks if block["type"] == "image"]
        assert len(figures) == len(plan["images"])
        for figure in figures:
            assert figure["hasCaption"]
            assert figure["children"][0]["text"].strip()
            links = [child for child in figure["children"] if child.get("type") == "link"]
            assert links and links[0]["url"] == figure["url"]
        assert plan["render_sha256"] == reports.digest(json.dumps(blocks, sort_keys=True))


def test_report_mechanisms_share_the_notebook_and_deck_canvas():
    from xml.etree import ElementTree

    layout = json.loads((ROOT / "reports/figures-guide-layout.json").read_text(encoding="utf-8"))
    assert {row["report"] for row in layout["figures"]} == set(reports.SLUGS)
    for row in layout["figures"]:
        assert (row["width"], row["height"]) == (1200, 675)
        assert row["all_reveals_checked"]
        svg = ElementTree.parse(ROOT / row["svg"]).getroot()
        assert svg.attrib["viewBox"] == "0 0 1200 675"
        assert row["png"].split("/", 1)[1] in (ROOT / "reports" / f"{row['report']}.md").read_text(encoding="utf-8")


def test_interrupted_creation_never_creates_another_report(tmp_path):
    receipts = {"pending": {"project": "example/teaching", "status": "creating"}}
    report, plan = reports.build_report("pending", "example/teaching")
    with pytest.raises(RuntimeError, match="creation was interrupted"):
        reports.publish(report, plan, receipts, tmp_path / "receipt.json")


def test_destination_mismatch_fails_before_publication(tmp_path):
    receipts = {"pending": {"project": "another/project", "id": "existing"}}
    report, plan = reports.build_report("pending", "example/teaching")
    with pytest.raises(ValueError, match="Receipt destination"):
        reports.publish(report, plan, receipts, tmp_path / "receipt.json")


def test_anonymous_readback_rejects_changed_content(monkeypatch):
    report, _ = reports.build_report("pending", "example/teaching")
    report.id = "recorded"
    model = report._to_model().spec.model_dump(mode="json", by_alias=True, exclude_none=True)
    view = {"project": {"entityName": "example", "name": "teaching"}, "displayName": report.title, "spec": json.dumps(model)}
    monkeypatch.setattr(reports, "public_query", lambda *_: {"view": view})
    assert reports.public_readback(report, "example/teaching")["anonymous_readback"]
    model["blocks"].pop()
    view["spec"] = json.dumps(model)
    with pytest.raises(RuntimeError, match="blocks differ"):
        reports.public_readback(report, "example/teaching")


def test_partial_publication_keeps_links_from_older_receipts():
    project = "example/teaching"
    receipts = {}
    for slug in reports.SLUGS:
        _, plan = reports.build_report(slug, project)
        receipts[slug] = {**plan, "status": "published", "url": f"https://wandb.ai/{project}/reports/learning--{slug}", "anonymous_readback": True}
    previous = reports.build_catalog(project, receipts, {})
    for slug in reports.SLUGS[1:]:
        del receipts[slug]["notebook_url"]
        del receipts[slug]["deck_url"]
    assert reports.build_catalog(project, receipts, previous) == previous
    # A fresh checkout can adopt one Report without dropping the other catalog entries.
    assert reports.build_catalog(project, {"pending": receipts["pending"]}, previous) == previous


def test_catalog_does_not_attach_current_links_to_an_unmatched_published_source():
    _, plan = reports.build_report("pending", "example/teaching")
    receipt = {**plan, "status": "published", "source_sha256": "an-older-source", "url": "https://wandb.ai/example/teaching/reports/learning--pending", "anonymous_readback": True}
    del receipt["notebook_url"]
    del receipt["deck_url"]
    with pytest.raises(RuntimeError, match="older published source"):
        reports.build_catalog("example/teaching", {"pending": receipt}, {})


def test_fresh_checkout_must_adopt_the_catalog_report():
    catalog = {"project": "example/teaching", "reports": {"pending": {"url": "https://wandb.ai/example/teaching/reports/learning--existing"}}}
    with pytest.raises(RuntimeError, match="--adopt pending=existing"):
        reports.check_catalog_identities("example/teaching", ["pending"], {}, catalog)
    reports.check_catalog_identities("example/teaching", ["pending"], {"pending": {"id": "existing"}}, catalog)
    reports.check_catalog_identities("another/destination", ["pending"], {}, catalog)
    with pytest.raises(ValueError, match="different Reports"):
        reports.check_catalog_identities("example/teaching", ["pending"], {"pending": {"id": "replacement"}}, catalog)
