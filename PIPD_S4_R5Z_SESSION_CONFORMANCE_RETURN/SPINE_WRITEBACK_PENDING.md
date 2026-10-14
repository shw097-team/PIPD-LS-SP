# Spine write-back PENDING (blocked by a foreign write lock)

Intended writes (not yet applied):
- `canonical_events` `EV-R5Z-CLOSEOUT-20261014`: ROUND `R5Z-20261014-session-conformance` `VERIFYING -> CLOSEOUT_CANDIDATE`, actor `hermes-main-R5Z`.
- `evidence_refs` `EVREF-R5Z-CLOSEOUT-20261014` (`round_closeout`) -> branch `r5z-evidence-return-20261014` : `PIPD_S4_R5Z_SESSION_CONFORMANCE_RETURN/SESSION_CLOSEOUT_R5Z.md`.
- `checkpoints` `CP-R5Z-CLOSEOUT-20261014` (wave `R5Z-SESSION-CONFORMANCE`, repo_head `4289b7651174`).
- `tt_records` `R5Z-TT-004` CLOSED, `R5Z-TT-005` CLOSED, `R5Z-TT-001` OPEN (blocking=1).

Observed: `sqlite3.OperationalError: database is locked` on every attempt -- 5 attempts this session-class
(2 earlier + 3 here), each with `busy_timeout` 60-180 s, plus an explicit `BEGIN IMMEDIATE` attempt that failed
immediately. WAL/SHM files exist but their mtimes are stale, consistent with an idle/foreign writer holding the
write lock rather than active traffic. No process owned by this round was killed to force the write.

Recovery: retry the same idempotent inserts when the lock clears (each insert is guarded by an existence check, so a
retry cannot duplicate rows), or have the shared-spine owner clear the stale lock. The round's own closure does NOT
depend on this row: the authoritative artifacts are the round directory and the pushed evidence branch.
