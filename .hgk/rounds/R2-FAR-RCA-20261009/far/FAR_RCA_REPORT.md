# FAR RCA Report — R2-FAR-RCA-20261009

**Research id:** FAR-PIPD-R2-SOD-RCA-20261009
**Work order:** WO-REQ-PIPD-R2-FAR-RCA-20261009 (admission REQ-/TS-/WO-REQ-PIPD-R2-FAR-RCA-20261009, FROZEN)
**Method:** governed autonomous research (FAR), read-only — route `NATIVE` / `fabric-autoresearch-native` (Fabric/fabric-autonomous-research/far_router.py)
**Aggregation lane:** EXECUTE (sealed) — writer `opencode-go/deepseek-v4.1-flash` (work_order above)
**Inputs:** `lanes/LANE_A_rca_verify.lane.json`, `lanes/LANE_B_rca_plan.lane.json`, `lanes/LANE_C_challenge.lane.json`, `lanes/LANE_D_remediation.lane.json`, `ResearchPlan.yaml`, `ResearchRequest.yaml`
**Claim ceiling:** this is a **FAR research conclusion only**. It is **not** HGK admission and **not** an independent PASS.

> Path convention: locators are reproduced verbatim from the lanes. `H/` = `C:\Projects\Agent_Workspace\HG-KSEOS`, `R/` = the live Hermes home (`%LOCALAPPDATA%\Packages\...\Local\hermes`), `Hermes/` = the Hermes agent tree, `HGK/` = the HGK mirror. Long paths are shown with the `HG-KSEOS/` prefix in the receipt sections below.

---

## 1. Decision summary

Two model-SoD deviations are confirmed, each with a distinct root cause:

- **Q1 (deviation 1):** the round ran an EXECUTE leg but **never started an independent VERIFY / Acceptance-Officer lane**, so **no 8-pack acceptance ran**. Root cause: **the checked dispatch chain has no obligatory EXECUTE-complete → independent-VERIFY handoff** — model-SoD policy is a *supply choice*, not a mandatory workflow edge.
- **Q2 (deviation 2):** the GPT-only PLANNING intent existed **only at the delegate/FAR subagent layer**; the lifecycle plan step and the admission authoring ran on the **deepseek main loop**. Root cause: **three different layers were all named "PLAN"** — a model policy, a deterministic state operation, and the real authoring worker — and only the third actually selects a model.

Both break the owner's PLAN→EXECUTE→VERIFY model-SoD and the "every governed round closes with independent acceptance" rule. A bounded adversarial challenge (LANE_C) corrected the framing of both (**C1**, **C2**), and LANE_D supplied a minimal-resistance, reversible uplift with a fail-closed self-check predicate.

---

## 2. Q1 — EXECUTE ran, but no independent VERIFY / AO lane

### 2.1 Root cause

No dispatch surface in the checked chain carries an obligatory **EXECUTE-complete → independent-VERIFY** handoff. Each surface stops one step short:

| # | Surface | What it does | What it does *not* do | Locator |
|---|---------|--------------|-----------------------|---------|
| A | Sealed Write launcher | consumes the binding, runs `codex.exe --model`, prints a write receipt, `exit 0` | start an Acceptance Officer | `H/scripts/start-hgk-hermes.ps1:328-361` (also `:15-17`, `:204-207`, `:235-260`, `:308-323`) |
| B | Lifecycle state machine | validates `EXECUTING → (VERIFYING, EVOLUTION_REVIEW)` | force passage through `VERIFYING` (it is skippable) | `H/src/hg_kseos/lifecycle.py:58` (also `:12-14`, `:49-62`, `:163-194`) |
| C | Kanban completion | recomputes readiness of **already-existing** children | spawn a missing VERIFY card | `Hermes/hermes_cli/kanban_db.py:2819-2827` (also `:2128-2187`, `:2723-2766`) |
| D | Per-round closure rule | states the obligation in a skill | auto-dispatch it (it is an orchestrator instruction) | `H/.hermes/skills/software-development/hgk-governed-execution/SKILL.md:196-207`; `H/src/hg_kseos/named_methods.py:151-192` |

