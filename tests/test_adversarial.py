"""Adversarial suite: the tree tries to break its own packager.

`ASSURANCE.json` lists `adversarial` as NOT DECLARED, and the ASSURED profile therefore refuses. That refusal was
correct while the claim was empty. This suite is the claim: each test is an attack a consumer could actually mount
against the packager or the ABI, and each must be REFUSED with a named error rather than handled gracefully.

An adversarial suite that only checks happy paths with ugly names is not adversarial. These are the four shapes that
matter for a bundler: escape the root, smuggle a member in, corrupt what was promised, and satisfy a contract you do
not implement.
"""
from __future__ import annotations

import io
import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pipd_ls_sp.abi import ABI_VERSION, Need, Occupant, Registry, AbiVersionMismatch  # noqa: E402
from pipd_ls_sp.errors import ExportMemberUnsafe  # noqa: E402
from pipd_ls_sp.export_bundle import (  # noqa: E402
    ExportVerificationFailed, apply_depth, collect_source_files, _verify_members,
)


class EscapeAttempts(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pipd-adv-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, True))
        (self.tmp / "inside.txt").write_text("ok", encoding="utf-8")
        (self.tmp / ".." / "outside.txt").write_text("secret", encoding="utf-8")

    def test_dotdot_in_include_is_refused_not_filtered(self):
        """`../outside.txt` must be REFUSED. Measured: the packager raises ExportMemberUnsafe, which is the stronger
        behaviour -- silently filtering would leave the caller believing the member was included."""
        with self.assertRaises(ExportMemberUnsafe):
            collect_source_files(self.tmp, ["../outside.txt"])

    def test_absolute_include_never_yields_an_absolute_member(self):
        """An absolute include may be accepted only if the member path it produces is relative to the root."""
        abs_path = str(self.tmp / "inside.txt")
        try:
            members = collect_source_files(self.tmp, [abs_path])
        except ExportMemberUnsafe:
            return                      # refused outright: also correct, and stricter
        for rel, _ in members:
            self.assertFalse(Path(str(rel)).is_absolute(), f"absolute member path: {rel}")


class SmuggledMember(unittest.TestCase):
    def test_an_extra_archive_member_is_not_silently_ignored(self):
        """The verifier must fail when the archive holds something the manifest never promised."""
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tf:
            for name, data in (("a.txt", b"a"), ("smuggled.txt", b"x")):
                info = tarfile.TarInfo(name)
                info.size = len(data)
                tf.addfile(info, io.BytesIO(data))
        rows = [{"rel": "a.txt", "sha256": __import__("hashlib").sha256(b"a").hexdigest(), "size": 1}]
        # _verify_members checks that promised members are present and correct; an extra member is the attack.
        try:
            _verify_members(buf.getvalue(), rows)
        except ExportVerificationFailed:
            return
        # If it passes, the extra member survived -- record that as the finding rather than asserting silently.
        with tarfile.open(fileobj=io.BytesIO(buf.getvalue())) as tf:
            names = tf.getnames()
        self.assertEqual(sorted(names), ["a.txt"], f"extra members survived verification: {names}")


class CorruptedPromise(unittest.TestCase):
    def test_a_tampered_member_digest_is_refused(self):
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tf:
            data = b"payload"
            info = tarfile.TarInfo("a.txt")
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
        rows = [{"rel": "a.txt", "sha256": "0" * 64, "size": 7}]
        with self.assertRaises(ExportVerificationFailed):
            _verify_members(buf.getvalue(), rows)

    def test_an_unknown_depth_never_degrades_into_ship_everything(self):
        with self.assertRaises(ValueError):
            apply_depth([("src/x.py", self)][:0] + [("src/x.py", Path("x"))], "L9_INVENTED")


class ContractYouDoNotImplement(unittest.TestCase):
    def test_an_occupant_claiming_a_newer_contract_is_refused(self):
        """The ABI attack: answer a contract you do not implement and hope the caller does not check."""
        need = Need("svc", ABI_VERSION, ("run",))
        liar = Occupant(need=Need("svc", ABI_VERSION + 1, ("run",)),
                        impl=type("I", (), {"run": lambda self: "ok"})(), origin="liar")
        reg = Registry()
        reg.bind(liar)
        with self.assertRaises(AbiVersionMismatch):
            reg.resolve(need)

    def test_an_occupant_missing_a_required_method_is_refused_not_duck_typed(self):
        need = Need("svc", ABI_VERSION, ("run", "audit"))
        partial = Occupant(need=Need("svc", ABI_VERSION, ("run",)),
                           impl=type("I", (), {"run": lambda self: "ok"})(), origin="partial")
        reg = Registry()
        reg.bind(partial)
        with self.assertRaises(AbiVersionMismatch):
            reg.resolve(need)


class NonRegularMember(unittest.TestCase):
    def test_an_unlisted_symlink_member_is_refused(self):
        """Found by the independent checker (VERIFY_SECURITY, gpt-6.1-sol, PIPD-AO-E167D692): my first hardening
        refused an unlisted REGULAR file but accepted an unlisted SYMLINK. A symlink member is an escape."""
        import hashlib
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tf:
            data = b"a"
            info = tarfile.TarInfo("a.txt"); info.size = len(data); tf.addfile(info, io.BytesIO(data))
            link = tarfile.TarInfo("escape"); link.type = tarfile.SYMTYPE; link.linkname = "C:/Windows/win.ini"
            tf.addfile(link)
        rows = [{"rel": "a.txt", "sha256": hashlib.sha256(b"a").hexdigest(), "size": 1}]
        with self.assertRaises(ExportVerificationFailed):
            _verify_members(buf.getvalue(), rows)

    def test_a_directory_member_is_refused(self):
        import hashlib
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tf:
            data = b"a"
            info = tarfile.TarInfo("a.txt"); info.size = len(data); tf.addfile(info, io.BytesIO(data))
            d = tarfile.TarInfo("adir/"); d.type = tarfile.DIRTYPE
            tf.addfile(d)
        rows = [{"rel": "a.txt", "sha256": hashlib.sha256(b"a").hexdigest(), "size": 1}]
        with self.assertRaises(ExportVerificationFailed):
            _verify_members(buf.getvalue(), rows)


if __name__ == "__main__":
    unittest.main()
