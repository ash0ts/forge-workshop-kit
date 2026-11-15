"""Build accessible ARIA transcripts and source excerpts from actual saved chats.

This command reads recordings already captured in Forge. It never sends a prompt,
retrieves a record, or substitutes a response for a missing conversation.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/forge_workshop_kit/assets/aria"
STYLE = """
:root { color-scheme:light dark; --paper:#f7f3e8; --ink:#142c32; --accent:#136b70; --line:#bec9c4; }
@media(prefers-color-scheme:dark) { :root { --paper:#152528; --ink:#ecede3; --accent:#8cdbce; --line:#526968; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink); font:18px/1.55 system-ui,sans-serif; }
main { max-width:1080px; margin:auto; padding:32px 28px; }
h1 { font-size:clamp(1.8rem,4vw,3rem); line-height:1.14; margin:.5em 0; }
h2 { font-size:1.35rem; margin-top:1.6em; }
a { color:var(--accent); overflow-wrap:anywhere; }
a:focus-visible,summary:focus-visible { outline:3px solid var(--accent); outline-offset:4px; }
.notice { padding:16px 20px; border-left:5px solid var(--accent); }
table { width:100%; border-collapse:collapse; table-layout:fixed; }
th,td { padding:12px; border-bottom:1px solid var(--line); vertical-align:top; text-align:left; overflow-wrap:anywhere; }
th:first-child,td:first-child { width:35%; }
pre { white-space:pre-wrap; overflow-wrap:anywhere; font:14px/1.6 ui-monospace,monospace; padding:18px; border:1px solid var(--line); border-radius:8px; }
.response { white-space:pre-wrap; overflow-wrap:anywhere; padding:20px; border:1px solid var(--line); }
img { display:block; max-width:100%; height:auto; }
.capture-frame { position:relative; }
.capture-box { position:absolute; border:2px solid #ffcf66; pointer-events:none; }
.capture-box b { position:absolute; top:-1.2em; left:-2px; padding:0 6px; color:#142c32; background:#ffcf66; font:700 13px/1.4 system-ui,sans-serif; }
small { opacity:.8; }
@media(max-width:600px) { main { padding:20px 16px; } th,td { padding:8px 5px; font-size:15px; } }
"""


def excerpt_from_prompt(prompt: str) -> dict | list:
    marker = "Saved evidence excerpts:"
    if marker not in prompt:
        raise ValueError("The actual prompt has no saved-evidence excerpt; supply the captured source separately.")
    value, _ = json.JSONDecoder().raw_decode(prompt.split(marker, 1)[1].lstrip())
    if not isinstance(value, (dict, list)):
        raise TypeError("A saved-evidence excerpt must contain structured records.")
    return value


def flatten(value, prefix=""):
    """Keep source field names and values; do not turn data into inferred claims."""
    if isinstance(value, dict):
        for key, child in value.items():
            yield from flatten(child, f"{prefix}.{key}" if prefix else str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from flatten(child, f"{prefix}[{index}]")
    else:
        yield prefix, value


def page(title: str, content: str) -> str:
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title><style>{STYLE}</style></head>'
            f'<body><main><h1>{html.escape(title)}</h1>{content}</main></body></html>')


def source_links(records: list[dict]) -> str:
    items = []
    for row in records:
        url = row.get("url") or row.get("trace_url") or row.get("run_url")
        label = row.get("label") or row.get("stage_name") or row.get("identity") or row.get("stage_id") or "Saved source"
        if url and url.startswith("https://"):
            items.append(f'<li><a href="{html.escape(url, quote=True)}">{html.escape(label)}</a></li>')
        else:
            items.append(f'<li>{html.escape(label)}: native link unavailable</li>')
    return "<ul>" + "".join(items) + "</ul>"


def attached_images(recording: dict, folder: Path) -> str:
    """Show only media explicitly recorded as attached to this ARIA question."""
    figures = []
    for attachment in recording.get("attachments", []):
        file = Path(attachment["path"])
        if file.name != attachment["path"] or not (folder / file).is_file():
            raise ValueError(f"Missing or invalid attachment: {attachment['path']}")
        caption = attachment.get("caption", "Image attached to the recorded question")
        figures.append(f'<figure><img src="{html.escape(file.name, quote=True)}" alt="{html.escape(caption, quote=True)}"><figcaption>{html.escape(caption)}</figcaption></figure>')
    return '<h2>Images attached to this question</h2>' + "".join(figures) if figures else ""


def capture_annotations(capture: dict) -> tuple[str, str]:
    boxes, labels = [], []
    for index, annotation in enumerate(capture.get("annotations", []), 1):
        x, y, width, height = (float(annotation[key]) for key in ("x", "y", "width", "height"))
        if not (0 <= x < 1 and 0 <= y < 1 and width > 0 and height > 0 and x + width <= 1 and y + height <= 1):
            raise ValueError("Screenshot annotations must stay within the original image.")
        boxes.append(f'<span class="capture-box" style="left:{100*x}%;top:{100*y}%;width:{100*width}%;height:{100*height}%" aria-hidden="true"><b>{index}</b></span>')
        labels.append(f'<li>{html.escape(annotation["label"])}</li>')
    return "".join(boxes), "<ol>" + "".join(labels) + "</ol>" if labels else ""


def build_recording(path: Path) -> dict:
    recording = json.loads(path.read_text(encoding="utf-8"))
    if recording.get("status") != "recorded":
        return {"path": str(path), "status": "not recorded; no transcript generated"}
    if not all(recording.get(key) for key in ("prompt", "response", "conversation_url", "citation_check")):
        raise ValueError(f"Incomplete actual recording: {path}")
    if not isinstance(recording["response"], str):
        raise TypeError(f"Response must be the captured text: {path}")
    stop = recording["stop_id"]
    if stop not in ("investigate", "conclusion") or path.name != stop + ".json":
        raise ValueError(f"Unexpected stop identity: {path}")
    prompt = recording["prompt"]
    excerpt = excerpt_from_prompt(prompt)
    records = recording.get("records", [])
    context = recording.get("context_method", "Context method was not recorded.")
    title = recording["workshop"].replace("_", " ").title() + " / " + ("Investigate this result" if stop == "investigate" else "Check our conclusion")
    source_name = stop + "-source-records"
    transcript_name = stop + "-transcript"
    source = {
        "kind": "saved-record excerpt; not a Forge screenshot",
        "recording_id": recording["id"],
        "recorded_at": recording.get("recorded_at"),
        "context_method": context,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "records": records,
        "excerpt": excerpt,
        "supplemental_evidence": recording.get("supplemental_evidence", {}),
        "attachments": recording.get("attachments", []),
        "citation_check": recording["citation_check"],
    }
    (path.parent / (source_name + ".json")).write_text(json.dumps(source, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rows = "".join(f'<tr><th scope="row">{html.escape(field)}</th><td>{html.escape(json.dumps(value, ensure_ascii=False))}</td></tr>' for field, value in flatten(excerpt))
    source_body = ('<p class="notice"><strong>Saved-record excerpt.</strong> These are the exact values supplied in the instructor’s recorded prompt. This page is a local teaching view, not a native Forge capture and not a participant execution.</p>'
                   f'<p>{html.escape(context)}</p><h2>Open the source records</h2>{source_links(records)}'
                   f'<h2>Values supplied to ARIA</h2><table><thead><tr><th>Source field</th><th>Recorded value</th></tr></thead><tbody>{rows}</tbody></table>'
                   f'<details><summary>Complete supplied excerpt</summary><pre>{html.escape(json.dumps(excerpt, indent=2, ensure_ascii=False))}</pre></details>'
                   f'<p><a href="{transcript_name}.html">Read the actual ARIA conversation</a></p>')
    if recording.get("supplemental_evidence"):
        source_body += '<h2>Additional context supplied with this question</h2><pre>' + html.escape(json.dumps(recording["supplemental_evidence"], indent=2, ensure_ascii=False)) + '</pre>'
    source_body += attached_images(recording, path.parent)
    (path.parent / (source_name + ".html")).write_text(page(title + " / source values", source_body), encoding="utf-8")
    check = recording["citation_check"]
    md = [f"# {title}", "", "**Recorded instructor investigation.** These are saved instructor records, not the outcome of an unexecuted participant edit.", "", f"Recorded: {recording.get('recorded_at', 'unavailable')}", "", f"Context: {context}", "", f"[ARIA conversation]({recording['conversation_url']})", "", f"[Offline source values]({source_name}.html)", "", "## Exact submitted prompt", "", "```text", prompt, "```", "", "## Actual ARIA response", "", recording["response"], "", "## Instructor citation check", "", f"Claim: {check.get('claim', '')}", "", f"Assessment: {check.get('assessment', 'unresolved')}", "", check.get("reason", ""), ""]
    if check.get("record_url"):
        md += [f"[Checked record]({check['record_url']})", ""]
    for attachment in recording.get("attachments", []):
        md += [f"![{attachment.get('caption', 'Attached image')}]({attachment['path']})", ""]
    transcript = "\n".join(md)
    (path.parent / (transcript_name + ".md")).write_text(transcript, encoding="utf-8")
    body = ('<p class="notice"><strong>Recorded instructor investigation.</strong> These are saved instructor records, not the outcome of an unexecuted participant edit.</p>'
            f'<p>{html.escape(context)}</p><p><a href="{html.escape(recording["conversation_url"], quote=True)}">Open the actual ARIA conversation</a> · <a href="{source_name}.html">Check the supplied source values offline</a></p>'
            f'<h2>Exact submitted prompt</h2><pre>{html.escape(prompt)}</pre>'
            f'<h2>Actual ARIA response</h2><div class="response">{html.escape(recording["response"])}</div>'
            f'<h2>Instructor citation check</h2><p><strong>{html.escape(check.get("assessment", "unresolved"))}:</strong> {html.escape(check.get("claim", ""))}</p><p>{html.escape(check.get("reason", ""))}</p>')
    body += attached_images(recording, path.parent)
    if check.get("record_url", "").startswith("https://"):
        body += f'<p><a href="{html.escape(check["record_url"], quote=True)}">Open the checked record in Forge</a></p>'
    for capture in recording.get("captures", []):
        file = Path(capture["path"])
        if file.name != capture["path"] or not (path.parent / file).is_file():
            raise ValueError(f"Missing or invalid capture: {capture['path']}")
        caption = html.escape(capture.get("caption", ""))
        caption += f' <a href="{html.escape(file.name, quote=True)}">Open the original capture at full size</a>.'
        if capture.get("source_url", "").startswith("https://"):
            caption += f' <a href="{html.escape(capture["source_url"], quote=True)}">Open this view in Forge</a>.'
        boxes, labels = capture_annotations(capture)
        body += f'<figure><div class="capture-frame"><img src="{html.escape(file.name, quote=True)}" alt="{html.escape(capture.get("caption", "Native product capture"), quote=True)}">{boxes}</div><figcaption>{caption}{labels}</figcaption></figure>'
    (path.parent / (transcript_name + ".html")).write_text(page(title, body), encoding="utf-8")
    recording["excerpt_path"] = source_name + ".json"
    recording["excerpt_html"] = source_name + ".html"
    recording["transcript_paths"] = {"markdown": transcript_name + ".md", "html": transcript_name + ".html"}
    path.write_text(json.dumps(recording, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"workshop": recording["workshop"], "stop_id": stop, "status": "built", "source_fields": len(list(flatten(excerpt)))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, default=ASSETS)
    args = parser.parse_args()
    paths = sorted([*args.assets.glob("*/investigate.json"), *args.assets.glob("*/conclusion.json")])
    print(json.dumps([build_recording(path) for path in paths], indent=2))


if __name__ == "__main__":
    main()
