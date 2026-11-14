"""A small transit product built against real, pinned MBTA timetable records.

The reference scorer stays outside worker directories. Candidate code runs in a
bounded child process without inherited credentials. This is reviewed local code
execution, not an operating-system security sandbox.
"""
from __future__ import annotations

import ast
import gzip
import hashlib
import html
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ASSETS = Path(__file__).parent / "assets" / "transit"
DATASET_ID = "mbta-red-central-20241128-v1"
START, END = date(2024, 11, 28), date(2024, 12, 4)
LOCAL = timezone(timedelta(hours=-5))  # The pinned week contains no DST transition.
EDITABLE_FILES = ("query.py", "presentation.py")


def load_data(root=None):
    root = Path(root or ASSETS)
    manifest = json.loads((root / "manifest.json").read_text())
    if manifest["dataset_id"] != DATASET_ID:
        raise ValueError("This workshop requires the pinned historical timetable.")
    for name, expected in manifest["files"].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Dataset checksum mismatch: {name}")
    tables = json.loads(gzip.decompress((root / "tables.json.gz").read_bytes()))
    return {**tables, "manifest": manifest}


def public_tables(data=None):
    return {k: v for k, v in (data or load_data()).items() if k != "manifest"}


def data_manifest():
    return load_data()["manifest"]


def _day(value):
    day = date.fromisoformat(value)
    if not START <= day <= END:
        raise ValueError("Choose a service date from 2024-11-28 through 2024-12-04.")
    return day


def _active(data, day):
    stamp = day.strftime("%Y%m%d")
    weekday = day.strftime("%A").lower()
    active = {r["service_id"] for r in data["calendar"]
              if r["start_date"] <= stamp <= r["end_date"] and r[weekday] == "1"}
    for row in data["calendar_dates"]:
        if row["date"] == stamp:
            if row["exception_type"] == "1":
                active.add(row["service_id"])
            elif row["exception_type"] == "2":
                active.discard(row["service_id"])
    return active


def _instant(day, value):
    hours, minutes, seconds = map(int, value.split(":"))
    return datetime.combine(day, datetime.min.time(), tzinfo=LOCAL) + timedelta(hours=hours, minutes=minutes, seconds=seconds)


def _platform(data, stop_id):
    matches = [r for r in data["stops"] if r["stop_id"] == stop_id and r["location_type"] == "0"]
    if not matches:
        raise ValueError("Choose one of the ten platform stop IDs in this teaching subset.")
    return matches[0]


def reference_departures(data, stop_id, at, limit=5):
    """Independent oracle: materialize timetable occurrences, then query time."""
    stop = _platform(data, stop_id)
    now = datetime.fromisoformat(at)
    if now.utcoffset() is None:
        raise ValueError("The query timestamp must include a UTC offset.")
    now = now.astimezone(LOCAL)
    _day(now.date().isoformat())
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("Choose a limit from 1 to 20.")
    trips = {t["trip_id"]: t for t in data["trips"]}
    output = []
    for offset in range((END - START).days + 1):
        day = START + timedelta(days=offset)
        active = _active(data, day)
        for event in data["stop_times"]:
            if event["stop_id"] != stop_id or event["pickup_type"] == "1":
                continue
            trip = trips[event["trip_id"]]
            if trip["service_id"] not in active:
                continue
            departure = _instant(day, event["departure_time"])
            if now <= departure <= now + timedelta(hours=2):
                output.append({"trip_id": trip["trip_id"], "route_id": trip["route_id"],
                               "headsign": trip["trip_headsign"], "stop_id": stop_id,
                               "stop_name": stop["stop_name"], "service_date": day.isoformat(),
                               "departure_time": departure.isoformat()})
    return sorted(output, key=lambda r: (r["departure_time"], r["trip_id"]))[:limit]


