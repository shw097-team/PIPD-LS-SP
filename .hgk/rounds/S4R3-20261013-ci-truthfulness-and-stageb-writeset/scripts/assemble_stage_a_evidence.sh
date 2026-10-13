#!/usr/bin/env bash
# Assemble the S4R3 round's Stage A evidence pack from the raw logs that already exist locally.
# Nothing here re-runs a test: it only selects, copies and hashes what was actually produced.
set -uo pipefail
R3=".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"
EV="$R3/evidence"
GH="C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3-wt/.hgk/_r3repair/github"
STRIP='s/^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.]+Z //'
mkdir -p "$EV/01_SUBJECT" "$EV/02_LEDGER" "$EV/03_CI_TEST" "$EV/09_OWNER_RELEASE"

# --- R3 hosted-CI failure extract (the defect's own evidence, from the GitHub raw job log) --------
# The raw job log prefixes every line with an RFC3339 timestamp; it is stripped first so that
# unittest's own anchored lines ("Ran ...", "FAILED (...)") can be matched at all. The unstripped
# original stays beside it and its digest is recorded, so the strip is auditable.
{
  echo "# Extract of the raw hosted-CI job logs at the FROZEN failing subject e71fee6dd3aa73724baec4e8d9cc72127fbe36ed"
  echo "# source: .hgk/_r3repair/github/ci_job_115112781888.log (transcoded to .txt to normalise CRLF)"
  echo "# run 38341318079 job 115112781888  (GitHub API conclusion=success; the log says otherwise)"
  echo
  echo "=== unittest summary lines ==="
  sed -E "$STRIP" "$GH/ci_job_115112781888.txt" | grep -nE "^(Ran [0-9]+ tests|FAILED \(|OK \()" | head -20
  echo
  echo "=== FAIL/ERROR ids (11 in the full suite, 2 in the focused suite) ==="
  sed -E "$STRIP" "$GH/ci_job_115112781888.txt" | grep -nE "^(FAIL|ERROR): " | head -30
  echo
  echo "=== the pipeline shape that produced the false green ==="
  sed -E "$STRIP" "$GH/ci_job_115112781888.txt" | grep -nE "unittest .*tee |unittest .*tail " | head -10
} > "$EV/03_CI_TEST/r3_hosted_ci_failure_extract.txt"
sha256sum "$GH/ci_job_115112781888.log" "$GH/plugin_job_115112712475.log" > "$EV/03_CI_TEST/r3_github_raw_log_digests.txt"

{
  echo "# Extract of the public-plugin-verify job at e71fee6e (conclusion=failure)"
  echo "# run 38341318074 job 115112712475"
  echo
  sed -E "$STRIP" "$GH/plugin_job_115112712475.txt" | grep -nE "WRITE_SET_VIOLATION|UPGRADE_WROTE|skipped|Process completed with exit code" | head -25
} > "$EV/03_CI_TEST/r3_hosted_plugin_job_extract.txt"

# --- subject ---------------------------------------------------------------------------------------
cat > "$EV/01_SUBJECT/subject.json" <<'EOF'
{
  "schema_id": "PIPD-S4-R3-STAGE-A-SUBJECT/1",
  "repo": "https://github.com/shw097-team/PIPD-LS-SP",
  "change_sequence": [
    {"id": "S4R3-STAGE-A-CORE-REPAIR", "class": "NARROW_REPAIR"},
    {"id": "S4R3-STAGE-B-DISTRIBUTION", "class": "UPGRADE"}
  ],
  "frozen_base": {
    "branch": "feat/s4post-triple-upgrade-20261013-r3",
    "commit": "e71fee6dd3aa73724baec4e8d9cc72127fbe36ed",
    "tree": "2875287352529ee92277d7dc4f37cd12ffc977c7"
  },
  "remote_main_at_freeze": "224591431a164ab72a9423cd180e417e8a762403",
  "stage_a_candidate": "517d7a5d3f00935e1589908f456dfacea8fd8a74",
  "stage_a_branch": "fix/s4r3-stage-a-ci-truthfulness-20261013",
  "stage_b_candidate": "8481f29",
  "stage_b_branch": "feat/s4r3-stage-b-distribution-20261013",
  "stage_b_declared_base": "517d7a5d3f00935e1589908f456dfacea8fd8a74",
  "gate_claims": {
    "merge": "HOLD",
    "public_release": "HOLD",
    "S4_FULL_PASS": "NOT_GRANTED",
    "four_host_uat": "NOT_EXECUTED",
    "vendor_portal_validation": "NOT_EXECUTED"
  },
  "note": "stage_b_candidate is the abbreviated sha of the Stage B commit recorded in the same round as stage_a_candidate; the full 40-hex value is in 09_OWNER_RELEASE/PUSH_READBACK.txt after the push."
}
EOF

echo "extract lines: $(wc -l < "$EV/03_CI_TEST/r3_hosted_ci_failure_extract.txt") / $(wc -l < "$EV/03_CI_TEST/r3_hosted_plugin_job_extract.txt")"
cat "$EV/03_CI_TEST/r3_github_raw_log_digests.txt"
