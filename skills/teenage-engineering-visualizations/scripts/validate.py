#!/usr/bin/env python3
"""Validate generated structure and estimates; --browser verifies actual glyph bounds."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--browser", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((args.directory / "index.json").read_text(encoding="utf-8"))
    issues = []
    for state in manifest["states"]:
        svg = args.directory / state["svg"]
        tree = ET.fromstring(svg.read_text(encoding="utf-8"))
        if not tree.find("{http://www.w3.org/2000/svg}title").text:
            issues.append(f"Missing accessible title: {svg.name}")
        for image in tree.iter("{http://www.w3.org/2000/svg}image"):
            if not image.attrib.get("href", "").startswith("data:"):
                issues.append(f"Unbundled media: {svg.name}")
    for frame in json.loads((args.directory / "text-bounds.json").read_text(encoding="utf-8")):
        for text in frame["text"]:
            x,y,w,h = text["box"]
            if text["estimated_width"] > w + 1 or x < 0 or y < 0 or x+w > manifest["width"]+1 or y+h > manifest["height"]+1:
                issues.append(f'{frame["file"]}: {text["text"]!r} exceeds bounds')
    if args.browser:
        subprocess.run(["node",str(ROOT / "scripts/export.mjs"),str(args.directory.resolve()),""],check=True)
    receipt_path = args.directory / "browser-validation.json"
    browser = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.exists() else None
    if browser and not browser["passed"]:
        issues.append("Browser measured overflow; inspect browser-validation.json")
    result = {"id":manifest["id"],"states":len(manifest["states"]),"structure":"passed" if not issues else "failed","actual_text_bounds":"passed" if browser and browser["passed"] else "not checked","issues":issues}
    print(json.dumps(result,indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
