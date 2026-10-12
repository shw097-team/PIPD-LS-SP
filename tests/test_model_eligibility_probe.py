"""Drive ``tools/model_eligibility_probe.py`` against an in-process ``http.server`` stub.

No real host is contacted: the stub binds ``127.0.0.1:0`` (an ephemeral port) and the only network
failure exercised is a refused connection to a local port that is known to be closed. There are no
sleeps, and the whole module is expected to finish in a couple of seconds.

Cases: (a) both turns healthy -> exit 0, ``eligible: true``; (b) the second turn returns HTTP 400
with a ``reasoning_content`` error body -> exit 3 and the typed reason recorded; (c) connection
refused -> exit 2. It also checks that a credential in the environment is never echoed.
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

PROBE = ROOT / "tools" / "model_eligibility_probe.py"
DECLARED = "declared-model-under-test"
OBSERVED = "stub-observed-model"
SECRET = "sk-sentinel-must-never-appear"


class _StubEndpoint:
    """A minimal OpenAI-compatible stub; ``mode`` selects the second-turn behaviour."""

    def __init__(self, mode: str) -> None:
        self.mode = mode
        self.requests: list[dict] = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args) -> None:  # keep the test output clean
                pass

            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(length) or b"{}")
                outer.requests.append({"path": self.path, "body": body})
                status, payload = outer._respond(len(outer.requests))
                raw = json.dumps(payload).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base_url = f"http://127.0.0.1:{self._server.server_address[1]}/v1"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def _respond(self, turn: int) -> tuple[int, dict]:
        if self.mode == "reasoning_content" and turn >= 2:
            return 400, {"error": {
                "message": "Provider error 400: Upstream request failed: [invalid_request_error] "
                           "The `reasoning_content` in the thinking mode must be passed back to "
                           "the API.",
                "type": "invalid_request_error"}}
        if turn == 1:
            return 200, {"model": OBSERVED, "choices": [{
                "index": 0, "finish_reason": "tool_calls", "message": {
                    "role": "assistant", "content": None,
                    "tool_calls": [{"id": "call_stub_1", "type": "function", "function": {
                        "name": "probe_echo", "arguments": "{\"text\": \"ping\"}"}}]}}]}
        return 200, {"model": OBSERVED, "choices": [{
            "index": 0, "finish_reason": "stop",
            "message": {"role": "assistant", "content": "pong"}}]}

    def close(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)


def _free_port() -> int:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


class ModelEligibilityProbe(unittest.TestCase):
    def _run(self, base_url: str, out: Path, *, api_key: str | None = None) -> subprocess.CompletedProcess:
        env = dict(os.environ)
        if api_key is None:
            env.pop("OPENAI_API_KEY", None)
        else:
            env["OPENAI_API_KEY"] = api_key
        return subprocess.run(
            [sys.executable, str(PROBE), "--base-url", base_url, "--model", DECLARED,
             "--out", str(out), "--timeout", "3"],
            capture_output=True, text=True, env=env)

    def test_healthy_two_turns_is_eligible(self) -> None:
        stub = _StubEndpoint("healthy")
        self.addCleanup(stub.close)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "receipt.json"
            proc = self._run(stub.base_url, out, api_key=SECRET)
            self.assertEqual(proc.returncode, 0, proc.stderr[-600:])
            receipt = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(receipt["declared_model"], DECLARED)
        self.assertEqual(receipt["observed_model"], OBSERVED)
        self.assertEqual((receipt["turn1"], receipt["turn2"]), ("PASS", "PASS"))
        self.assertIs(receipt["eligible"], True)
        self.assertIsNone(receipt["typed_reason"])
        # The second turn must CONTINUE the conversation: the tool call is echoed back with a result.
        self.assertGreaterEqual(len(stub.requests), 2)
        roles = [m.get("role") for m in stub.requests[1]["body"]["messages"]]
        self.assertIn("assistant", roles)
        self.assertIn("tool", roles)
        # A credential in the environment must never be printed or stored.
        self.assertNotIn(SECRET, proc.stdout + proc.stderr)
        self.assertNotIn(SECRET, json.dumps(receipt))

    def test_second_turn_reasoning_content_is_typed_refusal(self) -> None:
        stub = _StubEndpoint("reasoning_content")
        self.addCleanup(stub.close)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "receipt.json"
            proc = self._run(stub.base_url, out)
            self.assertEqual(proc.returncode, 3, proc.stderr[-600:])
            receipt = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(receipt["turn1"], "PASS")
        self.assertEqual(receipt["turn2"], "FAIL")
        self.assertIs(receipt["eligible"], False)
        self.assertEqual(receipt["typed_reason"], "reasoning_content_not_echoed")

    def test_connection_refused_is_a_transport_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "receipt.json"
            proc = self._run(f"http://127.0.0.1:{_free_port()}/v1", out)
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            receipt = json.loads(out.read_text(encoding="utf-8"))
        self.assertIs(receipt["eligible"], False)
        self.assertEqual(receipt["typed_reason"], "transport_error")
        self.assertEqual(receipt["turn1"], "FAIL")


if __name__ == "__main__":
    unittest.main(verbosity=2)
