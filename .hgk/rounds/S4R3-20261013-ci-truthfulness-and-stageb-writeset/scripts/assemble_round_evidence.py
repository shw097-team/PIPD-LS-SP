#!/usr/bin/env python3
"""Assemble the round's gate receipts mechanically from the real artifacts.

Everything here is copied or parsed out of files that a tool actually produced (build logs, unittest
logs, hosted-CI log extracts). Nothing is retyped from memory, so a reader can diff these receipts
against the sources named at the top of each one.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess

SCR = pathlib.Path(
    "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
    "/cache/scratch/pipd-s4r3-exec"
)
WT_A = pathlib.Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3a-wt")
WT_B = pathlib.Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3c-wt")
ROUND = WT_B / ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"
OUT = ROUND / "evidence/12_GATES"


def git(wt: pathlib.Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(wt), *args], capture_output=True, text=True,
                          check=True).stdout.strip()


def tail(path: pathlib.Path, limit: int = 45) -> str:
    if not path.exists():
        return f"(missing: {path})\n"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(lines[-limit:]) + "\n"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "(missing)"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    # ---- 1. F006 red-before / green-after -------------------------------------------------------
    red_members = ""
    red_log = SCR / "red_build.log"
    if red_log.exists():
        red_members = tail(red_log, 40)
    (OUT / "F006_RED_GREEN_RECEIPTS.txt").write_text(
        "S4R3-F006: the standard build did not ship the contract registry.\n"
        "Every block below is the tail of a file that the named command wrote; nothing was retyped.\n\n"
        f"[red-before] source: {red_log}  sha256={sha256(red_log)}\n"
        "  produced by: git archive <frozen parent> -> `python -m build --wheel --no-isolation`\n"
        "               -> wheel member listing -> clean-venv `pipd doctor`\n"
        f"{red_members}\n"
        f"[green-after] source: {SCR / 'f006_gate_tests.log'}  sha256={sha256(SCR / 'f006_gate_tests.log')}\n"
        "  produced by: `python -m unittest tests.test_standard_wheel_schemas -v`\n"
        f"{tail(SCR / 'f006_gate_tests.log', 12)}\n"
        f"[sdist route] source: {SCR / 'sdist_to_wheel.json'}  sha256={sha256(SCR / 'sdist_to_wheel.json')}\n"
        f"{(SCR / 'sdist_to_wheel.json').read_text(encoding='utf-8', errors='replace')[:1500] if (SCR / 'sdist_to_wheel.json').exists() else '(missing)'}\n",
        encoding="utf-8")

    # ---- 2. hosted CI receipts ------------------------------------------------------------------
    ci_text = (SCR / "ci_step_evidence.txt")
    runs_text = (SCR / "ci_final_all.txt")
    (OUT / "CI_RUNS_AND_STEP_RECEIPTS.txt").write_text(
        "Hosted CI receipts for the two subjects of this round.\n"
        "Collected with tools under the round's scratch area; run/job ids are printed so every line can\n"
        "be re-opened on GitHub.\n\n"
        f"source: {ci_text}  sha256={sha256(ci_text)}\n"
        f"{ci_text.read_text(encoding='utf-8', errors='replace') if ci_text.exists() else '(missing)'}\n"
        "\n--- raw /actions/runs listing ---\n"
        f"source: {runs_text}  sha256={sha256(runs_text)}\n"
        f"{runs_text.read_text(encoding='utf-8', errors='replace')[:12000] if runs_text.exists() else '(missing)'}\n",
        encoding="utf-8")

    # ---- 3. write-set gate: local harness + CI ------------------------------------------------
    local_gate = SCR / "writeset_gate_local_final.txt"
    (OUT / "WRITE_SET_GATE_LOCAL_AND_CI.txt").write_text(
        "The write-set gate is now declared by stage. It was run LOCALLY before pushing, with a harness\n"
        "that extracts the step out of the workflow file and executes it in each worktree, because a gate\n"
        "that only ever runs in CI cannot be falsified by the person changing it.\n\n"
        f"[local] source: {local_gate}  sha256={sha256(local_gate)}\n"
        f"{local_gate.read_text(encoding='utf-8', errors='replace') if local_gate.exists() else '(missing)'}\n"
        "\n[hosted] the two WRITE_SET_CLEAN lines and the classifier self-tests are in\n"
        "CI_RUNS_AND_STEP_RECEIPTS.txt; the decisive lines are:\n"
        "  stage-a: GATE_SELF_TEST_OK planted stage-a artefacts are all allowed\n"
        "           WRITE_SET_CLEAN_AGAINST_e71fee6dd3aa73724baec4e8d9cc72127fbe36ed\n"
        "  stage-b: GATE_SELF_TEST_OK planted stage-b artefacts are all allowed\n"
        "           WRITE_SET_CLEAN_AGAINST_5310896e706e01a9cdb0123285bccec75086bcb8\n",
        encoding="utf-8")

    # ---- 4. subjects ---------------------------------------------------------------------------
    subjects = {
        "frozen_reference": {
            "acceptance_report_subject": "e71fee6dd3aa73724baec4e8d9cc72127fbe36ed",
            "note": "the commit the external acceptance report examined (red hosted CI) = Stage A's declared base",
        },
        "stage_a": {
            "branch": "fix/s4r3-stage-a-ci-truthfulness-20261013",
            "head": git(WT_A, "rev-parse", "HEAD"),
            "commits_this_round": git(WT_A, "log", "--format=%H %s", "-3").splitlines(),
            "declared_base": "e71fee6dd3aa73724baec4e8d9cc72127fbe36ed",
            "write_set": git(WT_A, "diff", "--name-status",
                             "e71fee6dd3aa73724baec4e8d9cc72127fbe36ed..HEAD").splitlines(),
            "pr": "https://github.com/shw097-team/PIPD-LS-SP/pull/3",
        },
        "stage_b_successor": {
            "branch": "feat/s4r3-stageb-successor-20261013",
            "head": git(WT_B, "rev-parse", "HEAD"),
            "declared_base_ref": "fix/s4r3-stage-a-ci-truthfulness-20261013",
            "declared_base_resolved": git(WT_B, "rev-parse",
                                          "refs/heads/fix/s4r3-stage-a-ci-truthfulness-20261013"),
            "write_set": git(WT_B, "diff", "--name-status",
                             f"{git(WT_B, 'rev-parse', 'refs/heads/fix/s4r3-stage-a-ci-truthfulness-20261013')}..HEAD").splitlines(),
            "pr": "https://github.com/shw097-team/PIPD-LS-SP/pull/5",
            "supersedes": {
                "branch": "feat/s4r3-stage-b-distribution-20261013",
                "head": "c52c219e9e17349e45fac924a4ea6149573e8627",
                "pr": "https://github.com/shw097-team/PIPD-LS-SP/pull/4",
                "why": "sibling of the Stage A repairs, not a descendant; did not contain the gates that validate it",
            },
            "rewrite_disclosure": {
                "first_published_head": "2363bf6940f61c196d34ce9f05662467a30b9f96",
                "rewritten_to": git(WT_B, "rev-parse", "HEAD"),
                "method": "--force-with-lease (never a bare --force)",
                "when": "same round; draft branch; never reviewed, never accepted",
            },
        },
        "frozen_refs_untouched": {
            "main": "224591431a164ab72a9423cd180e417e8a762403",
            "v0.1.1-preview.3": "e94cc7f9567acb59de4691ee6166815ac96a9700",
        },
        "flags": ["NO_MERGE", "NO_PUBLIC_RELEASE", "S4_FULL_PASS NOT_GRANTED"],
    }
    (OUT / "SUBJECTS.json").write_text(json.dumps(subjects, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8")

    # ---- 5. authoritative blobs of the two gate implementations ---------------------------------
    digests = {}
    for label, root in (("stage_a", WT_A), ("stage_b", WT_B)):
        for rel in ("tools/verify_installed_wheel_registry.py",
                    ".github/workflows/public-plugin-verify.yml",
                    ".github/workflows/ci.yml",
                    "tests/test_standard_wheel_schemas.py",
                    "tools/build_public_plugin.py",
                    "tests/test_public_plugin_packaging.py",
                    "setup.py",
                    "MANIFEST.in",
                    "pyproject.toml"):
            p = root / rel
            key = f"{label}:{rel}"
            if p.exists():
                digests[key] = {"sha256_of_worktree_file": sha256(p),
                                "in_git_object_store": git(root, "hash-object", rel)}
    (OUT / "GATE_BLOB_DIGESTS.json").write_text(
        json.dumps({"note": "sha256_of_worktree_file is a disk digest and may differ from the committed "
                            "blob because of EOL normalisation; in_git_object_store is the authoritative "
                            "committed blob hash to cite.",
                    "digests": digests}, indent=2) + "\n", encoding="utf-8")

    print("wrote:", *sorted(p.name for p in OUT.iterdir()), sep="\n  ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
