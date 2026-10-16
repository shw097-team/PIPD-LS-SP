# PLAN lane brief — FAR research: is the ZIP spec the cause of the host refusal?

You are the PLAN & Orchestrator lane. You do NOT execute, you do NOT write files. You read the
round directory and print ONE JSON object as your final answer.

## Round directory
`C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout`

## Read these first
1. `FAR_R5R3_ZIPSPEC/RESEARCH_INPUT.json` — the verified byte-level evidence and the hypothesis set.
2. `host_smoke/HOST_UPLOAD_REJECTION_R5R3.json` — the verbatim host response and its capture context.
3. `PRIVATE_PLUGIN_UPLOAD_RUNBOOK.md` — the existing runbook and its discrimination order.
4. `ROUND_STATUS_CLOSEOUT.md` — what the round has already established.

## The owner's question (must be answered head-on)
FDA 建立 GPT 私人外掛程式時，上傳 ZIP 後 GPT 回應「無法新增外掛程式。請再試一次。」，
是否是 ZIP 的相關規格不符合 GPT 外掛程式建立的要求？

## What is already established (do not re-litigate)
- The rejected archive (A, sha256 545e359a..., 68357 B, release v0.1.1-preview.4) and the archive the
  SAME live account already accepted and installed (B, R5Y) have 56 members each, identical names and
  identical sizes. Only 2 provenance members differ in content; the entire plugin-spec surface
  (plugin.json, 8x SKILL.md, icon, schemas, derivations) is byte-identical.
- plugin.json is byte-identical => both archives declare plugin_id `pipd-ls-sp-public-skills` and
  version `0.1.1`.
- The host response is a generic retry prompt; no rule id, no field, no per-file reason.

## What we need from you (PLAN lane deliverable)
Print one JSON object with:
- `far_verdict_zh`: a direct answer to the owner's question, distinguishing
  "spec surface violation" (refuted by byte identity) from the surviving causes. Name what the
  evidence DOES and DOES NOT support, and give the honest confidence per claim.
- `discrimination_order`: an ordered probe list (each: probe id, artifact, exact UI step, what an
  ACCEPT outcome would prove, what a REJECT outcome would prove, cost, stop rule). Cheapest and most
  decisive first. At most 4 probes. No retry storms (at most one retry for the transient hypothesis).
- `decision_zh`: the best engineering decision under these constraints —
  低阻力、高可行、高工程必要性、不過度工程化、對齊本 session 目標與 PIPD-LS-SP / PIPD-PKG 封裝契約、
  可寫入驗收報告. Say explicitly which artifact (if any) must be rebuilt, which fields (if any) must
  change, and why that is the minimum sufficient change.
- `what_would_change_my_mind`: falsifiers for your own decision.
- `pkg_contract_note`: what the PIPD-PKG packaging contract should require so this class of failure is
  impossible (one rule, minimal, not a framework).
- `claim_ceiling`: what this JSON does not establish.

Answer in Traditional Chinese (Taiwan) for the prose fields; keep identifiers, paths and hashes in
English. Do not assert any probe outcome — the probes have not been run yet.
