"""Read the pinned teaching data to refresh one displayed window. No training or API calls."""
from pathlib import Path
import hashlib
import importlib.util
import json
import numpy as np

root = Path(__file__).resolve().parents[1]
repo = root.parents[1]
source = repo / "src/forge_workshop_kit/solar.py"
spec = importlib.util.spec_from_file_location("deck_solar_loader", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
data = repo / "data/solar-v1"
module.verify_data(data)
splits, normalization = module.load_goes(data)
train = splits["train"]
origin = "2014-02-01T01:00"
index = int(np.where(train["ids"] == origin)[0][0])
record = {
    "source": "src/forge_workshop_kit/solar.py:load_goes",
    "dataset_sha256": hashlib.sha256((data / "manifest.json").read_bytes()).hexdigest(),
    "origin": origin,
    "target_time": str(np.datetime64(origin) + np.timedelta64(30, "m")),
    "latest_log10": float(train["persistence"][index, 0]),
    "target_log10": float(train["y"][index, 0]),
    "standardized_latest": float(train["x"][index, 1, -1]),
    "mean_xrsb": normalization["mean"][0][1][0],
    "std_xrsb": normalization["std"][0][1][0],
    "counts": {key: len(value["ids"]) for key, value in splits.items()},
    "raw_flux": float(10 ** train["persistence"][index, 0]),
}
assert np.isclose((record["latest_log10"] - record["mean_xrsb"]) / record["std_xrsb"], record["standardized_latest"])
(root / "data/teaching-window.json").write_text(json.dumps(record, indent=2) + "\n")
print("Saved one observed window; no model calls or training runs.")
