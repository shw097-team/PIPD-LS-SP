# WO-S4-SELFBOOT-04 receipt — source-constrained self-bootstrap example

Round: `POSTRELEASE-20261011-s4-narrow-repair`
Task: `WO-S4-SELFBOOT-04` (P2 LIMITED ACTIVE, post-release narrow repair)
Writer: Codex bounded writer (`deepseek-v4.1-flash`)
Interpreter (pinned): `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`
  (Python `3.11.9`, `jsonschema 4.26.0`)
Candidate head at work start: `4445db5a6d1b3138946fd7c4fe3b712e4faf1af7`
Ceiling: **candidate-only — no commit, no push, no tag, no release.**

Admitted write scope actually written:

* `docs/NORMATIVE_SOURCE_MAP.md` (new)
* `examples/self-bootstrap/**` (new)
* `tests/test_postrelease_selfbootstrap.py` (new)
* `.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/**` (this receipt + raw run logs)

No other file was written. `README.md`, `schemas/**`, `src/**`, `dist/**`, `tools/**` and the other
`tests/test_postrelease_*.py` files carry **pre-existing / other-WO** changes that this WorkOrder did
not touch (see §7).

---

## 0. Summary

| Part | Delivered | Evidence |
|---|---|---|
| 1. `docs/NORMATIVE_SOURCE_MAP.md` | DERIVED INDEX; owner/version/digest-or-marker/locator/consumers per source family | file + §5 |
| 2. `examples/self-bootstrap/` | replayable example driven by the SHIPPED CLI in an isolated root | `transcript.txt`, `digests.json`, `negative_stale_context.txt` |
| 3. Positive path | `init → intake → compile-pi → bind-pd → compile-ecp → compile-tqaep → validate` = `PASS` | §3.1 |
| 3. Negatives | missing source → `AUTHORITY_UNKNOWN`; stale context → `STALE_PROVIDER`; both exit 2 | §3.2 |
| 3. Replay | same root, same inputs → **byte-identical `digests.json`** | §3.3 |
| 4. Unit test | `tests/test_postrelease_selfbootstrap.py` 6/6 `ok`; baseline 7/7 `ok` | §3.4 |

---

## 1. Part 1 — `docs/NORMATIVE_SOURCE_MAP.md`

Opens with the required header: **this file is a DERIVED INDEX, not a competing master; the external
canonical standard remains the single source of truth; bodies are not copied here.**

Covered: the external SSOT `PIPD-LIFECYCLE-SPEC@1.1.0` (authoritative, **not restated**), the
Blueprint (`PIPD-LS-SP_藍圖`), the skeleton (`PIPD-LS-SP_skeleton`), the 11 packages
`PIPD-PKG-00..10`, and the 10 documents `PIPD_LS_DOC-00..09`. Each family records owning authority,
version, a SHA-256, an external locator, and consumers (8 skills / 19 schema families / S0–S4).

Digest policy: every per-file digest was **recomputed live from disk** and cross-checked against the
in-repo preflight manifest `.hgk/preflight/source-manifest.json` (all `OK`); family digests are the
manifest `manifest_sha256` values quoted as recorded. No digest was invented. Had a source been
unreadable here, the cell would read `NOT_VERIFIED_HERE` (digest) or `NOT_PUBLIC`; as written every
named source was readable, so no marker was needed. The map contains **identity metadata only** — no
PKG/DOC/blueprint/skeleton body is copied into the repository.

> One header correction was made after the first draft: the provenance line now points at this
> receipt's real path (`.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/WO-S4-SELFBOOT-04_RECEIPT.md`)
> instead of a placeholder `law/…` path.

---

## 2. Part 2 — `examples/self-bootstrap/`

```
examples/self-bootstrap/
  README.md                     # what it proves / does NOT prove
  input/intent.json             # minimal intent card (goal + one source locator)
  input/source_clauses.txt      # the self-contained clause source atoms are compiled from
  input/repocontext.json        # minimal read-only RepoContext template
  run_selfbootstrap.py          # driver: creates the workspace in an isolated root via the CLI
  digests.json                  # recomputed digests of the ACTUAL run
  transcript.txt                # REAL stdout/stderr/exit of the positive run
  negative_stale_context.txt    # REAL output of the two negative cases
```

`run_selfbootstrap.py` uses the **real signatures** read from `src/pipd_ls_sp/cli.py` and
`src/pipd_ls_sp/pipeline.py`; no flag is invented. The CLI is invoked as the shipped module entry
point `python -m pipd_ls_sp.cli` (global `--root` before the subcommand). `--root` is **refused** if
it resolves inside the repository. The workspace is always created outside the repository.

`transcript.txt` and `negative_stale_context.txt` were produced by **actually running** the script and
capturing its output — no expected transcript was hand-authored.

---

## 3. Named acceptance commands (raw output + exit codes)

All commands run from `<repo> = C:/Projects/Agent_Workspace/PIPD-postrelease-wt` with
`PYTHONPATH=<repo>/src`.

### 3.1 Positive run

