# VERIFY/SECURITY brief — independent re-derivation of the host-refusal attribution

Round directory: `C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout`

You are the independent checker. You MUST NOT write any file anywhere, and you MUST NOT run any git write
command, contact any outside host, or change any state. Work read-only and answer as your ONLY final message
with one compact JSON object.

You cannot re-run the live UI uploads (they already happened and are not repeatable by you). Your job is to
re-derive **every local, byte-level and record-level claim** below from the artifacts on disk, and to FLAG any
claim you cannot re-derive.

## Claims to re-derive

C1. In `host_smoke/`, `cand-A-preview4-served.zip` and `cand-B-r5y-known-good.zip` each contain **56 members**
    with identical names, identical uncompressed sizes, identical per-member zip metadata (compress_type,
    date_time, external_attr, create_system) and identical ordering; and exactly **two** members differ in
    content: `pipd-ls-sp-public-skills/RELEASE_RECEIPT.json` and
    `pipd-ls-sp-public-skills/SOURCE_TO_PLUGIN_MAPPING.json`.

C2. `pipd-ls-sp-public-skills/plugin.json` is byte-identical in A and B (its sha256 starts `9ba0eace19e9`),
    so both archives declare the same `name` (`pipd-ls-sp-public-skills`) and the same `version` (`0.1.1`).

C3. `host_smoke/cand-E-preview4-version-bumped.zip` differs from A in **only** the two members
    `plugin.json` and `RELEASE_RECEIPT.json` (54 of 56 members byte-identical), that difference is confined to
    the `version` field (0.1.1 -> 0.1.2), and every member's zip metadata is identical to A's.

C4. `host_smoke/cand-F-preview4-new-id.zip` differs from A in **only** `plugin.json` (55 of 56 members
    byte-identical), and that difference is confined to the `name` field; the provenance fields
    (`source_commit`, `source_tree`) in `RELEASE_RECEIPT.json` and `SOURCE_TO_PLUGIN_MAPPING.json` are
    preserved from A.

C5. The four probe records `FAR_R5R3_ZIPSPEC/probe_P1.json` … `probe_P5.json` are internally consistent:
    each names the artifact it actually uploaded, carries that artifact's sha256, and its `steps` show the
    UI flow it claims. Report any record whose sha256 does not match the file on disk.

C6. `FAR_R5R3_ZIPSPEC/VERDICT_P2.json` adjudicates probe P2's machine verdict from `HOST_REJECTED` to
    `HOST_ACCEPTED`; check that the raw probe file still carries the unedited machine verdict and that the
    adjudication states its evidence and its unexplained transient honestly.

C7. `FAR_R5R3_ZIPSPEC/CANDIDATE_E_MANIFEST.json` and `CANDIDATE_F_MANIFEST.json` state sha256 and byte sizes
    that match the files on disk.

## Output (single JSON, your final message)

```
{"nonce": "<the nonce you were given>",
 "claims": [{"id": "C1", "verdict": "PASS|FAIL|UNCERTAIN", "how": "<the command you ran>",
             "finding": "<what you observed>", "disagreement": "<or null>"}, ...],
 "unverified_by_me": ["<the claims, e.g. the live host outcomes, that no local re-derivation can settle>"],
 "new_findings": ["<anything you found that this round did not claim, or none>"],
 "claim_ceiling": "<what your pass does not establish>"}
```

Rules: a surface-level agreement is not a re-derivation — run the commands and report what they printed.
If a claim is true only under a narrower reading than written, say so and mark UNCERTAIN. Report the exact
numbers you measured (member counts, differing member names, hashes you computed), not counts you read from
this brief.

Your nonce is `R5R3-FAR-VERIFY-20261016-7d21a4c9`. Echo it as the `nonce` field of your final JSON and state
it once at the start of that message.

