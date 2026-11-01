# R21 FAR evidence — what remains, what cannot pass, who decides

Round `R21-FAR-20261101`. Everything here was produced on the author's host and is **candidate
evidence**: it is not an acceptance, not a main integration, not a release.

## Lane receipts (the three-role split, measured)

| Lane | Model | Receipt | Result |
|---|---|---|---|
| PLAN | `openai-codex/gpt-6.1-sol` (owner OAuth) | `far_receipts/PLAN_R21FAR_v2.json` | ok, rank 1, 117.6 s |
| EXECUTE | `opencode-go/deepseek-v4.1-flash` (Codex CLI, front door 10100) | `far_receipts/EXECUTE_R21FAR_C5.json` | ok, exit 0, log `far/EXECUTE_R21FAR_C5_RUN.log` |
| VERIFY | `openai-codex/gpt-6.1-sol` (owner OAuth) | `far_receipts/VERIFY_R21FAR.json` | ok, verdict **OBJECT** (absorbed in the synthesis) |

`far/sources/TOKEN_ATTRIBUTION.json` records a receipt defect measured this round: on an
OAuth-direct turn no usage ledger row exists, yet the dispatcher force-set `usage_receipt_ok=true`
from the codex rollout. Attribution is proven; billing is not. The candidate fix is in
`patches/hgk-lane-dispatch.usage-semantics/` (9/9 logic tests, canonical file untouched).

## Owner rulings (signed through the passphrase envelope)

| Ruling | Subject | Signature |
|---|---|---|
| `rulings/OWNER_RULING_R21_D4.json` | supported PASS count; 16 unsupported PASS rows reclassified | `.signature.json` |
| `rulings/OWNER_RULING_R21_D3_D5_W2.json` | OPS denominator 31 vs contract 32; TT-20 has no record; review_lock claim withdrawn | `.signature.json` |

Window `WIN-759646a93af5`, scope `permit_sign,admission_bundle_sign,registry_row_sign,merkle_root_sign`,
ceiling `REPOSITORY_WRITE`. Signatures are produced by the broker; the private key never leaves it.

## Recompute

```bash
python tools/far_build_gap_ledger.py          # 18 gap rows, each bound to a file sha
python tools/far_build_product.py             # claim/fit/rejected ledgers + run receipt
python tools/w7_evidence_audit_v2.py          # row-specific evidence rule (family manifests rejected)
PYTHONPATH=<repo>/src python tools/test_d7_semantics.py   # 9/9 on the candidate patch
```

## Headline numbers

- work queue: 22 rows, 19 PASS / 3 FAIL — **supported PASS = 3** (WP-FHS-10/11/17); 16 carry no
  row-specific artefact and were reclassified by ruling D4.
- WP-20 denominator is 192 cells (18 measured / 12 surface-exists-not-run / 48 no runner / 114 NOFIT).
- OPS ECP: 31 measured edges; the contract's 32nd is `NOT_LOCATED_IN_SOURCE`.
- S5: A8/B3 four canonical defects reproduce; candidate patch passes 6/6; C5 allowlist + narrow
  rollback PASS, checker-edited diff is `DETECTABLE_NOT_PREVENTED`.
- Three SP offices: no host-issued identity on this host (`SP_HOST_LOAD_UNPROVEN`).

## What is NOT claimed

Independent acceptance, native completeness for the three SP offices, main integration, release.
