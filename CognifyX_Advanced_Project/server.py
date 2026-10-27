"""CognifyX local demo server; uses only Python's standard library."""
from __future__ import annotations
import json
import mimetypes
import os
import shutil
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
SOURCE = ROOT / "c_engine" / "cognifyx_engine.c"
BINARY = BUILD / ("cognifyx_engine.exe" if os.name == "nt" else "cognifyx_engine")
PORT = int(os.environ.get("COGNIFYX_PORT", "8765"))


def compile_engine() -> bool:
    BUILD.mkdir(exist_ok=True)
    compiler = shutil.which("gcc") or shutil.which("clang")
    if not compiler:
        print("[WARN] C compiler not found. Dashboard will use built-in JavaScript fallback scoring.")
        print("       Install GCC/MinGW-w64 and add gcc to PATH to enable the C engine.")
        return False
    command = [compiler, "-std=c11", "-O2", "-Wall", "-Wextra", str(SOURCE), "-o", str(BINARY)]
    try:
        res = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            print("[WARN] C engine compilation failed; browser fallback remains available.")
            if res.stderr:
                print(res.stderr.strip())
            return False
        print(f"[OK] C engine compiled: {BINARY.name}")
        return True
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"[WARN] Could not compile C engine: {exc}")
        return False


def run_engine(*args: str) -> dict:
    if not BINARY.exists():
        raise RuntimeError("C engine is not compiled")
    proc = subprocess.run([str(BINARY), *map(str, args)], capture_output=True, text=True, timeout=5)
    if proc.returncode != 0:
        raise ValueError(proc.stderr.strip() or "C engine rejected the request")
    return json.loads(proc.stdout)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        print("[HTTP] " + (fmt % args))

    def send_json(self, status: int, payload: dict):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "same-origin")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            args = parse_qs(parsed.query)
            try:
                if parsed.path == "/api/health":
                    return self.send_json(200, {"ok": True, "c_engine": BINARY.exists(), "app": "CognifyX"})
                if parsed.path == "/api/score":
                    keys = ["correct", "wrong", "skipped", "seconds", "total"]
                    vals = [int(args[k][0]) for k in keys]
                    return self.send_json(200, run_engine("score", *map(str, vals)))
                if parsed.path == "/api/adapt":
                    level = int(args.get("level", ["2"])[0])
                    correct = int(args.get("correct", ["0"])[0])
                    return self.send_json(200, run_engine("adapt", str(level), str(correct)))
                if parsed.path == "/api/recommend":
                    keys = ["quant", "logic", "verbal", "computer"]
                    vals = [int(args.get(k, ["50"])[0]) for k in keys]
                    return self.send_json(200, run_engine("recommend", *map(str, vals)))
                return self.send_json(404, {"error": "API route not found"})
            except (ValueError, KeyError, IndexError) as exc:
                return self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                return self.send_json(503, {"error": str(exc), "c_engine": False})
        if parsed.path == "/":
            self.path = "/index.html"
        return super().do_GET()


def main():
    engine_ok = compile_engine()
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print("\nCognifyX Advanced is ready.")
    print(f"Dashboard: http://127.0.0.1:{PORT}")
    print(f"C engine: {'enabled' if engine_ok else 'fallback mode'}")
    print("Press Ctrl+C to stop the local server.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping CognifyX...")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
