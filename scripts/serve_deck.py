"""Serve an offline deck on loopback, including direct slide links."""

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--port", type=int, default=8047)
args = parser.parse_args()
root = Path(__file__).resolve().parent


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(root), **kwargs)

    def do_GET(self):
        requested = Path(self.translate_path(urlsplit(self.path).path))
        if not requested.exists() and not requested.suffix:
            self.path = "/index.html"
        super().do_GET()


with ThreadingHTTPServer(("127.0.0.1", args.port), Handler) as server:
    print(f"Open http://127.0.0.1:{server.server_port}/1", flush=True)
    server.serve_forever()
