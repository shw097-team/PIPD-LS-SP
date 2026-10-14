# Checker arm-binding ledger (VERIFY_SECURITY lane, round R5Z)

The lane's *self-reported* model is never binding. The dispatcher receipt is.

| dispatch | required arm | served arm | rank | exit | nonce | receipt verdict | consequence |
|---|---|---|---|---|---|---|---|
| attempt 1 (full audit) | opencode-go/glm-5.3-flash | **opencode-go/deepseek-v4.1-flash** | 1 | TIMEOUT 1800.04 s | false | none written (runner hit its own 2100 s cap, exit 1) | measurements valid; **not** a GLM-5.3-Flash verdict |
| recheck attempt 2 | opencode-go/glm-5.3-flash | **opencode-go/deepseek-v4.1-flash** | 1 | 0 | true | `ok=false / ERR_REQUIRED_ARM_NOT_SERVED` | verdict PASS but **not arm-compliant** |
| arm3 | opencode-go/glm-5.3-flash | **opencode-go/glm-5.3-flash** | 3 | 0 | true | `ok=false / ERR_CHECKER_MUTATED_SUBJECT` (subject_mutation VOID) | arm binding **proven**; window voided because the maker copied verdicts into the audited round tree mid-run |
| arm4 | opencode-go/glm-5.3-flash | pending | 3 | – | – | pending | bounded re-run with zero maker writes into the audited set |

Root cause of the arm mismatch: `config/lane-route-slots.candidate.json` orders `opencode-go/deepseek-v4.1-flash` rank 1 for
both lanes, so an unforced dispatch serves it and the receipt then flags the required-arm mismatch. Remediation applied:
`--force-rank 3 --require-arm opencode-go/glm-5.3-flash`.

Discipline when a guard trips: freeze, disclose, re-run bounded -- never widen the guard, never re-label a voided window
as a pass. arm3's measurements are kept; its window verdict is VOID.
