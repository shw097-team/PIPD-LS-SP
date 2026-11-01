"""Sign an arbitrary bounded payload through the OPEN owner window (broker on loopback).

Protocol measured from owner_window.py:211-263:
  POST /sign  {token, kind, body_json, payload_sha256, effect_class?, enrollments_sha256}
  kind in ALLOWED_KINDS = {merkle_root, row}; the window must be OPEN and within its budget.

The private key never leaves the broker; this client only receives signature_hex. No passphrase is
read, stored or printed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import time
import urllib.request

HOME = pathlib.Path(r"C:\Users\user\.hgk-owner")


def load_window() -> dict:
    return json.loads((HOME / "window.json").read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--body", required=True, help="file whose exact bytes are signed")
    ap.add_argument("--kind", default="row", choices=["row", "merkle_root"])
    ap.add_argument("--effect-class", default=None)
    ap.add_argument("--out", required=True, help="receipt path (json)")
    a = ap.parse_args()

    w = load_window()
    if w.get("state") != "OPEN":
        raise SystemExit(f"REFUSED_WINDOW_NOT_OPEN: state={w.get('state')}")
    token = (HOME / "window.token").read_text(encoding="utf-8").strip()
    body = pathlib.Path(a.body).read_bytes()
    req = {"token": token, "kind": a.kind, "body_json": body.decode("utf-8"),
           "payload_sha256": hashlib.sha256(body).hexdigest(),
           "enrollments_sha256": w.get("enrollments_sha256_at_open")}
    if a.effect_class:
        req["effect_class"] = a.effect_class
    port = w.get("port")
    if not port:
        raise SystemExit("REFUSED_NO_PORT: window.json has no port (broker not serving)")
    data = json.dumps(req, ensure_ascii=False).encode("utf-8")
    r = urllib.request.Request(f"http://127.0.0.1:{port}/sign", data=data,
                               headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            out = json.loads(resp.read().decode("utf-8"))
            code = resp.status
    except urllib.error.HTTPError as e:            # a typed refusal is a result, not a crash
        out = json.loads(e.read().decode("utf-8") or "{}")
        code = e.code
    receipt = {"schema": "OWNER_SIGNING_RECEIPT/1", "window_id": w.get("window_id"),
               "kind": a.kind, "body_path": str(pathlib.Path(a.body).resolve()),
               "payload_sha256": req["payload_sha256"], "http_status": code,
               "signed": bool(out.get("signature_hex")),
               "signature_hex": out.get("signature_hex"),
               "ops_used": out.get("ops_used"), "error": out.get("error"),
               "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    p = pathlib.Path(a.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: receipt[k] for k in ("http_status", "signed", "ops_used", "error", "payload_sha256")},
                     ensure_ascii=False))
    return 0 if receipt["signed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
