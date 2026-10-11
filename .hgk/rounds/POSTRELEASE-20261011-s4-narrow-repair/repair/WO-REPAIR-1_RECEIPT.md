# WO-REPAIR-1 — Post-release narrow repair iteration 1 (receipt)

Round: `POSTRELEASE-20261011-s4-narrow-repair`
Branch: `postrelease-narrow-repair-20261011`  HEAD: `dbe38719` (tree `7606c769`)
Repairs in scope: **R1** (verifier F07 — bash quickstart fails silently on Windows),
**R2** (verifier F03 — self-bootstrap README over-claims replay determinism).
No commit / push / tag / release. Working tree left modified.

Host note: the shell is Windows PowerShell; `bash` is Git Bash 5.2.37 (msys). The pinned
interpreter on this host is `...\hermes-agent\venv\Scripts\python.exe` (Python 3.11.17) whose
**venv has no `pip`**; a full Python 3.11 (`C:\Users\user\AppData\Local\Programs\Python\Python311`)
with pip 24.0 is also installed. Both are used below and the difference is called out where it
matters.

---

## R1 — bash quickstart: fail fast + portable activation

### R1.a — `python -m unittest tests.test_postrelease_quickstart -v`

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
----------------------------------------------------------------------
Ran 7 tests in 0.005s
OK
```
Exit code: **0**. Verdict: **PASS**.

### R1.b — the test now mechanically asserts the new invariants

`tests/test_postrelease_quickstart.py` gained class `QuickstartBashFailFast` with three tests
(see the literal diff below):

* `test_block_starts_with_set_e` — the quickstart bash block's **first line starts with `set -e`**.
* `test_block_activates_portably_with_windows_fallback` — some line has `||` **and**
  `.venv/Scripts/activate`.
* `test_no_bare_posix_only_activate` — any line referencing `.venv/bin/activate` must also carry a
  `||` fallback (a bare POSIX-only activate cannot be present).

Re-run: covered by R1.a above (all seven tests OK, exit 0). Verdict: **PASS**.

### R1.c — fresh-directory trace, block extracted programmatically

The bash block was extracted directly from `README.md` with a regex
(`^```bash…^```$`, first block containing the wheel + SHA256SUMS) — **not retyped** — and written to
scratch:
```
C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4post/repair/r1trace/quickstart.sh
```
First extracted line: ``set -e                             # stop at the first failing step; no step fails silently``

**Trace 1 — pinned interpreter (whose global venv has no pip) — establishes FAIL-FAST.**
Command:
```
bash -x quickstart.sh        # cwd = .../repair/r1trace
```
Raw output (complete):
```
+ set -e
+ BASE=https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2
+ curl -fsSLO .../pipd_ls_sp-0.1.0-py3-none-any.whl
+ curl -fsSLO .../SHA256SUMS
+ grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS
+ sha256sum -c -
pipd_ls_sp-0.1.0-py3-none-any.whl: OK
+ python -m venv .venv
Error: Command '[....venv\Scripts\python.exe', '-m', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1.
```
Exit code: **1**. The block **stops at `python -m venv`** — nothing after it runs, and there is no
global install. This is exactly the fail-fast behaviour R1 asked for. Verdict: **PASS**.

**Trace 2 — full Python 3.11 on PATH — exercises the venv-install path.**
Command:
```
PATH="/c/Users/user/AppData/Local/Programs/Python/Python311:$PATH" bash -x quickstart.sh \
    # cwd = .../repair/r1trace_sys
