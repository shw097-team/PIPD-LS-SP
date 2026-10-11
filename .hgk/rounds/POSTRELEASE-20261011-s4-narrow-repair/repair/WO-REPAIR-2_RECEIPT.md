# WO-REPAIR-2 — Post-release narrow repair iteration 2 (receipt)

Round: `POSTRELEASE-20261011-s4-narrow-repair`
Branch: `postrelease-narrow-repair-20261011`  HEAD: `dbe38719`
Repair in scope: **R3** (verifier F07, second shell) — the **PowerShell** quickstart block in
`README.md` must fail fast.
No commit / push / tag / release. Working tree left modified.

Host note: shell is Windows PowerShell; the requested runner is
`C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe`
(**PowerShell 7.6.5**). `$PSNativeCommandUseErrorActionPreference` on this host is **`False`** —
which is *why* `$ErrorActionPreference = 'Stop'` alone is not sufficient here. The default
`python` on PATH is the **pip-less** pinned interpreter
(`...\hermes-agent\venv\Scripts\python.exe`, Python 3.11.17, `No module named pip`); a full
Python 3.11 (`C:\Users\user\AppData\Local\Programs\Python\Python311`, 3.11.9, pip 24.0) is also
installed. Both are used below.

---

## R3 — PowerShell quickstart: fail fast

### R3.a — `python -m unittest tests.test_postrelease_quickstart -v`

Command:
```
python -m unittest tests.test_postrelease_quickstart -v
```
Raw output:
```
test_block_activates_portably_with_windows_fallback (...) ... ok
test_block_starts_with_set_e (...) ... ok
test_no_bare_posix_only_activate (...) ... ok
test_block_download_and_checksum_sets (...) ... ok
test_published_digest_literal_in_both_blocks (...) ... ok
test_root_precedes_subcommand (...) ... ok
test_unverified_one_line_install_is_present_and_labels_itself (...) ... ok
test_every_native_command_is_last_exit_code_guarded (...) ... ok
test_first_code_line_sets_error_action_preference_stop (...) ... ok
----------------------------------------------------------------------
Ran 9 tests in 0.005s
OK
```
Exit code: **0**. Verdict: **PASS**.

### R3.b — the test now mechanically asserts the new invariant

`tests/test_postrelease_quickstart.py` gained class `QuickstartPowerShellFailFast` with two tests
(no existing test modified; see the literal diff below):

* `test_first_code_line_sets_error_action_preference_stop` — the PowerShell block's **first
  non-comment, non-empty line** must match `\$ErrorActionPreference\s*=\s*['\"]Stop['\"]`. This
  asserts on the literal form I actually wrote: `$ErrorActionPreference = 'Stop'`.
* `test_every_native_command_is_last_exit_code_guarded` — every visible `python`/`pipd` native
  step must be immediately followed by `if ($LASTEXITCODE -ne 0) { throw ... }`, because
  `$ErrorActionPreference` does not trap native exit codes on this host.

Re-run: covered by R3.a above (all nine tests OK, exit 0). Verdict: **PASS**.

### R3.c — programmatic extraction + fail-fast trace (fresh empty dir, pip-less python first)

The PowerShell block was extracted directly from `README.md` by regex
(`^```powershell…^```$`, the block containing `Get-FileHash`) — **not retyped** — using
`.../s4post/repair/r3ps/extract_ps.py`, written to
`.../s4post/repair/r3ps/quickstart.ps1` (copied to the round as
`repair/traces/r3_quickstart_extracted.ps1`).

First extracted line:
```
$ErrorActionPreference = 'Stop'   # stop at the first failing step; no step fails silently
```

Run from the **fresh empty** directory `.../s4post/repair/r3ps_run_fail` with the pip-less
interpreter placed **first on PATH**:
```
PATH = C:\...\hermes-agent\venv\Scripts;<rest of PATH>
pwsh.exe -NoProfile -File ...\r3ps\quickstart.ps1
```
Raw output (complete):
```
pipd_ls_sp-0.1.0-py3-none-any.whl: OK
Error: Command '['C:\\Users\\user\\...\\r3ps_run_fail\\.venv\\Scripts\\python.exe', '-m', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1.
Exception: C:\Users\user\...\r3ps\quickstart.ps1:16
Line |
  16 |  … XITCODE -ne 0) { throw "python -m venv failed (exit $LASTEXITCODE)" }
     |                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     | python -m venv failed (exit 1)
```
Exit code: **1**. The block stops **at `python -m venv`** — no `Activate.ps1`, no pip install, no
`pipd` "not recognized" cascade, no global install. Verdict: **PASS** (required non-zero exit with
stop-at-first-failure).

