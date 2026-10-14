#!/usr/bin/env python3
"""Splice the stage-aware write-set step into the two copies of public-plugin-verify.yml.

Both copies end up byte-identical except for the single `STAGE:` line, so a reviewer diffing the Stage
A branch against the Stage B branch sees exactly the declaration that differs and nothing else.
"""
from __future__ import annotations

import pathlib

WT_A = pathlib.Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3a-wt")
WT_B = pathlib.Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3c-wt")
REL = ".github/workflows/public-plugin-verify.yml"
BLOCK = pathlib.Path(
    "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
    "/cache/scratch/pipd-s4r3-exec/new_writeset_step_stage_a.yml"
).read_text(encoding="utf-8")

START = "      - name: Prove the upgrade wrote only inside its allowed set\n"
END_MARK = 'echo "WRITE_SET_CLEAN_AGAINST_${BASE}"\n'
STAGE_LINE = "          STAGE: stage-a\n"


def splice(text: str, stage: str) -> str:
    start = text.index(START)
    end = text.index(END_MARK, start) + len(END_MARK)
    block = BLOCK.replace(STAGE_LINE, f"          STAGE: {stage}\n")
    assert f"STAGE: {stage}\n" in block, stage
    return text[:start] + block + text[end:]


def main() -> int:
    # Stage B first: it is the copy that already carries the earlier F002 repair, and the Stage A copy
    # is then made identical to it apart from the declaration.
    target = WT_B / REL
    spliced = splice(target.read_text(encoding="utf-8"), "stage-b")
    target.write_text(spliced, encoding="utf-8")
    print(f"wrote {target} ({len(spliced)} chars)")

    target_a = WT_A / REL
    stage_a = spliced.replace("          STAGE: stage-b\n", "          STAGE: stage-a\n")
    assert "STAGE: stage-a\n" in stage_a
    target_a.write_text(stage_a, encoding="utf-8")
    print(f"wrote {target_a} ({len(stage_a)} chars)")

    diff = [i for i, (x, y) in enumerate(zip(stage_a.splitlines(), spliced.splitlines())) if x != y]
    print("differing lines between the two copies:", [(i + 1, stage_a.splitlines()[i].strip(),
                                                       spliced.splitlines()[i].strip()) for i in diff])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
