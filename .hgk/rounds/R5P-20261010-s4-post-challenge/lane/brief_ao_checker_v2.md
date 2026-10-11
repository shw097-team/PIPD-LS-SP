# INDEPENDENT CHECKER BRIEF — R5P focused re-verification (attempt 2) — PIPD-LS-SP

You are the independent Acceptance Officer for the **R5P** round (post-challenge S4 focused repair)
of `PIPD-LS-SP`. Your first pass returned `FAIL` with 5 of 8 checks failing. The maker has since
repaired two of them and produced evidence about the other three. **Your job now is to re-derive, on
the NEW frozen subject, whether each disputed check still fails — and to say so from your own raw
runs, not from this brief and not from the maker's files.**

## 0. Frozen subject

| role | value |
|---|---|
| baseline | `r5-s4-packreader` @ `0f06eec96386b7349db8b41ac6cf9c7455d326f1` (tree `1f7564282fd708fab2ddeadbbbe4e424a3c564be`) |
| round code commit | `b3d08b7d651a548ae74dc45453224fe393c41269` |
| round packaging commit | `0f64d1f8f84ca3f5815254353abcc039589d457d` |
| **round repair commit = re-verification subject** | **`812af79422c087f0ef5a07188fbec061df6b47e0`** (tree `d3b79d2bc7aba08368a02a9f34204d14c9b06bbd`) |
| wheel (unchanged by the repair) | sha256 `bb070a6f525382edc521bcf7fe127579e1e329024113ab4fe2881eeeea7b0a76`, 231852 bytes |
| claim ceiling | `CANDIDATE_ONLY` — you may not promote anything |

Mounts:
- `/w` — **pristine export of `812af79`** (read-only, no `.git`, no round scratch).
- `/round` — this round's own evidence (read-only). **Candidate evidence, not proof.**
- `/briefs` — lane scripts/briefs (read-only).
- `/ao` — your output directory (the only writable place).

## 1. Your first pass (attempt 1) — what you already reported

`C1_DOCTOR_TRUTH PASS`; `C3`/`C5 PASS`. FAILs:

| id | your finding |
|---|---|
| `C2_DETERMINISTIC_SUITE` | 301 tests, 10 failures, 15 errors, 15 skipped |
| `C4_PER_ATOM_GATE` | identical filler 5316.2 FAIL, but **re-stamped `subject_id` filler 161.6 PASS** |
| `C6_DOCS` | `README` names the wrong current branch |
| `C7_SECURITY_FAIL_CLOSED` | `repair --subject C:/Windows/system32/x.dll --authorized-root /w` exits 0 CANDIDATE |
| `C8_SUBJECT_BINDING` | digest `f2b288ad…`, 283 files ≠ brief's `4a039259…` |

## 2. What the maker changed since (verify, do not trust)

1. **C4 repair.** `tools/perf_budget.py` no longer counts obligations by `subject_id`. An obligation
   must carry a statement; its identity is sha256 of the normalised statement. Statement-less atoms
   are counted separately as `unvalidated_atom_count` and never vote; the rejected identity-addressed
   count and the rate it would have produced are printed beside the vote.
2. **C6 repair.** `README.md` line ~38 now names `r5p-post-challenge-repair` (baseline
   `r5-s4-packreader` @ `0f06eec9`).
3. **C8 definition fixed.** `ops/bound_digest.py` in `/round/ops/` publishes the ONE bound
   definition (`product_snapshot.walk` scope) and labels the narrower `equivalence.py` scope as
   rejected. `/round/evidence/DIGEST_BINDING.json` carries both numbers for `812af79`.
4. **C7 explanation.** The disputed case is also an existing in-repo test,
   `tests/test_negative_and_rollback.py::TestRollback::test_repair_subject_must_also_be_inside_the_authorised_root`,
   parameterised on `C:/Windows/system32/x.dll`. On Windows that spelling is absolute and outside the
   authorised root, so the guard fires; on Linux the same string is a *relative* path. The maker's
   host run of that test (Windows) passes. Judge for yourself whether the product is at fault, and
   say what the honest cross-platform claim is.
