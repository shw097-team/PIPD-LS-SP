# PLAN lane contract — FAR Gate-1 decision for round R5R3-20261016 (preview.4 closeout)

You are the PLAN & Orchestrator research step. Answer with ONE compact JSON object as your only
final answer. Do NOT write files. Do NOT contact any host. Do NOT run any git write command.

## Task class
FAR class `RESEARCH_LITERATURE_REPO` (repo-and-documents question). Route fields are fixed by the
capability matrix and are NOT yours to choose:
`decision: NATIVE_WITH_SELECTED_ARIS`, `reason_code: FAR_ROUTE_NATIVE_ARIS`.

## Subject
Published release `v0.1.1-preview.4` of `shw097-team/PIPD-LS-SP` (2026-10-14). The round must close out
that release: decide the BEST engineering action set over the residual list below, under the constraint
"low friction, high feasibility, high engineering necessity, NOT over-engineered".

## Hard facts already measured (treat as given; do not re-litigate)
1. The published plugin ZIP (68,357 B, sha256 `545e359a5ca6abc7...`) is the BYTE-EXACT, deterministic
   product of frozen commit `cc6c193` (two independent builds at that commit both reproduce it).
2. The private-host import of that ZIP was REFUSED server-side on 2026-10-14 ("cannot add plugin, try
   again"), twice, with no error code; the commit message records `the private-host import was refused
   by the host`. Status today: CAUSE_UNRESOLVED.
3. Offline member-by-member diff of that ZIP against the ZIP that a PREVIOUS round (`R5Y`) uploaded and
   installed SUCCESSFULLY: 56 members identical except 2 provenance metadata members
   (`RELEASE_RECEIPT.json`, `SOURCE_TO_PLUGIN_MAPPING.json` source commit/tree). Root `plugin.json` and all
   8 `SKILL.md` bodies are byte-identical. Therefore manifest location/fields (H1/H2) are EXCLUDED as
   causes and the account/platform side (H3) is the leading hypothesis.
4. The published assets do NOT carry later repair commits (e.g. `749dc32`); the released wheel's
   `requirements.py` predates them. Only main does.
5. Owner gates still NOT_GRANTED: NEW_RELEASE, PRIVATE_HOST_INSTALL, PUBLIC_DIRECTORY, PRODUCTION,
   S4_FULL_PASS. MERGE was granted and executed (PR #16 merged, main = `d3bd5456`).

## Residual / open list to rule on (each needs EXECUTE-NOW, OWNER-READY, or OUT-OF-SCOPE)
R1 host import of the published ZIP still unproven end-to-end.
R2 published assets lack the r5r2 repairs (`749dc32`) — does the round cut a successor release?
R3 two extra diagnostic ZIP variants prepared earlier are UNTESTED (need consented upload).
R4 TT-03: a claimed `DRIFT_VALUE` on the GSTACK/readback surface; the live re-measure of
   `config/hermes-codex-lane.json` `codex_sha256` vs the actual binary MATCHES, so the drift is either
   already repaired or lives on a different surface.
R5 TT-01 credential mechanism for push (GCM/askpass wrapper) — durable fix vs per-invocation workaround.
R6 TT-02 stage-c allowlist amendment (a product write-set gate) — landed with PR #16?
R7 The prior successful R5Y private-plugin upload procedure is documented but not generalised into a
   reusable runbook.
R8 Round-governance surfaces to be exercised and evidenced: KANBAN board, SWARM graph, GSTACK named-method
   readback, OPENSPEC change.

## Your output (ONE JSON object, these keys exactly)
```
{
  "far_route": {"task_class": "...", "decision": "...", "reason_code": "..."},
  "chosen_plan": [ {"id": "D1", "action": "...", "why": "...", "friction": "LOW|MED|HIGH",
                    "feasibility": "LOW|MED|HIGH", "necessity": "LOW|MED|HIGH",
                    "owner_gate_needed": true|false} , ... ],
  "rejected_alternatives": [ {"alt": "...", "why_rejected": "..."} ],
  "residual_rulings": { "R1": "EXECUTE-NOW|OWNER-READY|OUT-OF-SCOPE", "R2": "...", ... },
  "non_over_engineering_check": "...",
  "claim_ceiling": "..."
}
```
Keep `chosen_plan` to at most 6 items, ordered by execution sequence. Prefer actions that are LOCAL and
REVERSIBLE; never propose cutting a release, force-pushing, or an install the owner has not granted.
