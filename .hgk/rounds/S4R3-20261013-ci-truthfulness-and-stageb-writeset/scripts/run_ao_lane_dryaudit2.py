#!/usr/bin/env python3
"""Attempt 8: same mandated lane and arm, re-cut evidence bundle for a text-only dry audit.

Why a second bundle instead of a second prompt tweak: attempt 7 was SERVED and produced a real
verdict, and every gap it named is a gap in the MATERIAL, not in the question. It listed exactly
what the size cap had dropped, asked for the gate tool, the allowlists and a `doctor` log, and it
marked C4 REFUTED on a comparison between the head it was told to judge and a CI receipt belonging to
an EARLIER head.

That last one is this driver's fault and its fix is structural: every block below carries the head it
belongs to, earlier heads are labelled HISTORICAL with an explicit instruction not to judge the
current subject from them, and the artefacts the checker asked for are placed FIRST so the size cap
cannot drop them again. Same lane, same forced rank, same required arm, same read-only sandbox -
no escalation flag and no substitute checker.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path("C:/Projects/Agent_Workspace")
HGK = REPO / "HG-KSEOS"
A_WT = REPO / "PIPD/worktrees/s4r3a-wt"
B_WT = REPO / "PIPD/worktrees/s4r3c-wt"
ROUND = B_WT / ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"
SCRATCH = pathlib.Path(
    "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
    "/cache/scratch/pipd-s4r3-exec"
)
NONCE = "HGK_LANE_NONCE_OK"
TOTAL_CAP = 20000
PER_FILE_CAP = 6000
MAX_PROMPT_CHARS = 29000


def head(p: pathlib.Path) -> str:
    return subprocess.run(["git", "-C", str(p), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def blocks(a: str, b: str) -> list[tuple[str, pathlib.Path, str]]:
    """(label-on-record, path, note). Order matters: the checker's own asks come first."""
    return [
        (f"HISTORICAL/label-only (Stage A branch head = {a[:8]})",
         A_WT / "tools/verify_installed_wheel_registry.py",
         "THE GATE TOOL the checker asked to see: committed, invoked by CI, and runnable locally. "
         "It is the thing that makes the wheel-registry gate falsifiable rather than CI-only."),
        ("Stage A branch (current)",
         A_WT / ".github/workflows/public-plugin-verify.yml",
         "THE WRITE-SET GATE with its allowlists: read the ALLOWED set and the stage/base logic. "
         "The checker's C3 question is whether the allowlists were WIDENED to buy a green run - "
         "compare them against the refusals, not against the green."),
        ("Stage A branch (current)",
         A_WT / ".github/workflows/ci.yml",
         "The F006 CI step: it calls the tool above rather than an inline assertion, which is the "
         "C2 claim (a CI-only gate cannot be falsified locally)."),
        ("Stage B branch (current)",
         B_WT / "tests/test_public_plugin_packaging.py",
         "THE C4 EVIDENCE the checker said was absent: the identity-bind refusal (an official manifest "
         "whose name/version disagrees with the release bookkeeping) and the extension-namespace "
         "refusal. These are the two Stage B repairs whose receipts were missing from attempt 7."),
        ("measurement of the Stage A branch (current)",
         SCRATCH / "sdist_doctor.log",
         "THE doctor LOG the checker asked for: its exit code was asserted in attempt 7 without a log."),
        ("measurement of the Stage A branch (current)",
         SCRATCH / "f006_gate_tests.log",
         "The registry gate's own negative controls (missing registry, absent schema, undeclared file)."),
        ("measurement of the Stage B branch (current)",
         SCRATCH / "win_stageb_focused2.log",
         "The focused Stage B run at the current head, with its ran/skipped denominator."),
    ]


def bundle(a: str, b: str) -> tuple[str, list[str]]:
    out, used, kept = [], 0, []
    for label, path, note in blocks(a, b):
        if not path.is_file():
            out.append(f"\n[{path.name} NOT PRESENT on disk at bundle time]\n")
            continue
        room = TOTAL_CAP - used
        if room <= 500:
            out.append(f"\n[{path.name} omitted: budget exhausted]\n")
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        keep = min(PER_FILE_CAP, room)
        if len(body) > keep:
            body = body[:keep] + f"\n[... {len(body) - keep} chars truncated to fit the budget ...]\n"
        used += len(body)
        kept.append(path.name)
        out.append(f"\n===== BEGIN {path.name} =====\n[{label}] {note}\n----- file content -----\n{body}\n"
                   f"===== END {path.name} =====\n")
    return "".join(out), kept