Therefore **"EXECUTE ran" does not imply "VERIFY started."**

### 2.2 What *is* present (do not overclaim its absence)

Enforcement constructs exist — they are simply **not mandatorily wired** into the independent-lane dispatch on this path:

- `record_workorder_result` refuses `writer == checker` (raises `ERR_WORKORDER_SELF_REVIEW`) — `H/src/hg_kseos/spine.py:324-345`.
- `ReleaseReducer` raises `INDEPENDENT_ACCEPTANCE_MISSING` / `FAIL_CLOSED` when `independent_passed=false` or the checker is empty — `H/src/hg_kseos/release.py:44-64,624-625`.
- A runnable **pre-dispatch guard** exists: `H/scripts/hgk-lane-guard.py` (refuses a same-model dispatch, `exit 2`; adoption record at `H/evidence/review/FAR_LANE_SOD_004_ADOPTION_EVIDENCE_2026-10-07.md:40-53,86-93` notes dispatcher/delegation integration was **not applied**).

These are **result gates at call time**, and the first two **trust the caller's identity/boolean**. They are not a scheduler that starts VERIFY, and they do not prove an independent process or 8-pack execution.

### 2.3 Model-routing facts that compound the miss

- Ordinary `delegate_task` does **not** read Kanban card pins and does **not** switch model by EXECUTE/VERIFY lane; each child uses the same credentials' model/provider — `H/config/model-lane-assignment.json:106-125`; `Hermes/tools/delegate_tool.py:374-394`; `Hermes/tools/delegate_tool_config.py:416-422,482-506`.
- Only the *real* Kanban dispatch converts `card.model_override/provider_override/reasoning_effort` into worker argv `-m/--provider/--reasoning` — `Hermes/hermes_cli/kanban_db_dispatch.py:2676-2709`. With no pins, the argv carries no lane model choice.
- The terminal one-shot is the actually pinnable surface: `hermes_cli.main -m glm-5.3-flash --provider opencode-go --reasoning medium -z <prompt>` — `Hermes/hermes_cli/_parser.py:130-157`; `Hermes/hermes_cli/cli_init_mixin.py:156-180`. A tool smoke is **not** acceptance execution.

### 2.4 Contributing weakness (not proven causal)

`meta_gates.evidence_reducer` hardcodes `independent_receipt_missing = 0` with no required capsule denominator; running the real function with `capsules=[]` yields `verdict=PASS`. This is an **absence-detection blind spot**; there is **no evidence it was invoked this round**, so its direct causality is **ABSTAIN** — `H/src/hg_kseos/meta_gates.py:95-126`.

### 2.5 Cases concluded / alternatives

- **Counterexample that refutes a global claim, not Q1:** FAR-LANE-VERIFY-002 session `20261007_133742_33767d` **did** have a fresh GLM subagent with a PARTIAL verdict (`R/logs/agent.log:12915-12947`; `H/var/far-lane-verify-002/lanes/lane_v1d_challenge.json:2-12`; `H/evidence/review/FAR_LANE_VERIFY_002_EVIDENCE_2026-10-07.md:26-30`). Model separation is possible without kanban dispatch; the Q1 miss was a *deliberate-dispatch* gap.
- **Alternatives considered:** GLM provider outage (cannot explain "no dispatch at all" → ABSTAIN on transport failure); "config already auto-hands-off" (refuted — declaration, pins, promotion and spawn are different surfaces); "no enforcement at all" (refuted — conditional gates exist); "delegation budget exhausted" (ABSTAIN).

### 2.6 Reproduce commands (Q1)

