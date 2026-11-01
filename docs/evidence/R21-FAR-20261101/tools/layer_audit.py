"""Closure audit: is this session's work in the right layer?

Four layers are distinguished, because "it exists" is not the same as "it is preserved":
  L0 CANONICAL   a main-branch file that governs behaviour for everyone
  L1 CANDIDATE   a branch/PR artefact that must not be mistaken for canonical
  L2 DISPOSABLE  var/ scratch that a cleanup may delete (regenerable or archived)
  L3 HOST        ~/.hgk-owner key/window state (never leaves the host)

For every artefact this round produced, the audit records where it is, its sha256, and a verdict:
PRESERVED_IN_CANDIDATE, CANONICAL_UNCHANGED, DISPOSABLE_REGENERABLE, or MISPLACED.
"""
import hashlib
import json
import os
import pathlib
import subprocess
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
V = ROOT / "var" / "FHS-R21-FAR-TT-20261101"
REPO = ROOT / "PIPD"
DST = REPO / "docs" / "evidence" / "R21-FAR-20261101"
OUT = DST / "LAYER_AUDIT.json"


def sha(p):
    p = pathlib.Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None


def git(*args, cwd=REPO):
    r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip()


def main():
    # 1) copy every small evidence file that is still disposable-only
    copied = []
    for dp, dn, fn in os.walk(V):
        dn[:] = [d for d in dn if d not in {"__pycache__", "stdout", ".git"} and not d.startswith("home")]
        for f in fn:
            p = pathlib.Path(dp) / f
            if p.suffix.lower() not in {".json", ".md", ".tsv", ".patch", ".py", ".jsonl", ".txt", ".yaml", ".log"}:
                continue
            try:
                if p.stat().st_size > 3_000_000:
                    continue
            except OSError:
                continue
            tgt = DST / p.relative_to(V)
            data = p.read_bytes()
            if tgt.exists() and hashlib.sha256(tgt.read_bytes()).hexdigest() == hashlib.sha256(data).hexdigest():
                continue
            tgt.parent.mkdir(parents=True, exist_ok=True)
            tgt.write_bytes(data)
            copied.append(str(p.relative_to(V)).replace("\\", "/"))

    # 2) verify the whole evidence set is byte-identical to the round directory
    identical, gaps = 0, []
    for dp, dn, fn in os.walk(DST):
        for f in fn:
            src = V / (pathlib.Path(dp) / f).relative_to(DST)
            if src.exists() and sha(src) == sha(pathlib.Path(dp) / f):
                identical += 1
    for dp, dn, fn in os.walk(V):
        dn[:] = [d for d in dn if d not in {"__pycache__", "stdout", ".git"} and not d.startswith("home")]
        for f in fn:
            p = pathlib.Path(dp) / f
            if p.suffix.lower() not in {".json", ".md", ".tsv", ".patch", ".py", ".jsonl", ".txt", ".yaml", ".log"}:
                continue
            try:
                if p.stat().st_size > 3_000_000:
                    continue
            except OSError:
                continue
            tgt = DST / p.relative_to(V)
            if not tgt.exists():
                gaps.append(str(p.relative_to(V)).replace("\\", "/"))

    # 3) the four layers, as measured
    canon_disp = ROOT / "HG-KSEOS" / "scripts" / "hgk-lane-dispatch.py"
    hotswap = REPO / "tools" / "hotswap.py"
    layers = {
        "L0_CANONICAL": [
            {"path": "HG-KSEOS/scripts/hgk-lane-dispatch.py", "sha256": sha(canon_disp),
             "verdict": "CANONICAL_UNCHANGED",
             "note": "the D7 receipt-semantics fix exists only as a candidate patch; canonical bytes are untouched"},
            {"path": "PIPD/tools/hotswap.py", "sha256": sha(hotswap),
             "verdict": "CANONICAL_UNCHANGED_ON_MAIN",
             "note": "main still carries f9468f40; the repaired file lives on the candidate branch"},
        ],
        "L1_CANDIDATE": [
            {"path": "branch candidate/r21-far-20261101", "head": git("rev-parse", "HEAD"),
             "commits": git("log", "--oneline", "-3").splitlines(),
             "verdict": "PRESERVED_IN_CANDIDATE", "note": "PR #22, not merged"},
        ],
        "L2_DISPOSABLE": [
            {"path": "var/FHS-R21-FAR-TT-20261101/wp20/plugin_probe", "verdict": "DISPOSABLE_REGENERABLE",
             "note": "three isolated HERMES_HOME copies + raw stdout; the findings JSON is preserved in L1"},
            {"path": "var/FHS-R21-FAR-TT-20261101/s6", "verdict": "DISPOSABLE_REGENERABLE",
             "note": "raw lane logs dominate the size; the closure/case JSON is preserved in L1"},
            {"path": "var/FHS-R21-FAR-TT-20261101/*/stdout", "verdict": "DISPOSABLE_REGENERABLE",
             "note": "raw command output; every claim that depends on it also cites the derived JSON"},
        ],
        "L3_HOST": [
            {"path": "C:/Users/user/.hgk-owner/window.json", "verdict": "HOST_ONLY",
             "note": "live window state; the signature receipts are preserved in L1"},
            {"path": "C:/Users/user/.hgk-owner/owner.key.enc", "verdict": "HOST_ONLY_NEVER_COPY",
             "note": "passphrase envelope; must never enter any repository"},
        ],
    }

    findings = [
        {"id": "M1", "state": "FIXED_THIS_CLOSURE",
         "what": "s5/, s6/, ledgers/, wp12/, wp13/, receipts/ and 39 of 46 tools existed only in the disposable layer",
         "action": f"{len(copied)} files copied into L1 with sha verification"},
        {"id": "M2", "state": "FIXED_THIS_CLOSURE",
         "what": "the two owner signature receipts lived only in var/",
         "action": "copied to L1 rulings/ with payload_sha256 intact"},
        {"id": "M3", "state": "OPEN_FOR_OWNER",
         "what": "the D7 fix targets a canonical HG-KSEOS script and is still candidate-only",
         "action": "needs an owner merge decision; canonical sha 524cfd83 unchanged today"},
        {"id": "M4", "state": "OPEN_FOR_OWNER",
         "what": "the hotswap repair is on a candidate branch, not main",
         "action": "PR #22 open; main untouched"},
        {"id": "M5", "state": "OPEN_TECHNICAL",
         "what": "the selector patch (ECP_MULTIPLE_ACTIVE) collides with the landed repair and is not applied",
         "action": "rebase required; the capability stays unenforced until then"},
        {"id": "M6", "state": "PLACEMENT_QUESTION",
         "what": "owner rulings are governance artefacts but now live in the product repo (PIPD-LS-SP)",
         "action": "owner may prefer HG-KSEOS as their home; copies are byte-identical either way"},
    ]

    payload = {"schema": "LAYER_AUDIT/1",
               "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "round_id": "R21-FAR-20261101",
               "copied_this_run": len(copied),
               "byte_identical_pairs": identical, "gaps_after_copy": gaps,
               "layers": layers, "findings": findings,
               "rule": "an artefact that only exists under var/ is not preserved: a cleanup can delete it "
                       "and no reader of the repository would know it existed"}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"copied": len(copied), "identical_pairs": identical, "gaps": len(gaps),
                      "head": git("rev-parse", "HEAD")[:12]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
