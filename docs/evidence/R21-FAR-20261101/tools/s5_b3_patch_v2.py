"""Candidate patch for the two B3 defects: single-use receipts and effect-class binding.

Measured (s5/B3_CASES.json v2):
  * the same DEV grant authorised two separate swaps (coverage satisfied both times) -> no receipt consumption
  * a grant minted with operation=host_operation authorised a repository swap -> the operation is never read

The patch builds on the preimage-checking candidate already produced for WP-13, so the final candidate is one file
that refuses stale preimages, foreign effects, and reused receipts. Canonical PIPD/tools/hotswap.py is untouched.
"""
import difflib
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
B3 = S5 / "b3"
BASE_PATCHED = V / "patches" / "PIPD" / "tools" / "hotswap.py"
CANON = ROOT / "PIPD" / "tools" / "hotswap.py"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
PY = sys.executable

V1 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v1"\ndef build():\n    return Impl()\n'
V2 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\ndef build():\n    return Impl()\n'

CONSUME_HELPER = '''

def _consume(grant: dict, entry, candidate) -> None:
    """Burn the receipt so a second bind of the same grant on the same target cannot pass."""
    ledger = Path(os.environ.get("HGK_CONSUMED_LEDGER", str(Path.home() / ".hgk-consumed.jsonl")))
    row = {"nonce": grant.get("nonce"), "entry": _norm(entry), "candidate": _norm(candidate),
           "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\\n")

'''


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def build():
    out_dir = S5 / "patch"
    out_dir.mkdir(parents=True, exist_ok=True)
    text = BASE_PATCHED.read_text(encoding="utf-8")

    anchor = "    # 4. the grant must name the exact artefact when it names one at all"
    if anchor not in text:
        raise SystemExit("preimage block not found; refusing to guess")
    effect_block = (
        "    # 3c. the grant's operation must belong to THIS effect class.\n"
        '    DEV_OPERATIONS = {"install_occupant", "repo_write", "repo_patch"}\n'
        '    op = (grant.get("operation") or "").strip()\n'
        '    info["operation"] = op\n'
        "    if op and op not in DEV_OPERATIONS:\n"
        '        problems.append("GRANT_EFFECT_MISMATCH")\n\n' + anchor)
    text2 = text.replace(anchor, effect_block, 1)

    consume_block = (
        "    # 3d. a receipt is single-use: burned against this exact (entry, candidate) pair.\n"
        '    ledger = Path(os.environ.get("HGK_CONSUMED_LEDGER", str(Path.home() / ".hgk-consumed.jsonl")))\n'
        '    key = {"nonce": grant.get("nonce"), "entry": _norm(entry), "candidate": _norm(candidate)}\n'
        '    info["receipt_key"] = key\n'
        "    if ledger.exists():\n"
        '        for line in ledger.read_text(encoding="utf-8").splitlines():\n'
        "            try:\n"
        "                prior = json.loads(line)\n"
        "            except json.JSONDecodeError:\n"
        "                continue\n"
        '            if prior.get("nonce") == key["nonce"] and prior.get("entry") == key["entry"]:\n'
        '                problems.append("GRANT_ALREADY_CONSUMED")\n'
        '                info["consumed_by"] = prior\n'
        "                break\n\n" + anchor)
    text2 = text2.replace(anchor, consume_block, 1)

    ret = "    return info, problems\n"
    if ret not in text2:
        raise SystemExit("bind_grant return not found; refusing to guess")
    text2 = text2.replace(ret, "    if not problems:\n        _consume(grant, entry, candidate)\n" + ret, 1)

    marker = "\ndef main("
    if marker not in text2:
        raise SystemExit("module-level main() not found; refusing to guess where to define _consume")
    text2 = text2.replace(marker, CONSUME_HELPER + "def main(", 1)

    (out_dir / "PIPD" / "tools").mkdir(parents=True, exist_ok=True)
    src_dst = out_dir / "PIPD" / "src"
    if not src_dst.exists():
        shutil.copytree(ROOT / "PIPD" / "src", src_dst)
    dst = out_dir / "PIPD" / "tools" / "hotswap_b3.py"
    dst.write_text(text2, encoding="utf-8", newline="\n")
    diff = difflib.unified_diff(CANON.read_text(encoding="utf-8").splitlines(True), text2.splitlines(True),
                                fromfile="a/PIPD/tools/hotswap.py", tofile="b/PIPD/tools/hotswap.py", n=3)
    (out_dir / "hotswap.b3.patch").write_text("".join(diff), encoding="utf-8", newline="\n")
    return dst


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


def issue(out, root, nonce, operation="install_occupant", preimage_overrides=None):
    ws = out.parent / f"ws_{out.stem}.json"
    entries = [{"path": str(root / "occupant.py"), "preimage": sha(root / "occupant.py")},
               {"path": str(root / "candidate.py"), "preimage": sha(root / "candidate.py")}]
    if preimage_overrides:
        for e in entries:
            for suffix, value in preimage_overrides.items():
                if e["path"].endswith(suffix):
                    e["preimage"] = value
    ws.write_text(json.dumps({"writeset": entries}), encoding="utf-8")
    out.unlink(missing_ok=True)
    subprocess.run([PY, str(ISSUER), "issue", "--principal", "owner", "--operation", operation,
                    "--writeset", str(ws), "--ttl", "900", "--epoch", "40",
                    "--scope", f"B3 patch {operation}", "--nonce", nonce, "--subject", "WP-FHS-13",
                    "--out", str(out)], capture_output=True, text=True)


