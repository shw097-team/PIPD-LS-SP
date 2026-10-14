Bundle v2: S4R3 F1 remedy, re-offered for independent audit (lane VERIFY_SECURITY, read-only).

v2 exists because the v1 audit returned R1 REFUTED and R4/R5 INCONCLUSIVE, and all three were defects of
THIS bundle rather than of the remedy: R1's wording was ambiguous about the comparison baseline, R4 asked
you to accept a derivation that v1 did not carry, and R5's pair diff was TRUNCATED by v1 at 400 chars.
The remedy is unchanged. Nothing in v1 was argued away - the R1 wording is corrected to say what it meant,
and the two missing derivations are carried as their own blocks.

You are an independent checker. Everything you can see is below; you cannot read this machine's files or
run anything here, so a claim needing a block you were not given is INCONCLUSIVE - say which block would
settle it. The executor's prose is a CLAIM; grade the blocks. Answer per claim with exactly one of
CONFIRMED / REFUTED / INCONCLUSIVE, then one sentence citing the block text that decided it. End your
message with this token on its own line: HGK_LANE_NONCE_OK

R1  This remedy ADDS no allowlist entry to either arm: relative to the PREVIOUS head it removes two
    entries and adds none. (Its net change versus the FROZEN subject is a different, separately disclosed
    fact - see R4 and BLOCK 3 - and is not what R1 claims.)
R2  The exclusion is DECLARED and PRINTED, not silent, and cannot be reached from any product path.
R3  With the change in force the governed PRODUCT write set is clean: zero UNLISTED, zero DENIED.
R4  The surviving entry docs/USER_GUIDE.md is MEASURED as necessary: BLOCK 5 runs the classifier twice
    over the same governed diff, with the entry present and stripped, and names the path that falls out.
R5  The stacked invariant was restored, and the two gate-file copies differ in exactly one line - shown
    uninjured in BLOCK 6.
R6  The withdrawn sentence no longer appears, and its replacement discloses the one measured addition.

