#!/usr/bin/env python3
"""Attempts 9 and 10: the SPLIT bundles the checker's own gap list implies.

Measured constraint that forces the split: the dispatcher passes the prompt as a command-line
argument, so a bundle larger than ~29k chars cannot be spawned at all. Attempt 6 hit that limit;
attempt 7 spent its budget on raw receipts and had no source; attempt 8 spent it on source and had no
raw receipts - and said so, in both directions. One bundle cannot carry both, so this driver runs two
focused audits against the same subject with the same lane, arm and sandbox:

  BUNDLE=code      the gate tool, the two workflow steps with their allowlists, and the Stage B test
                   source - i.e. the material that answers "was anything relaxed?".
  BUNDLE=evidence  the raw receipts: the doctor JSON, the sdist-route receipt, the gate's own
                   negative-control log, the focused-run denominators, and a freshly generated
                   registry listing with per-file digests - i.e. the material that answers "does the
                   registry that shipped equal the registry in the tree?".

Every block is labelled with the branch it belongs to, and the prompt repeats the reason: attempt 7
produced a false REFUTED by comparing the current head against a receipt from an earlier head.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
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
TOTAL_CAP = 21000
PER_FILE_CAP = 20000
MAX_PROMPT_CHARS = 29000


def head(p: pathlib.Path) -> str:
    return subprocess.run(["git", "-C", str(p), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def excerpt(path: pathlib.Path, marker: str, before: int = 5, after: int = 80, max_hits: int = 3) -> str:
    """Return the regions of `path` around lines matching `marker`, so a big file fits the budget."""
    if not path.is_file():
        return f"[{path.name} NOT PRESENT]"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    rx = re.compile(marker)
    hits = [i for i, l in enumerate(lines) if rx.search(l)][:max_hits]
    if not hits:
        return f"[{path.name}: no line matched {marker!r}; head follows]\n" + "\n".join(lines[:60])
    out = []
    for h in hits:
        lo, hi = max(0, h - before), min(len(lines), h + after)
        out.append(f"[{path.name} lines {lo + 1}-{hi}]\n" + "\n".join(lines[lo:hi]))
    return "\n...\n".join(out)


def registry_listing() -> str:
    """A fresh listing of the canonical registry with per-file digests (the checker asked for this)."""
    base = A_WT / "schemas"
    if not base.is_dir():
        return "[schemas/ not found in the Stage A worktree]"
    rows = []
    for p in sorted(base.rglob("*")):
        if p.is_file() and p.suffix.lower() in (".json", ".yaml", ".yml"):
            rows.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(A_WT).as_posix()}")
    return (f"canonical registry listing from {base.as_posix()} - {len(rows)} files:\n" + "\n".join(rows))


def blocks(bundle: str, a: str, b: str) -> list[tuple[str, str, str]]:
    """(label, block name, text)."""
    if bundle == "receipts":
        return [
            ("measurement of the Stage A branch (current) - head-bound",
             "RECEIPT_PACK_C1_C2.json - every command, its cwd, its OWN exit code",
             (ROUND / "evidence/12_GATES/RECEIPT_PACK_C1_C2.json").read_text(
                 encoding="utf-8", errors="replace")),
        ]
    if bundle == "c3":
        return [
            ("Stage A branch (current)",
             "WRITE_SET_GATE_STEP.yml - the write-set gate step, verbatim from the workflow, with its "
             "allowlist, its frozen-path and traversal refusals and its planted-violation self-test",
             (ROUND / "evidence/12_GATES/WRITE_SET_GATE_STEP.yml").read_text(
                 encoding="utf-8", errors="replace")),
            ("measurement of the current Stage A branch",
             "refusals and allowances actually recorded, local run and hosted CI run side by side",
             (ROUND / "evidence/12_GATES/C3_REFUSAL_RECEIPT_DISTILLED.txt").read_text(
                 encoding="utf-8", errors="replace")),
        ]
    if bundle == "c4":
        return [
            ("Stage B branch (current)",
             "the Stage B refusal tests, verbatim - CR-IDENTITY-BIND and CR-EXT-UNREVIEWED",
             (ROUND / "evidence/12_GATES/C4_STAGE_B_REFUSAL_TESTS_SOURCE.py").read_text(
                 encoding="utf-8", errors="replace")),
            ("measurement of the current Stage B head",
             "the verbose run of those tests at the current head, with the denominator",
             (ROUND / "evidence/12_GATES/C4_REFUSAL_TESTS_RUN.log").read_text(
                 encoding="utf-8", errors="replace")),
            ("measurement of the current Stage B head",
             "re-pin and declared-base evidence, measured (merge-base) rather than asserted",
             (ROUND / "evidence/12_GATES/C4_REPIN_AND_DECLARED_BASE.txt").read_text(
                 encoding="utf-8", errors="replace")),
        ]
    if bundle == "family":
        # The targeted follow-up: the receipt three audits asked for, whole, plus the real doctor
        # receipts (attempt 10 supplied a broken doctor log and the checker caught it).
        ci = ROUND / "evidence/12_GATES/CI_RUNS_AND_STEP_RECEIPTS.txt"
        doc_lines = []
        if ci.is_file():
            for line in ci.read_text(encoding="utf-8", errors="replace").splitlines():
                if "INSTALLED" in line or "families" in line or "doctor" in line.lower():
                    doc_lines.append(line.strip()[:300])
        return [
            ("measurement of the Stage A branch (current) - head-bound",
             "FAMILY_IDENTITY_RECEIPT.md (the artefact the lane named)",
             (ROUND / "evidence/12_GATES/FAMILY_IDENTITY_RECEIPT.md").read_text(
                 encoding="utf-8", errors="replace")),
            ("measurement of the Stage A branch (current)",
             "the REAL doctor receipts (attempt 10 supplied a broken log; the checker caught it)",
             "\n".join(doc_lines[:40]) or "[no doctor lines found]"),
            ("Stage A branch (current)", "what the lane still says it cannot see",
             (ROUND / "evidence/12_GATES/AO_LANE_DRYAUDIT_VERDICT_A9_A10.md").read_text(
                 encoding="utf-8", errors="replace")[:3000]),
        ]
    if bundle == "code":
        return [
            ("Stage A branch (current)", "tools/verify_installed_wheel_registry.py",
             excerpt(A_WT / "tools/verify_installed_wheel_registry.py", r".", 0, 400, 1)),
            ("Stage A branch (current)", "ci.yml - the F006 step",
             excerpt(A_WT / ".github/workflows/ci.yml", r"verify_installed_wheel_registry", 20, 60)),
            ("Stage A branch (current)", "public-plugin-verify.yml - declared-base logic and allowlists",
             excerpt(A_WT / ".github/workflows/public-plugin-verify.yml",
                      r"STAGE_A_BASE|STAGE_B_BASE|ALLOWED|frozen", 10, 45, 6)),
            ("Stage B branch (current)", "test_public_plugin_packaging.py - the C4 refusals",
             excerpt(B_WT / "tests/test_public_plugin_packaging.py",
                      r"def test_20|identity|identity_bind|extension", 4, 55, 6)),
        ]
    return [
        ("measurement of the Stage A branch (current)", "registry listing with per-file digests",
         registry_listing()),
        ("measurement of the Stage A branch (current)", "sdist-route receipt",
         (SCRATCH / "sdist_to_wheel.json").read_text(encoding="utf-8", errors="replace")
         if (SCRATCH / "sdist_to_wheel.json").is_file() else "[absent]"),
        ("measurement of the Stage A branch (current)", "doctor log",
         (SCRATCH / "sdist_doctor.log").read_text(encoding="utf-8", errors="replace")
         if (SCRATCH / "sdist_doctor.log").is_file() else "[absent]"),
        ("measurement of the Stage A branch (current)", "gate negative-control log",
         excerpt(SCRATCH / "f006_gate_tests.log", r"^test_|ok$|FAIL", 0, 3, 40)),
        ("measurement of the Stage B branch (current)", "focused run denominators",
         (SCRATCH / "win_stageb_focused2.log").read_text(encoding="utf-8", errors="replace")[-2500:]
         if (SCRATCH / "win_stageb_focused2.log").is_file() else "[absent]"),
        ("Stage A branch (current)", "blob digests index",
         (ROUND / "evidence/12_GATES/GATE_BLOB_DIGESTS.json").read_text(encoding="utf-8", errors="replace")
         if (ROUND / "evidence/12_GATES/GATE_BLOB_DIGESTS.json").is_file() else "[absent]"),
    ]


def build(bundle: str, a: str, b: str) -> tuple[str, list[str]]:
    parts, used, kept = [], 0, []
    for label, name, text in blocks(bundle, a, b):
        room = TOTAL_CAP - used
        if room <= 500:
            parts.append(f"\n[{name} omitted: budget exhausted]\n")
            continue
        keep = min(PER_FILE_CAP, room)
        if len(text) > keep:
            text = text[:keep] + f"\n[... {len(text) - keep} chars truncated to fit the budget ...]\n"
        used += len(text)
        kept.append(name)
        parts.append(f"\n===== BEGIN {name} =====\n[{label}]\n----- content -----\n{text}\n===== END {name} =====\n")
    focus = ("whether any oracle, threshold, denominator or validator was RELAXED, and whether the "
             "write-set allowlists were widened"
             if bundle == "code" else
             "whether the registry that shipped equals the registry in the tree, and whether each "
             "green signal has its paired negative")
    prompt = f"""You are the INDEPENDENT VERIFIER for a governed round; you are a checker distinct from
