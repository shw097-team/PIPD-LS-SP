"""Prove the three WP-13 tool patches actually change behaviour, on the patched copies only.

Each test states the defect it must reproduce-then-fix:
  T1 (AO F6) a module that declares NEED v2, loaded under a v1 need, must be refused;
  T2 (AO F3) a grant whose writeset preimage is wrong must refuse the swap;
  T3 (AO F4) issued_at after receipt.started_at must refuse, before started_at must pass;
  T4 (AO F2) the receipt's NEG must report serves_old, not a copy of POS.served;
  T5 (AO F7) a valid, in-TTL, signed grant whose writeset misses the target must refuse for COVERAGE only.
The same tests are also run against the UNPATCHED originals where that is meaningful, so the diff is
attributable to the patch rather than to the fixture.
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
BASE = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "patches"
WP13 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp13"
T = BASE / "tests"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
PATCHED_HOTSWAP = BASE / "PIPD" / "tools" / "hotswap.py"
PATCHED_SRC = BASE / "PIPD" / "src"
ORIG_HOTSWAP = ROOT / "PIPD" / "tools" / "hotswap.py"
ORIG_SRC = ROOT / "PIPD" / "src"

V1 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v1"\ndef build():\n    return Impl()\n'
V2 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\ndef build():\n    return Impl()\n'


def sh(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def run(cmd, env_extra=None, cwd=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=180, env=env, cwd=cwd)
    return {"cmd": [str(c) for c in cmd], "rc": r.returncode, "stdout": (r.stdout or "")[-900:],
            "stderr": (r.stderr or "")[-600:]}


def fixture(tag):
    d = T / tag
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    (d / "occupant.py").write_text(V1, encoding="utf-8", newline="\n")
    (d / "candidate.py").write_text(V2, encoding="utf-8", newline="\n")
    return d


def issue(ws_path, out_path, nonce):
    return run([sys.executable, ISSUER, "issue", "--principal", "owner", "--operation", "install_occupant",
                "--writeset", ws_path, "--ttl", "900", "--epoch", "40",
                "--scope", "WP-FHS-13 remediation test", "--nonce", nonce, "--subject", "WP-FHS-13",
                "--out", out_path])


results = {}

# ---- T1: declared NEED v2 under a v1 requirement -----------------------------
d = fixture("t1")
(d / "occupant_v2need.py").write_text(
    'from pipd_ls_sp.abi import Need\n'
    'NEED = Need("cap.attest", 2, ("identity",))\n'
    'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\n'
    'def build():\n    return Impl()\n', encoding="utf-8", newline="\n")
probe = T / "probe_need.py"
probe.write_text(
    "import sys, json\n"
    "from pathlib import Path\n"
    "from pipd_ls_sp.abi import Need, make_consumer, ABI_VERSION\n"
    f"path = Path(r'{d / 'occupant_v2need.py'}')\n"
    "try:\n"
    "    c = make_consumer(Need('cap.attest', ABI_VERSION, ('identity',)), path)\n"
    "    print(json.dumps({'ok': True, 'value': c.serves('identity')}))\n"
    "except Exception as e:\n"
    "    print(json.dumps({'ok': False, 'type': type(e).__name__, 'code': getattr(e, 'code', None), 'msg': str(e)[:160]}))\n",
    encoding="utf-8", newline="\n")

for label, src in (("patched", PATCHED_SRC), ("original", ORIG_SRC)):
    results[f"T1_{label}"] = run([sys.executable, probe], env_extra={"PYTHONPATH": str(src),
                                                                    "PYTHONDONTWRITEBYTECODE": "1"})

# ---- T2/T5: grants that must be refused -------------------------------------
d2 = fixture("t2")
ws_bad = T / "ws_bad_preimage.json"
ws_bad.write_text(json.dumps({"writeset": [
    {"path": str(d2 / "occupant.py"), "preimage": "0" * 64},
    {"path": str(d2 / "candidate.py"), "preimage": sh(d2 / "candidate.py")}]}, indent=1), encoding="utf-8")
g_bad = T / "grant_bad_preimage.json"
results["T2_issue"] = issue(ws_bad, g_bad, f"T2-{int(time.time())}")

ws_other = T / "ws_misses_target.json"
ws_other.write_text(json.dumps({"writeset": [
    {"path": str(T / "unrelated_a.py"), "preimage": "1" * 64},
    {"path": str(T / "unrelated_b.py"), "preimage": "2" * 64}]}, indent=1), encoding="utf-8")
g_other = T / "grant_misses_target.json"
results["T5_issue"] = issue(ws_other, g_other, f"T5-{int(time.time())}")


def swap(tag, grant, hotswap=PATCHED_HOTSWAP, src=PATCHED_SRC):
    d = fixture(tag)
    out = T / f"receipt_{tag}.json"
    r = run([sys.executable, hotswap, "--root", d, "--entry", "occupant.py", "--candidate", d / "candidate.py",
             "--expect-old", "cap-attest-v1", "--expect-new", "cap-attest-v2",
             "--need", "cap.attest", "--method", "identity",
             "--grant", grant, "--grant-verifier", ISSUER, "--out", out],
            env_extra={"PYTHONPATH": str(src), "PYTHONDONTWRITEBYTECODE": "1"})
    r["receipt"] = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
    return r


results["T2_patched"] = swap("t2", g_bad)
results["T2_original"] = swap("t2", g_bad, hotswap=ORIG_HOTSWAP, src=ORIG_SRC)
results["T5_patched"] = swap("t5", g_other)

# ---- T3: ordering predicate, unit level on the patched binder ----------------
bind_test = T / "bind_ordering.py"
bind_test.write_text(
    "import json, sys\n"
    "from pathlib import Path\n"
    f"sys.path.insert(0, r'{BASE / 'PIPD' / 'tools'}')\n"
    "import importlib.util\n"
    f"spec = importlib.util.spec_from_file_location('hs', r'{PATCHED_HOTSWAP}')\n"
    "hs = importlib.util.module_from_spec(spec); spec.loader.exec_module(hs)\n"
    f"grant = json.loads(Path(r'{WP13 / 'grant_covering.json'}').read_text(encoding='utf-8'))\n"
    "issued = grant['issued_at']\n"
    f"entry = Path(r'{WP13 / 'fixture-covering' / 'candidate.py'}')\n"
    f"cand = Path(r'{WP13 / 'fixture-covering' / 'candidate.py'}')\n"
    "out = {}\n"
    "for label, started in (('started_after_grant', issued + 5), ('started_before_grant', issued - 5)):\n"
    "    info, problems = hs.bind_grant(Path(%r), entry, cand, __import__('hashlib').sha256(cand.read_bytes()).hexdigest(),\n"
    "                                   Path(r'%s'), started_epoch=started)\n"
    "    out[label] = {'issued_before_effect': info.get('issued_before_effect'),\n"
    "                  'ordering_reference': info.get('ordering_reference'), 'problems': problems}\n"
    "print(json.dumps(out, indent=1))\n" % (str(WP13 / "grant_covering.json"), str(ISSUER)),
    encoding="utf-8", newline="\n")
results["T3"] = run([sys.executable, bind_test], env_extra={"PYTHONPATH": str(PATCHED_SRC),
                                                            "PYTHONDONTWRITEBYTECODE": "1"})

(T / "RESULTS.json").write_text(json.dumps(results, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8", newline="\n")

# ---- report ------------------------------------------------------------------
def code_of(r):
    rc = r.get("receipt") or {}
    return rc.get("code") or rc.get("why")


print("T1 patched :", results["T1_patched"]["stdout"].strip()[:200])
print("T1 original:", results["T1_original"]["stdout"].strip()[:200])
for k in ("T2_patched", "T2_original", "T5_patched"):
    r = results[k]
    print(f"{k}: rc={r['rc']} code={code_of(r)} problems={ (r.get('receipt') or {}).get('grant', {}).get('problems') }")
print("T3:", results["T3"]["stdout"].strip()[:400])
t4 = results["T2_patched"].get("receipt") or {}
print("T4 neg fields:", json.dumps(t4.get("neg"), ensure_ascii=False))
