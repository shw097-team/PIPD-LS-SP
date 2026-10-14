#!/usr/bin/env python3
"""Run the write-set gate step LOCALLY, exactly as the workflow would.

This is the discipline the F006 gate failure taught: a gate that only ever runs in CI cannot be
falsified by the person changing it. The script pulls the step's `run` and `env` out of the workflow
file, writes the run text to a temporary LF-only .sh, and executes it with GIT bash inside the
worktree under review.

Two host facts this encodes, both learned the hard way:
  * a bare `bash` on this host resolves to WSL bash, which cannot read C:/ paths and which mangles
    arguments containing backticks or quotes; Git bash must be named explicitly.
  * the script must be passed as a FILE, not as `-c <script>`: the run text contains backticks,
    quotes, `$` expansions and Windows paths, and every one of them is an opportunity for the launcher
    to reinterpret the argument before bash ever sees it.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import yaml

GIT_BASH = "C:/Program Files/Git/bin/bash.exe"
SCRATCH = pathlib.Path(
    "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
    "/cache/scratch/pipd-s4r3-exec"
)
TARGETS = [
    ("stage-a", pathlib.Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3a-wt")),
    ("stage-b", pathlib.Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3c-wt")),
]
REL = ".github/workflows/public-plugin-verify.yml"
BLOCK_NAME = "Prove the upgrade wrote only inside its allowed set"


def main() -> int:
    if not pathlib.Path(GIT_BASH).exists():
        print(f"git bash not found at {GIT_BASH}", file=sys.stderr)
        return 2
    failures = 0
    for expect_stage, wt in TARGETS:
        doc = yaml.safe_load((wt / REL).read_text(encoding="utf-8"))
        step = next(s for s in doc["jobs"]["verify"]["steps"]
                    if s.get("name", "").startswith(BLOCK_NAME))
        env = {}
        for key, value in (step.get("env") or {}).items():
            text = str(value)
            env[key] = "" if text.startswith("${{") else text
        if env.get("STAGE") != expect_stage:
            print(f"STAGE mismatch in {wt.name}: {env.get('STAGE')!r} != {expect_stage!r}", file=sys.stderr)
            failures += 1
            continue

        script = SCRATCH / f"writeset_step_{expect_stage}.sh"
        # LF only: this host's checkout has core.autocrlf on, and a stray \r inside a bash script turns
        # `set -euo pipefail` into a failed command lookup.
        script.write_bytes(step["run"].replace("\r\n", "\n").encode("utf-8"))
        script.chmod(0o755)

        proc = subprocess.run([GIT_BASH, str(script)], cwd=str(wt),
                              env={**os.environ, **env}, capture_output=True, text=True)
        print(f"===== {expect_stage} in {wt.name} (base env: "
              f"{env.get('STAGE_A_BASE_SHA', '')[:12]}/{env.get('STAGE_B_BASE_REF', '')}) "
              f"-> exit {proc.returncode} =====")
        print(proc.stdout.rstrip())
        if proc.stderr.strip():
            print("--- stderr ---")
            print(proc.stderr.rstrip())
        if proc.returncode != 0:
            failures += 1
    print(f"\n{len(TARGETS) - failures}/{len(TARGETS)} gate runs clean")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
