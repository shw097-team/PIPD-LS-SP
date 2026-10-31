"""The consumer must observe the swap; a version mismatch must refuse rather than call.

The claim WP-FHS-13 needs is narrow and checkable: after the occupant behind a Need is replaced, the *same consumer
object* answers with the new implementation and no longer with the old one. If that test passes, the ABI is wired; if
it passes only when the consumer is rebuilt, the consumer is caching and the swap was never observed.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pipd_ls_sp.abi import (  # noqa: E402
    ABI_VERSION, AbiDuplicateOccupant, AbiUnsatisfied, AbiVersionMismatch,
    Consumer, Need, Occupant, Registry, make_consumer, occupant_from_file,
)

V1 = '''
class Impl:
    def render(self):
        return "v1"
def build():
    return Impl()
'''

V2 = '''
class Impl:
    def render(self):
        return "v2"
def build():
    return Impl()
'''

WRONG_VERSION = '''
class Impl:
    def render(self):
        return "v99"
def build():
    return Impl()
'''

NO_METHOD = '''
class Impl:
    def something_else(self):
        return "x"
def build():
    return Impl()
'''


class AbiTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pipd-abi-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, True))

    def _file(self, name: str, body: str) -> Path:
        p = self.tmp / name
        p.write_text(body, encoding="utf-8")
        return p

    def test_consumer_reaches_the_occupant(self):
        need = Need("renderer", ABI_VERSION, ("render",))
        c = make_consumer(need, self._file("v1.py", V1))
        self.assertEqual(c("render"), "v1")

    def test_the_same_consumer_observes_a_swap(self):
        need = Need("renderer", ABI_VERSION, ("render",))
        reg = Registry()
        reg.bind(occupant_from_file(need, self._file("v1.py", V1)))
        consumer = Consumer(need, reg)                      # built ONCE, before the swap
        self.assertEqual(consumer("render"), "v1")

        reg.bind(occupant_from_file(need, self._file("v2.py", V2)), replace=True)
        self.assertEqual(consumer("render"), "v2", "a consumer built before the swap must see the new occupant")

        # NEG: the old implementation is no longer what this consumer reaches.
        self.assertNotEqual(consumer("render"), "v1")

    def test_serves_reports_pos_and_neg_with_origin(self):
        need = Need("renderer", ABI_VERSION, ("render",))
        c = make_consumer(need, self._file("v1.py", V1))
        pos = c.serves("render")
        self.assertTrue(pos["ok"])
        self.assertEqual(pos["value"], "v1")
        self.assertIn("v1.py", pos["origin"])
        neg = c.serves("no_such_method")
        self.assertFalse(neg["ok"])
        self.assertEqual(neg["code"], "ERR_ABI_UNSATISFIED")

    def test_version_mismatch_refuses_instead_of_calling(self):
        need = Need("renderer", ABI_VERSION, ("render",))
        occ = Occupant(need=Need("renderer", ABI_VERSION + 1, ("render",)),
                       impl=type("I", (), {"render": lambda self: "v99"})(), origin="wrong-version")
        reg = Registry()
        reg.bind(occ)
        with self.assertRaises(AbiVersionMismatch):
            reg.resolve(need)

    def test_missing_method_refuses(self):
        need = Need("renderer", ABI_VERSION, ("render",))
        reg = Registry()
        reg.bind(occupant_from_file(need, self._file("nomethod.py", NO_METHOD)))
        with self.assertRaises(AbiVersionMismatch):
            reg.resolve(need)

    def test_duplicate_occupant_refuses_unless_replacing(self):
        need = Need("renderer", ABI_VERSION, ("render",))
        reg = Registry()
        reg.bind(occupant_from_file(need, self._file("v1.py", V1)))
        with self.assertRaises(AbiDuplicateOccupant):
            reg.bind(occupant_from_file(need, self._file("v2.py", V2)))
        reg.bind(occupant_from_file(need, self._file("v2.py", V2)), replace=True)
        self.assertEqual(Consumer(need, reg)("render"), "v2")

    def test_missing_file_is_a_named_refusal(self):
        need = Need("renderer", ABI_VERSION, ("render",))
        with self.assertRaises(AbiUnsatisfied) as ctx:
            occupant_from_file(need, self.tmp / "absent.py")
        self.assertEqual(ctx.exception.code, "ERR_ABI_UNSATISFIED")


if __name__ == "__main__":
    unittest.main()
