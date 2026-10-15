"""R5S freeze probe: capture the live subject/refs/release/CI/lane state for this session.

Read-only. Writes only the JSON it is asked for.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("C:/Projects/Agent_Workspace/PIPD")
OUT = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/R5S-20261015-s4-preview4-verify-close/00_freeze/R5S_FREEZE.json")
API = "https://api.github.com/repos/shw097-team/PIPD-LS-SP"


def sh(args, cwd=REPO):
    p = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def api(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "hgk-round-probe"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


out = {
    "schema": "R5S-FREEZE/1",
    "round": "R5S-20261015-s4-preview4-verify-close",
    "captured_utc": datetime.now(timezone.utc).isoformat(),
    "purpose": "delta-only re-freeze: the R5R round already published preview.4; this session verifies the "
               "published state, repairs the lane transport fault, and runs the outstanding independent re-check.",
}

rc, head, _ = sh(["git", "rev-parse", "HEAD"])
rc2, main, _ = sh(["git", "rev-parse", "origin/main"])
_, tree, _ = sh(["git", "rev-parse", "origin/main^{tree}"])
_, tags, _ = sh(["git", "tag", "--list"])
_, refs, _ = sh(["git", "ls-remote", "origin", "refs/heads/r5r-evidence-return-20261014"])
out["subject"] = {
    "local_checkout_head": head,
    "origin_main_commit": main,
    "origin_main_tree": tree,
    "tags_present": [t for t in tags.splitlines() if t.strip()],
    "evidence_branch_remote": refs,
}

rel = api("/releases")
out["releases"] = [
    {
        "tag": r["tag_name"],
        "draft": r["draft"],
        "prerelease": r["prerelease"],
        "published_at": r["published_at"],
        "target_commitish": r["target_commitish"],
        "assets": [
            {"name": a["name"], "size": a["size"], "state": a["state"], "digest": a.get("digest")}
            for a in r["assets"]
        ],
    }
    for r in rel
]
prs = api("/pulls?state=all&per_page=20")
out["pull_requests"] = [
    {
        "number": p["number"],
        "state": p["state"],
        "merged": bool(p["merged_at"]),
        "head": p["head"]["ref"],
        "merge_commit": (p.get("merge_commit_sha") or "")[:8],
        "title": p["title"][:90],
    }
    for p in prs
]
out["open_pull_requests"] = [p["number"] for p in prs if p["state"] == "open"]
runs = api("/actions/runs?branch=main&per_page=5")
out["main_workflow_runs"] = [
    {"name": r["name"], "head_sha": r["head_sha"][:8], "conclusion": r["conclusion"], "run": r["id"], "url": r["html_url"]}
    for r in runs["workflow_runs"]
]

# lane transport evidence
_, ports, _ = sh(["bash", "-lc", "netstat -an | grep -E '1010[0-9]' || true"])
out["lane_transport"] = {"listeners_1010x": ports.splitlines()}
bins = sorted(Path("C:/Users/user/AppData/Local/OpenAI/Codex/bin").glob("*/codex.exe"))
out["codex_binaries_installed"] = [
    {"path": str(b).replace("\\", "/"), "sha256": sha256_file(b), "bytes": b.stat().st_size, "mtime_utc": datetime.fromtimestamp(b.stat().st_mtime, timezone.utc).isoformat()}
    for b in bins
]
cfg = json.loads((Path("C:/Projects/Agent_Workspace/HG-KSEOS/config/hermes-codex-lane.json")).read_text(encoding="utf-8-sig"))
pinned = cfg["codex_executable"].replace("\\", "/")
out["lane_pin"] = {
    "declared_codex_executable": pinned,
    "declared_codex_sha256": cfg.get("codex_sha256"),
    "declared_codex_version": cfg.get("codex_version"),
    "path_exists": Path(pinned).exists(),
    "declared_sha_matches_a_live_binary": any(b["sha256"].lower() == str(cfg.get("codex_sha256", "")).lower() for b in out["codex_binaries_installed"]),
}

# the local round artifacts of the previous session
prev = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/R5R-20261014-s4-preview4-focused-close")
out["previous_round"] = {
    "dir": str(prev).replace("\\", "/"),
    "files": sorted(str(p.relative_to(prev)).replace("\\", "/") for p in prev.rglob("*") if p.is_file())[:200],
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k: out[k] for k in ("subject", "open_pull_requests", "lane_pin", "lane_transport", "codex_binaries_installed")}, indent=1, ensure_ascii=False))
print("WROTE", OUT, OUT.stat().st_size, "bytes")