5. **C2 explanation.** The container has no `git` and mounts `/w` read-only, so git-dependent and
   write-dependent tests cannot pass there. The maker ran the suite on a clean Windows worktree of
   `812af79` (`/round/evidence/host_fullsuite_repair.txt`). **Do not re-run the full suite here** —
   instead state plainly whether the container is a valid suite environment at all, and require the
   host raw file as the suite evidence.

## 3. Checks you must re-derive on `812af79` (your own runs, in this order)

1. `C1` — rebuild the wheel from `/w` in `/ao`, install into a fresh venv, and re-run the two B4
   mutations (RECORD unchanged / RECORD adjusted, legitimately named wheel, `ArtifactIdentity.schema.json`
   removed). Each must install, then `pipd doctor` must exit non-zero with a typed FAIL naming
   ArtifactIdentity, and the health control must exit 0 with 19/19. **Confirm your earlier PASS still
   holds on this subject.**
2. `C4` — reproduce your exact dilution attack against `tools/perf_budget.py` in `/w`, both variants:
   (a) byte-identical filler, (b) identical filler re-stamped with fresh `subject_id`/`req_id`. Report
   the voting metric, the denominator, and both rates. **The re-stamped variant must no longer reach
   or fall below the budget.** Also confirm the historical `context_bytes_per_artefact 343547 > 20000`
   FAIL row is still present and unrewritten.
3. `C6` — read `/w/README.md` yourself and decide whether a first-screen reader can tell which branch
   is under review, what the licence grants, and where acceptance lives.
4. `C7` — re-run your security probe AND the in-repo test above; state the platform condition under
   which each verdict holds. If you believe the product is still at fault, give the exact argv and
   the invariant you think it violates.
5. `C8` — run `/round/ops/bound_digest.py /w` and compare its `bound_product_digest` with
   `/round/evidence/DIGEST_BINDING.json`. Say whether one definition is now unambiguous, and whether
   the digest you re-derived matches.
6. `C2` — decide, from `/round/evidence/host_fullsuite_repair.txt` and your own reading of the failing
   tests in `/w/tests/`, whether any of your container failures are product defects. Name them if so.

## 4. Rules

- Read-only on `/w`; write only under `/ao`. Never modify the product. Never use `git` state — there
  is none in `/w`; use file hashes.
- No credentials, no network, no `pip install` from an index; build the wheel from `/w` only.
- Every claim needs `command`, `exit`, raw stdout/stderr file, and the file/line it rests on.
- Distinguish `CONFIRMED_DEFECT`, `EVIDENCE_GAP`, `ORACLE_DISAGREEMENT` (your oracle was wrong),
  `NON_BLOCKING_OBSERVATION`, `OUT_OF_SCOPE`.
- Do not promote the claim ceiling. You may not issue `RELEASED`, `PRODUCTION_VERIFIED`, or accept on
  the maker's behalf.

## 5. Deliverables (write into `/ao`)

1. `AO_VERDICT_V2.json`:
```json
{"checker_id": "...", "subject_commit": "812af79422c087f0ef5a07188fbec061df6b47e0",
 "subject_tree": "d3b79d2bc7aba08368a02a9f34204d14c9b06bbd", "wheel_sha256": "...",
 "checks": [{"id": "C1", "verdict": "PASS|FAIL", "evidence": "path", "note": "..."}],
 "attempt1_recheck": [{"id": "C4", "attempt1": "FAIL", "now": "PASS|FAIL", "why": "..."}],
 "classification": {"<check>": "CONFIRMED_DEFECT|EVIDENCE_GAP|ORACLE_DISAGREEMENT|NON_BLOCKING_OBSERVATION|OUT_OF_SCOPE"},
 "overall": "PASS|FAIL|PARTIAL", "independent_of_maker": true,
 "human_ratification": "PENDING", "claim_ceiling": "CANDIDATE_ONLY"}
```
2. `AO_V2.log` — human-readable, in繁體中文, with the raw numbers you measured.
3. Raw stdout/stderr for every command you ran.

Report at the end: `AO_V2 <overall> C1=.. C2=.. C4=.. C6=.. C7=.. C8=..`
