"""The profile axis must change the bytes, not just the label.

WP-FHS-11 was blocked on `BLOCKED_PROFILE_CONTENT`: `--profile LITE` and `--profile STANDARD` both shipped 79 files
with archive `a6b3c8b3bbdf`, so six of the nine host cells could not be measured -- there was no second artefact to
measure. `profiles.py` had declared `artifact_depth` all along; nothing consumed it.

These tests pin the consumer:
  * LITE ships strictly fewer members than STANDARD, and its member set is a subset of STANDARD's;
  * the two archives have different digests (the point of the axis);
  * ASSURED still refuses, because this tree does not declare the assurance it would need;
  * an unknown depth raises instead of silently shipping everything under a narrower label.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pipd_ls_sp.export_bundle import apply_depth, collect_source_files, write_bundle  # noqa: E402


class DepthTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pipd-depth-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def _bundle(self, profile: str) -> dict:
        target = self.tmp / profile.lower()
        write_bundle(ROOT, target, profile=profile)
        return json.loads((target / "export_manifest.json").read_text(encoding="utf-8"))

    def test_lite_is_strictly_smaller_and_a_subset_of_standard(self):
        lite = self._bundle("LITE")
        std = self._bundle("STANDARD")
        lite_rel = {r["rel"] for r in lite["files"]}
        std_rel = {r["rel"] for r in std["files"]}
        self.assertLess(len(lite_rel), len(std_rel), "LITE must ship strictly fewer members than STANDARD")
        self.assertEqual(lite_rel - std_rel, set(), "LITE must be a subset of STANDARD, not a different slice")

    def test_the_two_profiles_do_not_share_an_archive_digest(self):
        lite = self._bundle("LITE")
        std = self._bundle("STANDARD")
        self.assertNotEqual(lite["archive"]["sha256"], std["archive"]["sha256"],
                            "identical archives mean the profile axis is a label")

    def test_depth_is_recorded_in_the_manifest(self):
        self.assertEqual(self._bundle("LITE")["profile"]["artifact_depth"], "L1_SCHEMA_CONTRACT")
        self.assertEqual(self._bundle("STANDARD")["profile"]["artifact_depth"], "L3_INTEGRATION_RUNTIME")

    def test_assured_still_refuses_on_an_undeclared_tree(self):
        target = self.tmp / "assured"
        proc = subprocess.run([sys.executable, "-m", "pipd_ls_sp.cli", "export", "--out", str(target),
                               "--profile", "ASSURED"], cwd=str(ROOT), capture_output=True, text=True,
                              env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")})
        self.assertNotEqual(proc.returncode, 0, "ASSURED must refuse; this tree declares no independent checker")
        self.assertFalse((target / "export_manifest.json").exists(), "a refused profile must leave nothing on disk")

    def test_unknown_depth_raises_instead_of_shipping_everything(self):
        members = collect_source_files(ROOT, None)
        with self.assertRaises(ValueError):
            apply_depth(members, "L2_IMAGINARY")


if __name__ == "__main__":
    unittest.main()
