"""Real timetable coverage, independent scoring, and bounded candidate execution."""
import json
import subprocess
from pathlib import Path

import pytest

from forge_workshop_kit import transit


def test_pinned_real_archive_and_exception():
    data = transit.load_data()
    assert data["manifest"]["archive_sha256"] == "a034da05b7d71d9ce8977b9c59bee831cec52c4bf4a560ae3ad09e3064c27bcd"
    assert len(data["stop_times"]) == 6260
    assert {"service_id": "ThanksgivingDay", "date": "20241128", "exception_type": "1", "holiday_name": "Thanksgiving Day"} in data["calendar_dates"]
    row = next(r for r in data["stop_times"] if r["trip_id"] == "63926435" and r["stop_id"] == "70076")
    assert row["departure_time"] == "24:08:00"
    result = transit.reference_departures(data, "70076", "2024-11-29T00:00:00-05:00")
    actual = next(r for r in result if r["trip_id"] == "63926435")
    assert actual["departure_time"] == "2024-11-29T00:08:00-05:00"
    assert actual["service_date"] == "2024-11-28"


def test_weekday_holiday_and_utc_queries_differ_correctly():
    data = transit.load_data()
    holiday = transit.reference_departures(data, "70075", "2024-11-28T18:00:00-05:00")
    weekday = transit.reference_departures(data, "70075", "2024-11-29T18:00:00-05:00")
    assert holiday and weekday
    assert {r["trip_id"] for r in holiday}.isdisjoint(r["trip_id"] for r in weekday)
    assert weekday == transit.reference_departures(data, "70075", "2024-11-29T23:00:00+00:00")
    assert transit.reference_departures(data, "70076", "2024-11-29T02:00:00-05:00") == []


def test_last_direct_train_keeps_absolute_arrival_and_direction():
    data = transit.load_data()
    result = transit.reference_last_departure(data, "70080", "70072", "2024-11-28")
    assert result["arrival_time"] > result["departure_time"]
    assert result["departure_time"].startswith("2024-11-29")
    assert transit.reference_last_departure(data, "70072", "70080", "2024-11-28") is None
    assert transit.reference_last_departure(data, "70072", "70072", "2024-11-28") is None


@pytest.mark.parametrize("args", [
    ("place-pktrm", "2024-11-29T18:00:00-05:00", 5),
    ("70076", "2024-11-29T18:00:00", 5),
    ("70076", "2025-11-29T18:00:00-05:00", 5),
    ("70076", "2024-11-29T18:00:00-05:00", 0),
])
def test_query_contract_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        transit.reference_departures(transit.load_data(), *args)


@pytest.mark.parametrize("order", [1, 2])
def test_independent_reference_accepts_worked_sources_and_rejects_starter(order):
    result = transit.evaluate(transit.worked_sources(order), order)
    assert result["passed"] is True
    assert result["passed_count"] == result["total"]
    assert all(row["outputs"]["source_fingerprint"] == result["fingerprint"] for row in result["rows"])
    starter = transit.evaluate(transit.starter_sources(order), order)
    assert starter["passed"] is False
    assert starter["passed_count"] < starter["total"]


def test_prepared_repair_demonstrates_measured_implementation_gain():
    result = transit.qualify_service_day_repair()
    assert result["improved"]
    assert result["before"]["passed_count"] == 8
    assert result["after"]["passed_count"] == 10
    assert "no model calls" in result["kind"]


def test_prepared_task_claim_repair_uses_the_real_factory_transaction():
    result = transit.qualify_coordination_repair()
    assert result["improved"]
    assert result["before"]["successful_claims"] == 2
    assert result["after"]["successful_claims"] == 1
    owner = next(row["worker"] for row in result["after"]["attempts"] if row["claimed"])
    assert result["after"]["saved_owner"] == owner