```
Exit code: **0**. Per-step exits (PS4=`+[exit=$?] `):
```
+[exit=0] BASE=...
+[exit=0] curl -fsSLO .../whl
+[exit=0] curl -fsSLO .../SHA256SUMS
+[exit=0] grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS
+[exit=0] sha256sum -c -
+[exit=0] python -m venv .venv
+[exit=0] . .venv/bin/activate              <- POSIX layout absent on Windows
+[exit=1] . .venv/Scripts/activate          <- fallback fires; exit 1 was the prior command
+[exit=0] python -m pip install ./pipd_ls_sp-0.1.0-py3-none-any.whl
+[exit=0] pipd doctor
+[exit=0] pipd --help
+[exit=0] pipd --root ./myproject init
+[exit=0] pipd doctor
```
(Note: with PS4=`+[exit=$?]` the value shown *prefixing* a command is the exit of the **preceding**
command; hence `+[exit=1] . .venv/Scripts/activate` reports that `. .venv/bin/activate` returned 1,
after which the `||` fallback sourced the Windows activate successfully.)
Install line: `Successfully installed attrs-26.1.0 jsonschema-4.26.0 … pipd-ls-sp-0.1.0 …`
`pipd doctor` resolved schemas from `...\r1trace_sys\.venv\Lib\site-packages\pipd_ls_sp\schemas`.

**Venv evidence (`pip show` / `sys.path`):**
```
=== python -m pip show pipd-ls-sp ===
Name: pipd-ls-sp
Version: 0.1.0
Location: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\s4post\repair\r1trace_sys\.venv\Lib\site-packages
Requires: jsonschema
=== sys.path (venv) ===
C:\Users\user\AppData\Local\Programs\Python\Python311\python311.zip
C:\Users\user\AppData\Local\Programs\Python\Python311\DLLs
C:\Users\user\AppData\Local\Programs\Python\Python311\Lib
C:\Users\user\AppData\Local\Programs\Python\Python311
C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\s4post\repair\r1trace_sys\.venv
C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\s4post\repair\r1trace_sys\.venv\Lib\site-packages
```
Verdict: **PASS** — the block completes **inside** the venv; it does not end with a global install.

### R1 cleanup — no global residue

Global site-packages were checked for the package **after** the runs:
```
full Python311:            pipd_ls_sp spec: None
pinned hermes-agent venv:  pipd_ls_sp spec: None
```
Nothing landed in any global site-packages, so nothing needed uninstall. Both scratch venvs created
by the runs were **removed**:
```
removed: .../repair/r1trace/.venv
removed: .../repair/r1trace_sys/.venv
```
Recoverability: the venvs are disposable scratch artefacts; the wheel is re-downloadable. Verdict: **PASS**.

---

## R2 — self-bootstrap README: state the determinism exactly as strong as the evidence

### R2.a — test encodes the corrected, weaker claim

`tests/test_postrelease_selfbootstrap.py` gained
`TestSelfBootstrap.test_replay_is_root_bound_not_root_independent` (see diff below):

* (a) two slices into the **same** root produce identical `PI/PD/ECP/TQAEP` content hashes and
  identical bundle digest;
* (b) two **different** roots produce identical `PI` and `TQAEP` hashes, while `PD`, `ECP` and the
  bundle digest **differ** — i.e. the test asserts `NotEqual` for the root-bound artefacts, matching
  the corrected claim.

Command:
```
python -m unittest tests.test_postrelease_selfbootstrap -v
```
Raw output:
```
test_chain_replay_is_deterministic ... ok
test_chain_runs_and_validates ... ok
test_missing_source_is_refused_typed ... ok
test_replay_is_root_bound_not_root_independent ... ok
test_shipped_cli_init_runs_in_isolated_root ... ok
test_stale_context_is_refused_typed ... ok
test_trace_closure_has_no_orphans ... ok
----------------------------------------------------------------------
Ran 7 tests in 0.439s
OK
```
Exit code: **0**. Verdict: **PASS**.

### R2.b — re-run the example twice into the same scratch root

Command (run twice), scratch root `.../repair/sb_replay` (outside the repo, as the driver requires):
```
PYTHONPATH=<repo>/src python examples/self-bootstrap/run_selfbootstrap.py --root \
    C:/Users/user/.../scratch/s4post/repair/sb_replay
```
Both runs: `SELFBOOT-SUMMARY verdict=PASS checked=4 … bundle_digest=436a1e7e6a56fb9c` — exit **0**.
`compare run1 run2` → **IDENTICAL**. Same-root replay is deterministic.

**Is the committed `examples/self-bootstrap/digests.json` a real replay (not stale)?** Yes.
Its `content_hash` fields recompute *exactly* to its own recorded `bundle_digest`:
```
committed bundle_digest:                   55b416c6f6e28cb074741ec932470b310a34ad1645de30278ec1af143953137a
recomputed from committed content_hashes:  55b416c6f6e28cb074741ec932470b310a34ad1645de30278ec1af143953137a
CONSISTENT
```
It differs from my fresh run **only** in the root-bound artefacts (`PD`, `ECP`, `bundle_digest`) and
the `schema_source.path` echo — which is precisely the cross-root difference F03 documents. It is
**not stale**, so `digests.json` was **not regenerated**. Verdict: **PASS**.

> Side-effect disclosure: the driver, on each positive run, unconditionally rewrites both
> `examples/self-bootstrap/digests.json` **and** `examples/self-bootstrap/negative_stale_context.txt`
> from the current run. `negative_stale_context.txt` is **outside** this WorkOrder's write scope, so
> **both files were restored to HEAD** (`git checkout --`) after the runs. No content in either file
> was changed by this repair.

---

## Literal diffs of each changed file

### `README.md`
```diff
@@ -29,6 +29,7 @@ Copy-paste, from a shell. Requires **Python >= 3.11** and `curl`.
 ### bash / POSIX
 
 ```bash
+set -e                             # stop at the first failing step; no step fails silently
 # 1. Fetch the published wheel and the checksum list, from the immutable tag.
 BASE=https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2
@@ -47,7 +48,7 @@
 # 3. Install into a virtual environment.
 python -m venv .venv
-. .venv/bin/activate               # Windows: .venv\Scripts\activate
+. .venv/bin/activate 2>/dev/null || . .venv/Scripts/activate   # POSIX: .venv/bin/ ; Windows: .venv/Scripts/
 python -m pip install ./pipd_ls_sp-0.1.0-py3-none-any.whl
```

