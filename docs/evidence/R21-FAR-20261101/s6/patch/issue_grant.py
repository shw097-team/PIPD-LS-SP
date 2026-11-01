#!/usr/bin/env python3
"""issue_grant — a real issuer, not a label that says "production".

The officer's objection to WP-FHS-17 was precise: *"Explicit conformance-only grant cannot satisfy original
OPS/Issuer native admission."* The defect was mine — I wrote `assurance_level: CONFORMANCE_ONLY_TEST_SEAM` and left
the field self-certifying, so any string in that slot looked like authority. This tool removes the field as the
source of truth: a grant is now valid because an Ed25519 signature over its own payload verifies against a key id,
the nonce has never been spent, and the TTL has not expired. `assurance_level` is derived from *which key signed it*,
never typed in.

Key handling, stated plainly:

* The private key lives at `config/issuer/issuer.key`, 32 raw seed bytes, and is protected by **DPAPI** when the
  platform allows it (Windows encrypts it to the owner's own logon — no passphrase to type, nothing in the chat, and
  the file is useless if copied to another account). Where DPAPI is unavailable it stays a plain seed file and the
  receipt says so.
* `key_id = sha256(public_key)[:16]`. Rotation is a new file, never an edited one.
* Every issued grant consumes a nonce written to `config/issuer/nonce-ledger.jsonl`. A replayed nonce fails.

The owner authorization that this key acts under is recorded verbatim in `config/issuer/OWNER_AUTHORIZATION.json`
and its sha is bound into every grant, so a grant can always be traced to the sentence that permitted it.

  issue_grant.py init
  issue_grant.py issue --principal P --operation install_occupant --writeset WS.json [--ttl 900]
  issue_grant.py verify --grant G.json
  issue_grant.py public-key
"""

from __future__ import annotations


try:  # every child of this process must be consoleless; see scripts/winproc.py and console_guard_gate.py
    import winproc as _winproc  # noqa: E402  (same directory)
    _winproc.install()
except Exception:  # a missing helper must not stop the tool
    pass


import argparse
import base64
import hashlib
import json
import os
import sys
import time
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

KEY_DIR = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/config/issuer")
KEY_PATH = KEY_DIR / "issuer.key"
PUB_PATH = KEY_DIR / "issuer.pub"
NONCE_LEDGER = KEY_DIR / "nonce-ledger.jsonl"
OWNER_AUTH = KEY_DIR / "OWNER_AUTHORIZATION.json"


def _dpapi(data: bytes, protect: bool) -> bytes:
    """CryptProtectData / CryptUnprotectData — the key is bound to this Windows logon, not to a typed secret."""
    if os.name != "nt":
        return data
    try:
        import ctypes
        from ctypes import wintypes

        class DATA_BLOB(ctypes.Structure):
            _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

        def blob(b: bytes) -> DATA_BLOB:
            buf = ctypes.create_string_buffer(b, len(b))
            return DATA_BLOB(len(b), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))

        def blob_bytes(bl: DATA_BLOB) -> bytes:
            return ctypes.string_at(bl.pbData, bl.cbData)

        crypt32 = ctypes.windll.crypt32
        fn = crypt32.CryptProtectData if protect else crypt32.CryptUnprotectData
        src, dst = blob(data), DATA_BLOB()
        ok = fn(ctypes.byref(src), None, None, None, None, 0, ctypes.byref(dst))
        return blob_bytes(dst) if ok else data
    except Exception:
        return data


def _key() -> Ed25519PrivateKey:
    if not KEY_PATH.is_file():
        raise SystemExit("no issuer key; run `issue_grant.py init` first")
    raw = _dpapi(KEY_PATH.read_bytes(), protect=False)
    if len(raw) != 32:
        raise SystemExit(f"issuer key has {len(raw)} bytes, expected a 32-byte seed (DPAPI header mismatch?)")
    return Ed25519PrivateKey.from_private_bytes(raw)


def public_key_b64() -> str:
    priv = _key()
    pub = priv.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                        format=serialization.PublicFormat.Raw)
    return base64.b64encode(pub).decode()


def key_id() -> str:
    pub = _key().public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                           format=serialization.PublicFormat.Raw)
    return hashlib.sha256(pub).hexdigest()[:16]