def test_public_tests_allow_workers_to_build_independent_files():
    partial = transit.starter_sources()
    partial["query.py"] = transit.WORKED_QUERY
    assert transit.development_check(partial, transit.task_specs()[0])["passed"]
    assert not transit.development_check(partial, transit.task_specs()[1])["passed"]
    partial = transit.starter_sources()
    partial["presentation.py"] = transit.WORKED_PRESENTATION
    assert transit.development_check(partial, transit.task_specs()[1])["passed"]
    assert not transit.development_check(partial, transit.task_specs()[0])["passed"]


def test_worker_sources_contain_contract_but_not_acceptance_cases():
    sources = transit.starter_sources()
    assert set(sources) == {"query.py", "presentation.py", "contract.md", "sample.json"}
    assert "final-day" not in json.dumps(sources)
    assert "2024-12-04T12:00" not in json.dumps(sources)


@pytest.mark.parametrize("order", [1, 2])
def test_reserved_cases_exclude_public_ids_and_outputs_are_integrated(order):
    public = {row["case_id"] for row in transit._cases(order, public=True)}
    reserved = {row["case_id"] for row in transit._cases(order, public=False)}
    assert not public.intersection(reserved)
    result = transit.evaluate(transit.worked_sources(order), order)
    by_id = {row["case_id"]: row for row in result["rows"]}
    for case_id in reserved:
        assert by_id["integrated/"+case_id]["outputs"]["prediction"] == by_id[case_id]["outputs"]["prediction"]


def test_presentation_escapes_titles_and_shows_query_values():
    sources = transit.worked_sources()
    result = transit.run_sources(sources, [{"call": "presentation.render_board", "args": [
        [{"stop_name": "<img src=x onerror=alert(1)>", "headsign": "<b>North</b>", "departure_time": "2024-11-29T00:08:00-05:00"}], "<script>bad</script>"]}])
    value = result["results"][0]["value"]
    assert "<script>" not in value and "<img" not in value and "<b>" not in value
    assert "&lt;img" in value and "2024-11-29T00:08:00-05:00" in value


def test_source_import_policy_and_timeout():
    sources = transit.worked_sources()
    sources["query.py"] = "import os\n" + sources["query.py"]
    with pytest.raises(ValueError, match="approved"):
        transit.run_sources(sources, [])
    sources["query.py"] = "def departures(*args):\n    while True: pass\n"
    result = transit.run_sources(sources, [{"call": "query.departures", "args": ["70076", "2024-11-29T18:00:00-05:00"]}], timeout=.1)
    assert result["status"] == "timeout"


def test_child_environment_omits_credentials(monkeypatch):
    monkeypatch.setenv("WANDB_API_KEY", "never-send-this-to-worker-code")
    actual = subprocess.run
    captured = {}
    def inspect(*args, **kwargs):
        captured.update(kwargs["env"])
        return actual(*args, **kwargs)
    monkeypatch.setattr(subprocess, "run", inspect)
    assert transit.run_sources(transit.worked_sources(), [
        {"call": "query.departures", "args": ["70076", "2024-11-29T00:00:00-05:00"]}])["status"] == "completed"
    assert "WANDB_API_KEY" not in captured
    assert set(captured) <= {"HOME", "USERPROFILE", "TMPDIR", "TEMP", "TMP", "SYSTEMROOT", "WINDIR"}


def test_export_is_runnable_and_contains_no_credentials(tmp_path):
    result = transit.export_app(transit.worked_sources(2), tmp_path / "product", order=2)
    app = Path(result["app"])
    compile(app.read_text(), str(app), "exec")
    assert (app.parent / "query.py").read_text() == transit.WORKED_QUERY
    assert transit.load_data(app.parent)["manifest"]["dataset_id"] == transit.DATASET_ID
    assert "WANDB_API_KEY" not in app.read_text()


def test_changed_dataset_bytes_are_rejected(tmp_path):
    for name in ("manifest.json", "tables.json.gz", "developers-license-agreement.pdf"):
        (tmp_path / name).write_bytes((transit.ASSETS / name).read_bytes())
    (tmp_path / "tables.json.gz").write_bytes(b"changed")
    with pytest.raises(ValueError, match="checksum"):
        transit.load_data(tmp_path)
