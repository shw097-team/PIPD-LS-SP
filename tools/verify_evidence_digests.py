#!/usr/bin/env python3
"""Recompute the per-entry sha256 recorded in the evidence manifest, classify every mismatch by the
bytes the digest was actually computed over, and report generation-identity ancestry.

Why this exists: nothing else recomputes the digest each entry of
``.hgk/artifacts/evidence_manifest.json`` claims for its file, and
``tools/build_publication_manifest.py`` folds those digests into ``crosswalk_digest``. A silent class
of drift (a file edited after the manifest was sealed) therefore stays invisible.

The gate (v2 -- a hash match against *some* basis is NOT sufficient). For each entry with path ``p``,
recorded digest ``r`` and on-disk bytes ``d``::

    normalize_eol(b) = b.replace(b"\\r\\n", b"\\n")               # CRLF -> LF

    basis digests, first match wins:
        disk                 sha256(d)
        crlf_disk            sha256(crlf(d)) or sha256(lf(d))
        head_blob            sha256(blob(p)@HEAD)
        crlf_head_blob       sha256(crlf(blob@HEAD)) or sha256(lf(blob@HEAD))
        candidate_blob       sha256(blob(p)@sealed_candidate)
        crlf_candidate_blob  sha256(crlf(blob@cand)) or sha256(lf(blob@cand))

    MATCH_RAW          sha256(d) == r.
    BENIGN_EOL         some basis ``x`` hashes to ``r`` AND normalize_eol(x) == normalize_eol(d):
                       a pure checkout / line-ending difference, never a failure.
    UNEXPLAINED_DRIFT  otherwise: ``p`` is missing, no basis hashes to ``r``, or a basis hashes to
                       ``r`` but its content is not EOL-equivalent to ``d`` -- the recorded digest
                       describes bytes that no longer describe the file, which is genuine drift.

The content-equality clause is MANDATORY. Accepting ``blob@candidate`` (or any crlf variant) on a
hash match alone would rubber-stamp a real post-seal content edit: the old snapshot still hashes to
the recorded digest even though the file has genuinely changed.

Byte transformations implemented, exactly (both directions; a ``crlf_*`` basis matches either)::

    crlf(b) = b.replace(b"\\r\\n", b"\\x00").replace(b"\\n", b"\\r\\n").replace(b"\\x00", b"\\r\\n")
              (lone LF -> CRLF)
    lf(b)   = b.replace(b"\\r\\n", b"\\n")                        (CRLF -> LF)

A file with no CRLF and no lone LF is unchanged by both, so ``disk`` wins for it.

The sealed candidate revision is read from the sibling seal (``<manifest stem>.seal.json`` ->
``candidate.candidate_tree_sha`` then ``candidate.repo_commit_sha``); it is never hard-coded. With no
sibling seal the candidate bases are simply unavailable.

Generation identity is REPORT-ONLY: for every JSON payload carrying ``candidate_head`` the report
records whether that revision is an ancestor of HEAD. A non-ancestor is named in the report and the
run still exits 0 without ``--strict`` (making it fatal was adjudicated a no-op / downgrade).

Writes nothing except the optional ``--json`` output path. The default run prints the full report and
exits 0; ``--strict`` exits 1 iff the unexplained set is non-empty; ``--json`` prints the compact
summary ``{"checked","match_raw","benign_eol","unexplained","basis_counts"}``. The full report keeps
the keys the existing in-tree test reads (``checked``, ``match``, ``missing``, ``stale``,
``identity_checks``).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / ".hgk" / "artifacts" / "evidence_manifest.json"

# Ordered basis labels; the first one whose digest matches the recorded value names the bytes.
BASIS_LABELS = ("disk", "crlf_disk", "head_blob", "crlf_head_blob",
                "candidate_blob", "crlf_candidate_blob")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _crlf(data: bytes) -> bytes:
    """Expand every lone LF to CRLF (an existing CRLF is left alone)."""
    return data.replace(b"\r\n", b"\x00").replace(b"\n", b"\r\n").replace(b"\x00", b"\r\n")


def _lf(data: bytes) -> bytes:
    """Collapse every CRLF to LF."""
    return data.replace(b"\r\n", b"\n")


def _normalize_eol(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def _eol_variants(data: bytes) -> tuple[bytes, bytes]:
    return _crlf(data), _lf(data)


def _git(root: Path, *args: str, data: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], input=data, capture_output=True)


def _read_blobs(root: Path, specs: list[str]) -> dict[str, bytes]:
    """Resolve many ``<rev>:<path>`` blob specs with ONE ``git cat-file --batch`` call.

    Only specs whose object exists are returned; a missing path is simply absent. When ``git`` is
    unavailable or the rev cannot be resolved the map is empty and the blob bases do not match.
    """
    if not specs:
        return {}
    proc = _git(root, "cat-file", "--batch",
                data="".join(f"{spec}\n" for spec in specs).encode("utf-8"))
    if proc.returncode != 0:
        return {}
    blobs: dict[str, bytes] = {}
    data, pos = proc.stdout, 0
    for spec in specs:
        try:
            end = data.index(b"\n", pos)
        except ValueError:
            break
        header = data[pos:end]
        if header.endswith(b" missing"):
            pos = end + 1
            continue
        fields = header.rsplit(b" ", 1)
        if len(fields) != 2:
            break
        size = int(fields[1])
        blobs[spec] = data[end + 1:end + 1 + size]
        pos = end + 1 + size + 1
    return blobs


def _sealed_revision(manifest_path: Path) -> str | None:
    """The sealed candidate tree (preferred) or commit from the manifest's sibling seal, if any."""
    seal = manifest_path.with_name(manifest_path.stem + ".seal.json")
    if not seal.is_file():
        return None
    try:
        payload = json.loads(seal.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    candidate = payload.get("candidate") if isinstance(payload, dict) else None
    if not isinstance(candidate, dict):
        return None
    for key in ("candidate_tree_sha", "repo_commit_sha"):
        value = candidate.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _verdict(basis_bytes: bytes, disk_bytes: bytes) -> str:
    """``benign_eol`` when a matching basis is EOL-equivalent to the disk bytes, else drift."""
    if _normalize_eol(basis_bytes) == _normalize_eol(disk_bytes):
        return "benign_eol"
    return "unexplained"


def _classify(rel: str, digest: str, root: Path, candidate_rev: str | None,
              blobs: dict[str, bytes]) -> tuple[str, str]:
    """Return ``(basis, verdict)`` for one manifest entry (see the module docstring's gate)."""
    target = root / rel
    if not target.is_file():
        return "unexplained", "unexplained"
    raw = target.read_bytes()
    if _digest(raw) == digest:
        return "disk", "match_raw"
    for variant in _eol_variants(raw):
        if _digest(variant) == digest:
            return "crlf_disk", _verdict(variant, raw)
    repo_bases = (("head_blob", "crlf_head_blob", f"HEAD:{rel}"),
                  ("candidate_blob", "crlf_candidate_blob",
                   f"{candidate_rev}:{rel}" if candidate_rev else None))
    for raw_label, eol_label, spec in repo_bases:
        if spec is None:
            continue
        blob = blobs.get(spec)
        if blob is None:
            continue
        if _digest(blob) == digest:
            return raw_label, _verdict(blob, raw)
        for variant in _eol_variants(blob):
            if _digest(variant) == digest:
                return eol_label, _verdict(variant, raw)
    return "unexplained", "unexplained"


def _identity_check(root: Path, rel: str, value: object) -> dict:
    """Report whether a recorded ``candidate_head`` is an ancestor of HEAD. Never raises."""
    rec: dict = {"path": rel, "candidate_head": value, "is_ancestor": False, "error": None}
    commit = value.strip() if isinstance(value, str) else ""
    if not commit:
        rec["error"] = "candidate_head is empty or not a string"
        return rec
    try:
        resolved = _git(root, "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}")
    except OSError:
        rec["error"] = "git unavailable"
        return rec
    if resolved.returncode != 0:
        rec["error"] = "candidate_head does not resolve to a commit"
        return rec
    ancestor = _git(root, "merge-base", "--is-ancestor", commit, "HEAD")
    if ancestor.returncode == 0:
        rec["is_ancestor"] = True
    elif ancestor.returncode == 1:
        rec["is_ancestor"] = False
    else:
        rec["error"] = (ancestor.stderr or b"git merge-base --is-ancestor failed").decode(
            "utf-8", "replace").strip()
    return rec


def build_report(manifest_path: Path, root: Path | None = None) -> dict:
    """Recompute every recorded digest, classify each mismatch by basis, and collect identity checks."""
    repo = Path(root) if root is not None else ROOT
    entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidate_rev = _sealed_revision(manifest_path)

    basis: dict[str, str] = {}
    verdict: dict[str, str] = {}
    stale: list[str] = []
    missing: list[str] = []
    pending: list[str] = []

    for rel in sorted(entries):
        target = repo / rel
        if not target.is_file():
            missing.append(rel)
            basis[rel], verdict[rel] = "unexplained", "unexplained"
            continue
        if _digest(target.read_bytes()) == entries[rel]:
            basis[rel], verdict[rel] = "disk", "match_raw"
            continue
        stale.append(rel)
        pending.append(rel)

    # Only the entries the disk bytes cannot explain need a repository readback.
    specs: list[str] = []
    for rel in pending:
        specs.append(f"HEAD:{rel}")
        if candidate_rev:
            specs.append(f"{candidate_rev}:{rel}")
    blobs = _read_blobs(repo, specs)
    for rel in pending:
        basis[rel], verdict[rel] = _classify(rel, entries[rel], repo, candidate_rev, blobs)

    identity_checks: list[dict] = []
    for rel in sorted(entries):
        target = repo / rel
        if not target.is_file():
            continue
        try:
            payload = json.loads(target.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            continue
        if isinstance(payload, dict) and "candidate_head" in payload:
            identity_checks.append(_identity_check(repo, rel, payload["candidate_head"]))

    counts = {label: 0 for label in (*BASIS_LABELS, "unexplained")}
    for rel in entries:
        counts[basis.get(rel, "unexplained")] += 1
    match_raw = sum(1 for rel in entries if verdict[rel] == "match_raw")
    benign_eol = sum(1 for rel in entries if verdict[rel] == "benign_eol")
    unexplained = [rel for rel in sorted(entries) if verdict[rel] == "unexplained"]
    return {
        "checked": len(entries),
        "match": match_raw,          # back-compat name for the raw-disk match count
        "match_raw": match_raw,
        "benign_eol": benign_eol,
        "explained": match_raw + benign_eol,
        "missing": len(missing),
        "stale": stale,
        "unexplained": unexplained,
        "basis_counts": counts,
        "candidate_revision": candidate_rev,
        "identity_checks": identity_checks,
    }


def _summary(report: dict) -> dict:
    return {
        "checked": report["checked"],
        "match_raw": report["match_raw"],
        "benign_eol": report["benign_eol"],
        "unexplained": len(report["unexplained"]),
        "basis_counts": report["basis_counts"],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Recompute evidence-manifest digests, classify every mismatch by basis, and "
                    "report generation-identity ancestry.")
    ap.add_argument("--manifest", metavar="PATH", default=None,
                    help=f"manifest to verify (default: {DEFAULT_MANIFEST})")
    ap.add_argument("--root", metavar="PATH", default=None,
                    help="repository root the manifest paths are relative to "
                         "(default: the checkout this tool lives in)")
    ap.add_argument("--json", metavar="PATH", nargs="?", const="", default=None,
                    help="print the compact summary and, when PATH is given, write it there too "
                         "(the only file ever written)")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when the unexplained set is non-empty (opt-in; report-only otherwise)")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else ROOT
    manifest = (Path(args.manifest) if args.manifest
                else root / ".hgk" / "artifacts" / DEFAULT_MANIFEST.name)
    report = build_report(manifest, root)

    if args.json is not None:
        text = json.dumps(_summary(report), ensure_ascii=False, separators=(",", ":"))
        if args.json:
            Path(args.json).write_text(text + "\n", encoding="utf-8", newline="")
        print(text)
    else:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    return 1 if (args.strict and report["unexplained"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
