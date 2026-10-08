#!/usr/bin/env bash
# Complete the canonical-board gate cards with real CLI receipts.
SRC='/c/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent'
export HERMES_HOME='C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes'
export PYTHONPATH="$SRC" PYTHONDONTWRITEBYTECODE=1
cd "$SRC" || exit 1
P=./venv/Scripts/python.exe
K=($P -B -m hermes_cli.main kanban)
REC="/c/Projects/Agent_Workspace/PIPD/.hgk/kanban"

$P -B -m hermes_cli.main kanban list --json > "$REC/canonical_dag.json" 2>&1
python - "$REC/canonical_dag.json" > "$REC/canonical_ids.txt" <<'PY'
import json,sys
raw=open(sys.argv[1],encoding="utf-8",errors="replace").read()
raw=raw[raw.index("["):] if "[" in raw else raw
for t in json.loads(raw):
    print(f"{t['id']}\t{t.get('status','')}\t{t['title']}")
PY
cat "$REC/canonical_ids.txt"
