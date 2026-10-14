#!/usr/bin/env python3
"""Drive the sealed VERIFY_SECURITY lane as a TEXT-ONLY dry audit (attempt 4).

ROOT CAUSE OF THE THREE EARLIER ATTEMPTS (recorded here because the earlier evidence got it
partly wrong): `hgk-lane-dispatch.py` declares `--nonce` with the DEFAULT value
`HGK_LANE_NONCE_OK` and requires that exact string to appear inside an assistant message item
(`nonce_in_agent_message`, carrier `item.completed/agent_message`). The caller must therefore ASK
the checker to echo that token - the dispatcher does not inject the request into the prompt. The
earlier prompts never asked for it, so an arm that answered perfectly still could not satisfy the
check and the lane returned ERR_NO_ARM_EMITTED_NONCE. The sandbox refusal that showed up in those
attempts was real but was NOT the decisive cause; the missing nonce instruction was.

This driver therefore (a) asks for the token explicitly, (b) tells the checker it may not execute
anything - the earlier attempts died because the checker tried to run a shell command and was
policy-refused - and (c) inlines the raw receipts so a text-only audit is possible at all, which is
exactly the dry audit the checker itself proposed.
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
# MEASURED (attempt 4, WinError 206): the dispatcher takes the prompt as a COMMAND-LINE argument
# (`codex exec ... args.prompt`, no file-based option), so a prompt larger than the Windows
# CreateProcess limit (~32k chars) cannot be spawned at all - it dies before any model sees it.
# The cap below is therefore a hard pre-spawn guard, not a style preference, and the evidence
# inlining is sized to fit inside it.
TOTAL_CAP = 20000
PER_FILE_CAP = 6000
MAX_PROMPT_CHARS = 29000


def head(path: pathlib.Path) -> str:
    return subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def receipts() -> str:
    gd = ROUND / "evidence/12_GATES"
    picked = sorted(p for p in gd.glob("*") if p.is_file()
                    and p.suffix.lower() in (".txt", ".json", ".md"))
    out, used = [], 0
    for p in picked:
        if used >= TOTAL_CAP:
            out.append(f"\n[{p.name} omitted: total cap {TOTAL_CAP} chars reached]\n")
            continue
        body = p.read_text(encoding="utf-8", errors="replace")
        # Clip to whichever is smaller: the per-file cap, or the room left in the total budget.
        # (Earlier this only checked the per-file cap, so the LAST file could overshoot the total
        # by a whole file - the exact overshoot that tripped the pre-spawn length guard.)
        room = TOTAL_CAP - used
        keep = min(PER_FILE_CAP, room)
        if len(body) > keep:
            body = body[:keep] + f"\n[... {len(body) - keep} chars truncated to fit the budget ...]\n"
        used += len(body)
        out.append(f"\n===== BEGIN FILE: {p.name} =====\n{body}\n===== END FILE: {p.name} =====\n")
    return "".join(out)


def build_prompt(a_head: str, b_head: str) -> str:
    return f"""You are the INDEPENDENT VERIFIER for a governed round. You are a checker distinct from
the maker. This is a TEXT-ONLY DRY AUDIT: you must NOT execute any command, script, shell or
interpreter, and you must not ask to; the sandbox will refuse you and that refusal has cost this
round three attempts already. Everything you need is supplied below. Reason over the supplied
material only, and say INCONCLUSIVE about anything the material cannot settle.

SUBJECT UNDER TEST
  Stage A branch head : {a_head}
  Stage B branch head : {b_head}
  Stage B is stacked on top of Stage A. The round's claim is that five defects were repaired at root
  cause, that every gate is now falsifiable locally, and that no oracle was relaxed.

CLAIMS TO ATTACK (one verdict each)
  C1  The standard build ships the contract registry: `python -m build` produces a wheel whose clean
      install reports registry mode=INSTALLED with 19 resolvable families, and `doctor` exits 0;
      the sdist-to-wheel route (build the wheel FROM the unpacked sdist) also holds.
  C2  The CI wheel-registry gate is genuinely falsifiable: it calls a committed tool that a local
      run can also execute, and a negative case turns it red.
  C3  The write-set gate now judges the branch's DECLARED stage and base rather than the pull-request
      base, so a Stage A repair is no longer counted as a Stage B write; the allowlists were NOT
      widened and the frozen-path refusals still refuse.
  C4  Stage B was re-pinned onto the repaired Stage A head, and two Stage B defects were closed:
      an official manifest whose name/version may disagree with the release bookkeeping, and
      extension namespaces outside the reviewed list are both refused.

