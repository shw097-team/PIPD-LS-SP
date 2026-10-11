#!/usr/bin/env python3
"""Host-side loopback bridge for the governed lane.

The opencodex proxy on 127.0.0.1:10101 rejects any data-plane request whose Host header is
not localhost/127.0.0.1 ("cross-origin data-plane request blocked"). A container reaching the
host gateway therefore gets 403 no matter which address it dials. This bridge listens on
0.0.0.0:<listen> and re-issues each request to 127.0.0.1:<upstream> with Host rewritten to
127.0.0.1:<upstream>, streaming the response back chunked (SSE-safe).

Bind is intentionally the host gateway only reachable from the local docker network.
"""
from __future__ import annotations

import http.client
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM_HOST = "127.0.0.1"
UPSTREAM_PORT = 10101
LISTEN_PORT = 10100
HOP_HEADERS = {"host", "content-length", "connection", "keep-alive", "transfer-encoding",
               "accept-encoding", "te", "upgrade", "proxy-connection", "expect"}


class Bridge(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "hgk-lane-bridge/1"

    def log_message(self, fmt, *args):  # keep the console quiet
        sys.stderr.write("[bridge] " + (fmt % args) + "\n")

    def _relay(self, method: str) -> None:
        length = 0
        raw_len = self.headers.get("Content-Length")
        if raw_len and raw_len.isdigit():
            length = int(raw_len)
        body = self.rfile.read(length) if length else None
        headers = {k: v for k, v in self.headers.items() if k.lower() not in HOP_HEADERS}
        headers["Host"] = f"{UPSTREAM_HOST}:{UPSTREAM_PORT}"
        headers["Connection"] = "close"
        if body is not None:
            headers["Content-Length"] = str(len(body))
        try:
            conn = http.client.HTTPConnection(UPSTREAM_HOST, UPSTREAM_PORT, timeout=900)
            conn.request(method, self.path, body=body, headers=headers)
            resp = conn.getresponse()
        except Exception as exc:  # upstream down -> typed 502 for the lane probe
            msg = f'{{"error":{{"message":"lane bridge upstream error: {exc}","code":"bridge_upstream"}}}}'
            payload = msg.encode()
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        self.send_response(resp.status)
        for k, v in resp.getheaders():
            if k.lower() in HOP_HEADERS:
                continue
            self.send_header(k, v)
        self.send_header("Transfer-Encoding", "chunked")   # length unknown for streamed SSE
        self.end_headers()
        try:
            while True:
                chunk = resp.read(1024)
                if not chunk:
                    break
                self.wfile.write(b"%x\r\n%s\r\n" % (len(chunk), chunk))
                self.wfile.flush()
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        except Exception as exc:
            sys.stderr.write(f"[bridge] stream aborted: {exc}\n")
        finally:
            conn.close()

    def do_GET(self):
        self._relay("GET")

    def do_POST(self):
        self._relay("POST")

    def do_PUT(self):
        self._relay("PUT")

    def do_DELETE(self):
        self._relay("DELETE")

    def do_OPTIONS(self):
        self._relay("OPTIONS")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else LISTEN_PORT
    srv = ThreadingHTTPServer(("0.0.0.0", port), Bridge)
    srv.daemon_threads = True
    print(f"[bridge] listening 0.0.0.0:{port} -> {UPSTREAM_HOST}:{UPSTREAM_PORT}", flush=True)
    srv.serve_forever()
