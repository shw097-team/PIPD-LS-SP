# FAR-PIPD-S4EXT-ARTIFACT-SELFREF-001 — Research Synthesis

**Gate 1 verdict: `CONFIRMS_USEFUL`** (proposal_hash `08d6274ff365fd07`) · `gate2_user_submission_allowed: true`
**Owner authority: granted** — the user authorized executing the adjudication ("用戶授權執行「FAR 裁決建議」").
**Round verdict is unchanged by this document.** The round stays `FAIL_CHALLENGE` until an independent
run says otherwise; nothing here is a self-acceptance.

## 1. What was asked

Two tracked files are written by the repository's own tooling during a mandated acceptance run, so a
read-only verifier watched the candidate mutate under it. The user authorized automatic FAR research
with a "low resistance, high engineering necessity" adjudication, executed directly.

## 2. What the study found (including where it corrected itself)

| # | Finding | Status |
|---|---|---|
| 1 | `candidate_head` in `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json` is a **generation-time identity**, and the house already declares this semantics elsewhere (`tools/build_dist.py:192`; `docs/ROUND3_DISCLOSURE.md` item A6 fixed the same class by renaming a field and adding a binding note, not by rewriting a generator) | FACT |
| 2 | The commuting value is an **ancestor** of HEAD, measured at **69 commits behind** — so the first draft's rule "`candidate_head == HEAD` or `HEAD^`" was **wrong** and was retracted | **CORRECTED** |
| 3 | The first draft's inference "no digest chain exists to break" was **wrong**: `.hgk/artifacts/evidence_manifest.json` records both digests and `tools/build_publication_manifest.py` folds `local_sha256` into `crosswalk_digest` | **CORRECTED** |
| 4 | Crosswalk **rows** do carry only paths (`tools/build_spec_del_crosswalk.py:407-409` checks existence) — the narrow claim stands, the broad inference did not | PARTIAL |
| 5 | No tool or test recomputes per-entry digests against disk, so regeneration makes the chain **silently** stale. Measured **before** this change: **1085 entries, 1044 match, 0 missing, 41 stale** | NEW DEFECT CLASS (TT-S4EXT-021) |
| 6 | The AO's read-only violation had a **precise root cause**: `tests/test_technology_admission.py:156` ran the generator without `--artifact`, so the **suite itself** rewrote the tracked file (AO attempt 3, pinned to file:line) | CONFIRMED DEFECT (TT-S4EXT-022) |
| 7 | Some artifacts name a `candidate_head` that is **not an ancestor of HEAD** at all (`s2/PERF_BUDGET.json`, `s2/pilots/GOLDEN_PILOTS.json`, `gp01-03.json`) | NEW FINDING, reported not fixed (TT-S4EXT-024) |

Lane C — an independent fresh-context challenger told to **falsify** rather than confirm — returned
`PARTIALLY_CONFIRMS` and falsified rows 2 and 3. That is why this study is worth more than its
starting symptom: the falsifications produced the digest discovery (row 5).

## 3. Adjudication executed (authorized)

| FAR item | Change | Resistance | Necessity |
|---|---|---|---|
| **F-018-A-REVISED** | `tests/test_technology_admission.py` call site redirected to a temporary `--artifact` copy (assertions unchanged) **+** `admit_technologies.py` gains `--for-commit <sha>` so the generation identity is reproducible | LOW | HIGH |
| **F-019-A** | `tools/history_secret_scan.py` gains an optional `--out PATH`; default unchanged (the file had no argument parser at all) | LOW | HIGH |
| **F-020-A** | new `tools/verify_evidence_digests.py` recomputes per-entry sha256 against disk and checks identity ancestry. **Reports by default; `--strict` opts in.** A hard repo-wide gate would have been a different, larger change and would have turned the repo red on arrival (41 pre-existing stale entries) | LOW | HIGH |

Rejected: F-018-C (delete the field) and F-019-C (declare it generated output and change nothing) —
both would leave the literal acceptance rule unsatisfiable.

**The rule was not narrowed.** The maker's position throughout: fix the tools so the verifier's literal
"any candidate mutation voids the verdict" rule becomes satisfiable, never relax the rule after a FAIL.

## 4. Verification of the execution (by the author, and then independently)

Author-side, after the writer's change:

- `python -m unittest tests.test_s4ext_artifact_reproducibility` → **Ran 4, OK**
- `python -m unittest tests.test_technology_admission tests.test_evidence_manifest tests.test_tooling_executes` → **Ran 28, OK (skipped=1)**
- `python -m unittest discover -s tests -t .` → **Ran 525 tests, OK (skipped=6), exit 0**
- **`.hgk/artifacts/` was empty BEFORE and empty AFTER that full run** — the exact condition three AO
  attempts failed on
- `python tools/verify_evidence_digests.py` → `checked 1085, match 1041, missing 0, stale 44`
  (41 pre-existing + 3 files edited by this change itself, as the writer disclosed), `identity_checks 56`

Writer lane disclosure: the bounded writer (Codex CLI) accidentally ran the generator once without
`--artifact`, rewrote the tracked artifact, restored it from HEAD, and disclosed it. That accident is
itself the AO's root cause reproduced live, which is why the call-site fix — not a workaround — is the
right remedy.

## 5. Lane incidents (disclosed, not silent)

- **D-03**: the round's mandated EXECUTE model `opencode-go/deepseek-v4.1-flash` cannot sustain a
  tool-calling session through the local adapter — `Provider error 400: The reasoning_content in the
  thinking mode must be passed back to the API`. It made no file changes.
- **D-04**: per the user's standing rule (switch to the lane's backup and continue, do not pause), the
  writer ran on `opencode-go/deepseek-v4-flash` — same provider, sibling without the thinking-mode
  defect — probed with a two-turn tool call before use. Declared and actual models are both recorded.

## 6. Nonclaims

- No product behaviour, schema, gate, claim ceiling or published artifact is asserted wrong.
- `FAIL_CHALLENGE` remains the round's independent verdict until a fresh run clears it.
- The 41 pre-existing stale digests and the non-ancestor identities (TT-S4EXT-024) are **reported,
  owned elsewhere, and not fixed here**.
- Nothing in this study is a release, publication or production claim.