=== BLOCK 1: the gate's write-set step, as it now stands ===
      - name: Prove the upgrade wrote only inside its allowed set
        # Positive allowlist, not a frozen-path blacklist: a change outside the set fails even if it
        # is harmless, and dist/ is denied explicitly. Measured as AO-03 of the round's independent
        # acceptance challenge, which showed the earlier blacklist-only guard let dist/ and arbitrary
        # non-frozen paths through.
        #
        # S4R3-F002 REPAIR, second iteration. The first repair moved the scope base off the pull
        # request's base branch for the Stage B copy only, so the Stage A branch was still measured as
        # main...HEAD - the whole triple-upgrade surface - and went red on paths Stage A never wrote,
        # reporting UPGRADE_WROTE_OUTSIDE_ALLOWED_SET about a range nobody was governing. The write set
        # that this gate may judge is the write set of the STAGE THE BRANCH IS. The branch therefore
        # declares its stage, its declared base must be an ancestor of the subject, and the pull
        # request base is printed as context that is explicitly NOT the governed set.
        #
        # The two stages have deliberately different, non-overlapping write sets. Stage A repairs the
        # pipeline (the CI exit-code truthfulness guard, the packaging build, the first-run examples,
        # the smoke test) and must be able to write src/ and the workflows; Stage B ships the
        # distribution surface and must not go near src/, schemas/ or dist/. Each stage is enumerated
        # file by file or by its own narrow prefix, and the classifier's self-test below still proves
        # that planted violations are REFUSED.
        #
        # Scope of the DENIED continuity, stated precisely because the earlier wording overstated it:
        # the frozen-path denial is unchanged for the stage-b set, whose DENIED omits nothing. The
        # stage-a arm deliberately ALLOWS src/, so "the denials are unchanged" is a statement about
        # the stage-b set and must not be read as uniform across the two stages.
        #
        # Allowlist disclosure, measured rather than asserted (locator:
        # evidence/12_GATES/ALLOWLIST_MINIMUM_MEASUREMENT.json, at the revision this file carries):
        # against the frozen subject the stage-b set carries exactly ONE addition, `docs/USER_GUIDE.md`,
        # and the governed diff is measured to require it - removing it makes that path UNLISTED and
        # this gate would refuse a path Stage B legitimately ships. This file previously claimed that
        # the change widened NEITHER allowlist; that claim was false and is withdrawn here.
        #
        # The round's own evidence tree is not in either allowlist. `.hgk/**` is excluded from the
        # governed PRODUCT write set by declaration (EXCLUDED_PREFIXES below), printed and counted in
        # this step's output. The earlier arrangement instead listed the round directory inside the
        # allowlist, which had this gate permit writes to the tree holding its own receipts; an
        # exclusion a reviewer can read beats a permission a reviewer has to notice.
        env:
          # Which stage this branch IS. This single line is the ONLY difference between the Stage A
          # and Stage B copies of this file; flipping it must never be combined with a new file added
          # to the allowlist in the same commit, or the pair stops being reviewable.
          STAGE: stage-b
          # Stage A's declared base: the frozen R3 subject the external acceptance report examined.
          STAGE_A_BASE_SHA: e71fee6dd3aa73724baec4e8d9cc72127fbe36ed
          # Stage B's declared base: the Stage A tip that Stage B is stacked on. Taken by ref so it
          # does not need editing every time the Stage A tip moves; the sha it resolves to is printed
          # below and is the value an auditor should cite.
          STAGE_B_BASE_REF: fix/s4r3-stage-a-ci-truthfulness-20261013
          PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}
        run: |
          set -euo pipefail
          case "${STAGE}" in
            stage-a)
              BASE="${STAGE_A_BASE_SHA}"
              ALLOWED='^(pyproject\.toml$|setup\.py$|MANIFEST\.in$|src/pipd_ls_sp/workspace\.py$|examples/first-run/run\.(sh|ps1)$|tests/test_web_fallback\.py$|tests/test_standard_wheel_schemas\.py$|tools/cli_smoke\.py$|tools/verify_installed_wheel_registry\.py$|\.github/workflows/(ci|public-plugin-verify)\.yml$)'
              DENIED='^(skills/|schemas/|dist/)'
              REFUSED_PLANTS='skills/pipd-core/SKILL.md schemas/TraceLink.schema.json dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl src/pipd_ls_sp/cli.py tools/build_public_plugin.py'
              ALLOWED_PLANTS='src/pipd_ls_sp/workspace.py pyproject.toml setup.py tests/test_web_fallback.py tools/verify_installed_wheel_registry.py'
              ;;
            stage-b)
              # Resolved by ref, not by a literal: a literal would have to be edited every time the
              # Stage A tip moves, and editing it is exactly the step that silently stops happening.
              # The borrowed ref name makes the base follow Stage A, and the resolved sha is printed
              # below. Verified fact, not an assumption: actions/checkout fetches
              # `+refs/heads/*:refs/remotes/origin/*`, so `origin/<branch>` is present on every run
              # (the fetch command is visible in the checkout step of run 38363888153).
              # Consequence, stated plainly: if Stage A advances, this branch goes red with
              # BASE_NOT_ANCESTOR until it is re-stacked. That is the invariant, not an accident.
              BASE="$(git rev-parse --verify --quiet "refs/heads/${STAGE_B_BASE_REF}" \
                   || git rev-parse --verify --quiet "refs/remotes/origin/${STAGE_B_BASE_REF}" \
                   || true)"
              if [ -z "${BASE}" ]; then
                echo "STAGE_B_BASE_UNRESOLVED: neither refs/heads/${STAGE_B_BASE_REF} nor refs/remotes/origin/${STAGE_B_BASE_REF} is present in this checkout; refusing to guess a write-set base" >&2
                exit 1
              fi
              ALLOWED='^(packaging/public-plugin/|tools/freeze_public_plugin_source\.py$|tools/build_public_plugin\.py$|tools/build_web_fallback\.py$|tests/test_public_plugin_packaging\.py$|tests/test_web_fallback\.py$|docs/install/|docs/USER_GUIDE\.md$|docs/adr/|openspec/changes/s4post-triple-upgrade/|\.github/workflows/public-plugin-verify\.yml$|README\.md$)'
              DENIED='^(skills/|src/|schemas/|dist/)'
              REFUSED_PLANTS='skills/pipd-core/SKILL.md schemas/TraceLink.schema.json dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl src/pipd_ls_sp/validate.py'
              ALLOWED_PLANTS='docs/install/PIPD_WEB_FALLBACK.md docs/USER_GUIDE.md README.md packaging/public-plugin/plugin.json'
              ;;
            *)
              echo "STAGE_UNDECLARED: this workflow must declare STAGE as stage-a or stage-b; it will not guess which write set applies to this subject" >&2
              exit 1
              ;;
          esac
          # Declared exclusion, not a permission. `.hgk/` is the governance scaffolding tree: this
          # round's admission records, receipts, study and re-derivation tools. It is not product, and
          # it is excluded here so both allowlists enumerate product paths only. Excluded paths are
          # counted and printed below, and the self-test proves no product path can reach this prefix.
          EXCLUDED_PREFIXES='^\.hgk/'
          echo "=== governed ${STAGE} write set (${BASE}...HEAD) ==="
          if [ -n "${PR_BASE_SHA}" ] && git cat-file -e "${PR_BASE_SHA}^{commit}" 2>/dev/null; then
            echo "--- CONTEXT ONLY, not a governed write set: pull request base ${PR_BASE_SHA}...HEAD ---"
            git diff --name-only "${PR_BASE_SHA}...HEAD" || true
            echo "--- end context inventory ---"
          fi
          if ! git cat-file -e "${BASE}^{commit}" 2>/dev/null; then
            echo "BASE_UNRESOLVED: ${BASE} is not present in this checkout; refusing to guess" >&2
            exit 1
          fi
          if ! git merge-base --is-ancestor "${BASE}" HEAD; then
            echo "BASE_NOT_ANCESTOR: ${BASE} is not an ancestor of HEAD; the declared ${STAGE} base does not belong to this subject" >&2
            exit 1
          fi
          CHANGED="$(git diff --name-only "${BASE}...HEAD")"
          if [ -z "${CHANGED}" ]; then
            echo "SCOPE_EMPTY: HEAD IS the declared ${STAGE} base, so there is no ${STAGE} write set to judge."
            echo "This run says nothing about a ${STAGE} write set; only the tree-level steps below say"
            echo "anything about this subject, and they must not be cited as a ${STAGE} write-set verdict."
          else
            printf '%s\n' "${CHANGED}"
          fi
          bad=0
          excluded=0
          excluded_list=""
          while IFS= read -r path; do
            [ -n "$path" ] || continue
            # A path segment of `..` is refused before any pattern test. The allowlist is anchored
            # regexes, so `<round>/../evil.sh` would classify as inside the round's evidence directory
            # while resolving outside it. `git diff --name-only` never emits `..` for git-tracked
            # paths, so this is defence in depth rather than a live hole - asserted by the plant below
            # so it cannot silently rot.
            case "/$path/" in
              */../*)
                echo "UPGRADE_WROTE_PATH_TRAVERSAL: $path" >&2
                bad=1
                continue
                ;;
            esac
            # Exclusion is tested AFTER the traversal refusal so a `/../` path cannot hide inside the
            # excluded prefix: scaffolding paths are skipped here, never silently accepted downstream.
            if printf '%s' "$path" | grep -Eq "$EXCLUDED_PREFIXES"; then
              excluded=$((excluded + 1))
              excluded_list="${excluded_list}${path}"$'\n'
              continue
            fi
            if printf '%s' "$path" | grep -Eq "$DENIED"; then
              echo "UPGRADE_WROTE_FROZEN_PATH: $path" >&2
              bad=1
            elif ! printf '%s' "$path" | grep -Eq "$ALLOWED"; then
              echo "UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: $path" >&2
              bad=1
            fi
          done <<< "${CHANGED}"
          echo "EXCLUDED_BY_DECLARATION (${EXCLUDED_PREFIXES}) from the governed PRODUCT write set: ${excluded} path(s)"
          if [ -n "${excluded_list}" ]; then printf '%s' "${excluded_list}" | sed 's/^/  excluded: /'; fi
          # Self-test of the classifier ITSELF (the S4R3-F002 retest requirement: a repaired gate must
          # demonstrably still refuse, otherwise a gate that accepts everything and a gate that refuses
          # everything look identical from the outside).
          for planted in ${REFUSED_PLANTS}; do
            if printf '%s' "$planted" | grep -Eq "$ALLOWED" && ! printf '%s' "$planted" | grep -Eq "$DENIED"; then
              echo "GATE_SELF_TEST_FAILED: ${planted} would have been ACCEPTED" >&2
              exit 1
            fi
          done
          for planted in ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/../evil.sh" "docs/install/../../src/pipd_ls_sp/validate.py"; do
            case "/$planted/" in
              */../*) echo "GATE_SELF_TEST_OK: ${planted} is refused as a traversal path" ;;
              *) echo "GATE_SELF_TEST_FAILED: ${planted} would have been accepted" >&2; exit 1 ;;
            esac
          done
          echo "GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused"
          for planted in ${ALLOWED_PLANTS}; do
            if printf '%s' "$planted" | grep -Eq "$DENIED" || ! printf '%s' "$planted" | grep -Eq "$ALLOWED"; then
              echo "GATE_SELF_TEST_FAILED: ${planted} would have been REFUSED" >&2
              exit 1
            fi
          done
          # The declared exclusion must be unreachable from every product path; otherwise it would be
          # a blanket escape and the classifier would judge less than it prints.
          for planted in ${ALLOWED_PLANTS} ${REFUSED_PLANTS}; do
            if printf '%s' "$planted" | grep -Eq "$EXCLUDED_PREFIXES"; then
              echo "GATE_SELF_TEST_FAILED: product path ${planted} would have been EXCLUDED" >&2
              exit 1
            fi
          done
          if ! printf '%s' ".hgk/rounds/example-round/evidence/12_GATES/x.json" | grep -Eq "$EXCLUDED_PREFIXES"; then
            echo "GATE_SELF_TEST_FAILED: the declared exclusion does not match the scaffolding tree" >&2
            exit 1
          fi
          echo "GATE_SELF_TEST_OK: the declared exclusion matches scaffolding only and no product path"
          echo "GATE_SELF_TEST_OK: planted ${STAGE} artefacts are all allowed"
          if [ "$bad" -ne 0 ]; then
            echo "WRITE_SET_VIOLATION (${STAGE} base ${BASE})" >&2
            exit 1
          fi
          echo "WRITE_SET_CLEAN_AGAINST_${BASE}"
=== BLOCK 2: the gate's own run output, verdict lines (and a truncated excluded list) ===
===== stage-a in s4r3a-wt (base env: e71fee6dd3aa/fix/s4r3-stage-a-ci-truthfulness-20261013) -> exit 0 =====
EXCLUDED_BY_DECLARATION (^\.hgk/) from the governed PRODUCT write set: 23 path(s)
GATE_SELF_TEST_OK: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/../evil.sh is refused as a traversal path
GATE_SELF_TEST_OK: docs/install/../../src/pipd_ls_sp/validate.py is refused as a traversal path
GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused
GATE_SELF_TEST_OK: the declared exclusion matches scaffolding only and no product path
GATE_SELF_TEST_OK: planted stage-a artefacts are all allowed
WRITE_SET_CLEAN_AGAINST_e71fee6dd3aa73724baec4e8d9cc72127fbe36ed
===== stage-b in s4r3c-wt (base env: e71fee6dd3aa/fix/s4r3-stage-a-ci-truthfulness-20261013) -> exit 0 =====
.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_LOCAL_AND_CI.txt
.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_STEP.yml
EXCLUDED_BY_DECLARATION (^\.hgk/) from the governed PRODUCT write set: 154 path(s)
  excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_LOCAL_AND_CI.txt
  excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_STEP.yml
GATE_SELF_TEST_OK: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/../evil.sh is refused as a traversal path
GATE_SELF_TEST_OK: docs/install/../../src/pipd_ls_sp/validate.py is refused as a traversal path
GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused
GATE_SELF_TEST_OK: the declared exclusion matches scaffolding only and no product path
GATE_SELF_TEST_OK: planted stage-b artefacts are all allowed
WRITE_SET_CLEAN_AGAINST_759b9f0dc880b2f960363b2ceaa68446c770061d
2/2 gate runs clean

  (first 6 of 177 excluded paths, listed verbatim by the gate;
   TRUNCATED BY THIS BUNDLE, not by the gate - BLOCK 3 carries the counts)
  excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/admission/s4r3_admission.json
  excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/01_SUBJECT/subject.json
  excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/02_LEDGER/R2_ATOM_LEDGER.json
  excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/02_LEDGER/R3_FAILURE_ROOT_CAUSE_MAP.json
  excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/02_LEDGER/R3_FINDING_LEDGER.json
  excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/03_CI_TEST/ci_fault_injection.txt
=== BLOCK 3: the mechanical measurement, verbatim receipt json ===
{
 "head": "910823a4d5eff79fcd1d74d3e7fdbcb1d1bd8213",
 "stage": "stage-b",
 "resolved_base": "759b9f0dc880b2f960363b2ceaa68446c770061d",
 "declared_exclusion": "^\\.hgk/",
 "counts": {
  "changed": 151,
  "excluded": 143,
  "unlisted_product": 0,
  "denied_product": 0
 },
 "net_allowlist_change": {
  "frozen subject": {
   "added": [
    "docs/USER_GUIDE\\.md$"
   ],
   "removed": [
    "\\.hgk/rounds/S4POST-20261012"
   ]
  },
  "previous head 35a68f0": {
   "added": [],
   "removed": [
    "\\.hgk/rounds/S4POST-20261012",
    "\\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/"
   ]
  }
 },
 "docs_product_paths": [
  "docs/USER_GUIDE.md",
  "docs/install/PIPD_WEB_FALLBACK.md",
  "docs/install/PIPD_WEB_FALLBACK.md.sha256",
  "docs/install/README.md"
 ],
 "product_rows": [
  {
   "path": ".github/workflows/public-plugin-verify.yml",
   "verdict": "ALLOWED"
  },
  {
   "path": "README.md",
   "verdict": "ALLOWED"
  },
  {
   "path": "docs/USER_GUIDE.md",
   "verdict": "ALLOWED"
  },
  {
   "path": "docs/install/PIPD_WEB_FALLBACK.md",
   "verdict": "ALLOWED"
  },
  {
   "path": "docs/install/PIPD_WEB_FALLBACK.md.sha256",
   "verdict": "ALLOWED"
  },
  {
   "path": "docs/install/README.md",
   "verdict": "ALLOWED"
  },
  {
   "path": "tests/test_public_plugin_packaging.py",
   "verdict": "ALLOWED"
  },
  {
   "path": "tools/build_public_plugin.py",
   "verdict": "ALLOWED"
  }
 ]
}
=== BLOCK 4: provenance and binding

# F1 remedy - the PRODUCT change, as an external officer reads it

Stage A branch head: 759b9f0dc880b2f960363b2ceaa68446c770061d
Stage B branch head: 46ae548311e7f38d520d4fe98df276d15867939d
Stacked invariant: merge-base(A head, B head) = 759b9f0dc880b2f960363b2ceaa68446c770061d

## The pair invariant: the two copies must differ in ONE line

    101c101
    <           STAGE: stage-a
    ---
    >           STAGE: stage-b
=== BLOCK 5: the necessity derivation, produced by running the classifier twice ===

# Necessity derivation for docs/USER_GUIDE.md in the stage-b allowlist

This is the derivation, not a restatement of it: the same classifier is run twice over the same
governed diff, once with the entry present and once with the entry STRIPPED, and the difference is
printed. A reader can re-run the two lines below and get the same output.

governed base (resolved from STAGE_B_BASE_REF) : 759b9f0dc880b2f960363b2ceaa68446c770061d
head                                          : 46ae548311e7f38d520d4fe98df276d15867939d
declared exclusion in force                   : '^\\.hgk/'
changed paths in the governed diff            : 162

RUN 1 - entry present    : UNLISTED=0 DENIED=0
RUN 2 - entry STRIPPED   : UNLISTED=1 DENIED=0

paths whose verdict changes when the entry is removed (RUN 1 -> RUN 2):
  docs/USER_GUIDE.md   ALLOWED -> UNLISTED

CONCLUSION, mechanical: removing the entry moves exactly the path(s) listed above from ALLOWED
to UNLISTED. Since UNLISTED is what the gate refuses, the entry is load-bearing for this diff.

=== BLOCK 6: the two gate-file copies, FULL unified diff, nothing truncated ===

# The two copies of the gate file, full unified diff, nothing truncated.
Stage A copy: worktrees/s4r3a-wt/.github/workflows/public-plugin-verify.yml
Stage B copy: worktrees/s4r3c-wt/.github/workflows/public-plugin-verify.yml

diff --git "a/C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4r3a-wt\\.github\\workflows\\public-plugin-verify.yml" "b/C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4r3c-wt\\.github\\workflows\\public-plugin-verify.yml"
index 67d52d9..9197ef7 100644
--- "a/C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4r3a-wt\\.github\\workflows\\public-plugin-verify.yml"
+++ "b/C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4r3c-wt\\.github\\workflows\\public-plugin-verify.yml"
@@ -98,7 +98,7 @@ jobs:
           # Which stage this branch IS. This single line is the ONLY difference between the Stage A
           # and Stage B copies of this file; flipping it must never be combined with a new file added
           # to the allowlist in the same commit, or the pair stops being reviewable.
-          STAGE: stage-a
+          STAGE: stage-b
           # Stage A's declared base: the frozen R3 subject the external acceptance report examined.
           STAGE_A_BASE_SHA: e71fee6dd3aa73724baec4e8d9cc72127fbe36ed
           # Stage B's declared base: the Stage A tip that Stage B is stacked on. Taken by ref so it
