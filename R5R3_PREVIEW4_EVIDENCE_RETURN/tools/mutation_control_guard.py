"""Mutation control for the round's guard, run against the REAL files.

For each mutation the files are backed up, mutated on disk, the focused acceptance command is run,
and the tree is restored from the backup - so the control proves the guard fires without leaving any
trace. A mutation that does NOT turn the guard red is a hole in the guard and is reported as such.

The four mutations correspond to the failure modes an independent checker demonstrated against the
first revision of this guard (a wrong digest inside the download paragraph, an impossible
build-source identity) plus the coverage hole it found in the tuple.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

WT = Path("C:/Projects/wt-r5r3")
ROUND = Path("C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout")
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
README = WT / "README.md"
TUPLE = WT / "docs" / "RELEASE_TUPLE.json"
TESTS = ["tests.test_r5r3_install_route_identity"]

SERVED = "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75"
ZEROS = "0" * 64


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def acceptance_rc() -> int:
    r = subprocess.run([PY, "-B", "-m", "unittest", *TESTS], cwd=str(WT), capture_output=True,
                       text=True, env={"PYTHONPATH": "src", "PATH": __import__("os").environ["PATH"],
                                       "SYSTEMROOT": __import__("os").environ.get("SYSTEMROOT", "")})
    return r.returncode


def mutate(name: str, fn) -> dict:
    backups = {p: p.read_bytes() for p in (README, TUPLE)}
    before = {str(p): sha(p) for p in backups}
    try:
        fn()
        rc = acceptance_rc()
    finally:
        for p, data in backups.items():
            p.write_bytes(data)
    after = {str(p): sha(p) for p in backups}
    return {"mutation": name, "guard_rc": rc, "guard_red": rc != 0,
            "restored": before == after}


def m_route_digest_to_zeros() -> None:
    """The download paragraph's digest is replaced by zeros; the correct digest stays elsewhere.

    The first attempt at this mutation replaced the FIRST occurrence of the digest in the file, which
    sits in a different paragraph (the historical R5Y one) - the guard was right to stay green and the
    probe was wrong. This version locates the paragraph that names the download and mutates inside it.
    """
    text = README.read_text(encoding="utf-8")
    paras = text.split("\n\n")
    hit = False
    for index, para in enumerate(paras):
        if f"releases/download/v0.1.1-preview.4/pipd-ls-sp-public-skills.zip" in para and SERVED in para:
            paras[index] = para.replace(SERVED, ZEROS)
            hit = True
    assert hit, "no paragraph both names the download and carries the served digest"
    README.write_text("\n\n".join(paras), encoding="utf-8")


def m_build_source_not_a_commit() -> None:
    data = json.loads(TUPLE.read_text(encoding="utf-8"))
    for r in data["releases"]:
        if r.get("release_id") == "v0.1.1-preview.4":
            r["build_source_commit"] = "not-a-commit"
    TUPLE.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def m_tuple_drops_a_served_asset() -> None:
    data = json.loads(TUPLE.read_text(encoding="utf-8"))
    for r in data["releases"]:
        if r.get("release_id") == "v0.1.1-preview.4":
            r["served_assets"].pop("PIPD_WEB_FALLBACK.md.sha256", None)
    TUPLE.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def m_unscoped_build_source() -> None:
    data = json.loads(TUPLE.read_text(encoding="utf-8"))
    for r in data["releases"]:
        if r.get("release_id") == "v0.1.1-preview.4":
            r.pop("build_source_scope", None)
    TUPLE.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> int:
    baseline = acceptance_rc()
    rows = [{"mutation": "BASELINE (unmutated tree)", "guard_rc": baseline,
             "guard_red": baseline != 0, "restored": True}]
    for name, fn in (("route-paragraph digest -> zeros", m_route_digest_to_zeros),
                     ("build_source_commit -> not-a-commit", m_build_source_not_a_commit),
                     ("tuple drops PIPD_WEB_FALLBACK.md.sha256", m_tuple_drops_a_served_asset),
                     ("build_source_scope removed", m_unscoped_build_source)):
        rows.append(mutate(name, fn))
    out = {"schema": "R5R3/mutation-control/1",
           "all_mutations_turned_the_guard_red": all(r["guard_red"] for r in rows[1:]),
           "baseline_green": rows[0]["guard_rc"] == 0,
           "tree_restored_after_every_mutation": all(r["restored"] for r in rows),
           "rows": rows}
    (ROUND / "raw" / "mutation_control.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if (out["all_mutations_turned_the_guard_red"] and out["baseline_green"]
                 and out["tree_restored_after_every_mutation"]) else 1


if __name__ == "__main__":
    sys.exit(main())
