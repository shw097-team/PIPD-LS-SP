#!/usr/bin/env python3
"""W5: every perf-budget entry carries provenance; an unprovenanced threshold is UNDECIDABLE."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

import perf_budget as PB  # noqa: E402


class PerfBudgetProvenance(unittest.TestCase):
    def test_unprovenanced_threshold_is_undecidable_not_pass(self):
        # A threshold with no in-repo provenance is UNDECIDABLE even when the measured value is
        # comfortably under it - an unratified budget cannot be turned green by a small number.
        verdict = PB._verdict(1.0, 2000, "UNPROVENANCED")
        self.assertEqual(verdict, "UNDECIDABLE")
        self.assertNotEqual(verdict, "PASS")
        self.assertNotEqual(verdict, "FAIL")
        # A provenanced threshold still decides normally.
        self.assertEqual(PB._verdict(1.0, 2000, "docs/S0_CONTRACT_SPEC.md#perf"), "PASS")
        self.assertEqual(PB._verdict(9999.0, 2000, "docs/S0_CONTRACT_SPEC.md#perf"), "FAIL")

    def test_exceeded_unprovenanced_budget_is_fail_and_exits_nonzero(self):
        # Fail-closed: an OVER-budget value is a fact about the artefact. Missing provenance must
        # not launder it into UNDECIDABLE/pass - it stays FAIL and the process exits non-zero.
        self.assertEqual(PB._verdict(9999.0, 2000, "UNPROVENANCED"), "FAIL")
        over = 343547.0  # the 20,000-byte context budget's real overrun
        row = PB._row("context_bytes_per_artefact", over)
        self.assertEqual(row["source_of_truth"], "UNPROVENANCED")
        self.assertTrue(row["exceeded"])
        self.assertEqual(row["verdict"], "FAIL")
        self.assertIn("note", row)
        self.assertEqual(PB.overall_verdict([row]), "FAIL")
        self.assertNotEqual(PB.exit_code("FAIL"), 0)

    def test_under_budget_unprovenanced_budget_is_undecidable_not_pass(self):
        row = PB._row("context_bytes_per_artefact", 10.0)
        self.assertFalse(row["exceeded"])
        self.assertEqual(row["verdict"], "UNDECIDABLE")
        self.assertNotEqual(row["verdict"], "PASS")
        self.assertEqual(PB.overall_verdict([row]), "UNDECIDABLE")
        self.assertEqual(PB.exit_code("UNDECIDABLE"), 0)

    def test_raw_overrun_not_rounded_away(self):
        # C7': a raw measurement of 2000.04 against the 2000 ms compile budget rounds to 2000.0 for
        # display, but the decision must use the UNROUNDED value, so it is flagged as exceeded.
        row = PB._row("compile_chain_ms", 2000.04)
        self.assertTrue(row["exceeded"], "raw 2000.04 > 2000 must be flagged exceeded")
        self.assertEqual(row["verdict"], "FAIL")
        self.assertEqual(row["budget"], 2000)
        self.assertEqual(row["value_display"], 2000.0)
        self.assertNotEqual(PB.exit_code(PB.overall_verdict([row])), 0)


if __name__ == "__main__":
    unittest.main()
