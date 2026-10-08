"""S0: exact 19/19 machine-contract family tests (positive + negative)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pipd_ls_sp import registry, validate  # noqa: E402


class TestS0Contracts(unittest.TestCase):
    def setUp(self) -> None:
        self.reg = registry.load_registry(ROOT / "schemas")

    def test_exact_19_identity_and_order(self) -> None:
        names = [f["contract"] for f in self.reg["families"]]
        self.assertEqual(len(names), 19, "exact-set must be 19/19")
        self.assertEqual(len(set(names)), 19, "no duplicates")
        self.assertEqual(names, registry.SOURCE_ORDER, "order must match §7.3")

    def test_every_schema_is_draft_2020_12_and_closed(self) -> None:
        for f in self.reg["families"]:
            schema = json.loads((ROOT / "schemas" / f"{f['contract']}.schema.json").read_text(encoding="utf-8"))
            self.assertIn("2020-12", schema.get("$schema", ""), f["contract"])
            self.assertFalse(schema.get("additionalProperties", True), f["contract"])
            self.assertEqual(schema.get("type"), "object")

    def test_registry_fields_are_enforced_by_schema(self) -> None:
        for f in self.reg["families"]:
            schema = json.loads((ROOT / "schemas" / f"{f['contract']}.schema.json").read_text(encoding="utf-8"))
            missing = set(f["required_fields"]) - set(schema.get("required", []))
            self.assertFalse(missing, f"{f['contract']} does not enforce {sorted(missing)}")

    def test_seam_only_materialization(self) -> None:
        mats = {f["contract"]: f["materialization"] for f in self.reg["families"]}
        self.assertEqual(mats["GENIEProjectionRef"], "SCHEMA_SEAM_ONLY_UNTIL_S6")
        self.assertEqual(mats["ExecutionBindingRef"], "SCHEMA_SEAM_ONLY_UNTIL_S5")
        self.assertEqual(mats["WorkOrderCandidate"], "REQUIRED_NOW_NONAUTHORITY")

    def test_a_twentieth_family_is_rejected(self) -> None:
        reg = json.loads(json.dumps(self.reg))
        reg["families"].append({"contract": "Invented", "required_fields": ["a"]})
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "registry.json").write_text(json.dumps(reg), encoding="utf-8")
            with self.assertRaises(registry.ValidationFail):
                registry.load_registry(Path(td))

    def test_negative_missing_schema_file_is_rejected(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            reg = json.loads(json.dumps(self.reg))
            for f in reg["families"]:
                (Path(td) / f"{f['contract']}.schema.json").write_text("{}", encoding="utf-8", newline="")
            reg["families"][0]["contract"] = "Renamed"
            (Path(td) / "registry.json").write_text(json.dumps(reg), encoding="utf-8")
            with self.assertRaises(registry.ValidationFail):
                registry.load_registry(Path(td))


if __name__ == "__main__":
    unittest.main(verbosity=2)
