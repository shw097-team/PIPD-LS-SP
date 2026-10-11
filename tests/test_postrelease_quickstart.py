"""POST-F01 quickstart regression: the checksum step must cover exactly what was downloaded.

The published ``v0.1.0-preview.2`` ``SHA256SUMS`` lists three assets (the wheel, the source
zip, the preview notes) while the README quickstart fetches only the wheel and ``SHA256SUMS``.
A bare ``sha256sum -c SHA256SUMS`` therefore exits non-zero with two "FAILED open or read"
lines. These tests pin the repaired contract and never touch the network:

  * every file a checksum command reads as input is a file the same block downloads;
  * the published wheel digest literal appears in both the bash and the PowerShell blocks;
  * ``pipd --root`` still precedes the subcommand everywhere it appears.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
README = ROOT / "README.md"

PUBLISHED_WHEEL_DIGEST = "d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f"
WHEEL = "pipd_ls_sp-0.1.0-py3-none-any.whl"
SHA256SUMS = "SHA256SUMS"

def _readme_text() -> str:
    return README.read_text(encoding="utf-8")


def _fenced_blocks(text: str, lang: str) -> list[str]:
    """Return the bodies of every ```lang fenced code block, in order."""
    pattern = re.compile(r"^```" + re.escape(lang) + r"[ \t]*\n(.*?)^```[ \t]*$", re.M | re.S)
    return pattern.findall(text)


def _download_set(block: str) -> set[str]:
    """Files a shell block downloads: curl (any flags, incl. ``-fsSLO``) / Invoke-WebRequest /
    ``--output``. The filename is the trailing path segment of the destination."""
    names: set[str] = set()
    for line in block.splitlines():
        if line.strip().startswith("#"):
            continue
        if re.search(r"\bcurl\b", line):
            for match in re.finditer(r"\"([^\"]+)\"", line):
                names.add(Path(match.group(1)).name)
        for match in re.finditer(r"-OutFile\s+\"?([^\s\"']+)\"?", line):
            names.add(Path(match.group(1)).name)
        for match in re.finditer(r"--output[= ]\s*\"?([^\s\"']+)\"?", line):
            names.add(Path(match.group(1)).name)
    return {Path(n).name for n in names}


def _checksum_input_set(block: str) -> set[str]:
    """Files a checksum command reads as input in this block."""
    reads: set[str] = set()
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        # POSIX: `... | sha256sum -c` verifies the lines piped in; the piped source file is
        # the checksum command's ONLY input, the digest-listed assets are NOT opened.
        if re.search(r"sha256sum\s+-c\s+-", line):
            for match in re.finditer(r"(\S+)\s*\|\s*sha256sum\s+-c\s+-", line):
                reads.add(Path(match.group(1)).name)
            continue
        # POSIX: `sha256sum -c <file>` opens <file>; if it is a sums file, every asset it
        # lists must itself have been downloaded.
        for match in re.finditer(r"sha256sum\s+-c\s+(\S+)", line):
            target = Path(match.group(1)).name
            if target == SHA256SUMS:
                reads |= _sums_entries(block)
            else:
                reads.add(target)
        # PowerShell: Get-FileHash -Path <file> opens <file>.
        for match in re.finditer(r"Get-FileHash\b[^\n]*?-Path\s+\"?([^\s\"']+)\"?", line):
            reads.add(Path(match.group(1)).name)
    return reads


def _sums_entries(block: str) -> set[str]:
    """Asset names referenced by the embedded published SHA256SUMS listing, if any."""
    names: set[str] = set()
    for match in re.finditer(r"^\s*[0-9a-f]{64}\s+\*?(\S+)\s*$", block, re.M):
        names.add(Path(match.group(1)).name)
    return names


class QuickstartChecksumScope(unittest.TestCase):
    def test_block_download_and_checksum_sets(self) -> None:
        text = _readme_text()
        bash_blocks = _fenced_blocks(text, "bash")
        ps_blocks = _fenced_blocks(text, "powershell")

        self.assertTrue(bash_blocks, "README has no ```bash quickstart block")
        self.assertTrue(ps_blocks, "README has no ```powershell quickstart block")

        quickstart_bash = next((b for b in bash_blocks if WHEEL in b and SHA256SUMS in b), None)
        self.assertIsNotNone(quickstart_bash, "no bash block fetches the wheel + SHA256SUMS")
        quickstart_ps = next((b for b in ps_blocks if WHEEL in b and SHA256SUMS in b), None)
        self.assertIsNotNone(quickstart_ps, "no powershell block fetches the wheel + SHA256SUMS")

        for label, block in (("bash", quickstart_bash), ("powershell", quickstart_ps)):
            with self.subTest(block=label):
                downloads = _download_set(block)
                checks = _checksum_input_set(block)
                # (a) the checksum command must cover exactly what was downloaded
                self.assertTrue(checks, f"{label}: no checksum command parsed")
                self.assertLessEqual(
                    checks,
                    downloads,
                    f"{label}: checksum reads {sorted(checks - downloads)} but the block only "
                    f"downloads {sorted(downloads)}",
                )
                self.assertIn(SHA256SUMS, downloads, f"{label}: SHA256SUMS is not downloaded")
                self.assertIn(WHEEL, downloads, f"{label}: the wheel is not downloaded")

    def test_published_digest_literal_in_both_blocks(self) -> None:
        text = _readme_text()
        bash_blocks = _fenced_blocks(text, "bash")
        ps_blocks = _fenced_blocks(text, "powershell")
        self.assertIn(PUBLISHED_WHEEL_DIGEST, text)
        self.assertTrue(
            any(PUBLISHED_WHEEL_DIGEST in b for b in bash_blocks),
            "published digest literal missing from the bash block",
        )
        self.assertTrue(
            any(PUBLISHED_WHEEL_DIGEST in b for b in ps_blocks),
            "published digest literal missing from the PowerShell block",
        )

    def test_unverified_one_line_install_is_present_and_labels_itself(self) -> None:
        text = _readme_text()
        url = (
            "https://github.com/shw097-team/PIPD-LS-SP/releases/download/"
            "v0.1.0-preview.2/pipd_ls_sp-0.1.0-py3-none-any.whl"
        )
        self.assertIn(f'python -m pip install "{url}"', text)
        lowered = text.lower()
        self.assertIn("no hash verification", lowered)

    def test_root_precedes_subcommand(self) -> None:
        text = _readme_text()
        for line in text.splitlines():
            stripped = line.strip()
            if "pipd --root" in stripped:
                # `--root` must be immediately followed by its value, then a subcommand.
                self.assertRegex(
                    stripped,
                    r"pipd --root \S+ \S+",
                    f"--root is not before the subcommand: {stripped!r}",
                )


if __name__ == "__main__":
    unittest.main()
