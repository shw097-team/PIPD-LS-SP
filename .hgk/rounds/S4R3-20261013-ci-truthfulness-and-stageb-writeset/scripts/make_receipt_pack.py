#!/usr/bin/env python3
"""Build the C1/C2 receipt pack the verification lane asked for: commands, exit codes, raw output.

The lane's asks, restated exactly: a doctor receipt carrying its OWN exit status and command binding,
the sdist-to-wheel receipt in the same bundle, and a negative run OF THE VERIFIER ITSELF rather than of
some neighbouring tool.

So every step here is recorded as an argv list plus its working directory, its exit code, and digests
of its output - not as prose. The source tree is taken with `git archive HEAD` into scratch, so the
build is bound to the committed head and the candidate work trees are never dirtied (`python -m build`
otherwise writes build/ and *.egg-info into the tree it builds from).

Two routes, both ending in the verifier:
  wheel route : git archive -> wheel -> fresh venv -> install -> doctor -> verifier, expect rc 0
  sdist route : git archive -> sdist -> extract -> wheel -> fresh venv -> install -> doctor ->
                verifier, expect rc 0
Five negative cases then mutate the doctor JSON, one per check the verifier implements, so a refusal
can be attributed to the check it was meant to exercise.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tarfile
import venv

REPO = pathlib.Path("C:/Projects/Agent_Workspace")
A_WT = REPO / "PIPD/worktrees/s4r3a-wt"
ROUND = REPO / "PIPD/worktrees/s4r3c-wt/.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"
SCR = pathlib.Path(
    "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
    "/cache/scratch/pipd-s4r3-exec")
# MEASURED: extracting the head-bound tree under the scratch path fails with WinError 206 - the
# repository carries paths like `.hgk/rounds/R11-.../openspec/changes/...` that push past MAX_PATH once
# the scratch prefix is prepended. Two fixes, both recorded: a SHORT working root, and skipping `.hgk/`
# when extracting, which is not part of the distribution and is not needed to build it.
WORK = pathlib.Path("C:/hgkrcpt")
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
VERIFIER_REL = "tools/verify_installed_wheel_registry.py"
STEPS: list[dict] = []


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def step(label: str, argv: list[str], cwd: pathlib.Path | None = None,
         stdout_to: pathlib.Path | None = None, expect: int | None = 0) -> dict:
    so = subprocess.PIPE
    fh = None
    if stdout_to is not None:
        fh = open(stdout_to, "wb")
        so = fh
    p = subprocess.run(argv, cwd=str(cwd) if cwd else None, stdout=so, stderr=subprocess.PIPE)
    if fh:
        fh.close()
    out = b"" if stdout_to else p.stdout
    rec = {"label": label, "argv": argv, "cwd": str(cwd) if cwd else None, "rc": p.returncode,
           "expected_rc": expect, "rc_as_expected": (expect is None or p.returncode == expect),
           "stdout_bytes": len(out), "stderr_bytes": len(p.stderr),
           "stderr_head": p.stderr.decode("utf-8", "replace")[:400].strip(),
           "stdout_sha256": hashlib.sha256(out).hexdigest() if out else None}
    if stdout_to is not None and stdout_to.is_file():
        rec["stdout_path"] = str(stdout_to)
        rec["stdout_file_sha256"] = sha(stdout_to)
        rec["stdout_head"] = stdout_to.read_text(encoding="utf-8", errors="replace")[:400]
    else:
        rec["stdout_head"] = out.decode("utf-8", "replace")[:400]
    STEPS.append(rec)
    print(f"  [{rec['rc']:>3}] {label}")
    return rec


def main() -> int:
    a_head = subprocess.run(["git", "-C", str(A_WT), "rev-parse", "HEAD"], capture_output=True,
                            text=True, check=True).stdout.strip()
    for d in (WORK, WORK / "neutral"):
        d.mkdir(parents=True, exist_ok=True)
    neutral = WORK / "neutral"

    # 1. head-bound source, without touching the candidate work tree
    tar = WORK / "head.tar"
    with open(tar, "wb") as fh:
        subprocess.run(["git", "-C", str(A_WT), "archive", "HEAD"], stdout=fh, check=True)
    tree = WORK / "tree_head"
    if tree.exists():
        shutil.rmtree(tree)
    tree.mkdir(parents=True)
    with tarfile.open(tar) as tf:
        members = [m for m in tf.getmembers() if not m.name.startswith(".hgk")]
        skipped = len(tf.getmembers()) - len(members)
        tf.extractall(tree, members=members)
    step("git archive HEAD -> scratch tree (head-bound build source)",
         ["git", "-C", str(A_WT), "archive", "HEAD"], cwd=WORK, stdout_to=tar)
    STEPS[-1]["extraction"] = {"members_extracted": len(members), "members_skipped_hgk": skipped,
                               "why": "the .hgk/ tree is not part of the distribution; it also carries "
                                      "paths that exceed MAX_PATH once a scratch prefix is prepended"}

    # 2. wheel route
    whl1_dir = WORK / "whl_wheel"
    step("build wheel from the head-bound tree", [PY, "-m", "build", "--wheel", "--outdir",
                                                 str(whl1_dir)], cwd=tree)
    whl1 = sorted(whl1_dir.glob("*.whl"))[0]
    venv1 = WORK / "venv_wheel"
    if venv1.exists():
        shutil.rmtree(venv1)
    step("create venv (system site-packages so the declared jsonschema dep is real, not skipped)",
         [PY, "-m", "venv", "--system-site-packages", str(venv1)])
    v1py = venv1 / "Scripts" / "python.exe"
    step("install the wheel (offline, deps from the host)",
         [str(v1py), "-m", "pip", "install", "-q", "--no-index", "--no-deps", str(whl1)])
    doc1 = WORK / "doctor_wheel.json"
    step("doctor from a neutral cwd -> its OWN exit status and stdout JSON",
         [str(v1py), "-m", "pipd_ls_sp.cli", "doctor"], cwd=neutral, stdout_to=doc1)
    step("C2 POSITIVE: verifier on the wheel route (deny-prefix = the build tree)",
         [PY, str(tree / VERIFIER_REL), str(doc1), "--expect-families", "19",
          "--deny-prefix", str(tree)])

    # 3. five negatives, one per check the verifier implements
    base = json.loads(doc1.read_text(encoding="utf-8"))
    mutations = {
        "verdict_not_pass": ("DOCTOR_VERDICT", lambda d: d.update(verdict="FAIL")),
        "mode_not_installed": ("DOCTOR_SCHEMA_MODE",
                               lambda d: d["schema_source"].update(mode="SOURCE")),
        "family_count_wrong": ("DOCTOR_FAMILIES", lambda d: d.update(families=18)),
        "family_count_not_an_int": ("DOCTOR_FAMILIES_TYPE", lambda d: d.update(families={"a": 1})),
        "schemas_path_inside_checkout": ("DOCTOR_SCHEMA_PATH_IN_CHECKOUT",
                                         lambda d: d["schema_source"].update(path=str(tree))),
    }
    for name, (code, mutate) in mutations.items():
        d = json.loads(json.dumps(base))
        mutate(d)
        f = WORK / f"doctor_negative_{name}.json"
        f.write_text(json.dumps(d, indent=1, sort_keys=True), encoding="utf-8")
        rec = step(f"C2 NEGATIVE [{name}] expect the verifier to refuse with {code}",
                   [PY, str(tree / VERIFIER_REL), str(f), "--expect-families", "19",
                    "--deny-prefix", str(tree)], expect=1)
        rec["expected_code"] = code
        rec["code_observed"] = code in rec["stderr_head"]

    # 4. sdist route, ending in the same verifier
    sd_dir = WORK / "sdist"
    step("build sdist from the head-bound tree", [PY, "-m", "build", "--sdist", "--outdir",
                                                 str(sd_dir)], cwd=tree)
    sd = sorted(sd_dir.glob("*.tar.gz"))[0]
    ex = WORK / "sdist_extracted"
    if ex.exists():
        shutil.rmtree(ex)
    ex.mkdir(parents=True)
    with tarfile.open(sd) as tf:
        tf.extractall(ex)
    inner = next(p for p in ex.iterdir() if p.is_dir())
    step("extract the sdist (tarfile, not the shell tar whose Windows drive parsing broke earlier)",
         [PY, "-c", f"import tarfile,pathlib;tarfile.open(r'{sd}').extractall(r'{ex}')"])
    whl2_dir = WORK / "whl_sdist"
    step("build wheel FROM the extracted sdist", [PY, "-m", "build", "--wheel", "--outdir",
                                                 str(whl2_dir)], cwd=inner)
    whl2 = sorted(whl2_dir.glob("*.whl"))[0]
    venv2 = WORK / "venv_sdist"
    if venv2.exists():
        shutil.rmtree(venv2)
    step("create venv for the sdist route", [PY, "-m", "venv", "--system-site-packages", str(venv2)])
    v2py = venv2 / "Scripts" / "python.exe"
    step("install the wheel that came from the sdist",
         [str(v2py), "-m", "pip", "install", "-q", "--no-index", "--no-deps", str(whl2)])
    doc2 = WORK / "doctor_sdist.json"
    step("doctor (sdist route)", [str(v2py), "-m", "pipd_ls_sp.cli", "doctor"], cwd=neutral,
         stdout_to=doc2)
    step("C1 POSITIVE: verifier on the sdist route", [PY, str(tree / VERIFIER_REL), str(doc2),
                                                      "--expect-families", "19",
                                                      "--deny-prefix", str(tree)])

    pack = {
        "pack": "C1_C2_receipts",
        "stage_a_head": a_head,
        "note_command_binding": ("Every step is an argv list with its working directory and exit code. "
                                 "The verifier's usage text mentions `pipd doctor --json`; this CLI "
                                 "version defines no --json flag - it always emits JSON on stdout - so "
                                 "the JSON above is stdout captured to a file, and that is stated "
                                 "rather than papered over."),
        "artifacts": {"wheel_route_wheel": {"name": whl1.name, "sha256": sha(whl1)},
                      "sdist": {"name": sd.name, "sha256": sha(sd)},
                      "sdist_route_wheel": {"name": whl2.name, "sha256": sha(whl2)},
                      "doctor_wheel_json": {"sha256": sha(doc1)},
                      "doctor_sdist_json": {"sha256": sha(doc2)}},
        "steps": STEPS,
        "summary": {
            "steps_total": len(STEPS),
            "steps_unexpected_rc": [s["label"] for s in STEPS if not s["rc_as_expected"]],
            "negatives_attributed": [s["label"] for s in STEPS
                                     if s.get("code_observed") is True],
            "negatives_unattributed": [s["label"] for s in STEPS
                                       if "code_observed" in s and s["code_observed"] is False],
        },
    }
    out = ROUND / "evidence/12_GATES/RECEIPT_PACK_C1_C2.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(pack, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(pack["summary"], indent=2, ensure_ascii=False))
    print("wrote", out.name, out.stat().st_size, "bytes")
    return 0 if not pack["summary"]["steps_unexpected_rc"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