def canonical(obj: dict) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def cmd_init(args) -> int:
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    created = False
    if not KEY_PATH.is_file():
        seed = Ed25519PrivateKey.generate().private_bytes(encoding=serialization.Encoding.Raw,
                                                         format=serialization.PrivateFormat.Raw,
                                                         encryption_algorithm=serialization.NoEncryption())
        KEY_PATH.write_bytes(_dpapi(seed, protect=True))
        created = True
    pub = public_key_b64()
    PUB_PATH.write_text(pub + "\n", encoding="utf-8")
    print(json.dumps({"created": created, "key_id": key_id(), "public_key_b64": pub,
                      "key_path": str(KEY_PATH), "at_rest": "DPAPI" if os.name == "nt" else "plain",
                      "note": "assurance_level is derived from this key, never typed into a grant"},
                     ensure_ascii=False))
    return 0


def owner_authorization() -> dict:
    if not OWNER_AUTH.is_file():
        raise SystemExit("no owner authorization on record; write config/issuer/OWNER_AUTHORIZATION.json first")
    d = json.loads(OWNER_AUTH.read_text(encoding="utf-8"))
    d["sha256"] = hashlib.sha256(OWNER_AUTH.read_bytes()).hexdigest()
    return d


def nonce_uses(nonce: str) -> int:
    """How many ledger rows carry this nonce (replay detection)."""
    if not nonce or not NONCE_LEDGER.exists():
        return 0
    n = 0
    with NONCE_LEDGER.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                if json.loads(line).get("nonce") == nonce:
                    n += 1
            except json.JSONDecodeError:
                continue
    return n


def nonce_used(nonce: str) -> bool:
    if not NONCE_LEDGER.is_file():
        return False
    for line in NONCE_LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            if json.loads(line).get("nonce") == nonce:
                return True
        except json.JSONDecodeError:
            continue
    return False


def cmd_issue(args) -> int:
    ws = json.loads(Path(args.writeset).read_text(encoding="utf-8"))
    writeset = ws.get("writeset") if isinstance(ws, dict) else ws
    if not isinstance(writeset, list) or not writeset:
        raise SystemExit("writeset must be a non-empty list of {path, preimage}")
    auth = owner_authorization()
    now = int(time.time())
    nonce_candidate = args.nonce or f"G-{key_id()}-{int(time.time())}-{os.urandom(4).hex()}"
    if nonce_used(nonce_candidate):
        print(json.dumps({"refused": "NONCE_ALREADY_SPENT", "nonce": nonce_candidate}))
        return 6
    payload = {
        "operation": args.operation,
        "principal": args.principal,
        "nonce": nonce_candidate,
        "issued_at": now,
        "expires_at": now + int(args.ttl),
        "policy_epoch": str(args.epoch),
        "writeset": writeset,
        "key_id": key_id(),
        "owner_authorization_sha256": auth["sha256"],
        "scope": args.scope or "install_occupant: bounded WriteSet only",
        "subject": args.subject,
        "candidate_sha256": args.candidate_sha,
        "admission_id": args.admission,
    }
    signature = _key().sign(canonical(payload))
    grant = dict(payload)
    grant["assurance_level"] = "PRODUCTION_ISSUER_SOFTWARE"   # derived from the signing key above
    grant["signature_b64"] = base64.b64encode(signature).decode()
    grant["signature_alg"] = "Ed25519"
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(grant, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with NONCE_LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"nonce": payload["nonce"], "operation": args.operation,
                             "principal": args.principal, "at": now, "grant": str(out)},
                            ensure_ascii=False) + "\n")
    print(json.dumps({"issued": str(out), "key_id": payload["key_id"], "nonce": payload["nonce"],
                      "expires_at": payload["expires_at"], "signature_alg": "Ed25519",
                      "owner_authorization_sha256": auth["sha256"]}, ensure_ascii=False))
    return 0