def reference_last_departure(data, origin_id, destination_id, service_date):
    day = _day(service_date)
    _platform(data, origin_id)
    _platform(data, destination_id)
    if origin_id == destination_id:
        return None
    active = _active(data, day)
    trips = {r["trip_id"]: r for r in data["trips"] if r["service_id"] in active}
    origins = [r for r in data["stop_times"] if r["stop_id"] == origin_id and r["pickup_type"] != "1"]
    destinations = {r["trip_id"]: r for r in data["stop_times"]
                    if r["stop_id"] == destination_id and r["drop_off_type"] != "1"}
    choices = []
    for origin in origins:
        trip = trips.get(origin["trip_id"])
        dest = destinations.get(origin["trip_id"])
        if not trip or not dest or int(dest["stop_sequence"]) <= int(origin["stop_sequence"]):
            continue
        choices.append({"trip_id": trip["trip_id"], "route_id": trip["route_id"],
                        "headsign": trip["trip_headsign"], "origin_stop_id": origin_id,
                        "destination_stop_id": destination_id, "service_date": day.isoformat(),
                        "departure_time": _instant(day, origin["departure_time"]).isoformat(),
                        "arrival_time": _instant(day, dest["arrival_time"]).isoformat()})
    return max(choices, key=lambda r: (r["departure_time"], r["trip_id"])) if choices else None


CONTRACT = '''# Transit product contract
This is a historical timetable explorer, not live travel advice. MassDOT/MBTA
provide the schedule data. The subset covers ten central Red Line platforms,
2024-11-28 through 2024-12-04. All times in this week use UTC-05:00.

Only query.py and presentation.py may change. Use Python's standard library.
No network calls, new processes, package imports, or reads of files outside the
workspace. Inputs are plain JSON tables with original GTFS column names and
string values. Do not hard-code trip IDs or expected answers.

query.departures(tables, stop_id, at, limit=5) returns a list of records with:
trip_id, route_id, headsign, stop_id, stop_name, service_date (YYYY-MM-DD), and
departure_time (ISO timestamp with UTC offset). Return departures at or after
the supplied aware timestamp and no more than two hours later, sorted by
(departure_time, trip_id), limited to 1..20. An empty list means none in that
window. Invalid platform/date/naive timestamp/limit raises ValueError.
Apply the weekday calendar AND calendar_dates additions/removals. GTFS hours
may exceed 23: 24:08:00 belongs to the stated service day but occurs at 00:08
on the following civil day. Check the previous service day after midnight.
Ignore stop times with pickup_type=1. Parent station IDs are not platform IDs.

query.last_departure(tables, origin_id, destination_id, service_date) returns
the latest direct trip on that service date, with trip_id, route_id, headsign,
origin_stop_id, destination_stop_id, service_date, departure_time, arrival_time.
Use stop_sequence to ensure the destination follows the origin on the SAME
trip; respect pickup_type/drop_off_type=1. Times stay absolute, including
after-midnight arrivals. Return None for no direct trip or identical stops.
Choose the maximum (departure_time, trip_id) for deterministic ties.

presentation.render_board(rows, title='Departures') returns escaped, readable
HTML with a heading, the stop name, destination and departure timestamp for
each row; show 'No scheduled departures in the next two hours' for []. Include
'Historical schedule' and 'MassDOT' attribution. Never call data real-time.
presentation.render_journey(journey, title='Last direct train') similarly shows
the origin, destination, both absolute timestamps, and service date. For None,
show 'No direct train in this timetable subset'. Escape text including title.
The presentation worker can use sample.json without waiting for query.py.
'''

