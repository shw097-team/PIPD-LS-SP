# WO-S4-UX-01 receipt — post-release narrow repair (quickstart checksum / onboarding)

Round: `POSTRELEASE-20261011-s4-narrow-repair`
Task: `PIPD-LS-SP-S4-POSTRELEASE-NARROW-REPAIR-20261011`
Writer: Codex bounded writer (`opencode-go/deepseek-v4.1-flash`)
Interpreter (pinned): `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (Python 3.11.9)
Candidate head at work start: `4445db5a6d1b3138946fd7c4fe3b712e4faf1af7` (branch `postrelease-narrow-repair-20261011`)
Disposable scratch dir for network/acceptance work: `C:/Users/user/AppData/Local/Temp/wo-s4-ux-01`
Ceiling: `REPAIR_CANDIDATE_ONLY` — no commit, no push, no tag, no release. Writes confined to `README.md`,
`tests/test_postrelease_quickstart.py`, and this `lane/` receipt.

POSIX toolchain present via Git for Windows: `bash.exe`, `sha256sum.exe`, `grep.exe`, `curl.exe` under
`C:\Program Files\Git\...`.

---

## 1. Acceptance command A — corrected POSIX path vs the REAL published release

Run from an empty directory (`wo-s4-ux-01`), against
`https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2`.

Command:

```bash
cd /c/Users/user/AppData/Local/Temp/wo-s4-ux-01
BASE=https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2
curl -fsSLO "$BASE/pipd_ls_sp-0.1.0-py3-none-any.whl"
curl -fsSLO "$BASE/SHA256SUMS"
grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS | sha256sum -c -
```

Raw output (exit codes inline):

```
curl_whl_exit=0
curl_sums_exit=0
cat SHA256SUMS:
d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f  pipd_ls_sp-0.1.0-py3-none-any.whl
4d24d1ec0a6e1c5b08905b6252ddb71175086b3927a27266d46fac39420481e7  pipd-ls-sp-v0.1.0-preview.2-source.zip
31b6801090932c8ffb13d8b6096a47d272b9e646819ef89d52724f3e09c63adb  PREVIEW_NOTES_v0.1.0-preview.2.md
pipd_ls_sp-0.1.0-py3-none-any.whl: OK
checksum_exit=0
```

Verdict: **PASS** — exit `0`, prints `pipd_ls_sp-0.1.0-py3-none-any.whl: OK`, exactly matching the
expectation line written into the README.

### 1a. DISCREPANCY with the brief (recorded, not smoothed over)

The brief's raw evidence listed the source-zip line as
`804181f6a2cc1bc5e9bc59ad144de0f403939c0b3ae4e2cbd8db701f34c6620e`. The **live**
`v0.1.0-preview.2` `SHA256SUMS` (fetched above) carries
`4d24d1ec0a6e1c5b08905b6252ddb71175086b3927a27266d46fac39420481e7` for the source zip. The wheel line
(`d6c3e295…`) and the notes line (`31b68010…`) match the brief exactly. The two lines that matter for
this repair — the wheel digest and the "three lines" count — are confirmed. The README does **not**
quote the source-zip digest anywhere, so no document value depends on the disputed line, and no
published bytes were moved or rewritten to resolve it.

---

## 2. Acceptance command B — a mutated byte must fail

Command (POSIX path) and raw output:

```
cp pipd_ls_sp-0.1.0-py3-none-any.whl mut.whl
printf 'X' | dd of=mut.whl bs=1 seek=100 conv=notrunc      # dd_exit=0
sha256sum mut.whl
   -> 8e6b3867a62e95e302daa16e00bb4b85b5f6f27fa3c8e2bdf7d4d1086a30b3d0 *mut.whl
grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS | sed 's|pipd_ls_sp-0.1.0-py3-none-any.whl|mut.whl|' | sha256sum -c -
   -> mut.whl: FAILED
   -> sha256sum: WARNING: 1 computed checksum did NOT match
