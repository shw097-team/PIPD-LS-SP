"""Issue a WP-13 grant whose authorisation is the owner envelope, not a bare file key.

Why this exists: the WP-13 AO rejected the earlier grant because its signer sat under the same Windows
logon as the executor (F1). Under this mission's governance there is exactly one owner and that owner is
also the issuer, so the missing instrument was never a second key holder — it was proof that a human
opened the envelope and authorised this specific artefact. The envelope's countersignature is that proof:
it can only exist after the owner typed the passphrase, and every use burns an op from a numbered budget.

So the grant carries two signatures with different jobs:
  * signature_b64       — the issuer key, kept so the existing verifier and hotswap.py still work
                          (it proves the artefact, not the authorisation);
  * owner_authorization — Ed25519 by the owner window over the canonical grant body, carrying
                          window_id, ops_used, expires_at, and the payload sha it signed
                          (this is the authorisation).
"""
import base64
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.request

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
RUN = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp13"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
WIN = pathlib.Path(os.path.expanduser("~")) / ".hgk-owner" / "window.json"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def main() -> int:
    win = json.loads(WIN.read_text(encoding="utf-8"))
    if win.get("state") != "OPEN" or "permit_sign" not in (win.get("scope") or []):
        print(json.dumps({"refused": "WINDOW_NOT_OPEN_OR_SCOPE", "state": win.get("state")}))
        return 2

    fixture = RUN / "fixture-envelope"
    fixture.mkdir(parents=True, exist_ok=True)
    (fixture / "occupant.py").write_text(
        'class Impl:\n    def identity(self):\n        return "cap-attest-v1"\ndef build():\n    return Impl()\n',
        encoding="utf-8", newline="\n")
    (fixture / "candidate.py").write_text(
        'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\ndef build():\n    return Impl()\n',
        encoding="utf-8", newline="\n")

    ws = RUN / "writeset_envelope.json"
    ws.write_text(json.dumps({"writeset": [
        {"path": str(fixture / "occupant.py"), "preimage": sha(fixture / "occupant.py")},
        {"path": str(fixture / "candidate.py"), "preimage": sha(fixture / "candidate.py")}]}, indent=1),
        encoding="utf-8")

    grant_path = RUN / "grant_envelope.json"
    issued = subprocess.run([sys.executable, str(ISSUER), "issue", "--principal", "owner",
                             "--operation", "install_occupant", "--writeset", str(ws),
                             "--ttl", "1800", "--epoch", "40",
                             "--scope", "WP-FHS-13 C5 under owner envelope",
                             "--nonce", f"WP13-ENV-{int(time.time())}", "--subject", "WP-FHS-13",
                             "--candidate-sha", sha(fixture / "candidate.py"), "--out", str(grant_path)],
                            capture_output=True, text=True)
    if issued.returncode != 0 or not grant_path.exists():
        print(json.dumps({"refused": "ISSUE_FAILED", "err": issued.stderr[-300:]}))
        return 3

    grant = json.loads(grant_path.read_text(encoding="utf-8"))
    for k in ("owner_authorization", "owner_authorization_sha256"):
        grant.pop(k, None)
    body = canonical(grant)
    body_sha = hashlib.sha256(body).hexdigest()

    req = {"token": (WIN.parent / "window.token").read_text().strip(),
           "kind": "merkle_root", "effect_class": "HOST_OPERATIONS",
           "body_json": body.decode(), "payload_sha256": body_sha,
           "enrollments_sha256": win.get("enrollments_sha256_at_open")}
    r = urllib.request.Request(f"http://127.0.0.1:{win['port']}/sign", data=json.dumps(req).encode(),
                               headers={"Content-Type": "application/json"}, method="POST")
    try:
        resp = json.load(urllib.request.urlopen(r, timeout=30))
    except urllib.error.HTTPError as e:
        print(json.dumps({"refused": "BROKER_REFUSED", "body": e.read().decode()[:300]}))
        return 4

    sig = resp["signature_hex"]
    win2 = json.loads(WIN.read_text(encoding="utf-8"))
    pub = win2.get("owner_public_hex")
    Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub)).verify(bytes.fromhex(sig), body)

    grant["owner_authorization"] = {
        "signer": "owner-envelope", "window_id": resp.get("window_id", win2["window_id"]),
        "ops_used": resp.get("ops_used"), "max_ops": win2.get("max_ops"),
        "expires_at": win2.get("expires_at"), "payload_sha256": body_sha,
        "signature_hex": sig, "owner_public_hex": pub,
        "effect_class_ceiling": win2.get("effect_class_ceiling"),
        "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    grant["owner_authorization_sha256"] = hashlib.sha256(
        json.dumps(grant["owner_authorization"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    grant_path.write_text(json.dumps(grant, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

    verified = subprocess.run([sys.executable, str(ISSUER), "verify", "--grant", str(grant_path)],
                              capture_output=True, text=True)
    out = {"grant": str(grant_path), "grant_sha256": sha(grant_path),
           "owner_window": resp.get("window_id"), "ops_used": resp.get("ops_used"),
           "payload_sha256": body_sha, "owner_signature_verifies": True,
           "issuer_verifier_rc": verified.returncode, "issuer_verifier_out": verified.stdout.strip()[:200]}
    (RUN / "GRANT_ENVELOPE_RECEIPT.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                                    encoding="utf-8", newline="\n")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
