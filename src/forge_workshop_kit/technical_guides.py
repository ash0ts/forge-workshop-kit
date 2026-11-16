"""Read-only technical diagrams shared with the workshop decks.

The renderer runs when maintainers build a release. Participants only read the
bundled SVGs. Guide selection never touches a session, stage, or provider.
"""
from __future__ import annotations

import base64
from functools import cache
from html import escape
from importlib.resources import files
import json
from pathlib import PurePosixPath


STYLE = """<style>
.technical-guide{container-type:inline-size;font-family:'IBM Plex Sans',system-ui,sans-serif;color:var(--wk-ink,#242522);border:1px solid var(--wk-line,#b6b7af);margin:18px 0;background:var(--wk-paper,#f4f3ef)}
.technical-guide-head{padding:12px 16px;background:#242522;color:#fff;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}.technical-guide-head strong{font-size:18px}.technical-guide-head span{font:12px 'IBM Plex Mono',monospace;color:#dadbd5}
.technical-guide nav{display:flex;gap:8px;flex-wrap:wrap;padding:12px 16px;border-bottom:1px solid var(--wk-line,#b6b7af)}
.technical-guide figure{margin:0}.technical-guide-image{display:block;width:100%;min-width:960px;height:auto;background:#f4f3ef}.technical-guide-caption{font-size:15px;line-height:1.5;padding:12px 16px;border-top:1px solid var(--wk-line,#b6b7af);margin:0}.technical-guide footer{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;flex-wrap:wrap}.technical-guide footer span{font:13px 'IBM Plex Mono',monospace}.technical-guide details{padding:0 16px 14px;font-size:14px;line-height:1.55}.technical-guide summary{cursor:pointer}.technical-guide a{color:inherit;text-decoration:underline}.technical-guide :is(button,a,summary):focus-visible{outline:3px solid #ec5b28;outline-offset:3px}.technical-guide details li{margin:8px 0}.technical-guide .technical-guide-note{padding:12px 16px;margin:0;font-size:13px;color:var(--wk-muted,#60625d)}.technical-guide pre{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.5 'IBM Plex Mono',monospace}.technical-guide-text-view{display:none;padding:12px}.technical-guide-text-view ol{list-style-position:inside;margin:0;padding:0}.technical-guide-text-view li{padding:12px;margin:0 0 10px;border:1px solid var(--wk-line,#b6b7af);font-size:15px;line-height:1.5;overflow-wrap:anywhere}.technical-guide-text-view li[data-focus="true"]{border-left:4px solid #ec5b28}.technical-guide-text-view p{margin:8px 0}
.technical-guide-scroll-hint{display:none;padding:10px 16px;margin:0;font-size:13px}.technical-guide-canvas{overflow-x:auto}.technical-guide-canvas:focus-visible{outline:3px solid #ec5b28;outline-offset:-3px}
@media(max-width:900px){.technical-guide-head{padding:10px 12px}.technical-guide nav,.technical-guide footer{padding:10px 12px}.technical-guide-caption{padding:10px 12px}.technical-guide-head strong{font-size:17px}.technical-guide-text-view{display:block}.technical-guide-canvas{max-width:100%}}
@container(max-width:950px){.technical-guide-scroll-hint,.technical-guide-text-view{display:block}}
@media(prefers-reduced-motion:reduce){.technical-guide *{animation:none!important;transition:none!important}}
</style>"""


def _assets():
    return files("forge_workshop_kit").joinpath("assets", "technical-guides")


