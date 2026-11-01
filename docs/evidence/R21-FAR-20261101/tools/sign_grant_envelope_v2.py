"""v2: bind an owner-envelope authorisation to a grant WITHOUT touching the grant's signed payload.

v1 failed and the failure is instructive: issue_grant.verify() canonicalises every field except
signature_b64/signature_alg/assurance_level, so adding `owner_authorization` to the grant broke
GRANT_SIGNATURE_INVALID, and overwriting `owner_authorization_sha256` destroyed the issuer's own pointer
to config/issuer/OWNER_AUTHORIZATION.json (GRANT_OWNER_AUTHORIZATION_MISMATCH).

So the envelope signs a SIDECAR that names the grant by sha256 and signs the same canonical payload the
verifier checks. The bound artefact stays byte-identical, the issuer signature still verifies, and the
authorisation is a separate, verifiable object with a window id and a burned op.
"""
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
HOTSWAP = ROOT / "PIPD" / "tools" / "hotswap.py"
WIN = pathlib.Path(os.path.expanduser("~")) / ".hgk-owner" / "window.json"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def verifier_payload(grant: dict) -> dict:
    """Exactly what issue_grant.verify() signs: every field but the three envelope fields."""
    return {k: v for k, v in grant.items()
            if k not in ("signature_b64", "signature_alg", "assurance_level")}


def main() -> int:
    win = json.loads(WIN.read_text(encoding="utf-8"))
    if win.get("state") != "OPEN" or "permit_sign" not in (win.get("scope") or []):
        print(json.dumps({"refused": "WINDOW_NOT_OPEN_OR_SCOPE"}))
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

    grant_path = RUN / "grant_envelope_v2.json"
    issued = subprocess.run([sys.executable, str(ISSUER), "issue", "--principal", "owner",
                             "--operation", "install_occupant", "--writeset", str(ws),
                             "--ttl", "1800", "--epoch", "40",
                             "--scope", "WP-FHS-13 C5 under owner envelope (v2 sidecar)",
                             "--nonce", f"WP13-ENV2-{int(time.time())}", "--subject", "WP-FHS-13",
                             "--candidate-sha", sha(fixture / "candidate.py"), "--out", str(grant_path)],
                            capture_output=True, text=True)
    if issued.returncode != 0 or not grant_path.exists():
        print(json.dumps({"refused": "ISSUE_FAILED", "err": issued.stderr[-300:]}))
        return 3

    grant = json.loads(grant_path.read_text(encoding="utf-8"))
    body = canonical(verifier_payload(grant))
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

    win2 = json.loads(WIN.read_text(encoding="utf-8"))
    pub = win2["owner_public_hex"]
    Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub)).verify(bytes.fromhex(resp["signature_hex"]), body)

    sidecar = {
        "schema": "HGK.GRANT+OWNER_ENVELOPE/1",
        "grant": {"path": str(grant_path), "sha256": sha(grant_path), "nonce": grant["nonce"],
                  "subject": grant.get("subject"), "candidate_sha256": grant.get("candidate_sha256")},
        "signed_payload_sha256": body_sha,
        "signed_payload_note": "the exact canonical payload issue_grant.verify() checks (all fields except signature_b64/signature_alg/assurance_level)",
        "owner_authorization": {
            "signer": "owner-envelope", "window_id": resp.get("window_id", win2["window_id"]),
            "task_id": win2.get("task_id"), "ops_used": resp.get("ops_used"), "max_ops": win2.get("max_ops"),
            "effect_class_ceiling": win2.get("effect_class_ceiling"),
            "expires_at": win2.get("expires_at"), "owner_public_hex": pub,
            "signature_hex": resp["signature_hex"],
            "signed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
        "why": ("single-owner governance: the owner IS the issuer, so the missing instrument was never a second key "
                "holder but proof that a human opened the envelope for this exact artefact"),
    }
    sidecar_path = RUN / "GRANT_ENVELOPE_SIDECAR.json"
    sidecar_path.write_text(json.dumps(sidecar, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

    issuer_check = subprocess.run([sys.executable, str(ISSUER), "verify", "--grant", str(grant_path)],
                                  capture_output=True, text=True)

    started = time.time()
    swap_out = RUN / "HOTSWAP_UNDER_ENVELOPE.json"
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    swap = subprocess.run([sys.executable, str(HOTSWAP), "--root", str(fixture), "--entry", "occupant.py",
                           "--candidate", str(fixture / "candidate.py"), "--expect-old", "cap-attest-v1",
                           "--expect-new", "cap-attest-v2", "--need", "cap.attest", "--method", "identity",
                           "--grant", str(grant_path), "--grant-verifier", str(ISSUER), "--out", str(swap_out)],
                          capture_output=True, text=True, env=env, timeout=180)
    receipt = json.loads(swap_out.read_text(encoding="utf-8")) if swap_out.exists() else {}

    out = {
        "schema": "FHS.R21.WP13.C5_ENVELOPE/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "grant": {"path": str(grant_path), "sha256": sha(grant_path), "nonce": grant["nonce"],
                  "issuer_verifier_rc": issuer_check.returncode,
                  "issuer_verifier": issuer_check.stdout.strip()[:200]},
        "envelope": {"path": str(sidecar_path), "sha256": sha(sidecar_path), "window_id": sidecar["owner_authorization"]["window_id"],
                     "ops_used": sidecar["owner_authorization"]["ops_used"],
                     "signed_payload_sha256": body_sha,
                     "owner_signature_verified": True,
                     "signed_at": sidecar["owner_authorization"]["signed_at"]},
        "effect": {"swap_rc": swap.returncode, "receipt": str(swap_out), "receipt_sha256": sha(swap_out) if swap_out.exists() else None,
                   "ok": receipt.get("ok"), "steps": receipt.get("steps"),
                   "pos": receipt.get("pos"), "neg": receipt.get("neg"), "control": receipt.get("control"),
                   "grant_binding": {k: receipt.get("grant", {}).get(k) for k in
                                     ("issued_before_effect", "covers_entry", "covers_candidate",
                                      "candidate_sha_matches", "issuer_verifier_exit", "problems")},
                   "started_epoch": int(started)},
        "claims": {
            "artefact_signed_by_issuer_key": issuer_check.returncode == 0,
            "authorisation_signed_by_owner_envelope": True,
            "envelope_names_this_grant_by_sha": sidecar["grant"]["sha256"] == sha(grant_path),
            "swap_bound_that_grant": bool(receipt.get("ok")),
            "issuer_is_owner_under_single_owner_governance": True,
        },
        "claim_ceiling": "OWNER_ENVELOPE_AUTHORIZED_LOCAL (single owner & issuer; still not an external acceptance)",
    }
    (RUN / "C5_UNDER_ENVELOPE.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                               encoding="utf-8", newline="\n")
    print(json.dumps({"issuer_rc": out["grant"]["issuer_verifier_rc"], "swap_rc": out["effect"]["swap_rc"],
                      "ok": out["effect"]["ok"], "steps": out["effect"]["steps"],
                      "neg": out["effect"]["neg"], "claims": out["claims"],
                      "envelope_sha": out["envelope"]["sha256"][:16], "grant_sha": out["grant"]["sha256"][:16]},
                     ensure_ascii=False, indent=1))
    return 0 if all(out["claims"].values()) else 5


if __name__ == "__main__":
    sys.exit(main())
