"""Render paired Solar qualification results from the saved summary only."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/solar-fixed-recipes-2026-11-14"


def draw():
    summary = json.loads((EVIDENCE / "summary.json").read_text())
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                         "svg.fonttype": "none", "axes.spines.top": False,
                         "axes.spines.right": False})
    for task, before, after, title, caption in (
        ("images", "manual", "zero_residual", "The same image edits do not help every seed",
         "199 overlapping windows on the same two known dates; 3 training seeds.\nMean error falls 5.79%; seed 43 gets 0.21% worse. Lower error is better."),
        ("goes", "persistence", summary["selected_goes_recipe"], "The GOES repair beats persistence on all three seeds",
         "2,694 overlapping windows on the same two known dates; 3 training seeds.\nThe recipe was selected on validation dates. Lower error is better."),
    ):
        figure, axis = plt.subplots(figsize=(10, 4.8))
        figure.patch.set_facecolor("#f8f5ed")
        axis.set_facecolor("#f8f5ed")
        for index, seed in enumerate(summary["seeds"]):
            rows = {r["recipe"]: r for r in summary["rows"] if r["task"] == task and r["seed"] == seed}
            first = rows[after]["persistence_error"] if before == "persistence" else rows[before]["error"]
            second = rows[after]["error"]
            axis.plot([first, second], [index, index], color="#a7a7a7", lw=2, zorder=1)
            axis.scatter(first, index, color="#4382a6" if task == "images" else "#777777", s=85,
                         marker="o", label="Manual model" if task == "images" else "Persistence" if index == 0 else None)
            axis.scatter(second, index, color="#bd7c20" if task == "images" else "#237a6c", s=85,
                         marker="s", label="Combined image edits" if task == "images" else "Worked repair" if index == 0 else None)
            axis.annotate(f"{first:.6f}", (first, index), xytext=(0, 12), textcoords="offset points", ha="center", fontsize=10)
            axis.annotate(f"{second:.6f}", (second, index), xytext=(0, -20), textcoords="offset points", ha="center", fontsize=10)
        handles, labels = axis.get_legend_handles_labels()
        unique = dict(zip(labels, handles, strict=True))
        axis.legend(unique.values(), unique.keys(), loc="upper right", frameon=False, fontsize=10)
        axis.set_yticks(range(3), [f"Seed {seed}" for seed in summary["seeds"]])
        axis.set_ylim(2.65, -1.1)
        axis.set_xlim((.106, .126) if task == "images" else (.157, .201))
        axis.set_xlabel("Disk-masked image MAE · standardized log1p intensity" if task == "images"
                        else "GOES MAE · log10 XRS-B flux")
        axis.grid(axis="x", color="#ddd7ca", lw=.7)
        axis.set_title(title, loc="left", fontsize=15, pad=18)
        figure.text(.1, .04, caption, fontsize=10, color="#444444")
        figure.subplots_adjust(left=.12, right=.97, top=.85, bottom=.24)
        for extension in ("svg", "png"):
            figure.savefig(EVIDENCE / f"{task}-seeds.{extension}", dpi=160)
        # Slides supply their own heading and limitations. Use the full slide width
        # for the plot so numeric labels remain readable from the room.
        figure.set_size_inches(12, 3.7)
        axis.set_title("")
        for text in list(figure.texts):
            text.remove()
        for text in axis.texts:
            text.set_fontsize(14)
        axis.tick_params(labelsize=14)
        axis.xaxis.label.set_fontsize(14)
        axis.legend(unique.values(), unique.keys(), loc="upper center", ncol=2,
                    frameon=False, fontsize=13)
        axis.set_ylim(2.65, -1.05)
        figure.subplots_adjust(left=.1, right=.97, top=.99, bottom=.23)
        for extension in ("svg", "png"):
            figure.savefig(EVIDENCE / f"{task}-seeds-deck.{extension}", dpi=160)
        plt.close(figure)


if __name__ == "__main__":
    draw()
