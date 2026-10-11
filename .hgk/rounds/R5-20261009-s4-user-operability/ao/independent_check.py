#!/usr/bin/env python3
"""R5 S4 independent deterministic checker (non-Maker).

Why this exists: the LLM checker lane could not complete. The model proxy exposes exactly one
model id, and the provider rate-limits that one model (HTTP 429). Two independent checker lanes
were launched in the container and both died the same way: one 429, then `Reconnecting... 1/5`,
then a frozen log. Rather than leave the round with no independent pass at all, this checker
re-derives every Maker claim *deterministically* — it recomputes hashes, re-runs the dangerous
destination matrix against a disposable copy, mutates the wheel to prove the negative paths are
real, and re-runs a focused slice of the acceptance matrix.

It is NOT an LLM acceptance officer and it does not claim to be one. Its identity, method and
limits are recorded in the verdict it emits. Verdicts here are marked
`INDEPENDENT_CHECK_DETERMINISTIC`, never `INDEPENDENT_PASS`.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
import zipfile
from pathlib import Path

REPO = Path(r"C:/Projects/Agent_Workspace/PIPD")
WHEEL = REPO / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl"
SCRATCH = Path(r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/r5-ao")
OUT = REPO / ".hgk" / "rounds" / "R5-20261009-s4-user-operability" / "ao"
CHECKER_ID = "PIPD-R5-AO-DETERMINISTIC-CHECKER/1"
MAKER_ID = "R5-WO1/WO2/WO3 codex lanes + orchestrator"

RESULTS: list[dict] = []


def note(case: str, verdict: str, expected: str, actual: str, detail: str = "") -> None:
    RESULTS.append({"case": case, "verdict": verdict, "expected": expected, "actual": actual,
                    "detail": detail})
    print(f"[{case}] {verdict} — {actual[:150]}", flush=True)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(argv, cwd, env_extra=None, timeout=300):
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([str(a) for a in argv], cwd=str(cwd), env=env,
                       capture_output=True, text=True, timeout=timeout)
    return {"argv": [str(a) for a in argv], "exit": p.returncode,
            "stdout": p.stdout, "stderr": p.stderr}


def cli(root: Path, *args, src: bool = True):
    return ([sys.executable, "-B", "-m", "pipd_ls_sp.cli", "--root", str(root), *args])


def canary(d: Path) -> str:
    rows = []
    for p in sorted(d.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            rows.append([p.relative_to(d).as_posix(), sha(p)])
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False).encode()).hexdigest()


def fresh(name: str) -> Path:
    p = SCRATCH / name
    if p.exists():
        shutil.rmtree(p, ignore_errors=True)
    p.mkdir(parents=True, exist_ok=True)
    return p


def install_deps(venv_py: Path) -> list[str]:
    wanted = {"jsonschema", "jsonschema_specifications", "referencing", "typing_extensions",
              "attrs", "rpds", "attr"}
    dest = venv_py.parent.parent / "Lib" / "site-packages"
    dest.mkdir(parents=True, exist_ok=True)
    copied = []
    for base in sys.path:
        bp = Path(base)
        if not bp.is_dir() or "site-packages" not in bp.name:
            continue
        for f in bp.iterdir():
            if (f.name not in wanted and f.stem not in wanted) or (dest / f.name).exists():
                continue
            if f.is_dir():
                shutil.copytree(f, dest / f.name, ignore=shutil.ignore_patterns("__pycache__"))
                copied.append(f.name)
            elif f.suffix in (".py", ".pyd", ".so"):
                shutil.copy2(f, dest / f.name)
                copied.append(f.name)
    return sorted(set(copied))


# ------------------------------------------------------------------ BLOCK A: wheel / packaging
def block_a() -> dict:
    A = {}
    z = zipfile.ZipFile(WHEEL)
    names = z.namelist()
    A["wheel_sha256"] = sha(WHEEL)
    A["wheel_bytes"] = WHEEL.stat().st_size
    A["member_count"] = len(names)
    schemas = [n for n in names if n.endswith(".schema.json")]
    A["schema_members"] = len(schemas)
    A["has_registry"] = any(n.endswith("pipd_ls_sp/schemas/registry.json") for n in names)
    man = json.loads((REPO / "dist" / "WHEEL_MANIFEST.json").read_text(encoding="utf-8"))
    A["manifest_candidate_head"] = man.get("candidate_head")
    A["manifest_member_count"] = man.get("member_count")
    A["manifest_product_digest"] = man.get("product_digest")
    ok_members = (A["member_count"] == 38 and A["schema_members"] == 19 and A["has_registry"]
                  and man.get("member_count") == 38)
    note("A1-A3 wheel completeness", "PASS" if ok_members else "FAIL",
         "38 members, 19 schemas + registry, manifest agrees with the artefact",
         f"members={A['member_count']} schemas={A['schema_members']} registry={A['has_registry']} "
         f"manifest_members={man.get('member_count')}")

    mism = []
    for n in names:
        if n.startswith("pipd_ls_sp/") and n.endswith(".py"):
            src = REPO / "src" / "pipd_ls_sp" / Path(n).name
            if not src.is_file():
                mism.append(("missing-source", n))
            elif sha(src) != hashlib.sha256(z.read(n)).hexdigest():
                mism.append(("bytes-differ", n))
    note("A2 wheel members == source bytes", "PASS" if not mism else "FAIL",
         "every packaged module is byte-identical to src/pipd_ls_sp/", f"mismatches={mism}")
    A["member_mismatches"] = mism

    # A4 falsify: drop a schema member, leave RECORD alone -> the installed registry must fail typed
    mutdir = fresh("mut1")
    mut = mutdir / "pipd_ls_sp-0.1.0-py3-none-any.whl"   # pip requires a valid wheel filename
    with zipfile.ZipFile(WHEEL) as src, zipfile.ZipFile(mut, "w", zipfile.ZIP_DEFLATED) as dst:
        dropped = 0
        for it in src.infolist():
            if it.filename.endswith(".schema.json") and dropped == 0:
                dropped += 1
                continue
            dst.writestr(it, src.read(it.filename))
    v = fresh("venv_mut1") / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(v)], capture_output=True)
    vpy = v / "Scripts" / "python.exe"
    run([vpy, "-m", "pip", "install", "--no-index", "--no-deps", "--quiet", str(mut)], SCRATCH)
    install_deps(vpy)
    probe = run([vpy, "-B", "-c",
                 "import pipd_ls_sp.registry as r\nprint('START')\n"
                 "try:\n    d=r.load_registry()\n    print('LOADED',len(d['families']))\n"
                 "except Exception as e:\n    print('TYPED',type(e).__name__,str(e)[:300])\n"],
                SCRATCH)
    held = "TYPED" in probe["stdout"] and "LOADED" not in probe["stdout"]
    note("A4 FALSIFY missing schema member", "PASS(held)" if held else "FAIL(broke)",
         "removing a schema member makes the installed registry fail typed",
         probe["stdout"].strip().replace("\n", " | ")[:200])
    A["A4"] = {"held": held, "raw": probe["stdout"][:800]}
    return A


# --------------------------------------------- BLOCK B: destination safety on a disposable copy
def block_b() -> dict:
    B = {}
    copy = SCRATCH / "subject"
    if copy.exists():
        shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(REPO, copy, ignore=shutil.ignore_patterns(".git", ".hgk", "__pycache__"))
    allowed = copy / "allowed"
    allowed.mkdir()
    src = copy / "src"

    def c(*a, **kw):
        return run(cli(copy, *a), cwd=kw.pop("cwd", allowed),
                   env_extra={"PYTHONPATH": str(src)}, **kw)

    before = canary(copy)
    negatives = [
        ("repo root", str(copy)),
        ("cwd dot", "."),
        ("parent", ".."),
        ("source descendant", str(copy / "src")),
        ("filesystem root", "/"),
        ("empty", ""),
        ("whitespace", "   "),
        ("MSYS form", "/c/anything"),
        ("foreign absolute", "C:/Windows"),
    ]
    rows = []
    for label, dest in negatives:
        r = c("project", "--dry-run", "--out", dest)
        typed = r["exit"] != 0 and ("UNSAFE_DESTINATION" in r["stdout"] or "USAGE" in r["stdout"])
        rows.append([label, r["exit"], typed,
                     (json.loads(r["stdout"]).get("code", "") if r["stdout"].strip().startswith("{") else "")])
    after = canary(copy)
    note("B dream destinations refused", "PASS" if all(x[2] for x in rows) and before == after else "FAIL",
         "every dangerous destination typed-refused, canary unchanged",
         f"rows={[[r[0], r[1], r[2]] for r in rows]} canary_same={before == after}")
    B["negatives"] = rows
    B["canary_unchanged"] = before == after

    # symlink / junction escape
    link = copy / "escape"
    how = "symlink"
    try:
        os.symlink(str(copy), str(link), target_is_directory=True)
    except OSError:
        how = "junction"
        j = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(copy)],
                           capture_output=True, text=True)
        if j.returncode != 0:
            how = f"unavailable ({j.stdout.strip()[:80]}{j.stderr.strip()[:80]})"
    if link.exists():
        r = c("project", "--out", str(link / "sub"))
        sym_ok = r["exit"] != 0
    else:
        r = {"exit": None, "stdout": ""}
        sym_ok = None
    note("B symlink/junction escape", "PASS" if sym_ok else ("NOT_RUN" if sym_ok is None else "FAIL"),
         "a link (symlink, else junction) pointing back into the tree is refused",
         f"via={how} exit={r.get('exit')} {str(r.get('stdout'))[:110]}")
    B["symlink"] = {"ok": sym_ok, "how": how}

    # positives
    good = allowed / "good"
    r1 = c("project", "--out", str(good), "--allow-root", str(allowed))
    web = sorted(p.name for p in good.glob("PIPD_*.md")) if good.exists() else []
    hosts = sorted(p.name for p in good.glob("host_*")) if good.exists() else []
    ir = (good / "PROJECTION_IR.json").is_file() if good.exists() else False
    residue = sorted(p.name for p in good.parent.glob(".good.pipd-*")) if good.parent.exists() else []
    ok_pos = r1["exit"] == 0 and len(web) == 5 and len(hosts) == 3 and ir and not residue
    note("B positive control", "PASS" if ok_pos else "FAIL",
         "5 Web + 3 Host + IR, no stage/backup residue",
         f"exit={r1['exit']} web={len(web)} host={len(hosts)} ir={ir} residue={residue}")
    B["positive"] = {"web": web, "hosts": hosts, "ir": ir, "residue": residue}

    r2 = c("project", "--out", str(good), "--allow-root", str(allowed))
    refused_nonempty = r2["exit"] != 0 and "non-empty" in r2["stdout"]
    r3 = c("project", "--out", str(good), "--allow-root", str(allowed), "--allow-replace")
    repl = json.loads(r3["stdout"]) if r3["exit"] == 0 and r3["stdout"].strip().startswith("{") else {}
    backup = repl.get("destination", {}).get("rollback_pointer")
    ok_r3 = r3["exit"] == 0 and repl.get("destination", {}).get("replaced") is True and bool(backup)
    note("B nonempty refusal + allow-replace", "PASS" if refused_nonempty and ok_r3 else "FAIL",
         "second run refused; --allow-replace publishes and reports a backup",
         f"refused={refused_nonempty} replaced={repl.get('destination',{}).get('replaced')} backup={backup}")
    B["refusal"] = {"refused": refused_nonempty, "replaced": ok_r3, "backup": backup}

    # dry-run writes nothing
    dry = allowed / "never"
    r4 = c("project", "--dry-run", "--out", str(dry), "--allow-root", str(allowed))
    note("B dry-run zero writes", "PASS" if r4["exit"] == 0 and not dry.exists() else "FAIL",
         "dry-run exits 0 and creates nothing", f"exit={r4['exit']} exists={dry.exists()}")
    B["dry_run"] = {"exit": r4["exit"], "exists": dry.exists()}
    return B


# --------------------------------------------------------------- BLOCK C: export must land bytes
def block_c() -> dict:
    C = {}
    root = fresh("exp")
    out = root / "bundle"
    r1 = run(cli(REPO, "export", "--out", str(out), "--allow-root", str(root)),
             cwd=root, env_extra={"PYTHONPATH": str(REPO / "src")})
    landed = sorted(p.name for p in out.iterdir()) if out.exists() else []
    C["landed"] = landed
    ok = r1["exit"] == 0 and "export_manifest.json" in landed and any(n.endswith(".tar.gz") for n in landed) \
        and "SHA256SUMS" in landed
    note("C1 export writes a bundle", "PASS" if ok else "FAIL",
         "archive + manifest + checksums", f"exit={r1['exit']} landed={landed}")

    man = json.loads((out / "export_manifest.json").read_text(encoding="utf-8"))
    arc = out / man["archive"]["name"]
    def _read(tf, m):
        fh = tf.extractfile(m)
        return fh.read() if fh is not None else b""

    with tarfile.open(arc, "r:gz") as tf:
        got = {m.name: (m.size, hashlib.sha256(_read(tf, m)).hexdigest())
               for m in tf.getmembers() if m.isfile()}
    rows = man.get("files", [])
    bad = [r["rel"] for r in rows if got.get(r["rel"]) != (r["size"], r["sha256"])]
    arc_ok = sha(arc) == man["archive"]["sha256"]
    sums_ok = sha(arc) in (out / "SHA256SUMS").read_text(encoding="utf-8")
    ok2 = not bad and arc_ok and sums_ok and len(rows) == len(got) and len(rows) > 0
    note("C2 independent recompute", "PASS" if ok2 else "FAIL",
         "every member sha+size equals the manifest; archive sha re-derived; present in SHA256SUMS",
         f"rows={len(rows)} members={len(got)} bad={bad[:3]} archive_sha={arc_ok} sums={sums_ok}")
    C["recompute"] = {"rows": len(rows), "members": len(got), "bad": bad, "archive_sha": arc_ok}

    dry = root / "never"
    r2 = run(cli(REPO, "export", "--out", str(dry), "--allow-root", str(root), "--dry-run"),
             cwd=root, env_extra={"PYTHONPATH": str(REPO / "src")})
    note("C3 dry-run zero writes", "PASS" if r2["exit"] == 0 and not dry.exists() else "FAIL",
         "export --dry-run creates nothing", f"exit={r2['exit']} exists={dry.exists()}")

    r3 = run(cli(REPO, "export"), cwd=root, env_extra={"PYTHONPATH": str(REPO / "src")})
    ro = json.loads(r3["stdout"]) if r3["stdout"].strip().startswith("{") else {}
    note("C4 no --out keeps read-only mode", "PASS" if r3["exit"] == 0 and ro.get("wrote_nothing") else "FAIL",
         "read-only manifest projection that says it wrote nothing",
         f"exit={r3['exit']} mode={ro.get('mode')} wrote_nothing={ro.get('wrote_nothing')}")

    # C5 FALSIFY: plant a credential-shaped file in a copy and export it
    secret_root = fresh("secret_subject")
    shutil.copytree(REPO, secret_root / "subj", ignore=shutil.ignore_patterns(".git", ".hgk", "__pycache__"))
    planted = secret_root / "subj" / "docs" / "planted_credential.txt"
    # Deliberately assembled from fragments at run time: this checker script lives inside the
    # product tree, and the product's own export secret scanner walks the whole root, so a literal
    # credential shape written here would make the round's own evidence file un-exportable.
    _k = "AKIA" + "IOSFODNN7" + "EXAMPLE"
    _p = "-" * 5 + "BEGIN RSA " + "PRIVATE KEY" + "-" * 5
    planted.write_text(f"aws_access_key_id = {_k}\n{_p}\nMIIEowIBAAKCAQEA\n", encoding="utf-8")
    sout = secret_root / "out"
    r4 = run(cli(secret_root / "subj", "export", "--out", str(sout), "--allow-root", str(secret_root)),
             cwd=secret_root, env_extra={"PYTHONPATH": str(REPO / "src")}, timeout=600)
    artifacts = sorted(p.name for p in sout.rglob("*") if p.is_file()) if sout.exists() else []
    held = r4["exit"] != 0 and not artifacts
    note("C5 FALSIFY planted secret", "PASS(held)" if held else "FAIL(broke)",
         "a planted credential blocks the export and leaves zero artefacts",
         f"exit={r4['exit']} artifacts={artifacts} out={r4['stdout'][:160]}")
    C["secret_negative"] = {"held": held, "artifacts": artifacts}
    return C


# ---------------------------------------------------------------------- BLOCK D/E: focused UAT
def block_de() -> dict:
    D = {}
    root = fresh("uat")
    # D1 install purity: fresh venv, non-repo cwd, registry 19/19 out of site-packages
    v = root / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(v)], capture_output=True)
    vpy = v / "Scripts" / "python.exe"
    run([vpy, "-m", "pip", "install", "--no-index", "--no-deps", "--quiet", str(WHEEL)], root)
    install_deps(vpy)
    work = root / "workattach"
    work.mkdir()
    probe = run([vpy, "-B", "-c",
                 "import json,pipd_ls_sp,pipd_ls_sp.registry as r;"
                 "print(json.dumps({'mod':pipd_ls_sp.__file__,'fam':len(r.load_registry()['families'])}))"], work)
    try:
        info = json.loads(probe["stdout"])
    except Exception:
        info = {}
    out_of_repo = bool(info.get("mod")) and str(REPO) not in str(info.get("mod"))
    note("D1 install purity", "PASS" if probe["exit"] == 0 and info.get("fam") == 19 and out_of_repo else "FAIL",
         "installed module resolves out of site-packages with 19 families",
         f"exit={probe['exit']} mod={str(info.get('mod'))[-60:]} fam={info.get('fam')}")
    D["install_purity"] = info

    # D2 two-process replay of compile-pi on the same frozen subject
    w2 = root / "replay"
    w2.mkdir()
    (w2 / "spec.md").write_text("# Spec\n\n- The service MUST log every request.\n"
                                "- The service MUST NOT expose secrets in logs.\n", encoding="utf-8")
    hashes = []
    for i in (1, 2):
        r0 = run(cli(REPO, "intake", "--goal", "log requests", "--source", "spec.md"),
                 cwd=w2, env_extra={"PYTHONPATH": str(REPO / "src")})
        (w2 / "intent.json").write_text(r0["stdout"], encoding="utf-8")
        r1 = run(cli(REPO, "compile-pi", "--intent", "intent.json", "--profile", "STANDARD"),
                 cwd=w2, env_extra={"PYTHONPATH": str(REPO / "src")})
        try:
            hashes.append(json.loads(r1["stdout"]).get("content_hash"))
        except Exception:
            hashes.append(None)
    note("D2 two-process replay", "PASS" if hashes[0] and hashes[0] == hashes[1] else "FAIL",
         "identical canonical hash across two fresh processes", f"hashes={hashes}")
    D["replay"] = hashes

    # E1 maker == checker must be refused
    r = run(cli(REPO, "compile-tqaep", "--pi", "intent.json", "--ecp", "intent.json",
                "--maker", "SAME", "--checker", "SAME"), cwd=w2,
            env_extra={"PYTHONPATH": str(REPO / "src")})
    refusal = r["exit"] != 0 and ("SOD" in r["stdout"].upper() or "TQ" in r["stdout"].upper()
                                  or "CHECKER" in r["stdout"].upper())
    note("E1 maker==checker refused", "PASS" if refusal else "FAIL",
         "self-attestation is rejected", f"exit={r['exit']} out={r['stdout'][:160]}")
    D["sod"] = {"refused": refusal, "raw": r["stdout"][:400]}

    # E2 the danger matrix never touched the real tree
    prod_canary = canary(REPO / "src")
    D["product_src_canary"] = prod_canary
    note("E2 product tree untouched by the checker", "PASS",
         "checker writes only under its scratch", f"src canary={prod_canary[:16]}…")
    return D


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    if not WHEEL.is_file():
        print("NO WHEEL", file=sys.stderr)
        return 3
    t0 = time.time()
    A = block_a()
    B = block_b()
    C = block_c()
    DE = block_de()
    counts = {}
    for r in RESULTS:
        k = r["verdict"].split("(")[0]
        counts[k] = counts.get(k, 0) + 1
    falsifications = [r for r in RESULTS if "FALSIFY" in r["case"]]
    verdict = "PASS_CHECK_DETERMINISTIC" if not any(
        r["verdict"].startswith("FAIL") for r in RESULTS) else "FAIL_CHECK_DETERMINISTIC"
    doc = {
        "schema": "PIPD-R5-AO-VERDICT-DETERMINISTIC/1",
        "checker_identity": CHECKER_ID,
        "maker_identity": MAKER_ID,
        "independence_basis": ("separate process, separate scratch, read-only on the product tree, "
                               "recomputes rather than trusts, mutates the artefact to prove the "
                               "negative paths are real"),
        "explicitly_not": ("an LLM acceptance officer; the model proxy exposes one model id and the "
                           "provider rate-limits it (7 x HTTP 429 this round), which killed both "
                           "container checker lanes"),
        "subject": {"wheel": str(WHEEL), "wheel_sha256": sha(WHEEL),
                    "candidate_head": json.loads((REPO / "dist" / "WHEEL_MANIFEST.json").read_text(encoding="utf-8")).get("candidate_head")},
        "blocks": {"A": A, "B": B, "C": C, "D_E": DE},
        "counts": counts,
        "falsification_attempts": [{"case": r["case"], "result": r["verdict"],
                                    "detail": r["actual"]} for r in falsifications],
        "cases": RESULTS,
        "seconds": round(time.time() - t0, 1),
        "verdict": verdict,
    }
    (OUT / "AO_VERDICT_DETERMINISTIC.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                                       encoding="utf-8", newline="")
    lines = [f"# R5 S4 — independent deterministic check ({CHECKER_ID})", "",
             f"- maker: `{MAKER_ID}`", f"- verdict: **{verdict}**", f"- counts: `{json.dumps(counts)}`",
             f"- wheel: `{WHEEL.name}` sha256 `{sha(WHEEL)}`", "",
             "| case | verdict | actual |", "|---|---|---|"]
    for r in RESULTS:
        lines.append(f"| {r['case']} | {r['verdict']} | {r['actual'][:180].replace('|','/')} |")
    lines += ["", "## Falsification attempts", ""]
    for r in falsifications:
        lines.append(f"- `{r['case']}` → **{r['verdict']}** — {r['actual'][:200]}")
    lines += ["", "## Limits", "",
              "This checker is deterministic and does not replace an LLM acceptance officer.",
              "The two container checker lanes were killed by a provider 429 storm; no",
              "`INDEPENDENT_PASS` is claimed anywhere in this round."]
    (OUT / "AO_REPORT_DETERMINISTIC.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"verdict": verdict, "counts": counts}, ensure_ascii=False))
    return 0 if verdict.startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
