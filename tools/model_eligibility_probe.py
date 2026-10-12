#!/usr/bin/env python3
"""Two-turn tool-call eligibility probe for an OpenAI-compatible endpoint.

Why this exists: a governed long run can die on the SECOND provider turn with
``Provider error 400: Upstream request failed: [invalid_request_error] The `reasoning_content` in
the thinking mode must be passed back to the API.`` By then the run has already done work. This
probe establishes the entitlement *before* the long run: turn 1 asks the endpoint for a tool call,
turn 2 continues that same conversation (assistant tool call + tool result), which is exactly where
the adapter defect bites. The result is recorded as a receipt carrying the DECLARED and the OBSERVED
model, so a model substitution is disclosed, never silent.

Exit status:
    0  both turns passed (``eligible`` is true);
    3  a typed refusal -- the probe reached the endpoint but a turn failed. For the known
       ``reasoning_content`` class the typed reason is ``reasoning_content_not_echoed``; other
       failures get a typed ``turnN_...``/``turnN_http_<status>`` reason;
    2  a transport / connection error (nothing was reachable, so no entitlement was established).

The receipt is printed to stdout and, when ``--out`` is given, also written there. Secrets: an
``Authorization`` header is added only when ``OPENAI_API_KEY`` is set in the environment; the value
is never printed, echoed, logged or written into the receipt.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REASONING_CONTENT_CODE = "reasoning_content_not_echoed"
TRANSPORT_CODE = "transport_error"

TOOLS = [{
    "type": "function",
    "function": {
        "name": "probe_echo",
        "description": "Echo text back so the follow-up turn has a tool result to continue from.",
        "parameters": {"type": "object", "properties": {"text": {"type": "string"}},
                       "required": ["text"]},
    },
}]


class TransportError(Exception):
    """The endpoint could not be reached, or the connection failed mid-flight (exit code 2)."""


def _endpoint(base_url: str) -> str:
    """Accept either a base URL (``.../v1``) or a full completions URL."""
    base = base_url.rstrip("/")
    return base if base.endswith("/chat/completions") else base + "/chat/completions"


def _decode(raw: bytes) -> dict:
    if not raw:
        return {}
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return {"raw": raw.decode("utf-8", "replace")}
    return payload if isinstance(payload, dict) else {"raw": raw.decode("utf-8", "replace")}


def _post(url: str, payload: dict, headers: dict, timeout: float) -> tuple[int, dict]:
    """POST JSON and return ``(status, decoded_body)``. Never raises for an HTTP status."""
    request = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, _decode(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, _decode(exc.read())
    except (urllib.error.URLError, OSError) as exc:
        raise TransportError(str(getattr(exc, "reason", exc))) from exc


def _first_message(body: dict) -> dict:
    choices = body.get("choices")
    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
        message = choices[0].get("message")
        if isinstance(message, dict):
            return message
    return {}


def _note_model(receipt: dict, body: dict) -> None:
    """Record the model the endpoint says it served (declared-vs-observed disclosure)."""
    model = body.get("model")
    if isinstance(model, str) and model.strip():
        receipt["observed_model"] = model.strip()


def probe(base_url: str, model: str, *, api_key: str | None = None,
          timeout: float = 10.0) -> tuple[dict, int]:
    """Run the two-turn probe and return ``(receipt, exit_code)`` (see the module docstring)."""
    url = _endpoint(base_url)
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    receipt = {
        "schema": "PIPD-MODEL-ELIGIBILITY-RECEIPT/1",
        "declared_model": model,
        "observed_model": model,
        "turn1": "FAIL",
        "turn2": "FAIL",
        "eligible": False,
        "typed_reason": None,
        "endpoint": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    messages = [{"role": "user",
                 "content": "Call the probe_echo tool with text=ping, then report the result."}]

    try:  # turn 1 -- ask for a tool call
        status, body = _post(url, {"model": model, "messages": messages, "tools": TOOLS,
                                   "tool_choice": "auto"}, headers, timeout)
    except TransportError:
        receipt["typed_reason"] = TRANSPORT_CODE
        return receipt, 2
    _note_model(receipt, body)
    if status != 200:
        receipt["typed_reason"] = f"turn1_http_{status}"
        return receipt, 3
    message = _first_message(body)
    tool_calls = message.get("tool_calls")
    if not tool_calls:
        receipt["typed_reason"] = "turn1_no_tool_call"
        return receipt, 3
    receipt["turn1"] = "PASS"
    messages = messages + [
        {"role": "assistant", "content": message.get("content"), "tool_calls": tool_calls},
        {"role": "tool", "tool_call_id": tool_calls[0].get("id") or "call_probe_1",
         "content": "ping"},
    ]

    try:  # turn 2 -- continue the conversation, which is where the adapter defect bites
        status2, body2 = _post(url, {"model": model, "messages": messages, "tools": TOOLS},
                               headers, timeout)
    except TransportError:
        receipt["typed_reason"] = TRANSPORT_CODE
        return receipt, 2
    _note_model(receipt, body2)
    if status2 != 200:
        blob = json.dumps(body2).lower()
        receipt["typed_reason"] = (REASONING_CONTENT_CODE if "reasoning_content" in blob
                                   else f"turn2_http_{status2}")
        return receipt, 3
    receipt["turn2"] = "PASS"
    receipt["eligible"] = True
    return receipt, 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Two-turn tool-call eligibility probe for an OpenAI-compatible endpoint.")
    ap.add_argument("--base-url", required=True,
                    help="OpenAI-compatible base URL, e.g. http://127.0.0.1:1234/v1")
    ap.add_argument("--model", required=True, help="the DECLARED model to probe")
    ap.add_argument("--out", metavar="PATH", default=None,
                    help="also write the receipt JSON to this path")
    ap.add_argument("--timeout", type=float, default=10.0, help="per-request timeout in seconds")
    args = ap.parse_args(argv)

    # The credential is read from the environment and used only as a header value. It is never
    # printed and never placed in the receipt.
    api_key = os.environ.get("OPENAI_API_KEY") or None
    receipt, code = probe(args.base_url, args.model, api_key=api_key, timeout=args.timeout)
    text = json.dumps(receipt, ensure_ascii=False, indent=1)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8", newline="")
    print(text)
    print(f"declared={receipt['declared_model']} observed={receipt['observed_model']} "
          f"turn1={receipt['turn1']} turn2={receipt['turn2']} eligible={receipt['eligible']} "
          f"typed_reason={receipt['typed_reason']}", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
