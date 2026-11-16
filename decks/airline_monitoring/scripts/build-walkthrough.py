"""Assemble a captioned guide from verified deck captures; no workshop runs."""

import argparse
import hashlib
import html
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


DECK = Path(__file__).resolve().parents[1]
OUT = DECK / "public" / "walkthrough"
SCENES = [
    ("002.png", "passenger-request", "Read the passenger's request", 16,
     "This is a simulated booking from the pinned tau-bench data. Change the outward flight, keep the return, and obtain confirmation before writing.", "illustrated source booking"),
    ("004.png", "replace-semantics", "Understand the booking API", 14,
     "The update replaces the whole flight list. A successful call does not establish that the list still contains every flight the passenger wanted.", "documented API behavior"),
    ("015.png", "capture-conversation", "Inspect a real tool error", 18,
     "This saved discovery run contains a reservation-read timeout. Read the arguments and error in Agent Lens. No booking change had occurred at this point.", "native rehearsal capture"),
    ("016.png", "capture-recovery", "Follow the recovery", 16,
     "The next read succeeded. The same conversation ultimately passed its booking checks. An error span alone would mislabel this request as an unresolved failure.", "native rehearsal capture"),
    ("019-click-3.png", "insights", "Check whether Insights is available", 16,
     "The prepared project had no completed native clustering run at qualification. This diagram explains the intended investigation; it is not a screenshot of a completed cluster.", "workflow explanation; native prerequisite unavailable"),
    ("027.png", "capture-tag-configuration", "Scope and save the monitoring rule", 18,
     "The recorded tag targets one workshop agent. Its criteria ask whether a change was unrequested, rather than counting flights. Participants create a separate tag in their own project.", "native rehearsal capture"),
    ("031.png", "capture-alignment", "Separate the review from the judge result", 20,
     "Expected result is the human review. Native Alignment tests returned HTTP 500 and supplied no judge outcome. Precision and recall cannot be claimed from these saved labels alone.", "native rehearsal capture; judge unavailable"),
    ("038.png", "live-missingness", "Keep unprocessed turns visible", 16,
     "A missing live tag can mean the turn is unprocessed or the judge was unavailable. Do not count it as a correct negative. Coverage and agreement use different denominators.", "monitoring logic"),
    ("040-click-3.png", "curation", "Turn a reviewed event into a test", 18,
     "Save the original booking, request, policy, expected behavior, and source turn. Replaying only the final booking would test the aftermath instead of reproducing the incident.", "regression-case construction"),
    ("050-click-4.png", "range-values", "Preserve flights outside the requested range", 18,
     "The repair keeps the prefix and suffix around the replaced range. The local omission drill demonstrates this repair. It is separate from the actual model's live behavior.", "explicitly simplified local repair example"),
    ("058.png", "capture-evaltables", "Compare matching requests in EvalTables", 18,
     "The native development comparison aligns four requests per version. Both versions passed all four. Open a row to inspect its booking state and trace before explaining a score.", "native rehearsal capture; development comparison"),
    ("060.png", "recorded-results", "Report the observed tie", 18,
     "The recorded final comparison passed six of six requests for both versions. Subsequent traffic passed four of four for both. The rehearsal does not establish a live quality improvement.", "recorded qualification outcomes"),
    ("066.png", "report", "Save the conclusion and stop automatic judging", 16,
     "Publish the saved comparisons and your conclusion, then verify that automatic tagging is off. The workshop remains a technical preview until native access and participant rehearsal pass.", "participant completion instructions"),
]


def timestamp(seconds, comma=False):
    hours, rest = divmod(seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}" + (",000" if comma else ".000")


