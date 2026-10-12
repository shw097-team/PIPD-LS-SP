# S4EXT-R1 round report — PIPD-LS-SP external-challenge narrow repair

```yaml
contract: PIPD-S4EXT-R1-REPAIR-ROUTEOUT/1
round: S4EXT-R1-20261012-external-challenge-repair
compiler_verdict: PROMPT_COMPILE_PASS (lint/activation/acceptance/compile, error_count 0)
contract_sha256: 24913b1533e471242aa356868a116f2c81cbc4c40bf93a39b0c67109bc0028a1
baseline_main_hint: 0a05f4fde899d5990a8c098e3feaa2d9d1d7e0de
candidate_commit: ab06757e31b51700302422ba34094c72cc372cb5
candidate_tree: 3ec1c18f73c4d185e3ebb51a02b411b1b839326a
branch: fix/s4-external-challenge-20261012-r1-provenance-trace
remote_head_readback: ab06757e31b51700302422ba34094c72cc372cb5  (match: true)
hgk_admission: round-level WorkOrder admission REFUSED_BY_LIFECYCLE_STATE (project EXECUTING);
               checkpoint CK-20261008-7483330D recorded
push_gate: performed with the pre-existing OS credential (helper=manager); the declared token file
           was never read; no secret in any log
claim_ceiling: MAKER_CANDIDATE_AND_LOCAL_TESTS_ONLY_UNTIL_EXTERNAL_REQUALIFICATION
s4_overall: NOT_GRANTED
release_gate: HOLD
production: NOT_CLAIMED
```

## What the round proves

| id | outcome |
|---|---|
| **F001** | Repaired as a candidate. Tuple split (`build_source_commit` vs `release_tag_target`), 8/8 pack documents regenerated, `MANIFEST.sha256` recomputed over EOL-normalised member bytes. The **published** ZIP keeps its exact bytes (sha256 `73c6c7e2…`, matching the release metadata); the correction is a new `-erratum1.zip` + `docs/ERRATUM_2026-10-12_preview3_release_provenance.md`. Public action = owner. |
| **F002** | Upgraded and repaired. The **published** wheel really does return `PASS` for mis-typed / orphaned / wrong-hash trace bundles (exit 0) — a confirmed runtime false PASS. The candidate returns exit 1, `verdict FAIL`, `closure FAILED` for all three, while a legal bundle still closes `FULL` and legacy `version="1"` survives. |
| **F003** | Closed as candidate evidence: the current release identity is pinned from the frozen tuple with a stale-negative; the historical `preview.2` test is untouched. |
| **G004** | Partial: full deterministic suite re-run on the candidate — **Ran 518 tests, OK (skipped=6)**. |
| **G005** | Not run: Web GPT-6 / Hermes Agent / Codex-UI interactive UAT recorded per host as `NOT_RUN`; the CLI half ran (installed wheel, alone). |
| **G006** | Partial: the wheel and Web-ZIP digests recomputed locally **match** the published metadata; no independent byte download from GitHub in this session. |
| **O007** | Repaired: `examples/first-run/run.sh` + `run.ps1`, self-locating, precondition-checked, `FIRST_RUN_OK`, plus `PRECONDITION_FAIL` evidence. |
| **O008** | No change by design (SemVer enlargement rejected). |
| **O009** | Repaired: typed refusal for a non-string request (replacing a bare `AttributeError`) + boundary tests. |
| **TT-S4EXT-007** | Done as an adjudication: 57 rows, 13 dispositions, no status upgrade, `DEL-008` not S4-blocking, 4 `DESIGN_ONLY` rows not implemented. |

## Coverage

* 19 schema families (unchanged count), 13 CLI verbs, 8 `skills/pipd-*` logical skills.
* 57-row crosswalk: 44 `EVIDENCED` / 9 `EVIDENCE_GAP` / 4 `DESIGN_ONLY`, read back unchanged;
  adjudication adds dispositions, never statuses.
* Return pack: 30 files in `evidence/` + `MANIFEST.json` with per-file sha256.

## Security and rollback

* `tools/deny_list_scan.py` → PASS; `tools/history_secret_scan.py` → history CLEAN, worktree CLEAN.
* No tag created/moved/deleted, no published asset rewritten, no `main` push, no force, no merge.
* Rollback: `git branch -D fix/s4-external-challenge-20261012-r1-provenance-trace` (local) and
  `git push origin --delete <branch>` (owner-gated); nothing else to undo.

## Open

* `TT-S4EXT-008` resolved as a role-separation record; `TT-S4EXT-009` (R04 wording) open at the knowledge owner;
  `TT-S4EXT-010` round-level WorkOrder admission open at the HG-KSEOS owner;
  `TT-S4EXT-011` owner acceptance per crosswalk disposition.
* Independent requalification of `ab06757e…` — not performed by the maker and not claimed.

**Next legal action:** an external verifier re-runs the replay commands in
`evidence/09_CHALLENGE/checker_identity.json` against `ab06757e…`; the release owner then decides
erratum vs new preview. Nothing in this round is `RELEASED` or `PRODUCTION_VERIFIED`.
