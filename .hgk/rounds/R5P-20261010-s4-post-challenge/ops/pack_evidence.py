#!/usr/bin/env python3
"""Build the R5P evidence_return_pack.

Binds the round's frozen subject (baseline / code / packaging / repair commits, wheel sha, bound
product digest), the change set versus the baseline, and a sha256 index of every raw artefact in the
round directory.

The raw index walks with os.walk and ignores OSError: the round directory legitimately contains
Linux-created venv symlinks (lib64) that cannot be read from Windows - independent challenge C-check
"F-R5P-01" is about exactly that failure mode in the product, so the packer must not repeat it. Huge
checker scratch (venvs, wheel build trees) is indexed only through the logs it produced.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROUND = Path(__file__).resolve().parents[1]
PIPD = ROUND.parents[2]
BASELINE = "0f06eec96386b7349db8b41ac6cf9c7455d326f1"
REPAIR_TIP = "f06b0e7b5f287e1b83cc737061da4bfad94acdf8"
EXPORT = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/"
              "hermes/cache/scratch/r5p-pushed-tree")
SKIP_PARTS = {".git", "__pycache__", "node_modules", "site-packages", "wheels"}
SKIP_PREFIX = ("venv_", "build_", "pip-")
KEEP_SUFFIX = {".json", ".jsonl", ".txt", ".md", ".log", ".sh"}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sh(*args: str) -> str:
    return subprocess.run(["git", "-C", str(PIPD).replace("\\", "/"), *args],
                          capture_output=True, text=True).stdout.strip()


def raw_index(root: Path) -> dict:
    out: dict[str, str] = {}
    for base, dirs, files in os.walk(root, onerror=lambda e: None):
        parts = Path(base).parts
        if any(p in SKIP_PARTS or p.startswith(SKIP_PREFIX) for p in parts):
            dirs[:] = []
            continue
        dirs[:] = sorted(d for d in dirs
                         if d not in SKIP_PARTS and not d.startswith(SKIP_PREFIX))
        for name in sorted(files):
            p = Path(base) / name
            if p.suffix not in KEEP_SUFFIX or "EVIDENCE_RETURN_PACK" in name:
                continue
            try:
                out[str(p.relative_to(root)).replace("\\", "/")] = sha256_file(p)
            except OSError:
                continue
    return out


def main() -> int:
    changed = [l for l in sh("diff", "--name-only", f"{BASELINE}..{REPAIR_TIP}").splitlines() if l.strip()]
    sys.path.insert(0, str(ROUND / "ops"))
    import bound_digest  # noqa: E402  (round-local, one definition of the product digest)

    root = EXPORT if EXPORT.is_dir() else PIPD
    bound = bound_digest.digest(root)
    pack = {
        "schema": "PIPD-R5P-EVIDENCE-RETURN-PACK/1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "subject": {
            "repo": "shw097-team/PIPD-LS-SP",
            "baseline_branch": "r5-s4-packreader",
            "baseline_commit": BASELINE,
            "baseline_tree": "1f7564282fd708fab2ddeadbbbe4e424a3c564be",
            "candidate_branch": sh("rev-parse", "--abbrev-ref", "HEAD"),
            "candidate_code_commit": "b3d08b7d651a548ae74dc45453224fe393c41269",
            "candidate_packaging_commit": "0f64d1f8f84ca3f5815254353abcc039589d457d",
            "candidate_commit": REPAIR_TIP,
            "candidate_tree": sh("rev-parse", f"{REPAIR_TIP}^{{tree}}"),
            "bound_product_digest": bound["digest"],
            "bound_product_digest_definition": bound_digest.BOUND_DEFINITION,
            "bound_product_digest_root": str(root).replace("\\", "/"),
            "bound_product_file_count": bound["file_count"],
            "wheel_sha256": sha256_file(root / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl"),
            "changed_paths": changed,
        },
        "claim_ceiling": "CANDIDATE_ONLY",
        "scope": "S0-S4_S4_NORMAL_USER_OPERABILITY",
        "independent_acceptance": "SEE ao/out/AO_VERDICT.json AND ao/out2/AO_VERDICT_V2.json",
        "release": "NOT_GRANTED",
        "human_ratification": "PENDING",
        "raw_artifacts": raw_index(ROUND),
    }
    out = ROUND / "evidence" / "EVIDENCE_RETURN_PACK.json"
    out.write_text(json.dumps(pack, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(out), "changed_paths": len(changed),
                      "bound_product_digest": bound["digest"],
                      "raw_count": len(pack["raw_artifacts"])}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
