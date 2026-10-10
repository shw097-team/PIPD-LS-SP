#!/usr/bin/env python3
"""S3 portable distribution: build a real, standards-shaped wheel + sdist-like bundle, with checksums.

Why a hand-built wheel: this host's python has no setuptools/build backend and the governance rule is
network-off by default, so `python -m build` cannot run. A wheel is just a zip with a defined layout
(PEP 427), and pip installs a wheel WITHOUT any build backend — so constructing it directly gives a
genuinely installable artefact instead of a claimed one. The output is verified by actually installing
it in an isolated environment (see portable_install_check.py).

R5-DIST-002: the wheel now carries the WHOLE `schemas/` tree mapped into the package
(`pipd_ls_sp/schemas/registry.json` + every `*.schema.json`), so an installed `pipd` can load its own
contract registry without the source checkout. The mirrored `pyproject.toml` `package-data` declaration
documents the same intent for any future backend build, but the wheel here is still hand-built.
"""
from __future__ import annotations

import base64
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"
SCHEMAS = ROOT / "schemas"
NAME, VERSION = "pipd_ls_sp", "0.1.0"
DISTINFO = f"{NAME}-{VERSION}.dist-info"
FROZEN_SOURCE = ROOT / ".hgk" / "rounds" / "R5-20261009-s4-user-operability" / "FROZEN_SOURCE.json"

# Files that must exist in the source tree for a wheel to be worth building. `schemas/registry.json`
# and each schema file NAMED BY THAT REGISTRY are added to this list at build time.
REQUIRED_SOURCE_FILES = [
    SRC / NAME / "cli.py",
    SRC / NAME / "requirements.py",
    SRC / NAME / "repo_context.py",
    SRC / NAME / "projection.py",
]


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _canonical_json(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _candidate_head() -> str:
    """Frozen candidate identity of the tree we build from; never invented, never from git."""
    if FROZEN_SOURCE.is_file():
        try:
            data = json.loads(FROZEN_SOURCE.read_text(encoding="utf-8"))
            head = data.get("head")
            if head:
                return head
        except (OSError, ValueError):
            pass
    return "UNKNOWN_FROZEN_SOURCE"


def _required_schema_files() -> list[Path]:
    reg_path = SCHEMAS / "registry.json"
    if not reg_path.is_file():
        return []
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    out = []
    for fam in data.get("families", []):
        contract = fam.get("contract")
        if contract:
            out.append(SCHEMAS / f"{contract}.schema.json")
    return out


def _assert_source_complete() -> None:
    missing = []
    for p in [SCHEMAS / "registry.json", *REQUIRED_SOURCE_FILES, *_required_schema_files()]:
        if not p.is_file():
            missing.append(str(p.relative_to(ROOT)))
    if not (SCHEMAS / "registry.json").is_file():
        # registry itself is missing, so the schema-file list could not be derived; say so.
        if str((SCHEMAS / "registry.json").relative_to(ROOT)) not in missing:
            missing.append(str((SCHEMAS / "registry.json").relative_to(ROOT)))
    if missing:
        raise RuntimeError(
            "refusing to build: source tree is missing required member(s): " + ", ".join(sorted(set(missing))))


def _record_line(path: str, data: bytes) -> str:
    h = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
    return f"{path},sha256={h},{len(data)}"


def build_wheel() -> dict:
    _assert_source_complete()
    DIST.mkdir(exist_ok=True)
    whl = DIST / f"{NAME}-{VERSION}-py3-none-any.whl"
    files: dict[str, bytes] = {}

    for p in sorted((SRC / NAME).rglob("*.py")):
        files[f"{NAME}/{p.relative_to(SRC / NAME).as_posix()}"] = p.read_bytes()

    # The whole schemas/ tree, mapped INTO the package so an installed pipd is self-sufficient.
    for p in sorted(SCHEMAS.rglob("*.json")):
        files[f"{NAME}/schemas/{p.relative_to(SCHEMAS).as_posix()}"] = p.read_bytes()

    files[f"{DISTINFO}/METADATA"] = (
        "Metadata-Version: 2.3\n"
        f"Name: pipd-ls-sp\nVersion: {VERSION}\n"
        "Summary: PIPD-LS-SP Pre-Implementation & Pre-Dev Lifecycle Skills Plugin (HG-KSEOS governed)\n"
        "Requires-Python: >=3.11\n"
        "Requires-Dist: jsonschema>=4.0\n"
        "License: LicenseRef-PIPD-Proprietary\n"
        "Description-Content-Type: text/markdown\n\n"
        "# PIPD-LS-SP\n\nGoverned pre-implementation contract compiler. Licence position: see LICENSE "
        "(no licence granted; owner grant pending, TT-PIPD-LICENSE-001).\n"
    ).encode()
    files[f"{DISTINFO}/WHEEL"] = (
        "Wheel-Version: 1.0\nGenerator: pipd-ls-sp hand-built (PEP 427)\n"
        "Root-Is-Purelib: true\nTag: py3-none-any\n"
    ).encode()
    files[f"{DISTINFO}/top_level.txt"] = (NAME + "\n").encode()
    files[f"{DISTINFO}/entry_points.txt"] = b"[console_scripts]\npipd = pipd_ls_sp.cli:main\n"

    # RECORD covers every file except itself.
    record = "".join(_record_line(k, v) + "\n" for k, v in sorted(files.items()))
    record += f"{DISTINFO}/RECORD,,\n"
    files[f"{DISTINFO}/RECORD"] = record.encode()

    with zipfile.ZipFile(whl, "w", zipfile.ZIP_DEFLATED) as z:
        for k in sorted(files):
            zi = zipfile.ZipInfo(k, date_time=(1980, 1, 1, 0, 0, 0))   # deterministic archive
            zi.external_attr = 0o644 << 16
            z.writestr(zi, files[k])

    member_hashes = {k: _sha256(v) for k, v in sorted(files.items())}
    # a source bundle with the checksums a consumer can re-derive
    manifest = {
        "artefact": whl.name,
        "sha256": _sha256(whl.read_bytes()),
        "bytes": whl.stat().st_size,
        "members": member_hashes,
        "member_count": len(member_hashes),
        "product_digest": _sha256(_canonical_json([[k, member_hashes[k]] for k in sorted(member_hashes)]).encode()),
        "entry_points": {"pipd": "pipd_ls_sp.cli:main"},
        "requires_dist": ["jsonschema>=4.0"],
        "licence": "LicenseRef-PIPD-Proprietary",
        "built_by": "hand-built PEP 427 (no build backend available offline)",
        "candidate_head": _candidate_head(),
    }
    (DIST / "WHEEL_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1),
                                              encoding="utf-8", newline="")
    sha = DIST / f"{whl.name}.sha256"
    sha.write_text(f"{manifest['sha256']}  {whl.name}\n", encoding="utf-8", newline="")
    return manifest


def main() -> int:
    m = build_wheel()
    print(json.dumps({k: m[k] for k in ("artefact", "sha256", "bytes", "member_count", "product_digest",
                                        "candidate_head", "entry_points", "licence")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
