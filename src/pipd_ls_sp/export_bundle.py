"""Portable export bundle: deterministic ``<name>.tar.gz`` + manifest + checksums.

總藍圖 §5.9.3 defines ``pipd export`` as a *portable export*: it must deliver an
archive, a manifest and checksums.  This module is the bounded, dependency-free
implementation of that bundle.

The bundle is built entirely in memory first (so a refused export writes nothing
anywhere), staged into a sibling directory on the same volume, independently
verified by re-opening the archive and recomputing every member digest, and only
then published atomically through the R5-WO1 publisher shared with the surface
projector.  The destination is resolved by the caller with the existing
``projection.resolve_output_destination`` *before* this module touches disk.
"""
from __future__ import annotations

import sys

import gzip
import io
import json
import os
import shutil
import tarfile
from pathlib import Path
from typing import Any

from . import projection
from .errors import ProfileVeto
from .profiles import compute_profile
from .errors import (ExportMemberUnsafe, ExportSecretFound,
                     ExportVerificationFailed)
from .util import canonical_json, sha256_bytes, sha256_file, sha256_text, utc_now
from .workspace import secret_scan, secret_scan_paths

BUNDLE_SCHEMA = "PIPD-EXPORT-BUNDLE/1"
MANIFEST_NAME = "export_manifest.json"
SUMS_NAME = "SHA256SUMS"
DEFAULT_INCLUDE = ["schemas", "src", "tests", "docs", "pyproject.toml"]

# Frozen per-member attributes so the archive is byte-deterministic across runs
# and hosts.  No wall-clock, no user/group, no execute bits.
_MEMBER_MTIME = 0
_MEMBER_MODE = 0o644


def _validate_rel(rel: str, root: Path) -> str:
    """Refuse any member path that is absolute, contains ``..`` or escapes root."""
    if not rel:
        raise ExportMemberUnsafe("empty member path in the export set")
    norm = rel.replace("\\", "/")
    if norm.startswith("/") or os.path.isabs(rel) or (len(norm) > 1 and norm[1] == ":"):
        raise ExportMemberUnsafe(f"absolute member path refused: {rel!r}")
    parts = [p for p in norm.split("/") if p not in ("", ".")]
    if ".." in parts:
        raise ExportMemberUnsafe(f"member path contains '..': {rel!r}")
    # Belt-and-braces containment: the real path must stay inside the source root.
    root_key = os.path.normcase(os.path.abspath(str(root)))
    real_key = os.path.normcase(os.path.abspath(os.path.join(str(root), norm)))
    if real_key != root_key and not real_key.startswith(root_key.rstrip("\\/") + os.sep):
        raise ExportMemberUnsafe(f"member path escapes the source root: {rel!r}")
    return "/".join(parts)


def collect_source_files(root: Path, include: list[str] | None = None) -> list[tuple[str, Path]]:
    """The manifest file set, sorted by relative path, with per-member path safety."""
    root = Path(root)
    found: list[tuple[str, Path]] = []
    for rel in include or DEFAULT_INCLUDE:
        target = root / rel
        if target.is_file():
            found.append((rel.replace("\\", "/"), target))
        elif target.is_dir():
            for x in sorted(target.rglob("*")):
                if not x.is_file():
                    continue
                if "__pycache__" in x.parts or ".git" in x.parts:
                    continue
                found.append((str(x.relative_to(root)).replace("\\", "/"), x))
    rows = sorted({rel: p for rel, p in found}.items(), key=lambda kv: kv[0])
    return [(_validate_rel(rel, root), p) for rel, p in rows]


def file_rows(members: list[tuple[str, Path]]) -> list[dict[str, Any]]:
    rows = [{"rel": rel, "size": p.stat().st_size, "sha256": sha256_file(p)}
            for rel, p in members]
    rows.sort(key=lambda r: r["rel"])
    return rows


def manifest_files_digest(rows: list[dict[str, Any]]) -> str:
    return sha256_text(canonical_json([[r["rel"], r["size"], r["sha256"]] for r in rows]))


