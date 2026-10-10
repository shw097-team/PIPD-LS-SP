#!/usr/bin/env python3
"""W5: every perf-budget entry carries provenance; an unprovenanced threshold is UNDECIDABLE."""
from __future__ import annotations

import json
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


class AdvisoryAndVotingRows(unittest.TestCase):
    """R5 S4 owner adjudication: the deciding row changed; the historical rows did not vanish."""

    def test_the_recorded_absolute_fail_is_advisory_not_voting(self):
        # The historical 343,547 > 20,000 row must still be measured, still read FAIL, and must no
        # longer decide. Deleting it, or greening it, would both be rewrites of the record.
        row = PB._row("context_bytes_per_artefact", 343547.0)
        self.assertEqual(row["verdict"], "FAIL")
        self.assertTrue(row["exceeded"])
        self.assertFalse(row["voting"])
        self.assertTrue(row.get("preserved"))
        self.assertIn("advisory_reason", row)

    def test_advisory_rows_cannot_turn_the_gate_green(self):
        # An advisory row's own verdict must not be able to lift or sink the overall verdict: the
        # overall verdict is computed over voting rows only (see main()).
        for metric in ("compile_chain_ms", "validate_19_contracts_ms", "cli_cold_start_ms"):
            with self.subTest(metric=metric):
                self.assertFalse(PB.PROVENANCE[metric]["voting"])

    def test_bytes_per_atom_is_the_voting_row_with_a_ratified_source(self):
        prov = PB.PROVENANCE["bytes_per_atom"]
        self.assertTrue(prov["voting"])
        self.assertEqual(prov["budget"], 2000)
        self.assertNotEqual(prov["source_of_truth"], "UNPROVENANCED")
        self.assertIn("OWNER_ADJUDICATION_R5_S4", prov["source_of_truth"])
        # Provenanced and within budget => PASS (not UNDECIDABLE).
        row = PB._row("bytes_per_atom", 1449.57, pi_bytes=343547, atoms=237)
        self.assertEqual(row["verdict"], "PASS")
        self.assertFalse(row["exceeded"])

    def test_the_rate_still_fails_over_its_budget(self):
        # Re-specifying the metric must not remove the gate: an over-rate artefact still FAILs.
        row = PB._row("bytes_per_atom", 4321.0)
        self.assertTrue(row["exceeded"])
        self.assertEqual(row["verdict"], "FAIL")
        self.assertNotEqual(PB.exit_code(PB.overall_verdict([row])), 0)

    def test_end_to_end_check_preserves_history_and_reports_the_rate(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = PB.main(["--check"])
        res = json.loads(buf.getvalue())
        self.assertEqual(res["voting_metrics"], ["bytes_per_atom"])
        self.assertIn("context_bytes_per_artefact", res["advisory_metrics"])
        self.assertEqual(res["historical"]["preserved_fails"], ["context_bytes_per_artefact"])
        self.assertIn("bytes_per_atom", [r["metric"] for r in res["rows"]])
        # The rate decides: it is within its ratified budget on this candidate.
        self.assertEqual(rc, 0)
        self.assertEqual(res["verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
