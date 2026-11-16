# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["pillow==12.3.0", "fonttools==4.68.0", "brotli==1.2.0"]
# ///
"""Generate timed ElevenLabs narration, then mix it with an existing workshop edit.

`plan`, `check`, and `mix` make no provider calls. Only `generate` submits paid
requests. An unfinished request is never resent automatically. Raw responses are
saved before decoding so an interrupted local conversion can resume without a call.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.elevenlabs.io"
SAFE_HEADERS = {"request-id", "history-item-id", "character-cost", "x-request-id", "content-type"}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha(value):
    if isinstance(value, Path):
        return hashlib.sha256(value.read_bytes()).hexdigest()
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def safe_id(value):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", str(value)):
        raise ValueError(f"Use letters, digits, hyphens or underscores for asset IDs: {value!r}")
    return str(value)


def load_api_key(env_file=None):
    """Read only supported key names, without executing or expanding a shell file."""
    names = ("ELEVENLABS_API_KEY", "ELEVEN_LABS_API_KEY")
    if env_file:
        found = {}
        for line in Path(env_file).read_text(encoding="utf-8").splitlines():
            match = re.match(
                r"^\s*(?:export\s+)?(ELEVENLABS_API_KEY|ELEVEN_LABS_API_KEY)\s*=\s*(.*?)\s*$", line
            )
            if match:
                value = match[2]
                if value[:1] in ("'", '"'):
                    quote = value[0]
                    end = value.find(quote, 1)
                    if end < 0 or (
                        value[end + 1 :].strip() and not value[end + 1 :].strip().startswith("#")
                    ):
                        raise ValueError("Malformed quoted ElevenLabs key in the selected env file")
                    value = value[1:end]
                else:
                    value = value.split(" #", 1)[0].strip()
                if not value or any(c.isspace() for c in value) or "$" in value or "`" in value:
                    raise ValueError("The selected env file must contain a literal ElevenLabs key")
                found[match[1]] = value
        key = next((found[name] for name in names if name in found), None)
    else:
        key = next((os.environ[name] for name in names if os.environ.get(name)), None)
    if not key:
        raise ValueError(
            "Set ELEVENLABS_API_KEY or ELEVEN_LABS_API_KEY, or pass --env-file explicitly"
        )
    return key


def request_json(method, path, key, payload=None):
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        API + path,
        body,
        method=method,
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )
    # No implicit HTTP retries: a timeout after dispatch has an uncertain cost.
    with urllib.request.urlopen(request, timeout=180) as response:
        headers = {k.lower(): v for k, v in response.headers.items() if k.lower() in SAFE_HEADERS}
        return response.read(), headers


def visual_identity(manifest):
    """Bind narration to the existing screen edit, excluding rewritten spoken text."""
    return {
        "canvas": manifest.get("canvas", [1920, 1080]),
        "fps": manifest.get("fps", 25),
        "chapters": [
            {
                "id": chapter["id"],
                "title": chapter["title"],
                "duration": chapter["duration"],
                "shots": [
                    {
                        key: shot.get(key, default)
                        for key, default in (
                            ("capture", None),
                            ("duration", None),
                            ("in", 0),
                            ("out", None),
                            ("rate", 1),
                            ("crop", None),
                            ("label", None),
                        )
                    }
                    for shot in chapter["shots"]
                ],
            }
            for chapter in manifest["chapters"]
        ],
    }


def make_plan(manifest, config):
    if config.get("schema_version") != 1:
        raise ValueError("Unsupported audio configuration version")
    voice = config["voice_id"]
    if not re.fullmatch(r"[A-Za-z0-9]+", voice):
        raise ValueError("Invalid ElevenLabs voice ID")
    maximum_tempo = float(config["timing"]["maximum_tempo"])
    if not 1 <= maximum_tempo <= 1.08:
        raise ValueError("The maximum tempo must be between 1 and 1.08")
    output_format = config.get("output_format", "mp3_44100_128")
    if output_format != "mp3_44100_128":
        raise ValueError("This exporter currently supports mp3_44100_128")
    rows, chapters, at = [], [], 0.0
    identifiers = set()
    for chapter in manifest["chapters"]:
        chapter_id = safe_id(chapter["id"])
        start = at
        for index, shot in enumerate(chapter["shots"]):
            asset_id = f"{chapter_id}-{index:02}"
            if asset_id in identifiers:
                raise ValueError(f"Duplicate asset identity: {asset_id}")
            identifiers.add(asset_id)
            duration = float(shot["duration"])
            text = " ".join(shot["narration"]).strip()
            if not text or duration <= sum(
                config["timing"][k] for k in ("lead_seconds", "tail_seconds")
            ):
                raise ValueError(f"Empty narration or unusable duration for {asset_id}")
            if len(text) > 10000:
                raise ValueError(f"{asset_id}: split narration before the model's character limit")
            payload = {
                "text": text,
                "model_id": config["model_id"],
                "voice_settings": config["voice_settings"],
                "apply_text_normalization": "on",
                "seed": int(hashlib.sha256(asset_id.encode()).hexdigest()[:8], 16),
            }
            path = f"/v1/text-to-speech/{voice}/with-timestamps?output_format={output_format}&enable_logging=true"
            request = {"path": path, "payload": payload}
            request_sha = sha(request)
            available = (
                duration - config["timing"]["lead_seconds"] - config["timing"]["tail_seconds"]
            )
            rows.append(
                {
                    "asset_id": asset_id,
                    "kind": "tts",
                    "name": f"{config['collection']} / {chapter['title']} / {index + 1:02}",
                    "chapter": chapter_id,
                    "shot": index,
                    "capture": shot["capture"],
                    "start": at,
                    "duration": duration,
                    "text": text,
                    "characters": len(text),
                    "required_words_per_minute": round(len(text.split()) / available * 60, 1),
                    "voice_id": voice,
                    "model_id": config["model_id"],
                    "request": request,
                    "request_sha256": request_sha,
                    "directory": f"shots/{asset_id}/{request_sha[:12]}",
                }
            )
            at += duration
        if not math.isclose(at - start, float(chapter["duration"]), abs_tol=0.001):
            raise ValueError(f"Shot durations do not match chapter {chapter_id}")
        chapters.append(
            {"id": chapter_id, "title": chapter["title"], "start": start, "duration": at - start}
        )
    effect_ids = {safe_id(asset["id"]) for asset in config.get("sound_effects", [])}
    chapter_ids = {chapter["id"] for chapter in chapters}
    for placement in config.get("effect_placements", []):
        if placement["effect"] not in effect_ids or placement["chapter"] not in chapter_ids:
            raise ValueError("Sound placement must refer to a defined effect and chapter")
        offset = float(placement.get("offset_seconds", 0.05))
        chapter = next(row for row in chapters if row["id"] == placement["chapter"])
        effect = next(row for row in config["sound_effects"] if row["id"] == placement["effect"])
        if (
            not math.isfinite(offset)
            or offset < 0
            or offset + effect["duration_seconds"] > chapter["duration"]
        ):
            raise ValueError("Sound effect must fit within its chapter")
    for asset in config.get("sound_effects", []):
        if not 0.5 <= float(asset["duration_seconds"]) <= 30:
            raise ValueError("Sound duration must be between 0.5 and 30 seconds")
        asset_id = safe_id(asset["id"])
        if asset_id in identifiers:
            raise ValueError(f"Duplicate asset identity: {asset_id}")
        identifiers.add(asset_id)
        payload = {
            "text": asset["prompt"],
            "duration_seconds": asset["duration_seconds"],
            "prompt_influence": asset.get("prompt_influence", 0.5),
            "loop": False,
            "model_id": asset.get("model_id", "eleven_text_to_sound_v2"),
        }
        request = {
            "path": f"/v1/sound-generation?output_format={output_format}&enable_logging=true",
            "payload": payload,
        }
        request_sha = sha(request)
        rows.append(
            {
                "asset_id": asset_id,
                "kind": "sfx",
                "name": f"{config['collection']} / {asset['name']}",
                "text": asset["prompt"],
                "characters": len(asset["prompt"]),
                "model_id": payload["model_id"],
                "duration": asset["duration_seconds"],
                "request": request,
                "request_sha256": request_sha,
                "directory": f"effects/{asset_id}/{request_sha[:12]}",
            }
        )
    return {
        "schema_version": 1,
        "collection": config["collection"],
        "seconds": at,
        "manifest_sha256": sha(manifest),
        "visual_sha256": sha(visual_identity(manifest)),
        "config_sha256": sha(config),
        "chapters": chapters,
        "characters": sum(row["characters"] for row in rows if row["kind"] == "tts"),
        "paid_tts_requests": sum(row["kind"] == "tts" for row in rows),
        "paid_sfx_requests": sum(row["kind"] == "sfx" for row in rows),
        "assets": rows,
    }


def validate_alignment(alignment):
    if not alignment:
        raise ValueError(
            "The provider returned no character alignment; keep the response and investigate"
        )
    chars, starts, ends = (
        alignment[k]
        for k in ("characters", "character_start_times_seconds", "character_end_times_seconds")
    )
    if not chars or len(chars) != len(starts) or len(chars) != len(ends):
        raise ValueError("Alignment arrays have different lengths")
    previous = 0.0
    for char, start, end in zip(chars, starts, ends, strict=True):
        if (
            not isinstance(char, str)
            or not math.isfinite(start + end)
            or start < previous - 0.005
            or end < start
        ):
            raise ValueError("Invalid or non-monotonic character alignment")
        previous = start
    return alignment


def decode_response(row, directory, receipt):
    response = directory / "response.bin"
    if receipt.get("response_sha256") and sha(response) != receipt["response_sha256"]:
        raise ValueError("Saved provider response changed; restore the original response")
    if row["kind"] == "tts":
        data = json.loads(response.read_bytes())
        # Normalized text matches the words spoken when the API expands numbers.
        alignment = validate_alignment(data.get("normalized_alignment") or data.get("alignment"))
        audio = base64.b64decode(data["audio_base64"], validate=True)
        if not audio:
            raise ValueError("Provider returned empty audio")
        (directory / "audio.mp3").write_bytes(audio)
        write(directory / "alignment.json", alignment)
        receipt.update(
            alignment_file="alignment.json", alignment_sha256=sha(directory / "alignment.json")
        )
    else:
        audio = response.read_bytes()
        if not audio or audio[:1] in (b"{", b"<"):
            raise ValueError("Sound response is not an audio body")
        (directory / "audio.mp3").write_bytes(audio)
    receipt.update(
        status="completed",
        completed_at=time.time(),
        audio_file="audio.mp3",
        audio_sha256=sha(directory / "audio.mp3"),
        audio_bytes=len(audio),
    )
    write(directory / "receipt.json", receipt)
    return receipt


def valid_saved(row, directory):
    path = directory / "receipt.json"
    if not path.exists():
        return None
    receipt = load(path)
    if receipt["request_sha256"] != row["request_sha256"]:
        raise ValueError(f"{row['asset_id']}: saved request does not match")
    if receipt["status"] == "completed":
        for key in ("audio", "alignment"):
            if f"{key}_file" in receipt:
                output = directory / receipt[f"{key}_file"]
                if not output.is_file() or sha(output) != receipt[f"{key}_sha256"]:
                    raise ValueError(
                        f"{row['asset_id']}: saved {key} missing or changed; restore the original file"
                    )
        return receipt
    if (directory / "response.bin").is_file():
        return decode_response(row, directory, receipt)
    return receipt


def _generate_one(row, output, key, retry_rejected=False):
    directory = output / row["directory"]
    receipt = valid_saved(row, directory)
    if receipt and receipt["status"] == "completed":
        return receipt
    if receipt and not (retry_rejected and receipt["status"] == "rejected"):
        raise RuntimeError(
            f"{row['asset_id']}: earlier request is {receipt['status']}. Do not resend. Check provider history and the local receipt."
        )
    directory.mkdir(parents=True, exist_ok=True)
    if receipt:
        write(directory / "attempts" / f"{int(receipt['started_at'] * 1000000)}.json", receipt)
    receipt = {k: v for k, v in row.items() if k not in ("request", "directory")}
    receipt.update(status="started", started_at=time.time(), provider="ElevenLabs")
    write(directory / "request.json", row["request"])
    write(directory / "receipt.json", receipt)
    try:
        raw, headers = request_json("POST", row["request"]["path"], key, row["request"]["payload"])
        # Preserve the paid response before parsing, media conversion, or publication.
        pending = directory / "response.bin.tmp"
        pending.write_bytes(raw)
        pending.replace(directory / "response.bin")
        receipt.update(
            status="response_saved",
            provider_headers=headers,
            response_sha256=sha(directory / "response.bin"),
        )
        write(directory / "receipt.json", receipt)
        return decode_response(row, directory, receipt)
    except urllib.error.HTTPError as error:
        # 5xx can occur after processing. 4xx is an explicit rejection, but retry is opt-in.
        receipt.update(
            status="rejected" if 400 <= error.code < 500 else "uncertain",
            http_status=error.code,
            error_type=type(error).__name__,
        )
        write(directory / "receipt.json", receipt)
        raise RuntimeError(
            f"{row['asset_id']}: provider HTTP {error.code}; saved {receipt['status']} receipt"
        ) from None
    except (OSError, ValueError, KeyError, TypeError) as error:
        receipt.update(
            status="response_saved" if (directory / "response.bin").exists() else "uncertain",
            error_type=type(error).__name__,
        )
        write(directory / "receipt.json", receipt)
        raise RuntimeError(
            f"{row['asset_id']}: {type(error).__name__}; {receipt['status']}, no automatic retry"
        ) from None


def generate_one(row, output, key, retry_rejected=False):
    directory = output / row["directory"]
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / "generation.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise RuntimeError(
            f"{row['asset_id']}: a generation lock exists. Check the running process and receipt; do not submit another request."
        ) from None
    try:
        with os.fdopen(descriptor, "w") as handle:
            handle.write(str(os.getpid()))
        return _generate_one(row, output, key, retry_rejected)
    finally:
        lock.unlink()


def tool(name):
    path = shutil.which(name)
    if not path:
        raise ValueError(f"Install {name} from the official FFmpeg distribution or package manager")
    return path


def run(command):
    subprocess.run([str(item) for item in command], check=True)


def probe(path):
    return json.loads(
        subprocess.check_output(
            [
                tool("ffprobe"),
                "-v",
                "error",
                "-show_format",
                "-show_streams",
                "-of",
                "json",
                str(path),
            ]
        )
    )


def fit_audio(audio_duration, shot_duration, timing):
    available = shot_duration - timing["lead_seconds"] - timing["tail_seconds"]
    tempo = max(1.0, audio_duration / available)
    if tempo > timing["maximum_tempo"] + 0.0001:
        raise ValueError(
            f"Narration needs {audio_duration:.2f}s in {available:.2f}s; required tempo {tempo:.3f} exceeds {timing['maximum_tempo']}. Shorten the script or extend this shot; audio will not be clipped."
        )
    return tempo


def audio_index(plan, output, config, require_complete=False):
    rows, problems = [], []
    for asset in plan["assets"]:
        directory = output / asset["directory"]
        row = {k: v for k, v in asset.items() if k != "request"}
        try:
            receipt = valid_saved(asset, directory)
            if not receipt or receipt["status"] != "completed":
                row["status"] = receipt["status"] if receipt else "not_generated"
                problems.append(f"{row['asset_id']}: {row['status']}")
            else:
                row.update(
                    status="completed",
                    audio_file=f"{row['directory']}/{receipt['audio_file']}",
                    receipt=f"{row['directory']}/receipt.json",
                    audio_sha256=receipt["audio_sha256"],
                    provider_headers=receipt.get("provider_headers", {}),
                )
                duration = float(probe(output / row["audio_file"])["format"]["duration"])
                row["audio_duration"] = duration
                if asset["kind"] == "tts":
                    row["alignment_file"] = f"{row['directory']}/alignment.json"
                    row["tempo"] = fit_audio(duration, row["duration"], config["timing"])
                    alignment = validate_alignment(load(output / row["alignment_file"]))
                    if max(alignment["character_end_times_seconds"]) > duration + 0.1:
                        raise ValueError("Character alignment extends past saved audio")
        except (ValueError, KeyError, subprocess.CalledProcessError) as error:
            row["status"] = "needs_review"
            row["problem"] = str(error)
            problems.append(f"{row['asset_id']}: {error}")
        rows.append(row)
    result = {k: v for k, v in plan.items() if k != "assets"}
    result.update(assets=rows, problems=problems, complete=not problems)
    write(output / "audio-index.json", result)
    if require_complete and problems:
        raise ValueError("Audio check failed:\n" + "\n".join(problems))
    return result


def caption_cues(alignment, start, tempo, asset_id, maximum_characters=84, maximum_seconds=5.5):
    """Group actual character timestamps into readable captions, never estimated slots."""
    validate_alignment(alignment)
    words, current, begin, end = [], "", None, None
    for char, at, until in zip(
        alignment["characters"],
        alignment["character_start_times_seconds"],
        alignment["character_end_times_seconds"],
        strict=True,
    ):
        for part in re.split(r"(\s+)", char):
            if not part:
                continue
            if part.isspace():
                if current:
                    words.append((current, begin, end))
                    current, begin = "", None
            else:
                begin = at if begin is None else begin
                current += part
                end = until
    if current:
        words.append((current, begin, end))
    cues, group = [], []

    def emit():
        if group:
            cues.append(
                {
                    "start": round(start + group[0][1] / tempo, 4),
                    "end": round(start + group[-1][2] / tempo, 4),
                    "text": " ".join(word[0] for word in group),
                    "asset_id": asset_id,
                }
            )

    for word in words:
        text = " ".join(item[0] for item in group + [word])
        if group and (
            len(text) > maximum_characters or (word[2] - group[0][1]) / tempo > maximum_seconds
        ):
            emit()
            group = []
        group.append(word)
        if word[0].endswith((".", "?", "!", ":", ";")):
            emit()
            group = []
    emit()
    return cues


def stamp(value, separator="."):
    ms = round(value * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02}{separator}{ms % 1000:03}"


def write_captions(cues, output):
    srt, vtt = [], ["WEBVTT", ""]
    previous_end = 0
    for number, cue in enumerate(cues, 1):
        if cue["start"] < previous_end - 0.01 or cue["end"] <= cue["start"]:
            raise ValueError("Caption intervals overlap or have no duration")
        text = cue["text"]
        srt.extend(
            [str(number), f"{stamp(cue['start'], ',')} --> {stamp(cue['end'], ',')}", text, ""]
        )
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        vtt.extend([f"{stamp(cue['start'])} --> {stamp(cue['end'])}", escaped, ""])
        previous_end = cue["end"]
    (output / "forge-workshops-narrated.srt").write_text("\n".join(srt), encoding="utf-8")
    (output / "forge-workshops-narrated.vtt").write_text("\n".join(vtt), encoding="utf-8")
    write(output / "narrated-captions.json", cues)


def verify_video_source(index, video, video_receipt=None, visual_manifest=None):
    receipt_path = video_receipt or video.parent / "production-receipt.json"
    manifest_path = visual_manifest or video.parent / "edit-resolved.json"
    if not receipt_path.is_file() or not manifest_path.is_file():
        raise ValueError(
            "The video needs its production receipt and resolved visual edit before mixing"
        )
    receipt = load(receipt_path)
    output = receipt.get("outputs", {}).get(video.name)
    if not output or output.get("sha256") != sha(video):
        raise ValueError("Video bytes do not match the selected production receipt")
    visual = load(manifest_path)
    if sha(visual_identity(visual)) != index["visual_sha256"]:
        raise ValueError(
            "Narration and video use different shots, timing, labels, or crops; rebuild the visual edit"
        )
    return {
        "video_receipt_sha256": sha(receipt_path),
        "visual_manifest_sha256": sha(manifest_path),
        "visual_sha256": index["visual_sha256"],
    }


def verify_wav_duration(path, seconds):
    with wave.open(str(path), "rb") as source:
        actual = source.getnframes()
        expected = round(seconds * source.getframerate())
        if actual != expected:
            raise ValueError(f"Wrong sample count for {path.name}: {actual}; expected {expected}")
        return {"samples": actual, "sample_rate": source.getframerate(), "seconds": seconds}


def prepare_voice_clip(source, destination, duration, tempo, lead, voice_lufs):
    # Trim by sample count: MP3 and loudnorm timestamps can otherwise shorten a
    # slot while leaving the enclosing video's duration unchanged.
    samples = round(duration * 48000)
    filter_audio = (
        f"atempo={tempo:.8f},loudnorm=I={voice_lufs}:TP=-2:LRA=7,aresample=48000,"
        f"asetpts=N/SR/TB,adelay={round(lead * 48000)}S:all=1,"
        f"apad=whole_len={samples},atrim=end_sample={samples},asetpts=N/SR/TB"
    )
    run(
        [
            tool("ffmpeg"),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            source,
            "-af",
            filter_audio,
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            destination,
        ]
    )
    return verify_wav_duration(destination, duration)


def mix(index, config, audio_output, video, destination, video_receipt=None, visual_manifest=None):
    source_identity = verify_video_source(index, video, video_receipt, visual_manifest)
    ffmpeg = tool("ffmpeg")
    info = probe(video)
    if abs(float(info["format"]["duration"]) - index["seconds"]) > 0.1:
        raise ValueError("Video duration does not match the narration manifest")
    destination.mkdir(parents=True, exist_ok=True)
    work = audio_output / "mix"
    work.mkdir(parents=True, exist_ok=True)
    clips, cues = [], []
    lead = config["timing"]["lead_seconds"]
    for row in index["assets"]:
        if row["kind"] != "tts":
            continue
        clip = work / f"{row['asset_id']}.wav"
        prepare_voice_clip(
            audio_output / row["audio_file"],
            clip,
            row["duration"],
            row["tempo"],
            lead,
            config["mix"]["voice_lufs"],
        )
        clips.append(clip)
        cues.extend(
            caption_cues(
                load(audio_output / row["alignment_file"]),
                row["start"] + lead,
                row["tempo"],
                row["asset_id"],
            )
        )
    concat = work / "narration.txt"
    concat.write_text(
        "".join("file '" + str(path.resolve()).replace("'", "'\\''") + "'\n" for path in clips),
        encoding="utf-8",
    )
    narration = destination / "narration.wav"
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat,
            "-c:a",
            "pcm_s16le",
            narration,
        ]
    )
    effects = [row for row in index["assets"] if row["kind"] == "sfx"]
    fx_command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=48000:cl=stereo",
    ]
    for row in effects:
        fx_command += ["-i", audio_output / row["audio_file"]]
    filters, labels = [], ["[0:a]"]
    for placement_index, placement in enumerate(config.get("effect_placements", [])):
        source = next(
            (i + 1 for i, row in enumerate(effects) if row["asset_id"] == placement["effect"]), None
        )
        if source is None:
            raise ValueError(f"Unknown sound effect {placement['effect']}")
        chapter = next(row for row in index["chapters"] if row["id"] == placement["chapter"])
        offset = chapter["start"] + placement.get("offset_seconds", 0.05)
        label = f"effect{placement_index}"
        filters.append(
            f"[{source}:a]loudnorm=I={config['mix']['effect_lufs']}:TP=-9:LRA=3,aresample=48000,afade=t=in:d=0.02,afade=t=out:st=0.35:d=0.15,adelay={round(offset * 1000)}:all=1[{label}]"
        )
        labels.append(f"[{label}]")
    filters.append(
        "".join(labels)
        + f"amix=inputs={len(labels)}:duration=first:normalize=0,atrim=duration={index['seconds']}[fx]"
    )
    effect_stem = destination / "sound-effects.wav"
    run(
        fx_command
        + [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[fx]",
            "-t",
            index["seconds"],
            "-c:a",
            "pcm_s16le",
            effect_stem,
        ]
    )
    mixed = destination / "mix.wav"
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            narration,
            "-i",
            effect_stem,
            "-filter_complex",
            "[0:a][1:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.84:level=false:latency=true[a]",
            "-map",
            "[a]",
            "-c:a",
            "pcm_s16le",
            mixed,
        ]
    )
    write_captions(cues, destination)
    clean = destination / "forge-workshops-narrated-clean.mp4"
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            video,
            "-i",
            mixed,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-map_metadata",
            "0",
            "-map_chapters",
            "0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            clean,
        ]
    )
    # Reuse the existing caption typography in a separate folder. Silent exports stay intact.
    spec = importlib.util.spec_from_file_location(
        "collection_video", ROOT / "scripts/build_collection_video.py"
    )
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    caption_output = work / "captions"
    # The silent edit already converted the bundled fonts. Reuse those local files.
    for weight in (400, 600):
        cached_font = video.parent / "fonts" / f"plex-{weight}.ttf"
        if cached_font.is_file():
            (caption_output / "fonts").mkdir(parents=True, exist_ok=True)
            shutil.copy2(cached_font, caption_output / "fonts" / cached_font.name)
    caption_track = renderer.render_caption_track(cues, caption_output, index["seconds"])
    captioned = destination / "forge-workshops-narrated-captioned.mp4"
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            clean,
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            caption_track,
            "-filter_complex",
            f"[0:v][1:v]overlay=0:{renderer.CAPTION_Y}:shortest=1[v]",
            "-map",
            "[v]",
            "-map",
            "0:a:0",
            "-map_metadata",
            "0",
            "-map_chapters",
            "0",
            "-c:v",
            "libx264",
            "-threads",
            "2",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-r",
            "25",
            "-t",
            index["seconds"],
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            captioned,
        ]
    )
    outputs = [
        narration,
        effect_stem,
        mixed,
        clean,
        captioned,
        destination / "forge-workshops-narrated.srt",
        destination / "forge-workshops-narrated.vtt",
    ]
    audio_verification = {
        path.name: verify_wav_duration(path, index["seconds"])
        for path in (narration, effect_stem, mixed)
    }
    for path in (clean, captioned):
        result = probe(path)
        if abs(float(result["format"]["duration"]) - index["seconds"]) > 0.1:
            raise ValueError(f"Wrong rendered duration: {path.name}")
        streams = [s for s in result["streams"] if s["codec_type"] == "audio"]
        if not streams:
            raise ValueError(f"Missing audio stream: {path.name}")
        if any(abs(float(s.get("duration", 0)) - index["seconds"]) > 0.05 for s in streams):
            raise ValueError(f"Wrong audio stream duration: {path.name}")
        audio_verification[path.name] = {
            "audio_seconds": [float(s["duration"]) for s in streams],
            "video_seconds": float(result["format"]["duration"]),
        }
    receipt = {
        "schema_version": 1,
        "collection": index["collection"],
        "seconds": index["seconds"],
        "manifest_sha256": index["manifest_sha256"],
        "config_sha256": index["config_sha256"],
        "input_video_sha256": sha(video),
        **source_identity,
        "renderer_sha256": sha(Path(__file__)),
        "captions": "provider character timestamps, adjusted only by recorded tempo and shot start",
        "generated_voice_id": config["voice_id"],
        "generated_voice_model": config["model_id"],
        "sound_effects": config.get("effect_placements", []),
        "timing": config["timing"],
        "audio_verification": audio_verification,
        "assets": [
            {
                k: row[k]
                for k in (
                    "asset_id",
                    "request_sha256",
                    "audio_duration",
                    "tempo",
                    "provider_headers",
                )
                if k in row
            }
            for row in index["assets"]
        ],
        "outputs": {
            path.name: {"sha256": sha(path), "bytes": path.stat().st_size} for path in outputs
        },
    }
    write(destination / "mix-receipt.json", receipt)
    return receipt


def history_index(index, output, key):
    """Read provider metadata for this collection, without touching unrelated history."""
    rows = []
    for asset in index["assets"]:
        if asset["kind"] != "tts" or asset["status"] != "completed":
            continue
        receipt = load(output / asset["receipt"])
        query = urllib.parse.urlencode(
            {
                "voice_id": asset["voice_id"],
                "source": "TTS",
                "search": asset["text"][:80],
                "date_after_unix": int(receipt["started_at"]) - 5,
                "page_size": 100,
            }
        )
        raw, _ = request_json("GET", "/v1/history?" + query, key)
        candidates = [
            row
            for row in json.loads(raw)["history"]
            if row.get("text") == asset["text"]
            and row.get("voice_id") == asset["voice_id"]
            and row.get("model_id") == asset["model_id"]
        ]
        request_id = receipt.get("provider_headers", {}).get("request-id")
        if request_id:
            candidates = [row for row in candidates if row.get("request_id") == request_id]
        row = {
            "asset_id": asset["asset_id"],
            "name": asset["name"],
            "request_sha256": asset["request_sha256"],
            "status": "matched" if len(candidates) == 1 else "unresolved",
            "matches": len(candidates),
        }
        if len(candidates) == 1:
            row.update(
                {
                    k: candidates[0].get(k)
                    for k in (
                        "history_item_id",
                        "request_id",
                        "date_unix",
                        "character_count_change_from",
                        "character_count_change_to",
                    )
                }
            )
        rows.append(row)
    result = {
        "schema_version": 1,
        "collection": index["collection"],
        "tts": rows,
        "sfx": "ElevenLabs history API does not return sound effects. Retain named local originals and upload receipts.",
    }
    write(output / "provider-history-index.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "generate", "check", "mix", "history-index"])
    parser.add_argument("--manifest", type=Path, default=ROOT / "media/walkthrough/edit.json")
    parser.add_argument("--config", type=Path, default=ROOT / "media/walkthrough/audio.json")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/walkthrough-production/audio")
    parser.add_argument(
        "--video", type=Path, default=ROOT / "dist/walkthrough-production/forge-workshops-clean.mp4"
    )
    parser.add_argument(
        "--video-receipt", type=Path, help="Production receipt with the input video SHA256"
    )
    parser.add_argument(
        "--visual-manifest", type=Path, help="Resolved visual edit used to render the input video"
    )
    parser.add_argument("--destination", type=Path, default=ROOT / "dist/walkthrough-production")
    parser.add_argument(
        "--env-file",
        type=Path,
        help="Read only the ElevenLabs key from this explicitly selected file",
    )
    parser.add_argument(
        "--only", action="append", help="Generate only this asset ID; repeat for several assets"
    )
    parser.add_argument(
        "--retry-rejected",
        action="store_true",
        help="Explicitly retry a prior HTTP 4xx rejection; never retries uncertain requests",
    )
    args = parser.parse_args()
    manifest, config = load(args.manifest), load(args.config)
    plan = make_plan(manifest, config)
    output = args.output.resolve()
    write(output / "plan.json", plan)
    if args.command == "plan":
        print(
            json.dumps(
                {
                    k: plan[k]
                    for k in (
                        "collection",
                        "seconds",
                        "characters",
                        "paid_tts_requests",
                        "paid_sfx_requests",
                    )
                }
            )
        )
        for row in plan["assets"]:
            if row["kind"] == "tts":
                print(
                    f"{row['asset_id']}: {row['duration']:g}s, {row['characters']} characters, {row['required_words_per_minute']} words/minute"
                )
        return
    if args.command == "generate":
        selected = [row for row in plan["assets"] if not args.only or row["asset_id"] in args.only]
        unknown = set(args.only or ()) - {row["asset_id"] for row in selected}
        if unknown:
            raise ValueError("Unknown asset ID: " + ", ".join(sorted(unknown)))
        key = load_api_key(args.env_file)
        try:
            for row in selected:
                receipt = generate_one(row, output, key, args.retry_rejected)
                print(f"{row['asset_id']}: {receipt['status']}", flush=True)
                if row["kind"] == "tts":
                    duration = float(
                        probe(output / row["directory"] / receipt["audio_file"])["format"][
                            "duration"
                        ]
                    )
                    fit_audio(duration, row["duration"], config["timing"])
        finally:
            audio_index(plan, output, config)
        return
    index = audio_index(plan, output, config, require_complete=args.command in ("check", "mix"))
    if args.command == "check":
        print(
            json.dumps(
                {"complete": True, "assets": len(index["assets"]), "seconds": index["seconds"]}
            )
        )
    elif args.command == "mix":
        receipt = mix(
            index,
            config,
            output,
            args.video.resolve(),
            args.destination.resolve(),
            args.video_receipt,
            args.visual_manifest,
        )
        print(json.dumps({"seconds": receipt["seconds"], "outputs": list(receipt["outputs"])}))
    elif args.command == "history-index":
        result = history_index(index, output, load_api_key(args.env_file))
        print(
            json.dumps(
                {
                    "tts": len(result["tts"]),
                    "matched": sum(row["status"] == "matched" for row in result["tts"]),
                }
            )
        )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, FileNotFoundError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
