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

ROOT = Path(__file__).resolve().parents[1]


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


if __name__ == "__main__":
    unittest.main()