WORKED_QUERY = '''from datetime import date, datetime, timedelta, timezone

TZ = timezone(timedelta(hours=-5))
START, END = date(2024, 11, 28), date(2024, 12, 4)

def active_services(tables, day):
    stamp = day.strftime('%Y%m%d')
    weekday = day.strftime('%A').lower()
    active = {r['service_id'] for r in tables['calendar']
              if r['start_date'] <= stamp <= r['end_date'] and r[weekday] == '1'}
    for row in tables['calendar_dates']:
        if row['date'] == stamp:
            if row['exception_type'] == '1':
                active.add(row['service_id'])
            elif row['exception_type'] == '2':
                active.discard(row['service_id'])
    return active

def departure_at(day, gtfs_time):
    h, m, s = map(int, gtfs_time.split(':'))
    return datetime.combine(day, datetime.min.time(), tzinfo=TZ) + timedelta(hours=h, minutes=m, seconds=s)

def platform(tables, stop_id):
    for row in tables['stops']:
        if row['stop_id'] == stop_id and row['location_type'] == '0':
            return row
    raise ValueError('Choose a platform in the teaching subset.')

def service_day(value):
    day = date.fromisoformat(value)
    if not START <= day <= END:
        raise ValueError('Date outside the historical teaching week.')
    return day

def departures(tables, stop_id, at, limit=5):
    stop = platform(tables, stop_id)
    now = datetime.fromisoformat(at)
    if now.utcoffset() is None:
        raise ValueError('Include the timestamp UTC offset.')
    now = now.astimezone(TZ)
    service_day(now.date().isoformat())
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError('Limit must be 1..20.')
    trips = {r['trip_id']: r for r in tables['trips']}
    result = []
    for shift in (-1, 0, 1):
        day = now.date() + timedelta(days=shift)
        if not START <= day <= END:
            continue
        active = active_services(tables, day)
        for row in tables['stop_times']:
            trip = trips[row['trip_id']]
            if row['stop_id'] != stop_id or row['pickup_type'] == '1' or trip['service_id'] not in active:
                continue
            departure = departure_at(day, row['departure_time'])
            if now <= departure <= now + timedelta(hours=2):
                result.append(dict(trip_id=trip['trip_id'], route_id=trip['route_id'],
                    headsign=trip['trip_headsign'], stop_id=stop_id, stop_name=stop['stop_name'],
                    service_date=day.isoformat(), departure_time=departure.isoformat()))
    return sorted(result, key=lambda r: (r['departure_time'], r['trip_id']))[:limit]

def last_departure(tables, origin_id, destination_id, service_date):
    day = service_day(service_date)
    platform(tables, origin_id)
    platform(tables, destination_id)
    if origin_id == destination_id:
        return None
    active = active_services(tables, day)
    rows_by_trip = {}
    for row in tables['stop_times']:
        rows_by_trip.setdefault(row['trip_id'], []).append(row)
    result = []
    for trip in tables['trips']:
        if trip['service_id'] not in active:
            continue
        rows = sorted(rows_by_trip.get(trip['trip_id'], []), key=lambda r: int(r['stop_sequence']))
        origin = None
        for row in rows:
            if row['stop_id'] == origin_id and row['pickup_type'] != '1':
                origin = row
            if origin and row['stop_id'] == destination_id and row['drop_off_type'] != '1' and int(row['stop_sequence']) > int(origin['stop_sequence']):
                result.append(dict(trip_id=trip['trip_id'], route_id=trip['route_id'],
                    headsign=trip['trip_headsign'], origin_stop_id=origin_id,
                    destination_stop_id=destination_id, service_date=service_date,
                    departure_time=departure_at(day, origin['departure_time']).isoformat(),
                    arrival_time=departure_at(day, row['arrival_time']).isoformat()))
                break
    return max(result, key=lambda r: (r['departure_time'], r['trip_id'])) if result else None
'''

WORKED_PRESENTATION = '''from html import escape

def render_board(rows, title='Departures'):
    heading = '<h2>' + escape(str(title)) + '</h2>'
    notice = '<p>Historical schedule. Data provided by MassDOT / MBTA.</p>'
    if not rows:
        return heading + notice + '<p>No scheduled departures in the next two hours</p>'
    cells = ''.join('<tr><td>' + escape(str(row['stop_name'])) + '</td><td>' +
                    escape(str(row['headsign'])) + '</td><td><time>' +
                    escape(str(row['departure_time'])) + '</time></td></tr>' for row in rows)
    return heading + notice + '<table><thead><tr><th>Platform</th><th>Toward</th><th>Scheduled departure</th></tr></thead><tbody>' + cells + '</tbody></table>'

def render_journey(journey, title='Last direct train'):
    heading = '<h2>' + escape(str(title)) + '</h2>'
    notice = '<p>Historical schedule. Data provided by MassDOT / MBTA.</p>'
    if journey is None:
        return heading + notice + '<p>No direct train in this timetable subset</p>'
    fields = [('From platform', 'origin_stop_id'), ('To platform', 'destination_stop_id'),
              ('Service date', 'service_date'), ('Departs', 'departure_time'), ('Arrives', 'arrival_time')]
    return heading + notice + '<dl>' + ''.join('<dt>' + label + '</dt><dd>' +
        escape(str(journey[key])) + '</dd>' for label, key in fields) + '</dl>'
'''


