"""Caption the recorded browser walkthrough without covering the notebook."""
from pathlib import Path
import json
import subprocess
import textwrap
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PREFIX = sys.argv[1] if len(sys.argv) > 1 else "worked-example"
if PREFIX not in {"worked-example", "recorded-result"}:
    raise ValueError("Choose worked-example or recorded-result")
REPLAY = PREFIX == "recorded-result"
RAW = ROOT / (".screenshots/replay-raw" if REPLAY else ".screenshots/walkthrough-raw")
OUT = ROOT / "public/walkthrough"
OUT.mkdir(parents=True, exist_ok=True)
STRIPS = RAW / "captions"
STRIPS.mkdir(exist_ok=True)
captions = json.loads((RAW / "local-segment-captions.json").read_text())
duration = float(subprocess.check_output([
    "/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries",
    "format=duration", "-of", "default=nw=1:nk=1",
    str(RAW / "local-segment.webm")
]))
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font = ImageFont.truetype(font_path, 30)
label_font = ImageFont.truetype(font_path, 17)

def stamp(seconds, separator="."):
    millis = round(seconds * 1000)
    return f"{millis//3600000:02}:{millis//60000%60:02}:{millis//1000%60:02}{separator}{millis%1000:03}"

vtt = ["WEBVTT", ""]
srt = []
segments = []
at = 0.0
for i, row in enumerate(captions, 1):
    if row["start"] > at:
        segments.append((row["start"] - at, ""))
    segments.append((row["end"] - row["start"], row["text"]))
    at = row["end"]
    vtt.extend([f'{stamp(row["start"])} --> {stamp(row["end"])}', row["text"], ""])
    srt.extend([str(i), f'{stamp(row["start"], ",")} --> {stamp(row["end"], ",")}', row["text"], ""])
if duration > at:
    segments.append((duration - at, ""))
concat = []
for i, (seconds, caption) in enumerate(segments):
    image = Image.new("RGB", (1600, 140), "#122c30")
    draw = ImageDraw.Draw(image)
    header = "TRANSIT WORKSHOP  /  RECORDED R4 RESULTS  /  NO NEW MODEL CALLS" if REPLAY else "TRANSIT WORKSHOP  /  WORKED EXAMPLE  /  NO MODEL CALLS"
    draw.text((34, 15), header, font=label_font, fill="#8ccec6")
    lines = textwrap.wrap(caption, width=98)
    for j, line in enumerate(lines):
        draw.text((34, 47 + j * 38), line, font=font, fill="#fff8e9")
    path = STRIPS / f"{i:03}.png"
    image.save(path)
    concat.extend([f"file '{path}'", f"duration {seconds:.3f}"])
concat.append(f"file '{path}'")
(STRIPS / "frames.txt").write_text("\n".join(concat) + "\n")
(OUT / f"{PREFIX}.vtt").write_text("\n".join(vtt))
(OUT / f"{PREFIX}.srt").write_text("\n".join(srt))
subprocess.run([
    "/opt/homebrew/bin/ffmpeg", "-y", "-i", str(RAW / "local-segment.webm"),
    "-f", "concat", "-safe", "0", "-i", str(STRIPS / "frames.txt"),
    "-filter_complex", "[0:v]pad=1600:1140:0:0:color=0x122c30[base];[base][1:v]overlay=0:1000:shortest=1[v]",
    "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
    "-pix_fmt", "yuv420p", "-r", "25", "-t", str(duration),
    "-movflags", "+faststart", str(OUT / f"{PREFIX}.mp4")
], check=True)
receipt_path = OUT / ("recorded-result-receipt.json" if REPLAY else "recording-receipt.json")
existing = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
receipt_path.write_text(json.dumps({
    **existing,
    "kind": "Actual browser recording with captions placed below the unaltered viewport",
    "source": "scripts/record-replay.mjs" if REPLAY else "scripts/record-walkthrough.mjs",
    "duration_seconds": duration,
    "paid_calls": 0,
    "live_agent_execution": False,
    "content": ["Saved R4 task board and actual patch", "Matching Agent Lens evidence", "Native aligned evaluations", "Actual R4 team first-release app"] if REPLAY else ["Notebook code edits", "Free acceptance, dispatch, claims, memory and scoring checks", "Reference app using real historical MBTA rows"],
    "limitations": "Replay of saved R4 executions, not a new live build. Both first builds passed 10/10; both follow-ups scored 14/18 after context-bound query failures. No memory advantage was established." if REPLAY else "This worked-example segment does not demonstrate live worker inference or an agent-produced application. Native rehearsal evidence is separate."
}, indent=2) + "\n")
print(OUT / f"{PREFIX}.mp4")
