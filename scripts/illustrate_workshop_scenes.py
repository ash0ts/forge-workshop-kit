"""Draw editable, illustrative workshop settings without network or model calls."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "visual-guides/scenes"
ASSETS = ROOT / "skills/teenage-engineering-visualizations/assets"
TOKENS = json.loads((ASSETS / "tokens.json").read_text(encoding="utf-8"))
C = TOKENS["colors"]
# The explicit scene reference uses these original pixel-office material colors.
M = {
    "edge": "#183d43", "wall": "#c2cdbd", "floor": "#e7e0cf",
    "tile": "#cfc5b0", "wood": "#af7955", "wood_dark": "#715545",
    "glass": "#dcebe5", "screen": "#eef2df", "green": "#4e8b70",
    "green_dark": "#295c50", "gold": "#e8bc57", "cream": "#fff4d0",
    "blue": "#497d9a", "rust": "#b86647", "skin": "#e7b28a",
    "skin_dark": "#bd886e", "hair": "#293d40", "night": "#244557",
}
STAGES = ("start", "inspect", "build", "compare", "release")
FONT_FILES = (("IBM Plex Sans", 400, "sans-latin-400"),
              ("IBM Plex Sans", 600, "sans-latin-600"),
              ("IBM Plex Mono", 400, "mono-latin-400"))


def embedded_fonts():
    rules = []
    for family, weight, stem in FONT_FILES:
        data = (ASSETS / "fonts" / f"ibm-plex-{stem}-normal.woff2").read_bytes()
        rules.append(f"@font-face{{font-family:'{family}';font-weight:{weight};"
                     f"src:url(data:font/woff2;base64,{base64.b64encode(data).decode()})}}")
    return "".join(rules)


class Scene:
    def __init__(self, slug, title, stage, fonts):
        self.slug, self.stage = slug, stage
        self.objects = []
        self.a = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" '
                  f'role="img" aria-labelledby="{slug}-{stage["id"]}-title {slug}-{stage["id"]}-desc" data-workshop="{slug}" '
                  f'data-stage="{stage["id"]}">',
                  f'<title id="{slug}-{stage["id"]}-title">{html.escape(title + ": " + stage["label"])}</title>',
                  f'<desc id="{slug}-{stage["id"]}-desc">{html.escape(stage["caption"])} '
                  'Original illustrative setting; it does not show an executed experiment.</desc>',
                  f'<defs><style>{fonts}</style></defs>']
        self.rect(0, 0, 1200, 675, C["paper"])
        self.text(32, 43, title, 30, weight=600)
        self.text(1168, 43, stage["label"], 26, anchor="end")

    def rect(self, x, y, w, h, fill, stroke=None, sw=3):
        self.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                      f'fill="{fill}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')

    def path(self, d, fill="none", stroke=None, sw=3, dash=None):
        self.a.append(f'<path d="{d}" fill="{fill}" stroke="{stroke or M["edge"]}" '
                      f'stroke-width="{sw}" stroke-linejoin="miter"'
                      + (f' stroke-dasharray="{dash}"' if dash else "") + '/>')

    def line(self, x1, y1, x2, y2, color=None, sw=3):
        self.path(f'M{x1} {y1}H{x2}' if y1 == y2 else f'M{x1} {y1}L{x2} {y2}',
                  stroke=color, sw=sw)

    def text(self, x, y, text, size=24, color=None, mono=False, weight=400, anchor="start"):
        self.a.append(f'<text x="{x}" y="{y}" font-family="IBM Plex {"Mono" if mono else "Sans"}" '
                      f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
                      f'fill="{color or M["edge"]}">{html.escape(str(text))}</text>')

    def circle(self, x, y, r, fill, stroke=None, sw=3):
        self.a.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" '
                      f'stroke="{stroke or "none"}" stroke-width="{sw}"/>')

    def image(self, x, y, w, h, uri):
        self.a.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{uri}"/>')

    def room(self, sign, wall=None):
        self.rect(34, 78, 1132, 496, M["floor"], M["edge"], 7)
        self.rect(34, 78, 1132, 104, wall or M["wall"], M["edge"], 7)
        for x in range(62, 1166, 48):
            self.line(x, 186, x, 571, M["tile"], 1)
        for y in range(218, 572, 44):
            self.line(38, y, 1162, y, M["tile"], 1)
        self.rect(62, 104, 350, 46, M["edge"])
        self.text(80, 136, sign, 26, M["cream"], mono=True)

    def desk(self, x, y, w):
        self.rect(x + 10, y + 24, 18, 92, M["wood_dark"])
        self.rect(x + w - 28, y + 24, 18, 92, M["wood_dark"])
        self.rect(x, y, w, 27, M["wood"], M["edge"], 3)
        self.rect(x, y, w, 7, "#c7966b")

    def monitor(self, x, y, w, h, label, screen=None):
        self.rect(x + w / 2 - 12, y + h, 24, 20, M["edge"])
        self.rect(x + w / 2 - 42, y + h + 17, 84, 9, M["edge"])
        self.rect(x, y, w, h, M["edge"])
        self.rect(x + 9, y + 9, w - 18, h - 18, screen or M["screen"])
        self.text(x + 17, y + 38, label, 24, mono=True)

    def keyboard(self, x, y, w=150):
        self.rect(x, y, w, 23, M["edge"])
        for row in range(2):
            for col in range(int((w - 10) / 13)):
                self.rect(x + 6 + col * 13, y + 5 + row * 8, 9, 5, M["glass"])

    def worker(self, x, y, shirt=None, skin=None, headset=False):
        self.rect(x + 2, y + 56, 88, 70, M["wood_dark"])
        self.rect(x + 22, y + 12, 54, 58, skin or M["skin"])
        self.rect(x + 16, y, 66, 22, M["hair"])
        self.rect(x + 16, y + 18, 12, 30, M["hair"])
        self.rect(x + 64, y + 32, 7, 7, M["hair"])
        self.rect(x + 6, y + 70, 92, 51, shirt or M["blue"])
        self.rect(x + 22, y + 121, 20, 31, M["hair"])
        self.rect(x + 65, y + 121, 20, 31, M["hair"])
        if headset:
            self.path(f'M{x+10} {y+44}V{y+4}H{x+88}V{y+44}', stroke=M["edge"], sw=8)
            self.rect(x + 1, y + 35, 18, 28, M["edge"])
            self.rect(x + 79, y + 35, 18, 28, M["edge"])
            self.path(f'M{x+91} {y+53}V{y+64}H{x+66}', stroke=M["edge"], sw=5)

    def paper(self, x, y, w, h, label, color=None, ruled=True):
        self.path(f'M{x} {y}H{x+w-18}L{x+w} {y+18}V{y+h}H{x}Z',
                  color or M["cream"], M["edge"], 3)
        self.path(f'M{x+w-18} {y}V{y+18}H{x+w}', stroke=M["edge"], sw=2)
        self.text(x + 12, y + 35, label, 24, mono=True)
        for offset in (52, 68, 84):
            if ruled and offset < h - 12:
                self.line(x + 12, y + offset, x + w - 16, y + offset, M["green"], 4)

    def cupboard(self, x, y, w, h, opened=False):
        self.rect(x, y, w, h, M["green_dark"], M["edge"], 4)
        for offset in (10, h / 2 + 5):
            self.rect(x + 8, y + offset, w - 16, h / 2 - 15, M["wall"], M["edge"], 3)
            self.rect(x + w / 2 - 19, y + offset + 12, 38, 8, M["edge"])
        if opened:
            self.rect(x - 12, y + h / 2, w + 24, h / 2 - 8, M["wood"], M["edge"], 3)
            self.paper(x + 18, y + h / 2 - 48, w - 36, 82, "SAVED")

    def object(self, identifier, bounds, pin):
        self.objects.append({"id": identifier, "bounds": list(bounds), "pin": list(pin)})

    def finish(self):
        target = next(o for o in self.objects if o["id"] == self.stage["active_object"])
        x, y, w, h = target["bounds"]
        px, py = target["pin"]
        self.rect(x - 6, y - 6, w + 12, h + 12, "none", C["accent"], 5)
        self.line(px, py + 19, px, y - 6, C["accent"], 4)
        self.circle(px, py, 21, C["accent"], M["edge"], 2)
        self.text(px, py + 9, self.stage["number"], 27, C["white"], weight=600, anchor="middle")
        self.circle(53, 614, 21, C["accent"])
        self.text(53, 623, self.stage["number"], 27, C["white"], weight=600, anchor="middle")
        self.text(88, 623, self.stage["caption"], 27)
        self.text(32, 661, "Illustrated workshop setting", 24, C["muted"])
        return "".join(self.a) + "</svg>"


def pending(s, k):
    s.room("PENDING, INC.")
    s.rect(948, 96, 174, 69, M["glass"], M["edge"], 5)
    s.line(1035, 98, 1035, 164, M["edge"], 4)
    s.line(950, 131, 1120, 131, M["edge"], 4)
    s.desk(84, 366, 455)
    s.monitor(102, 207, 237, 129, "EMPLOYEE")
    s.text(120, 282, "lookup_invoice" if k >= 2 else "task waiting", 24, mono=True)
    if k >= 2:
        s.line(121, 309, 302, 309, M["green"], 7)
    s.keyboard(132, 341, 186)
    s.paper(369, 224, 132, 139, "TASK")
    s.worker(226, 413, M["blue"])
    s.desk(623, 366, 434)
    if k >= 1:
        s.path('M644 239H742L756 250L770 239H868V353H770L756 364L742 353H644Z', M["gold"], M["edge"], 4)
        s.line(756, 251, 756, 354, M["edge"], 3)
        for y in (281, 303, 325):
            s.line(658, y, 730, y, M["wood_dark"], 5)
            s.line(782, y, 853, y, C["accent"] if k >= 2 and y == 303 else M["wood_dark"], 5)
    else:
        s.rect(674, 240, 162, 113, M["gold"], M["edge"], 4)
        s.text(688, 284, "HANDBOOK", 24, mono=True)
        s.line(689, 305, 817, 305, M["wood_dark"], 5)
    s.worker(683, 413, M["rust"], M["skin_dark"])
    s.text(350, 490, "EMPLOYEE", 24, mono=True)
    s.text(798, 490, "EDITOR", 24, mono=True)
    s.cupboard(916, 401, 160, 145, k >= 4)
    s.paper(921, 231, 122, 124, "TRACE")
    for y, label, fill in ((196, "BASE", M["cream"]), (251, "MANUAL", M["glass"]), (306, "AGENT", M["wall"])):
        s.rect(516, y, 110, 45, fill, M["edge"], 3)
        if k >= 3:
            s.text(571, y + 31, label, 24, mono=True, anchor="middle")
        else:
            s.line(529, y + 23, 613, y + 23, M["tile"], 5)
    s.object("task", (366, 220, 138, 145), (435, 196))
    s.object("handbook", (640, 235, 232, 129), (756, 208))
    s.object("employee-terminal", (98, 203, 245, 137), (215, 179))
    s.object("handbook-versions", (512, 192, 118, 163), (571, 168))
    s.object("saved-trace", (908, 390, 176, 163), (996, 366))


def solar(s, k):
    observation = json.loads((OUTPUT / "solar-observation.json").read_text(encoding="utf-8"))
    s.room("SOLAR ARCHIVE", "#bbcbd0")
    # The observation is measured. The surrounding room and process are drawn.
    s.rect(919, 98, 203, 66, M["night"], M["edge"], 4)
    s.path('M951 153V134H962V121H980V112H1013V121H1031V134H1043V153Z', M["glass"], M["edge"], 3)
    s.line(995, 112, 995, 153, M["edge"], 4)
    s.rect(1080, 115, 6, 6, M["cream"])
    s.rect(1101, 139, 6, 6, M["cream"])
    s.desk(67, 409, 794)
    s.monitor(88, 205, 230, 173, "AIA ARCHIVE", M["night"])
    s.rect(97, 214, 212, 36, M["edge"])
    s.text(106, 241, "AIA ARCHIVE", 24, M["cream"], mono=True)
    s.image(138, 252, 116, 116, observation["aia_uri"])
    s.monitor(363, 211, 270, 167, "GOES HISTORY")
    values = observation["xrsb_history"]
    lo, hi = min(values), max(values)
    points = [(382 + i * 230 / (len(values) - 1), 350 - (v - lo) / (hi - lo) * 75) for i, v in enumerate(values)]
    s.path("M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in points), stroke=M["green_dark"], sw=4)
    if k >= 1:
        s.rect(381, 266, 231, 88, "none", C["accent"], 3)
        s.line(612, 263, 612, 361, C["accent"], 3)
    s.keyboard(422, 383, 171)
    s.text(81, 465, "Recorded observations", 24)
    s.worker(423, 417, M["green"], M["skin_dark"])
    s.monitor(682, 258, 158, 120, "SOURCE")
    for row, width in enumerate((119, 82, 105, 65)):
        s.line(697, 313 + row * 14, 697 + width, 313 + row * 14, M["green"] if k >= 2 else M["tile"], 5)
    s.text(550, 511, "RESEARCHER", 24, mono=True)
    s.rect(903, 204, 217, 126, M["wall"], M["edge"], 4)
    s.paper(913, 219, 91, 96, "BASE")
    s.paper(1017, 219, 91, 96, "EDIT")
    if k >= 1:
        s.line(925, 286, 992, 286, M["blue"], 6)
        s.line(1029, 286, 1096, 286, M["rust"], 6)
    if k >= 3:
        s.rect(959, 312, 108, 33, M["edge"])
        s.text(1013, 338, "FROZEN", 24, M["cream"], mono=True, anchor="middle")
    s.cupboard(919, 383, 184, 164, k >= 4)
    s.object("observations", (84, 201, 238, 181), (204, 177))
    s.object("history-window", (359, 207, 278, 175), (499, 183))
    s.object("research-editor", (678, 254, 166, 128), (761, 230))
    s.object("experiment-comparison", (899, 200, 225, 154), (1011, 176))
    s.object("saved-experiment", (907, 375, 208, 178), (1107, 351))


def routing(s, k):
    s.room("SUPPORT DESK", "#c3cbd8")
    # Queue lanes are labels, not performance measurements.
    s.rect(613, 99, 510, 70, M["edge"])
    for j, lines in enumerate((("CARD", "ARRIVAL"), ("CARD", "NOT WORKING"), ("PENDING", "TRANSFER"))):
        s.text(625 + 168 * j, 128, lines[0], 24, M["cream"], mono=True)
        s.text(625 + 168 * j, 157, lines[1], 24, M["gold"], mono=True)
    s.desk(84, 388, 735)
    s.monitor(111, 218, 253, 139, "INBOX")
    for j in range(3):
        s.rect(127, 267 + j * 24, 218, 17, M["glass"], M["green"], 2)
        s.rect(134, 272 + j * 24, 10, 7, M["gold"])
        s.line(153, 276 + j * 24, 322, 276 + j * 24, M["green"], 3)
    s.keyboard(143, 363, 178)
    s.worker(201, 414, M["blue"], headset=True)
    s.paper(403, 239, 175, 140, "REQUEST")
    s.paper(321, 434, 128, 101, "BRIEF")
    if k >= 1:
        s.rect(416, 297, 145, 31, M["gold"])
        s.text(425, 321, "card help", 24)
    s.monitor(614, 224, 181, 133, "ROUTER")
    if k >= 2:
        for j in range(3):
            s.rect(632, 277 + j * 24, 17, 13, M["blue"])
            s.line(657, 283 + j * 24, 775, 283 + j * 24, M["green"], 5)
    else:
        for j in range(3):
            s.line(632, 283 + j * 24, 775, 283 + j * 24, M["tile"], 5)
    s.rect(871, 236, 241, 124, M["wood"], M["edge"], 4)
    s.paper(884, 246, 103, 99, "CASE")
    s.paper(997, 246, 103, 99, "LABEL")
    if k >= 2:
        s.line(895, 312, 975, 312, C["accent"], 6)
        s.line(1008, 312, 1088, 312, C["accent"], 6)
    if k >= 3:
        s.rect(954, 331, 79, 34, M["edge"])
        s.text(993, 357, "FIXED", 24, M["cream"], mono=True, anchor="middle")
    s.cupboard(886, 405, 211, 142, k >= 4)
    s.text(478, 490, "MANAGER", 24, mono=True)
    s.object("incoming-request", (107, 214, 261, 147), (237, 190))
    s.object("request-text", (399, 235, 183, 148), (490, 211))
    s.object("manager-brief", (313, 426, 144, 117), (385, 402))
    s.object("router", (610, 220, 189, 141), (704, 196))
    s.object("reviewed-case", (867, 232, 249, 132), (991, 208))
    s.object("label-bundle", (874, 397, 235, 156), (1100, 373))


def circuit_board(s, x, y, w, h):
    s.rect(x, y, w, h, M["green"], M["edge"], 4)
    for j in range(8):
        s.rect(x + 15 + j * (w - 34) / 8, y + h, 10, 19, M["gold"])
    for j in range(3):
        yy = y + 25 + j * 30
        s.path(f'M{x+13} {yy}H{x+48+j*10}V{yy+15}H{x+w-16}', stroke=M["gold"], sw=3)
    for xx in (x + 40, x + w - 91):
        s.rect(xx, y + 34, 51, 61, M["edge"])
        for j in range(5):
            s.rect(xx - 8, y + 39 + j * 11, 8, 4, M["cream"])
            s.rect(xx + 51, y + 39 + j * 11, 8, 4, M["cream"])
    for xx, yy in ((x + 12, y + 12), (x + w - 22, y + 12), (x + 12, y + h - 22), (x + w - 22, y + h - 22)):
        s.circle(xx + 5, yy + 5, 5, M["cream"], M["edge"], 2)


def inspection(s, k):
    s.room("PCB INSPECTION", "#cbd1be")
    # A pegboard and articulated magnifier distinguish a physical inspection bench.
    for x in range(466, 1120, 36):
        for y in (107, 142):
            s.rect(x, y, 5, 5, M["green_dark"])
    s.desk(76, 397, 1038)
    s.rect(93, 363, 331, 31, M["blue"], M["edge"], 3)
    circuit_board(s, 125, 236, 248, 127)
    s.rect(406, 365, 49, 27, M["edge"])
    s.path('M431 366V307L468 245L415 207', stroke=M["edge"], sw=11)
    s.circle(381, 206, 51, M["glass"], M["edge"], 8)
    if k >= 1:
        s.path('M348 193H371V214H408M355 224H389V182', stroke=M["gold"], sw=8)
        s.rect(369, 194, 26, 28, M["edge"])
    s.monitor(522, 226, 256, 140, "PATCH VIEW")
    if k >= 2:
        for row in range(5):
            for col in range(10):
                s.rect(540 + col * 22, 277 + row * 15, 18, 11,
                       M["gold"] if (row, col) == (3, 4) else M["green"])
    else:
        s.rect(541, 278, 219, 70, M["glass"])
        s.path('M565 313H735', stroke=M["green"], sw=6)
    s.keyboard(573, 372, 154)
    s.worker(568, 418, M["green"], M["skin_dark"])
    s.paper(835, 239, 118, 140, "048", ruled=False)
    s.paper(979, 239, 118, 140, "015", ruled=False)
    if k >= 3:
        for x, before, after in ((849, "MISS", "FLAG"), (993, "FLAG", "MISS")):
            s.text(x, 308, before, 24, mono=True)
            s.path(f'M{x+35} 315V333L{x+28} 326M{x+35} 333L{x+42} 326', stroke=M["edge"], sw=3)
            s.text(x, 364, after, 24, mono=True)
    s.text(434, 516, "REVIEWER", 24, mono=True)
    s.paper(735, 443, 214, 105, "ASSESSMENT", ruled=False)
    if k >= 2:
        s.text(751, 512, "DEFECTIVE", 24, mono=True)
        s.line(751, 529, 929, 529, M["green"], 4)
    else:
        s.line(751, 512, 929, 512, M["tile"], 4)
    s.rect(144, 448, 272, 97, M["edge"])
    s.rect(158, 461, 244, 70, M["wall"])
    s.rect(247, 432, 65, 16, M["edge"])
    if k >= 4:
        s.text(174, 505, "DETECTOR", 27, mono=True)
        s.rect(365, 478, 20, 20, M["gold"])
    else:
        s.line(177, 497, 376, 497, M["green"], 6)
    s.object("circuit-board", (120, 231, 258, 156), (244, 207))
    s.object("magnified-component", (323, 148, 116, 116), (381, 124))
    s.object("patch-view", (518, 222, 264, 148), (650, 198))
    s.object("reviewer-assessment", (731, 439, 222, 113), (840, 415))
    s.object("aligned-cases", (831, 235, 270, 148), (965, 211))
    s.object("saved-detector", (140, 428, 280, 121), (280, 404))


def transit(s, k):
    s.room("TRANSIT BUILD ROOM", "#c4ccd1")
    s.rect(651, 97, 471, 72, M["edge"])
    s.text(667, 126, "DEPARTURES", 24, M["cream"], mono=True)
    for j, label in enumerate(("CENTRAL", "HARBOR", "NORTH")):
        s.text(668 + j * 150, 156, label, 24, M["gold"], mono=True)
    s.desk(79, 376, 394)
    s.desk(727, 376, 394)
    s.monitor(107, 224, 245, 121, "BUILDER A")
    s.monitor(816, 224, 245, 121, "BUILDER B")
    for x in (124, 833):
        for j, width in enumerate((168, 120, 152)):
            s.line(x, 279 + j * 22, x + width, 279 + j * 22,
                   M["green_dark"] if k >= 2 else M["tile"], 6)
    s.keyboard(153, 350, 156)
    s.keyboard(858, 350, 156)
    s.worker(195, 414, M["blue"])
    s.worker(865, 414, M["rust"], M["skin_dark"])
    s.paper(502, 223, 190, 144, "SERVICE DAY", ruled=False)
    s.text(518, 285, "BEFORE", 24, mono=True)
    s.text(518, 337, "AFTER", 24, mono=True)
    s.line(516, 299, 678, 299, C["accent"] if k >= 1 else M["tile"], 5)
    if k >= 1:
        s.path('M659 273V329L650 320M659 329L668 320', stroke=C["accent"], sw=4)
    s.rect(503, 404, 190, 137, M["wood"], M["edge"], 4)
    s.text(519, 436, "SHARED APP", 24, mono=True)
    if k >= 3:
        s.path('M526 453H564L545 480L564 509H526L545 480Z', M["gold"], M["edge"], 3)
        s.text(583, 489, "WAIT", 24, mono=True)
    else:
        for j in range(3):
            s.rect(518, 450 + j * 24, 158, 15, M["glass"])
    if k == 2:
        s.rect(101, 218, 257, 133, "none", C["accent"], 5)
    s.paper(363, 242, 96, 107, "TASK")
    s.paper(732, 242, 72, 107, "OWN")
    if k >= 4:
        s.rect(492, 532, 212, 25, M["green_dark"])
        s.text(598, 553, "LESSON SAVED", 24, M["cream"], mono=True, anchor="middle")
    s.object("service-day", (498, 219, 198, 152), (598, 195))
    s.object("midnight-boundary", (511, 264, 171, 80), (598, 240))
    s.object("owned-work", (812, 220, 253, 129), (939, 196))
    s.object("combined-board", (499, 400, 198, 145), (598, 376))
    s.object("verified-lesson", (488, 526, 220, 35), (708, 502))


def plane(s, x, y, scale=1):
    s.a.append(f'<g transform="translate({x} {y}) scale({scale})">')
    s.path('M0 44H25L58 32H102L147 2H170L147 32H219L240 45V53H147L166 81H145L101 53H57L25 66H4L30 51H0Z',
           M["cream"], M["edge"], 3)
    for xx in range(66, 206, 18):
        s.rect(xx, 39, 7, 5, M["blue"])
    s.a.append('</g>')


def airline(s, k):
    s.room("BOOKING OPERATIONS", "#bfcbd4")
    s.rect(681, 92, 449, 149, M["glass"], M["edge"], 5)
    s.line(691, 222, 1120, 222, M["tile"], 6)
    plane(s, 772, 112, 1.2)
    s.line(903, 95, 903, 238, M["edge"], 5)
    s.desk(83, 394, 588)
    s.monitor(111, 222, 248, 141, "BOOKING")
    s.text(128, 291, "OUT →", 26, mono=True)
    s.text(128, 337, "← BACK", 26, mono=True)
    s.line(253, 285, 337, 285, C["accent"] if k >= 2 else M["green"], 7)
    s.line(253, 329, 337, 329, M["green"], 7)
    s.keyboard(153, 369, 159)
    s.worker(196, 415, M["blue"], headset=True)
    s.text(348, 512, "OPERATOR", 24, mono=True)
    s.paper(406, 239, 231, 140, "ITINERARY", ruled=False)
    s.text(423, 305, "OUTBOUND", 24, mono=True)
    s.text(423, 352, "RETURN", 24, mono=True)
    if k >= 1:
        s.rect(416, 280, 208, 31, "none", C["accent"], 3)
        s.rect(416, 327, 208, 31, "none", M["green"], 3)
    s.rect(733, 287, 388, 127, M["wall"], M["edge"], 4)
    if k >= 3:
        s.text(752, 319, "REPORT", 24, mono=True)
        for j, label in enumerate(("COMPLETION", "PRECISION / RECALL", "COVERAGE / MISSING")):
            s.text(752, 348 + j * 28, label, 24, mono=True)
    else:
        s.text(752, 319, "THREE QUESTIONS", 24, mono=True)
        for j, label in enumerate(("TOOL EXECUTED?", "BOOKING CORRECT?", "MONITOR DETECTED?")):
            s.text(752, 348 + j * 28, label, 24, mono=True)
        if k == 1:
            for j in range(3):
                s.rect(1085, 331 + j * 28, 15, 15, M["gold"], M["edge"], 2)
    s.rect(753, 439, 342, 103, M["wood"], M["edge"], 4)
    for j in range(4):
        s.rect(771 + j * 76, 453, 60, 72, M["cream"], M["edge"], 2)
        s.line(782 + j * 76, 475, 821 + j * 76, 475, M["green"], 4)
        s.line(782 + j * 76, 493, 811 + j * 76, 493, M["green"], 4)
        if k >= 2:
            s.rect(783 + j * 76, 507, 25, 8, M["gold"])
    if k >= 4:
        s.rect(811, 505, 230, 34, M["green_dark"])
        s.text(926, 532, "REGRESSION CASES", 24, M["cream"], mono=True, anchor="middle")
    s.object("booking", (107, 218, 256, 149), (235, 194))
    s.object("whole-itinerary", (402, 235, 239, 148), (522, 211))
    s.object("outbound-change", (119, 265, 222, 37), (230, 241))
    s.object("monitoring-rule", (729, 283, 396, 135), (927, 259))
    s.object("regression-cases", (749, 435, 350, 111), (1098, 411))


SCENES = {
    "pending": {
        "title": "Pending, Inc.", "draw": pending,
        "stages": [
            ("Read the task", "task", "Follow one customer request into the office."),
            ("Open the handbook", "handbook", "Find the rule that should guide the employee."),
            ("Propose a handbook edit", "handbook", "The editor proposes handbook changes for review."),
            ("Freeze the comparison", "handbook-versions", "Compare Base, Manual, and Agent harnesses on the same frozen cases."),
            ("Keep the tested handbook", "saved-trace", "Keep the handbook and the traces that support it."),
        ],
    },
    "solar": {
        "title": "Solar forecasting lab", "draw": solar,
        "stages": [
            ("Read the observations", "observations", "Start with dated observations, not a forecast result."),
            ("Ask the research question", "experiment-comparison", "Can a source change improve this fixed forecasting task?"),
            ("Give the agent a workbench", "research-editor", "The research agent edits source, runs experiments, and reads evidence."),
            ("Freeze the experiment", "experiment-comparison", "Keep the data split and evaluation rules fixed for comparison."),
            ("Save the experiment", "saved-experiment", "Keep observations, source, weights, and predictions linked."),
        ],
    },
    "routing": {
        "title": "Support routing desk", "draw": routing,
        "stages": [
            ("Read a request", "incoming-request", "Follow one support request toward its intended queue."),
            ("Meet the manager", "manager-brief", "The manager turns the support problem into a research task."),
            ("Review the dataset", "reviewed-case", "Read each request beside its assigned queue label."),
            ("Freeze the comparison", "reviewed-case", "Hold the cases and label meanings fixed across candidates."),
            ("Save the label map", "label-bundle", "Package the model with its ordered queue labels."),
        ],
    },
    "inspection": {
        "title": "Circuit-board inspection", "draw": inspection,
        "stages": [
            ("Inspect the board", "circuit-board", "Follow one board from the bench into inspection."),
            ("Read the assignment", "magnified-component", "Catch defects without sending every normal board for review."),
            ("Record the human assessment", "reviewer-assessment", "Save the reviewer’s decision before revealing the supplied label."),
            ("Keep the new failure visible", "aligned-cases", "Recorded retest: 048 is recovered; 015 becomes a new miss."),
            ("Save the detector", "saved-detector", "Preserve the encoder, normal bank, and classifier."),
        ],
    },
    "transit": {
        "title": "Transit build room", "draw": transit,
        "stages": [
            ("Read the schedule", "service-day", "Two builders share one departure-board problem."),
            ("Read the request", "service-day", "The departure board must handle trips after midnight."),
            ("Split work between two builders", "owned-work", "Two builders need clear ownership and a shared test contract."),
            ("More workers can mean waiting", "combined-board", "Extra workers can wait on the same shared resource."),
            ("Save a tested lesson", "verified-lesson", "Carry a lesson forward only after checking its effect."),
        ],
    },
    "airline_monitoring": {
        "title": "Airline booking operations", "draw": airline,
        "stages": [
            ("Read the booking", "booking", "Keep both journeys visible while changing the booking."),
            ("Keep three questions separate", "monitoring-rule", "Tool execution, booking quality, and monitor detection differ."),
            ("Curate a replayable case", "regression-cases", "Keep the initial booking, request, policy, and reviewed expectation."),
            ("Report each measure", "monitoring-rule", "Report denominators and missing judgments beside each measure."),
            ("Keep regression cases", "regression-cases", "Save reviewed incidents so a repair can be tested again."),
        ],
    },
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", action="append", choices=list(SCENES))
    args = parser.parse_args()
    fonts = embedded_fonts()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    previous = json.loads((OUTPUT / "index.json").read_text(encoding="utf-8")) if (OUTPUT / "index.json").exists() else {}
    saved = {row["slug"]: row for row in previous.get("scenes", [])}
    rows = []
    generated = 0
    for slug, config in SCENES.items():
        if args.only and slug not in args.only:
            if slug in saved:
                rows.append(saved[slug])
            continue
        generated += 1
        folder = OUTPUT / slug
        folder.mkdir(exist_ok=True)
        stages = []
        for number, (identifier, data) in enumerate(zip(STAGES, config["stages"]), 1):
            label, active, caption = data
            state = {"id": identifier, "number": number, "label": label,
                     "active_object": active, "caption": caption,
                     "svg": f"{slug}/{identifier}.svg"}
            scene = Scene(slug, config["title"], state, fonts)
            config["draw"](scene, number - 1)
            svg = scene.finish()
            (folder / f"{identifier}.svg").write_text(svg, encoding="utf-8", newline="\n")
            state["alt"] = f'{config["title"]}: {caption} Illustrative setting.'
            state["callouts"] = [{"number": number, "target": active,
                                  "label": label, "caption": caption}]
            state["sha256"] = hashlib.sha256(svg.encode()).hexdigest()
            stages.append(state)
        rows.append({"slug": slug, "title": config["title"], "viewBox": [0, 0, 1200, 675],
                     "provenance": "illustrative", "objects": scene.objects, "stages": stages})
    manifest = {"schema_version": 1, "generator": "scripts/illustrate_workshop_scenes.py",
                "stage_order": list(STAGES), "fonts_embedded": True,
                "minimum_label_px": 24, "scenes": rows}
    (OUTPUT / "index.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    print(f"Rendered {generated * 5} stages for {generated} workshop settings.")


if __name__ == "__main__":
    main()
