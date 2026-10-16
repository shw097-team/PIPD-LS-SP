# Claim corrections — R5R3 FAR sub-round (applied from the independent checker's verdict)

Checker: CODEX-CLI lane `VERIFY_SECURITY`, arm `opencode-go/deepseek-v4.1-flash` (mandated arm; served == required),
read-only sandbox, `used_rank 1`, 186.71 s, `usage_receipt_ok: true`, nonce `R5R3-FAR-VERIFY-20261016-7d21a4c9`
echoed in its own message. Verdict of record: `FAR_R5R3_ZIPSPEC/CHECKER_VERDICT_RAW.md` (7,925 chars, extracted
byte-exact from the lane's 394,540-byte stdout); receipt `raw/verify_ds_far_receipt.json`.
Standing rule applied: a correct checker finding is **fixed, not argued**.

## CC-1 (accepted, applied) — "every member's zip metadata identical" was an over-claim

The checker reproduced that candidates E and F differ from A on the **full** zip record (`compress_size` and
`header_offset` differ on members whose content is byte-identical), because they were re-deflated at a lower
effective level (level 6 reproduces their `compress_size`; level 9 reproduces A's). Decompressed bytes are
identical. So:

- Correct reading: E and F are **single-axis on the content axis** — the enumerated fields
  (name, uncompressed size, compress_type, date_time, external_attr, create_system, ordering) match A, and only
  the named members differ in bytes — but they are **not** byte-identical to A on the whole archive record.
- Corrected in `FAR_VERDICT.md` (caveat block) and `ENGINEERING_DECISION.md` (probe-candidate sentence).
- Consequence for the probe logic: **none**. The host decompresses; every content-level difference the probes
  relied on is unchanged, and A-vs-B (both produced by the round's own packers) is clean on the full record.
- Why it matters anyway: a future round comparing archives with a naive full-record diff will see ~50 "differing"
  members when 1-2 differ in content. The oracle is content, not the record.

## CC-2 (accepted, applied) — "four probe records" was inexact

The brief text said "four probe records `probe_P1.json` … `probe_P5.json`"; five exist (P1–P5). The brief is an
artifact of record and is **not** rewritten; the inexactness is recorded here and the count in the round status
is stated as five.

## CC-3 (recorded, not a finding) — the checker's own wording slip

Its `unverified_by_me` list contains the phrase "that B/D were refused with '無法取得'". That is not the record:
**A and E were refused** (with `無法新增外掛程式。請再試一次。`); **B, D and F were accepted**. The phrase sits
inside a list about what the checker could not observe, not inside a finding, so nothing else follows from it —
recorded here so it is not later read as a checker finding against the matrix.

## CC-4 (recorded) — what the checker explicitly could not settle

In its own words, its PASS "does NOT establish any live host behaviour: not that the host accepted B, refused
A/E/D/F, or that the host-refusal attribution … is settled. It does not prove the on-disk artifacts are the exact
bytes uploaded, nor that the probe records' step narratives correspond to unedited UI captures. No oracle or
canonical acceptance is produced by this check." The round's host claims therefore remain **UI-observed** at the
claim ceiling stated in `FAR_VERDICT.md`; the independent re-derivation covers the local byte-level and
record-level relations only.

## CC-5 (noted) — the two probe plugins still on the account

P4 and P5 created `pipd-smoke-minimal` and one probe-id plugin. Removing them is an owner action (one action
each); the round does not mutate the account's install state.
