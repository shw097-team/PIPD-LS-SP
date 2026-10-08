"""Guard the tightened TechnologyAdmission contract and the 22 source-designated rulings.

The schema previously declared every field as `{}` (no type) and only 9 fields, while the source's
PKG-00 §9.2 defines a 24-column design record. A record could therefore be schema-valid and still
carry garbage. These tests pin the typed contract and the per-candidate negative fixture.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
from pipd_ls_sp import validate as V  # noqa: E402


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

    def test_source_pin_gate_is_honestly_partial_not_pass(self) -> None:
        # The source never license-verifies. Rounding that up to PASS would be an over-claim.
        self.assertEqual(self.adm["gate_summary"]["G-TECH-SOURCE-PIN"].split("/")[0], "0")
        self.assertEqual(self.adm["runtime_state"].split(" ")[0], "NOT_EXECUTED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
