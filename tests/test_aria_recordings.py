"""An offline transcript must preserve the actual submitted prompt and response."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_aria_recordings", ROOT / "scripts/build_aria_recordings.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def test_extracts_exact_values_before_optional_prompt_suffix():
    prompt = 'Context\nSaved evidence excerpts: {"message":"line\\nnext", "score":0.0}\nDo not launch anything.'
    assert BUILDER.excerpt_from_prompt(prompt) == {"message": "line\nnext", "score": 0.0}


def test_build_preserves_actual_response_and_marks_source_as_local(tmp_path):
    response = "Synthetic test response: <a> & quoted `field`.\nSecond line."
    prompt = 'Saved evidence excerpts: {"event":{"result":"Skill not installed"}}\nKeep this exact suffix.'
    recording = {
        "id": "test-recording", "workshop": "pending_inc", "stop_id": "investigate",
        "status": "recorded", "recorded_at": "2026-11-15T00:00:00Z", "prompt": prompt,
        "response": response, "conversation_url": "https://example.org/conversation",
        "records": [{"identity": "run-1", "label": "Saved fixture", "url": "https://example.org/run"}],
        "context_method": "Synthetic test fixture; no live ARIA request.",
        "citation_check": {"claim": "Fixture", "assessment": "unresolved", "reason": "A unit test.", "record_url": "https://example.org/run"},
    }
    path = tmp_path / "investigate.json"
    path.write_text(json.dumps(recording))
    result = BUILDER.build_recording(path)
    saved = json.loads(path.read_text())
    assert result["status"] == "built"
    assert saved["response"] == response and saved["prompt"] == prompt
    assert response in (tmp_path / "investigate-transcript.md").read_text()
    assert "&lt;a&gt; &amp;" in (tmp_path / "investigate-transcript.html").read_text()
    assert 'href="https://example.org/run">Open the checked record' in (tmp_path / "investigate-transcript.html").read_text()
    assert "not a native Forge capture" in (tmp_path / "investigate-source-records.html").read_text()
    assert json.loads((tmp_path / saved["excerpt_path"]).read_text())["excerpt"] == {"event": {"result": "Skill not installed"}}


def test_unavailable_chat_never_gets_a_synthetic_transcript(tmp_path):
    path = tmp_path / "investigate.json"
    path.write_text(json.dumps({"status": "unavailable"}))
    result = BUILDER.build_recording(path)
    assert result["status"] == "not recorded; no transcript generated"
    assert list(tmp_path.iterdir()) == [path]


def test_actual_recording_requires_a_captured_response(tmp_path):
    path = tmp_path / "investigate.json"
    path.write_text(json.dumps({"status": "recorded", "prompt": "question"}))
    with pytest.raises(ValueError, match="Incomplete actual recording"):
        BUILDER.build_recording(path)


def test_attached_image_stays_identified_and_requires_local_file(tmp_path):
    attachment = {"path": "board.jpg", "caption": "Actual validation photograph; attached through Add images."}
    with pytest.raises(ValueError, match="Missing or invalid attachment"):
        BUILDER.attached_images({"attachments": [attachment]}, tmp_path)
    (tmp_path / "board.jpg").write_bytes(b"synthetic image bytes for path check")
    rendered = BUILDER.attached_images({"attachments": [attachment]}, tmp_path)
    assert 'src="board.jpg"' in rendered
    assert attachment["caption"] in rendered


def test_annotation_keeps_original_coordinates_and_text_alternative():
    boxes, labels = BUILDER.capture_annotations({"annotations": [{"x": .25, "y": .5, "width": .4, "height": .2, "label": "Returned booking"}]})
    assert "left:25.0%;top:50.0%;width:40.0%;height:20.0%" in boxes
    assert "Returned booking" in labels
    with pytest.raises(ValueError, match="within the original image"):
        BUILDER.capture_annotations({"annotations": [{"x": .9, "y": .5, "width": .4, "height": .2, "label": "Outside"}]})
