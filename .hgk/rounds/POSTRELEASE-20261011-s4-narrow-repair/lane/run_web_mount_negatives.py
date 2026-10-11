#!/usr/bin/env python3
"""WO-S4-WEB-02 raw negative demonstrations: drive ``build_mount_pack.verify_pack`` on four mutations.

Prints each mutation's verify result verbatim so the receipt carries real output, not a claim. Writes
nothing outside a temporary directory.
"""
from __future__ import annotations

import hashlib
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from tools import build_mount_pack as BMP  # noqa: E402

PACK = ROOT / "dist" / "mount" / "pipd-ls-sp-s4-chatgpt-mount-v0.1.0-preview.2"
PACK_NAME = PACK.name


def rewrite(path: Path, members: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            info = zipfile.ZipInfo(name, date_time=BMP.FIXED_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            info.create_system = 0
            zf.writestr(info, data)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        base = tdp / "pack.zip"
        BMP.build_pack(PACK, base)
        with zipfile.ZipFile(base) as zf:
            base_members = {n: zf.read(n) for n in zf.namelist()}

        # NEG-1: mutate a member's bytes
        m1 = dict(base_members)
        key = f"{PACK_NAME}/references/PIPD_S4_CORE.md"
        m1[key] = m1[key] + b"\n<!-- tamper -->\n"
        p1 = tdp / "neg1.zip"
        rewrite(p1, m1)
        _report("NEG-1 mutated member", p1)

        # NEG-2: add a member that is not in the manifest
        m2 = dict(base_members)
        m2[f"{PACK_NAME}/EXTRA.md"] = b"leak\n"
        p2 = tdp / "neg2.zip"
        rewrite(p2, m2)
        _report("NEG-2 unmanifested member", p2)

        # NEG-3: remove a member that the manifest lists
        m3 = dict(base_members)
        del m3[f"{PACK_NAME}/references/PIPD_EXAMPLES.md"]
        p3 = tdp / "neg3.zip"
        rewrite(p3, m3)
        _report("NEG-3 manifest entry missing from ZIP", p3)

        # NEG-4: a path that escapes the pack root
        m4 = dict(base_members)
        m4["../evil.md"] = b"escape\n"
        p4 = tdp / "neg4.zip"
        rewrite(p4, m4)
        _report("NEG-4 path escapes pack root", p4)
    return 0


def _report(label: str, path: Path) -> None:
    ok, problems = BMP.verify_pack(path)
    print(f"===== {label} =====")
    print(f"verify_pack -> ok={ok} exit={'0' if ok else '1'}")
    for p in problems:
        print(f"  - {p}")
    print()


if __name__ == "__main__":
    raise SystemExit(main())