def page(scenes):
    data = json.dumps(scenes).replace("</", "<\\/")
    transcript = "".join(
        f'<li><strong>{html.escape(s["title"])}</strong> — {html.escape(s["caption"])}</li>'
        for s in scenes
    )
    return '''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Airline monitoring — recorded guide</title>
<style>
:root { color-scheme: light dark; --paper:#f7f3e9; --ink:#173d3a; --line:#a7b7ae; }
* { box-sizing:border-box; } body { margin:0; background:var(--paper); color:var(--ink); font:18px/1.5 system-ui,sans-serif; }
main { max-width:1280px; margin:auto; padding:24px; } h1 { font-size:30px; line-height:1.2; margin:0 0 12px; } h2 { font-size:22px; }
p { max-width:90ch; } .label { text-transform:uppercase; letter-spacing:.06em; font-size:13px; }
figure { margin:20px 0 12px; } img,video { width:100%; height:auto; display:block; border:1px solid var(--line); background:#f7f3e9; }
figcaption { padding:16px 0 0; min-height:5em; font-size:20px; } nav { display:flex; flex-wrap:wrap; align-items:center; gap:12px; }
button,select { font:inherit; color:inherit; background:var(--paper); border:2px solid var(--line); border-radius:6px; padding:8px 14px; }
select { flex:1; min-width:180px; max-width:100%; } button:not(:disabled) { cursor:pointer; } button:disabled { opacity:.45; }
:focus-visible { outline:3px solid #007d80; outline-offset:4px; } a { color:inherit; text-underline-offset:3px; }
.details { border-top:1px solid var(--line); margin-top:24px; padding-top:16px; } .status { font-size:15px; }
li { margin:12px 0; } @media(max-width:600px) { main {padding:16px;} h1 {font-size:25px;} figcaption {font-size:17px;} }
@media(prefers-color-scheme:dark) { :root {--paper:#182a29;--ink:#f3f2e9;--line:#74928b;} }
</style>
<main>
<p class="label">Recorded guide from saved rehearsal screens</p>
<h1>Monitor an airline service agent and build better evaluations</h1>
<p>Follow the request, its trace, the monitoring rule, and the matching evaluation. These are saved diagrams and actual Forge captures, not a recording of live clicks. No model calls or publication run when you open this guide.</p>
<p><a href="https://ash0ts.github.io/forge-workshop-kit/packet/start/airline_monitoring.html">Download and start the current notebook</a> · <a href="https://github.com/ash0ts/forge-workshop-kit">Source and laptop setup</a></p>
<p class="status"><strong>Technical preview.</strong> Native Alignment returned no completed judge results, and prepared Insights had no completed cluster. The recorded agent comparison was a tie.</p>
<nav aria-label="Guide chapters"><button id="back">Back</button><select id="chapters" aria-label="Select chapter"></select><button id="next">Next</button></nav>
<figure><img id="screen" alt=""><figcaption id="caption" aria-live="polite"></figcaption></figure>
<p class="status"><span id="evidence"></span> · <a id="slide" href="../">Open this deck explanation</a></p>
<p class="status">Arrow keys change chapters. Home returns to the beginning; End opens the last chapter. Nothing plays automatically.</p>
<details class="details"><summary>Play or download the captioned video</summary>
<p>The silent video uses the same screens, with captions below the captured content. Pause whenever you need more time.</p>
<video controls preload="none" poster="frames/01.png"><source src="airline-monitoring-recorded-guide.mp4" type="video/mp4"><track kind="captions" src="captions.vtt" srclang="en" label="English"></video>
<p><a href="airline-monitoring-recorded-guide.mp4" download>Download the video</a> · <a href="captions.vtt" download>Download captions</a> · <a href="guide.json">View sources and capture hashes</a></p>
</details>
<details class="details"><summary>Read the complete transcript</summary><ol>''' + transcript + '''</ol></details>
</main>
<script>
const scenes = ''' + data + ''';
const chapters = document.getElementById('chapters');
scenes.forEach((s,i) => { const o=document.createElement('option'); o.value=i; o.textContent=`${i+1}. ${s.title}`; chapters.append(o); });
let current=0;
function show(index) { current=Math.max(0,Math.min(scenes.length-1,index)); const s=scenes[current];
  document.getElementById('screen').src=s.image; document.getElementById('screen').alt=s.title+'. '+s.caption;
  document.getElementById('caption').textContent=s.caption; document.getElementById('evidence').textContent=s.evidence;
  document.getElementById('slide').href='../'+s.slide+'/'; chapters.value=current;
  document.getElementById('back').disabled=current===0; document.getElementById('next').disabled=current===scenes.length-1;
  history.replaceState(null,'','#chapter-'+(current+1)); }
chapters.addEventListener('change',()=>show(Number(chapters.value)));
document.getElementById('back').addEventListener('click',()=>show(current-1));
document.getElementById('next').addEventListener('click',()=>show(current+1));
document.addEventListener('keydown',e=>{ if(['SELECT','INPUT','TEXTAREA','VIDEO'].includes(e.target.tagName))return;
 const actions={ArrowRight:current+1,ArrowLeft:current-1,Home:0,End:scenes.length-1};
 if(e.key in actions){e.preventDefault();show(actions[e.key]);} });
show((Number(location.hash.replace('#chapter-',''))||1)-1);
</script></html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", default="/Library/Fonts/Arial Unicode.ttf")
    parser.add_argument("--skip-video", action="store_true")
    args = parser.parse_args()
    shots = DECK / ".screenshots"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "frames").mkdir(exist_ok=True)
    layout = json.loads((DECK / "notes/slide-index.json").read_text())
    sources = {s["name"]: s["slide"] for s in layout}
    guide, elapsed, vtt = [], 0, "WEBVTT\n\n"
    for index, (capture, anchor, title, duration, caption, evidence) in enumerate(SCENES, 1):
        source = shots / capture
        destination = OUT / "frames" / f"{index:02}.png"
        shutil.copyfile(source, destination)
        row = {"title": title, "caption": caption, "evidence": evidence, "seconds": duration,
               "start_seconds": elapsed, "slide": sources[anchor], "anchor": anchor,
               "image": f"frames/{index:02}.png", "capture_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
        guide.append(row)
        vtt += f"{timestamp(elapsed)} --> {timestamp(elapsed+duration)}\n{caption}\n\n"
        elapsed += duration
    (OUT / "guide.json").write_text(json.dumps({"kind": "captioned guide assembled from saved rehearsal captures", "seconds": elapsed,
        "limitations": ["Not a recording of live user interactions", "Native Alignment unavailable at qualification", "No completed prepared Insights cluster", "Recorded final agent comparison tied at 6/6"],
        "deck_source_sha256": hashlib.sha256((DECK / "slides.md").read_bytes()).hexdigest(), "scenes": guide}, indent=2)+"\n")
    (OUT / "captions.vtt").write_text(vtt.rstrip()+"\n")
    (OUT / "index.html").write_text(page(guide))
    if args.skip_video:
        return
    font = Path(args.font).resolve()
    if not font.is_file():
        raise SystemExit("Supply a locally installed font with --font.")
    from PIL import Image, ImageChops, ImageDraw, ImageFont

    caption_font = ImageFont.truetype(str(font), 24)
    label_font = ImageFont.truetype(str(font), 14)
    with tempfile.TemporaryDirectory(prefix="airline-guide-") as temporary:
        tmp = Path(temporary)
        playlist = []
        for index, row in enumerate(guide, 1):
            frame = tmp / f"{index:02}.png"
            original = Image.open(OUT / row["image"]).convert("RGB")
            if original.size != (1280, 720):
                raise ValueError(f"Unexpected source capture size: {original.size}")
            canvas = Image.new("RGB", (1280, 880), "#173d3a")
            canvas.paste(original, (0, 0))
            draw = ImageDraw.Draw(canvas)
            draw.text((36, 730), "RECORDED GUIDE / SAVED REHEARSAL SCREENS", font=label_font, fill="#a9c5bb")
            lines, line = [], ""
            for word in row["caption"].split():
                candidate = (line + " " + word).strip()
                if draw.textlength(candidate, font=caption_font) > 1208:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
            if len(lines) > 3:
                raise ValueError(f"Caption exceeds three lines: {row['title']}")
            draw.multiline_text((36, 758), "\n".join(lines), font=caption_font, fill="white", spacing=9)
            if ImageChops.difference(original, canvas.crop((0, 0, 1280, 720))).getbbox():
                raise AssertionError("Caption rendering changed the source capture")
            canvas.save(frame)
            playlist.extend([f"file '{frame}'", f"duration {row['seconds']}"])
        playlist.append(f"file '{frame}'")
        concat = tmp / "frames.txt"
        concat.write_text("\n".join(playlist)+"\n")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
            "-t", str(elapsed), "-r", "15", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(OUT / "airline-monitoring-recorded-guide.mp4")], check=True)
    print(json.dumps({"chapters": len(guide), "seconds": elapsed, "output": str(OUT)}))


if __name__ == "__main__":
    main()
