#!/usr/bin/env python3
"""HotSwap with parity — the missing implementation behind WP-FHS-13.

MEASURED 2026-10-31: the delivery specifies HotSwap 81 times (08_TECHNOLOGY_DEFAULT_HOTSWAP.md) and implements it
zero times. Twenty files mention the word and every one of them is a QA repair tool or an officer verify script.
WP-FHS-13 therefore fails on `CAPABILITY_PARITY_NOT_PROVEN`, which is the spec's own first-fail for "熱替代 Issuer
或以選型當 invoke" — proving a swap happened is not the same as proving the new occupant serves and the old one
stopped serving.

This tool does the swap and proves the parity, in that order, on a NAMED target root:

    preimage    snapshot every file under --root with its digest
    bind        the current occupant must be the one we expect (else ERR_OCCUPANT_MISMATCH, no effect)
    stage       copy the candidate beside the target and verify its digest before anything moves
    swap        old -> .prev, staged -> target (os.replace, same volume)
    POS         invoke the NEW occupant; its identity must equal --expect-new
    NEG         invoke the OLD occupant path; it must no longer serve the old identity
    rollback    if POS or NEG fails, restore .prev and verify the preimage byte-for-byte

Exit 0 only when POS and NEG both hold. A swap that cannot demonstrate both is reported as
CAPABILITY_PARITY_NOT_PROVEN and rolled back -- the rollback is not a courtesy, it is part of the refusal.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCHEMA = "PIPD-HOTSWAP-RECEIPT/1"
ERR_OCCUPANT_MISMATCH = "ERR_OCCUPANT_MISMATCH"
ERR_CANDIDATE_DIGEST = "ERR_CANDIDATE_DIGEST"
ERR_PARITY_NOT_PROVEN = "CAPABILITY_PARITY_NOT_PROVEN"
ERR_ROLLBACK_FAILED = "ERR_ROLLBACK_FAILED"
ERR_GRANT_NOT_BOUND = "ERR_GRANT_NOT_BOUND"


def _norm(p) -> str:
    return os.path.normcase(os.path.normpath(str(p)))


def bind_grant(grant_path: Path, entry: Path, candidate: Path, cand_sha: str,
               verifier: Path, started_epoch: float | None = None) -> tuple[dict, list[str]]:
    """Bind the swap to an issuer-signed grant, and refuse when the grant does not cover it.

    The first WP-13 receipt could not answer C5 at all, and the independent checker said why: the only grant in the
    tree was issued 100 seconds AFTER the swap, and its writeset named two files, neither of which was the target.
    The cause was structural — this tool had no way to take a grant — so every swap it performed was, by
    construction, unauthorised. Adding the parameter is the repair; refusing without a covering grant is the
    prevention.

    The signature is NOT re-implemented here: the issuer's own verifier decides it, so there is exactly one opinion
    about what a valid signature is. What this function adds is the consumer's half, which the issuer cannot know:
    does this grant name the file we are about to overwrite, and the artefact we are about to install?
    """
    grant_path = Path(grant_path)
    info: dict = {"path": str(grant_path), "sha256": sha256_file(grant_path)}
    problems: list[str] = []
    try:
        grant = json.loads(grant_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return info, [f"GRANT_UNREADABLE:{exc.__class__.__name__}"]

    info.update({"nonce": grant.get("nonce"), "issued_at": grant.get("issued_at"),
                 "expires_at": grant.get("expires_at"), "subject": grant.get("subject"),
                 "operation": grant.get("operation"), "scope": grant.get("scope"),
                 "policy_epoch": grant.get("policy_epoch")})

    # 1. the issuer's verifier
    if not Path(verifier).is_file():
        problems.append("GRANT_VERIFIER_MISSING")
    else:
        proc = subprocess.run([sys.executable, str(verifier), "verify", "--grant", str(grant_path)],
                              capture_output=True, text=True, errors="replace", encoding="utf-8")
        info["issuer_verifier_exit"] = proc.returncode
        try:
            info["issuer_verifier"] = json.loads(proc.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            info["issuer_verifier"] = {"raw": (proc.stdout or proc.stderr or "")[-300:]}
        if proc.returncode != 0:
            for p in (info["issuer_verifier"] or {}).get("problems") or ["GRANT_REFUSED_BY_ISSUER"]:
                problems.append(p)

    # 2. ordering: an authorisation that postdates the effect authorises nothing
    issued = grant.get("issued_at")
    info["issued_before_effect"] = None
    if isinstance(issued, (int, float)):
        # compared with receipt.started_at when we have it, not with bind time (AO F4: a grant
        # issued after the run started but before this call used to pass)
        reference = float(started_epoch) if isinstance(started_epoch, (int, float)) else time.time()
        info["ordering_reference"] = ("receipt.started_at"
                                      if isinstance(started_epoch, (int, float)) else "bind_time")
        info["issued_before_effect"] = issued <= reference
        if not info["issued_before_effect"]:
            problems.append("GRANT_POSTDATES_EFFECT")

    # 3. coverage: the entry we overwrite, and the artefact we install
    ws = {_norm(w.get("path", "")) for w in (grant.get("writeset") or []) if isinstance(w, dict)}
    info["writeset_paths"] = sorted(ws)
    info["covers_entry"] = _norm(entry) in ws
    info["covers_candidate"] = _norm(candidate) in ws
    if not info["covers_entry"]:
        problems.append("GRANT_WRITESET_EXCLUDES_TARGET")
    if not info["covers_candidate"]:
        problems.append("GRANT_WRITESET_EXCLUDES_CANDIDATE")

    # 3b. the writeset's declared preimages must match the bytes actually on disk (AO F3: the tool
    # never read writeset preimages, so a stale or wrong preimage still bound)
    declared = {_norm(w.get("path", "")): (w.get("preimage") or "").strip().lower()
                for w in (grant.get("writeset") or []) if isinstance(w, dict)}
    info["preimage_checks"] = {}
    for label, path_obj in (("entry", entry), ("candidate", candidate)):
        want = declared.get(_norm(path_obj))
        if not want:
            continue
        got = hashlib.sha256(Path(path_obj).read_bytes()).hexdigest()
        info["preimage_checks"][label] = {"declared": want, "actual": got, "ok": got == want}
        if got != want:
            problems.append(f"GRANT_PREIMAGE_MISMATCH_{label.upper()}")

    # 3c. the grant's operation must belong to THIS effect class.
    DEV_OPERATIONS = {"install_occupant", "repo_write", "repo_patch"}
    op = (grant.get("operation") or "").strip()
    info["operation"] = op
    if op and op not in DEV_OPERATIONS:
        problems.append("GRANT_EFFECT_MISMATCH")

    # 3d. a receipt is single-use: burned against this exact (entry, candidate) pair.
    ledger = Path(os.environ.get("HGK_CONSUMED_LEDGER", str(Path.home() / ".hgk-consumed.jsonl")))
    key = {"nonce": grant.get("nonce"), "entry": _norm(entry), "candidate": _norm(candidate)}
    info["receipt_key"] = key
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            try:
                prior = json.loads(line)
            except json.JSONDecodeError:
                continue
            if prior.get("nonce") == key["nonce"] and prior.get("entry") == key["entry"]:
                problems.append("GRANT_ALREADY_CONSUMED")
                info["consumed_by"] = prior
                break

    # 3e. one live ECP per subject: a second grant for a subject that already has a consumed receipt
    # must be refused until the first one is closed (AO/edge B4: two active ECPs, no selector).
    subj = (grant.get("subject") or "").strip()
    info["subject"] = subj
    if subj and ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            try:
                prior = json.loads(line)
            except json.JSONDecodeError:
                continue
            if prior.get("subject") == subj and not prior.get("closed"):
                problems.append("ECP_MULTIPLE_ACTIVE")
                info["competing_ecp"] = prior
                break

    # 4. the grant must name the exact artefact when it names one at all
    named = (grant.get("candidate_sha256") or "").strip().lower()
    info["candidate_sha_named"] = named or None
    info["candidate_sha_matches"] = (not named) or named == cand_sha.lower()
    if not info["candidate_sha_matches"]:
        problems.append("GRANT_CANDIDATE_SHA_MISMATCH")

    info["problems"] = problems
    if not problems:
        _consume(grant, entry, candidate)
    return info, problems


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not root.exists():
        return out
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in ("__pycache__", ".git"))
        for fn in sorted(filenames):
            p = Path(dirpath) / fn
            try:
                out[str(p.relative_to(root)).replace("\\", "/")] = sha256_file(p)
            except OSError:
                out[str(p.relative_to(root)).replace("\\", "/")] = "UNREADABLE"
    return out


def invoke(entry: Path, timeout: int = 60) -> dict:
    """Ask the occupant who it is. The occupant is a script that prints its own identity token."""
    if not entry.exists():
        return {"served": False, "identity": None, "why": "absent"}
    try:
        res = subprocess.run([sys.executable, str(entry), "--identity"], capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"served": False, "identity": None, "why": f"{type(exc).__name__}: {exc}"}
    line = (res.stdout or "").strip().splitlines()
    identity = line[-1].strip() if line else None
    return {"served": res.returncode == 0, "identity": identity, "exit": res.returncode,
            "stderr_tail": (res.stderr or "")[-300:]}



def probe_through_abi(entry: Path, need: str, method: str) -> dict:
    """POS/NEG at the CONSUMER, not at the file.

    `invoke()` runs the entry as a separate process, which proves that *some* entry point answers differently. The
    work package asks whether the consumer the system actually calls reaches the new occupant. That is a different
    question and it has a different failure mode: a consumer that binds once keeps serving the old implementation
    after a perfect file swap. Going through the ABI makes the consumer the subject.
    """
    src = Path(__file__).resolve().parents[1] / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    from pipd_ls_sp.abi import ABI_VERSION, Need, make_consumer
    consumer = make_consumer(Need(need, ABI_VERSION, (method,)), entry)
    served = consumer.serves(method)
    return {"identity": served.get("value") if served.get("ok") else None,
            "served": bool(served.get("ok")), "via": "abi-consumer",
            "origin": served.get("origin"), "code": served.get("code")}



def _consume(grant: dict, entry, candidate) -> None:
    """Burn the receipt so a second bind of the same grant on the same target cannot pass."""
    ledger = Path(os.environ.get("HGK_CONSUMED_LEDGER", str(Path.home() / ".hgk-consumed.jsonl")))
    row = {"nonce": grant.get("nonce"), "subject": (grant.get("subject") or ""),
           "entry": _norm(entry), "candidate": _norm(candidate),
           "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="swap an occupant and prove POS/NEG parity")
    ap.add_argument("--root", required=True, help="named target root holding the current occupant")
    ap.add_argument("--entry", default="occupant.py", help="the occupant entry file inside --root")
    ap.add_argument("--candidate", required=True, help="the replacement occupant file")
    ap.add_argument("--expect-old", required=True, help="identity the current occupant must report")
    ap.add_argument("--need", default=None, help="resolve POS/NEG through the ABI consumer instead of the entry process")
    ap.add_argument("--method", default="identity")
    ap.add_argument("--expect-new", required=True, help="identity the candidate must report after the swap")
    ap.add_argument("--out", default=None, help="receipt path")
    ap.add_argument("--grant", default=None,
                    help="issuer-signed grant that must cover this swap; without one the swap is refused")
    ap.add_argument("--grant-verifier", default=os.environ.get(
        "HGK_GRANT_VERIFIER", r"C:\Projects\Agent_Workspace\HG-KSEOS\scripts\issue_grant.py"),
        help="the issuer's own verifier; signature checking is not re-implemented here")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    entry = root / args.entry
    candidate = Path(args.candidate).resolve()
    started_epoch = time.time()
    receipt: dict = {"schema": SCHEMA, "root": str(root), "entry": str(entry), "candidate": str(candidate),
                     "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                     "started_at_epoch": started_epoch, "steps": []}

    def finish(code: str | None, ok: bool, why: str) -> int:
        receipt.update({"code": None if ok else code, "ok": ok, "why": why,
                        "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps({k: receipt[k] for k in ("ok", "code", "why", "pos", "neg") if k in receipt},
                         ensure_ascii=False))
        return 0 if ok else 1

    pre = snapshot(root)
    receipt["preimage"] = {"files": len(pre), "digest": hashlib.sha256(
        json.dumps(sorted(pre.items())).encode()).hexdigest()}

    _probe = (lambda q: probe_through_abi(q, args.need, args.method)) if args.need else invoke
    before = _probe(entry)
    receipt["before"] = before
    if not before["served"] or before["identity"] != args.expect_old:
        return finish(ERR_OCCUPANT_MISMATCH, False,
                      f"the occupant reports {before.get('identity')!r}, expected {args.expect_old!r}; nothing moved")

    if not candidate.is_file():
        return finish(ERR_CANDIDATE_DIGEST, False, f"candidate is not a file: {candidate}")
    cand_sha = sha256_file(candidate)
    receipt["candidate_sha256"] = cand_sha

    # The grant is bound BEFORE anything moves, and a missing or non-covering grant is a refusal, not a warning.
    # `--grant` is optional so that fixture-level parity tests can still run, but any swap that is claimed as
    # authorised must show this block in its receipt, and `--require-grant` makes its absence fatal.
    if args.grant:
        info, problems = bind_grant(Path(args.grant), entry, candidate, cand_sha,
                                    Path(args.grant_verifier), started_epoch=started_epoch)
        receipt["grant"] = info
        if problems:
            return finish(ERR_GRANT_NOT_BOUND, False,
                          f"the grant does not cover this swap: {problems}; nothing moved")
        receipt["steps"].append("grant_bound")
    elif os.environ.get("HGK_REQUIRE_GRANT") == "1":
        return finish(ERR_GRANT_NOT_BOUND, False,
                      "no --grant given and HGK_REQUIRE_GRANT=1; an unauthorised swap is not performed")
    else:
        receipt["grant"] = {"bound": False,
                            "why": "no --grant given; this receipt cannot answer a grant clause"}

    if args.dry_run:
        return finish(None, True, "dry run: occupant bound and candidate hashed; nothing moved")

    prev = root / (args.entry + ".prev")
    staged = root / (args.entry + ".staged")
    try:
        shutil.copyfile(candidate, staged)
        if sha256_file(staged) != cand_sha:
            return finish(ERR_CANDIDATE_DIGEST, False, "the staged copy does not match the candidate digest")
        if prev.exists():
            prev.unlink()
        os.replace(entry, prev)
        os.replace(staged, entry)
        receipt["steps"].append("swapped")
    except OSError as exc:
        for p in (staged,):
            if p.exists():
                p.unlink()
        return finish(ERR_PARITY_NOT_PROVEN, False, f"swap failed before parity: {exc}")

    # POS and NEG are two properties of the SAME post-swap entry, and they are different questions:
    #   POS  does the target now serve the new capability?
    #   NEG  has the target stopped serving the old one?
    # A first version invoked the parked `.prev` file and called it NEG. That measured whether an old artefact can
    # still be executed from disk -- which it can, and should, since rollback depends on it. The clause is about
    # what the TARGET serves, not about what is still lying around.
    pos = _probe(entry)
    receipt["pos"] = pos
    # NEG reports the fact the question asks for, instead of copying POS["served"] (AO F2)
    neg = {"identity_after": pos["identity"],
           "serves_old": bool(pos["served"] and pos["identity"] == args.expect_old),
           "question": "does the target still serve the old capability?"}
    receipt["neg"] = neg
    receipt["control"] = {"identity": before["identity"], "served": before["served"],
                          "question": "did the target serve the old capability BEFORE the swap? (control)"}

    pos_ok = pos["served"] and pos["identity"] == args.expect_new
    neg_ok = not neg["serves_old"]
    if pos_ok and neg_ok:
        prev.unlink()
        receipt["rollback"] = "not needed"
        return finish(None, True,
                      f"POS: new occupant serves as {args.expect_new}; NEG: the old occupant no longer serves "
                      f"{args.expect_old}")

    # Parity failed -> restore the preimage. A refused swap must leave the world as it found it.
    try:
        if entry.exists():
            entry.unlink()
        os.replace(prev, entry)
        after = snapshot(root)
        restored = after == pre
        receipt["rollback"] = {"restored": restored, "preimage_files": len(pre), "after_files": len(after)}
        if not restored:
            return finish(ERR_ROLLBACK_FAILED, False,
                          f"parity failed AND the preimage was not restored ({len(after)} files vs {len(pre)})")
    except OSError as exc:
        return finish(ERR_ROLLBACK_FAILED, False, f"parity failed and rollback raised: {exc}")
    return finish(ERR_PARITY_NOT_PROVEN, False,
                  f"parity not proven (pos_ok={pos_ok}, neg_ok={neg_ok}); preimage restored")


if __name__ == "__main__":
    raise SystemExit(main())
