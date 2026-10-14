# Guard rule-text vs guard verdict (recorded, not argued)

The lane guard's own rule text reads: *"removed/changed => verdict void; added is recorded, not fatal"*.

arm3's receipt (`LANE_RECEIPT_VERIFY_arm3.json`) nonetheless returned `subject_mutation.verdict = "VOID"` with
`mutated = true` while `removed = []` and `changed = []`, the only difference being five files the maker ADDED inside
the guarded round tree during the window:

- 06_verification/ARM3_FREEZE_NOTE.md
- 06_verification/VERDICT_ARM3_PASS.json / .md
- 06_verification/VERIFY_attempt1_attempts.ndjson, VERIFY_recheck_attempts.ndjson

Two readings are possible and this pack records both rather than choosing:
1. **Strict implementation**: any difference (including additions) voids the window. The maker therefore treats arm3's
   window as VOID and re-ran bounded (arm4/arm5) with zero maker writes into the audited set.
2. **Stated rule**: additions are recorded but not fatal, in which case arm3's window would be CLEAN (additions only).

Either way the remedy is the same and has been applied: re-run with an empty actor window. This note exists so a later
reader does not have to rediscover the discrepancy; if it is an implementation bug it belongs to the lane tooling owner,
not to this round.
