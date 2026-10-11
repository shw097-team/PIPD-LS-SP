#!/usr/bin/env python3
"""R5Q P0 read-only preflight.

Collect live machine truth for the Owner Open Source Preview round and emit one JSON.
READ-ONLY: performs no writes outside its own out-dir, no git mutation, no network auth.

Contract: PIPD-LS-SP_HERMES_R5P_OWNER_OPENSOURCE_PREVIEW_EXECUTION_PROMPT_2026-10-10.md section 6 P0.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PIPD = Path(r"C:\Projects\Agent_Workspace\PIPD")
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
FABRIC = Path(r"C:\Projects\Agent_Workspace\Fabric")
KB_DOCS = Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD")
COMPILER = Path(r"C:\Projects\Agent_Workspace\知識庫\工程基座"
                r"\construction-acceptance-prompt-compiler\construction-acceptance-prompt-compiler")
CRED = Path(r"C:\Projects\Agent_Workspace\API KEY\Fine-grained personal access tokens.txt")
OUT = PIPD / ".hgk" / "rounds" / "R5Q-20261010-s4-owner-opensource-preview" / "preflight"

BASELINE = {
    "branch": "r5p-post-challenge-repair",
    "commit": "2efc84eac8e1939092c748d5b389b6dd72267aef",
    "tree": "e254ea23243e0c767bf79fc647b82341493a231c",
    "wheel_sha256_at_review": "bb070a6f525382edc521bcf7fe127579e1e329024113ab4fe2881eeeea7b0a76",
    "main_at_review": "3aebbbce948871c07b875ab92acf263d298ecf38",
    "candidate_head_in_manifest": "7c5bc585c7d889cd338da853be4efc4b8f07d3b2",
}


def sha256(p: Path) -> str | None:
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def git(*args: str) -> dict:
    cp = subprocess.run(["git", "-C", str(PIPD), *args], capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    return {"argv": ["git", *args], "exit": cp.returncode,
            "stdout": cp.stdout.strip(), "stderr": cp.stderr.strip()}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    r: dict = {"round": "R5Q-20261010-s4-owner-opensource-preview", "collected_utc": now,
               "mode": "READ_ONLY_PREFLIGHT", "checks": {}, "blockers": [], "drift": []}

    # --- git truth -------------------------------------------------------
    head = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    status = git("status", "--porcelain")
    r["checks"]["git"] = {
        "head": head["stdout"], "tree": tree["stdout"], "branch": branch["stdout"],
        "dirty_entries": len([l for l in status["stdout"].splitlines() if l.strip()]),
        "head_matches_baseline": head["stdout"] == BASELINE["commit"],
        "tree_matches_baseline": tree["stdout"] == BASELINE["tree"],
        "branch_matches_baseline": branch["stdout"] == BASELINE["branch"],
    }

    # --- wheel truth -----------------------------------------------------
    wheel = PIPD / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl"
    wsha = sha256(wheel)
    r["checks"]["wheel"] = {
        "path": str(wheel), "exists": wheel.is_file(), "bytes": wheel.stat().st_size if wheel.is_file() else None,
        "sha256": wsha, "matches_review_sha": wsha == BASELINE["wheel_sha256_at_review"],
        "sha256_file": (PIPD / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl.sha256").read_text(
            encoding="utf-8").strip() if (PIPD / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl.sha256").is_file() else None,
    }

    # --- license state ---------------------------------------------------
    lic = PIPD / "LICENSE"
    owner_slot = PIPD / "OWNER_LICENSE_DECISION.yaml"
    r["checks"]["license"] = {
        "license_sha256": sha256(lic),
        "license_spdx_line": [l.strip() for l in lic.read_text(encoding="utf-8").splitlines()
                              if "SPDX" in l] if lic.is_file() else [],
        "owner_slot_sha256": sha256(owner_slot),
        "owner_slot_decision": [l.split(":", 1)[1].strip() for l in
                                owner_slot.read_text(encoding="utf-8").splitlines()
                                if l.startswith("decision:")] if owner_slot.is_file() else [],
        "notice_present": (PIPD / "NOTICE").is_file(),
        "grant_state": "NO_GRANT",
    }

    # --- compiler bundle -------------------------------------------------
    r["checks"]["compiler_bundle"] = {
        "root": str(COMPILER), "exists": COMPILER.is_dir(),
        "script": str(COMPILER / "scripts" / "prompt_contract_compiler.py"),
        "script_exists": (COMPILER / "scripts" / "prompt_contract_compiler.py").is_file(),
        "schema_exists": (COMPILER / "references" / "prompt-contract.schema.json").is_file(),
        "references": sorted(p.name for p in (COMPILER / "references").glob("*.md")),
    }

    # --- normative sources ----------------------------------------------
    prompt_doc = KB_DOCS / "PROMPT" / "PIPD-LS-SP_HERMES_R5P_OWNER_OPENSOURCE_PREVIEW_EXECUTION_PROMPT_2026-10-10.md"
    go_doc = KB_DOCS / "驗收報告" / "PIPD_LS_SP_R5P_S0-S4_External_Challenge_CORRECTED_OWNER_OpenSource_Preview_GO_2026-10-10.md"
    r["checks"]["normative_sources"] = {
        "execution_prompt": {"path": str(prompt_doc), "exists": prompt_doc.is_file(), "sha256": sha256(prompt_doc)},
        "corrected_owner_go": {"path": str(go_doc), "exists": go_doc.is_file(), "sha256": sha256(go_doc)},
    }

    # --- credential gate (existence + ACL only; VALUE NEVER READ/PRINTED) --
    acl = subprocess.run(["icacls", str(CRED)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    r["checks"]["credential_gate"] = {
        "path": str(CRED), "exists": CRED.is_file(),
        "bytes": CRED.stat().st_size if CRED.is_file() else None,
        "acl_exit": acl.returncode,
        "acl_lines": [l.strip() for l in acl.stdout.splitlines() if l.strip()][:12],
        "read_by": "process_memory_only_via_credential_broker",
    }

    # --- tool availability ----------------------------------------------
    def which(name: str) -> str | None:
        for ext in ("", ".exe", ".cmd", ".bat"):
            cand = PIPD_which(name + ext)
            if cand:
                return cand
        return None

    def PIPD_which(x: str) -> str | None:
        import shutil
        return shutil.which(x)

    r["checks"]["tools"] = {
        "gh": which("gh"),
        "git": which("git"),
        "curl": which("curl"),
        "python": sys.executable,
        "python_version": sys.version.split()[0],
        "jsonschema": _mod_ver("jsonschema"),
        "build_backend_offline": "tools/build_dist.py (PEP427 hand-build, network-off)",
        "github_api_fallback": "HTTPS REST via urllib with process-scoped token (gh CLI absent)",
    }

    # --- HGK control plane ----------------------------------------------
    r["checks"]["hgk"] = {
        "root": str(HGK),
        "pyproject": (HGK / "pyproject.toml").is_file(),
        "venv_python": (HGK / ".venv" / "Scripts" / "python.exe").is_file(),
        "spine_db": (HGK / "var" / "shared-spine" / "hg-kseos.db").is_file(),
        "doctor_command": ["PYTHONPATH=<hgk>/src", "<hgk>/.venv/Scripts/python.exe", "-B", "-m", "hg_kseos",
                           "--root", str(HGK), "doctor"],
    }
    r["checks"]["fabric"] = {"root": str(FABRIC), "exists": FABRIC.is_dir(),
                             "role": "governance/contract surface only, read-only consumption"}

    # --- remote readback (anonymous, no credential) -----------------------
    ls = subprocess.run(["git", "ls-remote", "--heads",
                         "https://github.com/shw097-team/PIPD-LS-SP"],
                        capture_output=True, text=True, timeout=120)
    refs = {}
    for line in ls.stdout.splitlines():
        if "\t" in line:
            sha, ref = line.split("\t", 1)
            refs[ref.replace("refs/heads/", "")] = sha
    r["checks"]["github_public"] = {
        "exit": ls.returncode, "refs": refs,
        "main_is_r3": refs.get("main") == BASELINE["main_at_review"],
        "r5p_branch_public_sha": refs.get("r5p-post-challenge-repair"),
        "r5p_branch_matches_local": refs.get("r5p-post-challenge-repair") == BASELINE["commit"],
    }

    # --- drift table ------------------------------------------------------
    if not r["checks"]["git"]["branch_matches_baseline"] or not r["checks"]["git"]["head_matches_baseline"]:
        r["drift"].append({"item": "branch/HEAD", "expected": BASELINE["commit"],
                           "observed": r["checks"]["git"]["head"]})
    if not r["checks"]["wheel"]["matches_review_sha"]:
        r["drift"].append({"item": "wheel sha256", "expected": BASELINE["wheel_sha256_at_review"],
                           "observed": wsha})

    # --- fail-closed blockers (P0) ---------------------------------------
    def block(cid: str, cond: bool, detail: str) -> None:
        if cond:
            r["blockers"].append({"id": cid, "detail": detail})

    block("BLK_COMPILER_BUNDLE", not r["checks"]["compiler_bundle"]["script_exists"],
          "native prompt compiler script missing")
    block("BLK_NORMATIVE_SOURCE", not (prompt_doc.is_file() and go_doc.is_file()),
          "execution prompt or corrected owner GO report missing from the knowledge base")
    block("BLK_CREDENTIAL", not CRED.is_file(), "owner PAT credential file not present")
    block("BLK_HGK", not r["checks"]["hgk"]["venv_python"], "HG-KSEOS venv python missing")
    block("BLK_LOCAL_REPO", not (PIPD / ".git").exists(), "local PIPD repo missing")

    r["verdict"] = "PREFLIGHT_PASS" if not r["blockers"] else "PREFLIGHT_BLOCKED"
    (OUT / "R5Q_PREFLIGHT.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"verdict": r["verdict"], "blockers": r["blockers"],
                      "drift": r["drift"],
                      "git": r["checks"]["git"],
                      "wheel_sha_matches": r["checks"]["wheel"]["matches_review_sha"],
                      "compiler_ok": r["checks"]["compiler_bundle"]["script_exists"],
                      "gh": r["checks"]["tools"]["gh"],
                      "remote_r5p": r["checks"]["github_public"]["r5p_branch_public_sha"]},
                     ensure_ascii=False, indent=1))
    return 0


def _mod_ver(name: str) -> str | None:
    try:
        import importlib.metadata as md
        return md.version(name)
    except Exception:
        return None


if __name__ == "__main__":
    raise SystemExit(main())