```
PYTHONPATH=<repo>/src <interpreter> examples/self-bootstrap/run_selfbootstrap.py \
    --root C:/Projects/Agent_Workspace/_wo_s4_selfboot
```

Exit **0**. Summary line (from `transcript.txt`, line 558):

```
SELFBOOT-SUMMARY verdict=PASS checked=4 pi=PI-1b3b61e57cad3299 pd=PD-a1d27321a2195bc8 ecp=ECP-ad91032dd572e923 tqaep=TQAEP-4946f4ef45cee5b4 bundle_digest=cf370ce96b6de3b4
```

The `validate` step reported:

```
{"checked": 4, "findings": [], "verdict": "PASS",
 "schema_source": {"mode": "SOURCE", "path": ".../PIPD-postrelease-wt/schemas", ...}}
```

The printed summary matches `digests.json` (`bundle_digest` `cf370ce9…`, and each `subject_id`).

### 3.2 Negative runs (each expect non-zero, typed)

```
PYTHONPATH=<repo>/src <interpreter> examples/self-bootstrap/run_selfbootstrap.py \
    --root C:/Projects/Agent_Workspace/_wo_s4_accB --negative missing-source
```
Exit **2**:

```
{"code": "AUTHORITY_UNKNOWN", "exit": 2, "message": "source locator does not exist: examples/self-bootstrap/input/does_not_exist.txt", "verdict": "FAIL"}
```

```
PYTHONPATH=<repo>/src <interpreter> examples/self-bootstrap/run_selfbootstrap.py \
    --root C:/Projects/Agent_Workspace/_wo_s4_neg_stale --negative stale-context
```
Exit **2**:

```
{"code": "STALE_PROVIDER", "exit": 2, "message": "stale currentness claim: claimed epoch 0000000000000000... != host-derived 583419010c029946...", "verdict": "FAIL"}
```

Both negatives are also exercised **inside the positive run**, and their raw output is written to
`negative_stale_context.txt`. A `RepoContext` missing `root` is likewise refused
`REPO_CONTEXT_MISSING` (covered by `tests/test_s1_lite_slice.py`).

### 3.3 Replay claim (positive run × 2)

```
run 1: run_selfbootstrap.py --root <R>   # → digests.json (copy kept as lane/WO-SELFBOOT04.digests.run1.json)
run 2: run_selfbootstrap.py --root <R>   # → digests.json (copy kept as lane/WO-SELFBOOT04.digests.run2.json)
```

`digests.run1.json` and `digests.run2.json` are **byte-identical** (`DIGESTS_REPLAY_IDENTICAL=YES`).

Honest qualifier: the byte-identical claim holds for a **fixed** `--root`. `bind-pd` derives the
`RepoContext` from the actual host directory, so two runs against **different** roots produce the
same PI/ECP/TQAEP digests but a different PD digest (the root path is inside the hashed
`RepoContext`). Recomputed-of-the-same-inputs determinism is therefore a per-root property (or
root-independent for every artefact above PD), and the receipt states it that way rather than
overclaiming. The one transcript line that differs between run 1 and run 2 is the idempotent
`init` echo (`created` list empty on the second `init`, because the dirs already exist); it carries
no artefact digest.

### 3.4 Unit tests

```
PYTHONPATH=<repo>/src <interpreter> -m unittest tests.test_postrelease_selfbootstrap -v
```

Exit **0** — `Ran 6 tests … OK` (all six `ok`):
`test_chain_replay_is_deterministic`, `test_chain_runs_and_validates`,
`test_missing_source_is_refused_typed`, `test_shipped_cli_init_runs_in_isolated_root`,
`test_stale_context_is_refused_typed`, `test_trace_closure_has_no_orphans`.
Raw: `lane/WO-SELFBOOT04.unittest.log`.

```
PYTHONPATH=<repo>/src <interpreter> -m unittest tests.test_s1_lite_slice -v
```

Exit **0** — `Ran 7 tests … OK` (**baseline did not regress**).
Raw: `lane/WO-SELFBOOT04.baseline.log`.

---

## 4. Recomputed digests (positive run; from `digests.json`)

| Artefact | `subject_id` | `content_hash` | file `sha256` |
|---|---|---|---|
| IntentCard | `INTENT-c80197cd8fe6675b` | `c80197cd8fe6675be5bf6f23f9e94fe902aaa17c69423406d219f26edf899c5a` | `7d4131add0442c3742137e0da18222d273cc27b7f6ab632914c47d1b86a1e2c2` |
| PI-PKG | `PI-1b3b61e57cad3299` | `1b3b61e57cad3299ceac90cc48fb27a4cacfeac25828abc52560b7910780d31f` | `4a526e74cfbcb318fbb85a0ab23d23632678aba2482e1e72e30ab0f00c03e21a` |
| PD-PKG | `PD-a1d27321a2195bc8` | `a1d27321a2195bc8e15abf6a4e3a34136dfeaff386ef0b6fa4cf2cc31ef1e03a` | `05d79cc214c2d8ca186819f10b31934eee7c2ff5efc6318954fb9377cb597d82` |
| ECP | `ECP-ad91032dd572e923` | `ad91032dd572e923ee60f22ac552a7b7b236e462dfc679124f33933dcfe2bf86` | `495b6e3777b64ad7a2b11852ee531d2f4a9ed1738ce36f5b528c7ac6996eab75` |
| TQAEP | `TQAEP-4946f4ef45cee5b4` | `4946f4ef45cee5b45fc29103561eeb6a065aa08a43527449117f700f2a0bcf34` | `ee9c0120a04adc9a28b82183a7c7d9e112d568a6ad49e2361e98b48ad40afec0` |

