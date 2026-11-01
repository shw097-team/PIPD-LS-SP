"""S5 / EDGE-WO-B1-B3-DEV (SBL_TO_NATIVE): the DEV/OPS split, and the two ways it can leak.

Body (10B#L157-160):
  POS  DEV file patch != OPS native admission; two WO, two ECP where affected
       judge: DEV/OPS different WOs, separate source diff and real native ACK
  NEG  second issuer or shared receipt -> SECOND_ISSUER_OR_MIXED_EFFECT
       sub-code HANDOFF_ABI_OR_MOCK_ACK

Four probes, each on throwaway fixtures:
  POS            a DEV-operation grant binds a repo swap; a second, separately-issued grant is needed for any
                 other effect, so "two GRANTs" is observable
  NEG_shared     reuse the SAME grant for a second effect on a fresh fixture -> must refuse
  NEG_mixed      a grant minted for a host effect, used to authorise a repo swap -> must refuse
  NEG_issuer     a payload re-signed by a different key/issuer -> must refuse

Everything is measured; nothing is assumed to refuse.
"""
import base64
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
V = ROOT / "var" / "FHS-R21-FAR-TT-20261101"
S5 = V / "s5"
B3 = S5 / "b3"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
HOTSWAP = ROOT / "PIPD" / "tools" / "hotswap.py"
PY = sys.executable

V1 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v1"\ndef build():\n    return Impl()\n'
V2 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\ndef build():\n    return Impl()\n'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def reset(root: pathlib.Path):
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / "occupant.py").write_text(V1, encoding="utf-8", newline="\n")
    (root / "candidate.py").write_text(V2, encoding="utf-8", newline="\n")
    return root


def identity(root: pathlib.Path):
    for pc in root.glob("__pycache__"):
        shutil.rmtree(pc, ignore_errors=True)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run([PY, "-B", "-c", "import sys;sys.path.insert(0,str(sys.argv[1]));"
                                           "import occupant;print(occupant.build().identity())", str(root)],
                          capture_output=True, text=True, env=env).stdout.strip()


def issue(out, root, nonce, operation="install_occupant", subject="WP-FHS-13"):
    ws = out.parent / f"ws_{out.stem}.json"
    ws.write_text(json.dumps({"writeset": [
        {"path": str(root / "occupant.py"), "preimage": sha(root / "occupant.py")},
        {"path": str(root / "candidate.py"), "preimage": sha(root / "candidate.py")}]}), encoding="utf-8")
    out.unlink(missing_ok=True)
    p = subprocess.run([PY, str(ISSUER), "issue", "--principal", "owner", "--operation", operation,
                        "--writeset", str(ws), "--ttl", "900", "--epoch", "40",
                        "--scope", f"EDGE-WO-B1-B3-DEV {operation}", "--nonce", nonce, "--subject", subject,
                        "--out", str(out)], capture_output=True, text=True)
    return {"rc": p.returncode, "sha256": sha(out) if out.exists() else None, "operation": operation}


def swap(root, grant, out):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run([PY, "-B", str(HOTSWAP), "--root", str(root), "--entry", "occupant.py",
                        "--candidate", str(root / "candidate.py"), "--expect-old", "cap-attest-v1",
                        "--expect-new", "cap-attest-v2", "--need", "cap.attest", "--method", "identity",
                        "--grant", str(grant), "--grant-verifier", str(ISSUER), "--out", str(out)],
                       capture_output=True, text=True, env=env, timeout=180)
    rec = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    return {"rc": p.returncode, "ok": rec.get("ok"), "code": rec.get("code"),
            "problems": (rec.get("grant") or {}).get("problems"),
            "identity_after": identity(root)}


