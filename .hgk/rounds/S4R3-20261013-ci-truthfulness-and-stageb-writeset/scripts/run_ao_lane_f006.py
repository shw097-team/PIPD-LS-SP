#!/usr/bin/env python3
"""Drive the sealed VERIFY_SECURITY lane against the S4R3-F006 candidate.

Why a driver rather than a shell one-liner: the prompt is multi-line, contains quotes and Windows
paths, and the previous round lost time to MSYS quoting. Passing argv as a list removes that class of
error entirely, and every argument that identifies the subject (lane, cwd, forced rank, required arm)
is recorded in the receipt so the run can be re-issued exactly.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path("C:/Projects/Agent_Workspace")
HGK = REPO / "HG-KSEOS"
SCRATCH = pathlib.Path(
    "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
    "/cache/scratch/pipd-s4r3-exec"
)

RUNS = [
    {
        "lane": "VERIFY_SECURITY",
        "cwd": str(REPO / "PIPD/worktrees/s4r3a-wt"),
        "prompt_file": SCRATCH / "verify_prompt_s4r3x_f006.md",
        "out": SCRATCH / "ao_lane_f006" / "stdout.txt",
        "rank": "3",
        "arm": "opencode-go/glm-5.3-flash",
        "round": "S4R3X-20261013-f006-and-stageb-successor",
        "attempt": "3",
        "timeout": "1500",
    },
]


def main() -> int:
    args = sys.argv[1:]
    only = args[0] if args else None
    for run in RUNS:
        if only and only != run["lane"]:
            continue
        run["out"].parent.mkdir(parents=True, exist_ok=True)
        prompt = run["prompt_file"].read_text(encoding="utf-8")
        argv = [
            sys.executable,
            str(HGK / "scripts/hgk-lane-dispatch.py"),
            "--lane", run["lane"],
            "--prompt", prompt,
            "--cwd", run["cwd"],
            "--force-rank", run["rank"],
            "--require-arm", run["arm"],
            "--round", run["round"],
            "--attempt", run["attempt"],
            "--timeout", run["timeout"],
            "--attempt-log-dir", str(run["out"].parent / "attempts"),
        ]
        receipt = RUNS_RECEIPT(run, argv)
        (run["out"].parent / "invocation.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"=== {run['lane']} -> {run['out']} ===")
        print(" ".join(argv[:6]), "...")
        proc = subprocess.run(argv, cwd=str(HGK), capture_output=True, text=False)
        run["out"].write_bytes(proc.stdout)
        (run["out"].parent / "stderr.txt").write_bytes(proc.stderr)
        print(f"exit={proc.returncode} stdout_bytes={len(proc.stdout)}")
        print("--- tail ---")
        print(proc.stdout.decode("utf-8", "replace")[-3000:])
    return 0


def RUNS_RECEIPT(run: dict, argv: list[str]) -> dict:
    return {
        "lane": run["lane"],
        "cwd": run["cwd"],
        "force_rank": run["rank"],
        "require_arm": run["arm"],
        "round": run["round"],
        "attempt": run["attempt"],
        "timeout_s": run["timeout"],
        "prompt_file": str(run["prompt_file"]),
        "prompt_sha256": __import__("hashlib").sha256(
            run["prompt_file"].read_bytes()
        ).hexdigest(),
        "argv_head": argv[:2] + argv[2:6],
    }


if __name__ == "__main__":
    raise SystemExit(main())
