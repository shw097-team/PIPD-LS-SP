"""Guard the tightened TechnologyAdmission contract and the 22 source-designated rulings.

The schema previously declared every field as `{}` (no type) and only 9 fields, while the source's
PKG-00 §9.2 defines a 24-column design record. A record could therefore be schema-valid and still
carry garbage. These tests pin the typed contract, the per-candidate negative fixture, and the
R-AUD-007 repair: every row carries a pin/licence/TTL/fallback/exit/permission/provider-off/
disposition, and only a pinned ADOPT row may be reported active (MUT-TECH-PIN is refused by name).
"""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
from pipd_ls_sp import validate as V  # noqa: E402
import admit_technologies as A  # noqa: E402


class TechnologyAdmissionContract(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads((ROOT / "schemas" / "TechnologyAdmission.schema.json").read_text(encoding="utf-8"))
        self.adm = json.loads((ROOT / ".hgk" / "artifacts" / "s1" / "TECHNOLOGY_ADMISSIONS.json")
                              .read_text(encoding="utf-8"))

    def test_schema_is_typed_not_wildcard(self) -> None:
        wildcards = [k for k, v in self.schema["properties"].items() if v == {}]
        self.assertEqual(wildcards, [], f"untyped properties: {wildcards}")

    def test_schema_covers_the_source_design_record(self) -> None:
        for field in ("technology_id", "external_name", "capability_slot", "license",
                      "immutable_pin", "rollback_plan", "security_requirements"):
            self.assertIn(field, self.schema["properties"], field)

    def test_twenty_two_rulings_present_and_valid(self) -> None:
        self.assertEqual(len(self.adm["admissions"]), 22)
        for rec in self.adm["admissions"]:
            res = V.validate_bundle({"TechnologyAdmission": rec}, schemas_dir=ROOT / "schemas")
            self.assertEqual(res["verdict"], "PASS", f"{rec['technology_id']}: {res}")

    def test_every_candidate_has_a_rejected_negative_fixture(self) -> None:
        for g in self.adm["gates"]:
            cid = g["candidate"]
            fix = ROOT / "fixtures" / cid / "mutation-unpinned.json"
            self.assertTrue(fix.exists(), cid)
            bad = json.loads(fix.read_text(encoding="utf-8"))
            self.assertIn(bad["immutable_pin"], ("LATEST",), cid)
            neg = [x for x in g["gates"] if x["gate"] == "G-TECH-NEGATIVE"][0]
            self.assertEqual(neg["verdict"], "PASS", cid)
            # MUT-TECH-PIN must be the named mutation.
            self.assertEqual(neg["fixture_mutation"], "MUT-TECH-PIN", cid)

    def test_source_pin_gate_is_honestly_partial_not_pass(self) -> None:
        # The source never license-verifies. Rounding that up to PASS would be an over-claim.
        self.assertEqual(self.adm["gate_summary"]["G-TECH-SOURCE-PIN"].split("/")[0], "0")
        self.assertEqual(self.adm["runtime_state"].split(" ")[0], "NOT_EXECUTED")


class TechnologyAdmissionRepair(unittest.TestCase):
    """R-AUD-007: the 22 rows must carry a real pin/licence/TTL/... and only pinned ADOPT activates."""

    REQUIRED_COLUMNS = ("pin", "license", "ttl_security_note", "fallback", "exit_criterion",
                        "permission_scope", "provider_off_behaviour", "disposition")

    def setUp(self) -> None:
        self.adm = json.loads((ROOT / ".hgk" / "artifacts" / "s1" / "TECHNOLOGY_ADMISSIONS.json")
                              .read_text(encoding="utf-8"))
        self.rows = self.adm["admissions"]

    def _pinned_adopt(self) -> dict:
        """A fully pinned, licence-known, active ADOPT row (the positive case)."""
        rec = copy.deepcopy(self.rows[0])
        plc = rec["pin_license_currentness"]
        plc["pin"] = {"value": "v2026.10.09", "repository": "https://example.invalid/pinned",
                      "reason_code": "EXACT_PIN", "reason": ""}
        plc["license"] = {"value": "Apache-2.0", "known": True, "blocks_activation": False,
                          "disposition": "LICENCE_DECLARED_AT_SOURCE"}
        plc["disposition"] = "ADOPT"
        plc["reported_active"] = True
        return rec

    def test_every_row_carries_every_required_column(self) -> None:
        valid = {"ADOPT", "REFERENCE", "EVAL_ONLY", "QUARANTINE", "REJECT"}
        for rec in self.rows:
            plc = rec.get("pin_license_currentness")
            self.assertIsInstance(plc, dict, rec["technology_id"])
            for col in self.REQUIRED_COLUMNS:
                self.assertIn(col, plc, f"{rec['technology_id']} missing {col}")
                self.assertTrue(str(plc[col]).strip() not in ("", "None"),
                                f"{rec['technology_id']} empty {col}")
            self.assertIn(plc["disposition"], valid, rec["technology_id"])
            # an unverified pin is the literal UNAVAILABLE carrying a machine-readable reason
            if not plc["pin_verified"]:
                self.assertEqual(plc["pin"]["value"], "UNAVAILABLE", rec["technology_id"])
                self.assertTrue(plc["pin"].get("reason_code"), rec["technology_id"])
            # an unknown licence must carry the blocking disposition
            if not plc["licence_known"]:
                self.assertTrue(plc["license"]["blocks_activation"], rec["technology_id"])

    def test_no_non_adopt_row_is_reported_active(self) -> None:
        for rec in self.rows:
            plc = rec["pin_license_currentness"]
            if plc["disposition"] != "ADOPT":
                self.assertFalse(plc["reported_active"],
                                 f"{rec['technology_id']} ({plc['disposition']}) reported active")

    def test_positive_fully_pinned_adopt_row_passes(self) -> None:
        v = A.row_verdict(self._pinned_adopt())
        self.assertEqual(v["disposition"], "ADOPT")
        self.assertTrue(v["pin_verified"])
        self.assertTrue(v["source_pin_pass"])
        self.assertFalse(v["active_refused"])

    def test_mut_tech_pin_is_refused_and_named(self) -> None:
        # MUT-TECH-PIN: a row whose pin contradicts its active claim must be refused by name.
        bad = json.loads((ROOT / "fixtures" / "CAND-01" / "mutation-unpinned.json").read_text(encoding="utf-8"))
        v = A.row_verdict(bad)
        self.assertTrue(v["claims_active"])
        self.assertTrue(v["active_refused"], "MUT-TECH-PIN active claim was not refused")
        neg = A.gate_negative(self.rows[0], bad)
        self.assertEqual(neg["verdict"], "PASS")
        self.assertEqual(neg["fixture_mutation"], "MUT-TECH-PIN")

    def test_unknown_licence_activation_is_blocked(self) -> None:
        rec = self._pinned_adopt()
        rec["pin_license_currentness"]["license"] = {
            "value": "UNKNOWN", "known": False, "blocks_activation": True,
            "disposition": "UNKNOWN_LICENCE_BLOCKS_ACTIVATION"}
        v = A.row_verdict(rec)
        self.assertTrue(v["pin_verified"])
        self.assertFalse(v["licence_known"])
        self.assertTrue(v["active_refused"], "activation under an unknown licence was allowed")

    def test_non_adopt_row_reported_active_is_refused(self) -> None:
        rec = self._pinned_adopt()
        rec["pin_license_currentness"]["disposition"] = "REFERENCE"
        v = A.row_verdict(rec)
        self.assertEqual(v["disposition"], "REFERENCE")
        self.assertTrue(v["active_refused"],
                        "a non-ADOPT (REFERENCE) row reported active was not refused")


if __name__ == "__main__":
    unittest.main(verbosity=2)
