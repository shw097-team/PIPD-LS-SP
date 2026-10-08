"""Guard the tooling surface that the artefact suites do not exercise.

Why this test exists: a repo-wide line-ending repair accidentally added `newline=""` to
`Path.read_text` calls in tools/cli_smoke.py. `Path.read_text` does not accept that keyword, so the
CLI smoke runner crashed with TypeError. Nothing caught it: the unit suite does not execute
tools/*.py, and the independent checker was (correctly) told not to run tools that write into the
repo. A whole directory of executable tooling was therefore unverified.

These tests are cheap and execute the tooling for real.
"""
from __future__ import annotations

import py_compile
import subprocess
import sys
import unittest
from pathlib import Path

# Self-bootstrap, same rule as every other test file here: a test file must be runnable standalone.
# An independent checker had to run this one with PYTHONPATH=src, which is exactly the defect the
# previous round flagged in another test file. Relying on a sibling's import side effects is not ok.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class TestToolingExecutes(unittest.TestCase):
    def test_every_module_compiles(self) -> None:
        bad: list[str] = []
        for d in (ROOT / "src", ROOT / "tools", ROOT / "tests"):
            for f in sorted(d.rglob("*.py")):
                try:
                    py_compile.compile(str(f), doraise=True, cfile=str(f.with_suffix(".pyc.tmp")))
                except py_compile.PyCompileError as exc:
                    bad.append(f"{f.relative_to(ROOT)}: {exc}")
                finally:
                    f.with_suffix(".pyc.tmp").unlink(missing_ok=True)
        self.assertEqual(bad, [], "modules failed to compile")

    def test_cli_smoke_runs(self) -> None:
        """The 13-command CLI surface must actually execute, not just import."""
        r = subprocess.run([sys.executable, "-B", "tools/cli_smoke.py"], cwd=str(ROOT),
                           capture_output=True, text=True,
                           env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(r.returncode, 0,
                         f"cli_smoke.py exited {r.returncode}\n{(r.stderr or r.stdout)[-800:]}")

    def test_no_read_text_receives_newline(self) -> None:
        """Pin the specific defect: Path.read_text takes no `newline` keyword."""
        offenders = []
        for d in (ROOT / "src", ROOT / "tools", ROOT / "tests"):
            for f in sorted(d.rglob("*.py")):
                text = f.read_text(encoding="utf-8")
                i = 0
                while True:
                    j = text.find(".read_text(", i)
                    if j < 0:
                        break
                    k = j + len(".read_text(")
                    depth, c = 1, k
                    while depth > 0 and c < len(text):
                        depth += (text[c] == "(") - (text[c] == ")")
                        c += 1
                    if "newline=" in text[k:c]:
                        offenders.append(str(f.relative_to(ROOT)))
                        break
                    i = c
        self.assertEqual(offenders, [], "read_text() was given a `newline` argument")


    def test_tracked_file_metric_excludes_vcs_internals(self) -> None:
        """Pin the other class a checker caught: a file-count metric that counted .git objects.

        `tracked_files` used to be `rglob('*')` over the whole root, so it moved on every git repack
        and reported hundreds of version-control internals as project files.
        """
        import subprocess as sp
        from pipd_ls_sp.cli import _tracked_file_count

        n = _tracked_file_count(ROOT)
        tracked = [l for l in sp.run(["git", "-C", str(ROOT), "ls-files"],
                                     capture_output=True, text=True).stdout.splitlines() if l.strip()]
        self.assertEqual(n, len(tracked), "tracked_files must equal `git ls-files`, not rglob('*')")
        self.assertLess(n, 1000, "tracked_files looks like it is counting .git internals again")

    def test_export_manifest_has_no_vcs_paths(self) -> None:
        from pipd_ls_sp import workspace

        bundle = workspace.export_manifest(ROOT, include=["."])
        paths = [row["rel"] for row in bundle.get("files", [])]
        self.assertTrue(paths, "export bundle produced no rows")
        def _is_vcs_internal(p: str) -> bool:
            # `.git/...` is a version-control internal. `.gitattributes` / `.gitignore` are ordinary
            # project files that merely start with the same four characters - an earlier version of
            # this predicate flagged them and failed on a correct tree.
            return p == ".git" or p.startswith(".git/") or "/.git/" in p

        leaked = [p for p in paths if _is_vcs_internal(p)]
        self.assertEqual(leaked, [], "export manifest leaked version-control internals")
        self.assertGreater(len(paths), 50,
                           "include=['.'] must walk the tree; a tiny result means the walk was skipped")

    def test_every_test_file_bootstraps_sys_path(self) -> None:
        """No test file may depend on a sibling importing src/ first."""
        missing = []
        for f in sorted((ROOT / "tests").glob("test_*.py")):
            src = f.read_text(encoding="utf-8")
            if "sys.path.insert" not in src:
                missing.append(f.name)
        self.assertEqual(missing, [], "test files without a sys.path bootstrap")


if __name__ == "__main__":
    unittest.main()