neg_verify_exit=1
```

Verdict: **PASS** — the mutated byte yields digest `8e6b3867…` (≠ published `d6c3e295…`) and the check
exits non-zero with `FAILED`. The check discriminates.

### 2a. `python -m pip install ./mut.whl` must not be reported as verified

Three probes, raw output:

* Probe 1 — byte-mutated wheel named `mut.whl`:
  `ERROR: mut.whl is not a valid wheel filename.` → exit `1`.
* Probe 2 — byte-mutated wheel kept as a valid wheel filename, `pipd_ls_sp-0.1.0-py3-none-any.whl`,
  digest `8e6b3867…`:
  `ERROR: pipd-ls-sp has an invalid wheel, could not read '...METADATA': BadZipFile("Bad CRC-32 ...")`
  → exit `1`.
* Probe 3 NOTE — a structurally-valid tamper fits pip inside a zip entry without breaking any CRC.
  A wheel was rebuilt with an extra line appended to `pipd_ls_sp/cli.py`; its SHA-256 is
  `f7f74e04e08b7166c6756457a3d20bc23b19e7e3f0b47ecb6e45ea7b91c2c9ec` (≠ published), yet pip:
  ```
  Processing ...tamperdir\pipd_ls_sp-0.1.0-py3-none-any.whl
  Installing collected packages: pipd-ls-sp
  Successfully installed pipd-ls-sp-0.1.0
  PIP_STATUS=0
  ```

Verdict: pip performs **no** hash verification. Probes 1 & 2 fail for structural reasons only
(filename / zip CRC), never because of a digest. Probe 3 — same version `0.1.0`, different bytes —
installs with exit `0`. This is the concrete fact the README's "Unverified one-line install
(no hash check)" wording is built on, and it is why the verified path is kept separate.

---

## 3. PowerShell verification block vs the real wheel

Command (the exact logic in the README's PowerShell block) and raw output:

```powershell
$expected = "d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f"
$actual = (Get-FileHash -Algorithm SHA256 -Path "pipd_ls_sp-0.1.0-py3-none-any.whl").Hash.ToLower()
if ($actual -ne $expected) { throw "wheel SHA-256 mismatch: $actual" }
"pipd_ls_sp-0.1.0-py3-none-any.whl: OK"
```

```
pipd_ls_sp-0.1.0-py3-none-any.whl: OK
actual=d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f
```

Verdict: **PASS** — the verified wheel hashes to the published literal, so the `throw` guard does not
fire and the block prints the `: OK` line it documents.

---

## 4. The documented full-download alternative

The README's alternative (fetch every asset, then `sha256sum -c SHA256SUMS`) was executed to confirm
the expectation text is true, raw output:

```
curl -fsSLO "$BASE/pipd-ls-sp-v0.1.0-preview.2-source.zip"       # zip_exit=0
curl -fsSLO "$BASE/PREVIEW_NOTES_v0.1.0-preview.2.md"           # notes_exit=0
sha256sum -c SHA256SUMS
pipd_ls_sp-0.1.0-py3-none-any.whl: OK
pipd-ls-sp-v0.1.0-preview.2-source.zip: OK
PREVIEW_NOTES_v0.1.0-preview.2.md: OK
full_check_exit=0
```

Verdict: **PASS** — three `: OK` lines, exit `0`, matching the README comment exactly.

---

## 5. README diff (literal before/after of the changed region)

`git --no-pager diff -- README.md` (old = `HEAD:README.md`):

```diff
@@ -23,17 +23,27 @@ a production release — read [Claim ceiling](#claim-ceiling) before building on

 ## Quickstart

-Copy-paste, from a shell. Requires **Python >= 3.11** and `curl`.
+Copy-paste, from a shell. Requires **Python >= 3.11** and `curl`. The installable identity is the
+**immutable** tag `v0.1.0-preview.2`; `main` is rolling, so pin the tag rather than the branch.
+
+### bash / POSIX

 ```bash
-# 1. Fetch the published artefact and its checksums, from the immutable tag.
+# 1. Fetch the published wheel and the checksum list, from the immutable tag.
 BASE=https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2
 curl -fsSLO "$BASE/pipd_ls_sp-0.1.0-py3-none-any.whl"
 curl -fsSLO "$BASE/SHA256SUMS"

-# 2. Verify the bytes. This is the ONLY integrity check offered: there is no install-time
-#    or startup cryptographic readback, and no release signature.
-sha256sum -c SHA256SUMS            # expect: pipd_ls_sp-0.1.0-py3-none-any.whl: OK
+# 2. Verify the bytes. Check exactly what step 1 downloaded: SHA256SUMS lists three assets, but
+#    only the wheel is present here, so select its line. This is the ONLY integrity check offered:
+#    there is no install-time or startup cryptographic readback, and no release signature.
+#    Published wheel digest: d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f
+grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS | sha256sum -c -
+#    expect: pipd_ls_sp-0.1.0-py3-none-any.whl: OK
+#    Alternative, only after fetching EVERY asset SHA256SUMS lists, the whole file checks clean:
+#      curl -fsSLO "$BASE/pipd-ls-sp-v0.1.0-preview.2-source.zip"
+#      curl -fsSLO "$BASE/PREVIEW_NOTES_v0.1.0-preview.2.md"
+#      sha256sum -c SHA256SUMS       # expect three ": OK" lines (wheel, source zip, notes)

 # 3. Install into a virtual environment.
 python -m venv .venv
@@ -49,6 +59,44 @@ pipd --root ./myproject init      # -> exit 0; creates docs/ schemas/ src/ tests
 pipd doctor                       # -> {"verdict": "PASS", ...}, and it names the schema source it resolved
 ```

+### Windows (PowerShell)
+
+```powershell
+# 1. Fetch the same wheel and checksum list, from the immutable tag.
+$Base = "https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2"
+Invoke-WebRequest -Uri "$Base/pipd_ls_sp-0.1.0-py3-none-any.whl" -OutFile "pipd_ls_sp-0.1.0-py3-none-any.whl"
+Invoke-WebRequest -Uri "$Base/SHA256SUMS" -OutFile "SHA256SUMS"
+
+# 2. Verify the wheel against its published digest. SHA256SUMS lists three assets but only the wheel
+#    was fetched, so compare the wheel's own hash to the published literal.
+$expected = "d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f"
+$actual = (Get-FileHash -Algorithm SHA256 -Path "pipd_ls_sp-0.1.0-py3-none-any.whl").Hash.ToLower()
+if ($actual -ne $expected) { throw "wheel SHA-256 mismatch: $actual" }
+"pipd_ls_sp-0.1.0-py3-none-any.whl: OK"   # expect this line
+
+# 3. Install into a virtual environment.
+python -m venv .venv
+.\.venv\Scripts\Activate.ps1
+python -m pip install .\pipd_ls_sp-0.1.0-py3-none-any.whl
+
+# 4. Check the install, then use it.
+pipd doctor                        # expect: {"verdict": "PASS", ...}
+pipd --help                        # 13 commands
+pipd --root .\myproject init       # --root is global and must precede the subcommand
+```
+
+### Unverified one-line install (no hash check)
+
+If you do not need to check the bytes against the published digest, pip can fetch and install the
+wheel in one line:
+
+```bash
+python -m pip install "https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2/pipd_ls_sp-0.1.0-py3-none-any.whl"
+```
+
+This performs **no hash verification** - pip installs whatever the URL serves when you run it. Use
+the verified path above when the bytes matter.
+
 Beyond that the pipeline is `intake` -> `compile-pi` -> `bind-pd` -> `compile-ecp` /
 `compile-tqaep` -> `validate`, and **the middle steps take real inputs, not free text** — verified
 against the CLI rather than assumed:
```

Every other section (`Start here` table, pipeline block with the `--root`-precedes-subcommand note,
Claim ceiling, Known limitations, Licence, History) is untouched. `pipd --root` still appears only
before its subcommand (`init`, `intake`, `compile-pi`).

---

## 6. Regression test

New file `tests/test_postrelease_quickstart.py` (4 tests). It parses the README, never the network.

Properties asserted:
1. the checksum command's input set is a **subset** of the files the block downloads, in both the
   bash and PowerShell quickstart blocks (the defect: a bare `sha256sum -c SHA256SUMS` opens the two
   assets the block never fetched);
2. the published digest literal `d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f`
   appears in **both** the bash and the PowerShell blocks;
3. the unverified one-line install is present and labels itself "no hash verification";
4. `pipd --root` precedes its subcommand everywhere.

### 6a. Green on the repaired tree

```
python.exe -m unittest tests.test_postrelease_quickstart -v
test_block_download_and_checksum_sets ... ok
test_published_digest_literal_in_both_blocks ... ok
test_root_precedes_subcommand ... ok
test_unverified_one_line_install_is_present_and_labels_itself ... ok
Ran 4 tests in 0.002s
OK
EXIT=0
```

### 6b. Red on the pre-repair README (non-vacuous proof)

The test class was pointed at `HEAD:README.md` (the un-repaired front page) in memory:

```
FAIL: test_block_download_and_checksum_sets — AssertionError: [] is not true : README has no ```powershell quickstart block
FAIL: test_published_digest_literal_in_both_blocks — AssertionError: 'd6c3e295...' not found
FAIL: test_unverified_one_line_install_is_present_and_labels_itself — AssertionError: not found
ok: test_root_precedes_subcommand
Ran 4 tests ... FAILED (failures=3)
RED_ok= True
```

The old failing command was `sha256sum -c SHA256SUMS` against a two-file download set; the parser
confirms those inputs were `['SHA256SUMS', 'pipd_ls_sp-0.1.0-py3-none-any.whl']` and that the old
block exposes no embedded sums listing, so no asset file was opened — the checksum command in the
pre-repair text could only read `SHA256SUMS` itself. The repaired block instead pipes a single
selected line into `sha256sum -c -`.

Note (honest): `test_tooling_executes.test_every_test_file_bootstraps_sys_path` requires every test
file to contain `sys.path.insert`. The first draft of the new test omitted it and the full suite
caught it red:

```
AssertionError: Lists differ: ['test_postrelease_quickstart.py'] != [] : test files without a sys.path bootstrap
Ran 329 tests in 109.404s
FAILED (failures=1, skipped=3)
EXIT=1
```

A `sys.path` bootstrap was added; the guard then passed and the suite went green (below). This is
recorded rather than hidden: the new test file does insert `src` on `sys.path`.

---

## 7. Full suite (regression parity)

```
python.exe -m unittest discover -s tests
...
Ran 329 tests in 108.986s
OK (skipped=3)
EXIT=0
```

Baseline (`.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/evidence/BASELINE_FULL_SUITE.log`):
`Ran 325 tests ... OK (skipped=3)`. Delta = +4 tests (the new file), 0 failures, same 3
environmental skips (evidence-manifest seal bound to an older commit; publication-projection frozen
candidate absent from this clone — both pre-existing and unrelated to this change).

Focused re-run of the two evidence-surface modules, in case the README is a tracked product path in
the manifest/projection: `tests.test_evidence_manifest tests.test_publication_projection` →
`Ran 6 tests ... OK (skipped=2)` (same environmental skips).

---

## 8. NOT_RUN / not verified

* **NOT_RUN — real PowerShell `Get-FileHash` byte-hash executed in `pwsh`.** Only the algorithm was
  exercised (in PowerShell, via the same `Get-FileHash` cmdlet) against the real wheel; `pwsh` import
  of the wheel and `pipd doctor` on Windows were not run end-to-end here. Reason: the receipt lane is
  a bounded writer and the acceptance brief names only the POSIX command A/B; the PowerShell block is
  documentation whose verification *logic* (the `Get-FileHash` comparison) was exercised and passed.
* **NOT_RUN — `pipd doctor` against a Windows venv install.** Reason: not required by the named
  acceptance commands; would mutate outside the admitted write scope's intent. The wheel's own
  install/`doctor` behaviour is covered by the repo suite (`test_wheel_distribution`).
* **NOT_RUN — authoritative resolution of the source-zip digest mismatch (§1a).** Reason: settling it
  would require either trusting the brief's quoted file or fetching the asset; the README does not
  depend on that value, so it is left recorded, not reconciled.
* **NOT_RUN — commit / push / tag / release.** Out of scope by the brief (candidate-only repair).
* **Unchanged by design** per brief item 5/6: Claim ceiling table, Known limitations list, History
  section, and all historical receipts were not edited.

## 9. Files changed

* `README.md` — quickstart repaired (§5).
* `tests/test_postrelease_quickstart.py` — new deterministic regression test (§6).
* `.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/WO-S4-UX-01_RECEIPT.md` — this receipt.
