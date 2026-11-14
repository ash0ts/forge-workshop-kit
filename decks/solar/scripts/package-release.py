"""Compatibility entry point for the shared validated Solar release build."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
if __name__ == "__main__":
    subprocess.run([sys.executable, str(ROOT / "scripts/build_decks.py"), "--only", "solar", "--pdf", "--validate"], cwd=ROOT, check=True)
    print("Solar packages are in dist/decks/downloads. Nothing was published.")
