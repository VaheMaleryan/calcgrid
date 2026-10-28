#!/usr/bin/env python3
"""
PayoutFolio local preview and private operator dashboard.
Serves `dist/` on loopback only. This server does not ingest telemetry or receive payments.
"""

import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"
LOGS_DIR = ROOT_DIR / "logs"
TELEMETRY_LOG = LOGS_DIR / "telemetry.jsonl"
REPORT_FILE = LOGS_DIR / "autopilot_report.json"


class CalcGridServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def translate_path(self, path):
        translated = super().translate_path(path)
        clean_page = Path(translated + ".html")
        return str(clean_page) if not Path(translated).exists() and clean_page.is_file() else translated

    def do_GET(self):
        if self.path == "/api/health":
            report = {}
            if REPORT_FILE.exists():
                try:
                    report = json.loads(REPORT_FILE.read_text(encoding="utf-8"))
                except Exception:
                    pass
            self._send_json(200, {"ok": True, "status": "passed" if report.get("all_checks_passed") else "not_verified", "autopilot": report})
            return
        if self.path.startswith("/admin/dashboard"):
            priv_dash = LOGS_DIR / "private_dashboard.html"
            if priv_dash.exists():
                body = priv_dash.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
        super().do_GET()

    def do_POST(self):
        # The static release has no telemetry ingestion or payment receiver.
        self._send_json(404, {"ok": False})

    def end_headers(self):
        headers = DIST_DIR / "_headers"
        if headers.exists():
            for line in headers.read_text(encoding="utf-8").splitlines():
                if line.startswith("  ") and ":" in line:
                    name, value = line.strip().split(":", 1)
                    self.send_header(name, value.strip())
        super().end_headers()

    def _send_json(self, code: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8098))
    # Browsers keep speculative connections open; one idle socket must not block the preview.
    server = ThreadingHTTPServer(("127.0.0.1", port), CalcGridServerHandler)
    print(f"PayoutFolio local preview running at http://localhost:{port}")
    server.serve_forever()
