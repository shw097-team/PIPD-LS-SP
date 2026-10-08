#!/usr/bin/env bash
# PIPD-LS-SP gate DAG creation + evidence receipts
set -u
HP="/c/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
SRC="$HP/hermes-agent"
export HERMES_HOME="$HP" PYTHONPATH="$SRC" PYTHONDONTWRITEBYTECODE=1
cd "$SRC" || exit 1
K=(./venv/Scripts/python.exe -B -m hermes_cli.main kanban)
REC="/c/Projects/Agent_Workspace/PIPD/.hgk/kanban"; mkdir -p "$REC"

new() { # slug title parent...
  local slug="$1"; shift; local title="$1"; shift
  local args=(--idempotency-key "$slug" --created-by "hermes-orchestrator" --json)
  for p in "$@"; do args+=(--parent "$p"); done
  "${K[@]}" create "$title" "${args[@]}" 2>&1 | tail -1
}
J() { python -c "import sys,json;print(json.load(sys.stdin).get('id',''))" 2>/dev/null; }

C0=$(new PIPD-C0-PREFLIGHT "C0 Preflight: sources, baseline, compiler bundle, HGK doctor" | J)
G1=$(new PIPD-G1-KNOWLEDGE-READY "G-KNOWLEDGE-READY: 6/6 source families, NRTV, readback" "$C0" | J)
G2=$(new PIPD-G2-PROMPT-COMPILE "G-PROMPT-COMPILE: deterministic compiler PASS" "$C0" | J)
G3=$(new PIPD-G3-HGK-ADMISSION "G-HGK-ADMISSION: requirement/taskspec/workorder admitted" "$C0" | J)
G4=$(new PIPD-G4-EXEC-SURFACES "G-EXEC-SURFACES: KANBAN/SWARM/GSTACK/OPENSPEC/CODEX evidence" "$G1" "$G2" "$G3" | J)
G5=$(new PIPD-G5-S0-CONTRACTS "G-S0: 19 typed machine contracts + validators" "$G4" | J)
G6=$(new PIPD-G6-S1-LITE-SLICE "G-S1: LITE intent->PI->PD->ECP/TQAEP vertical slice" "$G4" | J)
G7=$(new PIPD-G7-SECURITY-ROLLBACK "G-SEC: secret scan + rollback drill" "$G4" | J)
G8=$(new PIPD-G8-INDEPENDENT-VERIFY "G-INDEPENDENT-VERIFY: fresh AO lane verdict" "$G5" "$G6" "$G7" | J)
G9=$(new PIPD-G9-EVIDENCE-MD "G-EVIDENCE-MD: frozen single-file evidence MD" "$G8" | J)
G10=$(new PIPD-G10-GITHUB-PUBLISH "G-GITHUB: candidate repo publish + readback" "$G9" | J)

printf 'C0=%s\nG1=%s\nG2=%s\nG3=%s\nG4=%s\nG5=%s\nG6=%s\nG7=%s\nG8=%s\nG9=%s\nG10=%s\n' \
  "$C0" "$G1" "$G2" "$G3" "$G4" "$G5" "$G6" "$G7" "$G8" "$G9" "$G10" | tee "$REC/dag_ids.txt"

"${K[@]}" list --json 2>&1 | tail -1 > "$REC/dag_list_initial.json"
echo "--- board state ---"
"${K[@]}" list 2>&1 | tail -20
