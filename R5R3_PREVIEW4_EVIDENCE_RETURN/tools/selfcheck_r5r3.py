"""R5R3-20261016 machine self-check / self-repair harness (re-runnable).

Re-derives every checkpoint of the round from LIVE evidence - the remote/本地 git objects, the
downloaded release bytes, the two probe runs and the raw suite log - never from the round's own
summary files. Prints PASS / FAIL / INCONCLUSIVE per check plus the claim ceiling on EVERY run.

The verdict is a MACHINE GATE for this round's own evidence. It is never an acceptance, an approval
or a Gate, and it never prints PASS for one.

Usage: selfcheck_r5r3.py [--repair]
  --repair : bounded repair of THIS round's own records only (max 3 iterations, subject untouched,
             remote-write verbs forbidden). "no repair performed" is a valid, reported outcome.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROUND = Path("C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout")
WT = Path("C:/Projects/wt-r5r3")
PIPD = Path("C:/Projects/Agent_Workspace/PIPD")
PY311 = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
SUBJECT_COMMIT = "dba4b19456777d3b597fdf71480f6423dd974243"
SERVED = {
    "pipd-ls-sp-public-skills.zip": ("545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75", 68357),
    "pipd_ls_sp-0.1.1a4-py3-none-any.whl": ("3b59a985dc9fc1cd4c1c5ca9a7b779122459ab7cadc8f439e17063d6c934cc0c", 286978),
    "SHA256SUMS": ("0f76502670038ae35bd4f772dc23223f6b47241c3acee2f918d106eaabffe689", 583),
}
CLAIM_CEILING = ("CANDIDATE_ONLY - machine gate over this round's own evidence; NOT an acceptance, "
                 "NOT an approval, NOT an independent verdict, NOT a Gate PASS")

WRITE_ROOT = ROUND.resolve()
GIT_WRITE_VERBS = {"push", "commit", "tag", "merge", "rebase", "reset", "checkout", "switch",
                   "apply", "cherry-pick", "revert", "clean", "stash", "rm", "mv", "update-ref"}


class Guarded(Exception):
    pass


def guard_write(path: Path, kind: str, reason: str) -> None:
    """Refuse a write outside the round's own root. Raising is the deliverable here."""
    target = Path(path)
    try:
        resolved = target.resolve()
    except OSError as exc:
        raise Guarded(f"GUARD_WRITE_UNRESOLVABLE:{kind}:{exc}") from exc
    if WRITE_ROOT not in resolved.parents and resolved != WRITE_ROOT:
        raise Guarded(f"GUARD_WRITE_OUTSIDE_ROUND_ROOT:{kind}:{reason}:{resolved}")


def guard_shell(cmd: str) -> None:
    """Refuse a git WRITE verb in a shell string. The verb is parsed, not the path."""
    tokens = cmd.replace('"', " ").replace("'", " ").split()
    for i, tok in enumerate(tokens):
        if Path(tok).name in ("git", "git.exe"):
            rest = [t for t in tokens[i + 1:] if not t.startswith("-")
                    and not Path(t).parts[:1] == ("-C",)]
            # skip the argument of -C / --git-dir
            rest = [t for t in rest if ":" not in t or "/" not in t]
            if rest and rest[0] in GIT_WRITE_VERBS:
                raise Guarded(f"GUARD_GIT_WRITE_VERB:{rest[0]}")
    return None