def starter_sources(order=1):
    if order not in (1, 2):
        raise ValueError("Choose work order 1 or 2.")
    query = '''def departures(tables, stop_id, at, limit=5):
    """Read the shared contract, then implement the departure query."""
    return []

def last_departure(tables, origin_id, destination_id, service_date):
    """Work order 2 adds the last direct train between two platforms."""
    return None
'''
    presentation = '''from html import escape

def render_board(rows, title='Departures'):
    return '<h2>' + escape(title) + '</h2><p>The board is waiting for an implementation.</p>'

def render_journey(journey, title='Last direct train'):
    return '<h2>' + escape(title) + '</h2><p>The journey view is waiting for an implementation.</p>'
'''
    if order == 2:
        query = WORKED_QUERY[:WORKED_QUERY.index('def last_departure')]+query[query.index('def last_departure'):]
        presentation = WORKED_PRESENTATION[:WORKED_PRESENTATION.index('def render_journey')]+presentation[presentation.index('def render_journey'):]
    data = load_data()
    sample = reference_departures(data, "70076", "2024-11-29T00:00:00-05:00", 2)
    return {"query.py": query, "presentation.py": presentation, "contract.md": CONTRACT,
            "sample.json": json.dumps({"departures": sample,
                "journey": reference_last_departure(data, "70080", "70072", "2024-11-28"),
                "table_columns": {name: list(rows[0]) for name, rows in public_tables(data).items() if rows},
                "raw_stop_time": next(r for r in data["stop_times"] if r["trip_id"] == "63926435" and r["stop_id"] == "70076")}, indent=2)}


def worked_sources(order=1):
    sources = starter_sources(order)
    sources.update({"query.py": WORKED_QUERY, "presentation.py": WORKED_PRESENTATION})
    return sources


def task_specs(order=1):
    if order not in (1, 2):
        raise ValueError("Choose work order 1 or 2.")
    feature = "departures" if order == 1 else "last_departure"
    return [
        {"id": f"order-{order}-query", "title": "Query scheduled departures" if order == 1 else "Find the last direct train",
         "instructions": f"Implement query.{feature} to the contract. Read contract.md and sample.json. Preserve existing public functions. Run public checks before finishing. Return real timetable records, never hard-coded answers.",
         "editable_files": ["query.py"], "depends_on": [], "tags": ["gtfs", "service-day", "query"],
         "scope": "transit", "readable_files": ["contract.md", "sample.json", "query.py", "presentation.py"]},
        {"id": f"order-{order}-presentation", "title": "Show the departures board" if order == 1 else "Show the last-train itinerary",
         "instructions": "Implement presentation.render_board" + (" and render_journey" if order == 2 else "") + ". Read contract.md and sample.json. Use escaped readable HTML with historical-data attribution and useful empty states. The sample lets you work without waiting for query.py. Preserve existing functions.",
         "editable_files": ["presentation.py"], "depends_on": [], "tags": ["presentation", "contract"],
         "scope": "transit", "readable_files": ["contract.md", "sample.json", "query.py", "presentation.py"]},
    ]


def source_fingerprint(sources):
    return hashlib.sha256(json.dumps({k: sources[k] for k in EDITABLE_FILES}, sort_keys=True).encode()).hexdigest()


