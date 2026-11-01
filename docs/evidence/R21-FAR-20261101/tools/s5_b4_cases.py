"""S5 / EDGE-WO-B1-B4-DEV (ECP_SELECTOR): one active ECP per WO, and unknown classes.

Body (10B#L181-184):
  POS  Ambiguous/multiple ECP gets NACK before dispatch; judge: one active ECP per WO; split iff distinct effects
  NEG  two active ECPs / unknown class -> ECP_MULTIPLE_OR_CLASS_UNKNOWN

Three tools are compared on the same cases so the gap is visible rather than asserted:
  canonical  PIPD/tools/hotswap.py
  candidate  s5/patch/PIPD/tools/hotswap_b3.py   (effect class + single-use receipt)
  selector   a further candidate that also refuses a second live ECP for the same subject
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
S5 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "s5"
B4 = S5 / "b4"
PATCHDIR = S5 / "patch" / "PIPD"
CAND = PATCHDIR / "tools" / "hotswap_b3.py"
CANON = ROOT / "PIPD" / "tools" / "hotswap.py"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
PY = sys.executable

V1 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v1"\ndef build():\n    return Impl()\n'
V2 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\ndef build():\n    return Impl()\n'

SELECTOR_BLOCK = '''    # 3e. one live ECP per subject: a second grant for a subject that already has a consumed receipt
    # must be refused until the first one is closed (AO/edge B4: two active ECPs, no selector).
    subj = (grant.get("subject") or "").strip()
    info["subject"] = subj
    if subj and ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            try:
                prior = json.loads(line)
            except json.JSONDecodeError:
                continue
            if prior.get("subject") == subj and not prior.get("closed"):
                problems.append("ECP_MULTIPLE_ACTIVE")
                info["competing_ecp"] = prior
                break

'''


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def build_selector():
    text = CAND.read_text(encoding="utf-8")
    anchor = "    # 4. the grant must name the exact artefact when it names one at all"
    if anchor not in text:
        raise SystemExit("anchor missing; refusing to guess")
    patched = text.replace(anchor, SELECTOR_BLOCK + anchor, 1)
    row_old = '    row = {"nonce": grant.get("nonce"), "entry": _norm(entry), "candidate": _norm(candidate),'
    row_new = ('    row = {"nonce": grant.get("nonce"), "subject": (grant.get("subject") or ""),\n'
               '           "entry": _norm(entry), "candidate": _norm(candidate),')
    if row_old not in patched:
        raise SystemExit("ledger row not found; the selector needs the subject recorded")
    patched = patched.replace(row_old, row_new, 1)
    dst = PATCHDIR / "tools" / "hotswap_selector.py"
    dst.write_text(patched, encoding="utf-8", newline="\n")
    diff = difflib.unified_diff(CANON.read_text(encoding="utf-8").splitlines(True),
                                dst.read_text(encoding="utf-8").splitlines(True),
                                fromfile="a/PIPD/tools/hotswap.py",
                                tofile="b/PIPD/tools/hotswap.py (selector candidate)", n=3)
    (S5 / "patch" / "hotswap.selector.patch").write_text("".join(diff), encoding="utf-8", newline="\n")
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


def issue(out, root, nonce, operation="install_occupant", subject="WO-B1-B4"):
    ws = out.parent / f"ws_{out.stem}.json"
    ws.write_text(json.dumps({"writeset": [
        {"path": str(root / "occupant.py"), "preimage": sha(root / "occupant.py")},
        {"path": str(root / "candidate.py"), "preimage": sha(root / "candidate.py")}]}), encoding="utf-8")
    out.unlink(missing_ok=True)
    subprocess.run([PY, str(ISSUER), "issue", "--principal", "owner", "--operation", operation,
                    "--writeset", str(ws), "--ttl", "900", "--epoch", "40",
                    "--scope", f"B4 {operation}", "--nonce", nonce, "--subject", subject,
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
            "problems": (rec.get("grant") or {}).get("problems"), "identity_after": identity(root)}


def run_tool(tool, tag, stamp):
    """Two grants for the same subject, plus an unknown-class grant."""
    ledger = B4 / f"ledger_{tag}.jsonl"
    ledger.unlink(missing_ok=True)
    f = reset(B4 / f"fixture_{tag}")
    g1, g2 = B4 / f"grant_{tag}_1.json", B4 / f"grant_{tag}_2.json"
    issue(g1, f, f"B4-{tag}-A-{stamp}", subject="WO-B1-B4")
    issue(g2, f, f"B4-{tag}-B-{stamp}", subject="WO-B1-B4")
    first = swap(tool, f, g1, B4 / f"swap_{tag}_1.json", ledger)
    (f / "occupant.py").write_text(V1, encoding="utf-8", newline="\n")
    second = swap(tool, f, g2, B4 / f"swap_{tag}_2.json", ledger)

    fu = reset(B4 / f"fixture_{tag}_unknown")
    gu = B4 / f"grant_{tag}_unknown.json"
    issue(gu, fu, f"B4-{tag}-U-{stamp}", operation="frobnicate_class", subject="WO-B1-B4-U")
    unknown = swap(tool, fu, gu, B4 / f"swap_{tag}_unknown.json", ledger)
    return {"first": first, "second_same_subject": second, "unknown_class": unknown}


def main():
    B4.mkdir(parents=True, exist_ok=True)
    sel = build_selector()
    stamp = int(time.time())
    results = {
        "canonical": run_tool(CANON, "canon", stamp),
        "candidate_b3": run_tool(CAND, "cand", stamp),
        "candidate_selector": run_tool(sel, "sel", stamp),
    }

    def verdict(second, unknown):
        return {
            "POS_one_active_ecp": ("PASS" if second["ok"] is False else "FAIL_SECOND_ECP_ACCEPTED"),
            "NEG_unknown_class": ("PASS" if unknown["ok"] is False else "FAIL_UNKNOWN_CLASS_ACCEPTED"),
        }

    summary = {k: verdict(v["second_same_subject"], v["unknown_class"]) for k, v in results.items()}
    doc = {"schema": "FHS.R21.S5.B4_CASES/1",
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "edge": "EDGE-WO-B1-B4-DEV", "pd": "PD-14", "domain": "ECP_SELECTOR",
           "tools": {"canonical_sha256": sha(CANON), "candidate_b3_sha256": sha(CAND),
                     "candidate_selector_sha256": sha(sel),
                     "selector_patch": "s5/patch/hotswap.selector.patch",
                     "selector_patch_sha256": sha(S5 / "patch/hotswap.selector.patch")},
           "results": results, "summary": summary,
           "claim_ceiling": ("unknown-class handling is enforceable by the candidate; one-live-ECP-per-subject "
                             "needs the selector candidate. Nothing here is accepted: all three tools are copies "
                             "and the canonical file is unmodified.")}
    (S5 / "B4_CASES.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                     encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for k, v in results.items():
        print(k, "| first", v["first"]["ok"], v["first"]["problems"],
              "| second", v["second_same_subject"]["ok"], v["second_same_subject"]["problems"],
              "| unknown", v["unknown_class"]["ok"], v["unknown_class"]["problems"])


if __name__ == "__main__":
    main()
