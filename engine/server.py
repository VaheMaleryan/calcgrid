#!/usr/bin/env python3
"""
CalcGrid Static Preview, Telemetry Receiver & Health Monitoring Server.
Serves the compiled static site from `dist/` and logs client telemetry/error beacons to `logs/telemetry.jsonl`.
"""

import json
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"
LOGS_DIR = ROOT_DIR / "logs"
TELEMETRY_LOG = LOGS_DIR / "telemetry.jsonl"
REPORT_FILE = LOGS_DIR / "autopilot_report.json"


class CalcGridServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            report = {}
            if REPORT_FILE.exists():
                try:
                    report = json.loads(REPORT_FILE.read_text(encoding="utf-8"))
                except Exception:
                    pass
            self._send_json(200, {"ok": True, "status": "healthy", "autopilot": report})
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
        if self.path == "/api/telemetry":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8", errors="ignore")
            LOGS_DIR.mkdir(parents=True, exist_ok=True)
            with open(TELEMETRY_LOG, "a", encoding="utf-8") as f:
                f.write(raw.strip() + "\n")
            self._send_json(200, {"ok": True})
            return
        self._send_json(404, {"ok": False})

    def _send_json(self, code: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8098))
    server = HTTPServer(("0.0.0.0", port), CalcGridServerHandler)
    print(f"🚀 CalcGrid Live Server + Telemetry Monitor running at http://localhost:{port}")
    server.serve_forever()
