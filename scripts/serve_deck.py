"""Serve an offline deck on loopback, including direct slide links."""

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import webbrowser

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--port", type=int, default=0, help="Local port; 0 chooses an available port")
parser.add_argument("--open", action="store_true", help="Open the presentation in your browser")
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


try:
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
except OSError as error:
    parser.exit(1, f"Cannot listen on port {args.port}: {error}. Try --port 0.\n")
with server:
    address = f"http://127.0.0.1:{server.server_port}/1"
    print(f"Open {address}\nKeep this terminal open. Press Ctrl-C to stop.", flush=True)
    if args.open:
        webbrowser.open(address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
