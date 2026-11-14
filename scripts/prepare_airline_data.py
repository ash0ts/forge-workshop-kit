"""Extract small fictional airline cases from a pinned, MIT-licensed source.

Run explicitly during release preparation. Participant imports never download data.
These simplified requests are a teaching adaptation, not a tau-bench evaluation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import urllib.request

REVISION = "989d3285ae669e49503324bdb9981bf14fccedeb"
BASE = f"https://raw.githubusercontent.com/sierra-research/tau2-bench/{REVISION}/"
OUT = Path(__file__).resolve().parents[1] / "src/forge_workshop_kit/assets/airline"
PARTITIONS = {
    "discovery": [21, 7, 39, 41, 0, 5, 27, 1],
    "monitoring": [11, 12, 28, 42],
    "development": [33, 34, 10, 20],
    "final": [30, 32, 19, 13, 26, 31],
    "subsequent": [2, 6, 8, 16],
}


def read(path):
    raw = urllib.request.urlopen(BASE + path, timeout=30).read()
    return raw, hashlib.sha256(raw).hexdigest()


def source_user(task):
    text = json.dumps(task["user_scenario"]["instructions"])
    return re.search(r"[a-z]+_[a-z]+_[0-9]+", text).group()


def extract(db, task, partition, index):
    user_id = source_user(task)
    user = db["users"][user_id]
    reservations = sorted((db["reservations"][r] for r in user["reservations"]),
                          key=lambda r: (r["cabin"] == "basic_economy", len(r["flights"]) < 2, r["reservation_id"]))
    candidates = []
    for reservation in reservations:
        for pos, old in enumerate(reservation["flights"]):
            if old["date"] < "2024-05-16":
                continue
            for number, flight in sorted(db["flights"].items()):
                status = flight["dates"].get(old["date"], {})
                if (number != old["flight_number"] and flight["origin"] == old["origin"]
                        and flight["destination"] == old["destination"]
                        and status.get("status") == "available"
                        and status["available_seats"][reservation["cabin"]] >= len(reservation["passengers"])):
                    candidates.append((reservation, pos, pos + 1, [{"flight_number": number, "date": old["date"]}]))
        # A valid connection-to-nonstop change must not be mistaken for a dropped leg.
        for pos in range(len(reservation["flights"]) - 1):
            first, second = reservation["flights"][pos:pos + 2]
            if (first["date"] != second["date"] or first["destination"] != second["origin"]
                    or first["origin"] == second["destination"] or first["date"] < "2024-05-16"):
                continue
            for number, flight in sorted(db["flights"].items()):
                status = flight["dates"].get(first["date"], {})
                if (flight["origin"] == first["origin"] and flight["destination"] == second["destination"]
                        and status.get("status") == "available"
                        and status["available_seats"][reservation["cabin"]] >= len(reservation["passengers"])):
                    candidates.append((reservation, pos, pos + 2, [{"flight_number": number, "date": first["date"]}]))
    # Prefer a genuine partial change; all tie-breaking uses source identifiers, never scores.
    candidates.sort(key=lambda c: (c[0]["cabin"] == "basic_economy",
        len(c[0]["flights"]) == c[2] - c[1], -(c[2] - c[1]), c[0]["reservation_id"], c[1], c[3][0]["flight_number"]))
    if candidates:
        reservation, start, stop, replacement = candidates[index % min(len(candidates), 3)]
    else:
        reservation = reservations[0]
        start, stop = 0, 1
        replacement = [{k: reservation["flights"][0][k] for k in ("flight_number", "date")}]
    reservation = json.loads(json.dumps(reservation))
    flights = {}
    for info in reservation["flights"] + replacement:
        flight = db["flights"][info["flight_number"]]
        flights[info["flight_number"]] = {k: flight[k] for k in ("flight_number", "origin", "destination")}
        flights[info["flight_number"]]["dates"] = {info["date"]: flight["dates"][info["date"]]}
    kind = "change"
    if not candidates or index % 4 == 3:
        kind = "read_only"
    elif reservation["cabin"] == "basic_economy":
        kind = "restricted"
    flight_names = ", ".join(f["flight_number"] for f in reservation["flights"][start:stop])
    replacement_names = ", ".join(f["flight_number"] for f in replacement)
    mission = (f"My user ID is {user_id}. My reservation is {reservation['reservation_id']}. "
               f"Replace only {flight_names} with {replacement_names} on {replacement[0]['date']}. "
               "Keep all other flights, the passengers, and the cabin. Tell me the fare difference and ask before making the change.")
    if kind == "read_only":
        mission = (f"My user ID is {user_id}. Please tell me the flights in reservation {reservation['reservation_id']}. "
                   "Do not change or cancel anything.")
    methods = {k: {key: value for key, value in p.items() if key in ("source", "id", "amount")}
               for k, p in user["payment_methods"].items() if p["source"] == "credit_card"}
    if not methods:
        methods = {k: {key: value for key, value in p.items() if key in ("source", "id", "amount")}
                   for k, p in user["payment_methods"].items() if p["source"] == "gift_card"}
    return {"id": f"airline-{partition}-{index + 1:02d}", "partition": partition,
        "source_task_id": str(task["id"]), "family_id": user_id, "kind": kind,
        "mission": mission, "initial": {"reservation": reservation, "flights": flights,
            "user": {"user_id": user_id, "payment_methods": methods}},
        "passenger": {"replace_start": start, "replace_stop": stop, "replacement": replacement,
            "allows_write": kind == "change", "max_extra_dollars": 10000},
        "fault": "lookup_once" if index == 1 and partition in ("discovery", "monitoring", "subsequent") else None,
        "source_url": f"https://github.com/sierra-research/tau2-bench/blob/{REVISION}/data/tau2/domains/airline/tasks.json"}


def main():
    paths = ["LICENSE", "data/tau2/domains/airline/db.json", "data/tau2/domains/airline/tasks.json",
             "data/tau2/domains/airline/policy.md", "data/tau2/domains/airline/split_tasks.json"]
    sources = {path: read(path) for path in paths}
    db = json.loads(sources[paths[1]][0]); tasks = {int(t["id"]): t for t in json.loads(sources[paths[2]][0])}
    cases = [extract(db, tasks[task_id], partition, i) for partition, ids in PARTITIONS.items() for i, task_id in enumerate(ids)]
    families = {}
    for case in cases:
        previous = families.setdefault(case["family_id"], case["partition"])
        assert previous == case["partition"], "A source passenger crosses partitions"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "cases.json").write_bytes((json.dumps(cases, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8"))
    (OUT / "LICENSE.txt").write_bytes(sources["LICENSE"][0])
    (OUT / "upstream-policy.md").write_bytes(sources[paths[3]][0])
    manifest = {"revision": REVISION, "license": "MIT", "source": "https://github.com/sierra-research/tau2-bench",
        "source_checksums": {p: sha for p, (_, sha) in sources.items()}, "task_partitions": PARTITIONS,
        "description": "Fictional records from Sierra; simplified scripted passenger requests. Not a benchmark replication.",
        "selection": "Fixed task IDs grouped by passenger; deterministic feasible flight search with source-ID tie-breaking. No model score used.",
        "excluded_train_ids_sharing_test_passengers": [3, 4, 9, 15, 17, 38, 40, 46, 47, 49],
        "adaptations": ["Narrow single-reservation requests replace the original multi-intent dialogue.",
            "Names, addresses, birth dates, email and card suffixes are absent from model-visible user records.",
            "No seat inventory mutation, new reservation booking, or upstream LLM user simulator.",
            "Payment updates and confirmations are checked by independent workshop code."],
        "cases_sha256": hashlib.sha256((OUT / "cases.json").read_bytes()).hexdigest()}
    (OUT / "provenance.json").write_bytes((json.dumps(manifest, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"cases": len(cases), "bytes": (OUT / "cases.json").stat().st_size,
        "kinds": {p: [c["kind"] for c in cases if c["partition"] == p] for p in PARTITIONS}}, indent=2))


if __name__ == "__main__":
    main()
