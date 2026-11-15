"""Render Report figures from saved public examples; no fitting or service calls."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "workshop-report-matplotlib")
)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
# Use the deck's existing IBM Plex font when its build is present.
fonts = list((ROOT / "decks/solar/dist/assets").glob("ibm-plex-sans-latin-*-normal-*.woff"))
BOLD_FAMILY = "DejaVu Sans"
if fonts:
    from fontTools.ttLib import TTFont

    for source in fonts:
        font = TTFont(source)
        font.flavor = None
        target = Path(tempfile.gettempdir()) / (source.stem + ".ttf")
        font.save(target)
        font_manager.fontManager.addfont(str(target))
    plt.rcParams["font.family"] = ["IBM Plex Sans", "DejaVu Sans"]
    BOLD_FAMILY = "IBM Plex Sans SemiBold"
plt.rcParams.update(
    {
        "font.size": 18,
        "svg.fonttype": "none",
        "svg.hashsalt": "forge-workshop-reports-routing-inspection-v1",
        "text.color": "#183a3b",
        "axes.labelcolor": "#183a3b",
    }
)
BG = "#f7f3e9"
INK = "#183a3b"
MUTED = "#526766"
TEAL = "#207b72"
BLUE = "#3971ae"
ORANGE = "#bc6638"
BORDER = "#c9d4cd"
PALE = "#e5eee7"
FIGURES = []


def read(path):
    return json.loads((ROOT / path).read_text())


def canvas(title, subtitle, height=8):
    fig = plt.figure(figsize=(14.4, height), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 100), ylim=(0, 100))
    ax.axis("off")
    ax.text(5, 94, title, fontsize=26, fontfamily=BOLD_FAMILY, fontweight=600, va="top")
    ax.text(5, 87, subtitle, fontsize=17, color=MUTED, va="top")
    return fig, ax


def box(ax, x, y, w, h, title, body="", color=TEAL, fill="white", title_size=20):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=.6,rounding_size=1", fc=fill, ec=BORDER, lw=1.2
        )
    )
    ax.plot([x + 1, x + w - 1], [y + h - 1, y + h - 1], color=color, lw=4)
    ax.text(
        x + 2,
        y + h - 5,
        title,
        fontsize=title_size,
        fontfamily=BOLD_FAMILY,
        fontweight=600,
        va="top",
        color=color,
    )
    if body:
        ax.text(x + 2, y + h - 11.5, body, fontsize=17, va="top", linespacing=1.4)


def arrow(ax, a, b, color=INK, style="-"):
    ax.add_patch(
        FancyArrowPatch(
            a, b, arrowstyle="-|>", mutation_scale=15, lw=1.7, color=color, linestyle=style
        )
    )


def finish(fig, slug, name, question, alt, sources, boundary):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    width, height = fig.canvas.get_width_height()
    for text in (item for axis in fig.axes for item in axis.texts):
        bounds = text.get_window_extent(renderer)
        if bounds.x0 < 0 or bounds.y0 < 0 or bounds.x1 > width or bounds.y1 > height:
            raise ValueError(f"Text outside {slug}/{name}: {text.get_text()}")
    dest = ROOT / "reports/assets" / slug / name
    fig.savefig(dest.with_suffix(".png"), dpi=150, facecolor=BG)
    svg = dest.with_suffix(".svg")
    fig.savefig(svg, facecolor=BG, metadata={"Date": None})
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(fig)
    FIGURES.append(
        {
            "id": slug + "/" + name,
            "question": question,
            "alt": alt,
            "boundary": boundary,
            "png": str(dest.with_suffix(".png").relative_to(ROOT)),
            "svg": str(dest.with_suffix(".svg").relative_to(ROOT)),
            "sources": [
                {"path": p, "sha256": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()}
                for p in sources
            ],
        }
    )


# A real validation request: the representation changes its prediction, but both defer.
routing = {
    k: read(f"evidence/routing-qualification-20261114/{k}-17.json") for k in ("tfidf", "embedding")
}
case = {
    k: next(r for r in d["validation_predictions"] if r["case_id"] == "official-train/00035")
    for k, d in routing.items()
}
fig, ax = canvas(
    "One request, two predictions",
    "Recorded validation example · official-train/00035 · no new model execution",
)
ax.text(5, 73, "“Can I get an update on my replacement card?”", fontsize=26, fontfamily=BOLD_FAMILY)
ax.text(5, 66, "Dataset intent: card_arrival", fontsize=18, color=MUTED)
for i, (key, title, color) in enumerate(
    [("tfidf", "Word features", BLUE), ("embedding", "Sentence features", ORANGE)]
):
    r = case[key]
    x = 5 + i * 47
    box(ax, x, 21, 43, 36, title, color=color)
    ax.text(x + 2, 42, r["prediction"], fontsize=21, fontfamily=BOLD_FAMILY)
    ax.text(x + 2, 34, f"Top probability: {r['confidence']:.3f}", fontsize=19)
    ax.text(x + 2, 26, "Send to review at cutoff 0.5", fontsize=18, color=color)
ax.text(
    5,
    10,
    "The second prediction matches the label. Neither version routes this request automatically.",
    fontsize=19,
)
finish(
    fig,
    "routing",
    "request-comparison",
    "What changes for the same request?",
    "Word features predict compromised_card at .053; sentence features predict card_arrival at .382. Both probabilities are below .5, so both send the request to review.",
    [f"evidence/routing-qualification-20261114/{k}-17.json" for k in routing],
    "One validation example. Probabilities are uncalibrated; changed prediction does not mean automatic routing.",
)

fig, ax = canvas(
    "What changes when we change the representation?",
    "The training messages and classifier settings stay the same.",
    8.7,
)
box(ax, 5, 62, 90, 16, "Request text", "Can I get an update on my replacement card?", title_size=18)
arrow(ax, (28, 61), (28, 55))
arrow(ax, (72, 61), (72, 55))
box(
    ax,
    5,
    31,
    43,
    22,
    "Word TF–IDF",
    "Tokens and adjacent pairs\nupdate · replacement · replacement card",
    color=BLUE,
)
box(
    ax,
    52,
    31,
    43,
    22,
    "Frozen sentence encoder",
    "384 numeric values per request\nEncoder weights stay fixed",
    color=ORANGE,
)
arrow(ax, (28, 30), (28, 23))
arrow(ax, (72, 30), (72, 23))
box(
    ax,
    5,
    6,
    90,
    15,
    "Logistic classifier: fit first, predict later",
    "fit(features, labels) learns coefficients; predict_proba(features) returns 77 columns.",
    title_size=19,
)
finish(
    fig,
    "routing",
    "representations",
    "What does the classifier receive?",
    "The same request becomes sparse TF–IDF word features or a frozen 384-value sentence vector. Each representation trains a logistic classifier with the same settings and 77 output columns.",
    ["src/forge_workshop_kit/routing.py", "docs/routing-workshop.md"],
    "Tokens are an illustrative subset, not a feature-importance explanation. No embedding coordinates or weights are fabricated.",
)

fig, ax = canvas(
    "More requests routed, with a similar error rate among them",
    "Recorded official test · 3,080 requests · cutoff 0.5",
    8.5,
)
metrics = [
    ("Macro-F1", "Every request; equal weight per intent", "macro_f1"),
    ("Routing coverage", "Fraction sent automatically", "coverage"),
    ("Accuracy when routed", "Only requests above the cutoff", "selective_accuracy"),
]
for i, (title, desc, key) in enumerate(metrics):
    y = 73 - i * 22
    ax.text(5, y, title, fontsize=22, fontfamily=BOLD_FAMILY)
    ax.text(5, y - 6, desc, fontsize=16, color=MUTED)
    for j, (kind, color, label) in enumerate(
        [("tfidf", BLUE, "Words"), ("embedding", ORANGE, "Sentences")]
    ):
        value = routing[kind]["final"][key]
        yy = y - 10 - j * 6
        ax.text(6, yy, label, fontsize=16, va="center", color=color)
        ax.plot([23, 81], [yy, yy], color=BORDER, lw=5, solid_capstyle="round")
        ax.plot([23, 23 + 58 * value], [yy, yy], color=color, lw=5, solid_capstyle="round")
        ax.text(
            84,
            yy,
            f"{value * 100:.2f}%",
            fontsize=20,
            fontfamily=BOLD_FAMILY,
            fontweight=600,
            va="center",
            color=color,
        )
ax.text(
    5,
    5,
    "Same benchmark split. Repeated deterministic fits reproduced these predictions; they are not independent trials.",
    fontsize=15,
    color=MUTED,
)
finish(
    fig,
    "routing",
    "classifier-results",
    "Which measured quantities improved?",
    "Macro-F1 rises from 87.94 to 92.02 percent, coverage from 75.84 to 91.10 percent, and accuracy among automatically routed requests from 96.06 to 96.15 percent.",
    ["evidence/routing-qualification-20261114/summary.json"],
    "Do not interpret cached classifier time as full service latency or deterministic seed repeats as uncertainty estimates.",
)

fig, ax = canvas(
    "The loader changes the label without changing the probability",
    "Controlled drill · three-label free-check example · p[0], p[1], p[2] are symbols",
    8.7,
)
xs = [33, 55, 77]
labels = ["card_not_working", "card_arrival", "cash_withdrawal"]
for x, p in zip(xs, ["p[0]", "p[1]", "p[2]"]):
    ax.text(x + 7, 73, p, fontsize=30, ha="center", fontfamily=BOLD_FAMILY)
ax.text(5, 72, "Model columns", fontsize=19, fontfamily=BOLD_FAMILY)
for y, title, order, color in [
    (55, "Healthy", labels, BLUE),
    (35, "Faulty", labels[1:] + labels[:1], ORANGE),
    (15, "Repaired", labels, TEAL),
]:
    ax.text(5, y + 3, title, fontsize=21, fontfamily=BOLD_FAMILY, fontweight=600, color=color)
    for x, label in zip(xs, order):
        ax.add_patch(Rectangle((x - 3, y - 3), 21, 13, fc="white", ec=BORDER, lw=1))
        ax.text(
            x + 7.5,
            y + 3,
            label.replace("_", "\n", 1),
            ha="center",
            va="center",
            fontsize=15,
            color=color,
        )
ax.text(
    5, 4, "Checking the set of names passes. Checking their order catches the defect.", fontsize=18
)
finish(
    fig,
    "routing",
    "label-mapping",
    "How can an unchanged probability route to the wrong queue?",
    "Three symbolic probability columns retain their positions while the faulty loader rotates their label names. Repair restores the original order. A set-membership check cannot detect this permutation.",
    ["src/forge_workshop_kit/routing_release.py"],
    "The labels come from the free-check fixture. This is an explanatory drill, not a captured production prediction.",
)

# Inspection: the feature computation and the measured tradeoffs.
fig, ax = canvas(
    "Give the classifier a whole-board view and local comparisons",
    "Fixed encoder weights · participant code assembles the features",
    9,
)
box(
    ax,
    5,
    63,
    90,
    16,
    "Photograph encoded by frozen ResNet-18",
    "Resize to 224 × 224; apply the saved channel normalization.",
    title_size=20,
)
arrow(ax, (27, 62), (27, 55))
arrow(ax, (73, 62), (73, 55))
box(
    ax,
    5,
    30,
    43,
    23,
    "Whole-image branch",
    "512 values summarizing the image\nThe baseline uses only this branch.",
    color=BLUE,
)
box(
    ax,
    52,
    30,
    43,
    23,
    "Patch branch",
    "14 × 14 positions, each with 64 values\nCompare each position with normal boards.",
    color=ORANGE,
)
arrow(ax, (27, 29), (35, 22))
arrow(ax, (73, 29), (65, 22))
box(
    ax,
    5,
    5,
    90,
    16,
    "512 image values + 196 patch distances = 708 features",
    "Standardize with training values, then fit the logistic classifier.",
    color=TEAL,
    title_size=20,
)
finish(
    fig,
    "inspection",
    "feature-path",
    "What extra information reaches the patch classifier?",
    "A frozen ResNet-18 produces 512 whole-image values and a 14 by 14 by 64 patch array. One distance per patch adds 196 values, yielding 708 features for the logistic classifier.",
    [
        "src/forge_workshop_kit/inspection_encoder.py",
        "src/forge_workshop_kit/inspection.py",
        "docs/inspection-workshop.md",
    ],
    "Supplied defect masks do not enter this path. The 64-channel projection is fixed, not learned by the classifier.",
)

fig, ax = canvas(
    "Compare the same location across normal boards",
    "Shape diagram · the highlighted position is illustrative; no distances are fabricated.",
    9,
)


def patch_grid(x, y, size, color):
    unit = size / 14
    for row in range(14):
        for column in range(14):
            selected = (row, column) == (8, 10)
            ax.add_patch(
                Rectangle(
                    (x + column * unit, y + (13 - row) * unit),
                    unit,
                    unit,
                    fc=color if selected else "white",
                    ec=BORDER,
                    lw=0.6,
                )
            )
    return (x + 10.5 * unit, y + 5.5 * unit)


q = patch_grid(6, 43, 28, BLUE)
ax.text(6, 77, "Query board", fontsize=21, fontfamily=BOLD_FAMILY, fontweight=600, color=BLUE)
ax.text(6, 37, "14 × 14 positions", fontsize=17)
ax.text(6, 32, "64 values at each position", fontsize=16, color=MUTED)
for x in [43, 62, 81]:
    point = patch_grid(x, 52, 14, ORANGE)
    arrow(ax, (point[0], 50), (point[0], 44), color=ORANGE)
ax.text(
    43,
    77,
    "Normal fitting boards",
    fontsize=21,
    fontfamily=BOLD_FAMILY,
    fontweight=600,
    color=ORANGE,
)
ax.text(43, 38, "Keep vectors from the same position.", fontsize=18)
ax.text(43, 32, "Scale channels using this reference bank.", fontsize=16, color=MUTED)
arrow(ax, (20, 29), (38, 23))
arrow(ax, (68, 29), (62, 23))
box(
    ax,
    5,
    7,
    90,
    16,
    "Choose the closest normal patch",
    "Retain its mean squared distance. Repeat at every position, then apply log1p.",
    title_size=21,
)
finish(
    fig,
    "inspection",
    "patch-distance",
    "What does one bright cell in the distance map measure?",
    "Each 64-value query patch is scaled using reference-bank variation, compared with normal patches at the same position, and assigned the smallest mean squared distance. Repeat at 196 positions.",
    ["src/forge_workshop_kit/inspection.py"],
    "The diagram does not invent patch distances or imply localization is causal. Self matches are excluded.",
)

predictions = read("evidence/inspection-teaching-retest-v2/predictions.json")
fig, ax = canvas(
    "A score only becomes a decision when compared with its cutoff",
    "Recorded teaching retest · both photographs have a defective dataset label",
    8.5,
)
ax.axvline(65, ymin=0.16, ymax=0.77, color=INK, lw=1.2, ls="--")
ax.text(65, 78, "score = cutoff", ha="center", fontsize=17)
ax.text(50, 72, "Pass / miss", fontsize=17, color=MUTED, ha="center")
ax.text(81, 72, "Flag defect", fontsize=17, color=MUTED, ha="center")
for i, (case_id, version) in enumerate(
    [
        ("pcb1-anomaly-048", "whole"),
        ("pcb1-anomaly-048", "nearest-patch"),
        ("pcb1-anomaly-015", "whole"),
        ("pcb1-anomaly-015", "nearest-patch"),
    ]
):
    row = next(r for r in predictions if r["case_id"] == case_id and r["version"] == version)
    y = 62 - i * 13
    delta = row["score"] - row["threshold"]
    x = 65 + delta * 29
    color = BLUE if version == "whole" else ORANGE
    name = "Whole-image" if version == "whole" else "With patches"
    ax.text(5, y + 2, f"{case_id.rsplit('-', 1)[-1]} · {name}", fontsize=18, fontfamily=BOLD_FAMILY)
    ax.text(
        5,
        y - 3,
        f"{row['score']:.3f} versus cutoff {row['threshold']:.3f}",
        fontsize=16,
        color=MUTED,
    )
    ax.plot([39, 91], [y, y], color=BORDER, lw=1)
    ax.scatter(x, y, s=180, color=color, zorder=3)
    ax.text(x, y + 3, "FLAG" if delta >= 0 else "MISS", fontsize=15, ha="center", color=color)
ax.text(
    5,
    8,
    "Positions show score − cutoff. The two detectors have different raw-score scales.",
    fontsize=17,
    color=MUTED,
)
finish(
    fig,
    "inspection",
    "case-decisions",
    "Why is one negative score a miss and another a detection?",
    "For board 048 the whole score is .507 below its cutoff and patch score .228 above its cutoff. For board 015 the whole score is .620 above and patch score .324 below. One miss is recovered and another introduced.",
    ["evidence/inspection-teaching-retest-v2/predictions.json"],
    "Decision values are not probabilities. Relative positions compare decisions, not calibrated certainty across models.",
)

res = read("evidence/inspection-teaching-retest-v2/results.json")
fig, ax = canvas(
    "The patch change helps in aggregate and still creates a new miss",
    "Teaching retest · 442 previously inspected test boards · 40 defective, 402 normal",
    8.7,
)
for i, (key, label, unit, maxval) in enumerate(
    [
        ("average_precision", "Average precision", "Higher is better", 1),
        ("misses", "Missed defects", "Out of 40 defects; lower is better", 40),
        ("false_alarms", "False alarms", "Out of 402 normal boards; lower is better", 402),
    ]
):
    y = 73 - i * 22
    ax.text(5, y, label, fontsize=22, fontfamily=BOLD_FAMILY)
    ax.text(5, y - 6, unit, fontsize=16, color=MUTED)
    for j, (method, color, name) in enumerate(
        [("whole", BLUE, "Whole"), ("nearest-patch", ORANGE, "Patches")]
    ):
        v = res["test"][method][key]
        yy = y - 10 - j * 6
        # Exact values are primary; count bars use a shared within-metric scale for legibility.
        span = 1 if key == "average_precision" else (8 if key == "misses" else 30)
        ax.text(6, yy, name, fontsize=16, va="center", color=color)
        if key == "average_precision":
            ax.plot([23, 81], [yy, yy], color=BORDER, lw=5, solid_capstyle="round")
        ax.plot([23, 23 + 58 * v / span], [yy, yy], color=color, lw=5, solid_capstyle="round")
        ax.text(
            84,
            yy,
            f"{v:.4f}" if key == "average_precision" else str(v),
            fontsize=21,
            fontfamily=BOLD_FAMILY,
            fontweight=600,
            va="center",
            color=color,
        )
ax.text(
    5,
    5,
    "Earlier average-patch recipe: AP fell from 0.8618 to 0.8554. The nearest-patch retest is shown above.",
    fontsize=15,
    color=MUTED,
)
finish(
    fig,
    "inspection",
    "detector-results",
    "Does the recovered board reflect an aggregate gain?",
    "On 442 test boards, average precision rises from .8729 to .8857, missed defects fall from 4 to 3, and false alarms fall from 23 to 18. The first average-patch recipe reduced average precision.",
    [
        "evidence/inspection-teaching-retest-v2/results.json",
        "evidence/inspection-qualification-v1/results.json",
    ],
    "The test images had already been inspected. This is a teaching retest, not independent confirmation or production qualification.",
)

(ROOT / "reports/figures-routing-inspection.json").write_text(
    json.dumps(
        {
            "schema_version": 1,
            "renderer": str(Path(__file__).relative_to(ROOT)),
            "figures": FIGURES,
        },
        indent=2,
    )
    + "\n"
)
print(json.dumps({"figures": len(FIGURES), "inference": 0, "training": 0}, indent=2))