REQUIRED REFUTATION ATTEMPTS - report the outcome of each, including the ones that "work":
  1. Look for any place where an oracle, threshold, denominator or validator was RELAXED rather than
     the defect repaired. State the strongest candidate you found, or state that you found none.
  2. Check whether each green signal is FALSIFIABLE: is there a negative case that makes it red, and
     does the same artefact exist as evidence for both the red and the green state?
  3. Check whether any quoted receipt is load-bearing but absent, or is a summary of something not
     shown. Name any claim that rests on the maker's prose rather than on a raw receipt.
  4. State what these receipts CANNOT establish: which installation routes, environments or
     acceptance acts are outside their coverage.

MATERIAL: raw receipts as committed in the round directory (verbatim)
{receipts()}

OUTPUT
  Give one line per claim: `C1: CONFIRMED | PARTIALLY_CONFIRMED | REFUTED | INCONCLUSIVE - reason`.
  Some files below are marked truncated or omitted to fit a hard command-line limit; if a claim
  depends on material that is missing, say INCONCLUSIVE and name the file you would need. Anything
  you cannot check from what is supplied counts against the claim, not for it.
  Then list what you could not verify and why, then residual risks.
  End with a final line of exactly:
  VERDICT: CONFIRMED | PARTIALLY_CONFIRMED | REFUTED | INCONCLUSIVE
  Then, on its own line, the exact token: {NONCE}
"""


def main() -> int:
    attempt = sys.argv[1] if len(sys.argv) > 1 else "4"
    a_head, b_head = head(A_WT), head(B_WT)
    prompt = build_prompt(a_head, b_head)
    if len(prompt) > MAX_PROMPT_CHARS:
        print(json.dumps({
            "refused": "ERR_PROMPT_TOO_LONG_FOR_ARGV",
            "prompt_chars": len(prompt), "max": MAX_PROMPT_CHARS,
            "why": ("the dispatcher passes the prompt as a command-line argument and has no file-based "
                    "option, so a longer prompt cannot be spawned (WinError 206) and would be recorded "
                    "as a failed attempt that no model ever saw. Refusing before the spawn is the "
                    "honest outcome; shrink the inlined evidence instead of hiding the failure."),
        }, indent=2, ensure_ascii=False))
        return 2
    SCRATCH.mkdir(parents=True, exist_ok=True)
    pf = SCRATCH / f"verify_prompt_s4r3x_dryaudit_a{attempt}.md"
    pf.write_text(prompt, encoding="utf-8", newline="\n")
    outdir = SCRATCH / "ao_lane_dryaudit"
    outdir.mkdir(parents=True, exist_ok=True)
    argv = [
        sys.executable, str(HGK / "scripts/hgk-lane-dispatch.py"),
        "--lane", "VERIFY_SECURITY",
        "--prompt", prompt,
        "--cwd", str(B_WT),
        "--force-rank", "3",
        "--require-arm", "opencode-go/glm-5.3-flash",
        "--nonce", NONCE,
        "--round", "S4R3X-20261013-f006-and-stageb-successor",
        "--attempt", attempt,
        "--timeout", "1500",
        "--attempt-log-dir", str(outdir / "attempts"),
    ]
    receipt = {
        "lane": "VERIFY_SECURITY", "mode": "text_only_dry_audit",
        "stage_a_head": a_head, "stage_b_head": b_head, "nonce": NONCE,
        "prompt_file": str(pf), "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "prompt_chars": len(prompt), "attempt": attempt, "timeout_s": 1500,
        "root_cause_of_earlier_attempts": (
            "the earlier prompts never asked the checker to echo the dispatcher's nonce token, so an "
            "answering arm still read ERR_NO_ARM_EMITTED_NONCE; the sandbox refusal seen in those runs "
            "was real but not decisive"),
    }
    (outdir / f"invocation_a{attempt}.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(receipt, indent=2, ensure_ascii=False)[:1200])
    proc = subprocess.run(argv, cwd=str(HGK), capture_output=True, text=False)
    (outdir / f"stdout_a{attempt}.txt").write_bytes(proc.stdout)
    (outdir / f"stderr_a{attempt}.txt").write_bytes(proc.stderr)
    print(f"exit={proc.returncode} stdout_bytes={len(proc.stdout)} stderr_bytes={len(proc.stderr)}")
    print("--- stdout tail ---")
    print(proc.stdout.decode("utf-8", "replace")[-2500:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
