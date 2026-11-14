"""Read-only teaching views of Solar inputs, authored functions, and saved predictions.

These helpers do not train, publish, or call a provider. The notebook owns controls;
the figures calculate only quantities participants can inspect beside their code.
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from . import solar


def window_values(split, normalization, index=0, *, standardized=False):
    index = int(index)
    inputs = np.asarray(split["x"][index])
    mean = np.asarray(normalization["mean"]).reshape(2, 1)
    std = np.asarray(normalization["std"]).reshape(2, 1)
    log_flux = inputs * std + mean
    return {
        "origin": str(split["ids"][index]),
        "inputs": inputs if standardized else log_flux,
        "log_flux": log_flux,
        "target": float(split["y"][index, 0]),
        "persistence": float(split["persistence"][index, 0]),
        "mean": mean[:, 0], "std": std[:, 0], "standardized": standardized,
    }


def window_figure(values):
    figure, axes = plt.subplots(1, 2, figsize=(12, 3.8), layout="constrained",
                               gridspec_kw={"width_ratios": [3, 1]})
    for channel, color in enumerate(("#4382a6", "#237a6c")):
        axes[0].plot(np.arange(-59, 1), values["inputs"][channel], color=color,
                     label=("XRSA", "XRSB")[channel])
    axes[0].axvline(0, color="#777", linestyle=":")
    axes[0].set(xlabel="Minutes relative to forecast origin", xlim=(-59, 1),
                ylabel="Standardized input" if values["standardized"] else "log10 flux (W/m²)",
                title="Model input: 2 channels × 60 samples")
    axes[0].legend()
    axes[1].scatter([0, 30], [values["persistence"], values["target"]],
                    color=["#237a6c", "#bd7c20"], s=65)
    axes[1].set(xticks=[0, 30], xticklabels=["Latest\nreading", "Future\ntarget"],
                xlim=(-8, 38), ylabel="log10 XRS-B flux (W/m²)",
                title="Baseline and target")
    figure.suptitle(values["origin"] + " UTC · target units stay unchanged")
    return figure


def window_rows(values):
    return [{"Channel": name, "Latest log10 flux": float(values["log_flux"][i, -1]),
             "Training mean": float(values["mean"][i]),
             "Training std": float(values["std"][i]),
             "Latest standardized input": float((values["log_flux"][i, -1] - values["mean"][i]) / values["std"][i])}
            for i, name in enumerate(("XRSA", "XRSB"))]


def forward_shapes(source, architecture, *, width=4):
    """Execute one forward pass through learner source, with no optimizer or fit call."""
    import torch
    from . import solar_teaching as teaching
    from .research import validate_source
    validate_source(source)
    shape = (2, 60) if architecture in ("mlp", "cnn") else (2, 8, 8)
    rows = []
    hooks = []
    # A shape demonstration must not alter the random state of later training.
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(17)
        model = teaching.functions(source)["build_model"](shape, {"architecture": architecture, "width": width})
        def capture(name):
            def hook(module, inputs, output):
                rows.append({"Layer": name, "Operation": type(module).__name__,
                             "Input shape": list(inputs[0].shape), "Output shape": list(output.shape)})
            return hook
        try:
            for name, module in model.named_modules():
                if name and not list(module.children()):
                    hooks.append(module.register_forward_hook(capture(name)))
            model.eval()
            with torch.no_grad():
                prediction = model(torch.zeros((2, *shape)))
            rows.append({"Layer": "returned forecast", "Operation": "forward result",
                         "Input shape": [2, *shape], "Output shape": list(prediction.shape)})
        finally:
            for hook in hooks:
                hook.remove()
    return rows


def scorer_fixture(error=1.0, *, inside=True):
    """Public arithmetic fixture with unequal mask sizes; not solar observations."""
    target = np.zeros((2, 1, 3, 3), dtype=np.float32)
    mask = np.zeros_like(target, dtype=bool)
    mask[0, 0, 1, 1] = True
    mask[1, 0, 1:, 1:] = True
    prediction = target.copy()
    if inside:
        prediction[0, 0, 1, 1] = error
        prediction[1, 0, 1:, 1:] = 2 * error
    else:
        prediction[:, 0, 0, 0] = error
    included = np.abs(prediction - target) * mask
    totals = included.sum(axis=(1, 2, 3))
    counts = mask.sum(axis=(1, 2, 3))
    errors = totals / counts
    rows = [{"Image": str(i + 1), "Included absolute error": float(totals[i]),
             "Included pixels": int(counts[i]), "Per-image MAE": float(errors[i])}
            for i in range(2)]
    return {"prediction": prediction, "target": target, "mask": mask,
            "included": included, "rows": rows, "expected": float(errors.mean())}


def fixture_figure(fixture):
    figure, axes = plt.subplots(2, 3, figsize=(9, 5), layout="constrained")
    for i in range(2):
        for j, (key, title) in enumerate((("prediction", "Prediction − target"),
                                         ("mask", "Included pixels"),
                                         ("included", "Absolute error × mask"))):
            values = fixture[key][i, 0]
            axes[i, j].imshow(values, cmap="Blues" if key == "mask" else "YlOrBr",
                              vmin=0 if key != "prediction" else min(0, float(values.min())))
            for y in range(3):
                for x in range(3):
                    axes[i, j].text(x, y, f"{float(values[y,x]):g}", ha="center", va="center",
                                    fontsize=13, bbox={"facecolor": "white", "alpha": .8, "edgecolor": "none"})
            axes[i, j].set_title(f"Image {i+1} · {title}", fontsize=11)
            axes[i, j].set_axis_off()
    figure.suptitle("Arithmetic example · targets are zero · average the two image errors equally")
    return figure


def comparison_execution(session, comparison, version):
    """Resolve a comparison's exact completed execution, never a later partial attempt."""
    if not comparison:
        return None
    rows = comparison.get("result", {}).get("rows", {}).get(version, [])
    identities = {row.get("evidence", {}).get("stage") for row in rows}
    if len(identities) != 1 or None in identities:
        return None
    identity = next(iter(identities))
    return next((row for row in session.completed() if row["id"] == identity), None)