def validate_sources(sources):
    if any(name not in sources for name in EDITABLE_FILES):
        raise ValueError("Both query.py and presentation.py are required.")
    allowed = {"datetime", "html", "math", "collections", "itertools", "functools", "re", "json", "typing", "bisect"}
    for name in EDITABLE_FILES:
        if not isinstance(sources[name], str) or len(sources[name].encode()) > 50000:
            raise ValueError(f"Keep {name} under 50 KiB of Python source.")
        tree = ast.parse(sources[name], filename=name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(a.name.split('.')[0] not in allowed for a in node.names):
                raise ValueError("Candidate imports must use the approved standard-library modules.")
            if isinstance(node, ast.ImportFrom) and (node.level or (node.module or '').split('.')[0] not in allowed):
                raise ValueError("Candidate imports must use the approved standard-library modules.")
            if isinstance(node, ast.Name) and node.id in {"open", "exec", "eval", "compile", "__import__", "getattr", "setattr", "globals", "locals", "vars", "breakpoint", "input"}:
                raise ValueError("Use pure query and rendering functions without dynamic code or file access.")
            if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
                raise ValueError("Dunder introspection is outside the workshop function contract.")
    return source_fingerprint(sources)


CHILD_RUNNER = '''import contextlib, importlib.util, io, json, sys
from pathlib import Path
try:
    import resource
    resource.setrlimit(resource.RLIMIT_CPU, (8, 8))
    resource.setrlimit(resource.RLIMIT_FSIZE, (8*1024*1024, 8*1024*1024))
    try:
        resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    except (ValueError, OSError):
        pass
except ImportError:
    pass
payload = json.loads(sys.stdin.read())
modules = {}
for name in ('query', 'presentation'):
    spec = importlib.util.spec_from_file_location(name, Path(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        spec.loader.exec_module(module)
    modules[name] = module
results = []
for request in payload['requests']:
    try:
        module, function = request['call'].split('.')
        args = request['args']
        if module == 'query':
            args = [payload['tables']] + args
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            value = getattr(modules[module], function)(*args)
        results.append({'ok': True, 'value': value})
    except Exception as exc:
        results.append({'ok': False, 'error_type': type(exc).__name__, 'error': str(exc)[:1000]})
sys.stdout.write(json.dumps(results))
'''


def run_sources(sources, requests, *, data=None, timeout=15):
    fingerprint = validate_sources(sources)
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="forge-transit-") as folder:
        root = Path(folder)
        for name in EDITABLE_FILES:
            (root / name).write_text(sources[name])
        (root / "runner.py").write_text(CHILD_RUNNER)
        env = {name: os.environ[name] for name in ("SYSTEMROOT", "WINDIR") if name in os.environ}
        env.update({"HOME": str(root), "USERPROFILE": str(root), "TMPDIR": str(root), "TEMP": str(root), "TMP": str(root)})
        try:
            result = subprocess.run([sys.executable, "-I", "-S", "runner.py"], cwd=root,
                input=json.dumps({"tables": public_tables(data), "requests": requests}),
                text=True, capture_output=True, timeout=timeout, env=env, check=False)
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "results": [], "elapsed_seconds": time.perf_counter()-started,
                    "fingerprint": fingerprint, "error": "Candidate exceeded the local execution time limit."}
        if result.returncode or len(result.stdout) > 4_000_000:
            return {"status": "execution_failed", "results": [], "elapsed_seconds": time.perf_counter()-started,
                    "fingerprint": fingerprint, "exit_code": result.returncode,
                    "error": result.stderr[-2000:] or "Candidate output exceeded its limit."}
        try:
            values = json.loads(result.stdout)
            if not isinstance(values, list) or len(values) != len(requests):
                raise ValueError("Wrong result count")
        except (ValueError, TypeError) as exc:
            return {"status": "execution_failed", "results": [], "elapsed_seconds": time.perf_counter()-started,
                    "fingerprint": fingerprint, "error": "Invalid candidate output: " + str(exc)}
    return {"status": "completed", "results": values, "fingerprint": fingerprint,
            "elapsed_seconds": time.perf_counter()-started, "exit_code": 0}


def _cases(order, public=False):
    base = [
        ("weekday-evening", "70076", "2024-11-29T18:00:00-05:00", 5),
        ("previous-service-day", "70076", "2024-11-29T00:00:00-05:00", 5),
        ("holiday-addition", "70075", "2024-11-28T18:00:00-05:00", 5),
        ("quiet-hours", "70076", "2024-11-29T02:00:00-05:00", 5),
        ("weekend", "70080", "2024-11-30T15:00:00-05:00", 3),
        ("utc-input", "70072", "2024-12-02T23:00:00+00:00", 4),
        ("other-direction", "70071", "2024-12-03T00:20:00-05:00", 4),
        ("final-day", "70077", "2024-12-04T12:00:00-05:00", 3),
    ]
    selected = base[:3] if public else base[3:]
    cases = [{"case_id": "departures/"+r[0], "call": "query.departures", "args": list(r[1:])} for r in selected]
    if order == 2:
        journeys = [
            ("holiday-last", "70080", "70072", "2024-11-28"),
            ("weekday-last", "70080", "70072", "2024-11-29"),
            ("wrong-direction", "70072", "70080", "2024-11-29"),
            ("weekend-last", "70071", "70079", "2024-11-30"),
            ("sunday-last", "70078", "70074", "2024-12-01"),
            ("same-platform", "70076", "70076", "2024-12-02"),
        ]
        cases += [{"case_id": "last-train/"+r[0], "call": "query.last_departure", "args": list(r[1:])}
                  for r in (journeys[:2] if public else journeys[2:])]
    return cases


