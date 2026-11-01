"""S5 / EDGE-WO-B1-A8 (NATIVE_HOTPATH): POS, rollback, and two NEGs -- with the false-pass removed.

The first run of this probe printed PASS for both NEGs and I nearly kept it. The receipts say otherwise:
both refused with ERR_OCCUPANT_MISMATCH ("occupant reports 'cap-attest-v2', expected 'cap-attest-v1'"), i.e. the
negative fixture was still serving the POS candidate because a stale __pycache__ came along with copytree. A refusal
for the wrong reason is not a pass, so this version asserts the occupant identity before every swap and clears
bytecode caches, and it tests rollback the way the tool implements it (restore .prev on failure) instead of
looking for a backup file that the tool never writes on success.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
V = ROOT / "var" / "FHS-R21-FAR-TT-20261101"
S5 = V / "s5"
A8 = S5 / "a8"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
HOTSWAP = ROOT / "PIPD" / "tools" / "hotswap.py"
PY = sys.executable

V1 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v1"\ndef build():\n    return Impl()\n'
V2 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\ndef build():\n    return Impl()\n'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def reset(root: pathlib.Path, candidate=V2):
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / "occupant.py").write_text(V1, encoding="utf-8", newline="\n")
    (root / "candidate.py").write_text(candidate, encoding="utf-8", newline="\n")


def identity(root: pathlib.Path):
    for pc in root.glob("__pycache__"):
        shutil.rmtree(pc, ignore_errors=True)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run([PY, "-B", "-c", "import sys;sys.path.insert(0,str(sys.argv[1]));"
                                        "import occupant;print(occupant.build().identity())", str(root)],
                       capture_output=True, text=True, env=env)
    return p.stdout.strip()


def issue(out, ws, nonce):
    p = subprocess.run([PY, str(ISSUER), "issue", "--principal", "owner", "--operation", "install_occupant",
                        "--writeset", str(ws), "--ttl", "900", "--epoch", "40",
                        "--scope", "EDGE-WO-B1-A8 hotpath probe", "--nonce", nonce, "--subject", "WP-FHS-13",
                        "--out", str(out)], capture_output=True, text=True)
    return {"rc": p.returncode, "exists": out.exists(), "sha256": sha(out) if out.exists() else None}


def swap(root, grant, out, expect_new="cap-attest-v2"):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run([PY, "-B", str(HOTSWAP), "--root", str(root), "--entry", "occupant.py",
                        "--candidate", str(root / "candidate.py"), "--expect-old", "cap-attest-v1",
                        "--expect-new", expect_new, "--need", "cap.attest", "--method", "identity",
                        "--grant", str(grant), "--grant-verifier", str(ISSUER), "--out", str(out)],
                       capture_output=True, text=True, env=env, timeout=180)
    rec = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    return {"rc": p.returncode, "receipt": out.name, "ok": rec.get("ok"), "code": rec.get("code"),
            "why": (rec.get("why") or "")[:160], "steps": rec.get("steps"),
            "problems": (rec.get("grant") or {}).get("problems"), "rollback": rec.get("rollback"),
            "stderr_tail": p.stderr.strip()[-160:]}


def main():
    A8.mkdir(parents=True, exist_ok=True)

    # ---------- POS: real swap + independent regression ----------
    fx = A8 / "fixture"
    reset(fx)
    pre_entry = sha(fx / "occupant.py")
    before = identity(fx)
    if before != "cap-attest-v1":
        raise SystemExit(f"fixture precondition broken: occupant reports {before!r}")
    ws = A8 / "ws_good.json"
    ws.write_text(json.dumps({"writeset": [{"path": str(fx / "occupant.py"), "preimage": pre_entry},
                                           {"path": str(fx / "candidate.py"), "preimage": sha(fx / "candidate.py")}]}),
                  encoding="utf-8")
    g = A8 / "grant_good.json"
    g.unlink(missing_ok=True)
    i_pos = issue(g, ws, f"A8-POS-{int(time.time())}")
    s_pos = swap(fx, g, A8 / "swap_pos.json")
    after = identity(fx)
    pos = {"grant": i_pos, "swap": s_pos,
           "regression": {"before": before, "after": after, "changed": before != after},
           "preimage_at_swap_time": pre_entry,
           "verdict": "PASS" if (s_pos["ok"] is True and before == "cap-attest-v1" and after == "cap-attest-v2")
                      else "FAIL"}

    # ---------- POS_rollback: parity failure must restore the preimage ----------
    fr = A8 / "fixture_rollback"
    reset(fr)
    pre_r = sha(fr / "occupant.py")
    (fr / "candidate.py").write_text('class Impl:\n    def identity(self):\n        return "cap-attest-WRONG"\n'
                                     'def build():\n    return Impl()\n', encoding="utf-8", newline="\n")
    ws_r = A8 / "ws_rollback.json"
    ws_r.write_text(json.dumps({"writeset": [{"path": str(fr / "occupant.py"), "preimage": pre_r},
                                             {"path": str(fr / "candidate.py"), "preimage": sha(fr / "candidate.py")}]}),
                    encoding="utf-8")
    g_r = A8 / "grant_rollback.json"
    g_r.unlink(missing_ok=True)
    issue(g_r, ws_r, f"A8-ROLL-{int(time.time())}")
    s_roll = swap(fr, g_r, A8 / "swap_rollback.json")
    restored_ok = (sha(fr / "occupant.py") == pre_r)
    rollback = {"swap": s_roll, "preimage_before": pre_r, "preimage_after": sha(fr / "occupant.py"),
                "byte_identical": restored_ok, "occupant_identity": identity(fr),
                "verdict": "PASS" if (s_roll["ok"] is False and restored_ok and identity(fr) == "cap-attest-v1")
                           else "FAIL"}

    # ---------- NEG1: writeset excludes the target (unbounded write) ----------
    fe = A8 / "fixture_escape"
    reset(fe)
    ws_e = A8 / "ws_escape.json"
    ws_e.write_text(json.dumps({"writeset": [{"path": str(fe / "unrelated.txt"), "preimage": "0" * 64}]}),
                    encoding="utf-8")
    g_e = A8 / "grant_escape.json"
    g_e.unlink(missing_ok=True)
    issue(g_e, ws_e, f"A8-ESC-{int(time.time())}")
    s_e = swap(fe, g_e, A8 / "swap_escape.json")
    esc = {"swap": s_e, "target_sha_before": sha(fe / "occupant.py"), "target_identity": identity(fe),
           "verdict": ("PASS" if (s_e["ok"] is False and identity(fe) == "cap-attest-v1"
                                  and (s_e["problems"] and any("WRITESET" in p for p in s_e["problems"])
                                       or s_e["code"] in ("ERR_GRANT_NOT_BOUND", "ERR_WRITESET_ESCAPE")))
                       else "FAIL")}

    # ---------- NEG2: preimage is not the file's (missing red reproducer) ----------
    fn = A8 / "fixture_no_red"
    reset(fn)
    ws_n = A8 / "ws_no_red.json"
    ws_n.write_text(json.dumps({"writeset": [{"path": str(fn / "occupant.py"), "preimage": "f" * 64},
                                             {"path": str(fn / "candidate.py"), "preimage": sha(fn / "candidate.py")}]}),
                    encoding="utf-8")
    g_n = A8 / "grant_no_red.json"
    g_n.unlink(missing_ok=True)
    issue(g_n, ws_n, f"A8-RED-{int(time.time())}")
    s_n = swap(fn, g_n, A8 / "swap_no_red.json")
    red = {"swap": s_n, "target_identity_after": identity(fn),
           "verdict": ("PASS" if (s_n["ok"] is False and identity(fn) == "cap-attest-v1") else
                       "FAIL_PREIMAGE_MISMATCH_ACCEPTED")}

    cases = {"TQ-B1-A8-POS": pos, "TQ-B1-A8-POS_rollback": rollback,
             "TQ-B1-A8-NEG_scope_escape": esc, "TQ-B1-A8-NEG_missing_red_reproducer": red}
    doc = {"schema": "FHS.R21.S5.A8_CASES/2",
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "edge": "EDGE-WO-B1-A8", "pd": "PD-08", "domain": "NATIVE_HOTPATH",
           "tools": {"hotswap.py": sha(HOTSWAP), "issue_grant.py": sha(ISSUER)},
           "supersedes": "v1 of this probe, whose two NEG 'PASS'es were refusals for the wrong reason "
                         "(ERR_OCCUPANT_MISMATCH from a stale __pycache__)",
           "cases": cases, "summary": {k: v["verdict"] for k, v in cases.items()}}
    (S5 / "A8_CASES.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8", newline="\n")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=1))
    print("pos:", s_pos["ok"], s_pos["steps"], before, "->", after)
    print("rollback:", s_roll["code"], "restored", restored_ok, identity(fr))
    print("escape:", s_e["code"], s_e["problems"], identity(fe))
    print("no_red:", s_n["code"], s_n["problems"], identity(fn))


if __name__ == "__main__":
    main()
