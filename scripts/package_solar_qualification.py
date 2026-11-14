"""Bundle completed Solar qualification outputs, excluding inputs and host paths."""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "solar-fixed-recipes-2026-11-14"
ALLOWLIST = ("candidate.py", "weights.pt", "predictions.npy", "losses.json")


def main():
    evidence = ROOT / "evidence" / NAME
    state = ROOT / ".workshop" / NAME
    output = ROOT / "dist" / (NAME + ".zip")
    output.parent.mkdir(exist_ok=True)
    files = {}
    for path in sorted(evidence.iterdir()):
        if path.is_file():
            files["evidence/" + path.name] = path.read_bytes()
    for split, filename in (("validation", "validation.json"), ("test", "evaluation.json")):
        records = json.loads((evidence / filename).read_text())
        for key, record in records.items():
            if record["status"] != "complete":
                continue
            for name in ALLOWLIST:
                path = state / split / key / name
                content = path.read_bytes()
                if hashlib.sha256(content).hexdigest() != record["files"][name]:
                    raise ValueError("Completed output differs: " + str(path))
                files[f"executions/{split}/{key}/{name}"] = content
    manifest = {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}
    files["checksums.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    files["README.txt"] = (
        b"Solar fixed-recipe qualification: three predeclared training seeds.\n"
        b"Known final dates are a teaching retest, not a new unseen benchmark.\n"
        b"Read evidence/protocol.json and evidence/summary.json first.\n"
        b"Prediction row order is the case_id order in each execution's error records.\n"
        b"Data, scoring, and reproduction instructions:\n"
        b"https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/solar-qualification.md\n"
        b"No Forge credentials, provider keys, raw host request files, or training inputs are included.\n"
    )
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 14, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content)
    print(json.dumps({"file": str(output.relative_to(ROOT)), "bytes": output.stat().st_size,
                      "sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "files": len(files)}))


if __name__ == "__main__":
    main()
