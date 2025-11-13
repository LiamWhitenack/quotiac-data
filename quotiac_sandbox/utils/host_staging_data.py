from collections.abc import Callable
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


def serve_json_dict(port: int = 6942) -> Callable[[dict[str, Any]], None]:
    """Start a server on localhost that serves the latest dictionary as JSON."""
    latest_data = {"message": "Initial placeholder"}

    class JSONHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != "/data.json":
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found")
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(latest_data).encode("utf-8"))

        def log_message(self, format, *args):  # type: ignore
            return  # Suppress logging

    def start_server():
        server = HTTPServer(("", port), JSONHandler)
        print(f"Serving JSON at http://localhost:{port}/data.json")
        server.serve_forever()

    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()

    def update(data: dict[str, Any]) -> None:
        nonlocal latest_data
        latest_data = data

    return update