def saved_predictions(session, names, split, *, executions=None):
    """Read specified executions, or latest validation runs; missing files stay missing."""
    from .solar_teaching import saved
    predictions, records, unavailable = {}, {}, {}
    for label, name in names.items():
        row = executions.get(label) if executions is not None else saved(session, name)
        if not row:
            unavailable[label] = ("Execution referenced by the saved comparison is unavailable"
                                  if executions is not None else "Not executed")
            continue
        if row["name"] != name:
            unavailable[label] = "Referenced execution does not match this comparison version"
            continue
        path = session.file("outputs/" + row["id"] + "/predictions.npy")
        if not path.exists():
            unavailable[label] = "Prediction file unavailable; restore its artifact"
            continue
        values = np.load(path, allow_pickle=False)
        if values.shape != split["y"].shape or not np.isfinite(values).all():
            unavailable[label] = "Saved predictions do not match this split"
            continue
        predictions[label] = values
        records[label] = row
    return predictions, records, unavailable


def aligned_images(predictions, split, *, index=0):
    index = int(index)
    target = split["y"][index, 0]
    mask = split["mask"][index, 0].astype(bool)
    arrays = [target, *(prediction[index, 0] for prediction in predictions.values())]
    lo = min(float(array.min()) for array in arrays)
    hi = max(float(array.max()) for array in arrays)
    error_hi = max((float(np.abs(array-target)[mask].max()) for array in arrays), default=0) or 1
    figure, axes = plt.subplots(2, len(arrays), figsize=(max(10, 3 * len(arrays)), 6.7),
                               squeeze=False)
    figure.subplots_adjust(left=.025, right=.975, top=.91, bottom=.18,
                           wspace=.16, hspace=.28)
    labels = ["Observed future", *predictions]
    for j, (label, array) in enumerate(zip(labels, arrays)):
        im = axes[0, j].imshow(array, origin="lower", cmap="magma", vmin=lo, vmax=hi)
        axes[0, j].set_title(label, fontsize=12)
        if j == 0:
            axes[1, j].imshow(mask, origin="lower", cmap="Greys", vmin=0, vmax=1)
            axes[1, j].set_title("Scoring mask", fontsize=12)
        else:
            err = np.where(mask, np.abs(array - target), np.nan)
            er = axes[1, j].imshow(err, origin="lower", cmap="inferno", vmin=0, vmax=error_hi)
            axes[1, j].set_title("Absolute error", fontsize=12)
        for axis in axes[:, j]:
            axis.set_axis_off()
    intensity_bar = figure.add_axes([.07, .075, .37, .025])
    figure.colorbar(im, cax=intensity_bar, orientation="horizontal",
                    label="Training-normalized log1p intensity")
    if predictions:
        error_bar = figure.add_axes([.56, .075, .37, .025])
        figure.colorbar(er, cax=error_bar, orientation="horizontal",
                        label="Absolute error inside the disk")
    figure.suptitle(str(split["ids"][index]) + " UTC · one forecast origin, shared color scales", fontsize=13)
    rows = [{"Version": label, "Forecast origin UTC": str(split["ids"][index]),
             "This image MAE": float(solar.errors(prediction[index:index+1], split["y"][index:index+1], split["mask"][index:index+1])[0]),
             "All images MAE": float(solar.errors(prediction, split["y"], split["mask"]).mean())}
            for label, prediction in predictions.items()]
    return figure, rows


def comparison_html(figure, origin):
    """Fill the notebook width; keep labels readable by scrolling on narrow screens."""
    import base64
    import html
    import io
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi=120)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    timestamp = html.escape(str(origin), quote=True)
    return (f'<section data-forecast-origin="{timestamp}">'
            f'<p><strong>Showing forecast origin:</strong> {timestamp} UTC</p>'
            '<div style="overflow-x:auto;width:100%" tabindex="0" '
            'aria-label="Aligned solar forecasts; scroll horizontally on a narrow screen">'
            f'<img src="data:image/png;base64,{encoded}" '
            f'alt="Predictions and disk-masked absolute errors for {timestamp} UTC. '
            'All forecasts share an intensity scale and all errors share an error scale." '
            'style="display:block;width:100%;min-width:720px;height:auto"/></div></section>')


def goes_investigation(prediction, split, *, losses=(), title="Saved GOES run"):
    figure, axes = plt.subplots(2, 1, figsize=(11, 6), layout="constrained")
    if len(losses):
        axes[0].plot(np.arange(1, len(losses)+1), losses, color="#237a6c")
        axes[0].set(xlabel="Training step", ylabel="Recorded training loss")
    else:
        axes[0].text(.5, .5, "Training loss is not saved for this execution", ha="center", transform=axes[0].transAxes)
    times = split["ids"].astype("datetime64[m]")
    stride = max(1, len(times) // 1000)
    for values, label, color in ((split["y"], "Observed future", "#222"),
                                  (split["persistence"], "Persistence", "#4382a6"),
                                  (prediction, "Saved model forecast", "#bd7c20")):
        axes[1].plot(times[::stride], values[::stride, 0], label=label, color=color, alpha=.85)
    axes[1].set(xlabel="Forecast origin UTC · target is 30 minutes later", ylabel="log10 XRS-B flux (W/m²)")
    axes[1].legend()
    figure.suptitle(title + " · training loss and forecast error are different measurements")
    return figure
