"""Edit actual CUA browser captures into a silent, captioned workshop tour.

The edit is data in media/walkthrough/edit.json. No browser, model, training, or
publication calls occur here. Capture timestamps determine playback timing;
extra reading time is an explicit freeze of the last captured frame.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "skills/teenage-engineering-visualizations/assets"
TOKENS = json.loads((STYLE / "tokens.json").read_text(encoding="utf-8"))
C = TOKENS["colors"]
WIDTH, HEIGHT, FPS = 1920, 1080, 25
SCREEN = (160, 60, 1600, 900)
CAPTION_Y = 958


def run(command):
    subprocess.run([str(item) for item in command], check=True)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stamp(seconds, separator="."):
    milliseconds = round(seconds * 1000)
    return f"{milliseconds//3600000:02}:{milliseconds//60000%60:02}:{milliseconds//1000%60:02}{separator}{milliseconds%1000:03}"


def concat_path(path):
    return "'" + str(Path(path).resolve()).replace("'", "'\\''") + "'"


def font(output, weight, size):
    path = output / "fonts" / f"plex-{weight}.ttf"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        source = STYLE / "fonts" / f"ibm-plex-sans-latin-{weight}-normal.woff2"
        loaded = TTFont(source)
        loaded.flavor = None
        loaded.save(path)
    return ImageFont.truetype(str(path), size)


def wrap(text, draw, selected_font, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textlength(test, font=selected_font) > width and line:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def caption_image(output, text, path):
    image = Image.new("RGB", (WIDTH, HEIGHT - CAPTION_Y), C["paper"])
    draw = ImageDraw.Draw(image)
    selected_font = font(output, 400, 31)
    lines = wrap(text, draw, selected_font, 1710)
    if len(lines) > 2:
        raise ValueError(f"Caption needs more than two lines: {text}")
    draw.line([(160, 1), (1760, 1)], fill=C["line"], width=1)
    for number, line in enumerate(lines):
        draw.text(((WIDTH - draw.textlength(line, font=selected_font)) / 2, 16 + number * 39), line, font=selected_font, fill=C["ink"])
    image.save(path)


def overlay_image(output, chapter, shot, path):
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 59), fill=C["paper"])
    draw.text((160, 11), f'{chapter["number"]:02}  {chapter["title"]}', font=font(output, 600, 27), fill=C["ink"])
    label = shot["label"]
    selected_font = font(output, 400, 20)
    draw.text((1760 - draw.textlength(label, font=selected_font), 16), label, font=selected_font, fill=C["muted"])
    draw.line((160, 52, 1760, 52), fill=C["line"], width=1)
    draw.rectangle((0, CAPTION_Y, WIDTH, HEIGHT), fill=C["paper"])
    image.save(path)


def cue_rows(manifest):
    """Keep each explanation inside the shot that actually shows its subject."""
    cues = []
    for chapter in manifest["chapters"]:
        shot_start = chapter["start"]
        for shot_index, shot in enumerate(chapter["shots"]):
            chunks = shot["narration"]
            total_words = sum(len(chunk.split()) for chunk in chunks)
            available = shot["duration"] - 1
            if total_words / available * 60 > 180:
                raise ValueError(f'{chapter["id"]}/{shot_index}: narration needs more reading time')
            at = shot_start + .5
            for chunk in chunks:
                seconds = available * len(chunk.split()) / total_words
                cues.append({"start": at, "end": at + seconds - .15, "text": chunk,
                             "chapter": chapter["id"], "shot": shot_index,
                             "capture": shot["capture"]})
                at += seconds
            shot_start += shot["duration"]
    return cues


def write_text_assets(manifest, output):
    cues = cue_rows(manifest)
    vtt, srt = ["WEBVTT", ""], []
    for number, cue in enumerate(cues, 1):
        vtt.extend([f'{stamp(cue["start"])} --> {stamp(cue["end"])}', cue["text"], ""])
        srt.extend([str(number), f'{stamp(cue["start"], ",")} --> {stamp(cue["end"], ",")}', cue["text"], ""])
    (output / "forge-workshops.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (output / "forge-workshops.srt").write_text("\n".join(srt), encoding="utf-8")
    lines = ["# Forge Workshop Kit: narration for the ten-minute tour", "", "Read this over the clean video. The captioned version uses these same words. The recording shows saved work and display-only interactions; it is not a new live experiment.", ""]
    for chapter in manifest["chapters"]:
        lines.extend([f'## {stamp(chapter["start"])[:8]}–{stamp(chapter["start"]+chapter["duration"])[:8]} · {chapter["title"]}', ""])
        at = chapter["start"]
        for shot in chapter["shots"]:
            lines.extend([f'**{stamp(at)[:8]}–{stamp(at+shot["duration"])[:8]} — Show:** {shot["description"]}.', "", " ".join(shot["narration"]), ""])
            at += shot["duration"]
    lines.extend(["## Link accompanying the recording", "", "External video viewers: https://utm.io/uuIan. External community Slack: https://utm.io/uuIaS. Internal reviews: https://ash0ts.github.io/forge-workshop-kit/. Link visits measure entry paths, not notebook copies or completion.", ""])
    (ROOT / "media/walkthrough/narration.md").write_text("\n".join(lines), encoding="utf-8")
    shutil.copy2(ROOT / "media/walkthrough/narration.md", output / "narration.md")
    (output / "captions.json").write_text(json.dumps(cues, indent=2) + "\n", encoding="utf-8")
    return cues


def capture_rows(raw, shot):
    path = raw / shot["capture"] / "capture.json"
    capture = json.loads(path.read_text(encoding="utf-8"))
    original = capture["frames"]
    start = float(shot.get("in", 0))
    stop = min(float(shot.get("out", capture["elapsed"])), float(capture["elapsed"]))
    selected = [row for row in original if start <= row["time"] < stop]
    if len(selected) < 2:
        raise ValueError(f"Not enough captured frames: {path}")
    rate = float(shot.get("rate", 1))
    if rate <= 0 or rate > 2:
        raise ValueError("Use a playback rate between 0 and 2; preserve readable interactions.")
    source_duration = (stop - selected[0]["time"]) / rate
    if source_duration > shot["duration"] + .05:
        raise ValueError(f'{shot["capture"]}: trim source or extend shot duration explicitly')
    frames = []
    for index, row in enumerate(selected):
        next_time = selected[index+1]["time"] if index+1 < len(selected) else stop
        image = path.parent / Path(row["file"]).name
        if not image.is_file():
            raise FileNotFoundError(image)
        frames.append((image, max(.001, (next_time-row["time"])/rate)))
    frames[-1] = (frames[-1][0], frames[-1][1] + max(0, shot["duration"]-source_duration))
    return path, capture, frames, source_duration


def render_shot(manifest, output, chapter, shot, index, ffmpeg):
    raw = output / "raw"
    capture_path, capture, frames, moving = capture_rows(raw, shot)
    work = output / "edit" / f'{chapter["id"]}-{index:02}'
    work.mkdir(parents=True, exist_ok=True)
    destination = work / "shot.mp4"
    fingerprint = hashlib.sha256(json.dumps({"shot":shot,"chapter":chapter["title"],"capture":digest(capture_path),"script":digest(__file__),"tokens":TOKENS},sort_keys=True).encode()).hexdigest()
    receipt = work / "receipt.json"
    if destination.exists() and receipt.exists() and json.loads(receipt.read_text(encoding="utf-8")).get("fingerprint") == fingerprint:
        return destination, json.loads(receipt.read_text(encoding="utf-8"))
    concat = ["ffconcat version 1.0"]
    for image, seconds in frames:
        concat.extend([f"file {concat_path(image)}", f"duration {seconds:.6f}"])
    concat.append(f"file {concat_path(frames[-1][0])}")
    (work / "frames.txt").write_text("\n".join(concat) + "\n", encoding="utf-8")
    overlay_image(output, chapter, shot, work / "overlay.png")
    crop = shot.get("crop")
    prefix = f"crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}," if crop else ""
    # Source pixels retain their aspect ratio. The footer is outside the screen.
    vf = f"[0:v]{prefix}fps={FPS},scale={SCREEN[2]}:{SCREEN[3]}:force_original_aspect_ratio=decrease,pad={WIDTH}:{HEIGHT}:(ow-iw)/2:{SCREEN[1]}+({SCREEN[3]}-ih)/2:color={C['paper']},setsar=1[screen];[screen][1:v]overlay=0:0:shortest=1[v]"
    run([ffmpeg,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",work/"frames.txt","-loop","1","-i",work/"overlay.png","-filter_complex",vf,"-map","[v]","-an","-c:v","libx264","-threads","2","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-r",FPS,"-t",shot["duration"],"-movflags","+faststart",destination])
    row = {"fingerprint":fingerprint,"capture":shot["capture"],"source_url":capture["url"],"capture_sha256":digest(capture_path),"source_motion_seconds":moving,"reading_hold_seconds":max(0,shot["duration"]-moving),"output_seconds":shot["duration"],"crop":crop,"label":shot["label"],"frames":len(frames)}
    receipt.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
    return destination, row


def render_caption_track(cues, output, duration):
    directory = output / "edit/captions"
    directory.mkdir(parents=True, exist_ok=True)
    rows, at = [], 0
    for cue in cues:
        if cue["start"] > at:
            rows.append((cue["start"] - at, ""))
        rows.append((cue["end"]-cue["start"], cue["text"]))
        at = cue["end"]
    if duration > at:
        rows.append((duration-at, ""))
    concat = ["ffconcat version 1.0"]
    for index, (seconds, text) in enumerate(rows):
        path = directory / f"{index:04}.png"
        caption_image(output, text, path)
        concat.extend([f"file {concat_path(path)}", f"duration {seconds:.6f}"])
    concat.append(f"file {concat_path(path)}")
    path = directory / "frames.txt"
    path.write_text("\n".join(concat)+"\n", encoding="utf-8")
    return path


def make_stills(manifest, output, ffmpeg):
    stills = output / "stills"
    stills.mkdir(exist_ok=True)
    panels = []
    for chapter in manifest["chapters"]:
        path = stills / f'{chapter["number"]:02}-{chapter["id"]}.png'
        run([ffmpeg,"-hide_banner","-loglevel","error","-y","-ss",chapter["start"]+min(8,chapter["duration"]-1),"-i",output/"forge-workshops-captioned.mp4","-frames:v","1",path])
        panels.append(path)
    sheet = Image.new("RGB",(1920, math.ceil(len(panels)/3)*396),C["paper"])
    draw = ImageDraw.Draw(sheet)
    for index,path in enumerate(panels):
        image=Image.open(path).convert("RGB").resize((624,351),Image.Resampling.LANCZOS)
        x,y=8+(index%3)*640,8+(index//3)*396
        sheet.paste(image,(x,y))
        draw.text((x+8,y+357),manifest["chapters"][index]["title"],font=font(output,400,19),fill=C["ink"])
    sheet.save(output/"contact-sheet.png")
    poster=Image.new("RGB",(WIDTH,HEIGHT),C["paper"])
    draw=ImageDraw.Draw(poster)
    draw.text((100,70),"FORGE WORKSHOP KIT",font=font(output,600,31),fill=C["accent"])
    draw.text((100,125),"Six practical workshops for using Forge",font=font(output,600,63),fill=C["ink"])
    draw.text((100,210),"A ten-minute tour of the exercises and the records behind them",font=font(output,400,31),fill=C["muted"])
    selected=[path for path in panels if any(key in path.name for key in ['pending','solar','routing','inspection','transit','airline'])]
    for index,path in enumerate(selected):
        image=Image.open(path).convert("RGB").crop((160,60,1760,958)).resize((548,308),Image.Resampling.LANCZOS)
        x,y=100+(index%3)*584,292+(index//3)*352
        poster.paste(image,(x,y))
        draw.rectangle((x,y,x+548,y+308),outline=C["line"],width=1)
        draw.text((x,y+314),path.stem.split('-',1)[1].capitalize(),font=font(output,600,22),fill=C["ink"])
    draw.text((100,1020),"Saved workshop executions · Real product screens · A narrated technical tour",font=font(output,400,24),fill=C["muted"])
    poster.save(output/"poster.png")


def package_edit(manifest, output, clips):
    """Ship shareable exports and cropped edit clips, never raw account headers."""
    timeline = []
    index = 0
    for chapter in manifest["chapters"]:
        at = chapter["start"]
        for number, shot in enumerate(chapter["shots"]):
            timeline.append({
                "file": f'clips/{chapter["id"]}-{number:02}.mp4',
                "start_seconds": at, "duration_seconds": shot["duration"],
                "chapter": chapter["title"], "label": shot["label"],
                "source_capture": shot["capture"],
            })
            at += shot["duration"]
            index += 1
    (output / "edit-final-cut.json").write_text(json.dumps({
        "canvas": [WIDTH, HEIGHT], "fps": FPS, "audio": "none",
        "instructions": "Clips are already cropped and framed. Place them at the stated start times. Add the narration and import the SRT; retime subtitles if your delivery differs.",
        "timeline": timeline,
    }, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(ROOT / "media/walkthrough/README.md", output / "README.md")
    files = [
        "forge-workshops-captioned.mp4", "forge-workshops-clean.mp4",
        "forge-workshops.srt", "forge-workshops.vtt", "narration.md",
        "poster.png", "contact-sheet.png", "index.html", "README.md",
        "edit-resolved.json", "edit-final-cut.json", "production-receipt.json",
    ]
    with zipfile.ZipFile(output / "forge-workshops-video-edit.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
        for name in files:
            archive.write(output / name, name)
        for row, path in zip(timeline, clips, strict=True):
            archive.write(path, row["file"])
        for path in sorted((output / "stills").glob("*.png")):
            archive.write(path, f"stills/{path.name}")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest",type=Path,default=ROOT/"media/walkthrough/edit.json")
    parser.add_argument("--output",type=Path,default=ROOT/"dist/walkthrough-production")
    parser.add_argument("--prepare-only",action="store_true")
    parser.add_argument("--chapter",help="Render one chapter's shots for layout review, without a final video")
    args=parser.parse_args()
    manifest=json.loads(args.manifest.read_text(encoding="utf-8"))
    output=args.output.resolve(); output.mkdir(parents=True,exist_ok=True)
    at=0
    for index,chapter in enumerate(manifest["chapters"],1):
        chapter.update(number=index,start=at)
        if sum(shot["duration"] for shot in chapter["shots"]) != chapter["duration"]:
            raise ValueError(f'{chapter["id"]}: shot durations do not equal chapter duration')
        at+=chapter["duration"]
    if at!=600: raise ValueError(f"The edit must last 600 seconds, found {at}")
    cues=write_text_assets(manifest,output)
    (output/"edit-resolved.json").write_text(json.dumps(manifest,indent=2)+"\n", encoding="utf-8")
    missing=sorted({shot["capture"] for chapter in manifest["chapters"] for shot in chapter["shots"] if not (output/"raw"/shot["capture"]/"capture.json").exists()})
    if args.prepare_only:
        render_caption_track(cues,output,at)
        print(json.dumps({"seconds":at,"chapters":len(manifest["chapters"]),"captions":len(cues),"missing_captures":missing})); return
    chosen=[row for row in manifest["chapters"] if not args.chapter or row["id"]==args.chapter]
    if not chosen: raise ValueError("Unknown chapter")
    needed=sorted({shot["capture"] for chapter in chosen for shot in chapter["shots"] if not (output/"raw"/shot["capture"]/"capture.json").exists()})
    if needed: raise FileNotFoundError("Missing actual browser captures: "+", ".join(needed))
    ffmpeg=shutil.which("ffmpeg")
    ffprobe=shutil.which("ffprobe")
    if not ffmpeg or not ffprobe: raise RuntimeError("Install FFmpeg from its official distribution or package manager.")
    clips=[]; receipts=[]
    for chapter in chosen:
        for index,shot in enumerate(chapter["shots"]):
            print(f'Rendering {chapter["id"]}/{shot["capture"]}',flush=True)
            clip,receipt=render_shot(manifest,output,chapter,shot,index,ffmpeg)
            clips.append(clip); receipts.append(receipt)
    if args.chapter: print(json.dumps({"chapter":args.chapter,"shots":[str(p) for p in clips]})); return
    concat=output/"edit/clips.txt"
    concat.write_text("\n".join(f"file {concat_path(p)}" for p in clips)+"\n", encoding="utf-8")
    metadata=output/"edit/chapters.txt"
    metadata.write_text(";FFMETADATA1\ntitle=Forge Workshop Kit: six practical workflows\n"+"".join(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={row["start"]*1000}\nEND={(row["start"]+row["duration"])*1000}\ntitle={row["title"]}\n' for row in manifest["chapters"]), encoding="utf-8")
    clean=output/"forge-workshops-clean.mp4"
    run([ffmpeg,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",concat,"-i",metadata,"-map_metadata","1","-map_chapters","1","-c","copy","-an","-movflags","+faststart",clean])
    captions=render_caption_track(cues,output,at)
    captioned=output/"forge-workshops-captioned.mp4"
    run([ffmpeg,"-hide_banner","-loglevel","error","-y","-i",clean,"-f","concat","-safe","0","-i",captions,"-filter_complex",f"[0:v][1:v]overlay=0:{CAPTION_Y}:shortest=1[v]","-map","[v]","-map_metadata","0","-map_chapters","0","-an","-c:v","libx264","-threads","2","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-r",FPS,"-t",at,"-movflags","+faststart",captioned])
    make_stills(manifest,output,ffmpeg)
    probes={path.name:json.loads(subprocess.check_output([ffprobe,"-v","error","-show_format","-show_streams","-of","json",str(path)])) for path in [clean,captioned]}
    for name,probe in probes.items():
        probe["format"]["filename"] = name
        if abs(float(probe["format"]["duration"])-600)>.1: raise ValueError(f"Unexpected duration: {name}")
        if any(s["codec_type"]=="audio" for s in probe["streams"]): raise ValueError(f"Unexpected audio: {name}")
        video=next(s for s in probe["streams"] if s["codec_type"]=="video")
        if (video["width"],video["height"])!=(WIDTH,HEIGHT): raise ValueError("Unexpected dimensions")
        if video["avg_frame_rate"] != f"{FPS}/1": raise ValueError("Unexpected frame rate")
    receipt={"schema_version":1,"title":manifest["title"],"duration_seconds":600,"canvas":[WIDTH,HEIGHT],"fps":FPS,"audio":"none; clean version is ready for a human dub","capture_method":"Actual browser frames captured through CUA. Timestamp timing retained; explicit reading holds extend the final frame.","manifest_sha256":digest(args.manifest),"renderer_sha256":digest(__file__),"paid_executions_during_capture":0,"shots":receipts,"outputs":{name:{"sha256":digest(output/name),"bytes":(output/name).stat().st_size} for name in ['forge-workshops-clean.mp4','forge-workshops-captioned.mp4','forge-workshops.srt','forge-workshops.vtt','poster.png','contact-sheet.png']},"probe":probes}
    (output/"production-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n", encoding="utf-8")
    (output/"index.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Forge Workshop Kit walkthrough</title><style>body{margin:2rem auto;max-width:1200px;padding:0 1rem;background:#f4f3ef;color:#242522;font:18px system-ui}video{width:100%;height:auto}a{color:#246cac}</style><h1>Six practical Forge workshops</h1><p>Actual browser interactions with saved experiments and teaching guides. No audio; use the narration script to record your own voice-over.</p><video controls preload="metadata" poster="poster.png"><source src="forge-workshops-captioned.mp4" type="video/mp4"></video><p><a href="forge-workshops-captioned.mp4">Captioned MP4</a> · <a href="forge-workshops-clean.mp4">Clean MP4 for dubbing</a> · <a href="narration.md">Narration script</a> · <a href="forge-workshops.srt">SRT</a></p><p>Full sessions remain technical previews; these captures do not replace an external-account or participant rehearsal.</p></html>', encoding="utf-8")
    package_edit(manifest, output, clips)
    print(output/"index.html")


if __name__=="__main__":
    main()
