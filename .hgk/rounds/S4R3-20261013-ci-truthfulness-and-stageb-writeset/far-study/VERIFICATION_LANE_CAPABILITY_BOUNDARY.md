# Validation-lane capability boundary (measured, not inferred)

## The measurement

Dispatched a bounded capability probe to the checker lane: lane `VERIFY_SECURITY`, forced rank 3,
arm `opencode-go/glm-5.3-flash`, sandbox `read-only`, served in 9.10 s with a matching usage receipt
and the required nonce. The probe asked for three actions and the verbatim outcome of each.

| action attempted | observed result |
|---|---|
| `git -C <tree> rev-parse HEAD` | refused: `blocked by policy` |
| `python -c "print(1+1)"` | refused: `blocked by policy` |
| read the first 3 lines of a file in the tree | refused: `blocked by policy` |

The checker then answered its own capability question: *"None observed: `exec_command`, the only
local-file/process tool available here, was refused for all three actions."* and *"I can adjudicate
only against explicitly provided content in this conversation or generally available web results; I
cannot verify any local repository, file, or process state."*

Receipts: `verify/CAPABILITY_PROBE_A6.md`, `verify/invocation_VERIFY_SECURITY_a6.json`.

## What this means, stated without softening

1. **A verdict from this lane is an audit of the bundle it was handed, not of the tree.** Its ceiling is
   "internally consistent and covering the claim", never "true of the repository". Every one of the
   round's eight earlier verdicts (attempts 7-14) is subject to this ceiling, which is exactly why they
   clustered at PARTIALLY_CONFIRMED: they could only judge the material placed in front of them.

2. **The co-location shortfalls were therefore real defects, and the fix is bundle composition** - not
   more dispatch attempts. Attempt 10 caught the bad `doctor` log because that log was inside the
   bundle. Attempt 12 came back PARTIALLY_CONFIRMED because the accepted family-identity artifact was
   not inside the bundle. The lane behaved consistently with its capability throughout.

3. **The round's own FAR verify prompt was mis-specified by me.** It asked the checker to re-derive the
   allowlist set-diff with `git show`, compute digests, and open the spine - none of which the lane can
   do. Its INCONCLUSIVE verdict across V1-V10
   (`verify/VERDICT_VERIFY_A5.md`) is a **defect of my instruction**, not of the study and not of the
   lane. The only information attempt 5 produced is this boundary.

4. **Consequence for the study's claim ceiling:** the study's factual claims have been re-derived
   mechanically, but **by the maker, not by an independent party**. No independent party has yet
   touched the tree. The only actor that can do tree-level verification here is the external acceptance
   officer, or a lane whose sandbox the owner widens to allow local read/exec - and widening a checker's
   sandbox is precisely the escalation this lane's rules forbid.

Receipt: attempt 5's per-claim INCONCLUSIVE table and the honest refusal to round up are preserved
verbatim at `verify/VERDICT_VERIFY_A5.md`.
