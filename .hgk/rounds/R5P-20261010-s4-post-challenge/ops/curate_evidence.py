"""Curate the R5P round into (a) a sanitized external bundle for the KB and (b) a sanitized in-repo subset.

The round directory is 235 MB and contains live Codex homes (lane/writer-home, lane/checker-home) with
auth material and cached binaries, plus 9,674 container artefacts under ao/out. None of that may leave
the machine. What an external acceptance officer actually needs is small and enumerable.

Outputs
  1. KB bundle:   <knowledge evidence root>/R5P/  + R5P_EXTERNAL_EVIDENCE_INDEX.json (sha256 per file)
  2. repo subset: <round>/repo_subset/  (paths mirrored under .hgk/rounds/R5P-.../<rel>)
Nothing is committed or pushed here.

Usage: python ops/curate_evidence.py
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import shutil

ROUND = pathlib.Path(__file__).resolve().parents[1]
KB = pathlib.Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\實作證據\R5P")
SUBSET = ROUND / "repo_subset"

# Included: evidence an officer can read and re-run. Excluded by construction: lane/*-home, ao/out/**,
# uat/out, uat/out3, venvs, caches, anything binary and large.
INCLUDE_GLOBS = [
    "CHECKPOINT_R5P.json",
    "evidence/*.json", "evidence/*.md", "evidence/*.txt",
    "ops/*.py",
    "uat/uat_matrix.py", "uat/uat_run_console.txt", "uat/uat_run_console2.txt",
    "uat/out2/UAT_MATRIX.json", "uat/out2/RAW_RUNS.jsonl",
    "ao/out/AO_VERDICT.json", "ao/out/AO_VERDICT_V2.json", "ao/out/AO_VERDICT_V3.json", "ao/out/AO_VERDICT_V4.json",
    "compiler/R5P.CONTRACT.json", "compiler/R5P.lint.raw.txt", "compiler/R5P.activation.raw.txt",
    "compiler/R5P.acceptance.raw.txt", "compiler/R5P.compile.raw.txt", "compiler/R5P.duplication.raw.txt",
    "admission/r5p_admission.json",
    "gstack/route_readback.json",
    "lane/brief_*.md", "lane/run_*.sh", "lane/symlink_negative.sh", "lane/bridge2.py",
    "lane/log_ao_v2.txt", "lane/log_ao_v3.txt", "lane/log_ao_v4.txt",
]
SECRET_PATTERNS = [
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"), re.compile(rb"ghp_[A-Za-z0-9]{30,}"),
    re.compile(rb"BEGIN (RSA|OPENSSH|EC) PRIVATE KEY"), re.compile(rb"sk-[A-Za-z0-9]{24,}"),
    re.compile(rb"[\"']?(access_token|refresh_token|id_token|client_secret|password)[\"']?\s*[:=]\s*[\"'][^\"']{12,}"),
]
MAX_KB = 12000


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def collect() -> list[pathlib.Path]:
    seen: dict[str, pathlib.Path] = {}
    for pattern in INCLUDE_GLOBS:
        for p in sorted(ROUND.glob(pattern)):
            if p.is_file():
                seen[str(p.relative_to(ROUND))] = p
    return [seen[k] for k in sorted(seen)]


def main() -> int:
    files = collect()
    # secret scan before anything is copied
    hits = []
    for p in files:
        blob = p.read_bytes()
        for rx in SECRET_PATTERNS:
            if rx.search(blob):
                hits.append((str(p.relative_to(ROUND)), rx.pattern.decode("utf-8", "replace")))
                break
    if hits:
        print(json.dumps({"aborted": "secret pattern found", "hits": hits}, ensure_ascii=False, indent=1))
        return 1

    for target in (KB, SUBSET):
        if target.exists():
            shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
    index_rows = []
    total = 0
    for p in files:
        rel = p.relative_to(ROUND)
        for target in (KB, SUBSET):
            dst = target / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)
        size = p.stat().st_size
        total += size
        index_rows.append({"path": rel.as_posix(), "bytes": size, "sha256": sha256(p)})

    index = {
        "schema": "PIPD-R5P-EXTERNAL-EVIDENCE-INDEX/1",
        "round": "R5P-20261010-s4-post-challenge",
        "subject": {"branch": "r5p-post-challenge-repair",
                    "pushed_tip": "f06b0e7b5f287e1b83cc737061da4bfad94acdf8",
                    "pushed_tree": "e1c98195ae50d58ec07ffd67fde585b860e119fd",
                    "sidecar_attested_subject": "194f1774e8e852f954d141c48389a74b0f0e302a"},
        "claim_ceiling": "CANDIDATE_ONLY", "human_ratification": "PENDING", "release": "NOT_GRANTED",
        "file_count": len(index_rows), "total_bytes": total,
        "excluded_on_purpose": [
            "lane/writer-home and lane/checker-home (live Codex homes: auth.json, plugin caches, binaries)",
            "ao/out/** except the four AO verdict JSONs (9,674 container artefacts, 162 MB: venvs, raw runs)",
            "uat/out and uat/out3 (superseded runs; out3 is round-scratch contaminated)",
            "the 225 KB wheel itself (it is in the pushed branch at dist/)",
        ],
        "how_to_reproduce": {
            "clone": "git clone --branch r5p-post-challenge-repair --single-branch https://github.com/shw097-team/PIPD-LS-SP.git",
            "suite": "PYTHONPATH=src python -B -m unittest discover -s tests -t .   # clean clone: Ran 311, OK (skipped=6)",
            "doctor_truth": "python -B -m pipd_ls_sp.cli --root <dir> doctor",
            "uat_matrix": "PYTHONPATH=<clone>/src python -B uat/uat_matrix.py --out <outdir> --mode both --wheel <clone>/dist/pipd_ls_sp-0.1.0-py3-none-any.whl",
            "attestation": "python tools/publication_attestation.py --verify --out .hgk/ao/pub/PUBLICATION_SUBJECT_ATTESTATION_R5P_POSTCHALLENGE.json --expect-commit 194f1774e8e852f954d141c48389a74b0f0e302a --expect-tree b1ec0abf4799fdc917aaa23dc75885b302407ee5",
        },
        "files": index_rows,
    }
    (KB / "R5P_EXTERNAL_EVIDENCE_INDEX.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    (SUBSET / "R5P_EXTERNAL_EVIDENCE_INDEX.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"files": len(index_rows), "bytes": total, "kb_dir": str(KB), "repo_subset": str(SUBSET),
                      "secret_scan": "clean"}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
