# Independent acceptance - R10, cross-model (CODEX CLI / VERIFY_SECURITY lane)

Round R10-20261011-s4-bclass-decisions. The receipt fields below are read from the machine receipt
and relay usage row; the could_not_verify block is lifted VERBATIM from the checker report text,
not paraphrased.

## 1. Verdict

```
verdict = FAIL        (on 1 of 12 items - see section 3)
nonce   = HGK_LANE_NONCE_OK
```

## 2. Which model actually served it (receipt, not the flag we passed)

- mode = forced_rank | required_arm = openai-codex/gpt-6.1-sol
- served_arm = openai-codex/gpt-6.1-sol | used_rank = 4
- attempt: rank 4 / openai-codex / gpt-6.1-sol / exit 0 / nonce True
- relay usage: provider openai-p6a1fe3 / model gpt-6.1-sol / status 200 / effort medium
- human_home_transport_acknowledged = True | codex_home_is_declared_lane_home = False
- used_seconds = 230.69

## 3. Non-mutation of the subject tree (the freeze that failed on the first attempt)

```
mutated = False
files   = 3979 -> 3979
added/removed/changed = [] / [] / []
digest before = 4bf16601eede4566c2578383dc13bb7ba9fa29bae05e274d371abca7385e9e19
digest after  = 4bf16601eede4566c2578383dc13bb7ba9fa29bae05e274d371abca7385e9e19
```

An earlier run was aborted because this round wrote a file AFTER launching it, so the guard would
have seen a mutation. That run also refused to start at all (ERR_LANE_HOME_NOT_ISOLATED, fail-closed)
until --allow-human-home-transport was passed. Both are recorded rather than tidied away.

## 4. could_not_verify - verbatim

```json
"could_not_verify": [
    "The additional admission-script digest cannot be recomputed because its manifest-pinned target is absent.",
    "The actual separate HG-KSEOS typed admission event and governance state were not independently queried; the receipt alone does not prove them.",
    "The historical R9 selftest 5/5 result was not independently reproduced.",
    "verify_offline.py was inspected but not executed; it constructs synthetic token values, and this audit did not use credential or token values.",
    "The receipt's universal assertion that no artifact contains any secret value was not verified; no credential-value search was performed.",
    "External lifecycle-standard ownership, external source bytes and owner ratification were not independently verified.",
    "Repository records do not establish host-wide absence of MCP installations or runtime integrations.",
    "Publication --check establishes published-subject consistency, not coverage of the two reported uncovered current-worktree tools."
  ],
```

## 5. The checker claim ceiling, verbatim

> This verdict covers the observed remote tag identities, current repository artifacts and named-object search, rerun generator checks, listed installation pins and specified non-activation search only; it does not certify live integrations, historical tests, governance admission, owner ratification or complete current-worktree publication."

## 6. What this verdict does and does not cover

It FAILs on exactly one item: INSTALL_MANIFEST.json pinned a target that did not exist (a Route-B
admission-script path for a round never created, because Route A was taken). The artefact was wrong.
That defect is FIXED in HG-KSEOS commit c989b8f - the script that performed the admission is now
installed and pinned, and 7/7 pins resolve. A fresh cross-model run against the post-fix frozen
commit has NOT been recorded; the fix is applied but re-verified only locally. That is open.

The two could_not_verify items that cut against this round own claims are carried above unfiltered:
the no-secret assertion was NOT independently established, and the broader acceptance table was
only PARTIAL on the evidence checked.

## 7. Claim ceiling for this round

R10_LOCALLY_VERIFIED__CONTROL_PLANE_INSTALL_ADMITTED_AND_NON_ACTIVATED__CROSS_MODEL_RE_VERIFICATION_OWED.
Cross-model means a different model family on the SAME control plane and the SAME host. It is not
external acceptance. The maker did not sign this.

## 8. Re-verification (run 3): FAIL again, second dangling target fixed

Run 3 verdict = FAIL, on checks 10 and 12. Check 10 exposed a SECOND dangling target (control_plane_admission_file.target) - same root cause, field I had not repointed. Fixed in HG-KSEOS d642525; every path-valued target now resolves.

Receipt for run 3: served_arm == required_arm == openai-codex/gpt-6.1-sol, used_rank 4, relay openai-p6a1fe3 / 200 / effort medium, mutated=False (3990 -> 3990, identical digest).

New could_not_verify fact: a full-tree HG-KSEOS snapshot was impossible because var/far-lane-sod-003/evidence/relay-supervisor.cooldown.json.lock denied read access.

Conclusion: re-verification remains OWED. Both FAILs were real artefact defects, not harness artefacts - which is why the harness/artefact distinction from R9 had to be made explicitly here.
