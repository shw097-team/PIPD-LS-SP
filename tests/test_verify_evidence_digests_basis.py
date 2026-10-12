"""Pin the basis-aware digest gate in ``tools/verify_evidence_digests.py``.

The gate must (a) name the bytes a recorded digest was computed over, (b) accept an EOL-only
difference as benign, and (c) still classify an entry as unexplained when the digest matches an old
snapshot whose *content* genuinely changed -- the false-pass the v2 brief forbids (a rubber stamp
that reports zero unexplained on a genuinely drifted tree is a task failure).

It also pins that generation-identity ancestry stays REPORT-ONLY: a non-ancestor ``candidate_head``
is named in the report and the run still exits 0 without ``--strict`` (and even with it).

Hermetic: every classification case builds its own throwaway git repository under ``tempfile``; no
network is used. Expected digests are computed from explicit byte literals (an independent oracle),
not by importing the tool's own transforms. The final test additionally checks the acceptance
property on THIS checkout: ``--strict`` exits non-zero whenever the unexplained set is non-empty.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

TOOL = ROOT / "tools" / "verify_evidence_digests.py"
GIT = shutil.which("git")

# Deterministic git identity and line-ending policy so the fixture is byte-exact on any host.
_GIT_ID = ["-c", "user.email=t@example.invalid", "-c", "user.name=probe",
           "-c", "commit.gpgsign=false", "-c", "init.defaultBranch=main",
           "-c", "core.autocrlf=false", "-c", "core.eol=lf"]


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _crlf(data: bytes) -> bytes:
    """Lone LF -> CRLF (the expansion the tool documents); an independent oracle."""
    return data.replace(b"\r\n", b"\x00").replace(b"\n", b"\r\n").replace(b"\x00", b"\r\n")


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True)


class _FixtureRepo:
    """A throwaway git checkout with a manifest (+ seal) that exercises every basis."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "repo"
        (self.root / "docs").mkdir(parents=True)

    def close(self) -> None:
        self._tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run([GIT, *_GIT_ID, *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout.strip()

    def write(self, rel: str, data: bytes) -> None:
        (self.root / rel).write_bytes(data)


@unittest.skipUnless(GIT, "git is required to build the fixture repository")
class BasisClassification(unittest.TestCase):
    """Every case builds the fixture tree, runs the real CLI, and reads its report."""

    # byte literals shared between the fixture and the expected digests
    DISK = b"disk-line\n"
    CRLF_ON_DISK = b"a\nb\n"
    HEAD_DRIFT_A = b"old head content\nsecond\n"
    HEADCRLF_A = b"alpha\r\nbeta\n"
    MIXED_HEAD = b"x\r\ny\n"
    CAND_HEAD = b"candidate content v1\n"
    CANDCRLF_HEAD = b"gamma\ndelta\n"
    CAND_BRANCH = b"cand-only payload\n"
    CANDCRLF_BRANCH = b"cand-only\r\nalpha\n"
    NO_BASIS = b"no basis carries these bytes\n"

    def setUp(self) -> None:
        self.fx = _FixtureRepo()
        self.addCleanup(self.fx.close)
        root = self.fx.root
        self.fx.git("init", "-q")
        # commit 1 (main): the "v1" content of every fixture file
        for rel, data in (("docs/disk.txt", self.DISK), ("docs/crlf.txt", self.CRLF_ON_DISK),
                          ("docs/head.txt", self.HEAD_DRIFT_A), ("docs/headcrlf.txt", self.HEADCRLF_A),
                          ("docs/mixed.txt", self.MIXED_HEAD), ("docs/cand.txt", self.CAND_HEAD),
                          ("docs/candcrlf.txt", self.CANDCRLF_HEAD),
                          ("docs/unknown.txt", b"whatever\n")):
            self.fx.write(rel, data)
        self.fx.git("add", "-A")
        self.fx.git("commit", "-qm", "base")
        # commit 2 (branch cand): different candidate blobs, diverging from main
        self.fx.git("checkout", "-q", "-b", "cand")
        self.fx.write("docs/cand.txt", self.CAND_BRANCH)
        self.fx.write("docs/candcrlf.txt", self.CANDCRLF_BRANCH)
        self.fx.git("add", "-A")
        self.fx.git("commit", "-qm", "candidate")
        self.cand_commit = self.fx.git("rev-parse", "HEAD")
        self.cand_tree = self.fx.git("rev-parse", "HEAD^{tree}")
        # commit 3 (main) so main and cand are genuinely divergent
        self.fx.git("checkout", "-q", "main")
        self.fx.write("docs/notes.txt", b"note\n")
        self.fx.git("add", "-A")
        self.fx.git("commit", "-qm", "advance main")
        # uncommitted working-tree edits: the drift each basis must classify
        self.fx.write("docs/head.txt", b"NEW head content\nsecond changed\n")
        self.fx.write("docs/headcrlf.txt", b"alpha\nbeta\nGAMMA\n")
        self.fx.write("docs/mixed.txt", b"x\ny\r\n")
        self.fx.write("docs/cand.txt", b"candidate content v2 changed\n")
        self.fx.write("docs/candcrlf.txt", b"cand-only\nalpha\nDELTA\n")

        self.manifest = {
            "docs/disk.txt": _sha(self.DISK),
            "docs/crlf.txt": _sha(_crlf(self.CRLF_ON_DISK)),
            "docs/head.txt": _sha(self.HEAD_DRIFT_A),
            "docs/headcrlf.txt": _sha(_crlf(self.HEADCRLF_A)),
            "docs/mixed.txt": _sha(self.MIXED_HEAD),
            "docs/cand.txt": _sha(self.CAND_BRANCH),
            "docs/candcrlf.txt": _sha(_crlf(self.CANDCRLF_BRANCH)),
            "docs/unknown.txt": _sha(self.NO_BASIS),
        }
        self.manifest_path = root / "evidence_manifest.json"
        self.manifest_path.write_text(json.dumps(self.manifest, indent=1), encoding="utf-8")
        (root / "evidence_manifest.seal.json").write_text(
            json.dumps({"schema": "PIPD-EVIDENCE-MANIFEST-SEAL/1",
                        "candidate": {"repo_commit_sha": self.cand_commit,
                                      "candidate_tree_sha": self.cand_tree}}), encoding="utf-8")
        self.expected_basis = {"disk": 1, "crlf_disk": 1, "head_blob": 2, "crlf_head_blob": 1,
                               "candidate_blob": 1, "crlf_candidate_blob": 1, "unexplained": 1}
        self.expected_unexplained = ["docs/cand.txt", "docs/candcrlf.txt", "docs/head.txt",
                                     "docs/headcrlf.txt", "docs/unknown.txt"]

    def _report(self) -> dict:
        proc = _run("--root", str(self.fx.root), "--manifest", str(self.manifest_path))
        self.assertEqual(proc.returncode, 0, proc.stderr[-600:])
        return json.loads(proc.stdout)

    def test_every_basis_is_named_and_the_content_clause_is_applied(self) -> None:
        """The first matching basis names the bytes, and EOL-equivalence decides benign vs drift."""
        report = self._report()
        self.assertEqual(report["checked"], 8)
        self.assertEqual(report["candidate_revision"], self.cand_tree)
        self.assertEqual(report["basis_counts"], self.expected_basis)
        self.assertEqual(report["match_raw"], 1)          # docs/disk.txt
        self.assertEqual(report["benign_eol"], 2)         # docs/crlf.txt + docs/mixed.txt
        self.assertEqual(report["unexplained"], self.expected_unexplained)
        # Back-compat keys the existing in-tree test reads must still be present.
        for key in ("checked", "match", "missing", "stale", "identity_checks"):
            self.assertIn(key, report)

    def test_json_summary_is_exactly_the_compact_contract(self) -> None:
        proc = _run("--root", str(self.fx.root), "--manifest", str(self.manifest_path), "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr[-600:])
        self.assertTrue(proc.stdout.startswith('{"checked"'), proc.stdout[:80])
        summary = json.loads(proc.stdout)
        self.assertEqual(list(summary.keys()),
                         ["checked", "match_raw", "benign_eol", "unexplained", "basis_counts"])
        self.assertEqual(summary, {"checked": 8, "match_raw": 1, "benign_eol": 2, "unexplained": 5,
                                   "basis_counts": self.expected_basis})

    def test_strict_exits_only_when_the_unexplained_set_is_non_empty(self) -> None:
        default = _run("--root", str(self.fx.root), "--manifest", str(self.manifest_path))
        self.assertEqual(default.returncode, 0, "the default run must stay report-only")
        strict = _run("--root", str(self.fx.root), "--manifest", str(self.manifest_path), "--strict")
        self.assertEqual(strict.returncode, 1, "genuine drift must fail --strict")

        # A manifest whose every entry is explained must pass --strict (no over-failing).
        clean = {"docs/disk.txt": _sha(self.DISK), "docs/crlf.txt": _sha(_crlf(self.CRLF_ON_DISK))}
        clean_path = self.fx.root / "clean_manifest.json"
        clean_path.write_text(json.dumps(clean), encoding="utf-8")
        clean_run = _run("--root", str(self.fx.root), "--manifest", str(clean_path), "--strict")
        self.assertEqual(clean_run.returncode, 0, clean_run.stdout + clean_run.stderr)


@unittest.skipUnless(GIT, "git is required to build the fixture repository")
class AncestryStaysReportOnly(unittest.TestCase):
    def test_non_ancestor_candidate_head_is_named_but_never_fatal(self) -> None:
        fx = _FixtureRepo()
        self.addCleanup(fx.close)
        fx.git("init", "-q")
        fx.write("docs/placeholder.txt", b"x\n")
        fx.git("add", "-A")
        fx.git("commit", "-qm", "base")
        # A parentless (root) commit is resolvable but can never be an ancestor of HEAD.
        tree = fx.git("rev-parse", "HEAD^{tree}")
        other = fx.git("commit-tree", tree, "-m", "divergent root")
        self.assertEqual(
            subprocess.run([GIT, *_GIT_ID, "merge-base", "--is-ancestor", other, "HEAD"],
                           cwd=fx.root, capture_output=True).returncode, 1,
            "fixture invariant: the divergent commit must NOT be an ancestor of HEAD")
        fx.write("docs/identity.json", b'{\n "candidate_head": "' + other.encode() + b'"\n}\n')
        manifest = {"docs/identity.json": _sha((fx.root / "docs" / "identity.json").read_bytes())}
        manifest_path = fx.root / "evidence_manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        proc = _run("--root", str(fx.root), "--manifest", str(manifest_path))  # no --strict
        self.assertEqual(proc.returncode, 0, "a non-ancestor candidate must not fail the run")
        self.assertIn(other, proc.stdout, "the report must still name the non-ancestor value")
        report = json.loads(proc.stdout)
        self.assertEqual(report["unexplained"], [])
        checks = [c for c in report["identity_checks"] if c["path"] == "docs/identity.json"]
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0]["candidate_head"], other)
        self.assertIs(checks[0]["is_ancestor"], False)
        self.assertIsNone(checks[0]["error"])
        # Even --strict must not escalate an ancestry finding (report-only by adjudication).
        strict = _run("--root", str(fx.root), "--manifest", str(manifest_path), "--strict")
        self.assertEqual(strict.returncode, 0, strict.stdout + strict.stderr)


class StrictGuardOnThisCheckout(unittest.TestCase):
    """The acceptance property on the real tree -- not a count, a gate behaviour."""

    def test_strict_exit_is_nonzero_exactly_when_unexplained_is_non_empty(self) -> None:
        manifest = ROOT / ".hgk" / "artifacts" / "evidence_manifest.json"
        if not manifest.is_file():
            self.skipTest("this checkout carries no evidence manifest to verify")
        default = _run()
        self.assertEqual(default.returncode, 0, "the default run is report-only, always exit 0")
        report = json.loads(default.stdout)
        unexplained = len(report["unexplained"])
        self.assertEqual(report["checked"],
                         report["match_raw"] + report["benign_eol"] + unexplained)
        strict = _run("--strict")
        expected = 1 if unexplained > 0 else 0
        self.assertEqual(
            strict.returncode, expected,
            f"--strict exit {strict.returncode} disagrees with unexplained={unexplained}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