the maker. TEXT-ONLY DRY AUDIT: do not execute any command or interpreter, and do not ask to.

This is FOCUSED BUNDLE `{bundle}` of a split audit. You audited this round twice already and returned
INCONCLUSIVE both times, naming the gaps each time; the bundle is split because the dispatcher passes
the prompt on a command line, so one prompt cannot carry both source and raw receipts. Your focus in
THIS bundle is: {focus}.

HEAD LABELLING (why it matters here): your first audit returned `C4: REFUTED` by comparing the head
you were told to judge against a CI receipt belonging to an EARLIER head. That was a defect in the
bundle, not in the candidate. Every block below is labelled with the branch it belongs to, all of them
CURRENT. If two blocks appear to conflict, say which labels conflict - do not conclude a refutation
from a mismatch you cannot attribute.

SUBJECT UNDER TEST (current)
  Stage A branch head : {a}
  Stage B branch head : {b}
  Stage B is stacked on top of Stage A.

CLAIMS
  C1  The standard build ships the contract registry (clean install reports mode=INSTALLED with the
      expected families; doctor exits 0; the sdist-to-wheel route also holds).
  C2  The CI wheel-registry gate is falsifiable: it calls a committed tool a local run can execute,
      and a negative case turns it red.
  C3  The write-set gate judges the branch's DECLARED stage and base, not the pull-request base; the
      frozen-path refusals still refuse. MEASURED DEVIATION (corrected wording): the stage-b
      allowlist gained TWO entries relative to the frozen subject (docs/USER_GUIDE.md and the
      round's own directory), against the admitted requirement whose wording forbids widening.
  C4  Stage B was re-pinned onto the repaired Stage A head; two Stage B defects are refused with typed
      errors (official manifest name/version disagreeing with the release bookkeeping; extension
      namespaces outside the reviewed list).

Judge as many claims as this bundle lets you judge, and mark the rest INCONCLUSIVE with the reason.
For the families question specifically, state whether this bundle lets you distinguish a correct
registry from a silently reduced one, and if not, the exact artefact that would.

MATERIAL ({len(kept)} blocks)
{''.join(parts)}

OUTPUT
  One line per claim: `C1: CONFIRMED | PARTIALLY_CONFIRMED | REFUTED | INCONCLUSIVE - reason`.
  Then what you could not verify and why, then residual risks.
  End with exactly:
  VERDICT: CONFIRMED | PARTIALLY_CONFIRMED | REFUTED | INCONCLUSIVE
  Then, on its own line, the token: {NONCE}
"""
    return prompt, kept


def run(bundle: str, attempt: str, a: str, b: str) -> int:
    prompt, kept = build(bundle, a, b)
    if len(prompt) > MAX_PROMPT_CHARS:
        print(json.dumps({"refused": "ERR_PROMPT_TOO_LONG_FOR_ARGV", "bundle": bundle,
                          "prompt_chars": len(prompt), "kept": kept}, ensure_ascii=False))
        return 2
    outdir = SCRATCH / "ao_lane_dryaudit"
    outdir.mkdir(parents=True, exist_ok=True)
    pf = SCRATCH / f"verify_prompt_s4r3x_{bundle}_a{attempt}.md"
    pf.write_text(prompt, encoding="utf-8", newline="\n")
    receipt = {"lane": "VERIFY_SECURITY", "mode": f"text_only_dry_audit_bundle_{bundle}",
               "bundle": bundle, "stage_a_head": a, "stage_b_head": b, "nonce": NONCE,
               "prompt_chars": len(prompt), "blocks_kept": kept, "attempt": attempt,
               "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest()}
    (outdir / f"invocation_{bundle}_a{attempt}.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    argv = [sys.executable, str(HGK / "scripts/hgk-lane-dispatch.py"),
            "--lane", "VERIFY_SECURITY", "--prompt", prompt, "--cwd", str(B_WT),
            "--force-rank", "3", "--require-arm", "opencode-go/glm-5.3-flash",
            "--nonce", NONCE, "--round", "S4R3X-20261013-f006-and-stageb-successor",
            "--attempt", attempt, "--timeout", "1500",
            "--attempt-log-dir", str(outdir / "attempts")]
    proc = subprocess.run(argv, cwd=str(HGK), capture_output=True, text=False)
    (outdir / f"stdout_{bundle}_a{attempt}.txt").write_bytes(proc.stdout)
    (outdir / f"stderr_{bundle}_a{attempt}.txt").write_bytes(proc.stderr)
    try:
        rec = json.loads(proc.stdout.decode("utf-8", "replace"))
        print(json.dumps({"bundle": bundle, "attempt": attempt, "ok": rec.get("ok"),
                          "code": rec.get("code"), "served_arm": rec.get("served_arm"),
                          "seconds": rec.get("used_seconds")}, ensure_ascii=False))
    except Exception:
        print(json.dumps({"bundle": bundle, "attempt": attempt, "exit": proc.returncode,
                          "stdout_bytes": len(proc.stdout)}, ensure_ascii=False))
    return 0


def main() -> int:
    a, b = head(A_WT), head(B_WT)
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which == "final3":
        plan = [("receipts", "12"), ("c3", "13"), ("c4", "14")]
    elif which == "both":
        plan = [("code", "9"), ("evidence", "10")]
    else:
        plan = [(which, sys.argv[2] if len(sys.argv) > 2 else "9")]
    for bundle, attempt in plan:
        rc = run(bundle, attempt, a, b)
        if rc:
            return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
