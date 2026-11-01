"""S5 / EDGE-WO-B1-C5 (CODEX_MINPATCH): allowlist discipline, narrow rollback, and a checker-edited diff.

Body (10B#L337-340):
  POS  No edit outside allowlist; narrow rollback   (judge: only affected files changed and full regression independent)
  NEG  checker edits same diff or no red test -> UNBOUNDED_PATCH_OR_REGRESSION

Measured against the selector candidate (s5/patch/PIPD/tools/hotswap_selector.py), which carries the preimage,
effect-class, single-use-receipt and one-live-ECP guards. The canonical tool is untouched.

Cases
  POS_allowlist_and_rollback   a grant whose writeset covers exactly the entry and the candidate; after the swap the
                               entry equals the candidate byte-for-byte, no other file changed, and restoring the
                               preimage returns the entry to its original sha (narrow rollback).
  NEG_allowlist_escape         a grant whose writeset covers a file that is NOT the entry; the swap must be refused
                               (this is the allowlist boundary) and the entry must stay byte-identical.
  NEG_checker_edits_diff       after a successful swap, mutate the landed file the way a checker would; the receipt's
                               candidate_sha256 no longer matches disk. Measures DETECTABILITY, not prevention: the
                               honest reading is "a re-verify step catches it", not "the tool blocks it".
  POS_regression_independent   identity is read in a separate process before and after, so the regression is not an
                               in-process invariant of the writer.
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
C5 = S5 / "c5"
TOOL = S5 / "patch" / "PIPD" / "tools" / "hotswap_selector.py"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
PY = sys.executable

V1 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v1"\ndef build():\n    return Impl()\n'
V2 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\ndef build():\n    return Impl()\n'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def reset(root):
    if root.exists():
        shutil.rmtree(root)
    (root / "src").mkdir(parents=True)
    (root / "docs").mkdir(parents=True)
    (root / "src" / "app.py").write_text(V1, encoding="utf-8", newline="\n")
    (root / "docs" / "README.md").write_text("# fixture\n\nuntouched by the patch.\n", encoding="utf-8", newline="\n")
    (root / "candidate.py").write_text(V2, encoding="utf-8", newline="\n")
    return root


def tree_hashes(root):
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            out[str(p.relative_to(root)).replace("\\", "/")] = sha(p)
    return out


def identity(root):
    for pc in root.rglob("__pycache__"):
        shutil.rmtree(pc, ignore_errors=True)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run([PY, "-B", "-c",
                        "import sys;sys.path.insert(0,str(sys.argv[1]));"
                        "from src.app import build;print(build().identity())", str(root)],
                       capture_output=True, text=True, env=env)
    return p.stdout.strip()


def issue(out, writeset_paths, preimages, nonce, operation="repo_patch", subject="WO-B1-C5"):
    ws = out.parent / f"ws_{out.name}.json"
    ws.write_text(json.dumps({"writeset": [{"path": str(p), "preimage": preimages[str(p)]} for p in writeset_paths]}),
                  encoding="utf-8")
    out.unlink(missing_ok=True)
    r = subprocess.run([PY, str(ISSUER), "issue", "--principal", "owner", "--operation", operation,
                        "--writeset", str(ws), "--ttl", "900", "--epoch", "40", "--scope", "C5 minpatch",
                        "--nonce", nonce, "--subject", subject, "--out", str(out)],
                       capture_output=True, text=True)
    return {"rc": r.returncode, "ws": str(ws)}


def swap(root, grant, out, ledger):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["HGK_CONSUMED_LEDGER"] = str(ledger)
    p = subprocess.run([PY, "-B", str(TOOL), "--root", str(root), "--entry", "src/app.py",
                        "--candidate", str(root / "candidate.py"), "--expect-old", "cap-attest-v1",
                        "--expect-new", "cap-attest-v2", "--need", "cap.attest", "--method", "identity",
                        "--grant", str(grant), "--grant-verifier", str(ISSUER), "--out", str(out)],
                       capture_output=True, text=True, env=env, timeout=180)
    rec = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    return {"rc": p.returncode, "ok": rec.get("ok"), "code": rec.get("code"),
            "problems": (rec.get("grant") or {}).get("problems"),
            "preimage": rec.get("preimage"), "candidate_sha256": rec.get("candidate_sha256"),
            "stderr_tail": p.stderr.strip()[-160:]}


def main():
    C5.mkdir(parents=True, exist_ok=True)
    ledger = C5 / "consumed_ledger.jsonl"
    ledger.unlink(missing_ok=True)
    stamp = int(time.time())
    results = {}

    # POS: allowlist = entry + candidate
    f1 = reset(C5 / "pos")
    before_tree = tree_hashes(f1)
    before_identity = identity(f1)
    pre = {str(f1 / "src" / "app.py"): sha(f1 / "src" / "app.py"), str(f1 / "candidate.py"): sha(f1 / "candidate.py")}
    iss = issue(C5 / "grant_pos.json", [f1 / "src" / "app.py", f1 / "candidate.py"], pre, f"C5-POS-{stamp}", subject="WO-B1-C5-POS")
    pos = swap(f1, C5 / "grant_pos.json", C5 / "swap_pos.json", ledger)
    after_identity = identity(f1)
    after_tree = tree_hashes(f1)
    changed = [k for k in after_tree if before_tree.get(k) != after_tree[k]]
    other_changed = [k for k in changed if k != "src/app.py"]
    landed_equals_candidate = sha(f1 / "src" / "app.py") == sha(f1 / "candidate.py")
    # narrow rollback: restore the preimage and confirm byte identity
    (f1 / "src" / "app.py").write_text(V1, encoding="utf-8", newline="\n")
    restored = sha(f1 / "src" / "app.py") == before_tree["src/app.py"]
    results["POS_allowlist_and_rollback"] = {
        "swap": pos, "identity_before": before_identity, "identity_after": after_identity,
        "files_changed": changed, "files_outside_allowlist_changed": other_changed,
        "landed_equals_candidate": landed_equals_candidate, "rollback_byte_identical": restored,
        "verdict": "PASS" if (pos["ok"] is True and other_changed == [] and landed_equals_candidate
                              and restored and before_identity != after_identity) else "FAIL"}

    results["POS_regression_independent"] = {
        "note": "identity read in a separate process before and after the swap",
        "before": before_identity, "after": after_identity,
        "verdict": "PASS" if before_identity.endswith("v1") and after_identity.endswith("v2") else "FAIL"}

    # NEG: allowlist escape -- grant covers a file that is not the entry
    f2 = reset(C5 / "neg_escape")
    pre2 = {str(f2 / "docs" / "README.md"): sha(f2 / "docs" / "README.md"),
            str(f2 / "candidate.py"): sha(f2 / "candidate.py")}
    issue(C5 / "grant_escape.json", [f2 / "docs" / "README.md", f2 / "candidate.py"], pre2, f"C5-ESC-{stamp}", subject="WO-B1-C5-ESC")
    esc = swap(f2, C5 / "grant_escape.json", C5 / "swap_escape.json", ledger)
    entry_untouched = sha(f2 / "src" / "app.py") == hashlib.sha256(V1.encode()).hexdigest()
    results["NEG_allowlist_escape"] = {
        "swap": esc, "entry_untouched": entry_untouched,
        "verdict": "PASS" if (esc["ok"] is False and entry_untouched
                              and any("WRITESET_EXCLUDES" in str(x) for x in (esc["problems"] or []))) else "FAIL"}

    # NEG: checker edits the landed diff
    f3 = reset(C5 / "neg_checker_edit")
    pre3 = {str(f3 / "src" / "app.py"): sha(f3 / "src" / "app.py"), str(f3 / "candidate.py"): sha(f3 / "candidate.py")}
    issue(C5 / "grant_edit.json", [f3 / "src" / "app.py", f3 / "candidate.py"], pre3, f"C5-EDT-{stamp}", subject="WO-B1-C5-EDT")
    edt = swap(f3, C5 / "grant_edit.json", C5 / "swap_edit.json", ledger)
    landed_sha = sha(f3 / "src" / "app.py")
    receipt_matches = landed_sha == edt.get("candidate_sha256")
    # the checker mutates the file it is supposed to be reading
    (f3 / "src" / "app.py").write_text(V1.replace('"cap-attest-v1"', '"cap-attest-v1-tampered"'),
                                       encoding="utf-8", newline="\n")
    tampered_sha = sha(f3 / "src" / "app.py")
    detected = tampered_sha != edt.get("candidate_sha256")
    results["NEG_checker_edits_diff"] = {
        "swap_ok": edt["ok"], "receipt_matches_disk_after_swap": receipt_matches,
        "detected_after_checker_mutation": detected,
        "verdict": "DETECTABLE_NOT_PREVENTED" if (edt["ok"] is True and receipt_matches and detected) else "FAIL",
        "honest_reading": "the tool does not stop a checker from editing the diff; the receipt's candidate_sha256 is what a "
                          "re-verify step must compare against"}

    summary = {k: v.get("verdict") for k, v in results.items()}
    doc = {"schema": "FHS.R21.S5.C5_CASES/1",
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "edge": "EDGE-WO-B1-C5", "pd": "PD-27", "domain": "CODEX_MINPATCH",
           "tool": {"path": str(TOOL.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(TOOL),
                    "note": "selector candidate; canonical PIPD/tools/hotswap.py untouched"},
           "canonical_sha256": sha(ROOT / "PIPD" / "tools" / "hotswap.py"),
           "results": results, "summary": summary,
           "claim_ceiling": ("author-side local measurement on copies. The allowlist boundary is enforced by the grant "
                             "writeset; a checker editing the diff afterwards is DETECTABLE via the receipt's "
                             "candidate_sha256 but is not prevented.")}
    out = S5 / "C5_CASES.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("pos", results["POS_allowlist_and_rollback"]["swap"]["ok"],
          results["POS_allowlist_and_rollback"]["files_outside_allowlist_changed"],
          "esc", results["NEG_allowlist_escape"]["swap"]["problems"],
          "edt", results["NEG_checker_edits_diff"]["verdict"])
    print("sha", sha(out)[:16])


if __name__ == "__main__":
    main()
