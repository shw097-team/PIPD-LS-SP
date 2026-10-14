# Advisory verdict from the mandated verification lane (dry audit, attempt 7)

This is the FIRST verdict this round obtained from the mandated independent checker. It is recorded
verbatim. Read the ceiling before the content.

## What this is, and what it is not

- Lane `VERIFY_SECURITY`, engine `codex-cli`, served arm **`opencode-go/glm-5.3-flash`** (rank 3,
  forced and required, `served_arm == required_arm`), sandbox `read-only`, escalation
  `sandbox_escalation_authorised: false`, duration 28.49 s.
- `ok: true`, `usage_receipt_ok: true`, `nonce_present: true` (carrier `item.completed/agent_message`).
- **Ceiling, in the dispatcher's own words**: "a pass here proves the Codex-CLI lane served this turn through the relay with a matching usage receipt; it is not an acceptance of any subject"
- Per this repository's operating rules a dispatched checker lane produces an **advisory verdict
  only** - never an OracleReceipt, never a canonical acceptance status. Nothing here closes
  `REQ-S4R3X-VERIFY-005`, and its overall verdict is `INCONCLUSIVE`, which counts as NOT verified.
- Method: a **text-only dry audit**. The checker executed nothing; the receipts were inlined in the
  prompt because earlier attempts were refused by the sandbox when the checker tried to read files.
  Same lane, same arm, same sandbox as before - no escalation flag, no substitute checker.

## The verdict, verbatim

```
C1: CONFIRMED - the supplied receipts show the red-before wheel lacked the registry, green-after clean install reports `mode=INSTALLED families=19`, and the sdist-to-wheel route is captured (`sdist_build_rc: 0`); the same log also shows negative controls that refuse a missing/mismatched registry.

C2: PARTIALLY_CONFIRMED - the CI step log shows a real committed gate running with self-tests for traversal and frozen-path refusals, which is falsifiable evidence at the CI layer. But the supplied material does not include the gate script itself or the tool's invocation path, so I cannot confirm the tool is committed and locally runnable, or confirm the negative case turns the CI red (only the green state is shown).

C3: PARTIALLY_CONFIRMED - the CI receipts show `WRITE_SET_CLEAN_AGAINST_e71fe6...` for Stage A and `WRITE_SET_CLEAN_AGAINST_5310896...` for Stage B, which is consistent with the gate now judging declared stages rather than the PR base, and the self-tests show traversal and frozen-path refusals. But the gate logic itself and the allowlists are not in the supplied material, so I cannot confirm allowlists were not widened and that the gate is now scoped to the declared base rather than the PR base.

C4: REFUTED - Stage B head is `60273fe3...` per CI receipts and `c44eaed6...` per the claim, and these do not match. The Manifest/name-version and extension-namespace refusals are not evidenced anywhere in the supplied material; no receipt covers either.

1. Strongest candidate for a relaxed oracle: the number of "19 resolvable families" is only asserted as a fixed value in output comments, with no diff shown against a strict baseline of expected families — a malicious (or accidental) reduction of bundled registry entries to a smaller accepted set would still print 19 and pass. The counter-evidence is byte-for-byte mirror tests, which substantially mitigates this but does not fully preclude it without seeing the base registry blob itself.

2. Green-signal falsifiability: the registry gate has negative controls shown in `f006_gate_tests.log` (missing registry, absent schema in registry, undeclared file on disk), which is strong. The write-set gate has self-tests showing planted traversal, frozen-path, and unlisted `src/**` paths are refused, which is also strong local falsifiability. The extension-namespace-refusals claim in C4 has no green signal shown at all. The wheels-shipped-registry claim lacks a shown negative for "wheel built without the shipped registry directory resolves at all" (only hidden in an omitted file).

3. Load-bearing but absent or summarised receipts: `MAX: 20000 chars reached` files omitted: `GATE_BLOB_DIGESTS.json`, `LOCAL_FULL_SUITE_RECEIPTS.txt`, `SELF_CAUGHT_FALSE_GREEN.md`, `SUBJECTS.json`, `WRITE_SET_GATE_LOCAL_AND_CI.txt`, `writeset_gate_local_final.txt`. Also `F006_RED_GREEN_RECEIPTS.txt` is truncated mid-JSON in the sdist-route block. The CI receipts are truncated mid-JSON too, so the full job/step list for the second head is not shown. `AO_LANE_OUTCOME.json` itself acknowledges no acceptance lane produced a verdict, so this round's instance is a text-only replacement, not a full lane substitute.

4. What these receipts cannot establish: coverage of any local Windows or macOS install route (build was Windows, CI was Ubuntu); `pip install` from PyPI, local, or private index routes; any acceptance signature beyond the self-declared receipts (no external verdict exists); the `doctor` exit code is asserted but no `doctor` log is shown, so local `doctor` exit-0 is proven only by assertion, not receipt.

Residual risks:
- The corroborating hashes in `CI_RUNS_AND_STEP_RECEIPTS.txt` point at scratch files whose digests I cannot re-derive without the underlying artifacts.
- The wheel member list and family count could be silently stale relative to the committed registry file; only a byte-for-byte mirror test guards this, and its log is present but its inputs are not.
- Missing receipts on C4's Stage B defects mean those two specific repairs are wholly unevidenced.

VERDICT: INCONCLUSIVE
HGK_LANE_NONCE_OK
```

## The executor's reading of that verdict, stated separately from it

1. **The overall verdict is INCONCLUSIVE, and that is not a pass.** C1 is the only claim the checker
   could confirm from what it was given.
2. **C4's `REFUTED` rests on a defect in MY bundle, not on a defect in the candidate.** The checker
   compared the subject it was told to judge (the current Stage B head) against a CI receipt that
   belongs to an EARLIER head, found them different, and called that a refutation. Both facts are
   true; the inference is not. I inlined receipts from several successive heads into one bundle
   without labelling which head each belonged to. Its own gap list says the same thing from the other
   side: no receipt in the bundle covers the identity-bind or extension-namespace repairs at all.
3. **The named omissions are exact and actionable** - the checker listed the files the size cap
   dropped and the two records it found truncated mid-JSON, and asked for the gate tool, the
   allowlists (to test the "allowlists were not widened" claim) and a `doctor` log (the exit code was
   asserted in the bundle but no log was shown). Those are a work item, not a mystery.
4. **Its strongest counter-argument is worth keeping**: the "19 families" figure is asserted by the
   receipts rather than diffed against a registry baseline, so a silently reduced registry could
   still print 19. It notes the byte-for-byte mirror test mitigates but does not eliminate that
   without the base blob.

## Binding

- attempt stdout (the artefact quoted above):
  `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-7-20261013T093831Z\attempt-2956-1791884311-3-stdout.txt`
  bytes=4469, sha256=42868d53031e9f3445e132bee761caeba656c57e46edbd8f69cd523ccd518a1e
- attempt stderr: `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-7-20261013T093831Z\attempt-2956-1791884311-3-stderr.txt`
  bytes=220, sha256=68d8efa5b4d34d0f338bd2593af9b03f6fb6dc99bd7cf3e93ad63330fce9473f
- Full lane receipt for the attempt: `scripts/run_ao_lane_dryaudit.py` invocation, receipt at
  `ao_lane_dryaudit/invocation_a7.json`, stdout `ao_lane_dryaudit/stdout_a7.txt`.
- The nonce contract that made attempts 2-3 fail is documented in
  `evidence/12_GATES/AO_LANE_ROOT_CAUSE_AND_ATTEMPT4.md`.