```powershell
cd C:\Projects\Agent_Workspace\HG-KSEOS
# rules exist but are not mandatorily wired:
python scripts/hgk-lane-guard.py --lane VERIFY_SECURITY `
  --maker-engine codex-cli --maker-model glm-5.3-flash `
  --target-engine hermes --target-model glm-5.3-flash --target-provider opencode-go `
  --admission ADMITTED
# -> decision=REFUSE; exit 2; ERR_LANE_SOD_VIOLATION

# VERIFYING is skippable:
rg -n "EXECUTING|EVOLUTION_REVIEW" src/hg_kseos/lifecycle.py
# -> 58: "EXECUTING": ("VERIFYING", "EVOLUTION_REVIEW")

# the Write branch prints a receipt then exits 0 (no AO follow-on):
Get-Content scripts/start-hgk-hermes.ps1 | Select-Object -Skip 322 -First 40

# absence-detection blind spot:
python -B -c "from hg_kseos import meta_gates as m; print(m.evidence_reducer(capsules=[]))"
# -> {'missing_capsules': 0, 'independent_receipt_missing': 0, ..., 'verdict': 'PASS'}
```

---

## 3. Q2 — GPT-only PLANNING absent at plan step and admission authoring

### 3.1 Root cause

Three layers share the name "PLAN" and only one of them selects a model:

1. **Owner policy** — declares PLAN = `engine=hermes`, `openai-codex/gpt-6.1-sol`, OpenAI OAuth, reasoning medium (`H/config/lane-routing-registry.yaml:52-70`).
2. **Deterministic state operation** — `lifecycle.plan()` reads intent, calls `_derive_tasks(goal, source_count)` to build a fixed keyword skeleton, then sets `PLAN_READY`. **No model call** — `H/src/hg_kseos/lifecycle.py:260-292,295-329`. `admit_requirement()` and `register_requirement → FROZEN → create_taskspec → create_workorder` make **no model call** and resolve no PLAN policy — `H/src/hg_kseos/lifecycle.py:555-609`; `H/src/hg_kseos/spine.py:151-322,53-89`.
3. **Real authoring worker** — the Hermes main loop (`opencode-go/deepseek-v4.1-flash`) or a `delegate_task`, whose model is set by delegation config or Kanban card pins.

`named_methods.route('plan')` returns a **method** route (`gstack.plan-eng-review`), not an LLM provider — `H/src/hg_kseos/named_methods.py:151-192`. And `actor` is a **lease-validated string**, not a model proof — the admission FROZEN event read carries `actor=hermes-planner`, `payload_json={}`, with no model/provider/session field (`H/var/far-plan-enforcement-011/coordination/admission.json:56-70`; `H/src/hg_kseos/spine.py:191-254,296-321`). So a GPT subagent plan does **not** make a main-loop-submitted admission GPT-authored, and a gpt-named actor cannot back-fill the proof.

### 3.2 Corollary

`H/config/model-lane-assignment.json:106-125` records `effective_wiring`: the main agent is `opencode-go/deepseek-v4.1-flash`; delegation is `openai-codex/gpt-6.1-sol`; the default EXECUTE route is `CODEX_CLI_SEALED_LANE`. So the GPT intelligence is genuinely present **only** at the delegate/FAR layer in the checked wiring.

### 3.3 Reproduce commands (Q2)

```powershell
cd C:\Projects\Agent_Workspace\HG-KSEOS
rg -n "def plan|_derive_tasks|no external LLM" src/hg_kseos/lifecycle.py
# -> 260 def plan; 273 self._derive_tasks(...); 296 "...no external LLM needed for the skeleton."

python -B -c "from hg_kseos import named_methods as nm; print(nm.route('plan'))"
# -> GSTACK / gstack.plan-eng-review  (a method route, no model field)

