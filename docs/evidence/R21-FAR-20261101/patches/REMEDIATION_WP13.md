# WP-FHS-13 — tool defects found by the independent AO, and the candidate patches

generated_utc: 2026-11-01T06:29:40Z
claim ceiling: **AUTHOR_SIDE_LOCAL**, candidate patches only — nothing was applied to PIPD or HG-KSEOS.

## What the AO showed (deleg_b31d237c, verdict PASS with 8 findings)

| id | sev | defect |
|---|---|---|
| F1 | high | the issuer key sits under the same Windows logon as the executor; `principal` is a free-text CLI string, so 'owner authorised it' is not evidenced |
| F2 | med | `hotswap.py` sets `neg = pos` and `neg_ok = pos.identity != expect_old`; the emitted `neg.served: true` answers a different question than its label |
| F3 | med | `bind_grant` reads only writeset **paths** and `candidate_sha256`; declared preimages are never compared with the bytes on disk |
| F4 | med | `issued_before_effect` compares `issued_at` with bind time, not with `receipt.started_at` |
| F5 | low | `assurance_level` is a string literal in `cmd_issue`, although the docstring says it is derived from the key |
| F6 | med | `occupant_from_file` stamps the caller's Need on the occupant, so name/version mismatch is unreachable through `make_consumer` |
| F7 | low | the refusal control trips `GRANT_EXPIRED` too, so it does not isolate the coverage check |
| F8 | info | single host clock; the signature half of C5 is only re-verifiable inside the 900 s TTL |

## Candidate patches

| patch | file | bytes | sha256 |
|---|---|---:|---|
| `abi.patch` | `PIPD/src/pipd_ls_sp/abi.py` | 1285 | `ea4d6023d51e7709bcb4855d8a8af9f2c7d508c22964911ba8e9de806c9684bf` |
| `hotswap.patch` | `PIPD/tools/hotswap.py` | 5290 | `4f15b109612ad7013b795130e02a35ba47f75dd569c5f96314edfa823959206a` |

Both applied only to `patches/PIPD/...` copies so hotswap's `parents[1]/src` convention still resolves.
Live repo files are byte-unchanged (`PIPD/tools/hotswap.py` sha256 still `f9468f406ac2…`).

## Tests: defect reproduced on the original, removed on the patch

| test | original behaviour | patched behaviour |
|---|---|---|
| T1 (F6) module declares NEED v2, loaded under v1 | served anyway: `{"ok": true, "value": {"ok": true, "value": "cap-attest-v2", "origin": "C:\\Projects\\Agen` | refused: `ERR_ABI_VERSION_MISMATCH` |
| T2 (F3) writeset preimage wrong | **swap succeeded**, problems `[]` | refused `['GRANT_PREIMAGE_MISMATCH_ENTRY']` |
| T3 (F4) issued_at after started_at | (predicate used bind time) | `GRANT_POSTDATES_EFFECT`, `ordering_reference=receipt.started_at` |
| T4 (F2) NEG semantics | `neg.served` copy of POS | `{"identity_after": "cap-attest-v2", "serves_old": false, "question": "does the target still serve the old capability?"}` |
| T5 (F7) valid, in-TTL, non-covering grant | — | refused for coverage only: `['GRANT_WRITESET_EXCLUDES_TARGET', 'GRANT_WRITESET_EXCLUDES_CANDIDATE']` |

Raw results: `patches/tests/RESULTS.json`; each receipt: `patches/tests/receipt_*.json`.

## What these patches do NOT fix

- **F1**: a distinct issuer needs a distinct credential holder. No patch can mint that; it needs an owner-held key under a separate logon/SID, or a HITL approval step. Recorded as a HOLD with that unblock.
- **F5**: the label is wrong about its own provenance. The honest options are to derive it from a key registry or delete it; I did neither, because changing an assurance label without the authority that issues it would be a document-level deception.
- **F8**: clock window is a property of the TTL, not a bug. A reviewer must re-verify inside the window or accept the recorded timestamps as the evidence.

## Consequence for the WP-13 claim

The independent AO passed C1–C5 **as a mechanism demonstration**. It refused the stronger readings, and after these patches three of those refusals become mechanically enforced (preimage, ordering, NEG) while two remain authority limits (F1, F5). WP-FHS-13 in `work_queue` stays **FAIL** until (i) a grant minted under a distinct credential exists and (ii) a checker other than this lane signs the verdict.
