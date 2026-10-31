"""The three SPs must be three capabilities, not three labels.

The delivery names 三 SP (LITE / STANDARD / ASSURED) and WP-FHS-11 counts cells per host per SP. The packager
emitted exactly one bundle and never consulted profiles.py, so the 9-cell denominator was unreachable for a reason
that had nothing to do with hosts.

The obvious wrong fix is a `--profile` flag that rewrites a manifest field: three bundles with three names and one
capability. These tests exist to make that fix fail. Requesting assurance a tree does not evidence is a veto.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pipd_ls_sp.errors import ProfileVeto  # noqa: E402
from pipd_ls_sp.export_bundle import enforce_profile, plan, write_bundle  # noqa: E402

FULL = {"capabilities": ["deterministic_validator", "negative_security", "adversarial", "independent_checker"],
        "evidence": {"negative_security": "tests/neg", "adversarial": "tests/adv",
                     "independent_checker": "receipts/checker.json"}}
STANDARD_ONLY = {"capabilities": ["deterministic_validator", "negative_security"],
                 "evidence": {"negative_security": "tests/neg"}}


class TestProfileEnforcement(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name) / "tree"
        self.root.mkdir()
        (self.root / "SKILL.md").write_text("# a bundle member\n", encoding="utf-8")

    def tearDown(self):
        self.td.cleanup()

    def declare(self, payload):
        (self.root / "ASSURANCE.json").write_text(json.dumps(payload), encoding="utf-8")

    def test_lite_needs_no_declaration_because_the_packager_is_the_validator(self):
        prof = enforce_profile(self.root, "LITE")
        self.assertEqual(prof["profile"], "LITE")
        self.assertFalse(prof["assurance_declaration_present"])
        self.assertEqual(prof["assurance_required"], ["deterministic_validator"])

    def test_asserting_assured_without_evidence_is_refused(self):
        with self.assertRaises(ProfileVeto) as ctx:
            enforce_profile(self.root, "ASSURED")
        self.assertIn("adversarial", str(ctx.exception))

    def test_asserting_assured_with_full_evidence_passes(self):
        self.declare(FULL)
        prof = enforce_profile(self.root, "ASSURED")
        self.assertEqual(prof["profile"], "ASSURED")
        self.assertEqual(prof["assurance_evidence"]["adversarial"], "tests/adv")

    def test_a_partial_declaration_cannot_be_escalated_into_assured(self):
        self.declare(STANDARD_ONLY)
        self.assertEqual(enforce_profile(self.root, "STANDARD")["profile"], "STANDARD")
        with self.assertRaises(ProfileVeto):
            enforce_profile(self.root, "ASSURED")

    def test_provider_off_escalates_lite_to_standard_and_enforces_the_new_floor(self):
        with self.assertRaises(ProfileVeto):
            enforce_profile(self.root, "LITE", provider_off_required=True)
        self.declare(STANDARD_ONLY)
        prof = enforce_profile(self.root, "LITE", provider_off_required=True)
        self.assertEqual(prof["profile"], "STANDARD")
        self.assertTrue(prof["escalated"])
        self.assertEqual(prof["escalation_reason"], "provider_off_parity")

    def test_plan_reports_the_profile_and_refuses_the_same_way(self):
        self.assertEqual(plan(self.root, profile="LITE")["profile"]["profile"], "LITE")
        with self.assertRaises(ProfileVeto):
            plan(self.root, profile="ASSURED")

    def test_write_bundle_records_the_profile_in_the_manifest(self):
        self.declare(STANDARD_ONLY)
        target = Path(self.td.name) / "dist" / "sp-standard"
        res = write_bundle(self.root, target, authorized_roots=[Path(self.td.name) / "dist"],
                           allow_replace=True, profile="STANDARD")
        self.assertEqual(res["verdict"], "PASS")
        self.assertEqual(res["profile"], "STANDARD")
        man = json.loads((target / "export_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(man["profile"]["profile"], "STANDARD")
        self.assertEqual(man["profile"]["assurance_declared"], ["deterministic_validator", "negative_security"])

    def test_an_unevidenced_profile_writes_nothing_at_all(self):
        target = Path(self.td.name) / "dist" / "sp-assured"
        with self.assertRaises(ProfileVeto):
            write_bundle(self.root, target, authorized_roots=[Path(self.td.name) / "dist"],
                         allow_replace=True, profile="ASSURED")
        self.assertFalse(target.exists(), "a refused profile must not leave a bundle on disk")


if __name__ == "__main__":
    unittest.main()