def _expected(data, case):
    fn = reference_departures if case["call"] == "query.departures" else reference_last_departure
    return fn(data, *case["args"])


def _presentation_checks(sources, order, data):
    board = reference_departures(data, "70076", "2024-11-29T00:00:00-05:00", 2)
    journey = reference_last_departure(data, "70080", "70072", "2024-11-28")
    title = '<script>alert("x")</script>'
    requests = [{"call": "presentation.render_board", "args": [board, title]},
                {"call": "presentation.render_board", "args": [[], "Departures"]}]
    required = [["Historical schedule", "MassDOT", "Park Street"]+[r["departure_time"] for r in board],
                ["No scheduled departures in the next two hours"]]
    if order == 2:
        requests += [{"call": "presentation.render_journey", "args": [journey, "Last train"]},
                     {"call": "presentation.render_journey", "args": [None, "Last train"]}]
        required += [[journey[k] for k in ("departure_time", "arrival_time", "service_date", "origin_stop_id", "destination_stop_id")],
                     ["No direct train in this timetable subset"]]
    execution = run_sources(sources, requests, data=data)
    checks = []
    for index, req in enumerate(requests):
        result = execution["results"][index] if index < len(execution["results"]) else {"ok": False}
        value = result.get("value", "")
        passed = result.get("ok") and isinstance(value, str) and all(word in value for word in required[index])
        if index == 0:
            passed = passed and '<script>' not in value and html.escape(title) in value
        checks.append({"case_id": "presentation/"+str(index), "passed": bool(passed),
                       "expected_fields": required[index], "output": value, "error": result.get("error")})
    return checks, execution


def development_check(sources, task=None, order=1):
    data = load_data()
    task_id = task.get("id", "") if isinstance(task, dict) else getattr(task, "id", str(task or ""))
    if "order-2" in task_id:
        order = 2
    checks = []
    if not task_id or "query" in task_id:
        cases = _cases(order, public=True)
        result = run_sources(sources, cases, data=data)
        for index, case in enumerate(cases):
            actual = result["results"][index] if index < len(result["results"]) else {"ok": False, "error": result.get("error")}
            expected = _expected(data, case)
            checks.append({"case_id": case["case_id"], "passed": actual.get("ok", False) and actual.get("value") == expected,
                           "expected": expected, "actual": actual.get("value"), "error": actual.get("error")})
    if not task_id or "presentation" in task_id:
        presentation_checks, _ = _presentation_checks(sources, order, data)
        checks += presentation_checks
    return {"passed": bool(checks) and all(c["passed"] for c in checks), "checks": checks,
            "fingerprint": source_fingerprint(sources), "test_kind": "public development checks"}


def development_runner(workspace, task):
    sources = {name: (Path(workspace) / name).read_text() for name in EDITABLE_FILES}
    return development_check(sources, task)


