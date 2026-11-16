"""Small SVG authoring primitives for original mechanism drawings.

These primitives draw geometry, not layouts. The author chooses the object,
its parts and each operation. Rendering/export stays in render.py.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = json.loads((ROOT / 'assets/tokens.json').read_text(encoding='utf-8'))['colors']


class Illustration:
    def __init__(self, title, *, width=1200, height=675):
        self.width, self.height = width, height
        self.items = [f'<title>{html.escape(title)}</title>',
                      f'<rect width="{width}" height="{height}" fill="{COLORS["paper"]}"/>']

    def rect(self, x, y, w, h, *, fill='none', stroke=None, sw=1.6, rx=0):
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke or COLORS["ink"]}" stroke-width="{sw}"/>')

    def path(self, d, *, fill='none', stroke=None, sw=1.6, dash=None):
        self.items.append(f'<path d="{d}" fill="{fill}" stroke="{stroke or COLORS["ink"]}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')

    def line(self, x1, y1, x2, y2, **kwargs):
        self.path(f'M{x1} {y1}L{x2} {y2}', **kwargs)

    def text(self, text, x, y, *, size=18, width=400, height=None, weight=400, mono=False, fill=None):
        """y is the top of a measured text area, not a font baseline."""
        height = height or size * 1.5
        self.items.append(f'<text x="{x}" y="{y + size}" font-family="IBM Plex {"Mono" if mono else "Sans"}" font-size="{size}" font-weight="{weight}" fill="{fill or COLORS["ink"]}" data-box="{x} {y} {width} {height}">{html.escape(str(text))}</text>')

    def circle(self, x, y, r, *, fill='none', stroke=None, sw=1.6):
        self.items.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke or COLORS["ink"]}" stroke-width="{sw}"/>')

    def arrow(self, x1, y1, x2, y2, *, color=None, dashed=False):
        from math import atan2, cos, sin
        a = atan2(y2-y1, x2-x1)
        self.line(x1, y1, x2, y2, stroke=color, dash='6 5' if dashed else None)
        points = [(x2-10*cos(a)+5*sin(a),y2-10*sin(a)-5*cos(a)),(x2,y2),(x2-10*cos(a)-5*sin(a),y2-10*sin(a)+5*cos(a))]
        self.path('M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in points), stroke=color)

    def label(self, number, text, x, y, tx, ty, *, width=280):
        """A numbered label with a precise target dot and orthogonal leader."""
        self.path(f'M{x+14} {y+26}V{ty}H{tx}', stroke=COLORS['muted'])
        self.circle(tx, ty, 3, fill=COLORS['ink'], sw=0)
        self.circle(x+14, y+13, 13, fill=COLORS['accent'], sw=0)
        self.text(number, x+8, y+1, size=17, width=20, weight=600)
        self.text(text, x+36, y-1, width=width, size=18, weight=600)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" font-family="IBM Plex Sans" fill="{COLORS["ink"]}">' + ''.join(self.items) + '</svg>'
        path.write_text(content, encoding='utf-8')
        return path
