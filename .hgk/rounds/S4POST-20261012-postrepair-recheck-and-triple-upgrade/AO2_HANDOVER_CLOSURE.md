# AO-02 closure - the clean-handover requirement

Round-2 verdict: `FAIL_CHALLENGE`, limited to one item. AO-01 and AO-03 both survived. The officer's
own wording: the *committed snapshot itself is clean*; what failed was the **delivered worktree
cleanliness promise**, and it asked that this be resolved "at handover/orchestration rather than by
changing the otherwise-passing code fixes".

## The finding, verbatim from the officer

At handover, before the officer wrote anything, `git status --porcelain` already reported four
untracked paths (the AO-02 brief, its runner, its log, and the push-credential incident note). A fifth
(Hermes host UAT) appeared later. Authorship of untracked files is not provable from porcelain, and
the officer correctly declined to attribute them to the candidate code.

## Remediation applied

1. Relocated the officer's own evidence out of the allowlist-external root `verify/` into this round's
   `verify/ao2/` - see `verify/ao2/LOCATION_NOTE.md`; 36/36 file hashes unchanged by the move.
2. Committed every remaining round artifact (AO-02 harness + raw log, the Hermes host UAT record, the
   push-credential incident note, the relocated evidence) so that the handed-over worktree is clean.
3. Verified `git status --porcelain` is empty afterwards, and recorded that readback.

## Claim ceiling after this closure

This closes a **handover-hygiene** item. It does not raise any gate:

* AO-01 and AO-03 were already independently reproduced RED (pre-fix) and GREEN (current).
* The closing commit is an **evidence/verification commit**: it must touch only `.hgk/rounds/**`.
  Any diff outside that prefix means the closure is invalid and must be reverted.
* `BUILD_PASS`, `HOST_QUALIFIED`, `PORTAL_APPROVED`, `PUBLISHED`, `PRODUCTION_VERIFIED` and
  `PIPD_S4_FULL_PASS` all remain **NOT GRANTED**.
* The subject the round-2 verdict is bound to is `0768174` / tree `6141fa9`. After the closure commit
  the HEAD moves; the officer's verdict is **not** retro-applied to the new HEAD. What is claimed is
  narrower and checkable: the code paths it verified are untouched, evidenced by a diff whose path set
  is confined to `.hgk/rounds/**`.