def swap(tool, root, grant, out, ledger):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["HGK_CONSUMED_LEDGER"] = str(ledger)
    p = subprocess.run([PY, "-B", str(tool), "--root", str(root), "--entry", "occupant.py",
                        "--candidate", str(root / "candidate.py"), "--expect-old", "cap-attest-v1",
                        "--expect-new", "cap-attest-v2", "--need", "cap.attest", "--method", "identity",
                        "--grant", str(grant), "--grant-verifier", str(ISSUER), "--out", str(out)],
                       capture_output=True, text=True, env=env, timeout=180)
    rec = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    return {"rc": p.returncode, "ok": rec.get("ok"), "code": rec.get("code"),
            "problems": (rec.get("grant") or {}).get("problems"),
            "identity_after": identity(root), "stderr_tail": p.stderr.strip()[-160:]}


def main():
    tool = build()
    syntax = subprocess.run([PY, "-c", f"import ast;ast.parse(open(r'{tool}',encoding='utf-8').read());print('ok')"],
                            capture_output=True, text=True)
    if syntax.returncode != 0:
        raise SystemExit(f"patched copy does not parse: {syntax.stderr[-400:]}")

    ledger = B3 / "consumed_ledger.jsonl"
    ledger.unlink(missing_ok=True)
    stamp = int(time.time())

    f1 = reset(B3 / "p_fixture")
    issue(B3 / "p_grant.json", f1, f"B3P-{stamp}")
    t1 = swap(tool, f1, B3 / "p_grant.json", B3 / "p_swap1.json", ledger)
    (f1 / "occupant.py").write_text(V1, encoding="utf-8", newline="\n")
    t2 = swap(tool, f1, B3 / "p_grant.json", B3 / "p_swap2.json", ledger)

    f2 = reset(B3 / "p_fixture_ops")
    issue(B3 / "p_grant_ops.json", f2, f"B3P-OPS-{stamp}", operation="host_operation")
    t3 = swap(tool, f2, B3 / "p_grant_ops.json", B3 / "p_swap_ops.json", ledger)

    f3 = reset(B3 / "p_fixture_pre")
    issue(B3 / "p_grant_pre.json", f3, f"B3P-PRE-{stamp}", preimage_overrides={"occupant.py": "f" * 64})
    t4 = swap(tool, f3, B3 / "p_grant_pre.json", B3 / "p_swap_pre.json", ledger)

    tests = {
        "T1_first_use_bound": {"expect": "ok", "got": {k: t1[k] for k in ("rc", "ok", "code", "problems")},
                               "verdict": "PASS" if t1["ok"] is True else "FAIL"},
        "T2_second_use_refused": {"expect": "GRANT_ALREADY_CONSUMED",
                                  "got": {k: t2[k] for k in ("rc", "ok", "code", "problems")},
                                  "verdict": "PASS" if (t2["ok"] is False and
                                                        "GRANT_ALREADY_CONSUMED" in (t2["problems"] or [])) else "FAIL"},
        "T3_host_effect_refused": {"expect": "GRANT_EFFECT_MISMATCH",
                                   "got": {k: t3[k] for k in ("rc", "ok", "code", "problems")},
                                   "verdict": "PASS" if (t3["ok"] is False and
                                                         "GRANT_EFFECT_MISMATCH" in (t3["problems"] or [])) else "FAIL"},
        "T4_stale_preimage_refused": {"expect": "GRANT_PREIMAGE_MISMATCH_ENTRY",
                                      "got": {k: t4[k] for k in ("rc", "ok", "code", "problems")},
                                      "verdict": "PASS" if (t4["ok"] is False and
                                                            "GRANT_PREIMAGE_MISMATCH_ENTRY" in (t4["problems"] or [])) else "FAIL"},
    }
    doc = {"schema": "FHS.R21.S5.B3_PATCH_TEST/1",
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "canonical_untouched": {"path": "PIPD/tools/hotswap.py", "sha256": sha(CANON)},
           "base": {"path": str(BASE_PATCHED.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(BASE_PATCHED),
                    "note": "the WP-13 preimage candidate; this patch extends it"},
           "patch": {"file": "s5/patch/hotswap.b3.patch", "bytes": (S5 / "patch/hotswap.b3.patch").stat().st_size,
                     "sha256": sha(S5 / "patch/hotswap.b3.patch"), "patched_copy_sha256": sha(tool)},
           "pre_state": {"ref": "s5/B3_CASES.json", "shared_receipt": "FAIL_SHARED_RECEIPT_ACCEPTED",
                         "mixed_effect": "FAIL_MIXED_EFFECT_ACCEPTED"},
           "tests": tests, "summary": {k: v["verdict"] for k, v in tests.items()},
           "claim_ceiling": ("candidate only, proven on copies; canonical hotswap.py still accepts reuse and foreign "
                             "effects until an authorised change lands")}
    (S5 / "B3_PATCH_TEST.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=1))
    for name, t in (("t1", t1), ("t2", t2), ("t3", t3), ("t4", t4)):
        print(name, t["ok"], t["code"], t["problems"], t["identity_after"])


if __name__ == "__main__":
    main()
