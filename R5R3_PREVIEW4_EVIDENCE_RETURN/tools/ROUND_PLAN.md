# R5R3-20261016 — S4 R5 / Preview.4 LIVE-SUBJECT CLOSEOUT (delta-only)

Round id: `R5R3-20261016-preview4-live-closeout`  ·  created 2026-10-16 (Asia/Taipei)
Governing order: `PIPD-S4-R5-PREVIEW4-PRIVATE-PLUGIN-ROUTEOUT/1` (PROMPT-3) + `PIPD-S4-EXT-ACCEPT-R5-20261014` challenge verdict (report -3)
Control plane: HG-KSEOS (`AGENTS.md` v2026-10-15.1) · Orchestration plane: Hermes · Product root: `C:/Projects/Agent_Workspace/PIPD`
Claim ceiling for this round: `CANDIDATE_ONLY` / machine gate + independent-checker verdict; nothing here is an Owner acceptance.

---

## 0. TS-00 FREEZE — live subject read (2026-10-16, not the 2026-10-14 report's subject)

| object | live value (re-read this session) |
|---|---|
| PIPD-LS-SP `origin/main` | `dba4b19456777d3b597fdf71480f6423dd974243` (PR #13 merge) |
| product worktree used for verification | `C:/Projects/wt-r5r3` (detached at that commit, `git worktree add`) |
| `v0.1.1-preview.4` | **published** 2026-10-14T10:37:36Z, target `main`, 7 assets |
| releases on the repo | preview.1, preview.2, preview.3, **preview.4** → no new tag is required by the R5 order |
| closed/merged PRs | #1..#13 (incl. #11 = D1/D2 + ClaimCeiling + preview.4, #12, #13 = per-segment/no-space boundary) |
| open draft PRs (prior rounds) | #14 (R6 candidate packet), #15 (R7-0 evidence, `src/` untouched) |
| local PIPD worktree | branch `r5p-post-challenge-repair` @ `2efc84e` — 228 commits BEHIND `origin/main`; carries uncommitted R7-0 candidate edits in `src/` → **not used as subject** |

**Delta-only disposition (mandatory, from the order §5 TS-00):** D1/D2 and `preview.4` already exist ⇒ this round does
NOT redo them. It re-derives the acceptance edges on the LIVE subject, repairs only genuine deltas, and closes the
change set with an evidence-return pack.

**Not re-opened (belongs to successor change sets, carried forward as TT, never silently dropped):**
`BLK-R7-WS1-STALE-BASELINE` (R7-0 hardening measured only on the `9bd33a1` tree), CNV R6/R7 backlog
(`R7_BLOCKERS_AND_TASKS.json` R7-01..09, 221 acceptance cases not run, Gates G-A..G-H 0/8, AUD-24 0/24),
PKG source #6 `FAIL_CLOSED`, 20 KP `*-R04` polarity defects (quarantined).

---

## 1. 核心大目標 (core goal)

On the LIVE subject (`main@dba4b19` + `v0.1.1-preview.4` served bytes), independently re-derive **every acceptance
edge the R5 challenge verdict names**, repair only genuine deltas inside a bounded WriteSet, publish a
machine-readable evidence-return pack to the repo for external acceptance, and emit the S4 phase verdict from
measured evidence — `S4_PREVIEW_MVP_PHASE_TEMP_CLOSED` only if all edges pass; otherwise `PARTIAL` /
`RELEASE_HOLD` with the exact failing edge. Permanent ceilings stay: `PUBLIC_DIRECTORY=OUT_OF_SCOPE`,
`S4_FULL_PASS=NOT_GRANTED`, `PRODUCTION=NOT_GRANTED`.

Completion function (order §1): `D1D2_NEG/POS_GREEN ∧ REAL_CI_EXIT_GREEN ∧ TRACE_NO_FALSE_PASS ∧
WHEEL_CLEAN_INSTALL ∧ PRIVATE_ZIP_8_SKILLS_SAFE ∧ IMMUTABLE_RELEASE_TUPLE ∧ SERVED_ASSET_HASH_READBACK ∧
OWNER_RELEASE_APPROVAL`.

## 2. 任務執行 SPEC (TS-00..TS-08, delta-only mapping)

| TS | R5 order intent | THIS round's delta-only action |
|---|---|---|
| TS-00 `FREEZE` | freeze refs/CI/release/skills | DONE above; subject = `dba4b19` + preview.4 |
| TS-01 `PATCH-D1` | negation polarity repair | **verify-only**: re-run the R5 counterexamples (zh/en new negatives, baseline positives, mixed scope) against the frozen tree; repair only a reproduced failure |
| TS-02 `PATCH-D2` | clause-boundary repair | **verify-only**: `api.example.com` / `v1.2.3` / `1.25` stay single atoms, two real sentences → 2 atoms, span/hash preserved |
| TS-03 `TYPE5` | ClaimCeiling 5 shapes | **verify-only**: 5 adversarial shapes → typed findings (no native exception) + legal positives not degraded |
| TS-04 `DEV+TQAEP` | red/green, full suite, wheel clean install, trace negatives | **run on the frozen subject**: real exit codes, wheel clean-venv install, `pipd doctor`, orphan/wrong-hash trace negatives |
| TS-05 `SCOPED-PR` | bounded PR | a **round-evidence PR** only (no product change unless a delta is found) |
| TS-06 `PREVIEW4-ONE-PACK` | one immutable preview.4 pack | **already released** ⇒ served-byte readback + SHA256SUMS reconciliation, no re-release, no tag move |
| TS-07 `PRIVATE-PLUGIN-SMOKE` | real private host smoke | recorded honestly as `NOT_SUPPORTED_FOR_ACCOUNT` unless an entitled account UI is driven; the ZIP is verified statically |
| TS-08 `CLOSE` | independent checker, cold re-derivation | VERIFY/SECURITY sealed lane on the frozen subject + verdict |

## 3. 任務執行清單 (CK-01..CK-15 — every item must carry an Evidence ID or an honest non-PASS status)

- [ ] CK-01 compiler lint/activation/acceptance/compile receipt + HGK WorkOrder admission
- [ ] CK-02 live main/release/tags/PR/CI + local HEAD frozen; R4/R5 work not redone
- [ ] CK-03 D1 new negatives + existing baselines + mixed scope, source locator preserved
- [ ] CK-04 D2 domain/version/decimal single-atom + true two-sentence split, span/hash stable
- [ ] CK-05 TYPE5 five shapes `PASS` or a written `DEFER_P2` with compatibility risk
- [ ] CK-06 exact allowlist/denied list, diff, rollback, no secret exposure
- [ ] CK-07 full + focused suite + trace error inputs + wheel clean venv, real exit codes
- [ ] CK-08 security negatives / fake PASS / prompt injection / 9th skill / illegal ZIP refused
- [ ] CK-09 bounded PR push + Owner/independent review; merged main SHA read back
- [ ] CK-10 tag → green main; wheel/source/web-fallback/private ZIP identity aligned
- [ ] CK-11 plugin ZIP 8/8 skills, one root, one manifest, CRC/paths/secrets/2×SHA
- [ ] CK-12 every served release asset SHA256 == SUMS/ReleaseTuple
- [ ] CK-13 README / install SSOT / user guide expose the ZIP + private-permission ceiling
- [ ] CK-14 private host smoke with POS/NEG or explicit `NOT_SUPPORTED_FOR_ACCOUNT`
- [ ] CK-15 independent checker binding / Owner ratification / TT-CR / phase verdict readback

## 4. 檢測清單 (machine self-check — this round's own harness)

`selfcheck_r5r3.py` re-derives each invariant from LIVE evidence (never from this round's own summary files) and
prints `PASS/FAIL/INCONCLUSIVE` per check plus the claim ceiling on every run. `INCONCLUSIVE` is never a pass.
The harness never prints PASS for an acceptance, an approval or a Gate.

1. `S1 subject_binding` — the reported subject commit equals `git rev-parse origin/main` and the wheel/ZIP/source
   assets of `v0.1.1-preview.4` hash to the values recorded in the pack.
2. `S2 d1_polarity` — the D1 matrix (zh/en negatives, baseline positives, mixed scope) all classify correctly.
3. `S3 d2_atoms` — the D2 matrix yields the expected atom count/polarity with spans pointing at the original text.
4. `S4 type5` — 5 adversarial shapes produce typed findings, 0 native exceptions; 2 legal positives stay green.
5. `S5 suite` — the full suite's real exit code and its `Ran/OK/skipped` line from the raw log.
6. `S6 wheel` — installed-wheel smoke incl. a wrong-hash/orphan trace negative.
7. `S7 zip` — 8 skills, single root, single manifest, no traversal entries, CRC of every member.
8. `S8 served_assets` — downloaded release bytes recompute to `SHA256SUMS`.
9. `S9 guards` — the harness's own guards refuse a write outside the round root and a git write verb.
10. `S10 negatives` — the harness detects an injected fake (a mutated digest / a removed skill) instead of passing.

## 5. Lane mandate (order) vs OBSERVED serving (must be reported separately, never merged)

| role | mandate | registry (epoch 19 / revision 19) | observed this round |
|---|---|---|---|
| PLAN & Orchestrator | in-Hermes, `openai-codex/gpt-6.1-sol` (medium, OAuth) | PLAN primary rebound by owner order 2026-10-15 to `opencode-go/glm-5.3-flash`; `gpt-6.1-sol` retained non-default, `usable_now=QUOTA_429_2026-10-15` | see §6 of the round report |
| EXECUTE (Codex CLI writer) | `opencode-go/deepseek-v4.1-flash` | arm list: `openai-codex/gpt-6-luna` (operator-selectable), `nvidia/…` (auto) | sealed lane receipt |
| VERIFY/SECURITY (Codex CLI checker) | `openai-codex/gpt-6.1-sol` (medium) | VERIFY_SECURITY arm A = `openai-codex/gpt-6.1-sol` default | sealed lane receipt |

SoD: `EXECUTE ≠ VERIFY_SECURITY` on the default arms (distinct families). `SOD006-C2` (PLAN == VERIFY default arm,
owner-ordered 2026-10-15) stays recorded OPEN, not hidden.

## 6. Execution surfaces required by the user's order

KANBAN board + gate DAG · SWARM (root + workers + verifier + synthesizer) · GSTACK named-method route readback ·
OPENSPEC change validated with the repo's own CLI · CODEX sealed lane as tracked writer/checker.