def resign_with_second_issuer(grant_path, out_path):
    grant = json.loads(grant_path.read_text(encoding="utf-8"))
    payload = {k: v for k, v in grant.items() if k not in ("signature_b64", "signature_alg", "assurance_level")}
    payload["key_id"] = "rogue-issuer-2"
    key = Ed25519PrivateKey.generate()
    sig = key.sign(canonical(payload))
    forged = dict(payload)
    forged["assurance_level"] = "PRODUCTION_ISSUER_SOFTWARE"
    forged["signature_b64"] = base64.b64encode(sig).decode()
    forged["signature_alg"] = "Ed25519"
    out_path.write_text(json.dumps(forged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {"path": out_path.name, "sha256": sha(out_path),
            "rogue_public_b64": base64.b64encode(key.public_key().public_bytes_raw()).decode()}


def main():
    B3.mkdir(parents=True, exist_ok=True)
    stamp = int(time.time())

    # POS: a DEV grant binds the swap; the effect is a repo write, not a host op
    fa = reset(B3 / "fixture_pos")
    g_dev = issue(B3 / "grant_dev.json", fa, f"B3-POS-{stamp}", operation="install_occupant")
    s_pos = swap(fa, B3 / "grant_dev.json", B3 / "swap_pos.json")
    # a second effect needs its own grant: mint a host-effect grant separately
    g_ops = issue(B3 / "grant_ops.json", fa, f"B3-OPS-{stamp}", operation="host_operation")

    # NEG_shared: reuse the same DEV grant on a fresh fixture
    fb = reset(B3 / "fixture_shared")
    s_shared = swap(fb, B3 / "grant_dev.json", B3 / "swap_shared.json")

    # NEG_mixed: use the host-effect grant to authorise a repo swap
    fc = reset(B3 / "fixture_mixed")
    s_mixed = swap(fc, B3 / "grant_ops.json", B3 / "swap_mixed.json")

    # NEG_issuer: same payload re-signed by a second issuer
    forged = resign_with_second_issuer(B3 / "grant_dev.json", B3 / "grant_second_issuer.json")
    p = subprocess.run([PY, str(ISSUER), "verify", "--grant", str(B3 / "grant_second_issuer.json")],
                       capture_output=True, text=True)
    fd = reset(B3 / "fixture_second_issuer")
    s_issuer = swap(fd, B3 / "grant_second_issuer.json", B3 / "swap_second_issuer.json")

    cases = {
        "TQ-B1-B3-POS": {
            "claim": "a DEV grant binds the repo swap; DEV and OPS are separate grants for separate WOs",
            "dev_grant": g_dev, "ops_grant": g_ops, "swap": s_pos,
            "verdict": "PASS" if s_pos["ok"] is True and s_pos["identity_after"] == "cap-attest-v2" else "FAIL",
        },
        "TQ-B1-B3-NEG_shared_receipt": {
            "claim": "the same grant may not authorise a second effect (shared receipt)",
            "swap": s_shared,
            "verdict": "PASS" if (s_shared["ok"] is False and s_shared["identity_after"] == "cap-attest-v1") else
                       "FAIL_SHARED_RECEIPT_ACCEPTED",
        },
        "TQ-B1-B3-NEG_mixed_effect": {
            "claim": "a host-effect grant may not authorise a repository write (mixed effect)",
            "swap": s_mixed,
            "verdict": "PASS" if (s_mixed["ok"] is False and s_mixed["identity_after"] == "cap-attest-v1") else
                       "FAIL_MIXED_EFFECT_ACCEPTED",
        },
        "TQ-B1-B3-NEG_second_issuer": {
            "claim": "a payload re-signed by a second issuer is refused",
            "forged_grant": forged,
            "verifier": {"rc": p.returncode, "stdout": p.stdout.strip()[:200]},
            "swap": s_issuer,
            "verdict": "PASS" if (p.returncode != 0 and s_issuer["ok"] is False
                                  and s_issuer["identity_after"] == "cap-attest-v1") else "FAIL_SECOND_ISSUER_ACCEPTED",
        },
    }
    doc = {"schema": "FHS.R21.S5.B3_CASES/1",
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "edge": "EDGE-WO-B1-B3-DEV", "pd": "PD-12", "domain": "SBL_TO_NATIVE",
           "tools": {"hotswap.py": sha(HOTSWAP), "issue_grant.py": sha(ISSUER)},
           "cases": cases, "summary": {k: v["verdict"] for k, v in cases.items()}}
    (S5 / "B3_CASES.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                     encoding="utf-8", newline="\n")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=1))
    print("pos:", s_pos["ok"], s_pos["identity_after"], "| shared:", s_shared["ok"], s_shared["identity_after"],
          "| mixed:", s_mixed["ok"], s_mixed["identity_after"],
          "| issuer:", p.returncode, s_issuer["ok"], s_issuer["identity_after"])


if __name__ == "__main__":
    main()