Get-Content var/far-plan-enforcement-011/coordination/admission.json | Select-Object -Skip 55 -First 15
# -> FROZEN event actor=hermes-planner, payload_json={}  (no model/provider/session)
```

---

## 4. Challenge adjustments (LANE_C, folded — not discarded)

The adversarial lane did not overturn the two conclusions, but it **changed their wording and internal structure**.

### 4.1 C1 — "no enforcement" → "exists but not mandatorily wired"

- **Was:** enforcement is absent; the round simply skipped verification.
- **Now:** rules and a candidate guard **exist** (completion rule `H/AGENTS.md:12,106-111`; `writer!=checker` guard `H/src/hg_kseos/spine.py:332`; delivery gate; `H/scripts/hgk-lane-guard.py`), but are **not mandatorily wired into the independent-lane dispatch on this path**. Record *exists-but-not-wired*, never *absent*.
- **Confounds (recorded):** a same-round "no verdict" may follow a dispatch that hit `user_stop`/guard retries (`H/evidence/review/FAR_LANE_SOD_005_RESEARCH_EVIDENCE_2026-10-07.md:44-62`); and even if wired, this run's guard reports `registry_epoch=13` vs `live_epoch=15` and "a bare ADMITTED string is not admissible" — so wiring alone is insufficient (`H/scripts/hgk-lane-guard.py:92-109`).

### 4.2 C2 — split "PLAN" into three layers

- **Layer 1 — skeleton generation:** deterministic, **no model call** — **HIGH** confidence (`H/src/hg_kseos/lifecycle.py:259-296`).
- **Layer 2 — plan authorship:** who wrote the intent/design/admission — **LOW** confidence for *this specific* admission (target admission identity and author lineage not obtained).
- **Layer 3 — admission submission:** typed API persistence — no planner-model attestation (`H/src/hg_kseos/spine.py:296-321`).
- **Counterexample that kills the strong claim:** `deleg_b78efec7` is recorded as a **gpt-6.1-sol** PLAN lane that produced a preimage-backed adoption design with concrete candidate diffs — GPT-authored substantive planning **does** exist at the subagent layer (`H/evidence/review/FAR_LANE_SOD_004_ADOPTION_EVIDENCE_2026-10-07.md:13-17`; `H/var/far-lane-sod-004/lanes/laneP_adoption_design.json:5,34-41`). It is a *subagent* plan, so it does not imply the lifecycle skeleton or admission body was GPT-authored.

**Challenge verdict:** `PASS_CHALLENGE_ADJUSTED` — 8 conditions raised; 4 closed, 2 adjusted, 1 conceded as confound, 2 closed with residual. Full record: `LaneE_Challenge.json`.

---

## 5. Minimal-resistance remediation plan (from LANE_D)

**Selected option:** *reuse the existing runtime + a narrow fix at the sealed Write boundary + an explicit prompt-protocol*. No new scheduler, DB, reducer, executor, or second control plane.

### 5.1 Change surface

| Target | Proposal | Preserve / note |
|--------|----------|-----------------|
| `H/scripts/start-hgk-hermes.ps1:1-12,235-260` | require WorkOrder/ExecutionBinding + PLAN receipt + frozen subject manifest + VERIFY contract locator; before the Write spawn, verify admitted lineage, receipt digest, actual PLAN provider/model, medium effort, and plan↔artifact binding; **missing ⇒ refuse** | keep singleton sanctioned chain, process isolation, frontdoor health, credential guards |
| `H/scripts/start-hgk-hermes.ps1:318-361` | after Codex success: **freeze the candidate**, start a fresh-context **pinned GLM one-shot**, wait, verify the receipt; missing/timeout/identity-drift/non-PASS ⇒ **non-zero exit** | receipt must separate `execute_exit, verify_invoked, verify_exit, verify_verdict, requested_identity, observed_identity, subject_digest, session/request linkage`; launcher must **not** write an acceptance PASS. Adjacent: `$usedToken` is used at `:347` before assignment at `:354` — if in the same write-set, only fix the order |
| `H/.hermes/skills/software-development/hgk-governed-execution/SKILL.md:165-167,196-207,214-220` | change the acceptance `delegate_task VERIFY_ONLY` designation to a pinned GLM kanban worker or a scoped one-shot; keep other Swarm leaves | maker may only submit a candidate |
| `H/src/hg_kseos/spine.py:324-346,376-512` | reuse typed APIs, lease, version, idempotency, registered-evidence guards | minimum plan does not modify this file; must not present the `writer!=checker` string check as model-identity verification |
| `H/src/hg_kseos/lifecycle.py:260-329,332-388,555-609` | **do not** change the deterministic planner; prompt-protocol forces `MODEL_PLAN_AUTHORING` and `DETERMINISTIC_ADMISSION` to be listed separately (`model_invoked=false`, `status=MODEL_NOT_INVOKED`) | — |
| `H/config/model-lane-assignment.json:24-28,41-45,54-97`; `H/config/lane-routing-registry.yaml:52-139` | keep routing, `fallbacks=[]`, arm A default, arm B never auto-selected | registry stays `CANDIDATE` |

### 5.2 Verify-lane route

- **Selected:** scoped synchronous Hermes one-shot —
  `<hermes_python> -B -m hermes_cli.main -m glm-5.3-flash --provider opencode-go --reasoning medium --cli chat -q '<read frozen VERIFY contract; evidence write-set only; output verdict>'`.
- **Reason:** avoids the `delegate_task` shared `gpt-6.1-sol` route and avoids a board-wide dispatch starting other ready cards.
- **Kanban alternative:** create a VERIFY card with `model_override=glm-5.3-flash`, `provider_override=opencode-go`, `reasoning_effort=medium`, depending on the EXECUTE candidate-ready card; start via `hermes kanban dispatch`.
- **Failure policy:** no GLM evidence ⇒ `NOT_VERIFIED`; never auto-switch arm B, never inherit shared delegation, never substitute launcher `exit=0`.

### 5.3 Blast radius

**One** existing HGK launcher Write branch, one authorization contract, one skill rule. No Hermes core/delegate change, **no second DB/scheduler/reducer**, **no routing or credential change**.

### 5.4 Rollback

Before implementation, save launcher/skill/contract **preimage digests** in the WorkOrder's evidence scope. Rollback points at the implementation commit and those preimages. On rollback: **stop new Writes, preserve the unaccepted state and all receipts; never delete canonical history and never roll back to an acceptance PASS.**

### 5.5 Plan-model provability & schema limit

- A fresh pinned `openai-codex/gpt-6.1-sol` (medium) session authors or re-audits the plan; the receipt binds actual input + model output + final admitted artifact digest. If deepseek later edits the plan, the earlier receipt no longer covers the new bytes ⇒ **re-PLAN**.
- Receipt must record requested provider/model/effort, resolved transport/auth type (OAuth; no secrets), `session_id`, request/usage linkage, observed provider/model, and output digest; **unknown stays UNKNOWN** — never fill from an actor label.
- **Schema limit:** `evidence_refs` has no subject/requirement field, so `resolve_acceptance` can only prove evidence is *registered*, not natively exclude foreign evidence (`H/src/hg_kseos/spine.py:413-417`). The minimum plan binds subject via an external receipt checker; non-forgeable model origin for *all* typed callers needs separately-authorized provenance schema.

### 5.6 `sod_self_check_predicate`

Scope is the **actual maker set** per required EXECUTE candidate (not registry declarations):

```
PASS iff
  admitted_lineage_valid
  AND route_activation_authorized
  AND plan_author_receipt_valid
  AND admission.model_invoked == false
  AND execute.engine == 'codex-cli-sealed'
  AND execute.observed_identity == 'opencode-go/deepseek-v4.1-flash'
  AND exists(completed_VERIFY_after_candidate_freeze)
  AND verify.observed_identity == 'opencode-go/glm-5.3-flash'
  AND verify.requested_effort == 'medium'
  AND verify.session_id not in maker_session_ids
  AND all(check_sod(maker.observed_model, verify.observed_model).ok for maker in actual_makers)
  AND subject_digest_matches_every_receipt
  AND candidate_unchanged_during_verify
  AND verify.verdict == 'PASS'
  AND typed_acceptance_readback_matches_verdict
  AND no_required_open_denominator_edges
