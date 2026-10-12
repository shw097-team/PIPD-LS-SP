# Owner decision record: EXECUTE lane model deviation

This file is the gate's authorisation input. Each line authorises exactly one value on one axis for
one role, in the form `authorizes_<model|effort|provider>: <ROLE> <value>`. The value must be a plain
identifier (letters, digits, dot, underscore, slash, hyphen) and is matched as a fixed string, so a
deviation cannot be named by a pattern, cannot inherit another role's exception, and cannot be met by
an axis the owner never ruled on.

authorizes_model: EXECUTE opencode-go/deepseek-v4-flash
authorizes_effort: EXECUTE none

The `authorizes_effort` line is factual, not an extra permission: the Stage-B artifacts this record
accepts were produced by the backup writer lanes at reasoning effort `none`, and the independent
verifier's verdict covers that artifact set as produced.

authorizes_model: VERIFY opencode-go/glm-5.3-flash
authorizes_provider: VERIFY opencode-go

## Checker failover (owner ruling, 2026-10-12, verbatim)

> 注意，倘若checker model：GPT 6.1 SOL-MEDIUM(OPEN AI OAuth)用量耗盡，checker model就改用備援：
> 「GLM-5.3-Flash(OPENCODE GO)」

Scope of this ruling, as implemented in `stage-b/run_checker_lane.sh`:

- It is a **checker** failover only. It does not authorise a writer deviation, which is why the key is
  `authorizes_checker:` and not the bare `authorizes:` line that the EXECUTE admission path greps. A broader
  key here would have widened the writer gate as a side effect.
- It triggers **only** on an exhaustion signature in the primary lane's log (quota, rate limit, 429,
  capacity, usage limit). Any other failure - a provider content filter, a safety flag, a protocol 400, a
  control-flow defect - is reported, never worked around by switching models.
- The backup route is the catalog route with slug `opencode-go/glm-5.3-flash` (verified present in
  `C:/Users/user/.codex/desktop-model-catalog.json`, models[9]), base URL `http://127.0.0.1:10102/v1`.
- Every failover writes `stage-b/CHECKER_FAILOVER_<LANE>.md` naming both models, both stamps and both exit
  codes. A verdict produced under the backup is a verdict by a **different checker model** and must say so.
- No silent retry: one primary attempt, at most one backup attempt.

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
