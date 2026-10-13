#!/usr/bin/env bash
# Local reproduction of the Stage B write-set gate (S4R3-F002 raw evidence).
#
# It re-uses the SAME classifier the workflow step uses, so the owner and an external checker can
# reproduce the verdict from the candidate commit alone. Run from the Stage B worktree root:
#     bash .hgk/rounds/S4R3-.../scripts/writeset_gate_repro.sh
set -uo pipefail

STAGE_B_BASE_SHA=517d7a5d3f00935e1589908f456dfacea8fd8a74
OUT=".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/05_UPGRADE/writeset_gate_local.txt"
ALLOWED='^(packaging/public-plugin/|tools/freeze_public_plugin_source\.py$|tools/build_public_plugin\.py$|tools/build_web_fallback\.py$|tests/test_public_plugin_packaging\.py$|tests/test_web_fallback\.py$|docs/install/|docs/USER_GUIDE\.md$|docs/adr/|openspec/changes/s4post-triple-upgrade/|\.github/workflows/public-plugin-verify\.yml$|README\.md$|\.hgk/rounds/S4POST-20261012|\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/)'
DENIED='^(skills/|src/|schemas/|dist/)'

{
  echo "=== S4R3-F002 local gate reproduction ==="
  echo "subject_head $(git rev-parse HEAD)"
  echo "declared_stage_b_base ${STAGE_B_BASE_SHA}"
  echo "upstream_main 224591431a164ab72a9423cd180e417e8a762403"
  echo
  echo "--- classifier self-test: planted paths that MUST be refused ---"
  for planted in "src/pipd_ls_sp/validate.py" "schemas/TraceLink.schema.json" "skills/pipd-core/SKILL.md" "dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl" "tools/verify_evidence_digests.py"; do
    if printf '%s' "$planted" | grep -Eq "$ALLOWED" && ! printf '%s' "$planted" | grep -Eq "$DENIED"; then
      echo "  ACCEPTED (WRONG): $planted"
    else
      echo "  refused: $planted"
    fi
  done
  echo "--- classifier self-test: planted paths that MUST be allowed ---"
  for planted in "docs/install/PIPD_WEB_FALLBACK.md" "docs/USER_GUIDE.md" "README.md" "packaging/public-plugin/plugin.json"; do
    if printf '%s' "$planted" | grep -Eq "$DENIED" || ! printf '%s' "$planted" | grep -Eq "$ALLOWED"; then
      echo "  REFUSED (WRONG): $planted"
    else
      echo "  allowed: $planted"
    fi
  done
  echo
  echo "--- upstream inventory: main...HEAD (context only, NOT the Stage B write set) ---"
  git diff --name-status "224591431a164ab72a9423cd180e417e8a762403...HEAD" | head -40
  echo "  (truncated to 40 lines; full range has $(git diff --name-only 224591431a164ab72a9423cd180e417e8a762403...HEAD | wc -l) paths)"
  echo
  echo "--- governed Stage B write set: ${STAGE_B_BASE_SHA}...HEAD ---"
  CHANGED="$(git diff --name-only "${STAGE_B_BASE_SHA}...HEAD")"
  if [ -z "$CHANGED" ]; then
    echo "  STAGE_B_SCOPE_EMPTY (HEAD is the declared base)"
  else
    git diff --name-status "${STAGE_B_BASE_SHA}...HEAD"
  fi
  bad=0
  while IFS= read -r path; do
    [ -n "$path" ] || continue
    case "/$path/" in
      */../*) echo "  UPGRADE_WROTE_PATH_TRAVERSAL: $path"; bad=1; continue ;;
    esac
    if printf '%s' "$path" | grep -Eq "$DENIED"; then
      echo "  UPGRADE_WROTE_FROZEN_PATH: $path"; bad=1
    elif ! printf '%s' "$path" | grep -Eq "$ALLOWED"; then
      echo "  UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: $path"; bad=1
    fi
  done <<< "$CHANGED"
  # Classifier plants, including the traversal shape an anchored allowlist regex would otherwise
  # accept while it resolves outside the directory it appears to sit in.
  for planted in "src/pipd_ls_sp/validate.py" "schemas/TraceLink.schema.json" "skills/x/SKILL.md" "dist/old.whl" \
                 ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/../evil.sh" \
                 "docs/install/../../src/pipd_ls_sp/validate.py"; do
    case "/$planted/" in */../*) echo "  PLANT_REFUSED_TRAVERSAL: $planted"; continue ;; esac
    if printf '%s' "$planted" | grep -Eq "$ALLOWED" && ! printf '%s' "$planted" | grep -Eq "$DENIED"; then
      echo "  PLANT_WOULD_BE_ACCEPTED: $planted"; bad=1
    else
      echo "  PLANT_REFUSED: $planted"
    fi
  done
  for planted in "docs/install/PIPD_WEB_FALLBACK.md" "README.md" "docs/USER_GUIDE.md"; do
    if printf '%s' "$planted" | grep -Eq "$DENIED" || ! printf '%s' "$planted" | grep -Eq "$ALLOWED"; then
      echo "  PLANT_WOULD_BE_REFUSED: $planted"; bad=1
    else
      echo "  PLANT_ALLOWED: $planted"
    fi
  done
  if [ "$bad" -eq 0 ]; then
    echo "  WRITE_SET_CLEAN_AGAINST_${STAGE_B_BASE_SHA}"
  else
    echo "  WRITE_SET_VIOLATION"
  fi
} | tee "$OUT"
