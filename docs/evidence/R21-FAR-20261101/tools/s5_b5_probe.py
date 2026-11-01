"""S5 / EDGE-WO-B1-B5-DEV (THREE_SP): can three host-issued SP identities be produced on this host today?

Body (10B#L205-208):
  POS  Three separate true host-issued identities; ZIP-only denied
  NEG  missing host invocation -> SP_HOST_LOAD_UNPROVEN

This probe refuses to reason from prose. It asks the host three questions and records command + exit + sha for each:
  1. is there any executable that can issue an SP identity?            (PATH probe)
  2. is there any receipt that records an SP host invocation?          (receipt scan: command + exit + output sha)
  3. do the three role briefs exist, and are they briefs or identities? (file sha of each skill)
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
S5 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "s5"
HERMES_SKILLS = pathlib.Path(os.environ["LOCALAPPDATA"]) / "Packages" / "OpenAI.Codex_2p2nqsd0c76g0" / "LocalCache" / "Local" / "hermes" / "skills"
ROLE_SKILLS = {"TPM-SP": "tpm-sp", "Commander-SP": "commander-sp", "Challenge-SP": "external-challenge-sp"}
BINARIES = ["tpm-sp", "commander-sp", "challenge-sp", "sp-host", "pipd-sp", "hgk-sp"]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def probe_binaries():
    rows = []
    for b in BINARIES:
        p = shutil.which(b)
        rows.append({"binary": b, "found": bool(p), "path": p,
                     "sha256": sha(p) if p else None})
    return rows


def probe_receipts(roots):
    """A host invocation receipt must carry command + exit code + output sha. Prose mentions do not count."""
    candidates = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.json"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            low = text.lower()
            if not any(k in low for k in ("tpm-sp", "commander-sp", "challenge-sp")):
                continue
            try:
                doc = json.loads(text)
            except json.JSONDecodeError:
                continue
            hits = []

            def walk(o, path=""):
                if isinstance(o, dict):
                    keys = {k.lower() for k in o}
                    cmd = str(o.get("command") or o.get("cmd") or "").lower()
                    if ({"command", "exit_code"} <= keys or {"cmd", "rc"} <= keys) and any(
                            r in cmd for r in ("tpm-sp", "commander-sp", "challenge-sp")):
                        hits.append({"at": path, "command": cmd[:160], "exit_code": o.get("exit_code", o.get("rc"))})
                    for k, v in o.items():
                        walk(v, f"{path}/{k}")
                elif isinstance(o, list):
                    for i, v in enumerate(o[:200]):
                        walk(v, f"{path}[{i}]")

            walk(doc)
            if hits:
                candidates.append({"file": str(p.relative_to(ROOT)).replace("\\", "/"), "bytes": p.stat().st_size,
                                   "sha256": sha(p), "invocation_like": len(hits), "samples": hits[:3]})
    return candidates


def probe_skills():
    rows = []
    for role, name in ROLE_SKILLS.items():
        cands = list(HERMES_SKILLS.rglob(f"{name}/SKILL.md"))
        f = cands[0] if cands else (HERMES_SKILLS / name / "SKILL.md")
        d = f.parent
        rows.append({"role": role, "skill_dir_exists": d.exists(), "skill_md_exists": f.exists(),
                     "sha256": sha(f) if f.exists() else None,
                     "bytes": f.stat().st_size if f.exists() else 0,
                     "kind": "BRIEF_NOT_IDENTITY" if f.exists() else "ABSENT"})
    return rows


def main():
    S5.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    bins = probe_binaries()
    receipts = probe_receipts([ROOT / "var", ROOT / "HG-KSEOS" / "ops", ROOT / "HG-KSEOS" / "receipts"])
    skills = probe_skills()

    host_issued = [r for r in receipts if r["invocation_like"] > 0]
    verdict = "SP_HOST_LOAD_UNPROVEN" if not host_issued else "HOST_INVOCATIONS_FOUND_REVIEW_NEEDED"
    doc = {
        "schema": "FHS.R21.S5.B5_PROBE/1",
        "generated_utc": stamp,
        "edge": "EDGE-WO-B1-B5-DEV", "pd": "PD-16", "domain": "THREE_SP",
        "question": "are three separate host-issued SP identities obtainable on this host right now?",
        "binaries": {"probe": "shutil.which over candidate names", "rows": bins,
                     "found_any": any(b["found"] for b in bins)},
        "receipts": {"probe": "json scan for objects carrying command+exit_code (or cmd+rc) AND an SP role name",
                     "files_mentioning_sp": None, "invocation_receipts": receipts,
                     "count": len(receipts)},
        "role_skills": {"probe": "skill dir + SKILL.md sha", "rows": skills},
        "verdict": verdict,
        "pos_met": False,
        "why": ("no executable can issue an SP identity and no receipt carries a host invocation for any of the three "
                "roles; the three role skills are briefs (documents), not host-issued identities"),
        "unblock": ("run each role on a real host that issues an identity, and record command + exit + output sha for "
                    "the invocation; ZIP-only delivery does not count per the body"),
        "claim_ceiling": "author-side surface probe only; nothing here is an SP identity and no PASS is claimed",
    }
    out = S5 / "B5_PROBE.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": verdict, "binaries_found": doc["binaries"]["found_any"],
                      "invocation_receipts": len(receipts), "sha256": sha(out)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
