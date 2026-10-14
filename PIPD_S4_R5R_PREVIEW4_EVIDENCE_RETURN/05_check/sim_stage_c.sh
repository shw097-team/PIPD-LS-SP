#!/usr/bin/env bash
# Adversarial simulation of the workflow's stage-c write-set gate against the FROZEN subject.
# Mirrors the logic in .github/workflows/public-plugin-verify.yml (lines ~150-260) exactly.
set -uo pipefail
WT="C:/Projects/Agent_Workspace/PIPD/worktrees/r5r-wt"
SUBJECT="$1"          # the frozen merge commit to judge
BASE="f4021aeff9c016cfb14f17e68a0c570ed4e825c5"

STAGE="stage-c"
# --- stage-c arm, copied verbatim from the workflow ---
ALLOWED='^(src/pipd_ls_sp/|schemas/|tests/|fixtures/|pyproject\.toml$|tools/build_dist\.py$|dist/|README\.md$|docs/install/|PREVIEW_NOTES_v0\.1\.1-preview\.4\.md$|\.github/workflows/public-plugin-verify\.yml$)'
DENIED='^(skills/|packaging/public-plugin/)'
REFUSED_PLANTS='skills/pipd-core/SKILL.md packaging/public-plugin/plugin.json src/other_package/thing.py docs/USER_GUIDE.md tools/build_public_plugin.py'
ALLOWED_PLANTS='src/pipd_ls_sp/requirements.py schemas/ClaimCeiling.schema.json tests/test_claim_ceiling_shape.py fixtures/REQ-NEG-PHRASES/source.txt dist/pipd_ls_sp-0.1.1a4-py3-none-any.whl README.md docs/install/README.md'
EXCLUDED_PREFIXES='^\.hgk/'

echo "=== governed ${STAGE} write set (${BASE}...${SUBJECT}) ==="
CHANGED="$(git -C "$WT" diff --name-only "$BASE" "$SUBJECT")"
printf '%s\n' "$CHANGED" | sed 's/^/  changed: /'
bad=0; excluded=0
while IFS= read -r path; do
  [ -n "$path" ] || continue
  case "/$path/" in */../*) echo "UPGRADE_WROTE_PATH_TRAVERSAL: $path" >&2; bad=1; continue;; esac
  if printf '%s' "$path" | grep -Eq "$EXCLUDED_PREFIXES"; then excluded=$((excluded+1)); continue; fi
  if printf '%s' "$path" | grep -Eq "$DENIED"; then echo "UPGRADE_WROTE_FROZEN_PATH: $path" >&2; bad=1
  elif ! printf '%s' "$path" | grep -Eq "$ALLOWED"; then echo "UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: $path" >&2; bad=1; fi
done <<< "$CHANGED"
echo "EXCLUDED_BY_DECLARATION: ${excluded}"
for planted in ${REFUSED_PLANTS}; do
  if printf '%s' "$planted" | grep -Eq "$ALLOWED" && ! printf '%s' "$planted" | grep -Eq "$DENIED"; then
    echo "GATE_SELF_TEST_FAILED: ${planted} would have been ACCEPTED" >&2; exit 1; fi
done
echo "GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused"
for planted in ${ALLOWED_PLANTS}; do
  if printf '%s' "$planted" | grep -Eq "$DENIED" || ! printf '%s' "$planted" | grep -Eq "$ALLOWED"; then
    echo "GATE_SELF_TEST_FAILED: ${planted} would have been REFUSED" >&2; exit 1; fi
done
echo "GATE_SELF_TEST_OK: planted stage-c artefacts are all allowed"
if [ "$bad" -ne 0 ]; then echo "WRITE_SET_VIOLATION (${STAGE} base ${BASE})" >&2; exit 1; fi
echo "WRITE_SET_CLEAN_AGAINST_${BASE}"
