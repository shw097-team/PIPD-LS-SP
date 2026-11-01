NONCE: PLAN-R21FAR-1793527600

Emit that exact nonce on the first line of your answer, then the JSON object.

# PLAN brief — R21 FAR: what remains, what cannot pass, who decides

You are the PLAN lane (read-only). Do not write files. Answer with ONE JSON object on stdout and nothing else.

## Measured state (all figures are from artefacts on this host, not from memory)

Round: R21, subject = `FHS-MSC_PIPD-LS-PKG` handoff patch v1 + the FAR/TT native E2E thin prompt.

- HGK work_queue: 19 PASS / 3 FAIL. The three FAIL are WP-FHS-12, WP-FHS-13, WP-FHS-20.
- 22-WP DAG sample: 19 PASS rows inspected, 16 carry no `evidence_ref` and no per-WP artifact dir (`NO_EVIDENCE_REOPEN`), 3 cite evidence.
- WP-FHS-12: root cause named (`pm.environments` at `hermes_bootstrap:527`), forwarder patched locally, AO verdict PARTIAL, ceiling `PATH_ENTRY_EQUIVALENCE_VERSION_AND_DISPATCH`.
- WP-FHS-13: C5 sign-before-act passes (5/5 claims), owner-envelope sidecar binds the verifier payload with 0 bytes changed in the grant; AO found F2/F3/F4/F6/F7 and candidate patches pass T1-T5.
- WP-FHS-20: 12 cells carry per-step sha; 4 claims were withdrawn after AO `deleg_0361E484` (plugin install leg, the "69 verbs" denominator, three `NO_SURFACE` kind rulings, the SIMPLE_AGENT classification).
- Kind surface re-measured with a denominator parsed from root help: 68 commands; `gateway install` is an OS service installer; `plugins list` does discriminate a user copy (bundled -> user + provenance line) and `plugins remove` restores the baseline byte-for-byte; a real `plugins install` was NOT exercised because the fixture is a bundled plugin, not a catalog entry.
- S5 DEV ECP (5 REPO_WRITE edges): A8, B3-DEV, B4-DEV executed. Four defects measured on the canonical tools: stale preimage accepted; one grant reused for a second swap; a `host_operation` grant authorising a repo write; two live ECPs for one subject. Candidate patches pass 4/4 and 2/2 on copies; canonical files untouched. B5-DEV (three host-issued SP identities) measured `SP_HOST_LOAD_UNPROVEN`: no SP binary, zero host-invocation receipts, three role skills are briefs. C5 (CODEX_MINPATCH) not started.
- S6 OPS ECP: 31 edges actually exist (OPS 14 / OBS 10 / DEV 5 / USER 2). The contract's "32 sub-contracts" is not located in the body. 2 defects found and patched as candidates, 1 partial (no receiver ABI/ACK), 11 PARK.
- TQAEP: 282 cases machine-read, each with a `case_sha256`; mapping to 12 TestClasses / 8 OracleTypes / G00-G14 not started.
- Native TPM / Commander / Challenge: no host-issued identity on this host.
- Owner envelope `WIN-91b01b7cd918`: OPEN, scope permit_sign/admission_bundle_sign/registry_row_sign, ceiling HOST_OPERATIONS, 40 ops, expires 2026-11-01T13:55:31Z.
- Not version controlled: `scripts/review_lock.py`. TT-20 has no record anywhere.

## Three questions to answer

1. GAPS: what is genuinely unfinished, residual, missing, blocked, or unclosed in this round — ordered by what it costs the deliverable, not by tidiness.
2. UNPASSABLE ITEMS: for each item that looks impossible to pass here, decide whether the impossibility is real or an artefact of over-reading, misreading, or a narrow assumption. Consider at least: an independent lane (fresh context, no candidate write), a local Docker sandbox, and the owner key envelope. Only if none applies, say the design itself needs to change, and say exactly which clause.
3. DECISIONS AND PROMOTION: which items require an owner/issuer decision (and what the smallest such decision is), which tested candidates are promotable to practical use, and which unmerged branches/candidates are fit to merge to main — with the gate that must pass first and who may sign it.

## Constraints to respect in your answer

- Candidate-only: no main move, no force push, no merge/tag/release by an agent.
- No PASS may be claimed without file + sha256 + rerunnable command + raw output, bound to the same operation.
- Independent reading only from a different principal's receipt; an author's self-test is not acceptance.
- Governance right-sizing: prefer the cheapest path that keeps the evidence binding.

## Output JSON shape

```json
{"gaps":[{"id":"","what":"","evidence":"","cost":"","state":"OPEN|PARK|HOLD|NOFIT"}],
 "unpassable":[{"id":"","claimed_reason":"","recheck":"OVER_READ|MISREAD|NARROW_ASSUMPTION|REAL","alternative":"","if_none_then_design_change":""}],
 "owner_decisions":[{"id":"","decision":"","smallest_form":"","who":"","blocking":"","envelope_op":""}],
 "promotions":[{"candidate":"","tested_by":"","gate_to_pass":"","signer":"","risk":""}],
 "merge_candidates":[{"branch_or_patch":"","tested_by":"","gate":"","recommendation":"MERGE|HOLD|REJECT"}],
 "execution_plan":[{"step":1,"action":"","lane":"PLAN|EXECUTE|VERIFY","evidence":"","stop_if":""}],
 "rulings":["..."]}
```

Answer in English. Keep every list item short. If a fact above contradicts your reading, say so in `rulings`.
