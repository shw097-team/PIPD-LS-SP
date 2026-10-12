# Tasks — S4EXT-R1 external-challenge narrow repair

Each task follows the round's discipline: **Reproduce → Minimal Patch → Positive / Negative /
Adversarial → Full Regression → Diff Review → Checkpoint**. A task is `DONE` only when its probe
exists, ran, and is referenced by a raw log in `S4_EXTERNAL_RETURN_PACK`.

## 1. Release provenance (TT-S4EXT-001, F001/G006) — DONE (candidate)

- [x] 1.1 Freeze the identity tuple: `docs/RELEASE_TUPLE.json` separates `build_source_commit`
      (`8faa64e5…`, the `v0.1.0-preview.2` tag) from `release_tag_target` (`cbf69756…`).
- [x] 1.2 Re-generate all 8 pack documents from the tuple; a stale identity may survive **only** on a
      line that explicitly discloses it (erratum / lineage note).
- [x] 1.3 Rebuild the pack member manifest through `tools/build_mount_pack.py`, with EOL-normalised
      canonical member bytes so `MANIFEST.sha256` is stable across platforms.
- [x] 1.4 Ship the correction as a **new** `…-erratum1.zip` + `.sha256`; leave the published ZIP
      byte-identical (digest recorded in `08_RELEASE/asset_sha256.txt`).
- [x] 1.5 Write `docs/ERRATUM_2026-10-12_preview3_release_provenance.md` (additive, cites the
      published digest).
- [x] 1.6 Positive + stale-negative checks in `tests/test_s4ext_release_provenance.py`.
- [ ] 1.7 **Owner**: decide public erratum vs new preview, and publish. *HOLD — not this round.*

## 2. Trace endpoint typing + bundle graph closure (TT-S4EXT-002, F002) — DONE (candidate)

- [x] 2.1 Type `TraceLink` endpoints: non-blank ids, 64-hex hashes, family enum, `additionalProperties:false`.
- [x] 2.2 Inline the **equivalent** constraints into `PI-PKG.trace.items` (no remote `$ref`).
- [x] 2.3 Call `pipeline.trace_closure()` from `validate_bundle()`; report `FULL` / `SCHEMA_ONLY` / `FAILED`.
- [x] 2.4 Positive: the legal PI/PD/ECP/TQAEP bundle still closes `FULL`; legacy `version="1"` preserved.
- [x] 2.5 Negatives: bad type, orphan endpoint, wrong 64-hex hash, duplicate link, extra key.
- [x] 2.6 **Runtime escalation probe**: the PUBLISHED wheel returns PASS for all three tampered bundles
      (recorded in `03_CLI/trace_mutation_findings.json`) — F002 is a real runtime false PASS.
- [x] 2.7 19-family ABI regression: full suite green.

## 3. Current-release regression pin (TT-S4EXT-003, F003) — DONE (candidate)

- [x] 3.1 Keep the historical `preview.2` test untouched.
- [x] 3.2 Pin the current release from the frozen tuple, not a floating branch.
- [x] 3.3 Wrong-old-tag negative and 8/8 document identity check.
- [x] 3.4 Fresh-run on the candidate.

## 4. First-run portability (TT-S4EXT-004, O007) — DONE (candidate)

- [x] 4.1 `examples/first-run/run.sh` and `run.ps1`, self-locating, no author path, no exported `PYTHONPATH`.
- [x] 4.2 Preconditions halt with `PRECONDITION_FAIL` and exit 3 (failing-first evidence).
- [x] 4.3 Whole chain + an asserted refusal, then `FIRST_RUN_OK`.
- [x] 4.4 `README.md` "Run it" rewritten to the portable form; the `--root`-before-subcommand
      statement keeps its required wording.
- [x] 4.5 No new CLI verb, no new skill.
- [ ] 4.6 Linux/macOS fresh-user run — **NOT_RUN** (no such host in this session).

## 5. Qualification evidence (TT-S4EXT-005, G004–G006) — PARTIAL

- [x] 5.1 Full deterministic suite on the candidate (raw log in `03_CLI/`).
- [x] 5.2 Installed wheel in a clean virtualenv: `doctor` PASS in INSTALLED mode, 19 families, all 13
      command helps, the full chain, two refusals with exit 2.
- [x] 5.3 Wheel and Web-ZIP digests recomputed locally and compared with the published metadata (match).
- [x] 5.4 Compiler gate C0–C9: `lint` → `activation` → `acceptance` → `compile` = `PROMPT_COMPILE_PASS`.
- [ ] 5.5 Web GPT-6 / Hermes Agent / Codex-UI interactive UAT — **NOT_RUN**, recorded per host.
- [ ] 5.6 Independent requalification of the frozen candidate — **OPEN** (external AO).

## 6. Profile boundaries (TT-S4EXT-006, O009) — DONE (candidate)

- [x] 6.1 3/4 and 6/7 axis thresholds; provider-off + complexity stays conservative.
- [x] 6.2 list/tuple immutability; `axes=None` default unchanged.
- [x] 6.3 Non-string `requested` → typed `ProfileVeto` (was a bare `AttributeError`).
- [x] 6.4 Unknown risk is never downgraded; `risk_evidence` never mints an approval.
- [x] 6.5 No risk engine added.

## 7. S4 active SPEC/DEL adjudication (TT-S4EXT-007) — DONE (adjudication only)

- [x] 7.1 One disposition per non-`EVIDENCED` row, generated from the crosswalk (no hand drift).
- [x] 7.2 `DEL-008` (S1/S5) explicitly **not** S4-blocking; 4 `DESIGN_ONLY` rows explicitly not implemented.
- [x] 7.3 Crosswalk stays read-only; `EVIDENCED != PASS`; `closed_outright_this_round` is empty.
- [ ] 7.4 Owner acceptance of each disposition — **OPEN** (`TT-S4EXT-011` candidates).

## 8. Governance surfaces — PARTIAL

- [x] 8.1 Prompt contract compiled (`PROMPT_COMPILE_PASS`, contract sha256 recorded).
- [x] 8.2 HGK checkpoint recorded (`CK-20261008-7483330D`); admission chain state read back.
- [ ] 8.3 Round-level WorkOrder admission — **REFUSED_BY_LIFECYCLE_STATE** (`TT-S4EXT-010`, owner).
- [x] 8.4 OpenSpec change directory for this round.
- [x] 8.5 Kanban / Swarm / G-Stack receipts under `.hgk/rounds/S4EXT-R1-*/governance/`.
- [ ] 8.6 HG-KSEOS push gate for `fix/s4ext-external-challenge-20261012-r1-*` — `PUSH_HOLD` until the
      owner gate is granted.
