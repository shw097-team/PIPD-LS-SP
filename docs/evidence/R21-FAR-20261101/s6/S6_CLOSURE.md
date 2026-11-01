# S6 — OPS ECP 逐 edge 收束

generated_utc: 2026-11-01T07:50:46Z

分母：正文宣告 **31** 條 edge，其中 **14** 條為 HOST_OP effect；契約寫的 32 在正文不存在。

| 狀態 | 條數 |
|---|---:|
| `PARK_NO_IMPLEMENTATION` | 11 |
| `EXECUTED_DEFECT_FOUND_PATCHED_CANDIDATE` | 2 |
| `PARTIAL_NO_RECEIVER_IMPLEMENTATION` | 1 |

實際跑掉的 case：**11**

## 兩個真缺陷（條文自己的 NEG 打出來的）

### EDGE-WO-B1-A2
- 缺陷：issue_grant accepts a replayed nonce (GRANT_VALID on the second grant)
- Raw：`s6/A2_CASES.json`
- 候選補丁：`s6/patch/issue_grant.nonce.patch`；測試 {'T1_first_issue_accepted': 'PASS', 'T2_replay_refused': 'PASS', 'T3_first_grant_still_valid': 'PASS'}

### EDGE-WO-B1-A3
- 缺陷：work_queue.cmd_settle overwrites a settled row (duplicate claim) and records PASS with an empty evidence_ref
- Raw：`s6/A3_CASES.json`
- 候選補丁：`s6/patch/work_queue.settle.patch`；測試 {'T1_first_settle_accepted': 'PASS', 'T2_second_settle_refused': 'PASS', 'T3_overwrite_with_fail_refused': 'PASS', 'T4_evidenceless_pass_refused': 'PASS'}

## 逐列

| edge | PD | domain | 狀態 | 解除條件 |
|---|---|---|---|---|
| `EDGE-WO-B1-A2` | PD-02 | ISSUER_SUBJECT | `EXECUTED_DEFECT_FOUND_PATCHED_CANDIDATE` | — |
| `EDGE-WO-B1-A3` | PD-03 | QUEUE_WO | `EXECUTED_DEFECT_FOUND_PATCHED_CANDIDATE` | — |
| `EDGE-WO-B1-A4` | PD-04 | RECEIVER_ABI | `PARTIAL_NO_RECEIVER_IMPLEMENTATION` | — |
| `EDGE-WO-B1-A6` | PD-06 | EFFECT_JOURNAL | `PARK_NO_IMPLEMENTATION` | a signed EFFECT_JOURNAL host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-A6-POS, TQ-B1-A6-NEG...) |
| `EDGE-WO-B1-A9` | PD-09 | NATIVE_CONTINUATION | `PARK_NO_IMPLEMENTATION` | a signed NATIVE_CONTINUATION host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-A9-POS, TQ-B1-A9-NEG...) |
| `EDGE-WO-B1-B3-OPS` | PD-13 | SBL_TO_NATIVE | `PARK_NO_IMPLEMENTATION` | a signed SBL_TO_NATIVE host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-B3-POS, TQ-B1-B3-NEG...) |
| `EDGE-WO-B1-B4-OPS` | PD-15 | ECP_SELECTOR | `PARK_NO_IMPLEMENTATION` | a signed ECP_SELECTOR host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-B4-POS, TQ-B1-B4-NEG...) |
| `EDGE-WO-B1-B5-OPS` | PD-17 | THREE_SP | `PARK_NO_IMPLEMENTATION` | a signed THREE_SP host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-B5-POS, TQ-B1-B5-NEG...) |
| `EDGE-WO-B1-C1` | PD-22 | FABRIC_PROMOTION | `PARK_NO_IMPLEMENTATION` | a signed FABRIC_PROMOTION host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-C1-POS, TQ-B1-C1-NEG...) |
| `EDGE-WO-B1-C2` | PD-23 | HGK_GWO | `PARK_NO_IMPLEMENTATION` | a signed HGK_GWO host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-C2-POS, TQ-B1-C2-NEG...) |
| `EDGE-WO-B1-C3-OPS` | PD-24 | SBL_GWO | `PARK_NO_IMPLEMENTATION` | a signed SBL_GWO host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-C3-POS, TQ-B1-C3-NEG...) |
| `EDGE-WO-B1-C4` | PD-26 | EXTERNAL_GRANT | `PARK_NO_IMPLEMENTATION` | a signed EXTERNAL_GRANT host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-C4-POS, TQ-B1-C4-NEG...) |
| `EDGE-WO-B1-C6` | PD-28 | REVOKE_RACE | `PARK_NO_IMPLEMENTATION` | a signed REVOKE_RACE host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-C6-POS, TQ-B1-C6-NEG...) |
| `EDGE-WO-B1-C8` | PD-30 | NATIVE_SUCCESSOR | `PARK_NO_IMPLEMENTATION` | a signed NATIVE_SUCCESSOR host receiver plus its edge oracle; then POS/NEG over 4 named cases (TQ-B1-C8-POS, TQ-B1-C8-NEG...) |

## 天花板

2 of 14 OPS edges were executed against their own POS/NEG and both failed a NEG, each fixed by a candidate patch on a copy; 1 is partial (no receiver implementation); 11 are parked with named unblock conditions. No OPS edge is accepted end-to-end and the canonical tools were not modified.

