#!/usr/bin/env python3
"""Publication projection manifest (REQ-PIPD-R4-W1 / R3-EXT-01, R-AUD-006, R-AUD-014).

Two *different* subjects are conflated by the local evidence manifest:

* the **frozen local candidate** the manifest is sealed against
  (``10cb3d31fcbd54fffe64152f4b17085866d0d75e`` / tree ``bba26ad0634e46169270e81109f9db22c967602a``), and
* the **published GitHub subject** (``3aebbbce948871c07b875ab92acf263d298ecf38`` /
  tree ``1a7dc57f9403202c32d1bc01deb1925ac1f6412e``).

Reading the local seal (``.hgk/artifacts/evidence_manifest.seal.json``) as a statement about the
published commit/tree MUST FAIL. This tool projects every one of the local manifest's entries onto
the published subject and states, per entry, exactly what that published subject contains:

* ``PUBLIC_IN_PUBLISHED_TREE`` -- the same path is present in the published tree;
* ``PRIVATE_ARCHIVE``         -- deliberately retained off-repo (harness logs in ``.hgk/ao/*.log``);
* ``EXCLUDED_OVERSIZE``       -- omitted for exceeding the GitHub blob limit (100 MiB);
* ``NOT_PUBLISHED``           -- worktree-only evidence the published tree never carried.

The tool NEVER rewrites the evidence manifest or its seal -- it binds to them read-only.

Digest formats (byte-deterministic):

* ``product_digest``  = sha256 over ``"<path>\\0<blob_content_sha256>\\n"`` for the sorted
  product paths (``src/ tools/ tests/ schemas/ skills/ docs/ dist/ fixtures``) of a subject tree.
* ``manifest_digest`` = the same formula over *every* path of a subject tree.
* ``crosswalk_digest`` = sha256 over ``"<path>\\0<disposition>\\0<local_sha256>\\0<published_or_EMPTY>\\n"``
  for the sorted entries of this projection.

Git access is read-only and offline: the reader decodes loose blob/tree/commit objects straight out
of ``.git/objects`` (the writer image has no ``git`` binary). It never commits, pushes, checks out,
resets or rewrites anything.

Commands
--------
``--write``  emit ``.hgk/ao/pub/PUBLICATION_PROJECTION_MANIFEST.json``.
``--check``  verify the projection; exit non-zero on any violation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GIT_DIR = ROOT / ".git"
PUB_DIR = ROOT / ".hgk" / "ao" / "pub"
PROJECTION = PUB_DIR / "PUBLICATION_PROJECTION_MANIFEST.json"
EVIDENCE_MANIFEST = ROOT / ".hgk" / "artifacts" / "evidence_manifest.json"
EVIDENCE_SEAL = ROOT / ".hgk" / "artifacts" / "evidence_manifest.seal.json"

SCHEMA = "PIPD-PUBLICATION-PROJECTION/1"
# Inherited from the frozen candidate tuple (FROZEN_CANDIDATE_R3.json / ROUND_STATE.json).
POLICY_VERSION = "CAPC-PROMPT-CONTRACT/1"

PUBLISHED_COMMIT = "3aebbbce948871c07b875ab92acf263d298ecf38"
PUBLISHED_TREE = "1a7dc57f9403202c32d1bc01deb1925ac1f6412e"
LOCAL_CANDIDATE_COMMIT = "10cb3d31fcbd54fffe64152f4b17085866d0d75e"
LOCAL_CANDIDATE_TREE = "bba26ad0634e46169270e81109f9db22c967602a"
PUBLISHED_REF = "r3-candidate"

# The product tree: the paths whose byte-identity is claimed across the two subjects.
PRODUCT_PREFIXES = ("src/", "tools/", "tests/", "schemas/", "skills/", "docs/", "dist/", "fixtures")

# GitHub hard-rejects blobs larger than 100 MiB.
OVERSIZE_LIMIT_BYTES = 100 * 1024 * 1024

DISPOSITIONS = (
    "PUBLIC_IN_PUBLISHED_TREE",
    "PRIVATE_ARCHIVE",
    "EXCLUDED_OVERSIZE",
    "NOT_PUBLISHED",
)

# Off-repo retention targets, keyed by manifest-path prefix.
PRIVATE_ARCHIVE_PREFIXES = (".hgk/ao/",)


class GitObjectUnavailable(RuntimeError):
    """A git object required for an offline digest is not present in the local store."""


# --------------------------------------------------------------------------------------------------
# Minimal read-only git object store reader
# --------------------------------------------------------------------------------------------------
def _loose_path(sha: str) -> Path:
    return GIT_DIR / "objects" / sha[:2] / sha[2:]


def read_object(sha: str) -> tuple[str, bytes]:
    """Return ``(type, body)`` for a loose object. Read-only; never writes."""
    p = _loose_path(sha)
    if not p.exists():
        raise GitObjectUnavailable(
            f"object {sha} is not a loose object in {GIT_DIR} and no pack index is consulted offline"
        )
    raw = zlib.decompress(p.read_bytes())
    header, _, body = raw.partition(b"\x00")
    obj_type = header.split(b" ", 1)[0].decode("ascii")
    return obj_type, body


def object_exists(sha: str) -> bool:
    return _loose_path(sha).exists()


def resolve_ref(ref: str) -> str:
    """Resolve a branch/tag name or a 40-hex sha to an object id (read-only)."""
    if len(ref) == 40 and all(c in "0123456789abcdef" for c in ref):
        if not object_exists(ref):
            raise GitObjectUnavailable(f"commit {ref} is not present in the local object store")
        return ref
    for candidate in (GIT_DIR / "refs" / "heads" / ref, GIT_DIR / "refs" / "tags" / ref):
        if candidate.exists():
            return candidate.read_text(encoding="ascii").strip()
    # packed-refs fallback
    packed = GIT_DIR / "packed-refs"
    if packed.exists():
        for line in packed.read_text(encoding="ascii").splitlines():
            if line.startswith("#") or not line.strip():
                continue
            sha, _, name = line.partition(" ")
            if name.strip() in (f"refs/heads/{ref}", f"refs/tags/{ref}", ref):
                return sha.strip()
    raise GitObjectUnavailable(f"cannot resolve ref {ref!r} in {GIT_DIR}")


def commit_tree(commit_sha: str) -> str:
    obj_type, body = read_object(commit_sha)
    if obj_type != "commit":
        raise GitObjectUnavailable(f"{commit_sha} is a {obj_type}, not a commit")
    header = body.split(b"\n\n", 1)[0].decode("utf-8", "replace")
    for line in header.splitlines():
        if line.startswith("tree "):
            return line.split(" ", 1)[1].strip()
    raise GitObjectUnavailable(f"commit {commit_sha} has no tree header")


def _parse_tree(body: bytes) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    i = 0
    while i < len(body):
        nul = body.index(b"\x00", i)
        mode, name = body[i:nul].split(b" ", 1)
        sha = body[nul + 1:nul + 21].hex()
        out.append((mode.decode("ascii"), name.decode("utf-8", "replace"), sha))
        i = nul + 21
    return out


def walk_tree(tree_sha: str, prefix: str = "") -> dict[str, str]:
    """Flatten a tree into ``{path: blob_oid}`` for every blob entry.

    Symlinks (``120000``) are blobs and are included. Gitlinks (``160000``, submodule pointers) are
    commits, not blobs -- they carry no content digest and are skipped, so the manifest digests stay
    a function of real file bytes only.
    """
    obj_type, body = read_object(tree_sha)
    if obj_type != "tree":
        raise GitObjectUnavailable(f"{tree_sha} is a {obj_type}, not a tree")
    files: dict[str, str] = {}
    for mode, name, sha in _parse_tree(body):
        path = prefix + name
        if mode == "40000":
            files.update(walk_tree(sha, path + "/"))
        elif mode in ("100644", "100755", "120000"):
            files[path] = sha
        # mode 160000 (gitlink) carries no blob content: skip.
    return files


_BLOB_SHA_CACHE: dict[str, str] = {}


def blob_content_sha256(blob_oid: str) -> str:
    """sha256 over the raw blob body (the manifest's per-file digest semantics)."""
    if blob_oid in _BLOB_SHA_CACHE:
        return _BLOB_SHA_CACHE[blob_oid]
    obj_type, body = read_object(blob_oid)
    if obj_type != "blob":
        raise GitObjectUnavailable(f"{blob_oid} is a {obj_type}, not a blob")
    digest = hashlib.sha256(body).hexdigest()
    _BLOB_SHA_CACHE[blob_oid] = digest
    return digest


def blob_size(blob_oid: str) -> int:
    obj_type, body = read_object(blob_oid)
    if obj_type != "blob":
        raise GitObjectUnavailable(f"{blob_oid} is a {obj_type}, not a blob")
    return len(body)


# --------------------------------------------------------------------------------------------------
# Digests
# --------------------------------------------------------------------------------------------------
def is_product_path(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in PRODUCT_PREFIXES)


def _digest_lines(pairs: list[tuple[str, str]]) -> str:
    h = hashlib.sha256()
    for path, blob_sha in sorted(pairs):
        h.update(path.encode("utf-8") + b"\x00" + blob_sha.encode("ascii") + b"\n")
    return h.hexdigest()


def product_digest(tree_or_map) -> str:
    """sha256 over the sorted product paths of a subject (tree sha or ``{path: blob_oid}``)."""
    tree_map = tree_or_map if isinstance(tree_or_map, dict) else walk_tree(tree_or_map)
    pairs = [(p, blob_content_sha256(oid)) for p, oid in tree_map.items() if is_product_path(p)]
    return _digest_lines(pairs)


def manifest_digest(tree_or_map) -> str:
    """sha256 over the sorted *every-path* listing of a subject (tree sha or ``{path: blob_oid}``)."""
    tree_map = tree_or_map if isinstance(tree_or_map, dict) else walk_tree(tree_or_map)
    pairs = [(p, blob_content_sha256(oid)) for p, oid in tree_map.items()]
    return _digest_lines(pairs)


def _crosswalk_digest(entries: dict[str, dict]) -> str:
    h = hashlib.sha256()
    for path in sorted(entries):
        e = entries[path]
        pub = e.get("published_blob_sha256") or "EMPTY"
        h.update(
            path.encode("utf-8")
            + b"\x00" + e["disposition"].encode("ascii")
            + b"\x00" + e["local_sha256"].encode("ascii")
            + b"\x00" + pub.encode("ascii")
            + b"\n"
        )
    return h.hexdigest()


# --------------------------------------------------------------------------------------------------
# Current-tree coverage (W9): the published subject is NOT the worktree. A passing published-subject
# check must never be read as "every current product file is accounted for" - that omission was
# silent, and is what this block makes explicit.
# --------------------------------------------------------------------------------------------------
def current_product_paths(repo: Path | None = None) -> list[str]:
    """Every current product path in the worktree (bytecode caches excluded)."""
    repo = repo or ROOT
    out: list[str] = []
    for prefix in PRODUCT_PREFIXES:
        base = repo / prefix
        if not base.exists():
            continue
        if base.is_file():
            out.append(prefix)
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(repo).as_posix()
            if "__pycache__" in rel.split("/") or rel.endswith(".pyc"):
                continue
            out.append(rel)
    return sorted(set(out))


def current_tree_coverage(entries: dict[str, dict] | None = None,
                          repo: Path | None = None) -> dict:
    """List every current product path with its disposition, or ``UNCOVERED``.

    ``entries`` is the published-subject projection crosswalk. A current path that is not one of its
    keys has no disposition at all in the manifest - it is UNCOVERED, and saying so is the point.
    """
    repo = repo or ROOT
    disposal_map: dict[str, str] = {}
    if entries is None and PROJECTION.exists():
        try:
            entries = json.loads(PROJECTION.read_text(encoding="utf-8")).get("entries", {})
        except (OSError, ValueError):
            entries = {}
    entries = entries or {}
    paths = current_product_paths(repo)
    coverage: list[dict] = []
    uncovered: list[str] = []
    for path in paths:
        disposition = entries.get(path, {}).get("disposition", "UNCOVERED") if entries else "UNCOVERED"
        if disposition == "UNCOVERED":
            uncovered.append(path)
        coverage.append({"path": path, "disposition": disposition, "covered": disposition != "UNCOVERED"})
    return {"product_prefixes": list(PRODUCT_PREFIXES),
            "paths_total": len(paths),
            "covered": len(paths) - len(uncovered),
            "uncovered_count": len(uncovered),
            "uncovered": uncovered,
            "coverage": coverage}


def check_current_coverage(entries: dict[str, dict] | None = None,
                           repo: Path | None = None) -> tuple[dict, list[str]]:
    """Return (coverage block, violations). Every UNCOVERED current product path is a violation."""
    block = current_tree_coverage(entries=entries, repo=repo)
    violations = [f"CURRENT_TREE_UNCOVERED: {p} has no disposition in the manifest"
                  for p in block["uncovered"]]
    return block, violations


# --------------------------------------------------------------------------------------------------
# Projection build
# --------------------------------------------------------------------------------------------------
def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_evidence_manifest() -> tuple[dict[str, str], bytes]:
    raw = EVIDENCE_MANIFEST.read_bytes()
    return json.loads(raw.decode("utf-8")), raw


def _disposition_for(path: str, manifest_local_sha: str, published_map: dict[str, str]) -> dict:
    """One disposition + reason + reference for a single manifest entry."""
    if path in published_map:
        return {
            "local_sha256": manifest_local_sha,
            "disposition": "PUBLIC_IN_PUBLISHED_TREE",
            "published_blob_sha256": blob_content_sha256(published_map[path]),
            "reason": "path is present in the published tree with byte-identical content",
            "reference": f"published tree blob {published_map[path]}",
        }

    # Not in the published tree. Classify why, using the local candidate that carries it.
    size = _local_size(path)
    if size is not None and size > OVERSIZE_LIMIT_BYTES:
        return {
            "local_sha256": manifest_local_sha,
            "disposition": "EXCLUDED_OVERSIZE",
            "published_blob_sha256": None,
            "reason": (
                f"blob is {size} bytes ({size / 1_000_000:.2f} MB) and exceeds the "
                f"{OVERSIZE_LIMIT_BYTES} byte (100 MiB) GitHub blob limit"
            ),
            "reference": (
                f"exclusion rule GITHUB_BLOB_LIMIT_100MiB; retained in the local candidate "
                f"{LOCAL_CANDIDATE_COMMIT}"
            ),
        }
    if any(path.startswith(p) for p in PRIVATE_ARCHIVE_PREFIXES):
        return {
            "local_sha256": manifest_local_sha,
            "disposition": "PRIVATE_ARCHIVE",
            "published_blob_sha256": None,
            "reason": "deliberately retained off-repo; never published by design",
            "reference": (
                f"private archive .hgk/ao/ (local object store {LOCAL_CANDIDATE_COMMIT}); "
                f"retention bound to local_sha256 {manifest_local_sha}"
            ),
        }
    return {
        "local_sha256": manifest_local_sha,
        "disposition": "NOT_PUBLISHED",
        "published_blob_sha256": None,
        "reason": "worktree-only execution evidence; absent from the published tree",
        "reference": (
            f"local candidate {LOCAL_CANDIDATE_COMMIT} (tree {LOCAL_CANDIDATE_TREE}); "
            f"not in published tree {PUBLISHED_TREE}"
        ),
    }


_LOCAL_SIZE_CACHE: dict[str, int | None] = {}


def _local_size(path: str) -> int | None:
    """Size of a path as carried by the frozen local candidate tree, else the worktree, else None."""
    if path in _LOCAL_SIZE_CACHE:
        return _LOCAL_SIZE_CACHE[path]
    size: int | None = None
    # Prefer the frozen candidate tree (stable, offline).
    local_map = _frozen_tree_map()
    if path in local_map:
        try:
            size = blob_size(local_map[path])
        except GitObjectUnavailable:
            size = None
    if size is None:
        fp = ROOT / path
        if fp.is_file():
            size = fp.stat().st_size
    _LOCAL_SIZE_CACHE[path] = size
    return size


_FROZEN_MAP: dict[str, str] | None = None


def _frozen_tree_map() -> dict[str, str]:
    global _FROZEN_MAP
    if _FROZEN_MAP is None:
        _FROZEN_MAP = walk_tree(commit_tree(LOCAL_CANDIDATE_COMMIT))
    return _FROZEN_MAP


def build_projection(*, published_commit: str, published_tree: str) -> dict:
    manifest, manifest_raw = load_evidence_manifest()
    seal = _load_json(EVIDENCE_SEAL) if EVIDENCE_SEAL.exists() else {}
    published_map = walk_tree(published_tree)

    entries: dict[str, dict] = {}
    for path, local_sha in sorted(manifest.items()):
        entries[path] = _disposition_for(path, local_sha, published_map)

    counts = {"total": len(entries)}
    for disposition in DISPOSITIONS:
        counts[disposition] = sum(1 for e in entries.values() if e["disposition"] == disposition)

    projection = {
        "schema": SCHEMA,
        "policy_version": POLICY_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "subject_scope": {
            "scope": "PUBLISHED_SUBJECT",
            "commit": published_commit,
            "tree": published_tree,
            "ref": PUBLISHED_REF,
            "statement": (
                "this crosswalk covers the published subject commit/tree only; it does NOT assert "
                "coverage of the current worktree (see the current_tree_coverage report)"
            ),
        },
        "published_subject": {"commit": published_commit, "tree": published_tree, "ref": PUBLISHED_REF},
        "local_candidate": {
            "commit": LOCAL_CANDIDATE_COMMIT,
            "tree": LOCAL_CANDIDATE_TREE,
            "role": "frozen local candidate the evidence manifest is sealed against",
        },
        "subjects_are_distinct": (
            published_commit != LOCAL_CANDIDATE_COMMIT and published_tree != LOCAL_CANDIDATE_TREE
        ),
        "product_paths": list(PRODUCT_PREFIXES),
        "oversize_limit_bytes": OVERSIZE_LIMIT_BYTES,
        "source_manifest": {
            "path": str(EVIDENCE_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "sha256": hashlib.sha256(manifest_raw).hexdigest(),
            "bytes": len(manifest_raw),
            "entries": len(manifest),
        },
        "source_manifest_seal": {
            "path": str(EVIDENCE_SEAL.relative_to(ROOT)).replace("\\", "/"),
            "sha256": hashlib.sha256(EVIDENCE_SEAL.read_bytes()).hexdigest() if EVIDENCE_SEAL.exists() else None,
            "candidate": seal.get("candidate", {}),
        },
        "product_digest": product_digest(published_map),
        "manifest_digest": manifest_digest(published_map),
        "counts": counts,
        "crosswalk_digest": _crosswalk_digest(entries),
        "entries": entries,
    }
    return projection


# --------------------------------------------------------------------------------------------------
# Projection check
# --------------------------------------------------------------------------------------------------
def _product_map(tree_map: dict[str, str]) -> dict[str, str]:
    return {p: blob_content_sha256(oid) for p, oid in tree_map.items() if is_product_path(p)}


def check_projection(
    projection: dict,
    *,
    manifest: dict[str, str],
    seal: dict,
    published_tree_map: dict[str, str],
    frozen_tree_map: dict[str, str],
) -> list[str]:
    """Return a list of violations for an (already loaded) projection. Empty == OK."""
    violations: list[str] = []
    entries = projection.get("entries", {})

    # Rule 3a: no entry silently dropped, none invented; the crosswalk covers the manifest exactly.
    missing = sorted(p for p in manifest if p not in entries)
    extra = sorted(p for p in entries if p not in manifest)
    if missing:
        violations.append(f"CROSSWALK_DROP: {len(missing)} manifest entries absent from projection, e.g. {missing[:3]}")
    if extra:
        violations.append(f"CROSSWALK_EXTRA: {len(extra)} projection entries not in manifest, e.g. {extra[:3]}")

    # Rule 1: PUBLIC_IN_PUBLISHED_TREE must actually be in the published tree, byte-for-byte.
    for path, e in entries.items():
        if e.get("disposition") != "PUBLIC_IN_PUBLISHED_TREE":
            continue
        if path not in published_tree_map:
            violations.append(f"PUBLIC_NOT_IN_TREE: {path} claims PUBLIC_IN_PUBLISHED_TREE but is absent")
            continue
        want = blob_content_sha256(published_tree_map[path])
        if e.get("published_blob_sha256") != want:
            violations.append(
                f"PUBLIC_DIGEST_MISMATCH: {path} published_blob_sha256="
                f"{e.get('published_blob_sha256')} but tree has {want}"
            )

    # Rule 4: the source seal must name the *local* candidate, never the published subject.
    seal_candidate = (seal.get("candidate") or {}) if isinstance(seal, dict) else {}
    seal_commit = seal_candidate.get("repo_commit_sha")
    seal_tree = seal_candidate.get("candidate_tree_sha")
    published = projection.get("published_subject", {})
    if seal_commit and seal_commit == published.get("commit"):
        violations.append(
            f"SEAL_SUBJECT_CONFLATION: seal names the published commit {seal_commit} as the "
            f"manifest's candidate; the manifest cannot assert the published subject"
        )
    if seal_tree and seal_tree == published.get("tree"):
        violations.append(
            f"SEAL_SUBJECT_CONFLATION: seal names the published tree {seal_tree}; "
            f"a seal for the local candidate may not be read as the published subject"
        )
    # The seal's recorded manifest digest must match the manifest bytes actually present.
    recorded = (seal.get("manifest") or {}).get("sha256") if isinstance(seal, dict) else None
    actual = hashlib.sha256(EVIDENCE_MANIFEST.read_bytes()).hexdigest()
    if recorded and recorded != actual:
        violations.append(
            f"SEAL_STALE: seal manifest sha256 {recorded} does not match the manifest bytes {actual}"
        )

    # Rule 2: product-path equality between the published tree and the frozen local candidate.
    pub_product = _product_map(published_tree_map)
    frz_product = _product_map(frozen_tree_map)
    only_pub = sorted(set(pub_product) - set(frz_product))
    only_frz = sorted(set(frz_product) - set(pub_product))
    if only_pub:
        violations.append(f"PRODUCT_PATH_ADDED: published product paths absent from candidate, e.g. {only_pub[:3]}")
    if only_frz:
        violations.append(f"PRODUCT_PATH_MISSING: candidate product paths absent from published, e.g. {only_frz[:3]}")
    drift = sorted(p for p in set(pub_product) & set(frz_product) if pub_product[p] != frz_product[p])
    if drift:
        violations.append(f"PRODUCT_BYTE_DRIFT: {len(drift)} product paths differ by content, e.g. {drift[:3]}")

    # Rule 3b: counts reconcile to the manifest total and each entry has exactly one disposition + reason.
    counts = projection.get("counts", {})
    if counts.get("total") != len(manifest):
        violations.append(f"COUNT_TOTAL: counts.total={counts.get('total')} != manifest entries={len(manifest)}")
    disposition_sum = sum(counts.get(d, 0) for d in DISPOSITIONS)
    if counts.get("total") != disposition_sum:
        violations.append(f"COUNT_RECONCILE: per-disposition sum {disposition_sum} != total {counts.get('total')}")
    actual_counts = {d: sum(1 for e in entries.values() if e.get("disposition") == d) for d in DISPOSITIONS}
    for d in DISPOSITIONS:
        if counts.get(d) != actual_counts[d]:
            violations.append(f"COUNT_MISMATCH[{d}]: recorded {counts.get(d)} != actual {actual_counts[d]}")
    for path, e in entries.items():
        if e.get("disposition") not in DISPOSITIONS:
            violations.append(f"BAD_DISPOSITION: {path} -> {e.get('disposition')!r}")
        if not e.get("reason"):
            violations.append(f"MISSING_REASON: {path}")
    return violations


def run_check(projection: dict) -> list[str]:
    manifest, _ = load_evidence_manifest()
    seal = _load_json(EVIDENCE_SEAL) if EVIDENCE_SEAL.exists() else {}
    published_tree = projection.get("published_subject", {}).get("tree", PUBLISHED_TREE)
    return check_projection(
        projection,
        manifest=manifest,
        seal=seal,
        published_tree_map=walk_tree(published_tree),
        frozen_tree_map=_frozen_tree_map(),
    )


# --------------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------------
def _resolve_subject(args) -> tuple[str, str]:
    commit = args.commit or resolve_ref(PUBLISHED_REF)
    tree = args.tree or commit_tree(commit)
    return commit, tree


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publication projection manifest (REQ-PIPD-R4-W1).")
    parser.add_argument("--commit", help="published subject commit (default: resolve r3-candidate)")
    parser.add_argument("--tree", help="published subject tree (default: from --commit)")
    parser.add_argument("--write", action="store_true", help=f"emit {PROJECTION.relative_to(ROOT)}")
    parser.add_argument("--check", action="store_true", help="verify the projection; non-zero on violation")
    parser.add_argument("--current", action="store_true",
                        help="with --check: also FAIL while any current worktree product path is UNCOVERED")
    args = parser.parse_args(argv)

    if not args.write and not args.check:
        parser.error("at least one of --write / --check is required")
    if args.current and not args.check:
        parser.error("--current is only meaningful together with --check")

    try:
        published_commit, published_tree = _resolve_subject(args)
    except GitObjectUnavailable as exc:
        print(json.dumps({"verdict": "FAIL", "reason": str(exc)}), file=sys.stderr)
        return 1

    if args.write:
        projection = build_projection(published_commit=published_commit, published_tree=published_tree)
        PUB_DIR.mkdir(parents=True, exist_ok=True)
        PROJECTION.write_text(
            json.dumps(projection, ensure_ascii=False, indent=1, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {PROJECTION.relative_to(ROOT)} ({len(projection['entries'])} entries)")

    exit_code = 0
    if args.check:
        projection = _load_json(PROJECTION)
        violations = run_check(projection)
        counts = projection.get("counts", {})
        # The coverage block is ALWAYS printed - a passing published-subject check must never be
        # read as silent coverage of the current tree.
        coverage = current_tree_coverage(entries=projection.get("entries", {}))
        current_violations: list[str] = []
        if args.current:
            _, current_violations = check_current_coverage(entries=projection.get("entries", {}))
            violations = violations + current_violations
        report = {
            "verdict": "PASS" if not violations else "FAIL",
            "subject_scope": projection.get("subject_scope") or {
                "scope": "PUBLISHED_SUBJECT",
                "commit": projection.get("published_subject", {}).get("commit"),
                "tree": projection.get("published_subject", {}).get("tree"),
            },
            "published_subject": projection.get("published_subject"),
            "current_tree_coverage": coverage,
            "counts": counts,
            "crosswalk_digest": projection.get("crosswalk_digest"),
            "product_digest": projection.get("product_digest"),
            "violations": violations,
        }
        print(json.dumps(report, ensure_ascii=False, indent=1))
        exit_code = 0 if not violations else 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
