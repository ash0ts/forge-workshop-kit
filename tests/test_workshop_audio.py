"""Audio contract checks use local responses; they never contact ElevenLabs."""

import array
import base64
import importlib.util
import json
import shutil
import urllib.error
import wave
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "workshop_audio", ROOT / "scripts/build_workshop_audio.py"
)
audio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio)


def configuration():
    value = audio.load(ROOT / "media/walkthrough/audio.json")
    value["sound_effects"] = []
    value["effect_placements"] = []
    return value


def manifest():
    return {
        "chapters": [
            {
                "id": "intro",
                "title": "Introduction",
                "duration": 10,
                "shots": [{"capture": "intro", "duration": 10, "narration": ["Hello there."]}],
            }
        ]
    }


def alignment(text="Hello there."):
    return {
        "characters": list(text),
        "character_start_times_seconds": [i * 0.1 for i in range(len(text))],
        "character_end_times_seconds": [(i + 1) * 0.1 for i in range(len(text))],
    }


def response():
    return json.dumps(
        {"audio_base64": base64.b64encode(b"ID3fixture").decode(), "alignment": alignment()}
    ).encode()


def first():
    return audio.make_plan(manifest(), configuration())["assets"][0]


def test_plan_uses_selected_voice_and_no_calls(monkeypatch):
    monkeypatch.setattr(audio, "request_json", lambda *a, **k: pytest.fail("Network call"))
    plan = audio.make_plan(manifest(), configuration())
    assert plan["seconds"] == 10
    assert plan["paid_tts_requests"] == 1
    row = plan["assets"][0]
    assert row["voice_id"] == "QIhD5ivPGEoYZQDocuHI"
    assert "with-timestamps" in row["request"]["path"]
    assert row["request"]["payload"]["model_id"] == "eleven_multilingual_v2"
    assert row["request"]["payload"]["voice_settings"]["speed"] == 1


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="FFmpeg not installed")
def test_voice_clip_has_exact_samples_and_delayed_audio(tmp_path):
    source, output = tmp_path / "tone.mp3", tmp_path / "slot.wav"
    audio.run(
        [
            audio.tool("ffmpeg"),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:duration=1:sample_rate=44100",
            "-c:a",
            "libmp3lame",
            source,
        ]
    )
    audio.prepare_voice_clip(source, output, 3.25, 1.04, 0.65, -18)
    with wave.open(str(output), "rb") as result:
        assert result.getframerate() == 48000
        assert result.getnframes() == 156000
        values = array.array("h", result.readframes(result.getnframes()))
        # The stereo lead is silence; the generated signal follows it. Checking
        # the container duration alone misses a short audio track in a long video.
        first = next(i // 2 for i, value in enumerate(values) if abs(value) > 20)
        assert 0.64 < first / 48000 < 0.68
        assert max(abs(value) for value in values[-9600:]) == 0
    with pytest.raises(ValueError, match="Wrong sample count"):
        audio.verify_wav_duration(output, 4)


def test_new_text_gets_new_request_and_timing_does_not():
    old = first()
    edit = manifest()
    edit["chapters"][0]["duration"] = 12
    edit["chapters"][0]["shots"][0]["duration"] = 12
    assert (
        audio.make_plan(edit, configuration())["assets"][0]["request_sha256"]
        == old["request_sha256"]
    )
    edit["chapters"][0]["shots"][0]["narration"] = ["Different narration."]
    assert (
        audio.make_plan(edit, configuration())["assets"][0]["request_sha256"]
        != old["request_sha256"]
    )


def test_success_is_reused_and_files_checked(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(
        audio,
        "request_json",
        lambda *args: (calls.append(args) or response(), {"request-id": "req1"}),
    )
    row = first()
    result = audio.generate_one(row, tmp_path, "not-a-key")
    assert result["status"] == "completed"
    assert result["provider_headers"] == {"request-id": "req1"}
    assert audio.generate_one(row, tmp_path, "not-a-key") == result
    assert len(calls) == 1
    (tmp_path / row["directory"] / "audio.mp3").write_bytes(b"changed")
    with pytest.raises(ValueError, match="saved audio missing or changed"):
        audio.generate_one(row, tmp_path, "not-a-key")
    assert len(calls) == 1


def test_ambiguous_request_never_retries(tmp_path, monkeypatch):
    calls = []

    def uncertain(*args):
        calls.append(args)
        raise TimeoutError()

    monkeypatch.setattr(audio, "request_json", uncertain)
    row = first()
    with pytest.raises(RuntimeError, match="uncertain"):
        audio.generate_one(row, tmp_path, "not-a-key")
    with pytest.raises(RuntimeError, match="Do not resend"):
        audio.generate_one(row, tmp_path, "not-a-key", retry_rejected=True)
    assert len(calls) == 1
    assert audio.load(tmp_path / row["directory"] / "receipt.json")["status"] == "uncertain"


def test_saved_response_recovers_without_request(tmp_path, monkeypatch):
    row = first()
    directory = tmp_path / row["directory"]
    audio.write(
        directory / "receipt.json",
        {"status": "response_saved", "request_sha256": row["request_sha256"]},
    )
    (directory / "response.bin").write_bytes(response())
    monkeypatch.setattr(audio, "request_json", lambda *a, **k: pytest.fail("Duplicate paid call"))
    result = audio.generate_one(row, tmp_path, "not-a-key")
    assert result["status"] == "completed"
    assert result["alignment_file"] == "alignment.json"


def test_concurrent_generation_is_blocked(tmp_path, monkeypatch):
    row = first()
    directory = tmp_path / row["directory"]
    directory.mkdir(parents=True)
    (directory / "generation.lock").write_text("12345")
    monkeypatch.setattr(audio, "request_json", lambda *a, **k: pytest.fail("Duplicate paid call"))
    with pytest.raises(RuntimeError, match="generation lock"):
        audio.generate_one(row, tmp_path, "not-a-key")


def test_rejected_retry_is_explicit_and_preserves_failed_attempt(tmp_path, monkeypatch):
    row = first()

    def reject(*args):
        raise urllib.error.HTTPError("https://api.elevenlabs.io", 401, "Unauthorized", {}, None)

    monkeypatch.setattr(audio, "request_json", reject)
    with pytest.raises(RuntimeError, match="rejected"):
        audio.generate_one(row, tmp_path, "not-a-key")
    with pytest.raises(RuntimeError, match="Do not resend"):
        audio.generate_one(row, tmp_path, "not-a-key")
    monkeypatch.setattr(audio, "request_json", lambda *args: (response(), {}))
    assert (
        audio.generate_one(row, tmp_path, "not-a-key", retry_rejected=True)["status"] == "completed"
    )
    attempts = list((tmp_path / row["directory"] / "attempts").glob("*.json"))
    assert len(attempts) == 1
    assert audio.load(attempts[0])["http_status"] == 401


def test_caption_times_come_from_alignment_not_word_count():
    value = alignment("Hi. Slow words.")
    # This word really begins much later in the provider's audio.
    value["character_start_times_seconds"] = [
        i * 0.1 if i < 4 else 3 + (i - 4) * 0.2 for i in range(15)
    ]
    value["character_end_times_seconds"] = [n + 0.1 for n in value["character_start_times_seconds"]]
    cues = audio.caption_cues(value, 20.65, 1.05, "intro-00")
    assert cues[0]["text"] == "Hi."
    assert cues[1]["text"] == "Slow words."
    assert cues[1]["start"] == pytest.approx(20.65 + 3 / 1.05, abs=0.0001)
    assert cues[1]["asset_id"] == "intro-00"


def test_overrun_is_reported_never_clipped():
    timing = configuration()["timing"]
    assert audio.fit_audio(8, 10, timing) == 1
    assert audio.fit_audio(9.5, 10, timing) == pytest.approx(
        9.5 / (10 - timing["lead_seconds"] - timing["tail_seconds"])
    )
    with pytest.raises(ValueError, match="will not be clipped"):
        audio.fit_audio(10, 10, timing)


def test_env_file_reads_only_key_alias_without_execution(tmp_path, monkeypatch):
    selected = tmp_path / "selected.env"
    selected.write_text(
        "OTHER_SECRET=should-not-be-used\nexport ELEVEN_LABS_API_KEY='fixture-key' # comment\n"
    )
    monkeypatch.setenv("ELEVENLABS_API_KEY", "different-key")
    assert audio.load_api_key(selected) == "fixture-key"
    selected.write_text("ELEVENLABS_API_KEY=$(bad-command)\n")
    with pytest.raises(ValueError, match="literal"):
        audio.load_api_key(selected)


def test_malformed_alignment_does_not_become_captions():
    bad = alignment()
    bad["character_end_times_seconds"] = []
    with pytest.raises(ValueError, match="different lengths"):
        audio.caption_cues(bad, 0, 1, "intro-00")


def test_checked_index_uses_actual_duration_and_keeps_asset_hash(tmp_path, monkeypatch):
    plan = audio.make_plan(manifest(), configuration())
    monkeypatch.setattr(audio, "request_json", lambda *args: (response(), {}))
    audio.generate_one(plan["assets"][0], tmp_path, "not-a-key")
    monkeypatch.setattr(audio, "probe", lambda path: {"format": {"duration": "3.2"}})
    result = audio.audio_index(plan, tmp_path, configuration(), require_complete=True)
    assert result["complete"]
    assert result["assets"][0]["audio_duration"] == 3.2
    assert result["assets"][0]["tempo"] == 1
    assert result["assets"][0]["audio_sha256"]
    assert (tmp_path / result["assets"][0]["audio_file"]).exists()


def test_saved_response_hash_is_checked_before_recovery(tmp_path, monkeypatch):
    row = first()
    directory = tmp_path / row["directory"]
    audio.write(
        directory / "receipt.json",
        {
            "status": "response_saved",
            "request_sha256": row["request_sha256"],
            "response_sha256": "wrong",
        },
    )
    (directory / "response.bin").write_bytes(response())
    monkeypatch.setattr(audio, "request_json", lambda *a, **k: pytest.fail("Duplicate paid call"))
    with pytest.raises(ValueError, match="Saved provider response changed"):
        audio.generate_one(row, tmp_path, "not-a-key")


def test_sound_placement_is_checked_before_generation():
    config = configuration()
    config["effect_placements"] = [{"effect": "missing", "chapter": "intro"}]
    with pytest.raises(ValueError, match="defined effect and chapter"):
        audio.make_plan(manifest(), config)


def test_video_identity_ignores_words_but_rejects_wrong_same_length_video(tmp_path):
    source = manifest()
    plan = audio.make_plan(source, configuration())
    video = tmp_path / "clean.mp4"
    video.write_bytes(b"saved video bytes")
    audio.write(
        tmp_path / "production-receipt.json",
        {"outputs": {"clean.mp4": {"sha256": audio.sha(video)}}},
    )
    changed_words = manifest()
    changed_words["chapters"][0]["shots"][0]["narration"] = ["Rewritten explanation."]
    audio.write(tmp_path / "edit-resolved.json", changed_words)
    assert audio.verify_video_source(plan, video)["visual_sha256"] == plan["visual_sha256"]
    wrong_shot = manifest()
    wrong_shot["chapters"][0]["shots"][0]["capture"] = "some-other-record"
    audio.write(tmp_path / "edit-resolved.json", wrong_shot)
    with pytest.raises(ValueError, match="different shots"):
        audio.verify_video_source(plan, video)
    audio.write(tmp_path / "edit-resolved.json", source)
    video.write_bytes(b"another video of the same duration")
    with pytest.raises(ValueError, match="Video bytes"):
        audio.verify_video_source(plan, video)
