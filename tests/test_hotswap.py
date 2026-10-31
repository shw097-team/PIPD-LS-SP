"""HotSwap must prove parity, and a refused swap must leave the world as it found it.

WP-FHS-13's first-fail is `CAPABILITY_PARITY_NOT_PROVEN` -- "熱替代 Issuer 或以選型當 invoke". The point of the
clause is that a swap is not a capability change until the new occupant SERVES and the old one STOPS serving.
These tests hold both directions, plus the rollback, because a swap tool that only reports success is worse than no
swap tool at all.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "hotswap.py"

OCCUPANT = '''import sys
if "--identity" in sys.argv:
    print("occupant-A")
    raise SystemExit(0)
'''

CANDIDATE = '''import sys
if "--identity" in sys.argv:
    print("occupant-B")
    raise SystemExit(0)
'''

BROKEN = '''import sys
raise SystemExit(3)
'''


def run(root: Path, candidate: Path, expect_old="occupant-A", expect_new="occupant-B") -> tuple[int, dict]:
    out = root.parent / "receipt.json"
    res = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--candidate", str(candidate),
                          "--expect-old", expect_old, "--expect-new", expect_new, "--out", str(out)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
    return res.returncode, json.loads(out.read_text(encoding="utf-8"))


class TestHotSwap(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.base = Path(self.td.name)
        self.root = self.base / "target"
        self.root.mkdir()
        (self.root / "occupant.py").write_text(OCCUPANT, encoding="utf-8")
        (self.root / "asset.txt").write_text("the target root carries other state\n", encoding="utf-8")

    def tearDown(self):
        self.td.cleanup()

    def test_a_good_swap_proves_pos_and_neg(self):
        cand = self.base / "candidate.py"
        cand.write_text(CANDIDATE, encoding="utf-8")
        code, r = run(self.root, cand)
        self.assertEqual(code, 0, r.get("why"))
        self.assertTrue(r["ok"])
        self.assertEqual(r["pos"]["identity"], "occupant-B")
        self.assertEqual(r["control"]["identity"], "occupant-A",
                         "the control must show the target served the OLD capability before the swap")
        self.assertNotEqual(r["neg"]["identity"], "occupant-A",
                            "after the swap the target must no longer serve the old capability")
        self.assertEqual(r["rollback"], "not needed")

    def test_the_swap_actually_replaced_the_entry(self):
        cand = self.base / "candidate.py"
        cand.write_text(CANDIDATE, encoding="utf-8")
        run(self.root, cand)
        self.assertIn("occupant-B", (self.root / "occupant.py").read_text(encoding="utf-8"))

    def test_a_wrong_expectation_is_refused_before_anything_moves(self):
        cand = self.base / "candidate.py"
        cand.write_text(CANDIDATE, encoding="utf-8")
        code, r = run(self.root, cand, expect_old="occupant-Z")
        self.assertEqual(code, 1)
        self.assertEqual(r["code"], "ERR_OCCUPANT_MISMATCH")
        self.assertIn("occupant-A", (self.root / "occupant.py").read_text(encoding="utf-8"),
                      "a refused bind must not touch the target")

    def test_a_candidate_that_does_not_serve_is_refused_and_rolled_back(self):
        cand = self.base / "broken.py"
        cand.write_text(BROKEN, encoding="utf-8")
        before = (self.root / "occupant.py").read_text(encoding="utf-8")
        code, r = run(self.root, cand)
        self.assertEqual(code, 1)
        self.assertEqual(r["code"], "CAPABILITY_PARITY_NOT_PROVEN")
        self.assertTrue(r["rollback"]["restored"], "the preimage must come back")
        self.assertEqual((self.root / "occupant.py").read_text(encoding="utf-8"), before)

    def test_other_state_in_the_root_survives_a_rollback(self):
        cand = self.base / "broken.py"
        cand.write_text(BROKEN, encoding="utf-8")
        run(self.root, cand)
        self.assertTrue((self.root / "asset.txt").is_file())
        self.assertEqual((self.root / "asset.txt").read_text(encoding="utf-8"),
                         "the target root carries other state\n")


if __name__ == "__main__":
    unittest.main()
