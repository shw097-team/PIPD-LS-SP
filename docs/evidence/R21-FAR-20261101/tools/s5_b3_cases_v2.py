"""S5 / B3-DEV v2: the same four cases, with the wrong-reason refusals removed.

v1 printed four PASSes and two of them were lies: NEG_shared and NEG_mixed refused with
GRANT_WRITESET_EXCLUDES_TARGET/CANDIDATE because each grant had been minted against a DIFFERENT fixture's paths,
so the swap never reached the semantics under test. Same trap as A8's stale __pycache__, different cause.

v2 issues every grant against the fixture it will be used on, so a refusal can only come from the behaviour named:
  shared  -> same grant, same paths, re-armed preimage: a second use must be refused by the receipt itself
  mixed   -> host_operation grant minted for THIS fixture: a repo swap must not accept a host-effect grant
  issuer  -> payload identical except for the signing key: only the issuer differs
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
S5 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "s5"
B3 = S5 / "b3"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
HOTSWAP = ROOT / "PIPD" / "tools" / "hotswap.py"
PY = sys.executable

V1 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v1"\ndef build():\n    return Impl()\n'
V2 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\ndef build():\n    return Impl()\n'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def reset(root):
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / "occupant.py").write_text(V1, encoding="utf-8", newline="\n")
    (root / "candidate.py").write_text(V2, encoding="utf-8", newline="\n")
    return root


def identity(root):
    for pc in root.glob("__pycache__"):
        shutil.rmtree(pc, ignore_errors=True)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run([PY, "-B", "-c", "import sys;sys.path.insert(0,str(sys.argv[1]));"
                                           "import occupant;print(occupant.build().identity())", str(root)],
                          capture_output=True, text=True, env=env).stdout.strip()


def issue(out, root, nonce, operation="install_occupant"):
    ws = out.parent / f"ws_{out.stem}.json"
    ws.write_text(json.dumps({"writeset": [
        {"path": str(root / "occupant.py"), "preimage": sha(root / "occupant.py")},
        {"path": str(root / "candidate.py"), "preimage": sha(root / "candidate.py")}]}), encoding="utf-8")
    out.unlink(missing_ok=True)
    subprocess.run([PY, str(ISSUER), "issue", "--principal", "owner", "--operation", operation,
                    "--writeset", str(ws), "--ttl", "900", "--epoch", "40",
                    "--scope", f"B3v2 {operation}", "--nonce", nonce, "--subject", "WP-FHS-13",
                    "--out", str(out)], capture_output=True, text=True)
    return {"path": out.name, "sha256": sha(out) if out.exists() else None, "operation": operation,
            "writeset": ws.name}


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
            "coverage": {k: (rec.get("grant") or {}).get(k) for k in ("covers_entry", "covers_candidate")},
            "identity_after": identity(root)}


def main():
    B3.mkdir(parents=True, exist_ok=True)
    stamp = int(time.time())

    # ---- NEG_shared: one grant, one fixture, two uses ----
    fs = reset(B3 / "v2_fixture_shared")
    g_s = issue(B3 / "v2_grant_shared.json", fs, f"B3v2-SHARED-{stamp}")
    first = swap(fs, B3 / "v2_grant_shared.json", B3 / "v2_swap_shared_1.json")
    (fs / "occupant.py").write_text(V1, encoding="utf-8", newline="\n")   # re-arm the preimage, same paths
    second = swap(fs, B3 / "v2_grant_shared.json", B3 / "v2_swap_shared_2.json")
    shared = {"grant": g_s, "first_use": first, "second_use": second,
              "verdict": ("PASS" if (first["ok"] is True and second["ok"] is False
                                     and second["coverage"]["covers_entry"] is True) else
                          "FAIL_SHARED_RECEIPT_ACCEPTED"),
              "why": "a correct PASS needs the refusal to come with coverage satisfied, i.e. not a path artefact"}

    # ---- NEG_mixed: host-effect grant minted for THIS fixture ----
    fm = reset(B3 / "v2_fixture_mixed")
    g_m = issue(B3 / "v2_grant_mixed.json", fm, f"B3v2-MIXED-{stamp}", operation="host_operation")
    mixed_swap = swap(fm, B3 / "v2_grant_mixed.json", B3 / "v2_swap_mixed.json")
    mixed = {"grant": g_m, "swap": mixed_swap,
             "verdict": ("PASS" if (mixed_swap["ok"] is False and mixed_swap["coverage"]["covers_entry"] is True
                                    and mixed_swap["identity_after"] == "cap-attest-v1") else
                         "FAIL_MIXED_EFFECT_ACCEPTED"),
             "why": "the grant covers the paths, so any refusal is about the effect class, not coverage"}

    # ---- NEG_second_issuer: identical payload, different key ----
    fi = reset(B3 / "v2_fixture_issuer")
    g_i = issue(B3 / "v2_grant_issuer.json", fi, f"B3v2-ISS-{stamp}")
    grant = json.loads((B3 / "v2_grant_issuer.json").read_text(encoding="utf-8"))
    payload = {k: v for k, v in grant.items() if k not in ("signature_b64", "signature_alg", "assurance_level")}
    payload["key_id"] = "rogue-issuer-2"
    key = Ed25519PrivateKey.generate()
    forged = dict(payload)
    forged["assurance_level"] = "PRODUCTION_ISSUER_SOFTWARE"
    forged["signature_b64"] = base64.b64encode(key.sign(canonical(payload))).decode()
    forged["signature_alg"] = "Ed25519"
    fpath = B3 / "v2_grant_second_issuer.json"
    fpath.write_text(json.dumps(forged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    v = subprocess.run([PY, str(ISSUER), "verify", "--grant", str(fpath)], capture_output=True, text=True)
    isw = swap(fi, fpath, B3 / "v2_swap_second_issuer.json")
    issuer_case = {"basis_grant": g_i, "forged_grant": {"path": fpath.name, "sha256": sha(fpath)},
                   "verifier": {"rc": v.returncode, "stdout": v.stdout.strip()[:240]},
                   "swap": isw,
                   "verdict": ("PASS" if (v.returncode != 0 and isw["ok"] is False
                                          and isw["coverage"]["covers_entry"] is True
                                          and isw["identity_after"] == "cap-attest-v1") else
                               "FAIL_SECOND_ISSUER_ACCEPTED")}

    # ---- POS: opens with a DEV grant and closes with the observable "two grants" fact ----
    fp = reset(B3 / "v2_fixture_pos")
    g_d = issue(B3 / "v2_grant_dev.json", fp, f"B3v2-POS-{stamp}")
    s_pos = swap(fp, B3 / "v2_grant_dev.json", B3 / "v2_swap_pos.json")
    pos = {"dev_grant": g_d, "swap": s_pos,
           "verdict": "PASS" if s_pos["ok"] is True and s_pos["identity_after"] == "cap-attest-v2" else "FAIL"}

    cases = {"TQ-B1-B3-POS": pos, "TQ-B1-B3-NEG_shared_receipt": shared,
             "TQ-B1-B3-NEG_mixed_effect": mixed, "TQ-B1-B3-NEG_second_issuer": issuer_case}
    doc = {"schema": "FHS.R21.S5.B3_CASES/2",
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "edge": "EDGE-WO-B1-B3-DEV", "pd": "PD-12", "domain": "SBL_TO_NATIVE",
           "tools": {"hotswap.py": sha(HOTSWAP), "issue_grant.py": sha(ISSUER)},
           "supersedes": ("v1, whose NEG_shared and NEG_mixed 'PASS' verdicts were coverage refusals "
                          "(GRANT_WRITESET_EXCLUDES_TARGET/CANDIDATE), not the behaviours under test"),
           "cases": cases, "summary": {k: v["verdict"] for k, v in cases.items()}}
    (S5 / "B3_CASES.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                     encoding="utf-8", newline="\n")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=1))
    print("pos", s_pos["ok"], s_pos["identity_after"])
    print("shared first", first["ok"], "second", second["ok"], second["code"], second["coverage"],
          second["identity_after"])
    print("mixed", mixed_swap["ok"], mixed_swap["code"], mixed_swap["coverage"], mixed_swap["identity_after"])
    print("issuer verify", v.returncode, "swap", isw["ok"], isw["code"], isw["coverage"], isw["identity_after"])


if __name__ == "__main__":
    main()