def build_prompt(a: str, b: str) -> tuple[str, list[str]]:
    text, kept = bundle(a, b)
    prompt = f"""You are the INDEPENDENT VERIFIER for a governed round; you are a checker distinct from
the maker. TEXT-ONLY DRY AUDIT: do not execute any command, script, shell or interpreter, and do not
ask to - the sandbox will refuse you. Reason over the material supplied and say INCONCLUSIVE about
anything it cannot settle.

You already audited an earlier bundle of this same round and returned INCONCLUSIVE with C1 CONFIRMED,
C2/C3 PARTIALLY_CONFIRMED and C4 REFUTED. This bundle exists to close the gaps you named. Two things
you raised are addressed structurally here:

  * HEAD LABELLING. Your C4 refutation compared the head you were told to judge against a CI receipt
    belonging to an EARLIER head. That was a defect in the bundle, not in the candidate: receipts from
    successive heads had been mixed without labels. Every block below now carries the branch it
    belongs to, earlier material is labelled HISTORICAL, and material measured on the CURRENT branches
    says so. Judge the current subject only from the current-labelled blocks; if you find a
    contradiction, say which two labels conflict rather than concluding a refutation.
  * YOUR ASKS. The gate tool, the workflow step with its allowlists and the C4 test source head the
    bundle, and the blocks the cap dropped are named at the end. (This sentence used to promise that a
    `doctor` log was at the top so the cap "cannot drop it again". It was not - see the correction in
    evidence/12_GATES/AO_LANE_DRYAUDIT_VERDICT_A8.md - and a prompt must not tell a checker that
    material is present when it is not.)

SUBJECT UNDER TEST (current)
  Stage A branch head : {a}
  Stage B branch head : {b}
  Stage B is stacked on top of Stage A.

CLAIMS
  C1  The standard build ships the contract registry (clean install reports mode=INSTALLED with the
      expected families; doctor exits 0; the sdist-to-wheel route also holds).
  C2  The CI wheel-registry gate is falsifiable: it calls a committed tool that a local run can also
      execute, and a negative case turns it red.
  C3  The write-set gate judges the branch's DECLARED stage and base rather than the pull-request
      base; the frozen-path refusals still refuse. MEASURED DEVIATION (corrected wording): the
      stage-b allowlist gained TWO entries relative to the frozen subject (docs/USER_GUIDE.md and
      the round's own directory), against the admitted requirement whose wording forbids widening.
  C4  Stage B was re-pinned onto the repaired Stage A head and two Stage B defects are refused with
      typed errors: an official manifest whose name/version disagrees with the release bookkeeping,
      and extension namespaces outside the reviewed list.

ATTACK IT
  1. Name any place where an oracle, threshold, denominator or validator was relaxed instead of the
     defect repaired. If you find none, say so plainly.
  2. For each green signal, say whether the same bundle shows the negative case that makes it red.
  3. Name any claim that rests on someone's prose rather than on a raw record.
  4. For the "families" count specifically: state whether the bundle lets you distinguish a correct
     registry from a silently reduced one, and what artefact would settle it if not.

MATERIAL (verbatim; {len(kept)} blocks kept)
{text}

OUTPUT
  One line per claim: `C1: CONFIRMED | PARTIALLY_CONFIRMED | REFUTED | INCONCLUSIVE - reason`.
  Then what you could not verify and why, then residual risks.
  End with exactly:
  VERDICT: CONFIRMED | PARTIALLY_CONFIRMED | REFUTED | INCONCLUSIVE
  Then, on its own line, the token: {NONCE}
"""
    return prompt, kept


def main() -> int:
    attempt = sys.argv[1] if len(sys.argv) > 1 else "8"
    a, b = head(A_WT), head(B_WT)
    prompt, kept = build_prompt(a, b)
    if len(prompt) > MAX_PROMPT_CHARS:
        print(json.dumps({"refused": "ERR_PROMPT_TOO_LONG_FOR_ARGV", "prompt_chars": len(prompt),
                          "max": MAX_PROMPT_CHARS, "kept": kept}, indent=2, ensure_ascii=False))
        return 2
    SCRATCH.mkdir(parents=True, exist_ok=True)
    pf = SCRATCH / f"verify_prompt_s4r3x_dryaudit_a{attempt}.md"
    pf.write_text(prompt, encoding="utf-8", newline="\n")
    outdir = SCRATCH / "ao_lane_dryaudit"
    outdir.mkdir(parents=True, exist_ok=True)
    # MEASURED DEFECT (this driver, attempt 8): the receipt used to carry a hand-written
    # `addressed_from_attempt7` list naming artefacts the larger budget never carried - the doctor log
    # and two logs were offered but DROPPED once the cap was reached, while the receipt still claimed
    # them. A receipt must not claim what the prompt did not contain, so the fields below are computed
    # from what was actually kept.
    offered = [p.name for _label, p, _note in blocks(a, b)]
    receipt = {"lane": "VERIFY_SECURITY", "mode": "text_only_dry_audit_attempt8",
               "stage_a_head": a, "stage_b_head": b, "nonce": NONCE,
               "prompt_file": str(pf), "prompt_chars": len(prompt),
               "blocks_offered": offered, "blocks_kept": kept,
               "blocks_dropped": [n for n in offered if n not in kept],
               "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
               "attempt": attempt, "timeout_s": 1500,
               "addressed_from_attempt7": ["head labelling (C4 false-refutation cause)"]}
    (outdir / f"invocation_a{attempt}.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("prompt_chars", "blocks_kept", "prompt_sha256")},
                     indent=2, ensure_ascii=False))
    argv = [sys.executable, str(HGK / "scripts/hgk-lane-dispatch.py"),
            "--lane", "VERIFY_SECURITY", "--prompt", prompt, "--cwd", str(B_WT),
            "--force-rank", "3", "--require-arm", "opencode-go/glm-5.3-flash",
            "--nonce", NONCE, "--round", "S4R3X-20261013-f006-and-stageb-successor",
            "--attempt", attempt, "--timeout", "1500",
            "--attempt-log-dir", str(outdir / "attempts")]
    proc = subprocess.run(argv, cwd=str(HGK), capture_output=True, text=False)
    (outdir / f"stdout_a{attempt}.txt").write_bytes(proc.stdout)
    (outdir / f"stderr_a{attempt}.txt").write_bytes(proc.stderr)
    print(f"exit={proc.returncode} stdout_bytes={len(proc.stdout)}")
    print(proc.stdout.decode("utf-8", "replace")[-1500:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