def _canonical_archive_name(target: Path) -> str:
    name = target.name or "export"
    return f"{name}.tar.gz"


def _build_archive(members: list[tuple[str, Path]]) -> bytes:
    """A deterministic gzip-compressed tar of the member bytes.

    Members are added sorted by rel path, each carrying a fixed mtime/uid/gid/mode,
    and the gzip layer fixes its own header mtime to 0 — so an identical source
    state yields a byte-identical archive.
    """
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.GNU_FORMAT) as tar:
        for rel, path in members:
            data = path.read_bytes()
            info = tarfile.TarInfo(name=rel)
            info.size = len(data)
            info.mtime = _MEMBER_MTIME
            info.mode = _MEMBER_MODE
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.type = tarfile.REGTYPE
            tar.addfile(info, io.BytesIO(data))
    return gzip.compress(raw.getvalue(), mtime=0)


def _sums_lines(rows: list[dict[str, Any]], archive: dict[str, Any]) -> str:
    entries = [(r["rel"], r["sha256"]) for r in rows] + [(archive["name"], archive["sha256"])]
    entries.sort(key=lambda kv: kv[0])
    return "".join(f"{sha}  {rel}\n" for rel, sha in entries)


ASSURANCE_FILE = "ASSURANCE.json"


def declared_assurance(root: Path) -> dict[str, Any]:
    """What this tree CLAIMS to evidence, from ASSURANCE.json at its root.

    Absent file means "declares nothing", which is not an error: LITE needs no declaration because the packager
    itself is the deterministic validator (it recomputes every member digest and re-opens the archive).
    """
    p = Path(root) / ASSURANCE_FILE
    if not p.is_file():
        return {"present": False, "capabilities": [], "evidence": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ProfileVeto(f"{ASSURANCE_FILE} is not readable JSON: {exc}")
    caps = [str(c) for c in (data.get("capabilities") or [])]
    return {"present": True, "capabilities": caps, "evidence": data.get("evidence") or {}}


def enforce_profile(root: Path, requested: str, *, provider_off_required: bool = False) -> dict[str, Any]:
    """Resolve the profile AND refuse to label a bundle with assurance it does not evidence.

    A ``--profile ASSURED`` that only rewrote a manifest field would produce three bundles with three names and
    one capability -- a label without a load, which is the failure this project keeps finding elsewhere.  So the
    requested profile's assurance floor is checked against what the tree actually declares, and a shortfall is a
    veto, not a warning.
    """
    from .profiles import PROFILES, compute_profile

    prof = compute_profile(requested, provider_off_required=provider_off_required)
    declared = declared_assurance(root)
    required = list(PROFILES[prof["profile"]]["assurance"])
    # deterministic_validator is the packager itself; everything else must be evidenced by the tree.
    missing = [c for c in required
               if c != "deterministic_validator" and c not in declared["capabilities"]]
    if missing:
        raise ProfileVeto(
            f"profile {prof['profile']} requires assurance {missing} that this tree does not declare in "
            f"{ASSURANCE_FILE}; refusing to label the bundle with a capability it does not evidence")
    prof["assurance_required"] = required
    prof["assurance_declared"] = declared["capabilities"]
    prof["assurance_declaration_present"] = declared["present"]
    prof["assurance_evidence"] = {c: declared["evidence"].get(c) for c in required}
    return prof


def plan(root: Path, include: list[str] | None = None, *, profile: str | None = None,
         provider_off_required: bool = False) -> dict[str, Any]:
    """The read-only plan for a bundle: file count, manifest digest, archive name, and profile."""
    root = Path(root)
    members = collect_source_files(root, include)
    block = None
    if profile:
        block = enforce_profile(root, profile, provider_off_required=provider_off_required)
        # The plan must count what the bundle will actually ship, or `pipd export --dry-run --profile lite` promises
        # 79 files and then writes a smaller archive.
        members = apply_depth(members, block["artifact_depth"])
    rows = file_rows(members)
    out: dict[str, Any] = {"file_count": len(rows), "manifest_sha256": manifest_files_digest(rows),
                           "files": rows, "source_root": str(root.resolve(strict=False))}
    if block is not None:
        out["profile"] = block
    return out


def _verify_members(archive_bytes: bytes, rows: list[dict[str, Any]]) -> None:
    """Re-open the produced archive and recompute every member digest."""
    expected = {r["rel"]: r for r in rows}
    seen: set[str] = set()
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            if member.name not in expected:
                raise ExportVerificationFailed(
                    f"archive member {member.name!r} is not in the manifest")
            data = tar.extractfile(member).read()
            row = expected[member.name]
            if len(data) != row["size"]:
                raise ExportVerificationFailed(
                    f"member {member.name!r} size {len(data)} != manifest {row['size']}")
            digest = sha256_bytes(data)
            if digest != row["sha256"]:
                raise ExportVerificationFailed(
                    f"member {member.name!r} sha256 {digest} != manifest {row['sha256']}")
            seen.add(member.name)
    missing = sorted(set(expected) - seen)
    if missing:
        raise ExportVerificationFailed(f"archive is missing manifest members {missing}")


# Artifact depth is a MEMBER-SET decision, not a label. profiles.py declares L1_SCHEMA_CONTRACT /
# L3_INTEGRATION_RUNTIME / L4_FAILURE_RECOVERY, but until this table existed every profile shipped the same 79 files
# with the same archive digest -- so `--profile lite` and `--profile standard` were the same bundle wearing two names.
# Measured 2026-10-31: both produced archive a6b3c8b3bbdf. That is the defect WP-FHS-11 was blocked on.
DEPTH_PREFIXES: dict[str, tuple[str, ...]] = {
    # The contract itself: the package modules a consumer imports, plus the declaration that says what it may claim.
    "L1_SCHEMA_CONTRACT": ("src/", "ASSURANCE.json", "pyproject.toml"),
    # Adding the proof that the package integrates: tests and the tools that exercise it.
    "L3_INTEGRATION_RUNTIME": ("src/", "tests/", "tools/", "ASSURANCE.json", "pyproject.toml"),
    # Adding what an operator needs to run and recover it.
    "L4_FAILURE_RECOVERY": ("",),
}


def apply_depth(members: list, depth: str) -> list:
    """Narrow the member set to what the profile's artifact depth actually is.

    Unknown depth raises rather than silently shipping everything: a typo in a profile name must not degrade into a
    full bundle that then carries a narrower label.
    """
    if depth not in DEPTH_PREFIXES:
        raise ValueError(f"unknown artifact_depth {depth!r}; known: {sorted(DEPTH_PREFIXES)}")
    prefixes = DEPTH_PREFIXES[depth]
    if "" in prefixes:
        return list(members)
    out = []
    for rel, path in members:
        r = str(rel).replace("\\", "/")
        if any(r == pref or r.startswith(pref) for pref in prefixes):
            out.append((rel, path))
    return out


def write_bundle(root: Path, target: Path, *, include: list[str] | None = None,
                 authorized_roots=None, allow_replace=None, profile: str | None = None,
                 provider_off_required: bool = False) -> dict[str, Any]:
    """Build, verify, stage and atomically publish a portable export bundle.

    ``target`` MUST already have been resolved by
    ``projection.resolve_output_destination`` — that happens before this call and
    therefore before any create/delete.  Nothing is written until the secret scan,
    the member-path safety check and the in-memory build have all succeeded.
    """
    root = Path(root)
    target = Path(target)

    # 0. Profile resolution happens BEFORE anything is built, so an unevidenced assurance claim costs no work and
    #    leaves nothing on disk.
    profile_block = enforce_profile(root, profile, provider_off_required=provider_off_required) if profile else None

    # 1. Member set + traversal safety (raises before any disk write). The profile narrows the set here, before the
    #    secret scan, so a narrower bundle is also scanned on exactly what it will ship.
    members = collect_source_files(root, include)
    if profile_block is not None:
        members = apply_depth(members, profile_block["artifact_depth"])

    # 2. Secrets: scan THE FILES THAT WILL SHIP, and fail closed on any hit. A repo-wide scan is also run, but its
    #    hits are reported as repo_hygiene instead of vetoing the pack -- measured 2026-10-31: a credential file at
    #    the repo root that is not in the include set blocked every Portable SP export, which blamed the artefact
    #    for a repository's problem.
    scan = secret_scan_paths([p for _rel, p in members], root)
    if scan["verdict"] != "PASS":
        raise ExportSecretFound(f"secret scan found {len(scan['hits'])} hits in the bundle")
    repo_scan = secret_scan(root)
    if repo_scan["verdict"] != "PASS":
        print(json.dumps({"warn": "REPO_HYGIENE_SECRETS_OUTSIDE_THE_BUNDLE",
                          "hits": len(repo_scan["hits"]),
                          "note": "these files are not in the archive; they are a repository finding, not a pack "
                                  "refusal"}, ensure_ascii=False), file=sys.stderr)
    rows = file_rows(members)
    archive_name = _canonical_archive_name(target)

    archive_bytes = _build_archive(members)
    manifest = {
        "schema": BUNDLE_SCHEMA,
        "generated_at": utc_now(),
        "source_root": str(root.resolve(strict=False)),
        "file_count": len(rows),
        "archive": {"name": archive_name, "size": len(archive_bytes),
                    "sha256": sha256_bytes(archive_bytes)},
        "files": rows,
    }
    if profile_block is not None:
        manifest["profile"] = profile_block
    digest = manifest_files_digest(rows)
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    sums_text = _sums_lines(rows, manifest["archive"])

    # 3. Independent verification of the in-memory archive before publishing.
    _verify_members(archive_bytes, rows)

    # 4. Stage on the same volume, verify from disk, publish atomically.
    parent = target.parent
    parent.mkdir(parents=True, exist_ok=True)
    stage = parent / f".{target.name}.pipd-stage-{projection.secrets.token_hex(8)}"
    stage.mkdir(parents=True, exist_ok=False)
    try:
        (stage / archive_name).write_bytes(archive_bytes)
        (stage / MANIFEST_NAME).write_text(manifest_text, encoding="utf-8", newline="")
        (stage / SUMS_NAME).write_text(sums_text, encoding="utf-8", newline="")

        # Re-verify from the staged bytes on disk.
        _verify_members((stage / archive_name).read_bytes(), rows)
        staged_sums = (stage / SUMS_NAME).read_text(encoding="utf-8")
        if staged_sums != sums_text:
            raise ExportVerificationFailed("staged SHA256SUMS does not match the manifest")

        # TOCTOU: re-verify containment/authorization immediately before publish.
        projection._verify_destination(Path(root).expanduser().resolve(strict=False), target,
                                       authorized_roots=authorized_roots)
        replaced, rollback = projection._publish_staged(stage, target)
    finally:
        if stage.exists():
            shutil.rmtree(stage, ignore_errors=True)

    return {
        "verdict": "PASS",
        "mode": "PORTABLE_BUNDLE",
        "out": str(target),
        "schema": BUNDLE_SCHEMA,
        "archive": manifest["archive"],
        "file_count": len(rows),
        "manifest_sha256": digest,
        "profile": (profile_block or {}).get("profile"),
        "requested_profile": (profile_block or {}).get("requested_profile"),
        "escalated": (profile_block or {}).get("escalated"),
        "secret_scan": scan["verdict"],
        "wrote": sorted([archive_name, MANIFEST_NAME, SUMS_NAME]),
        "destination": {
            "resolved": str(target),
            "authorized_roots": [str(Path(a)) for a in authorized_roots]
                                if authorized_roots else [],
            "replaced": replaced,
            "rollback_pointer": rollback,
            "staged": str(stage),
        },
    }
