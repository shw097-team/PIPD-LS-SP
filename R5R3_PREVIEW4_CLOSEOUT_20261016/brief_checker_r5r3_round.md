NONCE: R5R3-VERIFY-20261016-b7c41e9d
ROLE: independent acceptance officer (VERIFY/SECURITY). Read-only. You are checking a round's evidence, not
building anything.

You MUST NOT attempt any file write, must not create or modify any file, must not run any git write command,
must not send anything to any outside host, and must not read any report written by the round as a
substitute for measurement. If you cannot re-derive a claim from the artefacts themselves, output
`UNDERIVABLE` for that item instead of repeating the round's wording.

Print your FIRST line as the NONCE above. Your ONLY final answer must be one compact JSON object.

## Subject (frozen, read-only)
`C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout`

## What to check — re-derive each item yourself
C1. `raw/zip_repro/ZIP_REPRO_R5R3.json` claims two builds at source commit `cc6c193` produced the release's
    plugin ZIP byte-for-byte (68,357 B, sha256 `545e359a…`). Verify the FILE CLAIMS ARE INTERNALLY CONSISTENT
    and that both recorded builds carry the same length and digest. Recompute nothing you cannot: if the built
    artefacts are absent from the tree, say UNDERIVABLE and name what is missing.
C2. `raw/zip_repro_r5y/a/…zip` is a rebuild at commit `062d84ae` claimed to reproduce the previously
    host-accepted package (`2f9ae010…`, 68,355 B). Check the artefact's length and digest against that claim.
C3. `raw/control_plane_probe.json` reports the live lane routes, `check_drift` rows and SoD pairs. State which
    recorded values are internally consistent and call out any pair that contradicts.
C4. `TT_DISPOSITIONS.md` claims TT-02 landed on the canonical branch and TT-03 is not reproducible. Judge
    whether the EVIDENCE CITED supports each disposition, and name any disposition that overstates it.
C5. `OWNER_DECISION_REQUEST.md` claims three decisions are unexecuted and that gates remain NOT_GRANTED.
    Check the document for any sentence that asserts an owner act as done, or any claim ceiling that is
    missing where one is needed.
C6. Adversarial: name the single weakest claim in the packet, the cheapest way to falsify it, and whether the
    packet discloses it. If the packet contains over-reach, say so plainly.

## Output (one JSON object, these keys)
{"nonce": "...", "items": {"C1": {"verdict": "PASS|FAIL|UNDERIVABLE", "why": "..."}, ...},
 "weakest_claim": "...", "falsification_test": "...", "over_reach_found": true|false,
 "over_reach_detail": "...", "claim_ceiling": "..."}