def evaluate(sources, order=1):
    """Run all acceptance cases independently; never put these cases in prompts."""
    if order not in (1, 2):
        raise ValueError("Choose work order 1 or 2.")
    data = load_data()
    cases = _cases(order)
    execution = run_sources(sources, cases, data=data)
    rows = []
    for index, case in enumerate(cases):
        actual = execution["results"][index] if index < len(execution["results"]) else {"ok": False, "error": execution.get("error")}
        expected = _expected(data, case)
        correct = actual.get("ok", False) and actual.get("value") == expected
        rows.append({"case_id": case["case_id"], "inputs": {"function": case["call"], "arguments": case["args"]},
                     "outputs": {"prediction": actual.get("value"), "expected": expected, "error": actual.get("error"),
                                 "source_fingerprint": execution["fingerprint"]},
                     "scores": {"scenario_pass": float(correct)}, "status": "completed" if actual.get("ok") else "agent_error"})
    render_requests = []
    for row, case in zip(rows, cases):
        render = "render_board" if case["call"] == "query.departures" else "render_journey"
        render_requests.append({"call": "presentation." + render,
                                "args": [row["outputs"]["prediction"], "Acceptance result"]})
    presentation_execution = run_sources(sources, render_requests, data=data)
    for index, (query_row, case) in enumerate(zip(list(rows), cases)):
        rendered = presentation_execution["results"][index] if index < len(presentation_execution["results"]) else {"ok": False, "error": presentation_execution.get("error")}
        value = rendered.get("value", "")
        expected = query_row["outputs"]["expected"]
        if case["call"] == "query.departures":
            fields = ([str(r[key]) for r in expected for key in ("stop_name", "headsign", "departure_time")]
                      if expected else ["No scheduled departures in the next two hours"])
        else:
            fields = ([expected[key] for key in ("origin_stop_id", "destination_stop_id", "service_date", "departure_time", "arrival_time")]
                      if expected else ["No direct train in this timetable subset"])
        correct = bool(query_row["scores"]["scenario_pass"] and rendered.get("ok") and isinstance(value, str)
                       and all(html.escape(field) in value for field in fields)
                       and "Historical schedule" in value and "MassDOT" in value)
        rows.append({"case_id": "integrated/" + case["case_id"], "inputs": query_row["inputs"],
                     "outputs": {"html": value, "prediction": query_row["outputs"]["prediction"],
                                 "error": rendered.get("error"), "source_fingerprint": execution["fingerprint"]},
                     "scores": {"scenario_pass": float(correct)},
                     "status": "completed" if rendered.get("ok") else "agent_error"})
    passed = sum(r["scores"]["scenario_pass"] for r in rows)
    return {"order": order, "dataset_id": DATASET_ID, "rows": rows, "passed": passed == len(rows),
            "passed_count": int(passed), "total": len(rows),
            "source_fingerprint": hashlib.sha256(json.dumps(sources, sort_keys=True, allow_nan=False).encode()).hexdigest(),
            "scenario_pass_rate": passed / len(rows), "fingerprint": execution["fingerprint"],
            "elapsed_seconds": execution["elapsed_seconds"] + presentation_execution["elapsed_seconds"],
            "status": execution["status"], "kind": "reserved deterministic acceptance",
            "partition": "reserved; excludes public development case identities"}


def qualify_service_day_repair():
    """A deterministic service-day repair, not a claim about an agent run."""
    after = worked_sources()
    before = dict(after)
    before["query.py"] = before["query.py"].replace("for shift in (-1, 0, 1):", "for shift in (0, 1):")
    bad, good = evaluate(before), evaluate(after)
    return {"kind": "prepared implementation repair; no model calls", "before": bad, "after": good,
            "change": "Include the previous service day when querying shortly after midnight.",
            "improved": good["passed_count"] > bad["passed_count"], "inference_cost_usd": 0.0}


def qualify_coordination_repair():
    """Expose a task-claim race, then exercise the real atomic claim operation.

    The barrier makes both demonstration workers read the initial status before
    either writes. There are no model calls and no claimed agent-performance gain.
    """
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    from .factory import FactoryStop, TaskBoard

    row = {"status": "pending"}
    barrier = Barrier(2)

    def unsafe_claim(worker):
        observed = row["status"]
        barrier.wait(timeout=5)
        if observed == "pending":
            row.update(status="running", worker=worker)
            return {"worker": worker, "claimed": True}
        return {"worker": worker, "claimed": False}

    with ThreadPoolExecutor(max_workers=2) as pool:
        before = list(pool.map(unsafe_claim, ["worker-a", "worker-b"]))
    with tempfile.TemporaryDirectory(prefix="forge-claim-check-") as folder:
        board = TaskBoard(folder, task_specs()[:1], starter_sources())

        def atomic_claim(worker):
            try:
                board.claim("order-1-query", worker)
                return {"worker": worker, "claimed": True}
            except FactoryStop:
                return {"worker": worker, "claimed": False}

        with ThreadPoolExecutor(max_workers=2) as pool:
            after = list(pool.map(atomic_claim, ["worker-a", "worker-b"]))
        saved_owner = board.snapshot()["tasks"]["order-1-query"]["worker_id"]
    return {"kind": "prepared task-claim implementation repair; no model calls",
            "before": {"attempts": before, "successful_claims": sum(r["claimed"] for r in before)},
            "after": {"attempts": after, "successful_claims": sum(r["claimed"] for r in after),
                      "saved_owner": saved_owner},
            "invariant": "One pending task has at most one active owner.",
            "change": "Check readiness and save ownership in one locked TaskBoard transaction.",
            "improved": sum(r["claimed"] for r in before) == 2 and sum(r["claimed"] for r in after) == 1,
            "inference_cost_usd": 0.0}


