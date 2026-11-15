"""Render the Pending and Solar article diagrams from saved teaching records.

No training, inference, publication, or screenshot editing occurs here.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/workshop-report-matplotlib")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
BG, INK, MUTED = "#f7f4e9", "#153d3e", "#546862"
TEAL, BLUE, ORANGE, GRAY = "#237a6c", "#4382a6", "#c17b40", "#7c8985"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "svg.fonttype": "none",
    "svg.hashsalt": "workshop-reports-pending-solar-v1",
})


def page(title, subtitle, height=6.8):
    fig, ax = plt.subplots(figsize=(12, height), facecolor=BG)
    ax.set(xlim=(0, 12), ylim=(height, 0))
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    label(ax, .45, .38, title, 22, weight="bold")
    label(ax, .45, .86, subtitle, 12, color=MUTED)
    return fig, ax


def label(ax, x, y, text, size=14, color=INK, weight="normal", **kwargs):
    ax.text(x, y, text, fontsize=size, color=color, weight=weight,
            va="top", linespacing=1.45, **kwargs)


def box(ax, x, y, w, h, title, body="", color=TEAL, size=14):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=.06",
                             linewidth=1.5, edgecolor=color, facecolor="#fffdf7"))
    label(ax, x+.18, y+.15, title, size, color=color, weight="bold")
    if body:
        label(ax, x+.18, y+.6, body, 12)


def arrow(ax, start, end, color=INK, dashed=False):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14,
                              linewidth=1.6, color=color, linestyle="--" if dashed else "-"))


def save(fig, workshop, name):
    folder = ROOT / "reports" / "assets" / workshop
    folder.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "png"):
        output = folder / f"{name}.{extension}"
        metadata = {"Date": None} if extension == "svg" else None
        fig.savefig(output, dpi=170, facecolor=BG, metadata=metadata)
        if extension == "svg":
            output.write_text("\n".join(line.rstrip() for line in output.read_text().splitlines()) + "\n")
    plt.close(fig)


def pending_case():
    fig, ax = page("One invoice, two captured payments", "Fictional development ticket · Acme / inv-1 · Amounts in cents", 5.9)
    box(ax, .45, 1.5, 3.5, 3.35, "Before the employee acts", color=GRAY)
    label(ax, .7, 2.25, "pay-1       4,900   captured\npay-2       4,900   captured\n\nrefunds     []", 12, family="DejaVu Sans Mono")
    box(ax, 4.55, 2, 2.9, 2.25, "Requested change", "Keep pay-1.\nRefund pay-2 once.\nLeave other records alone.", color=BLUE)
    arrow(ax, (3.98, 3.05), (4.48, 3.05))
    arrow(ax, (7.5, 3.05), (8, 3.05))
    box(ax, 8.05, 1.5, 3.5, 3.35, "Recorded checked state", color=TEAL)
    label(ax, 8.3, 2.25, "pay-1       4,900   captured\npay-2       4,900   captured\n\nrefunds     pay-2: 4,900", 12, family="DejaVu Sans Mono")
    label(ax, .45, 5.15, "The simulator keeps captured payments in the ledger and adds a separate refund record.", 12)
    save(fig, "pending", "billing-state")


def pending_handoff():
    fig, ax = page("The Python return value has to reach the next request", "Worked learner code · This diagram explains dispatch, not a recorded model choice", 7.1)
    box(ax, .45, 1.5, 4.5, 1.5, "1  Chosen action", 'lookup_invoice\naccount_id="acme", invoice_id="inv-1"', color=BLUE)
    box(ax, 6.1, 1.5, 5.45, 1.5, "2  my_dispatch calls your function", "my_invoice_tool(world, **arguments)", color=BLUE)
    arrow(ax, (5, 2.25), (6.04, 2.25))
    box(ax, 6.1, 3.65, 5.45, 1.5, "3  Returned observation", "payments: [pay-1, pay-2]\nrefunds: []", color=TEAL)
    arrow(ax, (8.85, 3.06), (8.85, 3.59))
    box(ax, .45, 3.65, 4.5, 1.5, "4  my_observation appends", "Previous messages + chosen action\n+ serialized tool result", color=TEAL)
    arrow(ax, (6.04, 4.4), (5, 4.4))
    arrow(ax, (2.7, 5.22), (2.7, 5.8))
    label(ax, .45, 6, "Next model request includes the payment records.", 18, weight="bold")
    save(fig, "pending", "tool-handoff")


def pending_retry():
    evidence = json.loads((ROOT / "evidence/pending-retry-repair.json").read_text())
    assert evidence["before"]["membership_count"] == 2
    assert evidence["after"]["membership_count"] == 1
    fig, ax = page("A timeout leaves two different states to inspect", "Recorded local exercise · No model calls · Each recovery starts from the same committed write", 7.5)
    box(ax, .45, 1.45, 5.35, 1.25, "Office state", "join-alex committed. Alex is already a member.")
    box(ax, 6.2, 1.45, 5.35, 1.25, "Caller observation", 'error="timeout"; no acknowledgement', color=ORANGE)
    label(ax, .45, 3.15, "Starter recovery", 17, weight="bold", color=ORANGE)
    label(ax, 6.2, 3.15, "Repaired recovery", 17, weight="bold", color=TEAL)
    box(ax, .45, 3.7, 5.35, 1.4, "Send join-alex-retry", "New operation ID → another mutation", color=ORANGE)
    box(ax, 6.2, 3.7, 5.35, 1.4, "Send join-alex", "Same operation ID → saved receipt", color=TEAL)
    arrow(ax, (3.1, 5.18), (3.1, 5.7), ORANGE)
    arrow(ax, (8.9, 5.18), (8.9, 5.7), TEAL)
    label(ax, .65, 5.95, "2 memberships", 24, color=ORANGE, weight="bold")
    label(ax, .65, 6.55, "No verification read", 13)
    label(ax, 6.4, 5.95, "1 membership", 24, color=TEAL, weight="bold")
    label(ax, 6.4, 6.55, "onboarding_status confirms the account", 13)
    save(fig, "pending", "timeout-repair")


def pending_branches():
    records = json.loads((ROOT / "reports/assets/pending/recorded-branches.json").read_text())["records"]
    proposal = next(r for r in records if r["stage"] == "pending/round-1/propose")
    decision = next(r for r in records if r["stage"] == "pending/round-1/compose")["decision"]
    assert proposal["candidates"][0]["decision"] == "KEEP"
    assert proposal["candidates"][1]["harness"]["verify_before_finish"] is True
    assert decision["decision"] == "KEEP"
    fig, ax = page("The first editor round retained the parent", "Recorded billing probes · Solid arrows pass a harness; dashed arrows pass reviewed execution evidence", 7.5)
    box(ax, .45, 1.5, 3.25, 1.5, "Manual parent", "Verification skill installed\nFinish gate: off", color=GRAY)
    box(ax, 4.4, 1.5, 3.25, 1.5, "A · Retain this version", "Same instructions\nFinish gate: off", color=BLUE)
    box(ax, 8.3, 1.5, 3.25, 1.5, "B · Require check_work", "One workflow setting changes\nFinish gate: on", color=ORANGE)
    arrow(ax, (3.76, 2.25), (4.34, 2.25), GRAY)
    ax.plot([2.05, 2.05, 9.9], [1.45, 1.22, 1.22], color=GRAY, lw=1.3)
    arrow(ax, (9.9, 1.22), (9.9, 1.47), GRAY)
    box(ax, 4.4, 3.65, 3.25, 1.8, "Probe A completed", "Refund → account read\n→ finish accepted", color=BLUE)
    box(ax, 8.3, 3.65, 3.25, 1.8, "Probe B completed", "Refund → account read\n→ finish rejected\n→ check_work → accepted", color=ORANGE)
    arrow(ax, (6, 3.08), (6, 3.58), BLUE)
    arrow(ax, (9.9, 3.08), (9.9, 3.58), ORANGE)
    box(ax, .45, 3.65, 3.25, 1.8, "Composition decision", "Retain parent.\nBoth refunded once;\nthe gate added a rejection.", color=MUTED)
    arrow(ax, (4.34, 4.2), (3.76, 4.2), BLUE, True)
    ax.plot([9.9, 9.9, 2.05], [5.5, 5.8, 5.8], color=ORANGE, lw=1.5, linestyle="--")
    arrow(ax, (2.05, 5.8), (2.05, 5.48), ORANGE, True)
    label(ax, .45, 6.25, "The retained harness was executed again before the next round.", 17, weight="bold")
    label(ax, .45, 6.8, "This decision covers one billing case. It does not prove that completion gates are generally unnecessary.", 12)
    save(fig, "pending", "recorded-first-round")


def solar_goes():
    data = json.loads((ROOT / "decks/solar/public/recorded-study.json").read_text())
    stages = {s["id"]: s for s in data["stages"]}
    selected = stages["ff57eba2f9e3704d9bee074e4b4c9bea"]
    result = next(s["result"] for s in data["stages"] if s["name"] == "goes/final")
    fig, ax = page("Training loss fell. The forecast still lost to persistence.", "Recorded GOES search · 60 update steps · The training objective and forecast metric have different units", 6.7)
    loss_ax = fig.add_axes([.08, .23, .42, .52], facecolor=BG)
    losses = selected["result"]["losses"]
    loss_ax.plot(range(1, len(losses)+1), losses, color=BLUE, lw=2.5)
    loss_ax.set(xlabel="Training update", ylabel="Training loss · squared log-flux error")
    loss_ax.set_title("Selected model's recorded learning curve", loc="left", fontsize=12, color=INK)
    loss_ax.spines[["top", "right"]].set_visible(False)
    loss_ax.tick_params(colors=INK)
    label(ax, 6.7, 1.65, "Final forecast error", 18, weight="bold")
    label(ax, 6.7, 2.2, "Mean absolute log10 XRS-B error\n2,694 windows · lower is better", 12)
    label(ax, 6.7, 3.25, "Persistence", 15)
    label(ax, 10.9, 3.2, f'{result["metrics"]["persistence_error"]:.6f}', 20, color=TEAL, ha="right")
    label(ax, 6.7, 4.05, "Selected neural model", 15)
    label(ax, 10.9, 4.65, f'{result["metrics"]["error"]:.6f}', 26, color=ORANGE, ha="right", weight="bold")
    label(ax, .45, 6.05, "Winning among six short training runs did not establish a competitive forecast.", 14)
    save(fig, "solar", "goes-training-and-forecast")


def solar_branches():
    data = json.loads((ROOT / "decks/solar/public/recorded-study.json").read_text())
    stages = {s["name"]: s for s in data["stages"]}
    error = lambda name: stages[name]["result"]["metrics"]["error"]
    fig, ax = page("The second round tests two changes to the training procedure", "Recorded validation experiment · 142 images · Seed 17 · 40 updates · Same parent source and data", 8.8)
    box(ax, .45, 1.45, 11.1, 1.1, "Parent from round one: residual model + absolute-error training loss", color=GRAY)
    label(ax, .7, 2.08, f'Validation error {error("images/round-1/composition-test"):.6f}', 14)
    box(ax, .45, 3.15, 5.35, 2, "A · Start the correction at zero", "Change: zero-initialize the final layer\nHypothesis: stop spending early updates\nunlearning a random correction.", color=BLUE)
    box(ax, 6.2, 3.15, 5.35, 2, "B · Change the sampling order", "Change: sample epoch permutations\nHypothesis: more uniform example coverage\nwill reduce validation error.", color=ORANGE)
    arrow(ax, (3.1, 2.63), (3.1, 3.08), GRAY)
    arrow(ax, (8.9, 2.63), (8.9, 3.08), GRAY)
    label(ax, .65, 5.5, f'Tested: {error("images/round-2/probe-0"):.6f}', 23, color=BLUE, weight="bold")
    label(ax, 6.4, 5.5, f'Tested: {error("images/round-2/probe-1"):.6f}', 23, color=ORANGE, weight="bold")
    arrow(ax, (3.1, 6.1), (4.2, 6.8), BLUE, True)
    arrow(ax, (8.9, 6.1), (7.8, 6.8), ORANGE, True)
    box(ax, 2.15, 6.85, 7.7, 1.2, "Select A, then test the returned source again", "Composition test: 0.110916. B rejected. A+B was not tested.", color=MUTED)
    label(ax, .45, 8.35, "Error: mean disk-masked absolute error in standardized log1p intensity. Lower is better.", 11)
    save(fig, "solar", "recorded-code-branches")


if __name__ == "__main__":
    for build in (pending_case, pending_handoff, pending_retry, pending_branches, solar_goes, solar_branches):
        build()
