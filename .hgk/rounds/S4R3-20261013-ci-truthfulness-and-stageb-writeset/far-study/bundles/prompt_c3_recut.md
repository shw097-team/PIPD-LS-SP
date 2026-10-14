ROLE: you are the independent checker for a governed round. Because your sandbox refuses local
file reads and process execution (measured: `git`, `python` and a plain file read all returned
`blocked by policy` on this lane), EVERYTHING needed to judge is reproduced inline below. Judge only
what is inline. If a block needed for a sub-claim is absent, answer INCONCLUSIVE for that sub-claim and
name the missing block - do not infer it from the claim's wording, and do not round a failure up.
A verdict is CONFIRMED only if the inline blocks themselves settle it. End with the token on its own
line.

CLAIM C3 (CORRECTED WORDING - an earlier wording asserted the allowlist was NOT widened and was
falsified by this round's own diff): "The write-set gate judges the branch's DECLARED stage and base
rather than the pull-request base; the frozen-path refusals still refuse. MEASURED DEVIATION: the
stage-b allowlist gained exactly two entries relative to the frozen subject - docs/USER_GUIDE.md and
the round's own directory - against an admitted requirement whose wording forbids widening."

Adjudicate:
  C3a  does BLOCK 1's set-diff support "exactly two added entries", and name them
  C3b  does BLOCK 1 support "the DENIED set is unchanged", so the frozen-path refusal still refuses
  C3c  is any part of the corrected wording UNSUPPORTED or overstated by the blocks
  C3d  does BLOCK 2 show the gate comparing a DECLARED stage/base rather than the pull-request base
  C3e  do the refusal receipts in BLOCK 3 come from the same revision the diff compares

=== BLOCK 1: C3_ALLOWLIST_BASELINE_DIFF.txt (full) ===
# Baseline diff of the write-set gate's ALLOWED/DENIED sets (frozen R3 subject vs current heads)

How this was produced, mechanically and repeatably, with no manual editing:

    git -C <stage A worktree> show e71fee6dd3aa73724baec4e8d9cc72127fbe36ed:.github/workflows/public-plugin-verify.yml   # frozen base
    git -C <stage A worktree> show HEAD:.github/workflows/public-plugin-verify.yml        # current Stage A head
    git -C <stage B worktree> show ba27309b50d8623ed9d3ad9b33fe7a4ffb8a9ede:.github/workflows/public-plugin-verify.yml     # current Stage B head
    # every ALLOWED='...' / DENIED='...' assignment parsed, entries split on '|', then set-diffed

A FIRST ATTEMPT AT THIS ARTEFACT WAS WRONG AND WAS DISCARDED. Its extractor terminated on the wrong
token and captured 224 lines from the base against 348 from the head, which is not an allowlist; a
"diff" built from it would have been meaningless. The extraction above parses the assignments
themselves, so the counts below are entry counts, not line counts.

## What the frozen base carried

ONE allowlist and ONE denial set (the single-stage era, before the STAGE switch existed):

  ALLOWED (12 entries): ['README\\.md$', '\\.github/workflows/public-plugin-verify\\.yml$', '\\.hgk/rounds/S4POST-20261012', 'docs/adr/', 'docs/install/', 'openspec/changes/s4post-triple-upgrade/', 'packaging/public-plugin/', 'tests/test_public_plugin_packaging\\.py$', 'tests/test_web_fallback\\.py$', 'tools/build_public_plugin\\.py$', 'tools/build_web_fallback\\.py$', 'tools/freeze_public_plugin_source\\.py$']
  DENIED           : ['dist/', 'schemas/', 'skills/', 'src/']

Note `src/` is in the frozen base's DENIED set.

## What the current Stage A head carries

TWO allowlists and TWO denial sets, selected by `STAGE` (the current Stage A head declares
`STAGE: stage-a`; the Stage B head declares `STAGE: stage-b`).

  stage-a ALLOWED (13 entries): ['MANIFEST\\.in$', '\\.github/workflows/ci', '\\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/', 'examples/first-run/run\\.sh', 'ps1$', 'public-plugin-verify\\.yml$', 'pyproject\\.toml$', 'setup\\.py$', 'src/pipd_ls_sp/workspace\\.py$', 'tests/test_standard_wheel_schemas\\.py$', 'tests/test_web_fallback\\.py$', 'tools/cli_smoke\\.py$', 'tools/verify_installed_wheel_registry\\.py$']
  stage-a DENIED           : ['dist/', 'schemas/', 'skills/']

  stage-b ALLOWED (14 entries): ['README\\.md$', '\\.github/workflows/public-plugin-verify\\.yml$', '\\.hgk/rounds/S4POST-20261012', '\\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/', 'docs/USER_GUIDE\\.md$', 'docs/adr/', 'docs/install/', 'openspec/changes/s4post-triple-upgrade/', 'packaging/public-plugin/', 'tests/test_public_plugin_packaging\\.py$', 'tests/test_web_fallback\\.py$', 'tools/build_public_plugin\\.py$', 'tools/build_web_fallback\\.py$', 'tools/freeze_public_plugin_source\\.py$']
  stage-b DENIED           : ['dist/', 'schemas/', 'skills/', 'src/']

## The deltas, stated exactly

stage-b vs the frozen base:
  + 2 added: ['\\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/', 'docs/USER_GUIDE\\.md$']
  - 0 removed: []

stage-a vs the frozen base (a stage that did not exist in the frozen era, so every entry is new):
  entries not present in the base allowlist: 12
  base entries not present here            : 11

## What this means, without rounding

1. **The claim "the allowlists were NOT widened" is FALSE as written.** The stage-b allowlist gained
   exactly two entries against the frozen base. This contradicts the inline comment in the workflow
   itself ("This change widens NEITHER allowlist") and it contradicts the C3 claim this round put to
   the verification lane in attempts 7-13.
2. **The stage-b frozen-path denial is UNCHANGED**: skills/, src/, schemas/, dist/ all remain denied,
   and it is the denial - not the allowlist - that carries the frozen-path guarantee for stage-b.
3. **stage-a is a new stage whose DENIED set omits `src/`.** For that stage, `src/` files outside the
   single allowed path are still refused, but by the ALLOWLIST rather than by a category denial. That
   is a real change in mechanism for that stage, and it is exactly what repairing the pipeline
   required - it is not presented here as unremarkable.
4. **The more consequential of the two additions is the round directory itself**:
   `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` is inside the governed write set
   of the stage-b gate. The gate therefore permits writes to the directory that holds this round's
   own receipts. Its likely reason is ordinary (the round commits evidence and the gate would
   otherwise fail on it), but its effect is self-referential and it is recorded as such rather than
   justified away.
5. `docs/USER_GUIDE.md` is a doc addition consistent with stage B's distribution surface
   (`docs/install/` and `docs/adr/` were already allowed); it is still a widening.

## Ceiling

This is a mechanical set-diff of two committed revisions. It says what changed in the governed write
set; it does not say whether each change was necessary, and it is not an acceptance.


=== BLOCK 2: WRITE_SET_GATE_STEP.yml (the workflow step, verbatim) ===
# The write-set gate step, extracted VERBATIM from the Stage A head's workflow.
# Source: .github/workflows/public-plugin-verify.yml lines 59-201
# It is a workflow step, not a standalone script; that is why the refusal receipts below
# (local gate run + the CI self-test line) are supplied alongside it.

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
        # distribution surface and must not go near src/, schemas/ or dist/. This change widens
        # NEITHER allowlist: each stage is enumerated file by file or by its own narrow prefix, the
        # frozen-path denial for skills/, schemas/ and dist/ applies to both, and the classifier's
        # self-test below still proves that planted violations are REFUSED.
        env:
          # Which stage this branch IS. This single line is the ONLY difference between the Stage A
          # and Stage B copies of this file; flipping it must never be combined with a new file added
          # to the allowlist in the same commit, or the pair stops being reviewable.
          STAGE: stage-a
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
              ALLOWED='^(pyproject\.toml$|setup\.py$|MANIFEST\.in$|src/pipd_ls_sp/workspace\.py$|examples/first-run/run\.(sh|ps1)$|tests/test_web_fallback\.py$|tests/test_standard_wheel_schemas\.py$|tools/cli_smoke\.py$|tools/verify_installed_wheel_registry\.py$|\.github/workflows/(ci|public-plugin-verify)\.yml$|\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/)'
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
              ALLOWED='^(packaging/public-plugin/|tools/freeze_public_plugin_source\.py$|tools/build_public_plugin\.py$|tools/build_web_fallback\.py$|tests/test_public_plugin_packaging\.py$|tests/test_web_fallback\.py$|docs/install/|docs/USER_GUIDE\.md$|docs/adr/|openspec/changes/s4post-triple-upgrade/|\.github/workflows/public-plugin-verify\.yml$|README\.md$|\.hgk/rounds/S4POST-20261012|\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/)'
              DENIED='^(skills/|src/|schemas/|dist/)'
              REFUSED_PLANTS='skills/pipd-core/SKILL.md schemas/TraceLink.schema.json dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl src/pipd_ls_sp/validate.py'
              ALLOWED_PLANTS='docs/install/PIPD_WEB_FALLBACK.md docs/USER_GUIDE.md README.md packaging/public-plugin/plugin.json'
              ;;
            *)
              echo "STAGE_UNDECLARED: this workflow must declare STAGE as stage-a or stage-b; it will not guess which write set applies to this subject" >&2
              exit 1
              ;;
          esac
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
            if printf '%s' "$path" | grep -Eq "$DENIED"; then
              echo "UPGRADE_WROTE_FROZEN_PATH: $path" >&2
              bad=1
            elif ! printf '%s' "$path" | grep -Eq "$ALLOWED"; then
              echo "UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: $path" >&2
              bad=1
            fi
          done <<< "${CHANGED}"
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
          echo "GATE_SELF_TEST_OK: planted ${STAGE} artefacts are all allowed"
          if [ "$bad" -ne 0 ]; then
            echo "WRITE_SET_VIOLATION (${STAGE} base ${BASE})" >&2
            exit 1
          fi
          echo "WRITE_SET_CLEAN_AGAINST_${BASE}"



