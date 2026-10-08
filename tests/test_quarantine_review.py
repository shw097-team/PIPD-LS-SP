"""Guard the quarantine review path (TT-PIPD-KNOWLEDGE-QUARANTINE).

The rule this pins: a review path may EXPLAIN a quarantine, it may never CLEAR one. A security control
that an agent can switch off is not a control. It also pins the concrete finding that motivated the
path - an unanchored key pattern matching the tail of an ordinary identifier.
"""
from __future__ import annotations
import json, re, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
AW = ROOT.parent


class QuarantineReview(unittest.TestCase):
    def setUp(self) -> None:
        self.rev = json.loads((ROOT / ".hgk" / "knowledge" / "QUARANTINE_REVIEW.json").read_text(encoding="utf-8"))

    def test_every_quarantined_source_is_covered(self) -> None:
        rep = json.loads((ROOT / ".hgk" / "knowledge" / "KNOWLEDGE_READY_REPORT.json").read_text(encoding="utf-8"))
        self.assertEqual(len(self.rev["review"]), len(rep["knowledge_index_readback"]["quarantined"]))

    def test_review_does_not_disable_any_control(self) -> None:
        self.assertEqual(self.rev["controls_disabled"], [])
        self.assertEqual(self.rev["verdict"], "PARTIAL")
        self.assertTrue(self.rev["owner_decision_required"])

    def test_no_live_secret_suspect_is_waved_through(self) -> None:
        self.assertEqual(self.rev["classification_counts"].get("LIVE_SECRET_SUSPECT", 0), 0)

    def test_unanchored_key_pattern_really_matches_an_identifier_tail(self) -> None:
        # reproduces the finding rather than trusting it
        f = AW / "知識庫/工程基座/GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2/KnowledgePack/05_SDD_ADR_TASKSPEC.md"
        if not f.exists():
            self.skipTest("source corpus not present")
        text = f.read_text(encoding="utf-8", errors="replace")
        naive = re.compile(r"sk-[A-Za-z0-9_-]{20,}")
        anchored = re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9]{20,}")
        self.assertGreater(len(list(naive.finditer(text))), 0)
        self.assertEqual(len(list(anchored.finditer(text))), 0,
                         "the anchored form must not match an identifier tail")


if __name__ == "__main__":
    unittest.main(verbosity=2)