```

**Fail-closed:** a missing field, no invocation, unknown identity, different subject, `SUPERSEDED` candidate, or a missing independent verdict is **never PASS**; require `exists` first, then `all`, to avoid a vacuous empty-set PASS.
**Basis:** `H/src/hg_kseos/lane_policy.py:148-159,216-236`; `H/src/hg_kseos/lifecycle.py:485-552,612-643`; `H/src/hg_kseos/spine.py:324-346,421-512`.
**Observed controls (read-only):** `python -B` of `check_sod` shows `PLAN→GLM` PASS, `EXECUTE→GLM` PASS, `PLAN→PLAN` REFUSE, empty maker REFUSE.

### 5.7 Reproduce commands (remediation controls)

```powershell
cd C:\Projects\Agent_Workspace\HG-KSEOS
$env:PYTHONPATH="C:\Projects\Agent_Workspace\HG-KSEOS\src"
python -B -c "from hg_kseos import lane_policy as lp; \
  print('EXEC->GLM', lp.check_sod('deepseek-v4.1-flash','glm-5.3-flash')); \
  print('PLAN->GLM', lp.check_sod('gpt-6.1-sol','glm-5.3-flash')); \
  print('PLAN->PLAN', lp.check_sod('gpt-6.1-sol','gpt-6.1-sol')); \
  print('empty', lp.check_sod('','glm-5.3-flash'))"