=== BLOCK 3: C3_REFUSAL_RECEIPT_DISTILLED.txt ===
write-set gate refusals and allowances, from the recorded local and CI runs
(distilled from WRITE_SET_GATE_LOCAL_AND_CI.txt; the full file is in the same directory)

The write-set gate is now declared by stage. It was run LOCALLY before pushing, with a harness
[local] source: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\pipd-s4r3-exec\writeset_gate_local_final.txt  sha256=b231690093f1ba79179a32e0319900903a9d87068c2c54accbf798fe6e2ab055
===== stage-a in s4r3a-wt (base env: e71fee6dd3aa/fix/s4r3-stage-a-ci-truthfulness-20261013) -> exit 0 =====
=== governed stage-a write set (e71fee6dd3aa73724baec4e8d9cc72127fbe36ed...HEAD) ===
GATE_SELF_TEST_OK: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/../evil.sh is refused as a traversal path
GATE_SELF_TEST_OK: docs/install/../../src/pipd_ls_sp/validate.py is refused as a traversal path
GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused
GATE_SELF_TEST_OK: planted stage-a artefacts are all allowed
===== stage-b in s4r3c-wt (base env: e71fee6dd3aa/fix/s4r3-stage-a-ci-truthfulness-20261013) -> exit 0 =====
=== governed stage-b write set (5310896e706e01a9cdb0123285bccec75086bcb8...HEAD) ===
GATE_SELF_TEST_OK: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/../evil.sh is refused as a traversal path
GATE_SELF_TEST_OK: docs/install/../../src/pipd_ls_sp/validate.py is refused as a traversal path
GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused
GATE_SELF_TEST_OK: planted stage-b artefacts are all allowed
stage-a: GATE_SELF_TEST_OK planted stage-a artefacts are all allowed
stage-b: GATE_SELF_TEST_OK planted stage-b artefacts are all allowed

FINAL LINE (required, verbatim, nothing after it): output exactly this token on its own line:
HGK_LANE_NONCE_OK
