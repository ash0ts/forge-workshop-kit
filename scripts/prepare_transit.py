"""Prepare the pinned, historical MBTA teaching subset. No model calls."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import urllib.request
import zipfile
from datetime import date, timedelta
from pathlib import Path

ARCHIVE_URL = "https://cdn.mbtace.com/archive/20241128.zip"
ARCHIVE_SHA256 = "a034da05b7d71d9ce8977b9c59bee831cec52c4bf4a560ae3ad09e3064c27bcd"
DOC_REVISION = "02da961b963ba3d3a66042ca4d5bd19e21ce5c0a"
LICENSE_URL = f"https://raw.githubusercontent.com/mbta/gtfs-documentation/{DOC_REVISION}/developers-license-agreement.pdf"
LICENSE_SHA256 = "e791e24e86b9e974de060c3b238abfc392260cad54ccc0d2d3d4f0a61846b91a"
PLATFORMS = [str(n) for n in range(70071, 70081)]
START, END = date(2024, 11, 28), date(2024, 12, 4)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def get(url, expected, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with urllib.request.urlopen(url, timeout=120) as response:
            path.write_bytes(response.read())
    value = path.read_bytes()
    if digest(value) != expected:
        raise ValueError(f"Pinned source checksum mismatch: {path.name}")
    return value


def prepare(output, cache):
    archive = get(ARCHIVE_URL, ARCHIVE_SHA256, cache / "20241128.zip")
    license_data = get(LICENSE_URL, LICENSE_SHA256, cache / "mbta-license.pdf")
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        def rows(name):
            return list(csv.DictReader(io.TextIOWrapper(z.open(name), encoding="utf-8-sig")))

        calendar, exceptions = rows("calendar.txt"), rows("calendar_dates.txt")
        services = set()
        for offset in range((END - START).days + 1):
            day = START + timedelta(days=offset)
            stamp, weekday = day.strftime("%Y%m%d"), day.strftime("%A").lower()
            active = {r["service_id"] for r in calendar
                      if r["start_date"] <= stamp <= r["end_date"] and r[weekday] == "1"}
            for row in exceptions:
                if row["date"] == stamp:
                    if row["exception_type"] == "1":
                        active.add(row["service_id"])
                    elif row["exception_type"] == "2":
                        active.discard(row["service_id"])
            services.update(active)
        trips = [r for r in rows("trips.txt") if r["route_id"] == "Red" and r["service_id"] in services]
        trip_ids = {r["trip_id"] for r in trips}
        service_ids = {r["service_id"] for r in trips}
        stop_times = [r for r in csv.DictReader(io.TextIOWrapper(z.open("stop_times.txt"), encoding="utf-8-sig"))
                      if r["trip_id"] in trip_ids and r["stop_id"] in PLATFORMS]
        used_trips = {r["trip_id"] for r in stop_times}
        trips = [r for r in trips if r["trip_id"] in used_trips]
        stops = rows("stops.txt")
        parents = {r["parent_station"] for r in stops if r["stop_id"] in PLATFORMS}
        data = {
            "agency": [r for r in rows("agency.txt") if r["agency_id"] == "1"],
            "feed_info": rows("feed_info.txt"),
            "routes": [r for r in rows("routes.txt") if r["route_id"] == "Red"],
            "stops": [r for r in stops if r["stop_id"] in set(PLATFORMS) | parents],
            "trips": trips,
            "stop_times": stop_times,
            "calendar": [r for r in calendar if r["service_id"] in service_ids],
            "calendar_dates": [r for r in exceptions if r["service_id"] in service_ids],
        }
        for table in data.values():
            table.sort(key=lambda r: json.dumps(r, sort_keys=True))
        member_hashes = {name + ".txt": digest(z.read(name + ".txt")) for name in data}
    output.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    (output / "tables.json.gz").write_bytes(gzip.compress(encoded, mtime=0))
    (output / "developers-license-agreement.pdf").write_bytes(license_data)
    manifest = {
        "dataset_id": "mbta-red-central-20241128-v1", "archive_url": ARCHIVE_URL,
        "archive_sha256": ARCHIVE_SHA256, "archive_index": "https://cdn.mbta.com/archive/archived_feeds.txt",
        "source_member_sha256": member_hashes,
        "feed_version": data["feed_info"][0]["feed_version"],
        "valid_from": START.isoformat(), "valid_through": END.isoformat(),
        "agency_timezone": "America/New_York", "utc_offset_for_selected_dates": "-05:00",
        "route_ids": ["Red"], "platform_ids": PLATFORMS,
        "counts": {name: len(table) for name, table in data.items()},
        "selection": "All Red Line trips active during the archive validity week; stop times restricted to ten central platforms. Retain original columns and string values. Include parent stations, referenced calendars, and all exceptions for retained service IDs.",
        "limitations": "Historical scheduled departures, not observed arrivals or live predictions. Central Red Line subset only; no transfers, accessibility routing, fares, real-time disruptions, or dates outside the pinned week.",
        "license": "Massachusetts Department of Transportation Developers License Agreement (2009-11-13)",
        "license_url": LICENSE_URL, "license_sha256": LICENSE_SHA256,
        "attribution": "Contains historical schedule data provided by MassDOT and the MBTA. This independent teaching application is not affiliated with or endorsed by either agency.",
        "files": {name: digest((output / name).read_bytes()) for name in
                  ["tables.json.gz", "developers-license-agreement.pdf"]},
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"output": str(output), "counts": manifest["counts"],
                      "compressed_bytes": (output / "tables.json.gz").stat().st_size}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("src/forge_workshop_kit/assets/transit"))
    parser.add_argument("--cache", type=Path, default=Path(".cache/transit"))
    args = parser.parse_args()
    prepare(args.output, args.cache)
