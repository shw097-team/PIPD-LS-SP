# Owner decision record: EXECUTE lane model deviation

This file is the gate's authorisation input. Its presence allows exactly the model named on the
`authorizes:` line and nothing else; any other model is still refused.

authorizes: opencode-go/deepseek-v4-flash
authorizes_effort: none

The `authorizes_effort` line is factual, not an extra permission: the Stage-B artifacts this record
accepts were produced by the backup writer lanes at reasoning effort `none`, and the independent
verifier's verdict covers that artifact set as produced.

## What the owner ruled (verbatim, 2026-10-12)

> 用戶裁決，EXECUTE 車道是否接受 backup 模型產物作為 Stage-B candidate，必須使用
> 「Independent Acceptance Officer / VERIFY / SECURITY，轉交CODEX CLI 執行，checker model：
> GPT 6.1 SOL-MEDIUM(OPEN AI OAuth)」對backup 模型產物進行 Independent Acceptance Officer /
> VERIFY，倘若有通過，就接受，但要留下紀錄，並且使用FAR研究根因，並提出防止再度發生的
> 低阻力的最佳工程方案。

## What was actually done with it

| Step | Result | Record |
|---|---|---|
| Independent verification of the backup-model artifacts | `ACCEPT_WITH_CONDITIONS` | `verify/ao3/AO_VERDICT_STAGEB_R3.md` |
| Acceptance, scoped to the conditions, with the deviation recorded | ACCEPTED (scoped; conditions OPEN) | `ACCEPTANCE_RECORD_STAGEB.md` |
| Root cause of the deviation | Research finding; the assignment was never enforced by the harness | `verify/far/FAR_MODEL_DEVIATION_RESEARCH_RESULT.json` |
| Prevention | Admission gate in this directory | `run_lanes_gated.sh` |

## Honest limits of this authorisation

- It authorises one backup model as the source of a candidate. It does **not** assert that
  `opencode-go/deepseek-v4-flash` served those artifacts, because the logs do not authenticate the
  upstream model. The FAR study reached the same conclusion.
- It does not transfer to any future round. A new round needs a new explicit decision.
- It is not a licence to substitute silently: the gate records the pinned model in every lane
  manifest, so a deviating run is visible in the evidence rather than laundered by it.