@cache
def theme_style():
    """Apply the skill's packaged tokens to the existing notebook components."""
    colors = json.loads(_assets().joinpath("tokens.json").read_text(encoding="utf-8"))["colors"]
    return """<style>
:root{--wk-ink:INK;--wk-muted:MUTED;--wk-paper:var(--background,PAPER);--wk-line:LINE;--wk-accent:INK;--wk-gold:ACCENT}
.dark,.dark-theme,[data-theme="dark"]{--wk-ink:#f0f0eb;--wk-muted:#c7c8c1;--wk-paper:var(--background,#22231f);--wk-line:#6d6f65;--wk-accent:#f0f0eb}
.workshop-head{background:INK;color:PAPER;border-radius:0;border-top:3px solid ACCENT;padding:24px}.workshop-head p{color:#e1e2da}.workshop-label{color:#ff8858;letter-spacing:.04em;text-transform:none}.workshop-head h1{letter-spacing:-.5px}.workshop-head .workshop-lab-art{display:none}
.workshop-step h2{border-left:4px solid ACCENT;padding-left:12px}.workshop-result,.workshop-branch,.workshop-workbench fieldset,.workshop-evidence a,.workshop-workbench .wk-choice,.workshop-diff{border-radius:0}.workshop-result{border-left-width:2px}.workshop-result[data-status="unavailable"],.workshop-result[data-status="failed"]{border-left-color:var(--wk-line)}.workshop-context{font-family:'IBM Plex Mono',monospace;font-size:12px}.workshop-evidence a:focus-visible,.workshop-branch a:focus-visible,.workshop-branch summary:focus-visible{outline-color:ACCENT}.workshop-workbench .wk-panel{border-left-width:2px}
</style>""".replace("PAPER", colors["paper"]).replace("INK", colors["ink"]).replace("MUTED", colors["muted"]).replace("LINE", colors["line"]).replace("ACCENT", colors["accent"])


def _relative(path):
    value = PurePosixPath(str(path))
    if value.is_absolute() or ".." in value.parts or "\\" in str(path):
        raise ValueError("Guide assets must stay inside the bundled directory.")
    return value


@cache
def catalog():
    return json.loads(_assets().joinpath("index.json").read_text(encoding="utf-8"))


def workshop(slug):
    for row in catalog()["workshops"]:
        if slug in (row.get("slug"), row.get("notebook_slug"), row.get("deck_slug")):
            return row
    raise ValueError(f"No technical guides are registered for {slug!r}.")


def sequences(slug, step):
    """Return only explanations appropriate to the currently open lesson."""
    row = workshop(slug)
    chosen = [dict(item) for item in row["sequences"] if item["notebook_step"] == step]
    if step == "setup":
        chosen.insert(0, {"id": "overview", "title": "What you will build", "spec": row["overview"]})
    return chosen


def _directory(sequence):
    spec = _relative(sequence["spec"])
    return _assets().joinpath(*spec.with_suffix("").parts)


def read_guide(sequence):
    directory = _directory(sequence)
    rendered = json.loads(directory.joinpath("notebook", "index.json").read_text(encoding="utf-8"))
    if not rendered.get("states"):
        raise ValueError("A technical guide must contain at least one rendered state.")
    spec = json.loads(directory.joinpath("spec.json").read_text(encoding="utf-8"))
    return rendered, spec


def _steps_text(spec, *, visible=None, focus=()):
    rows = []
    for item in spec.get("steps", spec.get("nodes", [])):
        if visible is not None and item.get("id") not in visible:
            continue
        label = item.get("label", item.get("title", item.get("id", "")))
        detail = item.get("body", item.get("detail", item.get("description", "")))
        if isinstance(detail, list):
            detail = "; ".join(str(value) for value in detail)
        values = "".join("<p><b>" + name.title() + ":</b> " + escape(str(item[name])) + "</p>" for name in ("input", "output") if item.get(name))
        code = "<pre>" + escape(item["code"]) + "</pre>" if item.get("code") else ""
        rows.append('<li data-focus="' + str(item.get("id") in focus).lower() + '"><strong>' + escape(str(label)) + "</strong> " + escape(str(detail)) + values + code + "</li>")
    return "".join(rows)


def _description(spec):
    """Text alternative uses the same authored labels as the picture."""
    sources = []
    for item in spec.get("source_links", spec.get("sources", [])):
        if isinstance(item, str):
            item = {"url": item, "label": item}
        url = str(item.get("url", ""))
        label = str(item.get("label", item.get("title", url)))
        sources.append('<li><a target="_blank" rel="noopener" href="' + escape(url, quote=True) + '">' + escape(label) + " ↗</a></li>" if url.startswith("https://") else "<li>" + escape(label) + "</li>")
    return ('<details><summary>Text description and sources</summary><ul>' + _steps_text(spec) + "</ul>"
            + ("<ul>" + "".join(sources) + "</ul>" if sources else "") + "</details>")