# EXEC->GLM (True, 'SOD_OK ...'); PLAN->GLM (True, ...); PLAN->PLAN (False, SOD_VIOLATION); empty (False, SOD_UNDETERMINED)
```

---

## 6. Uncertainty, abstentions, and non-claims

**Residual uncertainty**

- The round's two MAKERs, the GLM smoke, the missing VERIFY dispatch and the missing 8-pack execution are taken as given from delegation context; the round transcript was not re-attested.
- No DB was read or modified: this round's `project_id`, acceptance rows, Kanban dependencies and reducer receipts were not confirmed.
- Not all gateways, cron, profile hooks or dynamic plugin routes were audited; "no auto handoff" is limited to checked source surfaces.
- `H/config/verify-lane-contract.json:117-120` `actual_hgk_consumer=null` applies only to FAR-LANE-SOD-007.
- Whether the release/SoD reducers were actually invoked this round: **ABSTAIN**. Whether `evidence_reducer` was invoked: **ABSTAIN**.
- Whether GLM transport would have failed on a full acceptance run: **ABSTAIN**.
- The raw main-agent transcript for the admission turn was not obtained; whether each GPT subagent really ran at `effort=medium` was not proven.

**Explicit non-claims**

- **Not HGK admission** — no requirement, task, WorkOrder or artifact is admitted by this report.
- **Not an independent PASS** — this is the FAR aggregation writer's conclusion, not an independent VERIFY verdict nor an AO result; the maker/writer cannot self-accept.
- **Not a mutation authorization** — no canonical apply, no commit, no push, no policy/credential/profile change, no production/release. Writes were confined to `PIPD/.hgk/rounds/R2-FAR-RCA-20261009/far/`.
- No proof of backend model weights, mutual provider independence, or actual reasoning depth.
- GUARD/ORACLE note: any ordering decision must use the implicit `rowid`, never wall-clock `created_at` (guarded by `tests/test_ordering_oracle.py`).

**Artifact set (this round):** `IntegratedFindings.yaml`, `LaneD_RootCause.json`, `LaneE_Challenge.json`, `ProposedEvolution.yaml`, `Gate1_Receipt.json`, `ResearchHandoff.yaml`, `FAR_RCA_REPORT.md`.