> Before the fix I reproduced the defect empirically: a bare `$ErrorActionPreference = 'Stop'`
> followed by `python -m venv .venv` printed the next statement (`REACHED_AFTER_VENV`) and exited
> **0**. The `$LASTEXITCODE` guards are what actually make the block fail fast on this host.

### R3.d — same run with working Python 3.11 first on PATH (fresh empty dir)

Same extracted script, run from the fresh empty directory `.../s4post/repair/r3ps_run_ok` with
`C:\Users\user\AppData\Local\Programs\Python\Python311` first on PATH:
```
pwsh.exe -NoProfile -File ...\r3ps\quickstart.ps1
```
Raw output (key lines):
```
pipd_ls_sp-0.1.0-py3-none-any.whl: OK
Successfully installed attrs-26.1.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 pipd-ls-sp-0.1.0 referencing-0.37.0 rpds-py-2026.9.1 typing-extensions-4.16.0
{ ... "schema_source": {"mode": "INSTALLED", "path": "...\\r3ps_run_ok\\.venv\\Lib\\site-packages\\pipd_ls_sp\\schemas"}, ... "verdict": "PASS" }
PIPD-LS-SP compiler CLI 0.1.0 (13 commands)
{ ... "created": ["docs","schemas","src","tests","dist"], "root": "...\\r3ps_run_ok\\myproject", "verdict": "PASS" }
```
Exit code: **0**. `pipd doctor` prints `"verdict": "PASS"`. Verdict: **PASS**.

Venv evidence — `pip show pipd-ls-sp` in the scratch venv resolves to the venv:
```
Name: pipd-ls-sp
Version: 0.1.0
Location: C:\Users\user\...\r3ps_run_ok\.venv\Lib\site-packages
```
The block completed **inside** the venv (the `INSTALLED` schema source is the venv's
`site-packages`); it did not end with a global install.

### R3.e — host hygiene

After the runs, every `.venv` created under scratch was removed, and `pipd_ls_sp` is present in
**no** global `site-packages`:
```
full Python311:            importlib spec: None
pip-less hermes venv:      importlib spec: None
Python311 Lib/site-packages pipd* files:  (none)
hermes venv  Lib/site-packages pipd* files:  (none)
scratch .venv count after cleanup: 0
```
Nothing landed globally, so nothing needed uninstall. Verdict: **PASS**.

Removed scratch venvs:
```
.../s4post/repair/r3ps_run_fail/.venv
.../s4post/repair/r3ps_run_ok/.venv
.../s4post/repair/r1trace_sys/.venv        <- stale iteration-1 leftover, removed too (see below)
```

> **Observation — stale iteration-1 venv:** iteration 1's receipt claimed it removed
> `r1trace/.venv` and `r1trace_sys/.venv`, but `r1trace_sys/.venv` was still on disk when I
> scanned. I removed it as well (out of my write scope but squarely within the host-hygiene
> rule). No `pipd_ls_sp` was installed inside it; it was an empty/failed build tree.

---

## Literal diff of each changed file (iteration 2)

### `README.md` (PowerShell block only; bash block untouched since iteration 1)
```diff
 ```powershell
+$ErrorActionPreference = 'Stop'   # stop at the first failing step; no step fails silently
 # 1. Fetch the same wheel and checksum list, from the immutable tag.
@@
 # 3. Install into a virtual environment.
 python -m venv .venv
+if ($LASTEXITCODE -ne 0) { throw "python -m venv failed (exit $LASTEXITCODE)" }
 .\.venv\Scripts\Activate.ps1
 python -m pip install .\pipd_ls_sp-0.1.0-py3-none-any.whl
+if ($LASTEXITCODE -ne 0) { throw "pip install failed (exit $LASTEXITCODE)" }
@@
 pipd doctor                        # expect: {"verdict": "PASS", ...}
+if ($LASTEXITCODE -ne 0) { throw "pipd doctor failed (exit $LASTEXITCODE)" }
 pipd --help                        # 13 commands
+if ($LASTEXITCODE -ne 0) { throw "pipd --help failed (exit $LASTEXITCODE)" }
 pipd --root .\myproject init       # --root is global and must precede the subcommand
+if ($LASTEXITCODE -ne 0) { throw "pipd init failed (exit $LASTEXITCODE)" }
 ```
```

