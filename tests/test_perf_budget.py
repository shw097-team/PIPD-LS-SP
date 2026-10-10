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


class HistoricalRecordedValue(unittest.TestCase):
    """D1 repair: the `historical` block must report the RECORDED value, not a live host reading.

    The historical 343,547 > 20,000 row is a record; a record that changes with the machine that
    happens to run it is not a record. `value` is read from the frozen baseline at test time (never
    hard-coded here) and the live measurement is carried beside it as `measured_now`.
    """

    def _baseline(self):
        path = ROOT / ".hgk" / "artifacts" / "s2" / "BYTES_PER_ATOM_BASELINE.json"
        self.assertTrue(path.exists(), f"baseline artefact must exist: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _historical_row(self, metric):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = PB.main(["--check"])
        self.assertEqual(rc, 0)
        res = json.loads(buf.getvalue())
        rows = {r["metric"]: r for r in res["historical"]["rows"]}
        self.assertIn(metric, rows)
        return rows[metric]

    def test_historical_value_is_the_recorded_baseline_not_the_measurement(self):
        baseline = self._baseline()
        expected = baseline["pi_bytes"]  # 343547, read from the artefact - never hard-coded
        row = self._historical_row("context_bytes_per_artefact")
        self.assertEqual(row["value"], expected)
        self.assertTrue(row["recorded"])
        self.assertEqual(row["origin"],
                         {"file": ".hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json",
                          "field": "pi_bytes"})
        # The verdict is decided from the RECORDED value against the UNCHANGED budget.
        self.assertEqual(row["verdict"], "FAIL")
        self.assertEqual(row["budget"], 20000)
        self.assertTrue(row["exceeded"])

    def test_historical_value_is_stable_across_live_measurements(self):
        baseline = self._baseline()
        expected = baseline["pi_bytes"]
        first = self._historical_row("context_bytes_per_artefact")
        second = self._historical_row("context_bytes_per_artefact")
        # `measured_now` is present and honest; `value` never follows it.
        self.assertIn("measured_now", first)
        self.assertIn("measured_now", second)
        self.assertEqual(first["value"], expected)
        self.assertEqual(second["value"], expected)
        # Sanity: if the live reading ever differed, `value` would still be the record.
        if first["measured_now"] != first["value"]:
            self.assertEqual(first["value"], expected)

    def test_unrecorded_advisory_metric_says_so_instead_of_fabricating(self):
        row = self._historical_row("compile_chain_ms")
        self.assertFalse(row["recorded"])
        self.assertIsNone(row["origin"])
        self.assertEqual(row["value"], row["measured_now"])
        self.assertEqual(row["budget"], 2000)
        self.assertIn("note", row)
        self.assertIn("no recorded value", row["note"])

    def test_no_source_comment_claims_verbatim_preservation_of_the_live_value(self):
        # Targeted, not a broad grep: the two corrected strings must describe what the code does.
        source = (ROOT / "tools" / "perf_budget.py").read_text(encoding="utf-8")
        self.assertNotIn("343,547 > 20,000 FAIL is preserved verbatim", source)
        self.assertNotIn("preserved verbatim and must never be rewritten", source)
        # The correction is present rather than the claim merely deleted.
        self.assertIn("RECORDED", source)
        self.assertIn("measured_now", source)


if __name__ == "__main__":
    unittest.main()
