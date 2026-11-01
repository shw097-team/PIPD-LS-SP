"""Build candidate patches for the three defects the WP-13 AO found in the tools themselves.

Nothing here is applied to the repos. The copies live under patches/PIPD/ so hotswap.py's
`parents[1]/src` convention still finds patches/PIPD/src, and every patch is emitted as a
unified diff with its sha256 so a reviewer can read the change without running it.

Fixes:
  P1 abi.py      occupant_from_file no longer stamps the caller's Need onto the occupant, so a module
                 that declares its own NEED is actually compared (AO F6: version/name gate unreachable).
  P2 hotswap.py  bind_grant compares the writeset's declared preimages with the bytes on disk (AO F3)
                 and compares issued_at with receipt.started_at instead of bind time (AO F4).
  P3 hotswap.py  NEG stops being a copy of POS: it reports serves_old explicitly (AO F2).
Not fixed here: F1 (issuer is the executor's own key), F5 (assurance_level literal), F8 (clock window)
- those are authority/documentation limits, recorded in REMEDIATION_WP13.md instead of patched quietly.
"""
import hashlib
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
BASE = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "patches"
SRC = {"abi": ROOT / "PIPD" / "src" / "pipd_ls_sp" / "abi.py",
       "hotswap": ROOT / "PIPD" / "tools" / "hotswap.py"}

DST = {"abi": BASE / "PIPD" / "src" / "pipd_ls_sp" / "abi.py",
       "hotswap": BASE / "PIPD" / "tools" / "hotswap.py"}

EDITS = {
    "abi": [(
        '    return Occupant(need=need, impl=getattr(mod, factory)(), origin=str(path))',
        '    declared = getattr(mod, "NEED", None)\n'
        '    if declared is not None and not isinstance(declared, Need):\n'
        '        raise AbiUnsatisfied(\n'
        '            f"{path} declares NEED of type {type(declared).__name__}, expected Need")\n'
        '    # A module that declares its own NEED is checked against the caller\'s need; stamping the\n'
        '    # caller\'s Need here made the version/name gate compare a Need with itself (AO WP-FHS-13 F6).\n'
        '    return Occupant(need=declared if declared is not None else need,\n'
        '                    impl=getattr(mod, factory)(), origin=str(path))',
    )],
    "hotswap": [
        ("def bind_grant(grant_path: Path, entry: Path, candidate: Path, cand_sha: str,\n               verifier: Path) -> tuple[dict, list[str]]:",
         "def bind_grant(grant_path: Path, entry: Path, candidate: Path, cand_sha: str,\n               verifier: Path, started_epoch: float | None = None) -> tuple[dict, list[str]]:"),
        ('        info["issued_before_effect"] = issued <= time.time()',
         '        # compared with receipt.started_at when we have it, not with bind time (AO F4: a grant\n'
         '        # issued after the run started but before this call used to pass)\n'
         '        reference = float(started_epoch) if isinstance(started_epoch, (int, float)) else time.time()\n'
         '        info["ordering_reference"] = ("receipt.started_at"\n'
         '                                      if isinstance(started_epoch, (int, float)) else "bind_time")\n'
         '        info["issued_before_effect"] = issued <= reference'),
        ('    # 4. the grant must name the exact artefact when it names one at all',
         '    # 3b. the writeset\'s declared preimages must match the bytes actually on disk (AO F3: the tool\n'
         '    # never read writeset preimages, so a stale or wrong preimage still bound)\n'
         '    declared = {_norm(w.get("path", "")): (w.get("preimage") or "").strip().lower()\n'
         '                for w in (grant.get("writeset") or []) if isinstance(w, dict)}\n'
         '    info["preimage_checks"] = {}\n'
         '    for label, path_obj in (("entry", entry), ("candidate", candidate)):\n'
         '        want = declared.get(_norm(path_obj))\n'
         '        if not want:\n'
         '            continue\n'
         '        got = hashlib.sha256(Path(path_obj).read_bytes()).hexdigest()\n'
         '        info["preimage_checks"][label] = {"declared": want, "actual": got, "ok": got == want}\n'
         '        if got != want:\n'
         '            problems.append(f"GRANT_PREIMAGE_MISMATCH_{label.upper()}")\n'
         '\n'
         '    # 4. the grant must name the exact artefact when it names one at all'),
        ('    neg = {"identity": pos["identity"], "served": pos["served"],\n           "question": "does the target still serve the old capability?"}',
         '    # NEG reports the fact the question asks for, instead of copying POS["served"] (AO F2)\n'
         '    neg = {"identity_after": pos["identity"],\n'
         '           "serves_old": bool(pos["served"] and pos["identity"] == args.expect_old),\n'
         '           "question": "does the target still serve the old capability?"}'),
        ('    neg_ok = pos["identity"] != args.expect_old',
         '    neg_ok = not neg["serves_old"]'),
        ('    receipt: dict = {"schema": SCHEMA, "root": str(root), "entry": str(entry), "candidate": str(candidate),\n                     "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "steps": []}',
         '    started_epoch = time.time()\n'
         '    receipt: dict = {"schema": SCHEMA, "root": str(root), "entry": str(entry), "candidate": str(candidate),\n'
         '                     "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),\n'
         '                     "started_at_epoch": started_epoch, "steps": []}'),
        ('        info, problems = bind_grant(Path(args.grant), entry, candidate, cand_sha, Path(args.grant_verifier))',
         '        info, problems = bind_grant(Path(args.grant), entry, candidate, cand_sha,\n'
         '                                    Path(args.grant_verifier), started_epoch=started_epoch)'),
    ],
}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


records = {}
for key, src in SRC.items():
    dst = DST[key]
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    text = dst.read_text(encoding="utf-8")
    applied = []
    for old, new in EDITS[key]:
        if old not in text:
            applied.append({"ok": False, "anchor": old[:70]})
            continue
        text = text.replace(old, new, 1)
        applied.append({"ok": True, "anchor": old[:70]})
    dst.write_text(text, encoding="utf-8", newline="\n")
    diff = subprocess.run(["git", "-c", "core.autocrlf=false", "diff", "--no-index", "--no-color",
                           str(src), str(dst)], capture_output=True, text=True)
    patch = BASE / f"{key}.patch"
    patch.write_text(diff.stdout, encoding="utf-8", newline="\n")
    records[key] = {"src": str(src), "src_sha256": sha(src), "dst": str(dst), "dst_sha256": sha(dst),
                    "edits": applied, "all_applied": all(e["ok"] for e in applied),
                    "patch": str(patch), "patch_sha256": sha(patch), "patch_bytes": patch.stat().st_size}

(base := BASE / "PATCH_MANIFEST.json").write_text(
    __import__("json").dumps({"schema": "FHS.R21.WP13.TOOL_PATCHES/1",
                              "note": "candidate patches only; nothing applied to the repos",
                              "records": records}, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8", newline="\n")
print(__import__("json").dumps({k: {"all_applied": v["all_applied"], "patch_bytes": v["patch_bytes"],
                                    "dst_sha256": v["dst_sha256"][:16]} for k, v in records.items()}, indent=1))