`bundle_digest = cf370ce96b6de3b4414c8bb195d83d25632321e0b0e284375895dec9f388240d`
(sha256 over the canonical `{name: content_hash}` rows; no timestamp is inside any digested field).

Repo file hashes at this writing: `examples/self-bootstrap/digests.json` =
`c9f8aa9f6238c3acd1478923a0f6c5ffc5a93e53ceae65f599fa94f930ffb576`;
`transcript.txt` = `22bd208c24b15cd0fba3634034cfe797b1d72fe0e629c61d9041d43fe4cbbbe8`;
`negative_stale_context.txt` = `58da690943b8770a326de2b55cd10ff29b2d82ddb85619d87478d778281ce293`.
`schemas/registry.json` = `85100a8e5ba6320f6648d33a14099fb999b2c452a94aff1652854d2550065e9d`.

---

## 5. What the example does NOT prove

* **Not independent acceptance.** The TQAEP record is a design-time candidate
  (`claim_ceiling = TQAEP_DESIGNED`, `independent_acceptance = NOT_GRANTED`); the checker receipt
  `deleg_example/lane-C` is recorded, not verified. A live S5 runtime checker must re-run it before
  any independent acceptance can be claimed.
* **Not a release.** No commit/push/tag/release; candidate artefact only.
* **Not the whole lifecycle.** Only the S1 LITE vertical slice is exercised; S0 source freeze,
  S2 technology admission, S3 surface/GENIE projection and all runtime stages are out of scope.
* **Not the external standard.** It does not restate, re-derive or copy any body of
  `PIPD-LIFECYCLE-SPEC@1.1.0`, the Blueprint, the packages or the documents; it binds only a
  self-contained local clause source.
* **Not a correctness proof of the compiler's semantics.** It shows the chain runs and refuses the
  two named negatives; it is not a proof that the compiler is semantically right.
* **Not a proof that real knowledge-base sources compile.** The example deliberately uses a local
  clause file so no external knowledge source is required at run time.

---

## 6. NOT_RUN items and reasons

| Item | Status | Reason |
|---|---|---|
| `compile-construction-contract` as a CLI subcommand | **NOT_RUN (not a CLI verb)** | The 13-command surface (`cli.COMMANDS`) does not expose it. It is exercised only through the pipeline API, in `tests/test_postrelease_selfbootstrap.py::test_chain_runs_and_validates`, and stated as such in `examples/self-bootstrap/README.md`. Not skipped silently. |
| S0 freeze / S2 admission / S3 projection / S5 runtime | **NOT_RUN** | Out of this WorkOrder's S1-LITE scope; the brief asks for the intent→…→validate chain only. |
| `pipd` console entry point (vs `python -m pipd_ls_sp.cli`) | **NOT_RUN** | No `pipd` shim is installed on this workstation's PATH; the shipped module entry point is the reproducible invocation and is what the acceptance commands use. |
| Live external source re-read for §2.1/§2.4/§2.5 bodies | **NOT_RUN** | Governance forbids copying PKG/DOC/blueprint/skeleton bodies into the repo; only digests/locators are indexed. Per-file digests were recomputed without copying bodies. |
| Standalone `--negative stale-context` in the brief's command list | **RUN anyway** | Not in the brief's three acceptance lines, but run for completeness (§3.2); exit 2, typed `STALE_PROVIDER`. |

---

## 7. Repo hygiene

* All disposable roots were created **outside** the repository (`_wo_s4_*` under
  `C:/Projects/Agent_Workspace/`), verified to resolve outside the repo, and removed after the run.
* `git status` shows this WorkOrder's deliverables as the only additions from this WO:
  `docs/NORMATIVE_SOURCE_MAP.md`, `examples/self-bootstrap/**`,
  `tests/test_postrelease_selfbootstrap.py`, and this `lane/` tree. No tracked file under
  `schemas/`, `src/`, `dist/`, `tools/`, `README.md` or another test file was modified by this WO.

Raw captures kept in this lane (`lane/`):

`WO-SELFBOOT04.positive1.txt`, `WO-SELFBOOT04.positive2.txt`, `WO-SELFBOOT04.positive.run2.txt`,
`WO-SELFBOOT04.digests.run1.json`, `WO-SELFBOOT04.digests.run2.json`,
`WO-SELFBOOT04.neg_missing.txt`, `WO-SELFBOOT04.neg_stale.txt`,
`WO-SELFBOOT04.negatives.run1.txt`, `WO-SELFBOOT04.unittest.log`, `WO-SELFBOOT04.baseline.log`.
