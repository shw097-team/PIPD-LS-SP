"""S5 / EDGE-WO-B1-A8 (NATIVE_HOTPATH): run the edge's POS and NEG against the real swap path.

Body (10B#L109-112):
  POS  Exact current hotpath with rollback pointer and independent regression
  NEG  unbounded writes or missing red reproducer -> HOTPATH_UNRESOLVED
       (sub-code UNMEASURED_REPAIR_OR_SCOPE_ESCAPE)

Cases run on a fixture, never on the live hotpath:
  POS  grant covers entry+candidate with true preimages  -> swap happens, backup is the rollback pointer,
       and an independent pre/post identity read is the regression
  NEG1 writeset excludes the target                      -> must refuse (scope escape)
  NEG2 writeset names a preimage that is not the file's  -> must refuse (no red reproducer for that write)

The canonical hotswap.py is known (AO finding F3) not to read preimages, so NEG2 is expected to expose that at the
edge level rather than only in the WP-13 review.
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
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
HOTSWAP = ROOT / "PIPD" / "tools" / "hotswap.py"
PY = sys.executable


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def issue(out, ws, nonce, subject="WP-FHS-13"):
    p = subprocess.run([PY, str(ISSUER), "issue", "--principal", "owner", "--operation", "install_occupant",
                        "--writeset", str(ws), "--ttl", "900", "--epoch", "40",
                        "--scope", "EDGE-WO-B1-A8 hotpath probe", "--nonce", nonce, "--subject", subject,
                        "--out", str(out)], capture_output=True, text=True)
    return {"rc": p.returncode, "stdout": p.stdout.strip()[:200], "exists": out.exists(),
            "sha256": sha(out) if out.exists() else None}


def swap(fixture, grant, out, entry="occupant.py"):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run([PY, str(HOTSWAP), "--root", str(fixture), "--entry", entry,
                        "--candidate", str(fixture / "candidate.py"), "--expect-old", "cap-attest-v1",
                        "--expect-new", "cap-attest-v2", "--need", "cap.attest", "--method", "identity",
                        "--grant", str(grant), "--grant-verifier", str(ISSUER), "--out", str(out)],
                       capture_output=True, text=True, env=env, timeout=180)
    rec = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    return {"rc": p.returncode, "receipt": str(out), "ok": rec.get("ok"), "steps": rec.get("steps"),
            "problems": (rec.get("grant") or {}).get("problems"),
            "preimage_checks": rec.get("preimage_checks"), "stderr_tail": p.stderr.strip()[-200:]}


def main():
    S5.mkdir(parents=True, exist_ok=True)
    fx = S5 / "a8" / "fixture"
    fx.mkdir(parents=True, exist_ok=True)
    (fx / "occupant.py").write_text('class Impl:\n    def identity(self):\n        return "cap-attest-v1"\n'
                                    'def build():\n    return Impl()\n', encoding="utf-8", newline="\n")
    (fx / "candidate.py").write_text('class Impl:\n    def identity(self):\n        return "cap-attest-v2"\n'
                                     'def build():\n    return Impl()\n', encoding="utf-8", newline="\n")
    for stale in fx.glob("occupant.py.hotswap-backup"):
        stale.unlink()
    pre_entry, pre_cand = sha(fx / "occupant.py"), sha(fx / "candidate.py")
    stamp = int(time.time())

    ws_good = S5 / "a8" / "ws_good.json"
    ws_good.write_text(json.dumps({"writeset": [
        {"path": str(fx / "occupant.py"), "preimage": pre_entry},
        {"path": str(fx / "candidate.py"), "preimage": pre_cand}]}), encoding="utf-8")
    ws_escape = S5 / "a8" / "ws_escape.json"
    ws_escape.write_text(json.dumps({"writeset": [
        {"path": str(fx / "unrelated.txt"), "preimage": "0" * 64}]}), encoding="utf-8")
    ws_no_red = S5 / "a8" / "ws_no_red.json"
    ws_no_red.write_text(json.dumps({"writeset": [
        {"path": str(fx / "occupant.py"), "preimage": "f" * 64},
        {"path": str(fx / "candidate.py"), "preimage": pre_cand}]}), encoding="utf-8")

    g_good, g_escape, g_no_red = (S5 / "a8" / n for n in ("grant_good.json", "grant_escape.json", "grant_no_red.json"))
    for g in (g_good, g_escape, g_no_red):
        g.unlink(missing_ok=True)
    i_good = issue(g_good, ws_good, f"A8-POS-{stamp}")
    i_escape = issue(g_escape, ws_escape, f"A8-ESC-{stamp}")
    i_no_red = issue(g_no_red, ws_no_red, f"A8-RED-{stamp}")

    before_identity = subprocess.run([PY, "-c", "import sys;sys.path.insert(0,str(sys.argv[1]));"
                                                "import occupant;print(occupant.build().identity())", str(fx)],
                                     capture_output=True, text=True)
    s_pos = swap(fx, g_good, S5 / "a8" / "swap_pos.json")
    after_identity = subprocess.run([PY, "-c", "import sys;sys.path.insert(0,str(sys.argv[1]));"
                                               "import occupant;print(occupant.build().identity())", str(fx)],
                                    capture_output=True, text=True)
    backup = fx / "occupant.py.hotswap-backup"
    rollback = {"backup_exists": backup.exists(),
                "backup_sha256": sha(backup) if backup.exists() else None,
                "matches_preimage": (sha(backup) == pre_entry) if backup.exists() else False,
                "note": "the backup file is the rollback pointer the body demands" if backup.exists() else
                        "no backup file: no rollback pointer"}

    # NEG cases run against a fresh fixture so the POS swap cannot mask them
    fx2 = S5 / "a8" / "fixture_neg"
    if fx2.exists():
        shutil.rmtree(fx2)
    shutil.copytree(fx, fx2)
    (fx2 / "occupant.py").write_text('class Impl:\n    def identity(self):\n        return "cap-attest-v1"\n'
                                     'def build():\n    return Impl()\n', encoding="utf-8", newline="\n")
    ws_escape2 = S5 / "a8" / "ws_escape2.json"
    ws_escape2.write_text(json.dumps({"writeset": [
        {"path": str(fx2 / "unrelated.txt"), "preimage": "0" * 64}]}), encoding="utf-8")
    ws_no_red2 = S5 / "a8" / "ws_no_red2.json"
    ws_no_red2.write_text(json.dumps({"writeset": [
        {"path": str(fx2 / "occupant.py"), "preimage": "f" * 64},
        {"path": str(fx2 / "candidate.py"), "preimage": sha(fx2 / "candidate.py")}]}), encoding="utf-8")
    g_e2, g_r2 = S5 / "a8" / "grant_escape2.json", S5 / "a8" / "grant_no_red2.json"
    for g in (g_e2, g_r2):
        g.unlink(missing_ok=True)
    issue(g_e2, ws_escape2, f"A8-ESC2-{stamp}")
    issue(g_r2, ws_no_red2, f"A8-RED2-{stamp}")
    s_escape = swap(fx2, g_e2, S5 / "a8" / "swap_escape.json")
    occupant_after_escape = (fx2 / "occupant.py").read_text(encoding="utf-8")
    s_no_red = swap(fx2, g_r2, S5 / "a8" / "swap_no_red.json")
    occupant_after_no_red = (fx2 / "occupant.py").read_text(encoding="utf-8")

    cases = {
        "TQ-B1-A8-POS": {
            "claim": "exact current hotpath with rollback pointer and independent regression",
            "grant": i_good, "swap": s_pos,
            "independent_regression": {"before": before_identity.stdout.strip(), "after": after_identity.stdout.strip(),
                                       "changed": before_identity.stdout.strip() != after_identity.stdout.strip()},
            "rollback": rollback,
            "verdict": ("PASS" if s_pos["ok"] and rollback["matches_preimage"]
                        and before_identity.stdout.strip() != after_identity.stdout.strip() else "FAIL"),
        },
        "TQ-B1-A8-NEG_scope_escape": {
            "claim": "unbounded writes (writeset excludes the target) -> HOTPATH_UNRESOLVED",
            "grant": i_escape, "swap": s_escape,
            "target_untouched": "cap-attest-v1" in occupant_after_escape,
            "verdict": "PASS" if (s_escape["rc"] != 0 and "cap-attest-v1" in occupant_after_escape) else
                       "FAIL_UNBOUNDED_WRITE_ACCEPTED",
        },
        "TQ-B1-A8-NEG_missing_red_reproducer": {
            "claim": "missing red reproducer (preimage is not the file's) -> HOTPATH_UNRESOLVED",
            "grant": i_no_red, "swap": s_no_red,
            "target_untouched": "cap-attest-v1" in occupant_after_no_red,
            "verdict": "PASS" if (s_no_red["rc"] != 0 and "cap-attest-v1" in occupant_after_no_red) else
                       "FAIL_PREIMAGE_MISMATCH_ACCEPTED",
        },
    }
    doc = {
        "schema": "FHS.R21.S5.A8_CASES/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "edge": "EDGE-WO-B1-A8", "pd": "PD-08", "domain": "NATIVE_HOTPATH",
        "tools": {"hotswap.py": sha(HOTSWAP), "issue_grant.py": sha(ISSUER)},
        "cases": cases,
        "summary": {k: v["verdict"] for k, v in cases.items()},
    }
    (S5 / "A8_CASES.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8", newline="\n")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=1))
    print("pos:", s_pos["ok"], s_pos["steps"], "| rollback", rollback["matches_preimage"])
    print("escape rc:", s_escape["rc"], s_escape["problems"], "| no_red rc:", s_no_red["rc"], s_no_red["problems"])


if __name__ == "__main__":
    main()
