"""S4EXT-R1 (TT-S4EXT-004 / O007): the first-run path must work for a NEW user.

O007 of the external challenge was a NON_BLOCKING_OBSERVATION on the README's
"Run it: the whole compiler chain, copy-paste" block: it pinned the author's own environment
(``PY=/c/Users/user/...``, ``PYTHONPATH="C:/Projects/Agent_Workspace/PIPD-postrelease-wt/src"``,
``ART="C:/Users/user/AppData/Local/Temp/pipd-first-run"``), so a user without that workspace could
not copy-paste it, and the chain depended on an exported PYTHONPATH.

The repair ships ``examples/first-run/run.sh`` and ``run.ps1``: both derive every path from their own
location, refuse with a typed precondition error when the interpreter is unusable, create their
scratch workspace outside the checkout, and drive
``doctor -> intake -> compile-pi -> bind-pd -> compile-ecp -> compile-tqaep -> assemble -> validate``
plus a typed refusal. Their exit code is the contract: 0 only when every positive step exited 0 AND
the refusal exited non-zero.

This module runs BOTH scripts as a real subprocess from a CWD outside the repository with a scrubbed
environment (no PYTHONPATH), which is exactly what "a fresh user in a new shell" means here.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
EXAMPLES = ROOT / "examples" / "first-run"
RUN_SH = EXAMPLES / "run.sh"
RUN_PS1 = EXAMPLES / "run.ps1"

# Developer-environment literals that must never reappear in the portable path.
FORBIDDEN_LITERALS = ("C:/Users/user", "C:\\Users\\user", "Agent_Workspace",
                      "PIPD-postrelease-wt", "PIPD-postrelease")

PWSH_CANDIDATES = (
    "pwsh",
    r"C:\Program Files\PowerShell\7\pwsh.exe",
)
PWSH_GLOB = "~/.cache/codex-runtimes/*/native/powershell/pwsh"


def _td() -> tempfile.TemporaryDirectory:
    """A temp dir that tolerates the WinError 32 handle races a subprocess leaves behind."""
    return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


def _find_pwsh() -> str | None:
    found = shutil.which("pwsh")
    if found:
        return found
    for candidate in PWSH_CANDIDATES[1:]:
        if Path(candidate).is_file():
            return candidate
    for hit in Path(os.path.expanduser(PWSH_GLOB)).parent.glob("pwsh*"):
        if hit.is_file() and hit.suffix.lower() in ("", ".exe"):
            return str(hit)
    return None


def _clean_env(tmpdir: str) -> dict:
    """A fresh-user environment: PYTHONPATH (and every other PYTHON* var) is dropped.

    ``PYTHON`` is set to the interpreter running this suite so the test does not depend on which
    ``python`` the host's PATH happens to resolve to (on this host the PATH ``python`` is a Microsoft
    Store alias stub). That is an interpreter choice, not a developer path: the scripts still derive
    the checkout, the fixture and the scratch workspace themselves, and their precondition check is
    exercised separately by ``test_run_sh_refuses_when_the_interpreter_is_unusable``.
    """
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith("PYTHON")}
    env["PYTHON"] = sys.executable
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _native(path: Path) -> str:
    """A path a native (non-MSYS) binary can open: ``C:/Projects/...``.

    MSYS/Git-Bash eats backslashes in an unquoted argv word, so a native tool must be handed the
    forward-slash form — the reverse of what an MSYS *builtin* wants.
    """
    return str(path).replace("\\", "/")


def _msys(path: Path) -> str:
    """A path MSYS bash itself resolves as a script argument: ``/c/Projects/...``."""
    text = str(path).replace("\\", "/")
    if len(text) > 2 and text[1] == ":":
        return "/" + text[0].lower() + text[2:]
    return text


def _find_bash() -> str | None:
    """Locate an MSYS/Git-Bash that can actually read a ``/c/...`` script path.

    A bare ``bash`` off PATH may resolve to the WSL ``/bin/bash``, which cannot open ``/c/...`` and
    answers "No such file or directory" even though the file is there. Candidates are probed with
    ``bash -n <script>`` and the first that parses the script wins; ``None`` means this host has no
    usable POSIX shell and the .sh runner is genuinely untestable here.
    """
    cands: list[Path] = []
    git = shutil.which("git")
    if git:
        root = Path(git).resolve().parent.parent
        cands += [root / "usr" / "bin" / "bash.exe", root / "bin" / "bash.exe"]
    for name in ("bash.exe", "bash"):
        found = shutil.which(name)
        if found:
            cands.append(Path(found))
    cands.append(Path("C:/Program Files/Git/usr/bin/bash.exe"))
    for cand in cands:
        if not cand.is_file():
            continue
        try:
            probe = subprocess.run([str(cand), "-n", _msys(RUN_SH)],
                                   capture_output=True, text=True, timeout=60)
        except Exception:
            continue
        if probe.returncode == 0:
            return str(cand)
    return None


BASH = _find_bash()


class PortableFirstRunScriptTests(unittest.TestCase):
    def test_both_scripts_exist(self) -> None:
        for script in (RUN_SH, RUN_PS1):
            self.assertTrue(script.is_file(), f"{script} is missing")

    def test_scripts_carry_no_developer_paths(self) -> None:
        for script in (RUN_SH, RUN_PS1):
            text = script.read_text(encoding="utf-8")
            for bad in FORBIDDEN_LITERALS:
                self.assertNotIn(bad, text, f"{script.name} pins a developer path: {bad}")

    def test_scripts_do_not_require_an_exported_pythonpath(self) -> None:
        sh = RUN_SH.read_text(encoding="utf-8")
        # the only PYTHONPATH assignment is derived from this script's own location
        assigns = [ln for ln in sh.splitlines() if "PYTHONPATH=" in ln and "export" in ln]
        self.assertTrue(assigns, "run.sh must set PYTHONPATH from its own root for source mode")
        for line in assigns:
            self.assertIn("$SRC_ROOT", line)

    def test_permission_bits_are_set_on_run_sh(self) -> None:
        self.assertTrue(os.access(RUN_SH, os.X_OK), "run.sh must be executable")

    @unittest.skipUnless(BASH, "no MSYS/Git-Bash on this host: the .sh runner is untestable here")
    def test_run_sh_completes_the_chain_from_a_foreign_cwd(self) -> None:
        with _td() as td:
            out = subprocess.run([BASH, _msys(RUN_SH)], cwd=td, env=_clean_env(td),
                                 capture_output=True, text=True, timeout=900)
            self.assertEqual(out.returncode, 0, out.stdout[-3000:] + out.stderr[-3000:])
            self.assertIn("FIRST_RUN_OK", out.stdout)
            self.assertIn('"verdict": "PASS"', out.stdout)
            self.assertIn('"closure": "FULL"', out.stdout)
            self.assertIn("refusal exit code: 2", out.stdout)

    @unittest.skipUnless(BASH, "no MSYS/Git-Bash on this host")
    def test_run_sh_refuses_when_the_interpreter_is_unusable(self) -> None:
        """Precondition failure is fail-closed and typed, not a traceback."""
        with _td() as td:
            env = _clean_env(td)
            env["PYTHON"] = "/nonexistent/interpreter"
            out = subprocess.run([BASH, _msys(RUN_SH)], cwd=td, env=env,
                                 capture_output=True, text=True, timeout=300)
            self.assertEqual(out.returncode, 3, out.stdout[-1500:] + out.stderr[-1500:])
            self.assertIn("PRECONDITION_FAIL", out.stderr)

    def test_run_ps1_completes_the_chain_from_a_foreign_cwd(self) -> None:
        pwsh = _find_pwsh()
        if pwsh is None:
            self.skipTest("pwsh is not available on this host")
        with _td() as td:
            env = _clean_env(td)
            out = subprocess.run(
                [pwsh, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUN_PS1)],
                cwd=td, env=env, capture_output=True, text=True, timeout=900)
            self.assertEqual(out.returncode, 0, out.stdout[-3000:] + out.stderr[-3000:])
            self.assertIn("FIRST_RUN_OK", out.stdout)
            self.assertIn('"closure": "FULL"', out.stdout)


class ReadmeIsPortableTests(unittest.TestCase):
    """The README's copy-paste block must not depend on the author's machine."""

    def setUp(self) -> None:
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_readme_has_no_absolute_developer_paths(self) -> None:
        offenders = [ln for ln in self.readme.splitlines()
                     if re.search(r"C:[\\/]Users[\\/]user|Agent_Workspace|PIPD-postrelease-wt",
                                  ln)]
        self.assertEqual(offenders, [], f"README still pins developer paths: {offenders[:3]}")

    def test_readme_points_at_the_portable_scripts(self) -> None:
        for name in ("examples/first-run/run.sh", "examples/first-run/run.ps1"):
            self.assertIn(name, self.readme, f"README must reference {name}")
        self.assertIn("FIRST_RUN_OK", self.readme,
                      "the README must state the scripts' success contract")
        # the PowerShell invocation is only correct if it names the .ps1 path (either separator)
        self.assertRegex(self.readme, r"examples[\\/]first-run[\\/]run\.ps1")

    def test_readme_keeps_the_step_by_step_chain(self) -> None:
        for verb in ("intake", "compile-pi", "bind-pd", "compile-ecp", "compile-tqaep", "validate"):
            self.assertIn(verb, self.readme, f"README lost the {verb} step")


if __name__ == "__main__":
    unittest.main(verbosity=2)