### `examples/self-bootstrap/README.md`
```diff
@@ -15,8 +15,13 @@
-* The chain is **replay-deterministic**: no timestamp enters a digested field, so the same inputs
-  produce identical artefact digests across runs (`digests.json`).
+* The chain is **replay-deterministic for identical rooted inputs**: no timestamp enters a digested
+  field, so the **same intent, the same clause source and the same `RepoContext.root`** produce
+  identical artefact digests across runs (`digests.json`). The determinism is bounded on purpose:
+  PD binds an absolute `RepoContext.root` **by design**, and ECP is derived from PD, so a *different*
+  root legitimately yields different PD and ECP digests while PI and TQAEP stay identical. That is
+  **environment binding, not nondeterminism** — the same inputs at a different root are not the same
+  inputs.
```

### `tests/test_postrelease_quickstart.py`
```diff
+class QuickstartBashFailFast(unittest.TestCase):
+    """R1 (F07): the bash quickstart must fail fast and activate portably. ..."""
+    def _quickstart_bash(self) -> str: ...
+    def test_block_starts_with_set_e(self) -> None: ...
+    def test_block_activates_portably_with_windows_fallback(self) -> None: ...
+    def test_no_bare_posix_only_activate(self) -> None: ...
```
(full body in the working tree; three added tests, no existing test modified)

### `tests/test_postrelease_selfbootstrap.py`
```diff
+    def test_replay_is_root_bound_not_root_independent(self) -> None:
+        """The determinism the example advertises is bounded to identical rooted inputs (F03). ..."""
+        ...
```
(full body in the working tree; one added test, no existing test modified)

---

## What I did NOT do, and why

* **No code / pipeline / schema change.** R2 explicitly says not to change what is digested; the
  digest behaviour (PD binds absolute root) was left exactly as shipped, only the README claim and
  the test were corrected.
* **No checksum weakening.** The filtered wheel-line check
  (`grep '  …whl$' SHA256SUMS | sha256sum -c -`), the PowerShell block, the published digest literal,
  and the separately-labelled "no hash verification" one-line install are untouched. No second
  unlabelled install path was added; the "no hash verification" label stays.
* **No touch of out-of-scope verifier findings.** F04 (rehashed permission expansion),
  F05 (`_profile_meta` sidecar not validated), F06 (empty `trace` array), F11, F12 are **disclosed
  limitations for this round**. I added **no** cross-record authorization checks, changed **no**
  `validate.py`, and widened **no** schema. I consider none of them trivially in-scope; none was acted on.
* **No files outside the write scope were authored.** The only writes outside the listed files were
  the two scratch venvs (removed) and the driver's unavoidable rewrite of
  `negative_stale_context.txt`, which was restored to HEAD.
* **No commit / push / tag / release.** The tree is left modified.
* **No credential use, no network beyond the released wheel URL** the quickstart already uses.

## New observations

1. **`set -e` is load-bearing here, and the host proves it.** Without `set -e`, `. .venv/bin/activate`
   on this host returns 1 and the block continues; with `set -e` plus the `||` fallback the block
   *either* completes in the venv *or* aborts. The pinned interpreter's missing-pip venv turns the
   `python -m venv` step into a genuine fail-fast demonstration.
2. **The driver rewrites two tracked files on every positive run.** `run_selfbootstrap.py` writes
   `digests.json` and `negative_stale_context.txt` unconditionally. Any future replay of the example
   will dirty `negative_stale_context.txt` even when no repair is intended — worth noting for
   whoever runs it next (a `--no-write` option would help but is out of scope here).
3. **The committed digest root is reported as `C:\c\Users\...\sb_replay`** (a literal duplicate
   drive-letter segment) whereas my fresh run reported `C:\Users\...\sb_replay`. Both are SOURCE-mode
   records pointing at the repo's own `schemas\`; the malformed prefix is cosmetic in the recorded
   `schema_source.path` echo and does not affect any digest. Reported, not repaired (out of scope).

## Repair surface (end of run)

See appended `git status --porcelain` and `git diff --stat` at the foot of this receipt.

---

## Appended: repair surface at end of run

```
$ git status --porcelain
 M README.md
 M examples/self-bootstrap/README.md
 M tests/test_postrelease_quickstart.py
 M tests/test_postrelease_selfbootstrap.py
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/admission/AUTH_BLOCKED_CHECKPOINT.json
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/evidence/FROZEN_FULL_SUITE.log
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/evidence/POST_F_DISPOSITION.json
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/evidence/TT_REGISTER_S4POST.json
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/WO-CONTRACT03.exec-20261011T083646Z.log
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/WO-SELFBOOT04.exec-20261011T083646Z.log
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/WO-UX01.exec-20261011T083646Z.log
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/WO-WEB02.exec-20261011T083646Z.log
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/repair/
?? .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/verify/
```

```
$ git diff --stat
 README.md                               |  3 +-
 examples/self-bootstrap/README.md       |  9 ++++--
 tests/test_postrelease_quickstart.py    | 47 ++++++++++++++++++++++++++++++
 tests/test_postrelease_selfbootstrap.py | 51 +++++++++++++++++++++++++++++++++
 4 files changed, 107 insertions(+), 3 deletions(-)
```

Tracked-file changes are exactly the four in-scope files (the two READMEs and the two tests). No
code, schema, pipeline, or out-of-scope file was modified; `digests.json` and
`negative_stale_context.txt` are unchanged versus HEAD.
