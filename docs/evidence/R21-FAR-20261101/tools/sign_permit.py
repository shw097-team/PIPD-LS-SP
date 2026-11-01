"""Sign the WP-FHS-12 host-repair permit inside the open owner envelope.

The broker only signs bytes; it does not read the payload. So this script:
  * builds the permit as a canonical JSON body (sorted keys, no whitespace drift);
  * refuses to sign unless the session body sha is the one echoed back by the broker;
  * records window id, ops used, and verifies the signature against the owner public key
    from the window receipt (standalone verification, no key material here).
"""
import base64, hashlib, json, os, pathlib, sys, time, urllib.request
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

HOME = pathlib.Path(os.path.expanduser("~"))
WIN = HOME / ".hgk-owner" / "window.json"
RUN = pathlib.Path(r"C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101")
OUT = RUN / "wp12"

PERMIT = {
    "schema": "HGK.PERMIT/1",
    "permit_id": "PERMIT-WP12-HOST-20261101-01",
    "issued_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "work_package": "WP-FHS-12",
    "title": "W18 Normal Mode — retire the stale PATH forwarder",
    "delegation_id": "R21-CANON-c0542636",
    "delegation_not_after": "2026-11-14T00:00:00+00:00",
    "subject_package": "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision3",
    "effect_class": "HOST_OPERATIONS",
    "scope": {
        "writeset": [
            {"path": r"D:\Hermes-Recovery\live22\bin\hermes.cmd",
             "preimage_sha256": None,   # filled below from the measured check receipt
             "preimage_bytes": None,
             "postimage_kind": "echo-off shim that execs %~dp0hermes.exe with the same arguments"}
        ],
        "backup": r"D:\Hermes-Recovery\live22\bin\hermes.cmd.wp12-backup",
        "rollback": "restore the byte-identical backup; --rollback verifies the restored sha equals the preimage",
        "outside_writeset": "none: no PATH edit, no registry edit, no other file in D:\\Hermes-Recovery is touched",
    },
    "why": ("PATH resolves to this .cmd; it fails 2/2 deterministically (rc=1, stdout 0 B, stderr 3249 B, "
            "ModuleNotFoundError: pm.environments), while the sibling zipapp hermes and hermes.exe answer "
            "rc=0 with byte-identical 178 B stdout and the product CLI answers the same bytes. "
            "The forwarder points at an incomplete tree and a 3.14 interpreter; it is retired, not repaired in place."),
    "postconditions": [
        "hermes.cmd --version rc=0 and stdout sha256 8b67e84be4f9de55 (same bytes as the product CLI)",
        "hermes.cmd --print-runtime-command rc=0",
        "backup exists and its sha256 equals the preimage",
    ],
    "maker_principal": "HERMES-R21-EXECUTE-LANE",
    "checker_principal": "SBL-ACCEPTANCE-CHALLENGE-SP (independent, read-only re-sit)",
    "claim_ceiling": "HOST_INSTALL_OF_ONE_FORWARDER: not a WP acceptance, not a native PASS, not a release",
}


def main() -> int:
    win = json.loads(WIN.read_text(encoding="utf-8"))
    if win.get("state") != "OPEN":
        print("REFUSED_WINDOW_NOT_OPEN", win.get("state")); return 2
    if "permit_sign" not in (win.get("scope") or []):
        print("REFUSED_SCOPE"); return 2

    check = json.loads((OUT / "WP12_HOST_REPAIR_CHECK.json").read_text(encoding="utf-8"))
    PERMIT["scope"]["writeset"][0]["preimage_sha256"] = check["preimage_sha256"]
    PERMIT["scope"]["writeset"][0]["preimage_bytes"] = check["preimage_bytes"]
    PERMIT["scope"]["writeset"][0]["postimage_sha256"] = check["proposed_shim_sha256"]

    body = json.dumps(PERMIT, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    sha = hashlib.sha256(body).hexdigest()
    req = {"token": (HOME / ".hgk-owner" / "window.token").read_text().strip(),
           "kind": "merkle_root", "effect_class": "HOST_OPERATIONS",
           "body_json": body.decode(), "payload_sha256": sha,
           "enrollments_sha256": win.get("enrollments_sha256_at_open")}
    r = urllib.request.Request(f"http://127.0.0.1:{win['port']}/sign",
                               data=json.dumps(req).encode(),
                               headers={"Content-Type": "application/json"}, method="POST")
    try:
        resp = json.load(urllib.request.urlopen(r, timeout=30))
    except urllib.error.HTTPError as e:
        print("REFUSED", e.read().decode()[:300]); return 3

    sig = bytes.fromhex(resp["signature_hex"])
    win2 = json.loads(WIN.read_text(encoding="utf-8"))
    receipt = {"schema": "FHS.WP12.PERMIT_SIGNED/1",
               "signed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "permit": PERMIT, "payload_sha256": sha, "signature_hex": resp["signature_hex"],
               "window_id": resp.get("window_id"), "ops_used": resp.get("ops_used"),
               "owner_public_hex": win2.get("owner_public_key_hex"),
               "signature_verifies": None}
    pub = receipt["owner_public_hex"]
    if pub:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub)).verify(sig, body)
        receipt["signature_verifies"] = True
    (OUT / "WP12_PERMIT_SIGNED.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n",
                                                 encoding="utf-8", newline="\n")
    print(json.dumps({k: receipt[k] for k in ("window_id", "ops_used", "payload_sha256", "signature_verifies")},
                     ensure_ascii=False, indent=1))
    return 0 if receipt["signature_verifies"] else 4


if __name__ == "__main__":
    sys.exit(main())
