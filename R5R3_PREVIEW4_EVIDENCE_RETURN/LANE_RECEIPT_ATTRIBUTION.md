# Lane receipt attribution

Receipt names are `<lane>_dispatch_receipt_attempt<N>.json` — no job key. Two jobs on one lane share the
numbering, so read attribution from the payload markers and the timestamped subdirectories.

| Receipt | Job | Job marker in payload | Result |
|---|---|---|---|
| `EXECUTE_dispatch_receipt_attempt1.json` | `brief_probe_execute.md` | `PROBE_DONE=R5R3-PROBE-d8e74bea7225`, `LANE_ECHO=EXECUTE` | FAILED `ERR_NO_ARM_EMITTED_NONCE` |
| `EXECUTE_dispatch_receipt_attempt2.json` | `brief_writer_ws_a.md` | writer receipt, no `PROBE_DONE` | OK, required == served |
| `VERIFY_SECURITY_dispatch_receipt_attempt1.json` | `brief_probe_verify.md` | read-only probe | FAILED `ERR_NO_ARM_EMITTED_NONCE` |
| `VERIFY_SECURITY_dispatch_receipt_attempt2.json` | `brief_checker_ws_b.md` | checker verdict | OK, `VERIFIED_WITH_FINDINGS` |

Per-attempt subdirectories are unique (`<lane>/attempt-<N>-<UTC timestamp>Z/`), so no artifact was lost: the
subdirectory names disambiguate what the flat receipt names cannot.

Only the writer and the checker dispatches are nonce-bound (`ok: true`). For the two probes, the two lanes behaved
differently and the difference is the point:

- the EXECUTE probe DID return a payload (`LANE_ECHO=EXECUTE`, `PROBE_DONE=R5R3-PROBE-d8e74bea7225`) plus the
  per-attempt row (`rank 1`, `provider opencode-go`, `model deepseek-v4.1-flash`) — but the dispatcher returned
  `ERR_NO_ARM_EMITTED_NONCE`, so it is recorded `TRANSPORT_PROBE_ONLY / NOT_BOUND`;
- the VERIFY probe returned **no payload at all**: `{"probe_stdout":"","lane_echo":"VERIFY_SECURITY"}` and its
  inner probe command reported `exit_code 1 / status failed`. A brief that has to write an output file cannot
  signal from a read-only lane, so this probe carries `NO_TRANSPORT_SIGNAL / NOT_BINDABLE` — and the lane's only
  binding evidence is the checker dispatch.

Tool defect recorded (not a product defect): the receipt name omits the job, which invited a mis-attribution
during the round and would invite one for any reader. A job key or a prompt hash in the name would fix it.