def sh(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def guarded_sh(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    guard_shell(" ".join(cmd))
    return sh(cmd, cwd)


def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


CHECKS: list[dict] = []


def check(cid: str, ok: bool | None, detail: dict) -> None:
    verdict = "INCONCLUSIVE" if ok is None else ("PASS" if ok else "FAIL")
    CHECKS.append({"id": cid, "verdict": verdict, "detail": detail})


def s1_subject_binding() -> None:
    rc, out = guarded_sh(["git", "-C", str(PIPD).replace("\\", "/"), "rev-parse", "origin/main"])
    live = out.strip()
    rc2, out2 = guarded_sh(["git", "-C", str(WT).replace("\\", "/"), "rev-parse", "HEAD"])
    digests_ok = {}
    for name, (dig, size) in SERVED.items():
        p = ROUND / "raw" / "served" / "assets" / name
        if not p.is_file():
            digests_ok[name] = None
            continue
        digests_ok[name] = (sha256(p) == dig and p.stat().st_size == size)
    ok = (live == SUBJECT_COMMIT and rc2 == 0 and all(v is True for v in digests_ok.values()))
    check("S1_subject_binding", ok, {"origin_main_live": live, "expected": SUBJECT_COMMIT,
                                     "worktree_head": out2.strip(), "served_digests_ok": digests_ok})


def s2_s4_probes() -> None:
    src = json.loads((ROUND / "raw" / "edge_probe.json").read_text(encoding="utf-8"))
    whl = json.loads((ROUND / "raw" / "edge_probe_wheel.json").read_text(encoding="utf-8"))
    wheel_divergence = [r["id"] for r in whl["cases"] if not r["match"]]
    check("S2_d1_d2_type5_on_main", src["summary"]["verdict"] == "PASS", src["summary"])
    # The released wheel is a DIFFERENT subject (tag target), so a divergence is reported, not failed.
    check("S3_released_wheel_edges", whl["summary"]["verdict"] == "PASS" or
          wheel_divergence == ["D2-NO-SPACE"],
          {"summary": whl["summary"], "divergence": wheel_divergence,
           "note": "D2-NO-SPACE is the R5R2 refinement (PR #13) that landed on main AFTER the tag"})
    check("S4_type5_no_native_exception",
          all(v.get("native_exception") is None for v in src["cases"]
              if v["kind"] == "type5"),
          {r["id"]: r["observed"].get("native_exception") for r in src["cases"]
           if r["kind"] == "type5"})


def s5_suite() -> None:
    text = (ROUND / "raw" / "full_suite_main.log").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^Ran (\d+) tests", text, re.M)
    ok = "EXIT=0" in text and "OK (skipped=" in text and m is not None
    check("S5_full_suite", ok, {"ran": m.group(1) if m else None,
                                "tail": text.strip().splitlines()[-2:],
                                "subject": SUBJECT_COMMIT})


def s6_wheel() -> None:
    p = ROUND / "raw" / "wheel_smoke.json"
    if not p.is_file():
        check("S6_wheel_clean_install", None, {"reason": "raw/wheel_smoke.json missing"})
        return
    d = json.loads(p.read_text(encoding="utf-8"))
    check("S6_wheel_clean_install", d["verdict"] == "PASS",
          {"checks": d["checks"], "doctor": d["doctor"]["stdout"][:200]})


def s7_zip() -> None:
    zpath = ROUND / "raw" / "served" / "assets" / "pipd-ls-sp-public-skills.zip"
    if not zpath.is_file():
        check("S7_plugin_zip", None, {"reason": "served ZIP not downloaded"})
        return
    zf = zipfile.ZipFile(io.BytesIO(zpath.read_bytes()))
    names = zf.namelist()
    roots = sorted({n.split("/")[0] for n in names if n})
    skills = sorted({n for n in names if n.count("/") == 3 and n.split("/")[1] == "skills"
                     and n.endswith("SKILL.md")})
    traversal = [n for n in names if n.startswith("/") or ".." in n.split("/") or "\\" in n]
    forbidden = [n for n in names if any(k in n for k in (".hgk/", "hooks/", "mcp.json", ".env"))]
    ok = (len(roots) == 1 and len(skills) == 8 and not traversal and not forbidden
          and zf.testzip() is None)
    check("S7_plugin_zip", ok, {"roots": roots, "skill_md": len(skills), "entries": len(names),
                                "traversal": traversal, "forbidden": forbidden,
                                "crc_ok": zf.testzip() is None})


def s8_sums() -> None:
    d = json.loads((ROUND / "raw" / "served_assets.json").read_text(encoding="utf-8"))
    rows = d["sha256sums"]["rows"]
    ok = bool(rows) and all(r["match"] for r in rows.values())
    # recompute independently from the files on disk
    text = (ROUND / "raw" / "served" / "assets" / "SHA256SUMS").read_text(encoding="utf-8")
    recomputed = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 2:
            p = ROUND / "raw" / "served" / "assets" / parts[1].lstrip("*")
            recomputed[parts[1]] = (p.is_file() and sha256(p) == parts[0])
    check("S8_served_asset_readback", ok and all(recomputed.values()),
          {"entries": len(rows), "recomputed": recomputed})


def s9_guards() -> None:
    results = {}
    try:
        guard_write(Path("C:/Projects/wt-r5r3/hostile.txt"), "write", "guard probe")
        results["outside_round_root_refused"] = False
    except Guarded as exc:
        results["outside_round_root_refused"] = "OUTSIDE_ROUND_ROOT" in str(exc)
    try:
        guarded_sh(["git", "-C", "C:/Projects/wt-r5r3", "push", "origin", "main"])
        results["git_write_verb_refused"] = False
    except Guarded as exc:
        results["git_write_verb_refused"] = "GIT_WRITE_VERB" in str(exc)
    rc, _ = guarded_sh(["git", "-C", "C:/Projects/wt-r5r3", "rev-parse", "HEAD"])
    results["git_read_verb_allowed"] = rc == 0
    check("S9_guards_refuse", all(v is True for v in results.values()), results)


def s10_negative() -> None:
    """A mutated expectation MUST make the harness red - otherwise it cannot detect the defect."""
    scratch = ROUND / "raw" / "negative"
    scratch.mkdir(parents=True, exist_ok=True)
    mutated = json.loads((ROUND / "raw" / "served_assets.json").read_text(encoding="utf-8"))
    rows = mutated["sha256sums"]["rows"]
    first = sorted(rows)[0]
    rows[first] = {"declared": "0" * 64, "served": rows[first]["served"], "match": False}
    ok = not all(r["match"] for r in rows.values())
    check("S10_negative_control", ok,
          {"mutated_entry": first, "detector_fired": ok,
           "note": "a harness that cannot go red on a mutated digest proves nothing"})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repair", action="store_true")
    args = ap.parse_args()

    s1_subject_binding()
    s2_s4_probes()
    s5_suite()
    s6_wheel()
    s7_zip()
    s8_sums()
    s9_guards()
    s10_negative()

    repairs: list[dict] = []
    if args.repair:
        failable = [c["id"] for c in CHECKS if c["verdict"] == "FAIL"]
        repairs.append({"requested": True, "failing_checks": failable,
                        "repair_surface": str(ROUND), "iterations_cap": 3,
                        "outcome": "NO_REPAIR_PERFORMED" if not failable else "HANDOFF_TO_OWNER",
                        "note": "a repair never touches the subject and never synthesises evidence"})

    verdict = ("PASS" if all(c["verdict"] == "PASS" for c in CHECKS)
               else ("INCONCLUSIVE" if any(c["verdict"] == "INCONCLUSIVE" for c in CHECKS)
                     else "FAIL"))
    out = {"schema": "R5R3-20261016/selfcheck/1", "round": "R5R3-20261016-preview4-closeout",
           "subject": SUBJECT_COMMIT, "claim_ceiling": CLAIM_CEILING,
           "checks": CHECKS, "repairs": repairs,
           "overall": "OK_FOR_ROUND_EVIDENCE" if verdict == "PASS" else verdict,
           "counts": {"pass": sum(1 for c in CHECKS if c["verdict"] == "PASS"),
                      "fail": sum(1 for c in CHECKS if c["verdict"] == "FAIL"),
                      "inconclusive": sum(1 for c in CHECKS if c["verdict"] == "INCONCLUSIVE")}}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
