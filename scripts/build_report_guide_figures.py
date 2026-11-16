"""Use the notebook/deck mechanism drawings in the six public Reports.

Only local SVG artwork is rendered. Native captures and scientific plots remain
unchanged, with their original aspect ratios and full-size source links.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/teenage-engineering-visualizations"
FIGURES = (
    ("pending", "pending", "dispatch"),
    ("solar", "solar", "model-shapes"),
    ("routing", "routing", "release"),
    ("inspection", "inspection", "patch-distance"),
    ("transit", "transit", "service-time"),
    ("airline", "airline_monitoring", "coverage"),
)


def build():
    records = []
    for report, workshop, guide in FIGURES:
        specification = ROOT / "visual-guides" / workshop / f"{guide}.json"
        source = json.loads(specification.read_text())
        output = ROOT / "dist/report-guide-figures" / report
        subprocess.run([
            sys.executable, str(SKILL / "scripts/render.py"), str(specification),
            "--output", str(output), "--layout", "slide", "--formats", "svg,html,png",
        ], check=True)
        manifest = json.loads((output / "index.json").read_text())
        validation = json.loads((output / "browser-validation.json").read_text())
        if not validation["passed"]:
            raise ValueError(f"{report}: a mechanism drawing has clipped text")
        # A static article needs the operation, not necessarily the last reveal.
        # The Routing final frame shows the repair; its fault frame makes the
        # changed column-to-label relationship visible without inventing scores.
        complete = next(row for row in manifest["states"] if row["id"] == "faulty") if report == "routing" else manifest["states"][-1]
        artwork = next(row for row in source["states"] if row["id"] == complete["id"])["artwork"]
        destination = ROOT / "reports/assets" / report
        for extension in ("svg", "png"):
            shutil.copyfile(output / complete[extension], destination / f"mechanism-{guide}.{extension}")
        records.append({
            "report": report, "guide": guide, "state": complete["id"],
            "width": manifest["width"], "height": manifest["height"],
            "provenance": source["provenance"],
            "specification": str(specification.relative_to(ROOT)),
            "specification_sha256": hashlib.sha256(specification.read_bytes()).hexdigest(),
            "artwork": str((specification.parent / artwork).relative_to(ROOT)),
            "png": f"reports/assets/{report}/mechanism-{guide}.png",
            "svg": f"reports/assets/{report}/mechanism-{guide}.svg",
            "guide_url": f"https://ash0ts.github.io/forge-workshop-kit/guides/{workshop}/{guide}/index.html",
            "source_links": source["source_links"],
            "all_reveals_checked": validation["passed"],
        })
    (ROOT / "reports/figures-guide-layout.json").write_text(json.dumps({
        "renderer": "scripts/build_report_guide_figures.py",
        "layout": "Shared 1200 by 675 mechanism drawings; original photographs and captures retain their ratio.",
        "figures": records,
    }, indent=2) + "\n")


if __name__ == "__main__":
    build()