def frame_html(sequence, number=0):
    rendered, spec = read_guide(sequence)
    number = max(0, min(int(number), len(rendered["states"]) - 1))
    state = rendered["states"][number]
    image = _directory(sequence).joinpath("notebook", *_relative(state["svg"]).parts).read_bytes()
    uri = "data:image/svg+xml;base64," + base64.b64encode(image).decode("ascii")
    label = state.get("label", state["id"])
    caption = state.get("caption", "")
    source_state = next((item for item in spec.get("states", []) if item["id"] == state["id"]), {})
    narrow = ('<div class="technical-guide-text-view"><p>' + escape(spec.get("question", "")) + '</p><ol>'
              + _steps_text(spec, visible=source_state.get("visible"), focus=source_state.get("focus", [])) + '</ol></div>')
    provenance = str(spec.get("provenance", "illustrative")).capitalize() + " example"
    content = ('<p class="technical-guide-scroll-hint">Scroll the drawing sideways to inspect it. A text explanation follows below.</p><figure><div class="technical-guide-canvas" tabindex="0" role="region" aria-label="Illustration; scroll horizontally on a narrow screen"><img class="technical-guide-image" src="' + uri + '" alt="'
               + escape(sequence["title"] + ": " + label, quote=True) + '">'
               + '</div>'
               + narrow
               + '<figcaption class="technical-guide-caption"><strong>' + escape(label) + "</strong>"
               + (" · " + escape(caption) if caption else "") + "<br><small>" + escape(provenance) + "</small></figcaption></figure>")
    return content + _description(spec), number, len(rendered["states"])


def controls(mo, slug, set_view):
    """Construct stable controls once, outside the reactive frame cell.

    Recreating buttons inside a batch replays their restored click values in
    marimo. Stable buttons use absolute destinations, so redraw is read-only.
    """
    buttons = {}

    def choose(step, identity, frame=None):
        def update(previous):
            current = dict(previous.get(step, {}))
            frames = dict(current.get("frames", {}))
            if frame is not None:
                frames[identity] = frame
            return {**previous, step: {"sequence": identity, "frames": frames}}
        set_view(update)

    row = workshop(slug)
    steps = {"setup", *(item["notebook_step"] for item in row["sequences"])}
    for step in sorted(steps):
        for sequence in sequences(slug, step):
            identity = sequence["id"]
            rendered, _ = read_guide(sequence)
            count = len(rendered["states"])
            buttons[(step, identity, "select")] = mo.ui.button(
                label=sequence["title"],
                on_change=lambda _, step=step, identity=identity: choose(step, identity),
                tooltip="Show this explanation; no work will run")
            for position in range(count):
                for action, delta in (("back", -1), ("next", 1)):
                    destination = max(0, min(position + delta, count - 1))
                    buttons[(step, identity, position, action)] = mo.ui.button(
                        label="← Back" if action == "back" else "Next →",
                        disabled=destination == position,
                        on_change=lambda _, step=step, identity=identity, destination=destination: choose(step, identity, destination))
    return buttons


def panel(mo, slug, step, view, buttons):
    """Render a frame with controls created by :func:`controls`.

    ``view`` is display-only mo.state; it is deliberately not a WorkshopSession.
    Creating this view does not create buttons or run their callbacks.
    """
    available = sequences(slug, step)
    if not available:
        return mo.md("")
    active = next((item for item in available if item["id"] == view.get(step, {}).get("sequence")), available[0])
    frame = view.get(step, {}).get("frames", {}).get(active["id"], 0)
    body, position, count = frame_html(active, frame)
    title = escape(active["title"])
    content = [mo.Html(theme_style() + STYLE + '<header class="technical-guide-head"><span>Visual guide</span><strong>' + title + '</strong></header>')]
    if len(available) > 1:
        content.append(mo.hstack([buttons[(step, item["id"], "select")] for item in available], justify="start", wrap=True))
    content.extend([
        mo.Html('<section class="technical-guide" aria-label="' + title + '">' + body + '</section>'),
        mo.hstack([buttons[(step, active["id"], position, "back")],
                   mo.Html('<span aria-live="polite">' + str(position + 1) + ' / ' + str(count) + '</span>'),
                   buttons[(step, active["id"], position, "next")]], justify="space-between", align="center"),
        mo.md("This guide explains the code below. Its controls do not execute the exercise. Illustrated and recorded examples are labeled in the drawing."),
    ])
    return mo.vstack(content, gap=0.5)