def export_app(sources, destination, order=1):
    """Export a self-contained editable marimo product with its pinned data."""
    validate_sources(sources)
    root = Path(destination)
    root.mkdir(parents=True, exist_ok=True)
    for name in EDITABLE_FILES:
        (root / name).write_text(sources[name])
    for name in ("manifest.json", "tables.json.gz", "developers-license-agreement.pdf"):
        (root / name).write_bytes((ASSETS / name).read_bytes())
    (root / "contract.md").write_text(CONTRACT)
    app = '''# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo==0.25.2"]
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import gzip, json
    from pathlib import Path
    import query, presentation
    tables = json.loads(gzip.decompress((Path(__file__).parent / 'tables.json.gz').read_bytes()))
    return mo, tables, query, presentation

@app.cell
def _(mo, tables):
    _intro = mo.md("# The last train is still on yesterday’s timetable\\nHistorical schedule data from MassDOT / MBTA, November 28 to December 4, 2024. Choose a platform and a time to see departures during the next two hours. This teaching app does not show live arrivals.")
    _style = mo.Html("<style>table{border-collapse:collapse;width:100%}th,td{padding:12px 16px;text-align:left;border-bottom:1px solid #8885}th{font-weight:650}dt{margin-top:12px;font-weight:650}dd{margin:4px 0 12px}table time{white-space:nowrap}</style>")
    platforms = {r['stop_name'] + ' / ' + r.get('platform_name', '') + ' (' + r['stop_id'] + ')': r['stop_id'] for r in tables['stops'] if r['location_type'] == '0'}
    stop = mo.ui.dropdown(platforms, value=next(k for k,v in platforms.items() if v == '70076'), label='Departure platform')
    route = mo.ui.dropdown(['All routes in this subset', 'Red'], value='Red', label='Route')
    at = mo.ui.text(value='2024-11-29T00:00:00-05:00', label='Historical date and time, including UTC offset', full_width=True)
    mo.vstack([_intro, _style, route, stop, at])
    return stop, at, platforms, route

@app.cell
def _(mo, tables, query, presentation, stop, at, route):
    try:
        rows = query.departures(tables, stop.value, at.value)
        rows = [r for r in rows if route.value != 'Red' or r['route_id'] == route.value]
        mo.output.append(mo.Html(presentation.render_board(rows)))
    except (ValueError, KeyError, TypeError) as _error:
        mo.output.append(mo.callout(mo.md('Check the selected platform and date. Use an ISO timestamp such as `2024-11-29T00:00:00-05:00`. '+str(_error)), kind='warn'))
    return
'''
    if order == 2:
        app += '''
@app.cell
def _(mo, platforms):
    origin = mo.ui.dropdown(platforms, value=next(k for k,v in platforms.items() if v == '70080'), label='From platform')
    destination = mo.ui.dropdown(platforms, value=next(k for k,v in platforms.items() if v == '70072'), label='To platform')
    service_date = mo.ui.text(value='2024-11-28', label='Service date, YYYY-MM-DD', full_width=True)
    mo.vstack([mo.md('## Last direct train on this service date\\nChoose platforms in the same direction. This example finds a direct journey; it does not plan transfers.'), origin, destination, service_date])
    return origin, destination, service_date

@app.cell
def _(mo, tables, query, presentation, origin, destination, service_date):
    import json as _json
    try:
        journey = query.last_departure(tables, origin.value, destination.value, service_date.value)
        mo.output.append(mo.vstack([mo.Html(presentation.render_journey(journey)),
                   mo.download(_json.dumps(journey, indent=2).encode(), filename='last-direct-train.json', label='Download this itinerary')]))
    except (ValueError, KeyError, TypeError) as _error:
        mo.output.append(mo.callout(mo.md('Check the platforms and service date. Use a date from 2024-11-28 through 2024-12-04. '+str(_error)), kind='warn'))
    return
'''
    app += "\nif __name__ == '__main__':\n    app.run()\n"
    (root / "app.py").write_text(app)
    (root / "README.md").write_text("# Transit timetable product\n\nRun `uv run --with marimo==0.25.2 marimo edit app.py`. The product needs no provider credentials.\n\nHistorical timetable only, covering 2024-11-28 through 2024-12-04. Data provided by MassDOT and MBTA under the included Developers License Agreement. No affiliation or endorsement.\n")
    return {"directory": str(root), "app": str(root / "app.py"), "fingerprint": source_fingerprint(sources), "order": order}