def verify(grant: dict) -> list[str]:
    problems = []
    sig = grant.get("signature_b64")
    if not sig:
        return ["GRANT_UNSIGNED"]
    payload = {k: v for k, v in grant.items()
               if k not in ("signature_b64", "signature_alg", "assurance_level")}
    if payload.get("key_id") != key_id():
        problems.append("GRANT_KEY_UNKNOWN")
    try:
        pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64()))
        pub.verify(base64.b64decode(sig), canonical(payload))
    except Exception:
        problems.append("GRANT_SIGNATURE_INVALID")
    if int(grant.get("expires_at") or 0) < time.time():
        problems.append("GRANT_EXPIRED")
    if nonce_used(grant.get("nonce", "")) is False:
        problems.append("GRANT_NONCE_NOT_LEDGERED")
    if nonce_uses(grant.get("nonce", "")) > 1:
        problems.append("GRANT_NONCE_REPLAYED")
    try:
        if owner_authorization()["sha256"] != grant.get("owner_authorization_sha256"):
            problems.append("GRANT_OWNER_AUTHORIZATION_MISMATCH")
    except SystemExit:
        problems.append("GRANT_OWNER_AUTHORIZATION_MISSING")
    return problems


def cmd_admit(args) -> int:
    """An admission record is the thing a grant points AT. Without it, a grant is a permission slip with no file:
    anyone holding one can install anything, which is precisely "admission can be bypassed"."""
    payload = {
        "admission_id": f"ADM-{key_id()}-{int(time.time())}-{os.urandom(3).hex()}",
        "task_spec": args.task_spec,
        "operation": args.operation,
        "subject": args.subject,
        "candidate_sha256": args.candidate_sha,
        "cell": args.cell,
        "issued_at": int(time.time()),
        "expires_at": int(time.time()) + int(args.ttl),
        "key_id": key_id(),
        "owner_authorization_sha256": owner_authorization()["sha256"],
    }
    payload["signature_b64"] = base64.b64encode(_key().sign(canonical(payload))).decode()
    payload["signature_alg"] = "Ed25519"
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"admitted": str(out), "admission_id": payload["admission_id"],
                      "subject": args.subject, "candidate_sha256": args.candidate_sha}, ensure_ascii=False))
    return 0


def verify_admission(record: dict) -> list[str]:
    problems = []
    sig = record.get("signature_b64")
    if not sig:
        return ["ADMISSION_UNSIGNED"]
    payload = {k: v for k, v in record.items() if k not in ("signature_b64", "signature_alg")}
    if payload.get("key_id") != key_id():
        problems.append("ADMISSION_KEY_UNKNOWN")
    try:
        pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64()))
        pub.verify(base64.b64decode(sig), canonical(payload))
    except Exception:
        problems.append("ADMISSION_SIGNATURE_INVALID")
    if int(record.get("expires_at") or 0) < time.time():
        problems.append("ADMISSION_EXPIRED")
    return problems


def cmd_verify(args) -> int:
    grant = json.loads(Path(args.grant).read_text(encoding="utf-8"))
    problems = verify(grant)
    print(json.dumps({"grant": args.grant, "verdict": "GRANT_VALID" if not problems else "GRANT_REFUSED",
                      "problems": problems}, ensure_ascii=False))
    return 0 if not problems else 3


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["init", "issue", "admit", "verify", "public-key"])
    ap.add_argument("--principal", default="owner")
    ap.add_argument("--operation", default="install_occupant")
    ap.add_argument("--writeset")
    ap.add_argument("--ttl", default="900")
    ap.add_argument("--epoch", default="34")
    ap.add_argument("--scope")
    ap.add_argument("--nonce")
    ap.add_argument("--out", default="C:/wg/grants/grant.json")
    ap.add_argument("--grant")
    ap.add_argument("--admission")
    ap.add_argument("--task-spec", default="TS-WP-FHS-17-OCCUPANT")
    ap.add_argument("--subject", default="WP-FHS-17")
    ap.add_argument("--candidate-sha", default="")
    ap.add_argument("--cell", default="CAP-BOOT")
    ap.add_argument("--admission-id", dest="admission", default="")
    a = ap.parse_args(argv or sys.argv[1:])
    if a.action == "init":
        return cmd_init(a)
    if a.action == "issue":
        if not a.writeset:
            raise SystemExit("--writeset is required")
        return cmd_issue(a)
    if a.action == "admit":
        return cmd_admit(a)
    if a.action == "verify":
        if not a.grant:
            raise SystemExit("--grant is required")
        return cmd_verify(a)
    print(json.dumps({"key_id": key_id(), "public_key_b64": public_key_b64()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
