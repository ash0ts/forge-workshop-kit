"""Check local resources needed by a built deck without opening a browser."""

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def check(deck, built, prefix="/"):
    deck, built = Path(deck), Path(built)
    references = set()
    # Slide source includes images and the explicit frame source for every reveal.
    slides = html.unescape((deck / "slides.md").read_text())
    references.update(re.findall(r'(?:src|href)=["\']([^"\']+)["\']', slides))
    references.update(re.findall(r'"src":\s*"([^"]+)"', slides))
    source = (built / "index.html").read_text()
    references.update(re.findall(r'<(?:script|link|img)\b[^>]*(?:src|href)=["\']([^"\']+)["\']', source))
    missing, remote, checked = [], [], []
    for reference in sorted(references):
        value = urlsplit(reference)
        if value.scheme or value.netloc or not value.path:
            continue
        path = unquote(value.path)
        # External source links and slide aliases are not rendering assets.
        if Path(path).suffix not in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".js", ".css", ".woff", ".woff2", ".html"}:
            continue
        if path.startswith(prefix):
            file = built / path[len(prefix):]
        elif path.startswith("/"):
            # Generated source has local-root paths even for the hosted build.
            file = built / path.lstrip("/")
        else:
            file = built / path
        checked.append(reference)
        if not file.is_file():
            missing.append(reference)
    for css in built.rglob("*.css"):
        for reference in re.findall(r'url\(["\']?([^\)"\']+)', css.read_text()):
            value = urlsplit(reference)
            if value.scheme in {"http", "https"} or value.netloc:
                remote.append(reference)
            elif not value.scheme and value.path:
                file = (built / value.path[len(prefix):]) if value.path.startswith(prefix) else css.parent / value.path
                checked.append(str(css.relative_to(built)) + ":" + reference)
                if not file.is_file():
                    missing.append(str(css.relative_to(built)) + ":" + reference)
    remote.extend(re.findall(r'<(?:script|link|img)\b[^>]*(?:src|href)=["\'](https?://[^"\']+)', source))
    remote.extend(re.findall(r'<(?:script|img|iframe)\b[^>]*src=["\'](https?://[^"\']+)', slides))
    return {"deck": str(deck), "build": str(built), "checked_assets": len(checked),
            "missing": sorted(set(missing)), "remote_render_dependencies": sorted(set(remote))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path)
    parser.add_argument("build", type=Path)
    parser.add_argument("--prefix", default="/")
    args = parser.parse_args()
    result = check(args.deck, args.build, args.prefix)
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["missing"] or result["remote_render_dependencies"]))
