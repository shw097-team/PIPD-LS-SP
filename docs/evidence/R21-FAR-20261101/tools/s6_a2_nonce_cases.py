"""S6 / EDGE-WO-B1-A2 (ISSUER_SUBJECT): run the edge's own POS and NEG instead of citing a name.

The body says, verbatim:
  POS  Token signature/principal/nonce/subject/TTL checked native-side before spawn; nonce consumed once.
  NEG  wrong issuer or replayed nonce -> PERMIT_SUBJECT_NONCE_REPLAY

So the four things to measure are: a good grant is accepted, a tampered signature is refused, an expired grant is
refused, and a REPLAYED nonce is refused. The fourth is the one that matters: reading issue_grant.py shows
`cmd_issue` appends to the nonce ledger without consulting it, so replay may well be accepted.

This script measures all four and records rc + raw sha for each. It does not fix anything; the patch comes after
the measurement, so the "before" state cannot be back-dated.
"""
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
RUN = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "s6"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
PY = sys.executable


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def issue(out, nonce, ttl=600, subject="WP-FHS-13", cand=None, ws=None):
    cmd = [PY, str(ISSUER), "issue", "--principal", "owner", "--operation", "install_occupant",
           "--writeset", str(ws), "--ttl", str(ttl), "--epoch", "40",
           "--scope", "EDGE-WO-B1-A2 subject/scope/nonce probe", "--nonce", nonce,
           "--subject", subject, "--out", str(out)]
    if cand:
        cmd += ["--candidate-sha", cand]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {"cmd": " ".join(cmd[1:]), "rc": p.returncode,
            "stdout_sha": hashlib.sha256(p.stdout.encode()).hexdigest(),
            "stderr_tail": p.stderr.strip()[-200:], "out_exists": out.exists(),
            "grant_sha": sha(out) if out.exists() else None}


def verify(grant):
    p = subprocess.run([PY, str(ISSUER), "verify", "--grant", str(grant)], capture_output=True, text=True)
    return {"cmd": f"issue_grant.py verify --grant {grant.name}", "rc": p.returncode,
            "stdout": p.stdout.strip()[:400], "stdout_sha": hashlib.sha256(p.stdout.encode()).hexdigest()}


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    fx = RUN / "a2fix"
    fx.mkdir(exist_ok=True)
    (fx / "occupant.py").write_text('def build():\n    return {"cap": "v1"}\n', encoding="utf-8", newline="\n")
    (fx / "candidate.py").write_text('def build():\n    return {"cap": "v2"}\n', encoding="utf-8", newline="\n")
    ws = RUN / "a2_writeset.json"
    ws.write_text(json.dumps({"writeset": [
        {"path": str(fx / "occupant.py"), "preimage": sha(fx / "occupant.py")},
        {"path": str(fx / "candidate.py"), "preimage": sha(fx / "candidate.py")}]}), encoding="utf-8")

    stamp = int(time.time())
    nonce = f"A2-POS-{stamp}"
    g1 = RUN / "grant_a2_pos.json"
    pos = issue(g1, nonce, ws=ws, cand=sha(fx / "candidate.py"))
    pos_verify = verify(g1)

    # the replay: same nonce, fresh grant file
    g2 = RUN / "grant_a2_replay.json"
    replay = issue(g2, nonce, ws=ws, cand=sha(fx / "candidate.py"))
    replay_verify = verify(g2)

    # tampered signature
    tampered = RUN / "grant_a2_tampered.json"
    if g1.exists():
        obj = json.loads(g1.read_text(encoding="utf-8"))
        sig = bytearray(__import__("base64").b64decode(obj["signature_b64"]))
        sig[0] ^= 0xFF
        obj["signature_b64"] = __import__("base64").b64encode(bytes(sig)).decode()
        tampered.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tamper_verify = verify(tampered)

    # expired
    g4 = RUN / "grant_a2_expired.json"
    exp = issue(g4, f"A2-EXP-{stamp}", ttl=-5, ws=ws, cand=sha(fx / "candidate.py"))
    exp_verify = verify(g4)

    cases = {
        "TQ-B1-A2-POS": {"claim": "signed grant with exact subject/scope/candidate is accepted",
                         "issue": pos, "verify": pos_verify,
                         "verdict": "PASS" if pos["rc"] == 0 and pos_verify["rc"] == 0 else "FAIL"},
        "TQ-B1-A2-NEG_replay": {"claim": "a replayed nonce must be refused (PERMIT_SUBJECT_NONCE_REPLAY)",
                                "issue": replay, "verify": replay_verify,
                                "verdict": ("PASS" if replay["rc"] != 0 and replay_verify["rc"] != 0 else
                                            "FAIL_REPLAY_ACCEPTED")},
        "TQ-B1-A2-NEG_signature": {"claim": "a tampered signature is refused",
                                   "verify": tamper_verify,
                                   "verdict": "PASS" if tamper_verify["rc"] != 0 else "FAIL"},
        "TQ-B1-A2-NEG_ttl": {"claim": "an expired grant is refused",
                             "issue": exp, "verify": exp_verify,
                             "verdict": "PASS" if exp_verify["rc"] != 0 else "FAIL"},
    }
    doc = {
        "schema": "FHS.R21.S6.A2_CASES/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "edge": "EDGE-WO-B1-A2", "pd": "PD-02", "domain": "ISSUER_SUBJECT",
        "tool": {"path": "HG-KSEOS/scripts/issue_grant.py", "sha256": sha(ISSUER)},
        "nonce": nonce,
        "cases": cases,
        "summary": {k: v["verdict"] for k, v in cases.items()},
        "finding": ("cmd_issue appends to config/issuer/nonce-ledger.jsonl without checking it, so the same nonce "
                    "mints a second grant that verify() accepts: TQ-B1-A2-NEG_replay fails against the body's own NEG."
                    if cases["TQ-B1-A2-NEG_replay"]["verdict"] != "PASS" else
                    "replay was refused; no finding"),
    }
    (RUN / "A2_CASES.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                       encoding="utf-8", newline="\n")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=1))
    print("pos_verify:", pos_verify["stdout"][:160])
    print("replay_verify:", replay_verify["stdout"][:160])
    print("tamper_verify:", tamper_verify["stdout"][:160])
    print("expired_verify:", exp_verify["stdout"][:160])


if __name__ == "__main__":
    main()