### `tests/test_postrelease_quickstart.py` (added `QuickstartPowerShellFailFast`; no existing test changed)
```diff
+class QuickstartPowerShellFailFast(unittest.TestCase):
+    def _quickstart_ps(self) -> str: ...
+    def _code_lines(self, block: str) -> list[str]: ...
+    def test_first_code_line_sets_error_action_preference_stop(self) -> None: ...
+    def test_every_native_command_is_last_exit_code_guarded(self) -> None: ...
```
(full body in the working tree)

---

## What I added, and why (smallest addition)

`$ErrorActionPreference = 'Stop'` alone does **not** stop this block. On PowerShell 7.6.5 with
`$PSNativeCommandUseErrorActionPreference = $False` (measured above), a non-zero native exit
(`python -m venv`, `python -m pip install`, `pipd ...`) does not raise and does not stop the
script. I therefore added the **minimum** guard immediately after each native step:
`if ($LASTEXITCODE -ne 0) { throw "<step> failed (exit $LASTEXITCODE)" }` — five of them, one per
native invocation. That is the smallest change that makes a failed native step stop the block. The
`Invoke-WebRequest` / `Get-FileHash` / `throw`-on-mismatch steps are cmdlet calls already governed
by `$ErrorActionPreference`, so they needed no addition.

## What I did NOT do, and why

* **No weakening of the checksum path.** The digest literal, `Get-FileHash` comparison, and the
  `throw` on mismatch are unchanged. No new unlabelled install path was added.
* **No change to the bash block.** `set -e` + the portable activation from iteration 1 are byte
  identical to HEAD^ for that block.
* **No touch of the "unverified one-line install"** block or its "no hash verification" label.
* **No edits outside the write scope** (`README.md`, `tests/test_postrelease_quickstart.py`, and my
  own `repair/` output). Nothing under `src/`, `docs/`, `dist/`, `tools/`, `openspec/`, schemas, or
  any other test file was changed.
* **No regeneration of** `examples/self-bootstrap/digests.json` or
  `examples/self-bootstrap/negative_stale_context.txt`. `git status` shows neither is modified.
* **No commit / push / tag / release.** Tree left modified.
* **No credential use, no network beyond the released wheel URL** the quickstart already uses.

## New observations

1. **`$PSNativeCommandUseErrorActionPreference` is the crux.** On this host it is `False`, so the
   acceptance brief's concern was correct: `$ErrorActionPreference` alone leaves native failures
   unbounded. The `$LASTEXITCODE` guards are load-bearing, not belt-and-braces — I proved the bare
   form exits 0 before adding them.
2. **The pip-less pinned interpreter is a genuine fail-fast probe.** Placing
   `...\hermes-agent\venv\Scripts\python.exe` first on PATH makes `python -m venv` fail with the
   exact `ensurepip … returned non-zero exit status 1` the operator measured, so the block now
   stops there instead of cascading into four "not recognized" errors and exiting 0.
3. **Stale iteration-1 venv left behind.** See R3.e — `r1trace_sys/.venv` survived iteration 1's
   cleanup claim. Removed.

## Repair surface (end of run)

See appended `git status --porcelain` and `git diff --stat`.

---

## Appended: repair surface at end of run (iteration 1 + 2 cumulative)
```
$ git status --porcelain
 M .hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json
 M .hgk/artifacts/s4/CLI_SURFACE.json
 M .hgk/artifacts/tqaep_design_tmp/ecp.json
 M .hgk/artifacts/tqaep_design_tmp/pi.json
 M README.md
 M examples/self-bootstrap/README.md
 M tests/test_postrelease_quickstart.py
 M tests/test_postrelease_selfbootstrap.py
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/...  (untracked round artefacts)

$ git diff --stat
 .hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json |   2 +-
 .hgk/artifacts/s4/CLI_SURFACE.json           |   2 +-
 .hgk/artifacts/tqaep_design_tmp/ecp.json     |   2 +-
 .hgk/artifacts/tqaep_design_tmp/pi.json      |   2 +-
 README.md                                    |   9 ++-
 examples/self-bootstrap/README.md            |   9 ++-
 tests/test_postrelease_quickstart.py         | 110 +++++++++++++++++++++++++++
 tests/test_postrelease_selfbootstrap.py      |  51 +++++++++++++
 8 files changed, 180 insertions(+), 7 deletions(-)
```
The tracked deltas attributable to this repair surface are exactly the two READMEs and the two
tests: iteration 1's `README.md` bash block + self-bootstrap README + `tests/test_postrelease_selfbootstrap.py`,
and iteration 2's `README.md` PowerShell block + `tests/test_postrelease_quickstart.py`. The four
`.hgk/artifacts/*.json` modifications are pre-existing round state, not authored by this WorkOrder.
