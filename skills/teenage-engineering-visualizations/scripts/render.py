#!/usr/bin/env python3
"""Render a figure specification without contacting any service.

SVG and HTML need Python 3.11+. Poster QR codes and PNG/PDF exports use the
pinned local Node dependencies. All fonts, images and styles are embedded.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import mimetypes
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / "assets/tokens.json").read_text(encoding="utf-8"))
COLORS = TOKENS["colors"]
METRICS_PATH = ROOT / "assets/font-metrics.json"
METRICS = json.loads(METRICS_PATH.read_text(encoding="utf-8")) if METRICS_PATH.exists() else {}
KINDS = {"overview", "sequence", "transformation", "comparison", "branches", "poster"}
PROVENANCE = {"actual", "recorded", "illustrative", "planned", "unavailable"}


def escaped(value):
    return html.escape(str(value), quote=True)


def slug(value):
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", str(value)).strip("-") or "figure"


def text_width(value, size, family="sans"):
    metrics = METRICS.get(family, {})
    return sum(metrics.get(c, .60 if family == "mono" else .54) for c in str(value)) * size


def wrap(value, width, size, family="sans"):
    lines = []
    for paragraph in str(value).splitlines() or [""]:
        line = ""
        for word in paragraph.split():
            if text_width(word, size, family) > width:
                if line:
                    lines.append(line)
                    line = ""
                segment = ""
                for char in word:
                    if segment and text_width(segment + char, size, family) > width:
                        lines.append(segment)
                        segment = ""
                    segment += char
                line = segment
            elif line and text_width(line + " " + word, size, family) > width:
                lines.append(line)
                line = word
            else:
                line = (line + " " + word).strip()
        lines.append(line)
    return lines


def font_css():
    definitions = []
    for name, family, weight in [
        ("ibm-plex-sans-latin-400-normal.woff2", "IBM Plex Sans", 400),
        ("ibm-plex-sans-latin-600-normal.woff2", "IBM Plex Sans", 600),
        ("ibm-plex-mono-latin-400-normal.woff2", "IBM Plex Mono", 400),
    ]:
        data = base64.b64encode((ROOT / "assets/fonts" / name).read_bytes()).decode()
        definitions.append(f"@font-face{{font-family:'{family}';font-weight:{weight};src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "".join(definitions)


FONT_CSS = font_css()
PRIMITIVES = (ROOT / "assets/primitives.svg").read_text(encoding="utf-8").split("<defs>", 1)[1].split("</defs>", 1)[0]


class Drawing:
    def __init__(self, spec, source, layout, state):
        self.spec, self.source, self.layout, self.state = spec, source, layout, state
        dimensions = TOKENS["layouts"][layout]
        self.w, self.h = dimensions["width"], dimensions["height"]
        self.items = []
        self.text_records = []
        self.warnings = []
        self.margin = 48 if self.w >= 1000 else 36

    def rect(self, x, y, w, h, fill="none", stroke=None, width=1.5):
        self.items.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" stroke="{stroke or COLORS["line"]}" stroke-width="{width:g}"/>')

    def line(self, x1, y1, x2, y2, color=None, dashed=False, arrow=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ''
        marker = ' marker-end="url(#arrow)"' if arrow else ''
        self.items.append(f'<path d="M{x1:g} {y1:g}L{x2:g} {y2:g}" fill="none" stroke="{color or COLORS["ink"]}" stroke-width="1.5"{dash}{marker}/>')

    def text(self, value, x, y, w, h, size=18, weight=400, family="sans", color=None, max_lines=None, preserve_whitespace=False):
        value = str(value or "")
        if not value:
            return y
        key = "semibold" if weight == 600 and family == "sans" else family
        actual = size
        lines = value.splitlines() if preserve_whitespace else wrap(value, w - 2, actual, key)
        cap = max_lines or max(1, int(h / (actual * 1.28)))
        floor = min(size, 15 if family == "mono" else 16)
        while (len(lines) > cap or len(lines) * actual * 1.28 > h or any(text_width(line, actual, key) > w for line in lines)) and actual > floor:
            actual -= .5
            lines = value.splitlines() if preserve_whitespace else wrap(value, w - 2, actual, key)
            cap = max_lines or max(1, int(h / (actual * 1.28)))
        if len(lines) * actual * 1.28 > h + 1 or any(text_width(line, actual, key) > w for line in lines):
            raise ValueError(f'Text does not fit {self.spec["id"]} at {x},{y} in {w}x{h}, size {actual}: {value[:90]!r}. Shorten the copy or choose a larger layout.')
        family_name = "IBM Plex Mono" if family == "mono" else "IBM Plex Sans"
        for index, line in enumerate(lines):
            baseline = y + actual + index * actual * 1.28
            box = f"{x:g} {y:g} {w:g} {h:g}"
            self.items.append(f'<text x="{x:g}" y="{baseline:g}" font-family="{family_name}" font-size="{actual:g}" font-weight="{weight}" fill="{color or COLORS["ink"]}" data-box="{box}" xml:space="preserve">{escaped(line)}</text>')
            self.text_records.append({"text": line, "box": [x, y, w, h], "size": actual, "family": family, "estimated_width": round(text_width(line, actual, key), 2)})
        return y + len(lines) * actual * 1.28

    def number(self, value, x, y, focus=False):
        self.items.append(f'<circle cx="{x:g}" cy="{y:g}" r="14" fill="{COLORS["accent"] if focus else COLORS["ink"]}"/>')
        self.items.append(f'<text x="{x:g}" y="{y+6:g}" text-anchor="middle" font-family="IBM Plex Sans" font-size="19" font-weight="600" fill="{COLORS["ink"] if focus else COLORS["white"]}">{escaped(value)}</text>')

    def symbol(self, symbol, x, y, size=64, color=None):
        symbol = symbol if symbol in {"file", "record", "component", "input", "output", "observation", "state"} else "component"
        self.items.append(f'<use href="#{symbol}" x="{x:g}" y="{y:g}" width="{size:g}" height="{size:g}" fill="none" stroke="{color or COLORS["ink"]}" stroke-width="1.5"/>')

    def media(self, value, x, y, w, h):
        if isinstance(value, dict):
            value = value.get("path") or value.get("src")
        if not value:
            return False
        if re.match(r"^[a-zA-Z]+:", str(value)):
            raise ValueError("Media must be a local path; remote resources are never downloaded.")
        path = (self.source.parent / value).resolve()
        if not path.is_file():
            raise ValueError(f"Missing local media: {path}")
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        data = base64.b64encode(path.read_bytes()).decode()
        self.items.append(f'<image x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{data}"/>')
        return True

    def group(self, step):
        visible = step["id"] in self.state.get("visible", [s["id"] for s in self.spec["steps"]])
        self.items.append(f'<g data-component="{escaped(step["id"])}" opacity="{1 if visible else .10}" aria-hidden="{str(not visible).lower()}">')
        return step["id"] in self.state.get("focus", [])

    def endgroup(self):
        self.items.append("</g>")

    def code(self, value, x, y, w, h):
        if not value:
            return
        self.rect(x, y, w, h, COLORS["panel"], COLORS["panel"])
        self.text(value, x + 12, y + 9, w - 24, h - 18, size=15, family="mono", preserve_whitespace=True)

    def header(self):
        m, w = self.margin, self.w - 2 * self.margin
        self.rect(m, 28, w, 34, COLORS["ink"], COLORS["ink"])
        self.text(self.spec.get("eyebrow", "Technical guide"), m + 14, 33, w - 190, 24, size=14, color=COLORS["white"])
        provenance = self.spec.get("native_capture", {}).get("provenance", "recorded") if self.state.get("capture") else self.spec["provenance"]
        self.text(provenance.upper(), self.w - m - 160, 33, 145, 24, size=12, family="mono", color=COLORS["white"])
        self.text(self.spec["title"], m, 78, w, 57, size=32, weight=600, max_lines=2)
        self.text(self.spec.get("question") or self.spec.get("summary", ""), m, 139, w, 50, size=18)

    def footer(self):
        m = self.margin
        self.line(m, self.h - 40, self.w - m, self.h - 40)
        self.text(self.state.get("caption", ""), m, self.h - 34, self.w - 2 * m - 70, 33, size=12)
        self.text(self.state.get("position", ""), self.w - m - 58, self.h - 34, 58, 33, size=12, family="mono")

    def focus_step(self):
        ids = self.state.get('focus') or self.state.get('visible') or [s['id'] for s in self.spec['steps']]
        return next((s for s in self.spec['steps'] if s['id'] == ids[-1]), self.spec['steps'][-1])

    def detail(self):
        step = self.focus_step()
        m, y = self.margin, self.h - 237
        full = self.w - 2 * m
        left, right = full * .46, full * .50
        rx = self.w - m - right
        self.line(m, y, self.w - m, y, COLORS['ink'])
        self.text(step['title'], m, y + 12, left, 35, size=21, weight=600)
        self.text(step.get('body'), m, y + 55, left, 110, size=17)
        notes = [a for a in self.spec.get('annotations', []) if a.get('target') == step['id']]
        if notes:
            self.text(' · '.join(f"{a.get('number', '')} {a['label']}" for a in notes), m, y + 164, left, 28, size=13)
        if step.get('code'):
            self.code(step['code'], rx, y + 12, right, 104)
            self.text(step.get('output', ''), rx + 10, y + 123, right - 20, 45, size=17, weight=600)
            if step.get('excerpt_label'):
                self.text(step['excerpt_label'], rx, y + 162, right, 32, size=12)
        elif step.get('media'):
            self.media(step['media'], rx, y + 12, right, 142)
            self.text(step.get('output', ''), rx, y + 161, right, 32, size=16, weight=600)
        else:
            self.text(step.get('input', ''), rx, y + 15, right, 50, size=17, family='mono')
            self.line(rx, y + 79, self.w - m, y + 79, dashed=True)
            self.text(step.get('output') or step.get('status', ''), rx, y + 93, right, 80, size=20, weight=600)

    def overview(self):
        steps, m, gap = self.spec['steps'], self.margin, 26
        if self.spec.get('hero'):
            full = self.w - 2 * m
            hero_width = full * .66
            x = m + hero_width + 28
            width = full - hero_width - 28
            step = self.focus_step()
            self.media(self.spec['hero'], m, 204, hero_width, self.h - 269)
            self.line(x - 14, 211, x - 14, self.h - 69)
            self.number(steps.index(step) + 1, x + 14, 226, True)
            self.text(step['title'], x, 258, width, 73, size=22, weight=600)
            self.text(step.get('body'), x, 345, width, 155, size=18)
            self.text(step.get('output') or step.get('input', ''), x, 520, width, self.h - 580, size=18, weight=600)
            return
        col = (self.w - 2 * m - gap * (len(steps) - 1)) / len(steps)
        top = 205
        for i, step in enumerate(steps):
            x = m + i * (col + gap)
            focus = self.group(step)
            self.number(i + 1, x + 14, top + 15, focus)
            self.symbol(step.get('symbol'), x + (col - 68) / 2, top + 34, 68, COLORS['accent'] if focus else None)
            self.text(step['title'], x, top + 116, col, 71, size=21, weight=600)
            if i < len(steps) - 1:
                self.line(x + col - 4, top + 69, x + col + gap - 8, top + 69, arrow=True)
            self.endgroup()
        self.detail()

    def sequence(self):
        steps, m = self.spec['steps'], self.margin
        top, bottom = 204, self.h - 256
        row = (bottom - top) / len(steps)
        for i, step in enumerate(steps):
            y = top + i * row
            focus = self.group(step)
            self.number(i + 1, m + 14, y + row / 2, focus)
            self.text(step['title'], m + 43, y + 6, self.w * .44 - m - 43, row - 8, size=19, weight=600)
            x = self.w * .48
            self.text(step.get('input') or step.get('output') or step.get('status', ''), x, y + 6, self.w - m - x, row - 8, size=16, family='mono')
            if i < len(steps) - 1:
                self.line(m + 14, y + row / 2 + 16, m + 14, y + row - 2, COLORS['line'])
            self.endgroup()
        self.detail()

    def transformation(self):
        steps, m, gap = self.spec['steps'], self.margin, 30
        col = (self.w - 2 * m - gap * (len(steps) - 1)) / len(steps)
        y = 207
        for i, step in enumerate(steps):
            x = m + i * (col + gap)
            focus = self.group(step)
            self.number(i + 1, x + 14, y + 15, focus)
            self.text(step['title'], x + 38, y, col - 38, 68, size=20, weight=600)
            input_height = 85 if self.layout == 'notebook' else 61
            self.rect(x, y + 83, col, input_height, COLORS['white'])
            self.text(step['input'], x + 10, y + 91, col - 20, input_height - 14, size=16, family='mono')
            self.line(x + col / 2, y + 85 + input_height, x + col / 2, y + 102 + input_height, arrow=True)
            self.text(step['output'], x + 8, y + 108 + input_height, col - 16, 66 if self.layout == 'notebook' else 47, size=17, weight=600)
            if i < len(steps) - 1:
                self.line(x + col + 3, y + 112, x + col + gap - 7, y + 112, arrow=True)
            self.endgroup()
        self.detail()

    def comparison(self):
        steps, m, gap, y = self.spec['steps'], self.margin, 26, 207
        col = (self.w - 2 * m - gap * (len(steps) - 1)) / len(steps)
        for i, step in enumerate(steps):
            x = m + i * (col + gap)
            focus = self.group(step)
            color = COLORS['parent'] if i == 0 else COLORS['candidate_a'] if i == 1 else COLORS['candidate_b']
            self.rect(x, y, col, 5, color, color)
            self.text(step['title'], x, y + 19, col, 66, size=21, weight=600)
            self.text(step.get('status', ''), x, y + 89, col, 36, size=13, family='mono')
            self.text(step.get('output') or step.get('input', ''), x, y + 129, col, 78, size=18, weight=600)
            self.endgroup()
        self.detail()

    def branches(self):
        steps, m = self.spec['steps'], self.margin
        if len(steps) < 3:
            raise ValueError('branches needs parent, candidate(s), and decision steps')
        parent, candidates, decision = steps[0], steps[1:-1], steps[-1]
        top, mid, low, cx = 201, 273, self.h - 290, self.w / 2
        self.group(parent)
        self.rect(cx - 235, top, 470, 44, COLORS['panel'])
        self.text(parent['title'], cx - 220, top + 8, 440, 31, size=18, weight=600)
        self.endgroup()
        gap = 42
        col = (self.w - 2 * m - (len(candidates) - 1) * gap) / len(candidates)
        for i, step in enumerate(candidates):
            x = m + i * (col + gap)
            focus = self.group(step)
            color = COLORS['candidate_a'] if i == 0 else COLORS['candidate_b']
            self.line(cx, top + 44, x + col / 2, mid - 8, arrow=True)
            self.rect(x, mid, col, 4, color, color)
            self.text(step['title'], x, mid + 13, col, 50, size=19, weight=600)
            self.text(step.get('status') or step.get('output', ''), x, mid + 67, col, 29, size=14, family='mono')
            self.line(x + col / 2, low - 9, cx, low + 7, dashed=True)
            self.endgroup()
        self.group(decision)
        self.rect(m + 65, low + 10, self.w - 2 * m - 130, 43, COLORS['white'])
        self.text(decision['title'], m + 82, low + 17, self.w - 2 * m - 164, 30, size=18, weight=600)
        self.endgroup()
        self.detail()

    def capture(self):
        capture = self.spec['native_capture']
        m = self.margin
        self.media(capture['media'], m, 202, self.w - 2 * m, self.h - 264)

    def poster(self):
        p, m = self.spec["poster"], 64
        w = self.w - 2 * m
        self.rect(m, 40, w, 43, COLORS["ink"], COLORS["ink"])
        self.text(self.spec.get("eyebrow", "Workshop guide"), m + 16, 47, w - 32, 30, size=17, color="white")
        self.text(self.spec["title"], m, 110, w, 164, size=58, weight=600, max_lines=2)
        self.text(p["situation"], m, 278, w, 97, size=25)
        hero_top, hero_height = 394, self.h * .285
        self.line(m, hero_top - 14, self.w - m, hero_top - 14)
        if not self.media(p.get("hero"), m, hero_top, w, hero_height):
            steps = self.spec["steps"]
            col = w / len(steps)
            for i, step in enumerate(steps):
                x = m + i * col
                self.symbol(step.get("symbol"), x + col / 2 - 48, hero_top + 35, 96)
                self.text(step["title"], x + 12, hero_top + 154, col - 24, 76, size=23, weight=600)
                if i < len(steps) - 1:
                    self.line(x + col - 20, hero_top + 83, x + col + 14, hero_top + 83, arrow=True)
        y = hero_top + hero_height + 20
        self.line(m, y, self.w - m, y)
        self.text("What you will build and check", m, y + 16, w, 36, size=25, weight=600)
        col, gap = (w - 44) / 3, 22
        for i, outcome in enumerate(p["outcomes"]):
            x = m + i * (col + gap)
            self.number(i + 1, x + 14, y + 81)
            self.text(outcome, x, y + 110, col, 103, size=23)
        y += 230
        self.text(p.get("roles_title") or ("Where Forge helps" if "forge" in p else "Tools and responsibilities"), m, y, w, 36, size=25, weight=600)
        forge = p.get("roles", p.get("forge", []))
        for i, item in enumerate(forge):
            row_y = y + 48 + i * 34
            self.text(item["name"], m, row_y, 235, 31, size=18, weight=600)
            self.text(item["action"], m + 246, row_y, w - 246, 31, size=18)
        bottom = self.h - 191
        if y + 48 + len(forge) * 34 > bottom - 15:
            raise ValueError("Poster has too many role entries; use at most four concise roles.")
        self.line(m, bottom, self.w - m, bottom)
        meta = f'{p["duration"]} · {p["prerequisites"]}'
        self.text(meta, m, bottom + 15, w - 155, 29, size=17, family="mono")
        self.text(p["dataset"], m, bottom + 51, w - 155, 42, size=17)
        self.text(p["cta"]["label"], m, bottom + 105, w - 155, 43, size=22, weight=600)
        qr = subprocess.run(["node", str(ROOT / "scripts/qr.mjs"), p["cta"]["url"]], text=True, capture_output=True, check=True).stdout.strip()
        self.items.append(f'<a href="{escaped(p["cta"]["url"])}"><image x="{self.w-m-128}" y="{bottom+21}" width="128" height="128" href="data:image/svg+xml;base64,{base64.b64encode(qr.encode()).decode()}"/></a>')
        self.text(p["cta"].get("display_url") or re.sub(r"^https?://", "", p["cta"]["url"]), m, self.h - 32, w, 23, size=12, family="mono")

    def render(self):
        self.items.append(f'<rect width="{self.w}" height="{self.h}" fill="{COLORS["paper"]}"/>')
        if self.spec["kind"] == "poster":
            self.poster()
        else:
            self.header()
            if self.state.get("capture"):
                self.capture()
            else:
                getattr(self, self.spec["kind"])()
            self.footer()
        description = self.spec.get("summary") or self.spec.get("question") or self.spec["title"]
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" role="img" aria-labelledby="figure-title figure-description">
<title id="figure-title">{escaped(self.spec["title"])}</title><desc id="figure-description">{escaped(description)} {escaped(self.state.get("caption", ""))}</desc>
<defs><style>{FONT_CSS}</style>{PRIMITIVES}<marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto-start-reverse"><path d="M0 0L7 3.5L0 7" fill="none" stroke="{COLORS["ink"]}"/></marker></defs>
{"".join(self.items)}</svg>'''
        prefix = slug(self.spec["id"]) + "-" + slug(self.state["id"]) + "-"
        svg = re.sub(r'id="([^"]+)"', lambda m: 'id="' + prefix + m[1] + '"', svg)
        svg = svg.replace('href="#', 'href="#' + prefix).replace('url(#', 'url(#' + prefix)
        return svg.replace('aria-labelledby="figure-title figure-description"', f'aria-labelledby="{prefix}figure-title {prefix}figure-description"')


def check_spec(spec):
    required = {"schema_version", "id", "title", "kind", "provenance", "steps"}
    missing = required - set(spec)
    if missing:
        raise ValueError(f"Missing spec fields: {sorted(missing)}")
    if spec["schema_version"] != 1 or spec["kind"] not in KINDS or spec["provenance"] not in PROVENANCE:
        raise ValueError("Unsupported schema version, composition, or provenance")
    steps = spec["steps"]
    min_steps = 0 if spec["kind"] == "poster" and spec.get("poster", {}).get("hero") else 1
    if not min_steps <= len(steps) <= 6:
        raise ValueError("Use one to six components; split longer explanations into figures")
    ids = [s["id"] for s in steps]
    if len(set(ids)) != len(ids):
        raise ValueError("Component IDs must be unique")
    if spec["kind"] == "transformation":
        for step in steps:
            if not str(step.get("input", "")).strip() or not str(step.get("output", "")).strip():
                raise ValueError(f"Transformation {step['id']} needs an explicit input and output")
    states = spec.get("states") or [{"id": "complete", "label": "Complete view", "visible": ids, "focus": [], "caption": spec.get("summary", "")}]
    if len({s["id"] for s in states}) != len(states):
        raise ValueError("State IDs must be unique")
    for state in states:
        for key in ["visible", "focus"]:
            if set(state.get(key, [])) - set(ids):
                raise ValueError(f"State {state['id']} has unknown {key} component IDs")
    if spec["kind"] == "poster" and len(spec["poster"]["outcomes"]) != 3:
        raise ValueError("A poster has exactly three learning outcomes")
    states = list(states)
    if spec.get("native_capture"):
        capture = spec["native_capture"]
        states.append({"id":"native-capture","label":capture["title"],"visible":ids,"focus":[],"caption":capture["investigation"],"capture":True})
    return states


def html_document(spec, frames):
    body = []
    for i, (state, svg) in enumerate(frames):
        body.append(f'<figure class="frame" data-state="{escaped(state["id"])}" aria-hidden="{str(i != 0).lower()}">{svg}</figure>')
    options = "".join(f'<option value="{i}">{i+1}. {escaped(s["label"])}</option>' for i, (s, _) in enumerate(frames))
    details = "".join(f'<li><strong>{escaped(s["title"])}</strong>: {escaped(s.get("body", ""))}{"<pre>"+escaped(s["code"])+"</pre>" if s.get("code") else ""}</li>' for s in spec["steps"])
    explanation = f'<details><summary>Read the complete explanation</summary><ol>{details}</ol></details>' if details else ''
    if spec["kind"] == "poster":
        poster = spec["poster"]
        outcomes = "".join(f'<li>{escaped(item)}</li>' for item in poster["outcomes"])
        roles = "".join(f'<li><strong>{escaped(item["name"])}</strong>: {escaped(item["action"])}</li>' for item in poster.get("roles", poster.get("forge", [])))
        metadata = "".join(f'<dt>{label}</dt><dd>{escaped(poster[key])}</dd>' for key, label in (("duration", "Duration"), ("prerequisites", "Prerequisites"), ("dataset", "Data")) if poster.get(key))
        cta = poster["cta"]
        explanation += f'<h2>What you will learn</h2><ol>{outcomes}</ol>'
        if roles:
            explanation += f'<h2>Where the parts help</h2><ul>{roles}</ul>'
        explanation += f'<dl>{metadata}</dl><p><a class="action" href="{escaped(cta["url"])}">{escaped(cta["label"])}</a></p>'
    source_items = list(spec.get("source_links", []))
    if spec.get("native_capture"):
        source_items.append({"url":spec["native_capture"]["source_url"],"label":"Open the native record shown in the capture"})
    sources = "".join(f'<li><a href="{escaped(s["url"])}">{escaped(s["label"])}</a></li>' for s in source_items)
    captions = json.dumps([s.get("caption", "") for s, _ in frames]).replace("<", "\\u003c")
    provenances = json.dumps([spec.get("native_capture", {}).get("provenance", "recorded") if state.get("capture") else spec["provenance"] for state, _ in frames]).replace("<", "\\u003c")
    color_variables = ":root{" + ";".join(f"--{name.replace('_', '-')}:{value}" for name, value in COLORS.items()) + "}"
    styles = color_variables + (ROOT / "assets/style.css").read_text(encoding="utf-8")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escaped(spec["title"])}</title><style>{FONT_CSS}{styles}</style></head><body><main>
{"".join(body)}<p class="caption" aria-live="polite"></p><nav aria-label="Explanation steps"><button id="back" type="button">← Back</button><label for="state">View</label><select id="state">{options}</select><button id="next" type="button">Next →</button><span class="status">{escaped(spec["provenance"])} example · display controls only</span></nav>
<section class="description"><h1>{escaped(spec["title"])}</h1><p>{escaped(spec.get("summary", ""))}</p>{explanation}<h2>Sources and related records</h2><ul>{sources}</ul></section></main>
<script>const captions={captions};const provenances={provenances};const frames=[...document.querySelectorAll('.frame')];const selector=document.querySelector('#state');let current=0;function show(n){{current=Math.max(0,Math.min(frames.length-1,n));frames.forEach((f,i)=>f.setAttribute('aria-hidden',String(i!==current)));selector.value=String(current);document.querySelector('#back').disabled=current===0;document.querySelector('#next').disabled=current===frames.length-1;document.querySelector('.caption').textContent=captions[current];document.querySelector('.status').textContent=provenances[current]+' example · display controls only';}}document.querySelector('#back').onclick=()=>show(current-1);document.querySelector('#next').onclick=()=>show(current+1);selector.onchange=()=>show(Number(selector.value));document.addEventListener('keydown',e=>{{if(e.target.matches('input,textarea,select'))return;if(e.key==='ArrowRight'){{show(current+1);e.preventDefault();}}if(e.key==='ArrowLeft'){{show(current-1);e.preventDefault();}}}});show(0);</script></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--layout", choices=list(TOKENS["layouts"]), default="slide")
    parser.add_argument("--formats", default="svg,html")
    args = parser.parse_args()
    formats = set(args.formats.split(","))
    if formats - {"svg", "html", "png", "pdf"}:
        parser.error("formats must be svg,html,png,pdf")
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    states = check_spec(spec)
    if spec["kind"] == "poster" and args.layout not in {"digital", "print"}:
        parser.error("posters use digital or print layout")
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {"schema_version": 1, "id": spec["id"], "kind": spec["kind"], "layout": args.layout, **TOKENS["layouts"][args.layout], "source_sha256": hashlib.sha256(args.spec.read_bytes()).hexdigest(), "states": [], "html": "index.html"}
    frames, bounds = [], []
    for i, state in enumerate(states):
        drawing = Drawing(spec, args.spec.resolve(), args.layout, {**state, "position": f"{i+1:02d}/{len(states):02d}"})
        svg = drawing.render()
        ET.fromstring(svg)
        filename = f'{i+1:02d}-{slug(state["id"])}.svg'
        (args.output / filename).write_text(svg, encoding="utf-8")
        manifest["states"].append({"id": state["id"], "label": state["label"], "svg": filename, "caption": state.get("caption", "")})
        frames.append((state, svg))
        bounds.append({"file": filename, "text": drawing.text_records})
    (args.output / "final.svg").write_text(frames[-1][1], encoding="utf-8")
    (args.output / "index.html").write_text(html_document(spec, frames), encoding="utf-8")
    (args.output / "text-bounds.json").write_text(json.dumps(bounds, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "index.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if formats & {"png", "pdf"}:
        subprocess.run(["node", str(ROOT / "scripts/export.mjs"), str(args.output.resolve()), ",".join(sorted(formats & {"png", "pdf"}))], check=True)
    print(json.dumps({"id": spec["id"], "output": str(args.output), "states": len(states), "formats": sorted(formats)}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        print(f"Cannot render figure: {error}", file=sys.stderr)
        sys.exit(1)
